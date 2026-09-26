#!/usr/bin/env python3
"""Validate staging.json and list which planned art is present or awaited.

    python3 visual-novel/tools/check-staging.py            # summary
    python3 visual-novel/tools/check-staging.py --missing  # every awaited file

Errors (exit 1): unknown scenes, stages that start on a line or page the
scene does not have or out of order, override lines that are not source
lines, cast names that never speak in their scene. Missing art is not an error; those
scenes simply stay on the typeset page until their files arrive. New
portraits need tools/crop-portraits.py (GIMP crop to the shared composition),
then every new file needs tools/grade-light.py (both light modes).
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


def painted_name(path, role, scene, plan):
    """The role-specific painted portrait for a plan path (as ui-reading.rpy)."""
    stem = Path(path).stem
    for suffix in ('-bright', '-night', '-ordinary'):
        if stem.endswith(suffix):
            stem = stem[:-len(suffix)]
            break
    wardrobe = None
    for candidate in ('arrival-cloak', 'arrival', 'formal', 'working'):
        if stem.endswith('-' + candidate):
            stem, wardrobe = stem[:-len(candidate) - 1], candidate
            break
    mood = plan['aliases'].get(stem, stem)
    if wardrobe is None:
        wardrobe = plan['wardrobe'].get(stem.split('-')[0], {}).get(str(scene))
    return '-'.join(part for part in (mood, wardrobe, 'speaking' if role == 'speaker' else 'listening') if part)


def painted_plan():
    """{batch: {name: [(scene, line, role)]}} for the painted portraits released in batches."""
    import runpy
    plan = json.loads((GAME / 'portrait-plan.json').read_text())
    beats = runpy.run_path(str(ROOT / 'tools/check-rovel-plan.py'), run_name='painted_plan')['load_plan']()['ROVEL_BEATS']
    uses = {}
    for (scene, line, _page), beat in sorted(beats.items()):
        for role in ('speaker', 'listener'):
            face = beat.get(role)
            if face:
                uses.setdefault(painted_name(face['image'], role, scene, plan), []).append((scene, line, role))
    batches = {}
    for batch in plan['batches']:
        names = {name: use for name, use in uses.items() if use[0][0] in batch['scenes']}
        names.update({name: [] for name in batch.get('also', [])})
        names.update({'%s-%s' % (s, role): [] for s in batch.get('sets', []) for role in ('speaking', 'listening')})
        batches[batch['batch']] = names
    return batches


def story_pages():
    """{(scene, source line): number of pages} as story.rpy reads them."""
    counts, scene, line = {}, 0, 0
    for text in (GAME / 'story.rpy').read_text().splitlines():
        text = text.strip()
        if text.startswith('label s') and text.endswith(':'):
            scene = int(text[7:-1])
        elif text.startswith('$ source_line = '):
            line = int(text.split('= ')[1])
        elif text.startswith('$ source_page = '):
            counts[scene, line] = int(text.split('= ')[1]) + 1
    return counts


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
    page_counts = story_pages()
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
        previous = (-1, 0)
        for stage in spec.get('stages', []):
            stages.setdefault(stage['image'], []).append(number)
            start = (stage.get('from', 0), stage.get('page', 0))
            if start[0] and start[0] not in lines:
                errors.append('S%03d stage %s starts on line %d, which is not a source line'
                              % (number, stage['image'], start[0]))
            elif start[0] and start[1] >= page_counts.get((number, start[0]), 1):
                errors.append('S%03d stage %s starts on page %d of line %d, which has %d'
                              % (number, stage['image'], start[1], start[0], page_counts.get((number, start[0]), 1)))
            if start <= previous:
                errors.append('S%03d stage %s is out of order' % (number, stage['image']))
            previous = start

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
    batches = painted_plan()
    total = sum(len(names) for names in batches.values())
    have = sum(present('art/portraits/%s.png' % name) for names in batches.values() for name in names)
    print('Painted portraits released in batches: %d of %d present (%s).' % (have, total, ', '.join(
        'batch %d: %d/%d' % (b, sum(present('art/portraits/%s.png' % n) for n in names), len(names))
        for b, names in sorted(batches.items()))))
    if args.missing:
        print('\nAwaited painted portraits, by batch:')
        for b, names in sorted(batches.items()):
            for name in sorted(names):
                if not present('art/portraits/%s.png' % name):
                    print('  batch %d  art/portraits/%s.png' % (b, name))
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
