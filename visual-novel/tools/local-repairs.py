#!/usr/bin/env python3
"""Local corrections to finished paintings, each kept as a layered GIMP master.

Repairs found in the S001-S005 sweep of 24 September 2026, done locally
instead of re-requesting the paintings:

  sliver    a stray metal sliver the image generator left on Tessa's drawing
            (S002), painted out from the surrounding paper by inpainting
  recolour  Iven's coat, which the S004 and S005 paintings made khaki and
            brown, shifted to the olive of his design and of the S003
            paintings; the coat is cut out by a segmentation mask

Each repair works on the base copy the game grades from (renpy/game/art/base/);
the untouched original is kept in art/local-repairs/originals/, and
art/local-repairs/<repair>/<file>.xcf holds the original and the repair as
separate layers (checked to flatten back to the result). The top-level copy
beside the base one is overwritten to match. Then run tools/grade-light.py.

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

# Iven's coat: segmentation prompts (points on the coat; points on shirt,
# trousers, hands, face, bag and background to leave out). The S003 painting
# gives the target olive.
COATS = {
    'window-together': ([(733, 499), (1040, 457), (1065, 565), (1148, 715), (758, 350), (725, 640)],
                        [(907, 457), (849, 682), (1048, 715), (949, 673), (866, 914), (849, 283)]),
    'window-pause': ([(1140, 302), (1119, 454), (1130, 756), (1097, 886), (1400, 356), (1454, 454), (1173, 648)],
                     [(1313, 378), (1302, 756), (1205, 972), (1389, 605), (1324, 551), (1248, 162), (1302, 76),
                      (1043, 432), (1540, 670), (1356, 810), (1162, 1058)]),
    'window-packing': ([(1180, 281), (1147, 432), (1158, 756), (1126, 864), (1439, 324), (1482, 410), (1212, 648)],
                       [(1363, 378), (1331, 756), (1234, 972), (1406, 486), (1514, 497), (1309, 162), (1352, 65),
                        (1082, 324), (1374, 778), (1536, 670), (1190, 1058)]),
    'ceremony-intervention': ([(600, 345), (570, 445), (560, 520), (625, 420), (590, 300)],
                              [(650, 520), (560, 645), (625, 580), (620, 230), (650, 455), (640, 435), (700, 370)]),
    'ceremony-yield': ([(660, 321), (614, 407), (586, 492), (717, 378), (580, 350)],
                       [(523, 492), (717, 492), (688, 583), (671, 213), (728, 458), (722, 429), (762, 321), (574, 652)]),
}
# Iven's olive coat in S003 (the ward-lit stage, as graded from its base
# images), measured through a coat mask made the same way: mean and spread of
# OpenCV 8-bit Lab over the coat.
OLIVE = {'mean': np.array([43.2, 129.2, 138.4], np.float32), 'std': np.array([22.9, 1.1, 4.0], np.float32)}


def original(path):
    """The file as it was before any local repair (saved on first use)."""
    keep = ORIGINALS / path.replace('/', '--')
    if not keep.is_file():
        keep.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(GAME / path, keep)
    return np.asarray(Image.open(keep).convert('RGB'))


def write(base_path, rgb):
    """Save the repair to the base copy, which the game grades from, and to
    the top-level copy beside it (no longer shown since the Intense grade was
    retired, but kept identical so nothing old resurfaces)."""
    Image.fromarray(rgb).save(GAME / base_path)
    Image.fromarray(rgb).save(GAME / base_path.replace('art/base/', 'art/', 1))


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
    # the paper's own grain over the filled strip
    noise = np.random.default_rng(5).normal(0, 2.2, rgb.shape[:2]).astype(np.float32)
    soft = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 0.8)
    out = np.clip(out.astype(np.float32) + (noise * soft)[..., None], 0, 255).astype(np.uint8)
    return out, soft


def clean_mask(prob):
    """Threshold, drop specks, fill pinholes, and feather by a pixel."""
    m = (prob > 0.5).astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    big = stats[1:, cv2.CC_STAT_AREA].max() if n > 1 else 0
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= 0.02 * big:
            keep[labels == i] = 1
    keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    return cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 1.0)


def lab_stats(rgb, mask):
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    sel = lab[mask > 0.9]
    return sel.mean(0), sel.std(0)


def recolour(rgb, mask, olive):
    """Move the coat's colour to the olive while keeping its own light, folds
    and weave: a and b take the olive's mean and spread; L keeps its texture
    and moves a third of the way toward the olive's brightness, so a coat in
    a bright hall stays light."""
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    mean, std = lab_stats(rgb, mask)
    new = lab.copy()
    for c in (1, 2):
        k = np.clip(olive['std'][c] / max(std[c], 1e-3), 0.6, 1.3)
        new[..., c] = olive['mean'][c] + (lab[..., c] - mean[c]) * k
    new[..., 0] = lab[..., 0] + (olive["mean"][0] - mean[0]) * 0.35
    full = cv2.cvtColor(np.clip(new, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
    out = rgb.astype(np.float32) * (1 - mask[..., None]) + full.astype(np.float32) * mask[..., None]
    return np.clip(out + 0.5, 0, 255).astype(np.uint8), full


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


def segment():
    import torch
    from transformers import SamModel
    model = SamModel.from_pretrained('facebook/sam-vit-large').eval()
    if torch.cuda.is_available():
        model = model.cuda()
    device = next(model.parameters()).device

    def run(path, pos, neg):
        im = Image.open(path).convert('RGB')
        w, h = im.size
        s = 1024 / max(w, h)
        nw, nh = int(round(w * s)), int(round(h * s))
        a = (np.asarray(im.resize((nw, nh), Image.BILINEAR), np.float32) - [123.675, 116.28, 103.53]) / [58.395, 57.12, 57.375]
        pad = np.zeros((1024, 1024, 3), np.float32)
        pad[:nh, :nw] = a
        x = torch.from_numpy(pad.transpose(2, 0, 1)[None].astype(np.float32)).to(device)
        points = torch.tensor([[[(px * s, py * s) for px, py in pos + neg]]], dtype=torch.float32).to(device)
        labels = torch.tensor([[[1] * len(pos) + [0] * len(neg)]]).to(device)
        with torch.no_grad():
            out = model(image_embeddings=model.get_image_embeddings(x), input_points=points,
                        input_labels=labels, multimask_output=True)
        m = out.pred_masks[0, 0][int(out.iou_scores[0, 0].argmax())][None, None]
        m = torch.nn.functional.interpolate(m, (1024, 1024), mode='bilinear')[..., :nh, :nw]
        m = torch.nn.functional.interpolate(m, (h, w), mode='bilinear')[0, 0]
        return (torch.sigmoid(m).cpu().numpy() * 255).astype(np.uint8)

    MASKS.mkdir(parents=True, exist_ok=True)
    for name, (pos, neg) in COATS.items():
        path = 'art/base/rovel/cg/%s.png' % name
        original(path)
        Image.fromarray(run(ORIGINALS / path.replace('/', '--'), pos, neg)).save(MASKS / (name + '.png'))
        print('mask', name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--segment', action='store_true', help='make the coat masks (needs torch, transformers)')
    args = parser.parse_args()
    if args.segment:
        segment()
        return
    for path, (p0, p1) in SLIVERS.items():
        before = original(path)
        after, _ = remove_sliver(before, p0, p1)
        changed = (after != before).any(axis=2).astype(np.float32)
        write(path, after)
        xcf = save_master('stray-sliver', path, before, after, changed, after)
        print('sliver removed:', path, '(%d px) ->' % changed.sum(), xcf.relative_to(VN))
    for name in COATS:
        mask = clean_mask(np.asarray(Image.open(MASKS / (name + '.png'))).astype(np.float32) / 255)
        for path in ('art/base/rovel/cg/%s.png' % name,):
            before = original(path)
            after, full = recolour(before, mask, OLIVE)
            write(path, after)
            xcf = save_master('iven-olive-coat', path, before, full, mask, after)
            print('coat recoloured:', path, '->', xcf.relative_to(VN))


if __name__ == '__main__':
    main()
