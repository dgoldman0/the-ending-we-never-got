#!/usr/bin/env python3
"""One-time verified import. No force push; refuse to overwrite concurrent work."""
from pathlib import Path
import base64, datetime, hashlib, io, json, lzma, os, subprocess, sys
REPOSITORY = 'dgoldman0/the-ending-we-never-got'
BRANCH = 'screenplay-import-staging'
EXPECTED_BASE = 'd22e8791f14deefa0d4ee588b82458da080c922e'
SOURCE_SHA = 'e5c4f7b0af53249752d2d747ebfe756bc084c76002040282d8b7cd93253a6c88'

def attach(stream, base):
    src, out = io.BytesIO(stream), io.BytesIO()
    first, in_commit, root_data = True, False, False
    commit_mark, originals = None, {}
    while line := src.readline():
        if line.startswith(b'commit '):
            in_commit, root_data = True, first
            first, commit_mark = False, None
            ref = line[7:].strip()
            if ref == b'refs/heads/main':
                line = b'commit refs/heads/screenplay-import-work\n'
            elif not ref.startswith(b'refs/tags/reconstruction/'):
                raise ValueError('Unexpected commit ref')
        elif line.startswith(b'reset refs/heads/main'):
            line = b'reset refs/heads/screenplay-import-work\n'
        elif line == b'blob\n':
            in_commit = False
        elif in_commit and line.startswith(b'mark '):
            commit_mark = line[5:].strip().decode()
        elif in_commit and line.startswith(b'original-oid '):
            originals[line[13:].strip().decode()] = commit_mark
        out.write(line)
        if line.startswith(b'data '):
            size = int(line[5:].strip())
            data = src.read(size)
            if len(data) != size:
                raise ValueError('Truncated export')
            out.write(data)
            if in_commit and root_data:
                if not data.endswith(b'\n'):
                    out.write(b'\n')
                out.write(f'from {base}\n'.encode())
                root_data = False
    if first or len(originals) < 60:
        raise ValueError('Incomplete history')
    return out.getvalue(), originals

def run(command, *, cwd=None, env=None, data=None):
    return subprocess.run(command, cwd=cwd, env=env, input=data,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode().strip()

def main():
    if os.environ.get('REPOSITORY') != REPOSITORY:
        raise RuntimeError('Unexpected repository')
    staging = Path(__file__).resolve().parents[2]
    inputs = staging / 'screenplay/.import'
    ready = json.loads((inputs/'READY.json').read_text())
    if ready['expected_base'] != EXPECTED_BASE:
        raise RuntimeError('Base mismatch')
    chunks = []
    for part in ready['parts']:
        name = part['name']
        if Path(name).name != name:
            raise ValueError('Unsafe part name')
        raw = (inputs/'parts'/name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != part['sha256']:
            raise ValueError('Part checksum failed: '+name)
        chunks.append(raw)
    compressed = b''.join(chunks)
    if len(compressed) != ready['compressed_bytes'] or hashlib.sha256(compressed).hexdigest() != ready['sha256']:
        raise ValueError('Aggregate checksum failed')
    stream = lzma.decompress(compressed)
    if hashlib.sha256(stream).hexdigest() != ready['export_sha256']:
        raise ValueError('Export checksum failed')
    modified, originals = attach(stream, EXPECTED_BASE)
    auth = base64.b64encode(('x-access-token:'+os.environ['GH_TOKEN']).encode()).decode()
    env = dict(os.environ, GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='http.extraheader',
        GIT_CONFIG_VALUE_0='AUTHORIZATION: basic '+auth, GIT_TERMINAL_PROMPT='0')
    repo = Path.cwd()/'imported-history'
    run(['git','clone','--no-checkout',f'https://github.com/{REPOSITORY}.git',str(repo)],env=env)
    g = lambda *args, **kwargs: run(['git',*args],cwd=repo,env=env,**kwargs)
    if g('rev-parse','origin/main') != EXPECTED_BASE:
        raise RuntimeError('main changed; refusing to overwrite concurrent work')
    if g('tag','--list','reconstruction/*'):
        raise RuntimeError('Reconstruction tags already exist')
    marks = repo.parent/'import.marks'
    g('fast-import','--quiet',f'--export-marks={marks}',data=modified)
    g('checkout','screenplay-import-work')
    g('config','user.name','Screenplay history import')
    g('config','user.email','screenplay-history-import@users.noreply.github.com')
    mark_map = dict(line.split() for line in marks.read_text().splitlines())
    record = {'attached_to':EXPECTED_BASE,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'commit_map':{old:mark_map[mark] for old,mark in originals.items()},
        'note':'Reconstructed commits were attached to the existing initialization commit. Original recovery IDs remain in reconstruction.json.'}
    path = repo/'screenplay/provenance/remote-commit-map.json'
    path.write_text(json.dumps(record,indent=2)+'\n')
    g('add',str(path.relative_to(repo)))
    g('commit','-m','Record reconstructed-history attachment and remote commit mapping')
    g('tag','-d','reconstruction/opening-11')
    g('tag','reconstruction/opening-11')
    if g('ls-tree','--name-only','HEAD') != 'screenplay':
        raise RuntimeError('Unexpected root-level files')
    source = repo/'screenplay/original-timeline/source.fountain'
    if hashlib.sha256(source.read_bytes()).hexdigest() != SOURCE_SHA:
        raise RuntimeError('Current screenplay bytes changed')
    print(run([sys.executable,str(source.parent/'tools/verify.py')],cwd=repo))
    provenance = json.loads((repo/'screenplay/provenance/reconstruction.json').read_text())
    for milestone in provenance['milestones']:
        result = subprocess.run(['git','show',milestone['tag']+':'+milestone['path']],cwd=repo,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
        if hashlib.sha256(result).hexdigest() != milestone['sha256']:
            raise RuntimeError('Historical checkpoint mismatch: '+milestone['tag'])
    g('merge-base','--is-ancestor',EXPECTED_BASE,'HEAD')
    g('fsck','--full')
    refs = g('tag','--list','reconstruction/*').splitlines()
    if len(refs) != 14:
        raise RuntimeError('Expected fourteen milestone tags')
    current = g('ls-remote','origin','refs/heads/main').split()[0]
    if current != EXPECTED_BASE:
        raise RuntimeError('main changed during verification; no push attempted')
    g('push','--atomic','origin','HEAD:refs/heads/main',*[f'refs/tags/{x}:refs/tags/{x}' for x in refs])
    tip = g('rev-parse','HEAD')
    if g('ls-remote','origin','refs/heads/main').split()[0] != tip:
        raise RuntimeError('Remote verification mismatch')
    print(json.dumps({'published':tip,'history_commits':len(g('rev-list','HEAD').splitlines()),
        'milestone_tags':len(refs),'source_sha256':SOURCE_SHA,'root':g('ls-tree','--name-only','HEAD')},indent=2))
    g('push','origin','--delete',BRANCH)
    print('Temporary staging branch removed.')

if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(exc.stderr.decode(errors='replace'),file=sys.stderr)
        raise SystemExit(exc.returncode)
