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

and from the check of batch 6 (26 September 2026), in FIXES: a doubled
head behind Serat (S021), a paste seam, Valcair's waxy bare hand (S054), ram
horns on Lucan (S057), a moustache on the sketch of Iven (S058), Renn's
stray leg (S035), and the faults GPT's repaints left in S011-S021: the
northern flag too small to see, Tessa's four-fingered hand, horn stubs on
Iven, a second horn on the mother, the ferryman's cut fist, a floating stone
sliver, the old weapon left behind a new crossbow, stars painted on Mara's
shields, the old Renn's hair and boot, badges without the split, a patch of
summer valley left in the S055 snow and the flat base of the S050 pillar.

Each repair works on the copy the game grades from (renpy/game/art/base/, or
the portrait source in renpy/game/art/portraits/); the untouched original is
kept in art/local-repairs/originals/. The sliver repair also has a layered
GIMP master (art/local-repairs/stray-sliver/); a coat recolour is reproduced
from its original, its mask (art/local-repairs/masks/) and this script. Then
run tools/crop-portraits.py and tools/grade-light.py.

A repair is only written over the file it was made from or over this tool's
own output. When GPT redelivers a painting (a repaint put in place from
art/repaints/, or a scene painting saved at its path), the tool says so and
leaves it; once the new painting is checked, a repair it carries over is
listed in CARRIED.

Coat masks come from the Segment Anything model (facebook/sam-vit-large)
prompted with the points below; they are cached in art/local-repairs/masks/.
Making them needs torch and transformers (the local tools venv):

    visual-novel/.tools/depth-venv/bin/python visual-novel/tools/local-repairs.py --segment
    python3 visual-novel/tools/local-repairs.py            # apply every repair
    python3 visual-novel/tools/local-repairs.py --only art/scenes/s021-serat.png
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
from PIL import Image, ImageDraw

VN = Path(__file__).resolve().parents[1]
GAME = VN / 'renpy/game'
HERE = VN / 'art/local-repairs'
ORIGINALS = HERE / 'originals'
MASKS = HERE / 'masks'
WRITTEN = HERE / 'written.json'          # the files this tool last wrote, with their hashes

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

def circle(cx, cy, r, n=24):
    """A polygon around a circle."""
    return [(cx + r * np.cos(2 * np.pi * k / n), cy + r * np.sin(2 * np.pi * k / n)) for k in range(n)]


