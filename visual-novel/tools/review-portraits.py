#!/usr/bin/env python3
"""Put new portraits into the game and lay out every line they appear on.

For each delivered batch this does the whole mechanical part of the check:
  1. crops every portrait in GIMP (tools/crop-portraits.py) and grades it into
     every light register (tools/grade-light.py --portraits --force);
  2. plays the game headless through every S001-S005 exchange that has
     portraits, plus each painted character's first line in every later
     scene, and captures each at 1920x1080;
  3. assembles contact sheets in renpy/test-output/portrait-review/: each tile
     is the portrait pair with its line, labelled with scene, line and files;
     and scene sheets (scenes-NN.png): the full screen at the first line under
     each scene painting and key moment;
  4. lays out, for every character with a portrait painted since the last
     review, all of that character's crops with the new ones marked, beside
     Tessa's likeness reference where it applies (identity-<name>.png), so a
     new set is compared with itself and with the sets already in the game.

The judgment stays with the reviewer: open the sheets, then full screens.

    python3 visual-novel/tools/review-portraits.py              # everything
    python3 visual-novel/tools/review-portraits.py --scenes 3   # S003 only
    python3 visual-novel/tools/review-portraits.py --no-crop    # art unchanged
    python3 visual-novel/tools/review-portraits.py --all        # identity sheets for every portrait
    python3 visual-novel/tools/review-portraits.py --no-crop --no-play   # sheets from the last run
"""
from pathlib import Path
import argparse
import json
import runpy
import subprocess

from PIL import Image, ImageDraw

VN = Path(__file__).resolve().parents[1]
GAME = VN / 'renpy/game'
OUT = VN / 'renpy/test-output/portrait-review'
TEST = GAME / 'review-portraits.rpy'
STAGE_BOX = (96, 736, 1640, 1012)          # both windows and the whole line
PAGE_BOXES = ((20, 240, 270, 520), (1690, 284, 1860, 472))
STAMP = OUT / 'reviewed.json'              # source mtimes at the last review
REFERENCES = {'tessa': VN / 'art/character-references/tessa/north-infirmary-face.png'}


def plan_lines(scenes):
    """[(scene, line, mode, label, page)] in reading order. mode is 'stage' (a
    line over a painting), 'page' (a line on the typeset book page) or 'scene'
    (the first line under each painting or key moment, kept as a full screen);
    page is the page of the line's paragraph (a stage can start partway)."""
    beats = runpy.run_path(str(VN / 'tools/check-rovel-plan.py'), run_name='review')['load_plan']()['ROVEL_BEATS']
    lines = []
    for (scene, line, page), beat in sorted(beats.items()):
        if page == 0 and beat.get('speaker') and (not scenes or scene in scenes):
            faces = [beat[r]['expression'] for r in ('speaker', 'listener') if beat.get(r)]
            lines.append((scene, line, 'stage', ' / '.join(faces), 0))
    staging = json.loads((GAME / 'staging.json').read_text())['scenes']
    source = json.loads((GAME / 'source-map.json').read_text())
    present = {p.stem for p in (GAME / 'art/portraits').glob('*.png')}
    for key, spec in sorted(staging.items(), key=lambda kv: int(kv[0])):
        number = int(key)
        if scenes and number not in scenes:
            continue
        blocks = source['scenes'][number - 1]['blocks']
        painted_stages = [st for st in spec.get('stages', []) if (GAME / st['image']).is_file()]
        mode = 'stage' if painted_stages else 'page'
        for st in painted_stages:
            first = next((b for b in blocks if b['line'] >= st.get('from', 0)), None)
            if first:
                page = st.get('page', 0) if first['line'] == st.get('from') else 0
                lines.append((number, first['line'], 'scene', Path(st['image']).stem, page))
        sets = set()
        for entry in spec['cast'].values():
            for candidate in (entry if isinstance(entry, list) else [entry]):
                if isinstance(candidate, str):
                    sets.add(candidate)
        painted = {s for s in sets if s + '-speaking' in present}
        if not painted:
            continue
        seen = set()
        for block in source['scenes'][number - 1]['blocks']:
            who = block.get('speaker')
            entry = spec['cast'].get(who)
            names = entry if isinstance(entry, list) else [entry]
            if who and who not in seen and any(isinstance(n, str) and n in painted for n in names):
                seen.add(who)
                lines.append((number, block['line'], mode, who.title(), 0))
    # one capture per line and page, in reading order
    unique = {}
    for entry in lines:
        unique.setdefault((entry[0], entry[1], entry[4]), entry)
    return sorted(unique.values(), key=lambda e: (e[0], e[1], e[4]))


