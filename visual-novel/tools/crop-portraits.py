#!/usr/bin/env python3
"""Crop every dialogue portrait from its source painting, in GIMP.

Portraits are rectangular crops of the paintings, not cut-outs: the painted
ground stays, so there are no mattes, fringes or sticker edges. Every crop
follows one composition, so faces share a scale and an eye line:

  - painted busts: the face is 46% of the crop's height; the head is centred
    on its silhouette at eye level, a little behind centre for gaze room, with
    5% headroom above the hair, so hair, collar and shoulders show;
  - the old bare heads are framed tighter (face 62%, top at 21%, 4% gaze
    room) because nothing below the neck was painted;
  - the lower edge crosses the neck above any damage in the painting;
  - the crop's shape matches the portrait window's interior.

GIMP then works on each crop (from a Script-Fu file generated in a temporary folder):
  the Senn, Mara, Iven and supporting-cast sheets are generator cut-outs with
  transparent grounds (the black and brown seen in some viewers is hidden
  pixel data), so their stair-stepped matte is pulled in a pixel and softened,
  dropping the black and red fringe, and a dark painted ground goes beneath;
  Tessa's sheet is an opaque painting, so her grey studio ground is taken
  down toward the others; GPT's transparent busts get the same ground; every
  crop gets the same soft vignette. Layered masters go to art/portrait-masters/<name>.xcf,
  flattened crops to renpy/game/art/cast/<name>.png, replacing a file only
  when its pixels changed, and the facing of each
  head to renpy/game/portrait-crops.json (the game mirrors a portrait so the
  speaker faces the listener).

    python3 visual-novel/tools/crop-portraits.py
    python3 visual-novel/tools/grade-light.py --portraits

New portraits in renpy/game/art/portraits/ are picked up automatically: their
face is detected, and "-speaking" files face right, "-listening" files left.
"""
from pathlib import Path
import json
import shutil
import subprocess
import tempfile

import cv2
import numpy as np
from PIL import Image

VN = Path(__file__).resolve().parents[1]
GAME = VN / 'renpy/game'
RAW = VN / 'art/rovel/raw'
MASTERS = VN / 'art/portrait-masters'
OUT = GAME / 'art/cast'
DATA = GAME / 'portrait-crops.json'

ASPECT = 204 / 233          # portrait window interior, width / height
OUT_SIZE = (408, 466)       # twice the speaker window's interior
# The old bare-head paintings are framed tight (there is nothing below the
# neck); painted busts show hair, collar and shoulders.
FACE_FRAC, FACE_TOP, GAZE_ROOM = 0.62, 0.21, 0.04
BUST_FRAC, BUST_HEADROOM, BUST_GAZE = 0.46, 0.05, 0.03

# Heads cut from the S001-S005 expression sheets: sheet, cell (x, y, w, h),
# face box in the cell's 640 px master scale (verified in play), facing, ground.
SHEET_HEADS = {
    'tessa-startled': ('tessa-expressions-v1', (0, 0, 627, 627), (54, 181, 358), 'left', 'grey'),
    'tessa-resolute': ('tessa-expressions-v1', (627, 0, 627, 627), (64, 208, 335), 'left', 'grey'),
    'tessa-wounded': ('tessa-expressions-v1', (0, 627, 627, 627), (55, 191, 350), 'left', 'grey'),
    'tessa-listening': ('tessa-expressions-v1', (627, 627, 627, 627), (60, 201, 340), 'left', 'grey'),
    'senn-assuring': ('senn-expressions-v1', (0, 0, 627, 836), (160, 120, 360), 'right', 'cutout'),
    'senn-listening': ('senn-expressions-v1', (627, 0, 627, 836), (159, 122, 349), 'right', 'cutout'),
    'senn-evasive': ('senn-expressions-v1', (1254, 0, 627, 836), (154, 124, 352), 'right', 'cutout'),
    'mara-controlled': ('mara-expressions-v1', (0, 0, 887, 887), (260, 131, 331), 'right', 'cutout'),
    'mara-uneasy': ('mara-expressions-v1', (887, 0, 887, 887), (260, 136, 329), 'right', 'cutout'),
    'iven-attentive': ('iven-expressions-v1', (0, 0, 887, 887), (60, 139, 356), 'left', 'cutout'),
    'iven-concerned': ('iven-expressions-v1', (887, 0, 887, 887), (60, 185, 341), 'left', 'cutout'),
    'olan': ('supporting-cast-v1', (0, 0, 512, 512), (46, 129, 318), 'left', 'cutout'),
    'priest': ('supporting-cast-v1', (512, 0, 512, 512), (250, 150, 312), 'right', 'cutout'),
    'mother': ('supporting-cast-v1', (1024, 0, 512, 512), (112, 156, 312), 'left', 'cutout'),
    'petitioner': ('supporting-cast-v1', (0, 512, 512, 512), (300, 90, 330), 'right', 'cutout'),
    'orra': ('supporting-cast-v1', (512, 512, 512, 512), (56, 109, 318), 'left', 'cutout'),
    'messenger': ('supporting-cast-v1', (1024, 512, 512, 512), (270, 109, 350), 'right', 'cutout'),
}