# Faults found in the check of batch 6 (26 September 2026), fixed by one or
# more steps per painting, applied in order to the painting as delivered and
# written once (a painting that needs several fixes gets all of them). Masks
# made with Segment Anything and checked by eye are in art/local-repairs/masks/;
# regions of a painting as it was before batch 6 (git 3b482c8), used to put
# back what the repaint broke, are in art/local-repairs/references/.
#
#   paint_out  fill a polygon from its surroundings (Navier-Stokes inpainting),
#              optionally only the pixels of one colour inside it ('select',
#              OpenCV Lab bounds, grown by 'grow'), never drawing on 'keep';
#              'shade' darkens it toward 'keep' (the shadow that casts) and
#              'grain' is a patch whose fine grain the fill takes
#   seam       blend the two pieces across a horizontal paste seam: each is
#              mirrored across the seam, broad tones over 'soft' rows, detail
#              over 'sharp' rows
#   match      a region takes another's colour and brightness (Lab mean and
#              spread), keeping its own modelling
#   smooth     a region's texture smoothed by a Gaussian over the region only,
#              with a fine grain added back
#   pencil     a pencil stroke erased back to the paper under it
#   stray      a region replaced with the floor at an offset, shaded by the
#              object beside it, its brightness brought to the floor around
#   clone      a region filled from the same painting at an offset (only the
#              pixels 'select' picks, if given), its brightness brought to
#              what is around it
#   restore    a region put back from the painting before batch 6, through a
#              polygon, or only its warm (skin) pixels
#   trim       an outline brought back to a rounded shape: pixels of the dark
#              mass outside a wobbling ellipse, inside 'zone', and a stray
#              'hook', are filled from the background
#   hand       a hand replaced by the mirror image of the figure's other hand,
#              turned to the arm's line and set on its wrist, in its light
#   flag       a flag drawn on its pole: a waving field with the northern star
#              (eight points, the four principal ones longer, a vertical split)
#   star       the split of the northern emblem drawn on badges (as in STARS)
FIXES = {
    # the second, partly hidden head behind Serat's own (horn, curls, cheek,
    # ear, neck) becomes his brother's coat in the shadow of Serat's head, the
    # strap across the brother's chest running on behind it; and a hard paste
    # seam across Lucan's knee
    'art/scenes/s021-serat.png': [
        ('paint_out', dict(
            fill=[(930, 163), (947, 165), (952, 180), (958, 191), (960, 199), (953, 210), (947, 220), (940, 231),
                  (935, 239), (931, 243.5), (922, 245), (913, 249), (906, 256), (904, 265), (907, 276), (917, 285),
                  (911, 293), (896, 296), (879, 293), (872, 272), (872, 245), (875, 226), (882, 211), (889, 196),
                  (899, 184), (914, 177), (927, 175)],
            keep=[(958, 191), (1010, 185), (1010, 320), (918, 320), (917, 285), (907, 276), (904, 265), (906, 256),
                  (913, 249), (922, 245), (931, 243.5), (935, 239), (940, 231), (947, 220), (953, 210), (960, 199)],
            shade=(0.62, 55), grain=(885, 150, 925, 180))),
        ('seam', dict(row=608, cols=(130, 480), soft=14, sharp=2.0)),
    ],
    # line 2094: the hand on Tessa's shoulder was a pale, waxy bare hand;
    # Valcair is in armour: it takes the dark steel of his other gauntlet
    'art/scenes/s054-strike.png': [
        ('match', dict(region='match--s054-strike', like='like--s054-strike')),
    ],
    # Lucan's horns came out ringed like a ram's; his are smooth
    'art/scenes/s057-father.png': [
        ('smooth', dict(region='smooth--s057-father', sigma=3.0, grain=1.5)),
    ],
    # the sketch of Iven had a moustache (the nose stroke ran on); the nose's
    # hook above and the smile below stay
    'art/scenes/s058-drawings.png': [
        ('pencil', dict(
            erase=[(1281, 416.5), (1288.5, 416), (1289, 421.5), (1296, 421.5), (1297, 417.5), (1303, 417.5),
                   (1309, 418), (1309, 425.5), (1300, 426), (1290, 425.5), (1281, 423)],
            close=11, grain=(1266, 400, 1282, 416))),
    ],
    # Renn's boot and shin came out from under the broken axle beside his
    # face; the deck under the axle's shadow replaces them, so his leg is
    # pinned under the axle (line 1412); the boy and Iven's hand are kept out
    # of the brightness match
    'art/scenes/s035-collapse.png': [
        ('stray', dict(fill='stray--s035-collapse', keep='keep--s035-collapse', clone=(0, 40),
                       shade=(0.85, 0.5, 6.0), match=14, feather=1.6,
                       skip=[(1240, 430, 1320, 560), (1120, 440, 1185, 505)])),
    ],
    # line 530: the northern flag over Bellweir came as a 26x20 px navy scrap
    # with a four-point cross, invisible at full screen; it is drawn larger,
    # higher on its pole, dark green with the white split star
    'art/scenes/s011-sanctuary.png': [
        ('flag', dict(clear=(59, 119, 84, 142), pole=(58.0, 86.0), size=(46, 29), star=10.5, soft=0.6,
                      field=[24, 46, 32], mark=[196, 204, 190], pole_colour=[20, 26, 38], pole_join=150)),
    ],
    # Tessa's raised right hand had a thumb and three fingers (item 36 gave
    # the left hand five): the right hand becomes the mirror of the left
    'art/scenes/s019-gray-scar-ferryhouse.png': [
        ('hand', dict(source='hand-from--s019-gray-scar-ferryhouse', target='hand-to--s019-gray-scar-ferryhouse',
                      skin=136, scale=(0.95, 1.08))),
    ],
    # the repaint left horn stubs and a pale horn tip in Iven's hair (he is
    # human); the old weapon's black tube and a bipod leg behind the new
    # crossbow; and undivided stars on the brother's and Lucan's badges
    'art/scenes/s021-rescue.png': [
        ('trim', dict(ellipse=(789.0, 270.0, 24.0, 24.5), wobble=[(0.045, 9, 1.3), (0.025, 17, 0.0)],
                      zone=(752, 236, 822, 262), dark=120,
                      hook=[(803, 242), (813, 242), (814, 250), (812, 257), (806, 256), (804, 250)],
                      grain=(770, 225, 810, 240))),
        ('clone', dict(fill=[(401, 438), (420, 438), (420, 626), (401, 626)], select={'L': (0, 52)}, grow=1,
                       offset=(30, 0), match=8, feather=0.9)),
        ('clone', dict(fill=[(406, 484), (414, 482), (434, 556), (426, 560)], select={'L': (95, 255)}, grow=1,
                       offset=(22, 0), match=8, feather=0.8)),
        ('star', dict(boxes=[(558, 409, 584, 435), (950, 324, 972, 346)])),
    ],
    # the repaint left a stone sliver floating under the arch, and the gate's
    # edge cut the ferryman's fist into two prongs (it was whole before
    # batch 6); undivided stars on Lucan's and Serat's badges
    'art/scenes/s021-lucan-returns.png': [
        ('paint_out', dict(
            fill=[(383, 124), (398, 113), (420, 104), (440, 98), (460, 93), (475, 91), (487, 92), (503, 96),
                  (518, 101), (532, 106), (542, 110), (540, 119), (530, 118), (515, 113), (500, 108),
                  (485, 104), (474, 103), (460, 105), (442, 110), (422, 116), (402, 124), (390, 132)],
            keep=[(360, 40), (620, 40), (620, 100), (560, 100), (530, 93), (500, 88), (470, 87), (445, 91),
                  (420, 99), (400, 108), (388, 118), (360, 128)],
            grain=(430, 124, 470, 136))),
        ('restore', dict(reference='s021-lucan-returns--340-440', fill=[(345, 445), (398, 445), (398, 505), (345, 505)],
                         warm=138, feather=0.6)),
        ('star', dict(boxes=[(980, 316, 1014, 350), (1186, 317, 1218, 349)])),
    ],
    # the repaint put a flat blade horn beside the northern mother's own ram
    # horn (her head as it was before batch 6); Lucan's badge undivided at
    # line 814, where Mara recognizes the royal split star
    'art/scenes/s018-gray-scar-ferry-approach.png': [
        ('restore', dict(reference='s018-gray-scar-ferry-approach--590-345',
                         fill=[(596, 402), (600, 382), (610, 368), (622, 357), (636, 352), (648, 356), (646, 368),
                               (632, 376), (620, 388), (612, 402)], feather=1.0)),
        ('star', dict(boxes=[(903, 447, 930, 474)])),
    ],
    # a brass compass star on Mara's shield (plain in the scenes around it,
    # and close to the northern emblem's shape): the boss stays; Serat's
    # badge undivided
    'art/scenes/s020-gray-scar-riverbank.png': [
        ('paint_out', dict(fill=circle(1742, 575, 62), spare=[circle(1740, 575, 6.5)], keep=circle(1740, 575, 8),
                           select={'b': (136, 255), 'L': (60, 255)}, grow=2, grain=(1690, 620, 1720, 650))),
        ('star', dict(boxes=[(918, 329, 948, 359)])),
    ],
    # a gold starburst on Mara's shield
    'art/scenes/s021-boat.png': [
        ('paint_out', dict(fill=[(1775, 785), (1835, 785), (1842, 840), (1834, 896), (1812, 955), (1785, 955),
                                 (1772, 880)],
                           keep=[(1838, 884), (1900, 850), (1900, 1000), (1790, 1000), (1806, 962)],
                           select={'b': (138, 255), 'L': (55, 255)}, grow=2, grain=(1745, 900, 1770, 930))),
    ],
    # undivided stars on Serat's and Lucan's badges
    'art/scenes/s021-gray-scar-covered-landing.png': [
        ('star', dict(boxes=[(1056, 323, 1085, 352), (873, 334, 903, 364)])),
    ],
    # the old, larger Renn's boot toe left on the floor between the bed and
    # the trunk, under the new boy's boots (the trunk is kept out of the fill)
    'art/scenes/s014-relief-warehouse.png': [
        ('paint_out', dict(fill=[(1433, 742), (1452, 738), (1470, 740), (1476, 752), (1476, 792), (1440, 794),
                                 (1430, 776)],
                           keep=[(1477, 690), (1620, 690), (1620, 900), (1477, 900)],
                           grain=(1395, 792, 1428, 812))),
    ],
    # a rectangle of the old green summer view left beside Tessa's head
    # under the new snowy valley (item 29): the snowy town and river from
    # higher on the slope fill it; her hair is left alone
    'art/scenes/s055-citadel-lower-stair-morning.png': [
        ('clone', dict(fill=[(246, 268), (337, 268), (337, 366), (246, 366)], select={'a': (0, 132)}, grow=1,
                       offset=(-70, -62), match=0, feather=1.2)),
    ],
    # below y 837 the right-edge pillar became a flat grey rectangle: its own
    # carved stone from higher up carries on down
    'art/scenes/s050-citadel-lower-stair.png': [
        ('clone', dict(fill=[(1809, 836), (1920, 836), (1920, 1080), (1809, 1080)], offset=(0, -243), match=0,
                       feather=1.5)),
    ],
    # the old, taller Renn's hair left on the wall above the new boy, cut
    # off by the repaint's straight edge
    'art/scenes/s014-boots-and-cap.png': [
        ('clone', dict(fill=[(1500, 280), (1556, 280), (1556, 303), (1500, 303)], offset=(-58, 0), match=8,
                       feather=1.5)),
    ],
}

