#!/usr/bin/env python3
"""Local corrections to finished paintings, each kept as a layered GIMP master.

Repairs found in the S001-S005 sweep of 24 September 2026, done locally
instead of re-requesting the paintings:

  sliver    a stray metal sliver the image generator left on Tessa's drawing
            (S002), painted out from the surrounding paper by inpainting
  recolour  Iven's coat, changed from olive to brown because green is the
            northern side's colour (user decision): the S003 paintings and
            close-ups, his ten portraits, and the two S004 ceremony paintings
            (khaki); the coat is cut out by a segmentation mask. The S005
            window paintings get back GPT's own brown.

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

# The stray sliver on the S002 drawing: a thin diagonal strip from p0 to p1.
SLIVERS = {
    'art/base/opening/cg/drawing-restart.png': ((941, 744), (964, 768)),
    'art/base/opening/cg/detail-drawing.png': ((224, 40), (246, 64)),
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
    'ward-entrance': dict(path='art/base/opening/cg/ward-entrance.png', box=(1097, 287, 1358, 548), seeds=[(1149, 391), (1227, 365)]),
    'ward-assessment': dict(path='art/base/rovel/cg/ward-assessment.png', box=(65, 222, 679, 940), seeds=[(209, 418), (600, 365), (156, 783)]),
    'blue-healing': dict(path='art/base/opening/cg/blue-healing.png', box=(65, 222, 627, 940), seeds=[(209, 418), (561, 391), (156, 783)]),
    'ward-standing-unlit': dict(path='art/base/opening/cg/ward-standing-unlit.png', box=(483, 261, 979, 940), seeds=[(561, 391), (627, 653), (561, 836), (901, 418), (927, 574)], extra=[((500, 560, 590, 941), [(540, 760)])]),
    'ward-standing-light': dict(path='art/base/opening/cg/ward-standing-light.png', box=(483, 261, 979, 940), seeds=[(561, 391), (627, 653), (561, 836), (901, 418), (927, 574)], extra=[((500, 560, 590, 941), [(540, 760)])]),
    'first-purification': dict(path='art/base/opening/cg/first-purification.png', box=(431, 248, 888, 836), seeds=[(627, 431), (836, 457), (849, 600)], extra=[((610, 330, 690, 560), [(650, 440)])]),
    'last-patch': dict(path='art/base/opening/cg/last-patch.png', box=(535, 248, 953, 875), seeds=[(653, 444), (875, 457), (901, 600)]),
    'purification-cleared': dict(path='art/base/opening/cg/purification-cleared.png', box=(587, 222, 979, 796), seeds=[(653, 444), (901, 457), (927, 600)]),
    'treatment-pause': dict(path='art/base/opening/cg/treatment-pause.png', box=(522, 248, 953, 927), seeds=[(600, 418), (875, 444), (901, 627)], extra=[((585, 255, 700, 585), [(630, 300), (665, 450)])]),
    'after-first-treatment': dict(path='art/base/opening/cg/after-first-treatment.png', box=(640, 143, 796, 627), seeds=[(684, 391), (692, 522)]),
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


def remove_sliver(rgb, p0, p1):
    """Inpaint the sliver: pixels near the segment that are far darker or
    paler than the paper and pencil around them."""
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


def segment():
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

    MASKS.mkdir(parents=True, exist_ok=True)
    for name, spec in COATS.items():
        pixels = original(spec['path'])
        rgb = pixels[..., :3].copy()
        if spec.get('portrait'):
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
        mask = clean_mask(prob, seeds)
        Image.fromarray((mask * 255 + 0.5).astype(np.uint8)).save(MASKS / (name + '.png'))
        print('mask', name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--segment', action='store_true', help='make the coat masks (needs torch, transformers)')
    args = parser.parse_args()
    if args.segment:
        segment()
        return
    for path, (p0, p1) in SLIVERS.items():
        before = original(path)[..., :3]
        after, _ = remove_sliver(before, p0, p1)
        changed = (after != before).any(axis=2).astype(np.float32)
        write(path, after)
        xcf = save_master('stray-sliver', path, before, after, changed, after)
        print('sliver removed:', path, '(%d px) ->' % changed.sum(), xcf.relative_to(VN))
    for path in RESTORE:
        keep = ORIGINALS / path.replace('/', '--')
        if keep.is_file():
            write(path, np.asarray(Image.open(keep)))
            print('restored:', path)
    for name, spec in COATS.items():
        pixels = original(spec['path'])
        mask = np.asarray(Image.open(MASKS / (name + '.png'))).astype(np.float32) / 255
        rgb = recolour(pixels[..., :3], mask, BROWN)
        write(spec['path'], np.dstack([rgb, pixels[..., 3]]) if pixels.shape[2] == 4 else rgb)
        print('coat recoloured:', spec['path'])


if __name__ == '__main__':
    main()
