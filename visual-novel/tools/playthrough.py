#!/usr/bin/env python3
"""Play the game without a window and capture every reading page, in order.

The game has to be judged as it is read: one line after another, each over its
picture. This plays the chosen scenes from their first line, captures each
page as the reader sees it (painting, camera framing, shade, portrait, text),
and lays the pages out as contact sheets, so a whole scene, or the whole
game, can be read as a sequence.

    python3 visual-novel/tools/playthrough.py                    # the whole game (about 40 minutes)
    python3 visual-novel/tools/playthrough.py --scenes 16 35     # two scenes
    python3 visual-novel/tools/playthrough.py --scenes 16 --lines 653 700
    python3 visual-novel/tools/playthrough.py --scenes 7 --set persistent.still_frames=True

Pages land in renpy/test-output/playthrough/pages/ as sNNN-LLLL-P.jpg and the
sheets in renpy/test-output/playthrough/sheets/ (both ignored by git).

One Ren'Py session at a time, on four render threads at low priority: the
software renderer is heavy and the machine is in use. The game's saves and
preferences are not touched (the run uses a private copy of the game folder's
links and its own save directory, like tools/run-tests.sh).

The camera is held still for the capture (stage_camera.freeze): each page
shows the framing its line settles on, halfway through its slow push, not a
frame caught mid-move. This is a record for reading, not a quality gate.
"""
from pathlib import Path
import argparse
import os
import re
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

VN = Path(__file__).resolve().parents[1]
GAME = VN / 'renpy/game'
SDK = Path(os.environ.get('RENPY_SDK', VN / '.tools/renpy-8.5.3-sdk'))
OUT = VN / 'renpy/test-output/playthrough'


def story_pages():
    """[(scene, line, page)] in reading order, from the generated story."""
    pages, scene, line = [], 0, 0
    for raw in (GAME / 'story.rpy').read_text().splitlines():
        text = raw.strip()
        for pattern, kind in ((r'\$ current_scene = (\d+)', 'scene'), (r'\$ source_line = (\d+)', 'line'),
                              (r'\$ source_page = (\d+)', 'page')):
            match = re.match(pattern, text)
            if match:
                value = int(match.group(1))
                if kind == 'scene':
                    scene = value
                elif kind == 'line':
                    line = value
                else:
                    pages.append((scene, line, value))
                break
    return pages


def page_name(scene, line, page):
    return 's%03d-%04d-%d' % (scene, line, page)


def capture(pages, out, settings, pause):
    steps = ['testcase playthrough_capture:',
             '    $ _test.timeout = 900.0',
             '    $ _preferences.text_cps = 0',
             "    $ _test.screenshot_directory = 'shots'",
             '    $ stage_camera.freeze = True']
    steps += ['    $ ' + setting for setting in settings]
    steps += ['    pause 1.0', "    click id 'main_begin'", '    pause 0.5']
    current = 1
    for scene, line, page in pages:
        if scene != current and (scene != current + 1 or (scene, line, page) == pages[0]):
            steps += ["    run Jump('s%03d')" % scene, '    pause 0.5']
        current = scene
        steps.append('    advance until eval (current_scene, source_line, source_page) == (%d, %d, %d)' % (scene, line, page))
        steps.append('    pause %.2f' % pause)
        steps.append("    screenshot '%s.png'" % page_name(scene, line, page))
    sandbox = Path(tempfile.mkdtemp(prefix='tenwg-play-'))
    shots = sandbox / 'shots-out'
    shots.mkdir()
    try:
        (sandbox / 'game/saves').mkdir(parents=True)
        (sandbox / 'savedir').mkdir()
        for item in GAME.iterdir():
            if item.name in ('saves', 'cache') or item.suffix in ('.rpyc', '.rpymc'):
                continue
            (sandbox / 'game' / item.name).symlink_to(item)
        (sandbox / 'game/playthrough-capture.rpy').write_text('\n'.join(steps) + '\n')
        (sandbox / 'shots').symlink_to(shots)
        env = dict(os.environ, SDL_AUDIODRIVER='dummy', LP_NUM_THREADS='4')
        log = out / 'run.log'
        with open(log, 'w') as handle:
            result = subprocess.run(
                ['nice', '-n', '19', 'xvfb-run', '-a', '-s', '-screen 0 1920x1080x24', str(SDK / 'renpy.sh'),
                 str(sandbox), '--savedir', str(sandbox / 'savedir'), 'test', 'playthrough_capture',
                 '--overwrite-screenshots'], env=env, stdout=handle, stderr=subprocess.STDOUT)
        for name in ('traceback.txt', 'errors.txt'):
            if (sandbox / name).is_file():
                shutil.copy(sandbox / name, out / name)
                print((sandbox / name).read_text()[-3000:])
        pages_dir = out / 'pages'
        pages_dir.mkdir(parents=True, exist_ok=True)
        done = 0
        for shot in sorted(shots.glob('*.png')):
            Image.open(shot).convert('RGB').save(pages_dir / (shot.stem + '.jpg'), quality=90)
            done += 1
        return result.returncode, done
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)


