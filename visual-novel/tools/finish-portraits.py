#!/usr/bin/env python3
"""Rebuild the S001-S005 dialogue portraits as clean, neutral masters.

The portraits were painted as bare heads on flat grounds (art/rovel/raw/*.png)
and cut out in GIMP (tools/finish-rovel.scm) with a grade baked in. Their
edges carried the ground's grey or brown into the hair, the necks ended in a
hard cut (red generation fringe on some), and the baked grades did not match
the current light registers.

For each head this script
  - crops the same cell from the neutral sheet, at the sheet's full resolution;
  - reuses the hand-made GIMP mask from the old portrait, upsampled with the
    painting itself as guide so it follows the hair;
  - removes the ground colour from partly transparent edge pixels;
  - dissolves the neck into shadow below the chin, so the head emerges from
    darkness instead of ending at a cut;
and writes renpy/game/art/cast/<name>.png. tools/grade-light.py then grades
these (and the new art/portraits/ busts) into each light register.

    python3 visual-novel/tools/finish-portraits.py
"""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

VN = Path(__file__).resolve().parents[1]
RAW = VN / 'art/rovel/raw'
OLD = VN / 'renpy/game/art/rovel/portraits'
OUT = VN / 'renpy/game/art/cast'
LONG_SIDE = 640

# name: (sheet, x, y, w, h, existing portrait whose GIMP mask is reused)
CELLS = {
    'tessa-startled': ('tessa-expressions-v1', 0, 0, 627, 627, 'tessa-startled-formal-ordinary'),
    'tessa-resolute': ('tessa-expressions-v1', 627, 0, 627, 627, 'tessa-resolute-formal-ordinary'),
    'tessa-wounded': ('tessa-expressions-v1', 0, 627, 627, 627, 'tessa-wounded-formal-ordinary'),
    'tessa-listening': ('tessa-expressions-v1', 627, 627, 627, 627, 'tessa-listening-formal-ordinary'),
    'senn-assuring': ('senn-expressions-v1', 0, 0, 627, 836, 'senn-assuring-bright'),
    'senn-listening': ('senn-expressions-v1', 627, 0, 627, 836, 'senn-listening-bright'),
    'senn-evasive': ('senn-expressions-v1', 1254, 0, 627, 836, 'senn-evasive-bright'),
    'mara-controlled': ('mara-expressions-v1', 0, 0, 887, 887, 'mara-controlled-ordinary'),
    'mara-uneasy': ('mara-expressions-v1', 887, 0, 887, 887, 'mara-uneasy-ordinary'),
    'iven-attentive': ('iven-expressions-v1', 0, 0, 887, 887, 'iven-attentive-ordinary'),
    'iven-concerned': ('iven-expressions-v1', 887, 0, 887, 887, 'iven-concerned-ordinary'),
    'olan': ('supporting-cast-v1', 0, 0, 512, 512, 'olan-ordinary'),
    'priest': ('supporting-cast-v1', 512, 0, 512, 512, 'priest-ordinary'),
    'mother': ('supporting-cast-v1', 1024, 0, 512, 512, 'mother-ordinary'),
    'petitioner': ('supporting-cast-v1', 0, 512, 512, 512, 'petitioner-bright'),
    'orra': ('supporting-cast-v1', 512, 512, 512, 512, 'orra-bright'),
    'messenger': ('supporting-cast-v1', 1024, 512, 512, 512, 'messenger-bright'),
}

# The heads on black grounds were generated with a thin pale outline; choke the
# matte by this many sheet pixels so the outline falls outside it.
CHOKE = {'senn': 3, 'mara': 3, 'iven': 2}

# Chin line (fraction of the cell height) where the neck begins to dissolve,
# and where it has gone. Measured on the sheets; heads sit at different heights.
NECK = {
    'tessa': (0.80, 0.97), 'senn': (0.80, 0.95), 'mara': (0.80, 0.95), 'iven': (0.82, 0.97),
    'olan': (0.78, 0.96), 'priest': (0.80, 0.97), 'mother': (0.80, 0.97),
    'petitioner': (0.80, 0.97), 'orra': (0.80, 0.97), 'messenger': (0.80, 0.97),
}


