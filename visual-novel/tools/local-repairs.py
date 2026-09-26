#!/usr/bin/env python3
"""Local corrections to finished paintings, each kept as a layered GIMP master.

Repairs found in the S001-S005 sweep of 24 September 2026, done locally
instead of re-requesting the paintings:

  sliver    a stray metal sliver the image generator left on Tessa's drawing
            (S002), painted out from the surrounding paper by inpainting; the
            close-up of the drawing was since repainted by GPT (25 September),
            so only the table painting keeps this repair
  recolour  Iven's coat, changed from olive to brown because green is the
            northern side's colour (user decision): the S003 paintings and
            close-ups, his ten portraits, and the two S004 ceremony paintings
            (khaki); the coat is cut out by a segmentation mask. The S005
            window paintings get back GPT's own brown.

and from the sweep of every painting of 26 September 2026:

  letter    lettering the image generator garbled: the old strokes are
            painted out from the paper around them, and the new text is set
            flat in a font, warped onto the card's corners and laid on as ink
            (the S058 catalog card read "SUMMOKING BOOK")
  skin      the coverlet's lace weave the generator printed onto Olan's
            cleared forearm (S003 purification paintings and the close-up):
            the fine pattern is taken out of the skin, its shading and the
            healer's red morning mark are kept
  ears      Lucan's ears came out pointed, like an elf's, in two S029
            paintings; his design gives him human ears. The pointed tip is
            covered with the hair just above it, so the ear's top reads round
            under his hair
  hair      Tessa's hair in the three S005 window paintings (GPT's repaints
            share one figure) came out a saturated copper red; the same day
            in S004, and in her likeness reference, it is chestnut. Its colour
            is moved to the S004 hair's, keeping its own light and strands
  star      northern badges painted as an undivided star: the vertical
            split of the northern emblem is drawn through the star's most
            vertical point, in the cloth's own dark (found on Lucan's, Serat's,
            a captain's and Vask's badges in ten paintings)
  recolour  (again) Iven's coat in four S003 paintings, re-masked from
            hand-placed points: the first masks missed a front panel and a
            sleeve and ran onto the apron as mauve blotches

Each repair works on the copy the game grades from (renpy/game/art/base/, or
the portrait source in renpy/game/art/portraits/); the untouched original is
kept in art/local-repairs/originals/. The sliver repair also has a layered
GIMP master (art/local-repairs/stray-sliver/); a coat recolour is reproduced
from its original, its mask (art/local-repairs/masks/) and this script. Then
run tools/crop-portraits.py and tools/grade-light.py.

Coat masks come from the Segment Anything model (facebook/sam-vit-large)
prompted with the points below; they are cached in art/local-repairs/masks/.
Making them needs torch and transformers (the local tools venv):

    visual-novel/.tools/depth-venv/bin/python visual-novel/tools/local-repairs.py --segment
    python3 visual-novel/tools/local-repairs.py            # apply every repair
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile

import cv2
import numpy as np
from PIL import Image

VN = Path(__file__).resolve().parents[1]
GAME = VN / 'renpy/game'
HERE = VN / 'art/local-repairs'
ORIGINALS = HERE / 'originals'
MASKS = HERE / 'masks'
WRITTEN = HERE / 'written.json'          # the files this tool last wrote into GPT's paintings

# The stray sliver on the S002 drawing: a thin diagonal strip from p0 to p1.
SLIVERS = {
    'art/base/opening/cg/drawing-restart.png': ((941, 744), (964, 768)),
    # the same sliver on the first drawing; its pen tip sits a little lower,
    # so the strip starts just past the tip and the pen still meets the paper
    'art/base/opening/cg/drawing-letter.png': ((949, 753), (966, 770)),
    # S035 crossing: a second, thinner scabbard shaft splits off Lucan's
    # below the hilt (sweep of 26 September); it is filled with the trouser
    # cloth 16 px to its left rather than inpainted from the brass beside it
    'art/scenes/s035-harrow-bridge-crossing.png': ((586, 610), (568, 735), (-16, 0)),
}

# Iven's coat, recoloured from olive to brown (user decision, 24 September
# 2026: green is the northern side's colour). Each entry: the image (the
# base copy the game grades from, or a portrait source), and either a box
# around Iven with seed points on the coat (Segment Anything is prompted with
# the box and with points it picks inside it: olive-brown pixels as coat,
# bright or skin-toned ones as not; only mask patches touching a seed are
# kept, which drops the grey-green blanket), or hand-placed points on and off
# the coat. Portraits are prompted from the lower part of the bust.
COATS = {
    'ward-entrance': dict(path='art/base/opening/cg/ward-entrance.png', box=(1090, 270, 1360, 600), hand=dict(
        pos=[(1180, 330), (1150, 480), (1230, 420), (1320, 350), (1325, 420)],
        neg=[(1270, 390), (1255, 320), (1300, 470), (1265, 265), (1380, 380), (1300, 560), (1240, 505)])),
    'ward-assessment': dict(path='art/base/rovel/cg/ward-assessment.png', box=(60, 150, 720, 700), hand=dict(
        pos=[(250, 330), (330, 250), (150, 560), (180, 440), (600, 300), (610, 420)],
        neg=[(510, 380), (500, 650), (430, 620), (540, 200), (430, 560), (720, 540), (220, 660), (640, 90), (700, 300), (700, 150)])),
    'blue-healing': dict(path='art/base/opening/cg/blue-healing.png', box=(65, 222, 627, 940), seeds=[(209, 418), (561, 391), (156, 783)]),
    'ward-standing-unlit': dict(path='art/base/opening/cg/ward-standing-unlit.png', box=(483, 261, 979, 940), seeds=[(561, 391), (627, 653), (561, 836), (901, 418), (927, 574)], extra=[((500, 560, 590, 941), [(540, 760)])]),
    'ward-standing-light': dict(path='art/base/opening/cg/ward-standing-light.png', box=(483, 261, 979, 940), seeds=[(561, 391), (627, 653), (561, 836), (901, 418), (927, 574)], extra=[((500, 560, 590, 941), [(540, 760)])]),
    'first-purification': dict(path='art/base/opening/cg/first-purification.png', box=(431, 248, 888, 836), seeds=[(627, 431), (836, 457), (849, 600)], extra=[((610, 330, 690, 560), [(650, 440)])]),
    'last-patch': dict(path='art/base/opening/cg/last-patch.png', box=(535, 248, 953, 875), seeds=[(653, 444), (875, 457), (901, 600)]),
    'purification-cleared': dict(path='art/base/opening/cg/purification-cleared.png', box=(587, 222, 979, 796), seeds=[(653, 444), (901, 457), (927, 600)]),
    'treatment-pause': dict(path='art/base/opening/cg/treatment-pause.png', box=(540, 230, 960, 620), hand=dict(
        pos=[(640, 290), (860, 330), (900, 430), (930, 520)],
        neg=[(720, 420), (700, 560), (720, 300), (740, 520), (600, 400), (840, 690), (720, 240)])),
    'after-first-treatment': dict(path='art/base/opening/cg/after-first-treatment.png', box=(620, 130, 880, 660), hand=dict(
        pos=[(690, 250), (670, 450), (700, 600), (740, 320), (805, 300)],
        neg=[(765, 450), (760, 600), (745, 180), (830, 390), (860, 250), (740, 100)])),
    'rested-hand': dict(path='art/base/opening/cg/rested-hand.png', box=(0, 0, 115, 320), seeds=[(40, 80), (60, 200)]),
    'treatment-blue': dict(path='art/base/rovel/details/treatment-blue.png',
                           pos=[(100, 40), (140, 90), (80, 70), (150, 30)],
                           neg=[(20, 60), (30, 150), (120, 150), (200, 130), (210, 60), (250, 20)]),
    'treatment-white': dict(path='art/base/rovel/details/treatment-white.png',
                            pos=[(160, 15), (430, 30), (480, 60), (400, 70)],
                            neg=[(240, 50), (90, 40), (350, 140), (560, 30), (600, 80), (200, 120)]),
    'ceremony-intervention': dict(path='art/base/rovel/cg/ceremony-intervention.png',
                                  pos=[(600, 345), (570, 445), (560, 520), (625, 420), (590, 300)],
                                  neg=[(650, 520), (560, 645), (625, 580), (620, 230), (650, 455), (640, 435), (700, 370)]),
    'ceremony-yield': dict(path='art/base/rovel/cg/ceremony-yield.png',
                           pos=[(660, 321), (614, 407), (586, 492), (717, 378), (580, 350)],
                           neg=[(523, 492), (717, 492), (688, 583), (671, 213), (728, 458), (722, 429), (762, 321), (574, 652)]),
    # S008 market (a GPT painting): his coat came out khaki, greener than
    # his brown in the paintings on either side (sweep of 26 September).
    's008-bellweir-market': dict(path='art/scenes/s008-bellweir-market.png', box=(110, 260, 320, 560), hand=dict(
        pos=[(150, 330), (160, 400), (270, 320), (275, 380), (285, 511), (141, 505)],
        neg=[(204, 311), (215, 395), (204, 474), (250, 460), (215, 250), (135, 442), (285, 442)])),
}
for _name in ('iven-attentive-speaking', 'iven-attentive-listening', 'iven-concerned-speaking',
              'iven-concerned-listening', 'iven-attentive-treatment-speaking', 'iven-attentive-treatment-listening',
              'iven-concerned-treatment-speaking', 'iven-concerned-treatment-listening',
              'iven-harrow-speaking', 'iven-harrow-listening'):
    COATS[_name] = dict(path='art/portraits/%s.png' % _name, portrait=True)

# The brown: Iven's coat as GPT painted it in the S005 window paintings (and
# from S006 on), measured over its mask as mean and spread of OpenCV 8-bit Lab.
BROWN = {'mean': np.array([44.1, 137.4, 137.1], np.float32), 'std': np.array([36.3, 4.3, 4.4], np.float32)}

# The S005 window paintings are simply given back GPT's own brown.
RESTORE = ['art/base/rovel/cg/window-packing.png', 'art/base/rovel/cg/window-pause.png',
           'art/base/rovel/cg/window-together.png']

# Lettering to reset: the card's corners (clockwise from top left), boxes on
# the card to leave alone (image pixels), the title and how many lines of
# handwriting follow it, all laid out on a flat 600x400 card.
LETTERING = {
    'art/scenes/s058-bellweir-market-spring.png': dict(
        quad=((961.7, 630.0), (1053.3, 619.2), (1088.3, 683.3), (993.3, 692.5)),
        keep=[(1033, 651, 1080, 688), (1011, 612, 1035, 634)],     # the little book drawing; Elin's thumb
        title='Summoning Book', title_box=(40, 70, 560, 140), lines=((45, 200, 330), (45, 245, 300), (45, 290, 250))),
}
INK = np.array([62, 50, 42], np.float32)

# Skin that took on a pattern from the cloth beside it: the forearm (a box
# and points for Segment Anything), boxes to leave alone (the healer's red
# morning mark) and boxes around the corruption's own dark marks, whose small
# pieces must not be taken for the pattern's dots. (The last-patch painting
# has only a trace of the pattern, and smoothing took its natural skin
# detail with it, so it is left alone.)
SKIN = {
    'art/base/rovel/details/treatment-white.png': dict(
        box=(220, 135, 505, 230), pos=[(300, 185), (380, 180), (460, 185)],
        neg=[(200, 205), (340, 125), (300, 245), (540, 160)], keep=[(430, 140, 475, 222)]),
    'art/base/opening/cg/purification-cleared.png': dict(
        box=(640, 570, 980, 690), pos=[(720, 630), (820, 625), (900, 630)],
        neg=[(600, 640), (800, 575), (800, 705), (1000, 600)], keep=[(915, 575, 962, 655)]),
    'art/base/opening/cg/first-purification.png': dict(
        box=(640, 570, 980, 690), pos=[(720, 630), (800, 640), (940, 630)],
        neg=[(600, 640), (800, 575), (800, 705), (1000, 600)], keep=[(915, 575, 962, 655)],
        marks=[(835, 580, 925, 665)]),
}


# Hair to bring to another painting's colour: prompts for Segment Anything,
# and the colour it takes, measured over Tessa's hair in S004 ceremony-refusal
# (OpenCV 8-bit Lab mean and spread).
CHESTNUT = {'mean': np.array([71.2, 140.3, 142.7], np.float32), 'std': np.array([46.8, 4.1, 6.0], np.float32)}
HAIR = {
    path: dict(box=(310, 110, 520, 340), pos=[(410, 150), (350, 230), (470, 200)],
               neg=[(415, 230), (415, 300), (400, 335), (300, 150), (530, 150), (412, 190)])
    for path in ('art/base/rovel/cg/window-packing.png', 'art/base/rovel/cg/window-pause.png',
                 'art/base/rovel/cg/window-together.png')
}

# Northern badges without the emblem's vertical split: a box around each star.
STARS = {
    'art/scenes/s010-bellweir-hills.png': [(1255, 300, 1300, 345)],
    'art/scenes/s026-quarry-loading-ramp.png': [(806, 302, 854, 348)],
    'art/scenes/s027-river-camp-gate.png': [(869, 259, 919, 309), (1035, 303, 1060, 328)],
    'art/scenes/s028-river-camp-infirmary.png': [(562, 182, 612, 232), (737, 182, 793, 232)],
    'art/scenes/s029-barge.png': [(449, 414, 486, 451)],
    'art/scenes/s029-launch.png': [(794, 374, 846, 424)],
    'art/scenes/s029-quarry-refusal.png': [(700, 380, 725, 407)],
    'art/scenes/s029-river-camps-visits.png': [(399, 384, 451, 436)],
    'art/scenes/s047-citadel-north-infirmary-before-dawn.png': [(684, 270, 724, 312)],
    'art/scenes/s057-citadel-lower-gate.png': [(1359, 299, 1411, 341), (1514, 256, 1566, 298)],
}

# Pointed ear tips to cover with hair: the area to cover (a polygon whose
# lower edge is the new, round top of the ear; only the lit skin inside it
# changes) and the offset of the hair copied over it (from above).
EARS = {
    'art/scenes/s029-river-camps-visits.png': dict(
        poly=[(340, 200), (398, 200), (398, 236), (390, 238), (382, 239), (375, 242), (369, 247),
              (365, 254), (363, 262), (340, 262)], offset=(0, 34)),
    'art/scenes/s029-barge.png': dict(
        poly=[(415, 210), (475, 210), (475, 247), (466, 249), (457, 250), (449, 254), (443, 260),
              (439, 268), (437, 278), (415, 278)], offset=(0, 38)),
}


def original(path):
    """The file as it was before any local repair (saved on first use)."""
    keep = ORIGINALS / path.replace('/', '--')
    if not keep.is_file():
        keep.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(GAME / path, keep)
    return np.asarray(Image.open(keep))


def write(path, pixels):
    """Save a repair. For a base copy, the top-level copy beside it (no longer
    shown since the Intense grade was retired) is kept identical."""
    Image.fromarray(pixels).save(GAME / path)
    if path.startswith('art/base/'):
        Image.fromarray(pixels).save(GAME / path.replace('art/base/', 'art/', 1))


def remove_sliver(rgb, p0, p1, clone=None):
    """Inpaint the sliver: pixels near the segment that are far darker or
    paler than the paper and pencil around them. With `clone` (an offset),
    they are filled from the image that far away instead."""
    h, w = rgb.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    (x0, y0), (x1, y1) = p0, p1
    t = np.clip(((xx - x0) * (x1 - x0) + (yy - y0) * (y1 - y0)) / ((x1 - x0) ** 2 + (y1 - y0) ** 2), -0.15, 1.15)
    dist = np.hypot(xx - (x0 + t * (x1 - x0)), yy - (y0 + t * (y1 - y0)))
    band = dist < 6
    lum = rgb.astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32)
    ring = (dist >= 7) & (dist < 14)
    paper = np.median(lum[ring])
    odd = band & ((lum < paper * 0.55) | (lum > paper + 22))
    mask = cv2.dilate(odd.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=2)
    mask &= band.astype(np.uint8) | cv2.dilate(band.astype(np.uint8), np.ones((3, 3), np.uint8))
    if clone:
        dx, dy = clone
        src = cv2.warpAffine(rgb, np.float32([[1, 0, -dx], [0, 1, -dy]]), (w, h), borderMode=cv2.BORDER_REFLECT)
        soft = cv2.GaussianBlur(cv2.dilate(mask, np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 0.9)
        out = rgb.astype(np.float32) * (1 - soft[..., None]) + src.astype(np.float32) * soft[..., None]
        return np.clip(out + 0.5, 0, 255).astype(np.uint8), soft
    out = cv2.inpaint(rgb, mask * 255, 4, cv2.INPAINT_TELEA)
    noise = np.random.default_rng(5).normal(0, 2.2, rgb.shape[:2]).astype(np.float32)
    soft = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 0.8)
    out = np.clip(out.astype(np.float32) + (noise * soft)[..., None], 0, 255).astype(np.uint8)
    return out, soft


def clean_mask(prob, seeds=None):
    """Threshold, keep the patches touching a seed (or, without seeds, all but
    specks), fill pinholes, and feather by a pixel."""
    m = (prob > 0.5).astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    big = stats[1:, cv2.CC_STAT_AREA].max() if n > 1 else 0
    wanted = {labels[y, x] for x, y in seeds or []} - {0}
    for i in range(1, n):
        if (i in wanted) if seeds else stats[i, cv2.CC_STAT_AREA] >= 0.02 * big:
            keep[labels == i] = 1
    keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    return cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 1.0)


def coat_gate(rgb):
    """1 where a pixel can belong to the coat, 0 where it is plainly
    something else: pale cloth (apron, shirt, bedding), skin or the blue of
    a dress. With hand-placed points the model already follows the coat's
    outline; this only drops what it takes in by mistake. (A tighter gate
    by hue was tried and rejected: the coat's own warm folds fail it.)"""
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    ok = ~((L > 150) | (a > 140) | (b < 126))
    return cv2.morphologyEx(ok.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)).astype(np.float32)