# Paintings GPT repainted in batch 6 (26 September 2026) starting from the
# repaired file, so the repair is already in the new painting: Olan's hand in
# the S003 treatment paintings and close-ups (Iven's brown coat and the
# cleared forearm kept), Mara's face at the ward entrance (the coat kept), and
# scene paintings whose badges keep their split and whose catalog card keeps
# its lettering. The tool leaves them alone; their kept originals and masters
# record what was repaired.
CARRIED = {
    'art/base/opening/cg/ward-entrance.png', 'art/base/opening/cg/treatment-pause.png',
    'art/base/opening/cg/after-first-treatment.png', 'art/base/opening/cg/rested-hand.png',
    'art/base/rovel/details/treatment-blue.png', 'art/base/rovel/details/treatment-white.png',
    'art/scenes/s010-bellweir-hills.png', 'art/scenes/s026-quarry-loading-ramp.png',
    'art/scenes/s027-river-camp-gate.png', 'art/scenes/s028-river-camp-infirmary.png',
    'art/scenes/s057-citadel-lower-gate.png', 'art/scenes/s058-bellweir-market-spring.png',
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


def _polygon(shape, points):
    """A polygon's coverage (0-1, anti-aliased) on an image of this shape."""
    m = np.zeros(shape[:2], np.uint8)
    cv2.fillPoly(m, [np.round(np.array(points) * 8).astype(np.int32)], 255, lineType=cv2.LINE_AA, shift=3)
    return m.astype(np.float32) / 255


def _select(rgb, bounds):
    """Pixels whose OpenCV Lab values lie within bounds ({'L': (low, high),
    'a': ..., 'b': ...}; a missing channel is not limited)."""
    lab = cv2.cvtColor(np.ascontiguousarray(rgb), cv2.COLOR_RGB2LAB).astype(np.float32)
    ok = np.ones(rgb.shape[:2], bool)
    for i, key in enumerate('Lab'):
        low, high = bounds.get(key, (0, 255))
        ok &= (lab[..., i] >= low) & (lab[..., i] <= high)
    return ok


def _chosen(rgb, spec):
    """The region a step works on: its polygon less any 'spare' polygons, or
    only the pixels of it that spec['select'] picks, grown by spec['grow']."""
    region = _polygon(rgb.shape, spec['fill'])
    for spare in spec.get('spare', []):
        region = region * (1 - _polygon(rgb.shape, spare))
    if 'select' in spec:
        grow = spec.get('grow', 1)
        picked = ((region > 0.5) & _select(rgb, spec['select'])).astype(np.uint8)
        picked = cv2.dilate(picked, np.ones((2 * grow + 1, 2 * grow + 1), np.uint8)) & (region > 0.01)
        region = picked.astype(np.float32)
    return region


def paint_out(rgb, spec):
    """Fill a region from its surroundings (Navier-Stokes inpainting) without
    drawing on the figure beside it, darken it toward that figure as the
    shadow it casts, and give it the surrounding cloth's grain."""
    h, w = rgb.shape[:2]
    region = _chosen(rgb, spec)
    keep = _polygon(rgb.shape, spec['keep']) if 'keep' in spec else np.zeros((h, w), np.float32)
    hole = cv2.dilate(((region > 0.01) | (keep > 0.5)).astype(np.uint8), np.ones((3, 3), np.uint8))
    base = cv2.inpaint(np.ascontiguousarray(rgb), hole, 9, cv2.INPAINT_NS).astype(np.float32)
    shade = np.ones((h, w), np.float32)
    if 'shade' in spec:
        darkest, reach = spec['shade']
        near = cv2.distanceTransform((keep < 0.5).astype(np.uint8), cv2.DIST_L2, 5)
        shade = darkest + (1 - darkest) * np.clip(near / reach, 0, 1)
    x0, y0, x1, y1 = spec['grain']
    patch = rgb[y0:y1, x0:x1].astype(np.float32)
    sd = float((patch - cv2.GaussianBlur(patch, (0, 0), 1.5)).std())
    noise = cv2.GaussianBlur(np.random.default_rng(11).normal(0, sd, (h, w)).astype(np.float32), (0, 0), 0.7)
    fill = base * shade[..., None] + noise[..., None] * 0.9
    alpha = cv2.GaussianBlur(region, (0, 0), 0.7)[..., None]
    return np.clip(rgb.astype(np.float32) * (1 - alpha) + fill * alpha + 0.5, 0, 255).astype(np.uint8)


def match_part(rgb, spec):
    """Give a region the colour and brightness of another (Lab mean and
    spread), keeping its own light and shade."""
    region = np.asarray(Image.open(MASKS / (spec['region'] + '.png'))) > 127
    like = np.asarray(Image.open(MASKS / (spec['like'] + '.png'))) > 127
    lab = cv2.cvtColor(np.ascontiguousarray(rgb), cv2.COLOR_RGB2LAB).astype(np.float32)
    have, want = lab[region], lab[like]
    new = lab.copy()
    for c, most in ((0, 1.6), (1, 1.5), (2, 1.5)):
        k = np.clip(want[:, c].std() / have[:, c].std(), 0.5, most)
        new[..., c] = want[:, c].mean() + (lab[..., c] - have[:, c].mean()) * k
    full = cv2.cvtColor(np.clip(new, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB).astype(np.float32)
    alpha = cv2.GaussianBlur(region.astype(np.float32), (0, 0), 0.8)[..., None]
    return np.clip(rgb.astype(np.float32) * (1 - alpha) + full * alpha + 0.5, 0, 255).astype(np.uint8)


def smooth_region(rgb, spec):
    """Smooth a region's texture with a Gaussian taken only over the
    region, and add back a fine grain."""
    region = np.asarray(Image.open(MASKS / (spec['region'] + '.png'))) > 127
    inner = cv2.erode(region.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.float32)
    lab = cv2.cvtColor(np.ascontiguousarray(rgb), cv2.COLOR_RGB2LAB).astype(np.float32)
    smooth = cv2.GaussianBlur(lab * inner[..., None], (0, 0), spec['sigma']) / \
        np.maximum(cv2.GaussianBlur(inner, (0, 0), spec['sigma'])[..., None], 1e-4)
    smooth[..., 0] += cv2.GaussianBlur(np.random.default_rng(2).normal(0, spec['grain'], region.shape).astype(np.float32),
                                       (0, 0), 0.6)
    full = cv2.cvtColor(np.clip(smooth, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB).astype(np.float32)
    alpha = cv2.GaussianBlur(region.astype(np.float32), (0, 0), 0.8)[..., None]
    return np.clip(rgb.astype(np.float32) * (1 - alpha) + full * alpha + 0.5, 0, 255).astype(np.uint8)


def mend_seam(rgb, spec):
    """Blend the two pieces of a painting across a horizontal seam."""
    src = rgb.astype(np.float32)
    h, w = src.shape[:2]
    row, (x0, x1) = spec['row'], spec['cols']
    upper, lower = src.copy(), src.copy()
    for k in range(60):
        upper[row + k] = src[row - 1 - k]
        lower[row - 1 - k] = src[row + k]
    yy = np.arange(h, dtype=np.float32)[:, None] + 0.5
    def ramp(width):
        return np.clip((yy - row + width) / (2 * width), 0, 1)[..., None]
    low_u, low_l = cv2.GaussianBlur(upper, (0, 0), 6), cv2.GaussianBlur(lower, (0, 0), 6)
    soft, sharp = ramp(spec['soft']), ramp(spec['sharp'])
    blend = low_u * (1 - soft) + low_l * soft + (upper - low_u) * (1 - sharp) + (lower - low_l) * sharp
    xs = np.arange(w, dtype=np.float32)[None, :]
    wx = np.clip((xs - x0) / 10, 0, 1) * np.clip((x1 - xs) / 10, 0, 1)
    wy = np.clip(1.5 - np.abs(yy - row) / (spec['soft'] + 2), 0, 1)
    alpha = (wx * wy)[..., None]
    return np.clip(src * (1 - alpha) + blend * alpha + 0.5, 0, 255).astype(np.uint8)


def erase_pencil(rgb, spec):
    """Take a pencil stroke off the paper: the paper's own tone under it
    (a morphological close lifts thin dark strokes), with the paper's grain."""
    h, w = rgb.shape[:2]
    region = np.zeros((h, w), np.uint8)
    cv2.fillPoly(region, [np.round(np.array(spec['erase']) * 8).astype(np.int32)], 255, lineType=cv2.LINE_AA, shift=3)
    region = region.astype(np.float32) / 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (spec['close'], spec['close']))
    paper = cv2.GaussianBlur(cv2.morphologyEx(np.ascontiguousarray(rgb), cv2.MORPH_CLOSE, kernel).astype(np.float32), (0, 0), 1.2)
    x0, y0, x1, y1 = spec['grain']
    patch = rgb[y0:y1, x0:x1].astype(np.float32)
    sd = float((patch - cv2.GaussianBlur(patch, (0, 0), 1.2)).std())
    noise = cv2.GaussianBlur(np.random.default_rng(3).normal(0, sd, (h, w)).astype(np.float32), (0, 0), 0.6)
    alpha = cv2.GaussianBlur(region, (0, 0), 0.8)[..., None]
    return np.clip(rgb.astype(np.float32) * (1 - alpha) + (paper + noise[..., None]) * alpha + 0.5, 0, 255).astype(np.uint8)


def clone_under(rgb, spec):
    """Replace a region with the floor beside it (copied from the given
    offset), shaded by the object next to it, and blended at the edge."""
    region = np.asarray(Image.open(MASKS / (spec['fill'] + '.png'))).astype(np.float32) / 255
    keep = np.asarray(Image.open(MASKS / (spec['keep'] + '.png'))) > 127
    dx, dy = spec['clone']
    floor = np.roll(np.roll(rgb.astype(np.float32), -dy, axis=0), -dx, axis=1)   # floor[y, x] = rgb[y + dy, x + dx]
    base, depth, reach = spec['shade']
    near = cv2.distanceTransform((~keep).astype(np.uint8), cv2.DIST_L2, 5)
    fill = floor * (base * (1 - depth * np.exp(-near / reach)))[..., None]
    hole = region > 0.5
    ring = (cv2.dilate(hole.astype(np.uint8), np.ones((17, 17), np.uint8)) > 0) & ~hole & ~keep
    for x0, y0, x1, y1 in spec['skip']:
        ring[y0:y1, x0:x1] = False

    def local_mean(image, mask):
        weight = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), spec['match'])[..., None]
        return cv2.GaussianBlur(image * mask[..., None], (0, 0), spec['match']) / np.maximum(weight, 1e-4)

    fill = fill * np.clip(local_mean(rgb.astype(np.float32), ring) / np.maximum(local_mean(fill, hole), 1), 0.3, 3)
    alpha = cv2.GaussianBlur(region, (0, 0), spec['feather'])[..., None]
    return np.clip(rgb.astype(np.float32) * (1 - alpha) + fill * alpha + 0.5, 0, 255).astype(np.uint8)