def box(x, r):
    return cv2.boxFilter(x, -1, (2 * r + 1, 2 * r + 1), normalize=True, borderType=cv2.BORDER_REFLECT)


def guided(guide, source, r, eps):
    """Guided filter (He et al.): smooth `source` along the edges of `guide`."""
    mean_i, mean_p = box(guide, r), box(source, r)
    cov = box(guide * source, r) - mean_i * mean_p
    var = box(guide * guide, r) - mean_i * mean_i
    a = cov / (var + eps)
    b = mean_p - a * mean_i
    return box(a, r) * guide + box(b, r)


def old_mask(name, w, h):
    """The GIMP mask from the old 512 portrait, mapped back onto the raw cell."""
    alpha = np.asarray(Image.open(OLD / (name + '.png')).getchannel('A'), np.float32) / 255.0
    long_side = max(w, h)
    sw, sh = round(512 * w / long_side), round(512 * h / long_side)
    ox, oy = round((512 - sw) / 2), round((512 - sh) / 2)
    cell = alpha[oy:oy + sh, ox:ox + sw]
    return cv2.resize(cell, (w, h), interpolation=cv2.INTER_CUBIC)


def ground_field(rgb, alpha):
    """The painted ground behind the head, spread under the head by normalized blur."""
    weight = (alpha < 0.03).astype(np.float32)
    field = np.zeros_like(rgb)
    for sigma in (8, 24, 64):
        num = cv2.GaussianBlur(rgb * weight[..., None], (0, 0), sigma)
        den = cv2.GaussianBlur(weight, (0, 0), sigma)[..., None]
        field = np.where(field.sum(axis=2, keepdims=True) > 0, field, num / np.maximum(den, 1e-4) * (den > 1e-3))
    return field


def finish(name, sheet, x, y, w, h, mask_from):
    raw = np.asarray(Image.open(RAW / (sheet + '.png')).convert('RGB'), np.float32) / 255.0
    rgb = raw[y:y + h, x:x + w].copy()
    grey = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    alpha = np.clip(guided(grey, old_mask(mask_from, w, h), 3, 2e-3), 0, 1)
    alpha = np.where(alpha < 0.02, 0, np.where(alpha > 0.98, 1, alpha))
    choke = CHOKE.get(name.split('-')[0], 0)
    if choke:
        disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * choke + 1, 2 * choke + 1))
        alpha = np.minimum(alpha, cv2.GaussianBlur(cv2.erode(alpha, disk), (0, 0), 0.8))

    # Remove the ground from edge pixels: F = (I - (1 - a) B) / a.
    ground = ground_field(rgb, alpha)
    a3 = alpha[..., None]
    fg = np.where(a3 > 0.04, (rgb - (1 - a3) * ground) / np.maximum(a3, 1e-3), rgb)
    rgb = np.clip(np.where(a3 > 0.97, rgb, fg), 0, 1)

    # Dissolve the neck into shadow below the chin.
    start, end = NECK[name.split('-')[0]]
    yy = np.arange(h, dtype=np.float32)[:, None] / h
    t = np.clip((yy - start) / (end - start), 0, 1)
    fade = 1 - t * t * (3 - 2 * t)
    alpha = alpha * fade
    rgb = rgb * (0.55 + 0.45 * fade)[..., None]   # the neck darkens as it goes

    scale = LONG_SIDE / max(w, h)
    size = (round(w * scale), round(h * scale))
    out = np.dstack([rgb, alpha])
    out = cv2.resize(out, size, interpolation=cv2.INTER_AREA)
    image = Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype('uint8'))
    image.save(OUT / (name + '.png'), optimize=True)
    return image.size


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, cell in CELLS.items():
        print(name, finish(name, *cell))


if __name__ == '__main__':
    main()