def shot_name(scene, line, page):
    return 's%03d-%03d%s.png' % (scene, line, '-p%d' % page if page else '')


def write_test(lines):
    steps = ['# Generated by tools/review-portraits.py for portrait review; not a quality gate.',
             'testcase portrait_review:',
             '    $ _test.timeout = 240.0',
             '    $ _preferences.text_cps = 0',
             "    $ _test.screenshot_directory = 'test-output/portrait-review/shots'",
             "    run Preference('display', 'fullscreen')",
             '    pause 1.0',
             "    click id 'main_begin'"]
    current = 1
    for scene, line, _mode, _label, page in lines:
        if scene > current + 1 or scene < current:
            steps.append("    run Jump('s%03d')" % scene)
            steps.append('    pause 0.5')
        current = scene
        steps.append('    advance until eval (current_scene, source_line, source_page) == (%d, %d, %d)' % (scene, line, page))
        steps.append('    pause 0.8')
        steps.append("    screenshot '%s'" % shot_name(scene, line, page))
    TEST.write_text('\n'.join(steps) + '\n')


def contact_sheets(lines):
    shots = OUT / 'shots'
    tiles = []
    for scene, line, mode, label, page in lines:
        path = shots / shot_name(scene, line, page)
        if not path.is_file() or mode == 'scene':
            continue
        shot = Image.open(path).convert('RGB')
        if mode == 'page':
            parts = [shot.crop(box) for box in PAGE_BOXES]
            tile = Image.new('RGB', (sum(p.width for p in parts) + 20, max(p.height for p in parts)), (30, 30, 30))
            x = 0
            for part in parts:
                tile.paste(part, (x, 0)); x += part.width + 20
        else:
            tile = shot.crop(STAGE_BOX)
        tile.thumbnail((700, 300), Image.LANCZOS)
        framed = Image.new('RGB', (700, tile.height + 26), (22, 22, 22))
        framed.paste(tile, (0, 0))
        ImageDraw.Draw(framed).text((6, tile.height + 7), 'S%03d line %d  %s' % (scene, line, label), fill=(235, 235, 235))
        tiles.append(framed)
    per_sheet = 12
    for n in range(0, len(tiles), per_sheet):
        group = tiles[n:n + per_sheet]
        rows = (len(group) + 1) // 2
        h = max(t.height for t in group)
        sheet = Image.new('RGB', (2 * 710 + 10, rows * (h + 10) + 10), (12, 12, 12))
        for i, t in enumerate(group):
            sheet.paste(t, (10 + (i % 2) * 710, 10 + (i // 2) * (h + 10)))
        target = OUT / ('sheet-%02d.png' % (n // per_sheet + 1))
        sheet.save(target)
        print('wrote', target.relative_to(VN))


def scene_sheets(lines):
    """Full screens at the start of each painting and key moment, four to a
    sheet, labelled, for judging the painting under the interface."""
    shots = OUT / 'shots'
    for old in OUT.glob('scenes-*.png'):
        old.unlink()
    tiles = []
    for scene, line, mode, label, page in lines:
        path = shots / shot_name(scene, line, page)
        if mode == 'scene' and path.is_file():
            shot = Image.open(path).convert('RGB').resize((960, 540), Image.LANCZOS)
            framed = Image.new('RGB', (960, 566), (22, 22, 22))
            framed.paste(shot, (0, 0))
            where = 'S%03d line %d%s' % (scene, line, ', page %d' % (page + 1) if page else '')
            ImageDraw.Draw(framed).text((6, 547), '%s  %s' % (where, label), fill=(235, 235, 235))
            tiles.append(framed)
    for n in range(0, len(tiles), 4):
        group = tiles[n:n + 4]
        sheet = Image.new('RGB', (2 * 970 + 10, ((len(group) + 1) // 2) * 576 + 10), (12, 12, 12))
        for i, t in enumerate(group):
            sheet.paste(t, (10 + (i % 2) * 970, 10 + (i // 2) * 576))
        target = OUT / ('scenes-%02d.png' % (n // 4 + 1))
        sheet.save(target)
        print('wrote', target.relative_to(VN))


def identity_sheets(everything):
    """Crops of the portraits painted since the last review, one sheet per character."""
    stamp = json.loads(STAMP.read_text()) if STAMP.is_file() else {}
    sources = {p.stem: p.stat().st_mtime for p in (GAME / 'art/portraits').glob('*.png')}
    fresh = {n for n, t in sources.items() if everything or stamp.get(n) != t}
    groups = {}
    for name in sorted(sources):
        groups.setdefault(name.split('-')[0], []).append(name)
    # a character with anything new is shown whole, new files marked, so a
    # new set is compared with the ones already in the game
    groups = {who: names for who, names in groups.items() if fresh & set(names)}
    for old in OUT.glob('identity-*.png'):
        old.unlink()
    W, H, per_row = 340, 388, 6
    for who, names in groups.items():
        tiles = [(p.name, Image.open(p)) for p in [REFERENCES.get(who)] if p]
        crops = [GAME / 'art/cast' / (n + '.png') for n in names]
        tiles += [(('NEW ' if c.stem in fresh else '') + c.stem, Image.open(c)) for c in crops if c.is_file()]
        rows = (len(tiles) + per_row - 1) // per_row
        sheet = Image.new('RGB', (per_row * (W + 8) + 8, rows * (H + 30) + 8), (20, 20, 20))
        draw = ImageDraw.Draw(sheet)
        for i, (label, im) in enumerate(tiles):
            im = im.convert('RGB')
            im.thumbnail((W, H), Image.LANCZOS)
            x, y = 8 + (i % per_row) * (W + 8), 8 + (i // per_row) * (H + 30)
            sheet.paste(im, (x, y))
            draw.text((x + 4, y + H + 8), label, fill=(230, 230, 230))
        target = OUT / ('identity-%s.png' % who)
        sheet.save(target)
        print('wrote', target.relative_to(VN))
    STAMP.write_text(json.dumps(sources, indent=1) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scenes', type=int, nargs='*', help='only these scene numbers')
    parser.add_argument('--no-crop', action='store_true', help='skip cropping and grading')
    parser.add_argument('--all', action='store_true', help='identity sheets for every portrait, not just new ones')
    parser.add_argument('--no-play', action='store_true', help='rebuild the sheets from the last screenshots')
    args = parser.parse_args()
    if not args.no_crop:
        subprocess.run(['python3', str(VN / 'tools/crop-portraits.py')], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(['python3', str(VN / 'tools/grade-light.py'), '--portraits'], check=True)
    lines = plan_lines(set(args.scenes or []))
    OUT.mkdir(parents=True, exist_ok=True)
    if not args.no_play:
        for old in (OUT / 'shots').glob('*.png') if (OUT / 'shots').is_dir() else []:
            old.unlink()
        write_test(lines)
        try:
            subprocess.run([str(VN / 'tools/run-tests.sh'), 'portrait_review'], check=True, stdout=subprocess.DEVNULL)
        finally:
            TEST.unlink(missing_ok=True)
            (GAME / 'review-portraits.rpyc').unlink(missing_ok=True)
    contact_sheets(lines)
    scene_sheets(lines)
    identity_sheets(args.all)
    print('%d lines captured.' % len(lines))


if __name__ == '__main__':
    main()
