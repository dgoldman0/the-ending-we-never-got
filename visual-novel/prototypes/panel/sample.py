#!/usr/bin/env python3
"""Capture the reading-panel samples beside the current screen.

Copies the prototype files into the game only for the run, captures four lines
(S002 night, S004 bright, S008 day, S023 night) with the current screen and
with each panel, removes the files again and writes a comparison sheet to
renpy/test-output/review/panel-samples.png.

    python3 visual-novel/prototypes/panel/sample.py
"""
from pathlib import Path
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
VN = HERE.parents[1]
GAME = VN / 'renpy/game'
SHOTS = VN / 'renpy/test-output/panel'
COPIES = {HERE / 'zz-panel-capture.rpy': GAME / 'zz-panel-capture.rpy',
          HERE / 'zz-panel-prototype.rpy': GAME / 'zz-panel-prototype.rpy'}


def run(case, files):
    for src in files:
        shutil.copy(src, COPIES[src])
    try:
        subprocess.run([str(VN / 'tools/run-tests.sh'), case], check=True, stdout=subprocess.DEVNULL)
    finally:
        for src in files:
            COPIES[src].unlink(missing_ok=True)
            COPIES[src].with_suffix('.rpyc').unlink(missing_ok=True)


def main():
    subprocess.run(['python3', str(HERE / 'build-panel.py')], check=True)
    capture, prototype = HERE / 'zz-panel-capture.rpy', HERE / 'zz-panel-prototype.rpy'
    run('panel_current', [capture])
    shutil.copytree(HERE / 'ui', GAME / 'panel', dirs_exist_ok=True)
    try:
        run('panel_samples', [capture, prototype])
    finally:
        shutil.rmtree(GAME / 'panel', ignore_errors=True)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 26)
    scenes = [('s004', 'S004 ceremony (bright)'), ('s002', 'S002 first night (night)'),
              ('s008', 'S008 Bellweir market (ordinary)'), ('s023', 'S023 Valcair and Lucan (night)')]
    cols = [('current', 'Current'), ('lacquer', 'Lacquer panel'), ('vellum', 'Vellum panel')]
    W, H = 960, 540
    sheet = Image.new('RGB', (len(cols) * (W + 10) + 10, len(scenes) * (H + 46) + 10), (16, 16, 16))
    draw = ImageDraw.Draw(sheet)
    for r, (scene, label) in enumerate(scenes):
        for c, (style, name) in enumerate(cols):
            x, y = 10 + c * (W + 10), 10 + r * (H + 46)
            sheet.paste(Image.open(SHOTS / ('%s-%s.png' % (style, scene))).convert('RGB').resize((W, H), Image.LANCZOS), (x, y + 38))
            draw.text((x, y + 4), '%s: %s' % (label, name), fill=(235, 235, 235), font=font)
    out = VN / 'renpy/test-output/review/panel-samples.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print('wrote', out.relative_to(VN))


if __name__ == '__main__':
    main()