def off_coat(prob, gate, area=150):
    """0-1 over the parts of a coat mask that are something else: patches of
    at least `area` pixels the gate rejects (apron, shirt, skin). Smaller
    rejected specks are dark folds of the coat itself and stay in."""
    off = ((prob > 0.5) & (gate < 0.5)).astype(np.uint8)
    off = cv2.morphologyEx(off, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, labels, stats, _ = cv2.connectedComponentsWithStats(off, 8)
    keep = np.isin(labels, [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] >= area])
    keep = cv2.dilate(keep.astype(np.uint8), np.ones((5, 5), np.uint8))
    return cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 1.2)


def lab_stats(rgb, mask):
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    sel = lab[mask > 0.9]
    return sel.mean(0), sel.std(0)


def recolour(rgb, mask, target):
    """Move the coat's colour to the target while keeping its own light, folds
    and weave: a and b take the target's mean and spread; L keeps its texture
    and moves a third of the way toward the target's brightness, so a coat in
    a bright hall stays light."""
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    mean, std = lab_stats(rgb, mask)
    new = lab.copy()
    for c in (1, 2):
        k = np.clip(target['std'][c] / max(std[c], 1e-3), 0.6, 1.3)
        new[..., c] = target['mean'][c] + (lab[..., c] - mean[c]) * k
    new[..., 0] = lab[..., 0] + (target['mean'][0] - mean[0]) * 0.35
    full = cv2.cvtColor(np.clip(new, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
    out = rgb.astype(np.float32) * (1 - mask[..., None]) + full.astype(np.float32) * mask[..., None]
    return np.clip(out + 0.5, 0, 255).astype(np.uint8)


def reletter(rgb, spec):
    """Paint out a card's garbled lettering and set new lettering in its
    perspective. Returns the new image and the changed area (0-1)."""
    from PIL import ImageDraw, ImageFont
    h, w = rgb.shape[:2]
    quad = np.float32(spec['quad'])
    H = cv2.getPerspectiveTransform(np.float32([(0, 0), (600, 0), (600, 400), (0, 400)]), quad)
    card = np.zeros((h, w), np.uint8)
    cv2.fillConvexPoly(card, np.int32(np.round(quad)), 1)
    card = cv2.erode(card, np.ones((7, 7), np.uint8))
    for x0, y0, x1, y1 in spec['keep']:
        card[y0:y1, x0:x1] = 0
    lum = rgb.astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32)
    paper = np.median(lum[card > 0])
    ink = (card > 0) & (lum < paper - 30)
    mask = cv2.dilate(ink.astype(np.uint8), np.ones((3, 3), np.uint8)) & card
    clean = cv2.inpaint(rgb, mask * 255, 3, cv2.INPAINT_TELEA)
    grain = np.random.default_rng(7).normal(0, 2.0, (h, w)).astype(np.float32)
    clean = np.clip(clean.astype(np.float32) + (grain * mask)[..., None], 0, 255)
    # the new lettering, drawn flat, then warped into the card's perspective
    # at four times the image's resolution and averaged down, so thin pen
    # strokes stay whole
    layer = Image.new('L', (600, 400), 0)
    draw = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = spec['title_box']
    face = str(GAME / 'fonts/EBGaramond12-Regular.ttf')
    size = 90
    while draw.textlength(spec['title'].upper(), font=ImageFont.truetype(face, size)) > x1 - x0 and size > 10:
        size -= 2
    draw.text((x0, y1), spec['title'].upper(), font=ImageFont.truetype(face, size), fill=255, anchor='ls',
              stroke_width=1, stroke_fill=255)
    rng = np.random.default_rng(11)
    for lx0, ly, lx1 in spec['lines']:       # a line of small joined-up handwriting
        x = lx0
        while x < lx1 - 20:
            end = min(x + int(rng.integers(30, 80)), lx1)
            t = np.arange(0, end - x, 0.5)
            r, k = rng.uniform(3.5, 5.5), rng.uniform(0.7, 0.95)
            xs = x + t + r * 0.6 * np.sin(t * k)
            ys = ly - r - r * np.cos(t * k) * rng.uniform(0.7, 1.0) - 1.5 * np.sin(t * 0.13)
            draw.line(list(zip(xs, ys)), fill=150, width=3, joint='curve')
            x = end + int(rng.integers(14, 24))
    scale = 4
    S = np.diag([scale, scale, 1.0]) @ H
    big = cv2.warpPerspective(np.asarray(layer, np.float32) / 255, S, (w * scale, h * scale), flags=cv2.INTER_LINEAR)
    alpha = cv2.resize(big, (w, h), interpolation=cv2.INTER_AREA)
    alpha = cv2.GaussianBlur(alpha, (0, 0), 0.4) * (cv2.dilate(card, np.ones((5, 5), np.uint8)) > 0)
    alpha = np.clip(alpha * 1.25, 0, 0.92)
    out = clean * (1 - alpha[..., None]) + INK * alpha[..., None]
    changed = np.clip(np.maximum(mask.astype(np.float32), alpha * 4), 0, 1)
    return np.clip(out + 0.5, 0, 255).astype(np.uint8), changed


def smooth_skin(rgb, mask, keep, marks=()):
    """Take a fine printed pattern out of skin: inside the mask, the detail
    finer than a few pixels is mostly removed (strong dark marks such as the
    corruption's veins stay), a faint grain is put back, and the boxes in
    `keep` are left as they were."""
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    m = mask.astype(np.float32)
    for x0, y0, x1, y1 in keep:
        m[y0:y1, x0:x1] = 0
    m = cv2.GaussianBlur(m, (0, 0), 1.5) * (mask > 0.5)
    weight = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 3.5) + 1e-4
    out = lab.copy()
    for c, sigma, amount in ((0, 3.5, 0.85), (1, 3.0, 0.8), (2, 3.0, 0.8)):
        low = cv2.GaussianBlur(lab[..., c] * mask, (0, 0), sigma) / weight
        residual = lab[..., c] - low
        gentle = np.clip(1 - (np.abs(residual) - 18) / 10, 0, 1) if c == 0 else 1.0
        out[..., c] = lab[..., c] - residual * amount * m * gentle
    grain = cv2.GaussianBlur(np.random.default_rng(9).normal(0, 1, m.shape).astype(np.float32), (0, 0), 0.7)
    out[..., 0] += grain * 2.2 * m
    result = cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
    # The pattern's evenly spaced dots survive as dark specks; paint them out,
    # but not near larger dark marks (the corruption's veins and patches).
    L = cv2.cvtColor(result, cv2.COLOR_RGB2LAB)[..., 0].astype(np.float32)
    dark = ((L - cv2.medianBlur(L.astype(np.uint8), 7).astype(np.float32)) < -9).astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(dark, 8)
    area = stats[:, cv2.CC_STAT_AREA]
    big = np.isin(labels, np.nonzero(area > 60)[0][1:] if n > 1 else [])
    near_big = cv2.dilate(big.astype(np.uint8), np.ones((25, 25), np.uint8)) > 0
    specks = np.isin(labels, np.nonzero(area <= 25)[0]) & (labels > 0) & (m > 0.3) & ~near_big
    for x0, y0, x1, y1 in marks:
        specks[y0:y1, x0:x1] = False
    specks = cv2.dilate(specks.astype(np.uint8), np.ones((3, 3), np.uint8))
    return cv2.inpaint(result, specks * 255, 2, cv2.INPAINT_TELEA)