def sheets(pages, out, columns, rows, tile):
    """Contact sheets, a scene at a time, pages in reading order."""
    sheet_dir = out / 'sheets'
    sheet_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
    height = tile * 9 // 16
    by_scene = {}
    for page in pages:
        by_scene.setdefault(page[0], []).append(page)
    written = 0
    for scene, scene_pages in by_scene.items():
        for old in sheet_dir.glob('s%03d-*.jpg' % scene):
            old.unlink()
        per = columns * rows
        for start in range(0, len(scene_pages), per):
            group = scene_pages[start:start + per]
            sheet = Image.new('RGB', (columns * tile, ((len(group) + columns - 1) // columns) * (height + 20)), (10, 10, 10))
            draw = ImageDraw.Draw(sheet)
            for index, page in enumerate(group):
                path = out / 'pages' / (page_name(*page) + '.jpg')
                x, y = (index % columns) * tile, (index // columns) * (height + 20)
                if path.is_file():
                    sheet.paste(Image.open(path).resize((tile, height), Image.LANCZOS), (x, y))
                draw.text((x + 4, y + height + 2), page_name(*page), fill=(230, 230, 230), font=font)
            sheet.save(sheet_dir / ('s%03d-%02d.jpg' % (scene, start // per + 1)), quality=86)
            written += 1
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--scenes', type=int, nargs='*', help='scene numbers (default: all 58)')
    parser.add_argument('--lines', type=int, nargs=2, metavar=('FIRST', 'LAST'), help='only these source lines')
    parser.add_argument('--set', action='append', default=[], metavar='NAME=VALUE',
                        help='a setting for the run, e.g. persistent.still_frames=True')
    parser.add_argument('--out', type=Path, default=OUT)
    parser.add_argument('--pause', type=float, default=0.5, help='seconds a page is held before its capture')
    parser.add_argument('--sheet', type=int, nargs=3, default=(4, 4, 480), metavar=('COLUMNS', 'ROWS', 'TILE'))
    parser.add_argument('--no-play', action='store_true', help='rebuild the sheets from the last capture')
    args = parser.parse_args()
    pages = story_pages()
    if args.scenes:
        pages = [p for p in pages if p[0] in set(args.scenes)]
    if args.lines:
        pages = [p for p in pages if args.lines[0] <= p[1] <= args.lines[1]]
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if not args.no_play:
        settings = [s.replace('=', ' = ', 1) for s in args.set]
        code, done = capture(pages, out, settings, args.pause)
        print('%d of %d pages captured (exit %d).' % (done, len(pages), code))
    print('%d sheets written to %s' % (sheets(pages, out, *args.sheet), out / 'sheets'))


if __name__ == '__main__':
    main()
