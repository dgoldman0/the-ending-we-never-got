#!/usr/bin/env python3
"""Validate staging.json and list which planned art is present or awaited.

    python3 visual-novel/tools/check-staging.py            # summary
    python3 visual-novel/tools/check-staging.py --missing  # every awaited file

Errors (exit 1): unknown scenes, override lines that are not source lines,
cast names that never speak in their scene. Missing art is not an error; those
scenes simply stay on the typeset page until their files arrive. New files
need tools/grade-light.py (both light modes) and, for portraits,
tools/portrait-faces.py.
"""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'renpy/game'
EXPRESSIONS = ('speaking', 'listening')


def portrait_key(path):
    """The neutral master a portrait path resolves to (as ui-reading.rpy does)."""
    stem = Path(path).stem
    if path.startswith('art/rovel/portraits/'):
        for suffix in ('-bright', '-night', '-ordinary'):
            if stem.endswith(suffix):
                stem = stem[:-len(suffix)]
                break
        for wardrobe in ('-arrival-cloak', '-arrival', '-formal', '-working'):
            if stem.endswith(wardrobe):
                stem = stem[:-len(wardrobe)]
                break
    return stem


def portrait_files(entry):
    """The planned files for a cast entry; for a list, the first (planned) choice."""
    if isinstance(entry, list):
        return portrait_files(entry[0])
    if isinstance(entry, dict):
        return sorted(set(entry.values()))
    return ['art/portraits/%s-%s.png' % (entry, expression) for expression in EXPRESSIONS]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--missing', action='store_true', help='list every awaited file')
    args = parser.parse_args()

    source = json.loads((GAME / 'source-map.json').read_text())
    staging = json.loads((GAME / 'staging.json').read_text())['scenes']
    errors, stages, portraits = [], {}, {}
    for key, spec in sorted(staging.items(), key=lambda item: int(item[0])):
        number = int(key)
        if not 1 <= number <= len(source['scenes']):
            errors.append('Unknown scene ' + key)
            continue
        blocks = source['scenes'][number - 1]['blocks']
        lines = {block['line'] for block in blocks}
        speakers = {block.get('speaker') for block in blocks if block.get('speaker')}
        for line in spec.get('lines', {}):
            if int(line) not in lines:
                errors.append('S%03d override names line %s, which is not a source line' % (number, line))
        for name, entry in spec.get('cast', {}).items():
            if name not in speakers:
                errors.append('S%03d cast lists %s, who does not speak in the scene' % (number, name))
            for path in portrait_files(entry):
                portraits.setdefault(path, []).append(number)
        for stage in spec.get('stages', []):
            stages.setdefault(stage['image'], []).append(number)

    def present(path):
        return (GAME / path).is_file()

    lit = [key for key, spec in staging.items()
           if any(present(stage['image']) for stage in spec.get('stages', []))]
    print('Staged scenes: %d planned, %d illustrated, %d on the typeset page.'
          % (len(staging), len(lit), len(staging) - len(lit)))
    print('Paintings: %d of %d present.' % (sum(map(present, stages)), len(stages)))
    print('Portraits: %d of %d present.' % (sum(map(present, portraits)), len(portraits)))
    lit_path = GAME / 'lit-assets.json'
    lit = json.loads(lit_path.read_text()) if lit_path.is_file() else {}
    ungraded = [path for path in stages if present(path) and path not in lit.get('images', {})]
    ungraded += [path for path in portraits if present(path)
                 and portrait_key(path) not in lit.get('portraits', {})]
    if ungraded:
        print('Present but not yet graded into the light registers (run tools/grade-light.py):')
        for path in ungraded:
            print('  ' + path)
    if args.missing:
        print('\nAwaited paintings:')
        for path, scenes in sorted(stages.items()):
            if not present(path):
                print('  %s  (S%s)' % (path, ', S'.join('%03d' % n for n in scenes)))
        print('\nAwaited portraits:')
        for path, scenes in sorted(portraits.items()):
            if not present(path):
                print('  %s  (%d scenes)' % (path, len(scenes)))
    if errors:
        print('\n' + '\n'.join(errors))
        sys.exit(1)


if __name__ == '__main__':
    main()