def _local_mean(image, mask, sigma):
    weight = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), sigma)[..., None]
    return cv2.GaussianBlur(image * mask[..., None].astype(np.float32), (0, 0), sigma) / np.maximum(weight, 1e-4)


def clone_region(rgb, spec):
    """Fill a region with the painting at an offset, brought to the
    brightness around the region (unless 'match' is 0), with a feathered
    edge."""
    src = rgb.astype(np.float32)
    region = _chosen(rgb, spec) > 0.5
    dx, dy = spec['offset']
    moved = np.roll(np.roll(src, -dy, axis=0), -dx, axis=1)       # moved[y, x] = src[y + dy, x + dx]
    ring = (cv2.dilate(region.astype(np.uint8), np.ones((17, 17), np.uint8)) > 0) & ~region
    sigma = spec.get('match', 10)
    if sigma:
        moved = moved * np.clip(_local_mean(src, ring, sigma) / np.maximum(_local_mean(moved, region, sigma), 1), 0.3, 3)
    alpha = cv2.GaussianBlur(region.astype(np.float32), (0, 0), spec.get('feather', 1.0))[..., None]
    return np.clip(src * (1 - alpha) + moved * alpha + 0.5, 0, 255).astype(np.uint8)


def restore_region(rgb, spec):
    """Put back a region of the painting as it was before batch 6 (a crop in
    art/local-repairs/references/ named <painting>--<x>-<y>), through a
    polygon, or only where the old crop is warm skin (a > spec['warm'])."""
    name = spec['reference']
    ref = np.asarray(Image.open(HERE / 'references' / (name + '.png')).convert('RGB')).astype(np.float32)
    x0, y0 = (int(v) for v in name.rsplit('--', 1)[1].split('-'))
    h, w = ref.shape[:2]
    alpha = _polygon(rgb.shape, spec['fill'])[y0:y0 + h, x0:x0 + w]
    if 'warm' in spec:
        lab = cv2.cvtColor(ref.astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
        warm = cv2.morphologyEx((lab[..., 1] > spec['warm']).astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
        alpha = alpha * warm
    alpha = cv2.GaussianBlur(alpha.astype(np.float32), (0, 0), spec.get('feather', 0.7))[..., None]
    out = rgb.astype(np.float32).copy()
    out[y0:y0 + h, x0:x0 + w] = out[y0:y0 + h, x0:x0 + w] * (1 - alpha) + ref * alpha
    return np.clip(out + 0.5, 0, 255).astype(np.uint8)


def trim_outline(rgb, spec):
    """Round off an outline: the dark mass outside a wobbling ellipse within
    'zone', and a stray 'hook', are filled from the background around them."""
    src = np.ascontiguousarray(rgb)
    h, w = src.shape[:2]
    lab = cv2.cvtColor(src, cv2.COLOR_RGB2LAB).astype(np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy, ax, ay = spec['ellipse']
    theta = np.arctan2((yy - cy) / ay, (xx - cx) / ax)
    wobble = 1 + sum(amp * np.sin(theta * freq + phase) for amp, freq, phase in spec['wobble'])
    inside = ((xx - cx) / ax) ** 2 + ((yy - cy) / ay) ** 2 <= wobble ** 2
    dark = lab[..., 0] < spec['dark']
    zx0, zy0, zx1, zy1 = spec['zone']
    zone = np.zeros((h, w), bool)
    zone[zy0:zy1, zx0:zx1] = True
    hook = _polygon(src.shape, spec['hook']) > 0.5
    region = (dark & ~inside & zone) | (hook & ~inside)
    region = cv2.dilate(region.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & ~inside & zone
    hole = cv2.dilate((region | (dark & zone) | (inside & zone)).astype(np.uint8), np.ones((3, 3), np.uint8))
    base = cv2.inpaint(src, hole, 7, cv2.INPAINT_NS).astype(np.float32)
    x0, y0, x1, y1 = spec['grain']
    patch = src[y0:y1, x0:x1].astype(np.float32)
    sd = float((patch - cv2.GaussianBlur(patch, (0, 0), 1.2)).std())
    noise = cv2.GaussianBlur(np.random.default_rng(4).normal(0, sd, (h, w)).astype(np.float32), (0, 0), 0.7)
    alpha = cv2.GaussianBlur(region.astype(np.float32), (0, 0), 0.7)[..., None]
    return np.clip(src * (1 - alpha) + (base + noise[..., None] * 0.8) * alpha + 0.5, 0, 255).astype(np.uint8)


def mirror_hand(rgb, spec):
    """Replace a hand (mask 'target') with the mirror image of the other hand
    (mask 'source'): only its skin (a > spec['skin']) is carried, turned from
    its own wrist-to-fingertips line to the target's, scaled within
    spec['scale'], set on the target's wrist and given the target's mean
    light and colour; the old hand is first filled from the light around it."""
    src = np.ascontiguousarray(rgb)
    h, w = src.shape[:2]
    lab = cv2.cvtColor(src, cv2.COLOR_RGB2LAB).astype(np.float32)
    source = np.asarray(Image.open(MASKS / (spec['source'] + '.png'))) > 127
    target = np.asarray(Image.open(MASKS / (spec['target'] + '.png'))) > 127
    skin_from = cv2.morphologyEx((source & (lab[..., 1] > spec['skin'])).astype(np.uint8), cv2.MORPH_OPEN,
                                 np.ones((2, 2), np.uint8)).astype(bool)
    skin_to = target & (lab[..., 1] > spec['skin'])

    def axis(mask):
        ys, xs = np.nonzero(mask)
        wrist = np.array([xs[ys >= ys.max() - 3].mean(), ys.max()], np.float32)
        tips = np.array([xs[ys <= ys.min() + 10].mean(), ys.min()], np.float32)
        return wrist, tips

    (w_from, t_from), (w_to, t_to) = axis(source), axis(target)
    hole = cv2.dilate(target.astype(np.uint8), np.ones((5, 5), np.uint8))
    hole[int(w_to[1]) - 2:, :] = 0                                  # not the sleeve below the wrist
    cleared = cv2.inpaint(src, hole, 9, cv2.INPAINT_NS)
    v_from = t_from - w_from
    v_from = np.array([-v_from[0], v_from[1]])                     # mirrored
    v_to = t_to - w_to
    angle = np.degrees(np.arctan2(v_to[1], v_to[0]) - np.arctan2(v_from[1], v_from[0]))
    scale = float(np.clip(np.linalg.norm(v_to) / np.linalg.norm(v_from), *spec['scale']))
    wrist = np.array([w - 1 - w_from[0], w_from[1]], np.float32)
    turn = cv2.getRotationMatrix2D((float(wrist[0]), float(wrist[1])), -float(angle), scale)
    turn[:, 2] += w_to - wrist
    hand = cv2.warpAffine(np.ascontiguousarray(src[:, ::-1]), turn, (w, h), flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REFLECT)
    cover = cv2.warpAffine(np.ascontiguousarray(skin_from[:, ::-1]).astype(np.float32), turn, (w, h))
    hand_lab = cv2.cvtColor(hand, cv2.COLOR_RGB2LAB).astype(np.float32)
    for c in range(3):
        hand_lab[..., c] += lab[..., c][skin_to].mean() - hand_lab[..., c][cover > 0.7].mean()
    hand = cv2.cvtColor(np.clip(hand_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB).astype(np.float32)
    alpha = cv2.GaussianBlur(np.clip(cover, 0, 1), (0, 0), 0.6)[..., None]
    return np.clip(cleared.astype(np.float32) * (1 - alpha) + hand * alpha + 0.5, 0, 255).astype(np.uint8)


def draw_flag(rgb, spec):
    """A cloth flag on its pole: the old flag ('clear') filled from the sky,
    then a waving field with the northern star (eight points, the four
    principal ones longer, a vertical split), drawn 4x and brought down, and
    the pole carried up to it."""
    src = np.ascontiguousarray(rgb)
    h, w = src.shape[:2]
    x0, y0, x1, y1 = spec['clear']
    old = np.zeros((h, w), np.uint8)
    old[y0:y1, x0:x1] = 1
    out = cv2.inpaint(src, old, 5, cv2.INPAINT_NS).astype(np.float32)
    ss = 4
    px, top = spec['pole']
    fw, fh = spec['size']
    cw, ch = (fw + 8) * ss, (fh + 16) * ss
    cloth, star, split_line = (Image.new('L', (cw, ch), 0) for _ in range(3))

    def sag(u):
        return (1.2 * u / fw + 2.4 * np.sin(2 * np.pi * u / 34 + 0.6) * (u / fw)) * ss

    us = np.linspace(0, fw, 60)
    ImageDraw.Draw(cloth).polygon([(u * ss, 2 * ss + sag(u)) for u in us] +
                                  [(u * ss, (2 + fh) * ss + sag(u) * 1.15) for u in us[::-1]], fill=255)
    cx, cy = 0.46 * fw * ss, (2 + fh / 2) * ss + sag(0.46 * fw)
    outer, inner, mid = spec['star'] * ss, spec['star'] * 0.37 * ss, spec['star'] * 0.6 * ss
    points = []
    for k in range(16):
        a = -np.pi / 2 + k * np.pi / 8
        rad = outer if k % 4 == 0 else (mid if k % 4 == 2 else inner)
        points.append((cx + rad * np.cos(a) * 0.92, cy + rad * np.sin(a)))
    ImageDraw.Draw(star).polygon(points, fill=255)
    ImageDraw.Draw(split_line).line([(cx, cy - outer * 1.02), (cx, cy + outer * 1.02)], fill=255, width=int(1.1 * ss))
    cloth, star, split_line = (np.asarray(m.resize((cw // ss, ch // ss), Image.LANCZOS)).astype(np.float32) / 255
                               for m in (cloth, star, split_line))
    fh2, fw2 = cloth.shape
    u = np.arange(fw2, dtype=np.float32)[None, :]
    fold = np.repeat(0.74 + 0.26 * np.cos(2 * np.pi * u / 34 + 0.6 + np.pi / 2), fh2, 0)[..., None]
    field, mark = np.array(spec['field'], np.float32), np.array(spec['mark'], np.float32)
    on_star = np.clip(star - split_line, 0, 1)[..., None] * cloth[..., None]
    colour = field * fold * (1 - on_star) + mark * (0.7 + 0.3 * fold) * on_star
    colour = colour + cv2.GaussianBlur(np.random.default_rng(9).normal(0, 2.5, (fh2, fw2)).astype(np.float32),
                                       (0, 0), 0.6)[..., None]
    alpha = cv2.GaussianBlur(cloth, (0, 0), spec['soft'])[..., None]
    fx, fy = int(px) + 1, int(top)
    out[fy:fy + fh2, fx:fx + fw2] = out[fy:fy + fh2, fx:fx + fw2] * (1 - alpha) + colour * alpha
    pole = np.zeros((h, w), np.float32)
    cv2.line(pole, (int(px * 4), int((top - 2) * 4)), (int(px * 4), int(spec['pole_join'] * 4)), 1.0, 2,
             cv2.LINE_AA, shift=2)
    pole = cv2.GaussianBlur(pole, (0, 0), 0.4)[..., None]
    out = out * (1 - pole * 0.9) + np.array(spec['pole_colour'], np.float32) * pole * 0.9
    return np.clip(out + 0.5, 0, 255).astype(np.uint8)


def split_stars(rgb, spec):
    for box in spec['boxes']:
        rgb, _ = split(rgb, fit_star(rgb, box))
    return rgb


FIX_STEPS = {'paint_out': paint_out, 'seam': mend_seam, 'match': match_part, 'smooth': smooth_region,
             'pencil': erase_pencil, 'stray': clone_under, 'clone': clone_region, 'restore': restore_region,
             'trim': trim_outline, 'hand': mirror_hand, 'flag': draw_flag, 'star': split_stars}


def _sha(path):
    return hashlib.sha256((GAME / path).read_bytes()).hexdigest()


ONLY = set()                            # --only: the files to repair this run


def guarded_write(path, after):
    """Write a repair only over the file it was made from, over this tool's
    own last output (recorded in WRITTEN) or over a file that already holds
    this result. If the painting was since redelivered, say so and leave it."""
    if ONLY and path not in ONLY:
        return False
    if path in CARRIED:
        print('carried into GPT\'s repaint, left alone:', path)
        return False
    written = json.loads(WRITTEN.read_text()) if WRITTEN.is_file() else {}
    current = np.asarray(Image.open(GAME / path))
    keep = np.asarray(Image.open(ORIGINALS / path.replace('/', '--')))
    ours = written.get(path) == _sha(path) or any(
        current.shape == other.shape and np.array_equal(current, other) for other in (keep, after))
    if ours:
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
    parser.add_argument('--only', nargs='+', metavar='PATH',
                        help='apply only the repairs to these files (paths under renpy/game/)')
    args = parser.parse_args()
    if args.only:
        ONLY.update(args.only)
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
        if not guarded_write(path, full):
            continue
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
        if guarded_write(path, np.dstack([rgb, pixels[..., 3]]) if pixels.shape[2] == 4 else rgb):
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
    for path, steps in FIXES.items():
        pixels = original(path)
        rgb = pixels[..., :3]
        for kind, spec in steps:
            rgb = FIX_STEPS[kind](rgb, spec)
        after = np.dstack([rgb, pixels[..., 3]]) if pixels.shape[2] == 4 else rgb
        if guarded_write(path, after):
            changed = (rgb != pixels[..., :3]).any(axis=2).astype(np.float32)
            xcf = save_master('batch6-check', path, pixels[..., :3], rgb, changed, rgb)
            print('fixed (%s):' % ', '.join(kind for kind, _ in steps), path, '(%d px) ->' % changed.sum(),
                  xcf.relative_to(VN))
    for path in RESTORE:
        if path in HAIR:            # written from its original above, with the hair matched
            continue
        keep = ORIGINALS / path.replace('/', '--')
        if keep.is_file() and guarded_write(path, np.asarray(Image.open(keep))):
            print('restored:', path)
    coated = {}
    for name, spec in COATS.items():
        pixels = original(spec['path'])
        mask = np.asarray(Image.open(MASKS / (name + '.png'))).astype(np.float32) / 255
        rgb = recolour(pixels[..., :3], mask, BROWN)
        coated[spec['path']] = np.dstack([rgb, pixels[..., 3]]) if pixels.shape[2] == 4 else rgb
        if spec['path'] in SKIN:            # written below, with the skin smoothed
            continue
        if guarded_write(spec['path'], coated[spec['path']]):
            print('coat recoloured:', spec['path'])
    for path, spec in SKIN.items():
        pixels = coated.get(path, original(path))
        mask = np.asarray(Image.open(MASKS / ('skin--' + Path(path).stem + '.png'))).astype(np.float32) / 255
        rgb = smooth_skin(pixels[..., :3], mask, spec['keep'], spec.get('marks', ()))
        if guarded_write(path, np.dstack([rgb, pixels[..., 3]]) if pixels.shape[2] == 4 else rgb):
            print('coat recoloured and skin pattern removed:' if path in coated else 'skin pattern removed:', path)


if __name__ == '__main__':
    main()