def neck_end(sheet, cell, face):
    """The lowest row of the painted neck under the face, from the sheet's alpha."""
    cx, cy, cw, ch = cell
    fx, fy, fs, _ = face
    alpha = np.asarray(Image.open(RAW / (sheet + '.png')).getchannel('A'))[cy:cy + ch, cx:cx + cw]
    x0, x1 = int(fx - cx + fs * 0.3), int(fx - cx + fs * 0.7)
    rows = np.where((alpha[:, x0:x1] > 128).sum(axis=1) > (x1 - x0) * 0.25)[0]
    return cy + int(rows.max())


def detect_face(path):
    """Largest face on a grey ground, for a new transparent bust. Tries the
    frontal detector, then looser settings, then the profile detector in both
    directions (strongly turned three-quarter views defeat the frontal one)."""
    image = Image.open(path).convert('RGBA')
    ground = Image.new('RGBA', image.size, (128, 128, 128, 255))
    ground.alpha_composite(image)
    grey = cv2.equalizeHist(cv2.cvtColor(np.array(ground.convert('RGB')), cv2.COLOR_RGB2GRAY))
    minimum = (min(image.size) // 8,) * 2
    width = grey.shape[1]
    attempts = [('haarcascade_frontalface_alt2.xml', 4, False), ('haarcascade_frontalface_alt2.xml', 2, False),
                ('haarcascade_frontalface_default.xml', 4, False), ('haarcascade_profileface.xml', 3, False),
                ('haarcascade_profileface.xml', 3, True)]
    for cascade, neighbours, flipped in attempts:
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + cascade)
        faces = detector.detectMultiScale(cv2.flip(grey, 1) if flipped else grey, 1.05, neighbours, minSize=minimum)
        if len(faces):
            x, y, w, h = max(faces, key=lambda f: f[2])
            if flipped:
                x = width - x - w
            return int(x), int(y), int(w)
    raise SystemExit('No face found in %s; add it to FACE_OVERRIDES' % path)


# Face boxes [x, y, size] measured by hand where the detectors frame a
# different part of the head than they do for the rest of a character's set.
FACE_OVERRIDES = {
    # the profile fallback boxes his whole head and beard; this is his face,
    # on the scale of his other two portraits
    'senn-assuring-speaking': (544, 335, 410),
}


def bust_box(path, face, facing):
    """A painted bust is framed on its silhouette, not the face box: in a
    three-quarter view the face sits off the skull's centre, so centring the
    face shoves the head against the back edge. The head is centred at eye
    level (a little behind centre, for gaze room) and the top of the hair gets
    a fixed headroom; the face box only sets the scale."""
    fx, fy, fs = face
    alpha = np.asarray(Image.open(path).convert('RGBA').getchannel('A'), np.float32) / 255
    h_img, w_img = alpha.shape
    eyes = alpha[int(fy + 0.3 * fs):int(fy + 0.6 * fs)]
    cols = np.where(eyes.max(axis=0) > 0.5)[0]
    left, right = (cols.min(), cols.max()) if len(cols) else (fx, fx + fs)
    height = min(fs / BUST_FRAC, h_img)
    width = height * ASPECT
    centre = 0.5 + (BUST_GAZE if facing == 'left' else -BUST_GAZE)
    x = (left + right) / 2.0 - centre * width
    x = min(max(x, 0), w_img - width)
    band = alpha[:, int(max(0, x)):int(min(w_img, x + width))]
    rows = np.where(band.max(axis=1) > 0.5)[0]
    top = rows.min() if len(rows) else fy - 0.3 * fs
    y = min(max(top - BUST_HEADROOM * height, 0), h_img - height)
    return int(round(x)), int(round(y)), int(round(width)), int(round(height))


def crop_box(face, bounds):
    """The composition rule for the old bare heads, clamped inside the source."""
    fx, fy, fs, facing = face
    frac, top, gaze = FACE_FRAC, FACE_TOP, GAZE_ROOM
    bx0, by0, bx1, by1 = bounds
    height = fs / frac
    height = min(height, (by1 - fy) / (1 - top), by1 - by0)   # keep the foot inside
    width = height * ASPECT
    if width > bx1 - bx0:
        width = bx1 - bx0
        height = width / ASPECT
    centre = 0.5 + (gaze if facing == 'left' else -gaze)
    x = fx + fs / 2 - centre * width
    y = fy - top * height
    x = min(max(x, bx0), bx1 - width)
    y = min(max(y, by0), by1 - height)
    return int(round(x)), int(round(y)), int(round(width)), int(round(height))