def match_hair(rgb, mask, target):
    """Give hair the target's colour (a and b: mean and spread) while its
    lightness keeps its own strands and shine."""
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    mean, std = lab_stats(rgb, mask)
    new = lab.copy()
    for c in (1, 2):
        new[..., c] = target['mean'][c] + (lab[..., c] - mean[c]) * target['std'][c] / max(std[c], 1e-3)
    # lightness: the target's mean, and a little of the gap in contrast
    new[..., 0] = target['mean'][0] + (lab[..., 0] - mean[0]) * 0.85
    full = cv2.cvtColor(np.clip(new, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
    out = rgb.astype(np.float32) * (1 - mask[..., None]) + full.astype(np.float32) * mask[..., None]
    return np.clip(out + 0.5, 0, 255).astype(np.uint8)



def fit_star(rgb, box):
    """Centre, axis angle (degrees from vertical) and half-length of the most
    vertical principal point of a bright star inside box."""
    x0, y0, x1, y1 = box
    crop = rgb[y0:y1, x0:x1].astype(np.float32)
    L = crop @ np.array([0.299, 0.587, 0.114], np.float32)
    bg = np.percentile(L, 40)
    w = np.clip((L - bg - 25) / 40, 0, 1)
    w = w * (cv2.GaussianBlur(w, (0, 0), 2) > 0.15)
    n, labels, stats, cents = cv2.connectedComponentsWithStats((w > 0.3).astype(np.uint8), 8)
    if n <= 1:
        return None
    big = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    w = w * (cv2.dilate((labels == big).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0)
    ys, xs = np.nonzero(w > 0.05)
    ww = w[ys, xs]
    cx, cy = (xs * ww).sum() / ww.sum(), (ys * ww).sum() / ww.sum()
    best = None
    for ang in np.arange(-30, 30.5, 1.0):
        t = np.radians(ang)
        dx, dy = np.sin(t), -np.cos(t)
        score, reach = 0.0, 0.0
        for sgn in (1, -1):
            for r in np.arange(1, 40, 0.5):
                px, py = cx + sgn * r * dx, cy + sgn * r * dy
                if not (0 <= px < w.shape[1] - 1 and 0 <= py < w.shape[0] - 1):
                    break
                v = cv2.getRectSubPix(w, (1, 1), (px, py))[0, 0]
                if v < 0.25:
                    break
                score += v
                reach = max(reach, r) if sgn == 1 else reach
        if best is None or score > best[0]:
            best = (score, ang)
    ang = best[1]
    t = np.radians(ang)
    ext = []
    for sgn in (1, -1):
        r_end = 0
        for r in np.arange(1, 40, 0.5):
            px, py = cx + sgn * r * np.sin(t), cy - sgn * r * np.cos(t)
            if not (0 <= px < w.shape[1] - 1 and 0 <= py < w.shape[0] - 1):
                break
            if cv2.getRectSubPix(w, (1, 1), (px, py))[0, 0] < 0.2:
                break
            r_end = r
        ext.append(r_end)
    return (x0 + cx, y0 + cy, ang, ext[0], ext[1], bg)

def split(rgb, star, width=1.4, scale=8):
    """Draw the split: a thin line of the cloth's own dark along the axis,
    from 1 px short of each tip."""
    cx, cy, ang, up, down, bg = star
    h, w = rgb.shape[:2]
    t = np.radians(ang)
    x0, y0 = int(cx) - 45, int(cy) - 45
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(w, x0 + 90), min(h, y0 + 90)
    patch = rgb[y0:y1, x0:x1].astype(np.float32)
    L = patch @ np.array([0.299, 0.587, 0.114], np.float32)
    dark = patch[L <= np.percentile(L, 25)].mean(0)
    big = np.zeros(((y1 - y0) * scale, (x1 - x0) * scale), np.uint8)
    a = ((cx - x0 + (up - 0.8) * np.sin(t)) * scale, (cy - y0 - (up - 0.8) * np.cos(t)) * scale)
    b = ((cx - x0 - (down - 0.8) * np.sin(t)) * scale, (cy - y0 + (down - 0.8) * np.cos(t)) * scale)
    cv2.line(big, tuple(int(round(v)) for v in a), tuple(int(round(v)) for v in b), 255, max(1, int(round(width * scale))), cv2.LINE_AA)
    alpha = cv2.resize(big.astype(np.float32) / 255, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA)[..., None]
    out = rgb.copy().astype(np.float32)
    out[y0:y1, x0:x1] = patch * (1 - alpha) + dark * alpha
    return np.clip(out + 0.5, 0, 255).astype(np.uint8), alpha


def cover_tip(rgb, poly, offset, feather=1.6):
    """Copy the hair above over the lit skin inside the polygon, with soft
    edges. Returns the new image and the changed area (0-1)."""
    h, w = rgb.shape[:2]
    area = np.zeros((h, w), np.uint8)
    cv2.fillPoly(area, [np.int32(poly)], 1)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    skin = cv2.dilate((lab[..., 0] > 70).astype(np.uint8), np.ones((5, 5), np.uint8))
    m = cv2.GaussianBlur((area & skin).astype(np.float32), (0, 0), feather)
    dx, dy = offset
    src = cv2.warpAffine(rgb, np.float32([[1, 0, dx], [0, 1, dy]]), (w, h), borderMode=cv2.BORDER_REFLECT)
    out = rgb.astype(np.float32) * (1 - m[..., None]) + src.astype(np.float32) * m[..., None]
    return np.clip(out + 0.5, 0, 255).astype(np.uint8), m


def _sha(path):
    return hashlib.sha256((GAME / path).read_bytes()).hexdigest()


def guarded_write(path, after):
    """Write a repair into one of GPT's paintings only over the file it was
    made from, or over this tool's own last output (recorded in WRITTEN). If
    the painting was since redelivered, say so and leave it."""
    written = json.loads(WRITTEN.read_text()) if WRITTEN.is_file() else {}
    current = np.asarray(Image.open(GAME / path))
    keep = np.asarray(Image.open(ORIGINALS / path.replace('/', '--')))
    ours = written.get(path) == _sha(path)
    if ours or (current.shape == keep.shape and np.array_equal(current, keep)):
        write(path, after)
        written[path] = _sha(path)
        WRITTEN.write_text(json.dumps(written, indent=1, sort_keys=True) + '\n')
        return True
    print('SKIPPED, the painting changed since this tool last wrote it; review it:', path)
    return False


def save_master(name, path, before, layer_rgb, alpha, after):
    """A GIMP master: the original, and the repair as a layer over it
    (layer_rgb shown through alpha). Checked by flattening it again in GIMP
    and comparing with the result."""
    folder = HERE / name
    folder.mkdir(parents=True, exist_ok=True)
    xcf = folder / (Path(path).stem + '.xcf')
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        Image.fromarray(before).save(tmp / 'original.png')
        layer = np.dstack([layer_rgb, (np.clip(alpha, 0, 1) * 255 + 0.5).astype(np.uint8)])
        Image.fromarray(layer).save(tmp / 'repair.png')
        check = tmp / 'check.png'
        script = ('(let* ((img (car (gimp-file-load RUN-NONINTERACTIVE "%s" "%s")))'
                  ' (base (car (gimp-image-get-active-layer img)))'
                  ' (fix (car (gimp-file-load-layer RUN-NONINTERACTIVE img "%s"))))'
                  ' (gimp-item-set-name base "Original, as delivered")'
                  ' (gimp-image-insert-layer img fix 0 -1)'
                  ' (gimp-layer-set-composite-space fix LAYER-COLOR-SPACE-RGB-PERCEPTUAL)'
                  ' (gimp-layer-set-blend-space fix LAYER-COLOR-SPACE-RGB-PERCEPTUAL)'
                  ' (gimp-item-set-name fix "Local repair: %s")'
                  ' (gimp-xcf-save 0 img fix "%s" "%s")'
                  ' (let ((flat (car (gimp-image-duplicate img))))'
                  '  (gimp-image-flatten flat)'
                  '  (file-png-save RUN-NONINTERACTIVE flat (car (gimp-image-get-active-drawable flat)) "%s" "%s" 0 9 0 0 0 0 0))'
                  ' (gimp-image-delete img))') % (tmp / 'original.png', tmp / 'original.png', tmp / 'repair.png',
                                                  name, xcf, xcf, check, check)
        subprocess.run(['gimp-console-2.10', '-i', '-d', '-f', '-b', script, '-b', '(gimp-quit 0)'],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        flat = np.asarray(Image.open(check).convert('RGB')).astype(int)
        worst = np.abs(flat - after.astype(int)).max()
        assert worst <= 2, (xcf, worst)
    return xcf


def auto_points(rgb, box):
    """Points inside the box for Segment Anything: olive-to-brown cloth as coat,
    bright or skin-toned pixels as not, spread out by k-means."""
    x0, y0, x1, y1 = box
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(int)[y0:y1, x0:x1]
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    coat = (a <= 134) & (b >= 128) & (b <= 160) & (L > 18) & (L < 120) & (a < b)
    other = (L > 170) | ((a > 140) & (L > 60))
    rng = np.random.default_rng(1)
    found = []
    for region, n in ((coat, 8), (other, 6)):
        pts = []
        ys, xs = np.nonzero(cv2.erode(region.astype(np.uint8), np.ones((9, 9), np.uint8)))
        if len(xs):
            idx = rng.choice(len(xs), min(n * 40, len(xs)), replace=False)
            cand = np.stack([xs[idx], ys[idx]], 1).astype(np.float32)
            k = min(n, len(cand))
            _, _, centres = cv2.kmeans(cand, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0),
                                       3, cv2.KMEANS_PP_CENTERS)
            for c in centres:
                q = cand[((cand - c) ** 2).sum(1).argmin()]
                pts.append((int(q[0]) + x0, int(q[1]) + y0))
        found.append(pts)
    return found


def segment(names=None):
    run = sam_runner()
    MASKS.mkdir(parents=True, exist_ok=True)
    for name, spec in COATS.items():
        if names and name not in names:
            continue
        mask = coat_mask(run, name, spec)
        Image.fromarray((mask * 255 + 0.5).astype(np.uint8)).save(MASKS / (name + '.png'))
        print('mask', name)
    for path, spec in HAIR.items():
        name = 'hair--' + Path(path).stem
        if names and name not in names:
            continue
        rgb = original(path)[..., :3].copy()
        mask = clean_mask(run(rgb, spec['pos'], spec['neg'], spec['box']), spec['pos'])
        Image.fromarray((mask * 255 + 0.5).astype(np.uint8)).save(MASKS / (name + '.png'))
        print('mask', name)
    for path, spec in SKIN.items():
        name = 'skin--' + Path(path).stem
        if names and name not in names:
            continue
        rgb = original(path)[..., :3].copy()
        prob = run(rgb, spec['pos'], spec['neg'], spec['box'])
        mask = clean_mask(prob, spec['pos'])
        Image.fromarray((mask * 255 + 0.5).astype(np.uint8)).save(MASKS / (name + '.png'))
        print('mask', name)


def sam_runner():
    """run(rgb, positive points, negative points, box=None) -> probability."""
    import torch
    from transformers import SamModel
    model = SamModel.from_pretrained('facebook/sam-vit-large').eval()
    if torch.cuda.is_available():
        model = model.cuda()
    device = next(model.parameters()).device

    def run(rgb, pos, neg, box=None):
        h, w = rgb.shape[:2]
        s = 1024 / max(w, h)
        nw, nh = int(round(w * s)), int(round(h * s))
        a = (np.asarray(Image.fromarray(rgb).resize((nw, nh), Image.BILINEAR), np.float32)
             - [123.675, 116.28, 103.53]) / [58.395, 57.12, 57.375]
        pad = np.zeros((1024, 1024, 3), np.float32)
        pad[:nh, :nw] = a
        x = torch.from_numpy(pad.transpose(2, 0, 1)[None].astype(np.float32)).to(device)
        kw = dict(input_points=torch.tensor([[[(px * s, py * s) for px, py in pos + neg]]], dtype=torch.float32).to(device),
                  input_labels=torch.tensor([[[1] * len(pos) + [0] * len(neg)]]).to(device))
        if box:
            kw['input_boxes'] = torch.tensor([[[v * s for v in box]]], dtype=torch.float32).to(device)
        with torch.no_grad():
            out = model(image_embeddings=model.get_image_embeddings(x), multimask_output=True, **kw)
        m = out.pred_masks[0, 0][int(out.iou_scores[0, 0].argmax())][None, None]
        m = torch.nn.functional.interpolate(m, (1024, 1024), mode='bilinear')[..., :nh, :nw]
        m = torch.nn.functional.interpolate(m, (h, w), mode='bilinear')[0, 0]
        return torch.sigmoid(m).cpu().numpy()

    return run


def coat_mask(run, name, spec):
    """The coat's mask (0-1) in one image, from the prompts in COATS."""
    pixels = original(spec['path'])
    rgb = pixels[..., :3].copy()
    if 'hand' in spec:
        # Hand-placed points on and off the coat, within a box (the sweep
        # of 26 September found the automatic points had landed on the
        # apron's shadows in two S003 paintings and missed a front panel
        # and a sleeve in two others).
        prob = run(rgb, spec['hand']['pos'], spec['hand']['neg'], spec.get('box'))
        for box, pos, neg in spec['hand'].get('extra', []):
            prob = np.maximum(prob, run(rgb, pos, neg, box))
        prob = prob * (1 - off_coat(prob, coat_gate(rgb)))
        seeds = list(spec['hand']['pos']) + [q for _, pos, _ in spec['hand'].get('extra', []) for q in pos]
    elif spec.get('portrait'):
        h, w = rgb.shape[:2]
        alpha = pixels[..., 3] if pixels.shape[2] == 4 else np.full((h, w), 255)
        rgb[alpha < 128] = 128                      # a neutral ground for the model
        box = (0, int(h * 0.45), w, h)
        pos, neg = auto_points(rgb, box)
        prob = run(rgb, pos, neg, box) * (alpha / 255.0)
        seeds = pos
    elif 'box' in spec:
        pos, neg = auto_points(rgb, spec['box'])
        prob = run(rgb, pos + list(spec['seeds']), neg, spec['box'])
        seeds = list(spec['seeds'])
        # a panel the first box misses (hanging behind a hand, or a lapel
        # beside Tessa) gets its own box; the masks are combined
        for box, more in spec.get('extra', []):
            p2, n2 = auto_points(rgb, box)
            prob = np.maximum(prob, run(rgb, p2 + list(more), n2, box))
            seeds += list(more)
        # The S003 coat is dark olive cloth: nothing pale (apron, shirt),
        # skin-toned (faces, hands) or blue (Tessa's dress) belongs to it.
        lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
        gate = (lab[..., 0] < 128) & (lab[..., 1] < 140) & (lab[..., 2] > 127)
        gate = cv2.morphologyEx(gate.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        for x0, y0, x1, y1 in spec.get('exclude', []):
            gate[y0:y1, x0:x1] = 0
        prob = prob * cv2.GaussianBlur(gate.astype(np.float32), (0, 0), 1.0)
    else:
        prob = run(rgb, spec['pos'], spec['neg'])
        seeds = None
    return clean_mask(prob, seeds)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--adopt', nargs='+', metavar='PATH',
                        help='record these files (paths under renpy/game/) as this tool\'s own output, after review')
    parser.add_argument('--segment', nargs='*', metavar='NAME',
                        help='make the coat masks, or only the named ones (needs torch, transformers)')
    args = parser.parse_args()
    if args.adopt:
        written = json.loads(WRITTEN.read_text()) if WRITTEN.is_file() else {}
        for path in args.adopt:
            written[path] = _sha(path)
        WRITTEN.write_text(json.dumps(written, indent=1, sort_keys=True) + '\n')
        return
    if args.segment is not None:
        segment(args.segment)
        return
    for path, (p0, p1, *clone) in SLIVERS.items():
        pixels = original(path)
        before = pixels[..., :3]
        after, _ = remove_sliver(before, p0, p1, clone[0] if clone else None)
        changed = (after != before).any(axis=2).astype(np.float32)
        full = np.dstack([after, pixels[..., 3]]) if pixels.shape[2] == 4 else after
        if path.startswith('art/scenes/'):                # a GPT painting, which may be redelivered
            if not guarded_write(path, full):
                continue
        else:
            write(path, full)
        xcf = save_master('stray-sliver', path, before, after, changed, after)
        print('sliver removed:', path, '(%d px) ->' % changed.sum(), xcf.relative_to(VN))
    for path, spec in LETTERING.items():
        pixels = original(path)
        rgb, changed = reletter(pixels[..., :3], spec)
        after = np.dstack([rgb, pixels[..., 3]]) if pixels.shape[2] == 4 else rgb
        if guarded_write(path, after):
            changed = (rgb != pixels[..., :3]).any(axis=2).astype(np.float32)
            xcf = save_master('lettering', path, pixels[..., :3], rgb, changed, rgb)
            print('lettering reset:', path, '->', xcf.relative_to(VN))
    for path in HAIR:
        pixels = original(path)
        mask = np.asarray(Image.open(MASKS / ('hair--' + Path(path).stem + '.png'))).astype(np.float32) / 255
        rgb = match_hair(pixels[..., :3], mask, CHESTNUT)
        write(path, np.dstack([rgb, pixels[..., 3]]) if pixels.shape[2] == 4 else rgb)
        print('hair colour matched:', path)
    for path, spec in EARS.items():
        if path in STARS:                   # written below, with its badge
            continue
        pixels = original(path)
        rgb, _ = cover_tip(pixels[..., :3], spec['poly'], spec['offset'])
        after = np.dstack([rgb, pixels[..., 3]]) if pixels.shape[2] == 4 else rgb
        if guarded_write(path, after):
            changed = (rgb != pixels[..., :3]).any(axis=2).astype(np.float32)
            xcf = save_master('ears', path, pixels[..., :3], rgb, changed, rgb)
            print('ear tip covered:', path, '->', xcf.relative_to(VN))
    for path, boxes in STARS.items():
        pixels = original(path)
        rgb = pixels[..., :3]
        if path in EARS:
            rgb, _ = cover_tip(rgb, EARS[path]['poly'], EARS[path]['offset'])
        for box in boxes:
            rgb, _ = split(rgb, fit_star(rgb, box))
        after = np.dstack([rgb, pixels[..., 3]]) if pixels.shape[2] == 4 else rgb
        if guarded_write(path, after):
            changed = (rgb != pixels[..., :3]).any(axis=2).astype(np.float32)
            xcf = save_master('star-split', path, pixels[..., :3], rgb, changed, rgb)
            print('star split drawn:', path, '(%d)' % len(boxes), '->', xcf.relative_to(VN))
    for path in RESTORE:
        if path in HAIR:            # written from its original above, with the hair matched
            continue
        keep = ORIGINALS / path.replace('/', '--')
        if keep.is_file():
            write(path, np.asarray(Image.open(keep)))
            print('restored:', path)
    coated = {}
    for name, spec in COATS.items():
        pixels = original(spec['path'])
        mask = np.asarray(Image.open(MASKS / (name + '.png'))).astype(np.float32) / 255
        rgb = recolour(pixels[..., :3], mask, BROWN)
        coated[spec['path']] = np.dstack([rgb, pixels[..., 3]]) if pixels.shape[2] == 4 else rgb
        if spec['path'].startswith('art/scenes/'):        # a GPT painting, which may be redelivered
            if not guarded_write(spec['path'], coated[spec['path']]):
                continue
        else:
            write(spec['path'], coated[spec['path']])
        print('coat recoloured:', spec['path'])
    for path, spec in SKIN.items():
        pixels = coated.get(path, original(path))
        mask = np.asarray(Image.open(MASKS / ('skin--' + Path(path).stem + '.png'))).astype(np.float32) / 255
        rgb = smooth_skin(pixels[..., :3], mask, spec['keep'], spec.get('marks', ()))
        write(path, np.dstack([rgb, pixels[..., 3]]) if pixels.shape[2] == 4 else rgb)
        print('skin pattern removed:', path)


if __name__ == '__main__':
    main()