def plan():
    jobs = []
    for name, (sheet, (cx, cy, cw, ch), (mx, my, ms), facing, ground) in SHEET_HEADS.items():
        k = max(cw, ch) / 640.0                     # master scale back to the sheet
        face = (cx + mx * k, cy + my * k, ms * k, facing)
        # the usable area ends above the painted neck's lumpy generated base
        foot = cy + ch - 0.02 * ch
        if ground == 'cutout':
            foot = min(foot, neck_end(sheet, (cx, cy, cw, ch), face) - 0.06 * face[2])
        jobs.append(dict(name=name, source=str(RAW / (sheet + '.png')), facing=facing, ground=ground,
                         box=crop_box(face, (cx, cy, cx + cw, foot))))
    for path in sorted((GAME / 'art/portraits').glob('*.png')):
        facing = 'left' if path.stem.endswith('-listening') else 'right'
        fx, fy, fs = FACE_OVERRIDES.get(path.stem) or detect_face(path)
        w, h = Image.open(path).size
        jobs.append(dict(name=path.stem, source=str(path), facing=facing, ground='bust',
                         box=bust_box(path, (fx, fy, fs), facing)))
    return jobs


def ground_seeds(job):
    """Points on the crop's border that are certainly ground, in output pixels."""
    if job['ground'] != 'grey':
        return []
    x, y, w, h = job['box']
    crop = Image.open(job['source']).convert('RGB').crop((x, y, x + w, y + h)).resize(OUT_SIZE, Image.LANCZOS)
    a = np.asarray(crop).astype(int)
    spread = a.max(axis=2) - a.min(axis=2)
    ok = (spread < 10) & (a.mean(axis=2) > 80) & (a.mean(axis=2) < 140)
    W, H = OUT_SIZE
    candidates = [(i, 2) for i in range(4, W - 4, 12)] + [(2, j) for j in range(4, int(H * 0.8), 12)] + \
                 [(W - 3, j) for j in range(4, int(H * 0.8), 12)]
    seeds = [(cx, cy) for cx, cy in candidates if ok[max(0, cy - 2):cy + 3, max(0, cx - 2):cx + 3].all()]
    return [v for point in seeds[::3] for v in point]


def scm_string(text):
    return '"' + text.replace('\\', '\\\\').replace('"', '\\"') + '"'


def write_script(jobs, out, masters, script):
    lines = ['; Generated by tools/crop-portraits.py. Run through GIMP 2.10 batch mode.',
             '(load ' + scm_string(str(VN / 'tools/crop-portraits-lib.scm')) + ')',
             '(define (crop-all)']
    for job in jobs:
        x, y, w, h = job['box']
        seeds = ' '.join(str(v) for v in ground_seeds(job))
        lines.append("  (crop-portrait %s %s %s %d %d %d %d %d %d %s '(%s))" % (
            scm_string(job['source']), scm_string(str(out / (job['name'] + '.png'))),
            scm_string(str(masters / (job['name'] + '.xcf'))), x, y, w, h, OUT_SIZE[0], OUT_SIZE[1],
            scm_string(job['ground']), seeds))
    lines.append(')')
    script.write_text('\n'.join(lines) + '\n')


def same_pixels(a, b):
    """GIMP's painted ground varies by a level or two between runs."""
    one, two = Image.open(a).convert('RGBA'), Image.open(b).convert('RGBA')
    return one.size == two.size and np.abs(np.asarray(one, int) - np.asarray(two, int)).max() <= 3


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    MASTERS.mkdir(parents=True, exist_ok=True)
    jobs = plan()
    # GIMP renders into a scratch folder; only crops whose pixels changed
    # replace the files in the game, so an unchanged portrait keeps its file,
    # its master and its date (grade-light.py regrades by date).
    with tempfile.TemporaryDirectory() as scratch:
        scratch = Path(scratch)
        script = scratch / 'crop-all.scm'
        write_script(jobs, scratch, scratch, script)
        # Script-Fu batch commands do not share definitions: load and run in one.
        subprocess.run(['gimp-console-2.10', '-i', '-d', '-f',
                        '-b', '(begin (load %s) (crop-all))' % scm_string(str(script)),
                        '-b', '(gimp-quit 0)'], check=True)
        for job in jobs:
            fresh, current = scratch / (job['name'] + '.png'), OUT / (job['name'] + '.png')
            if current.is_file() and (MASTERS / (job['name'] + '.xcf')).is_file() and same_pixels(fresh, current):
                continue
            shutil.move(str(fresh), current)
            shutil.move(str(scratch / (job['name'] + '.xcf')), MASTERS / (job['name'] + '.xcf'))
            print('new crop', job['name'])
    DATA.write_text(json.dumps({
        '_note': 'Written by tools/crop-portraits.py: which way each cropped head faces, and its '
                 'crop box in the source painting. The game mirrors a portrait so the speaker '
                 'faces the listener.',
        'facing': {job['name']: job['facing'] for job in jobs},
        'boxes': {job['name']: job['box'] for job in jobs}}, indent=1) + '\n')
    for job in jobs:
        print('%-24s %-11s box %s' % (job['name'], job['ground'], job['box']))


if __name__ == '__main__':
    main()
