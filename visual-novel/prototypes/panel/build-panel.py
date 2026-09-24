#!/usr/bin/env python3
"""Draw the reading-panel samples in code (prototype, not yet in the game).

Two surfaces for the lower band of the reading screen, each with one fine
engraved border across its width, portrait niches set into the surface and a
small lozenge in place of the continue knot:

  lacquer  deep celadon-black lacquer, gilt engraving
  vellum   warm vellum, ink and gilt engraving

    python3 visual-novel/prototypes/panel/build-panel.py
"""
from pathlib import Path
import math
import runpy

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
VN = HERE.parents[1]
UI = HERE / 'ui'
kit = runpy.run_path(str(VN / 'tools/build-ui-assets.py'), run_name='panel')
light_relief, smoothstep, sun_masks, closed_arch_sdf = kit['light_relief'], kit['smoothstep'], kit['sun_masks'], kit['closed_arch_sdf']
GILT = kit['GILT']
OSS = 3

W, H = 1920, 344          # panel image, placed at y = 736
TOP = 36                  # the surface starts here; above it, a soft cast shadow
SPEAKER = (120, 800, 228, 256)    # portrait niches in screen coordinates
LISTENER = (1490, 846, 150, 168)
Y0 = 1080 - H

SURFACES = {
    'lacquer': dict(top=(20, 29, 29), bottom=(9, 13, 14), grain=2.2, sheen=0.05,
                    groove=(0, 0, 0), line=GILT, ink_line=None),
    'vellum': dict(top=(226, 216, 194), bottom=(206, 194, 170), grain=5.0, sheen=0.0,
                   groove=(70, 52, 34), line=GILT, ink_line=(92, 70, 48)),
}


def save(img, name):
    UI.mkdir(parents=True, exist_ok=True)
    img.save(UI / name, optimize=True)


def surface(kind):
    s = SURFACES[kind]
    rng = np.random.default_rng(5)
    h = H - TOP
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    rgb = np.array(s['top'], np.float32) * (1 - t) + np.array(s['bottom'], np.float32) * t
    rgb = np.repeat(rgb, W, axis=1)
    fine = cv2.GaussianBlur(rng.normal(0, 1, (h, W)).astype(np.float32), (0, 0), 0.8)
    low = cv2.resize(rng.normal(0, 1, (6, 24)).astype(np.float32), (W, h), interpolation=cv2.INTER_CUBIC)
    rgb += (fine * s['grain'] + low * s['grain'] * 0.5)[..., None]
    if kind == 'vellum':
        fibre = cv2.GaussianBlur(rng.normal(0, 1, (h, W)).astype(np.float32), (0, 0), sigmaX=6, sigmaY=0.5)
        rgb += fibre[..., None] * 9
        yy, xx = np.mgrid[0:h, 0:W].astype(np.float32)
        edge = np.clip(1 - np.minimum(xx, W - xx) / 260, 0, 1) ** 2
        rgb *= (1 - 0.10 * edge)[..., None]
    if s['sheen']:
        # a long soft reflection across the lacquer, as from a window
        yy, xx = np.mgrid[0:h, 0:W].astype(np.float32)
        band = np.exp(-((yy - 38 - xx * 0.02) / 26) ** 2) * (0.6 + 0.4 * np.sin(xx / W * math.pi))
        rgb += band[..., None] * 255 * s['sheen']
    out = np.zeros((H, W, 4), np.float32)
    out[TOP:, :, :3] = rgb
    out[TOP:, :, 3] = 255
    # cast shadow onto the painting above the panel
    shade = (np.linspace(0, 1, TOP) ** 2.2 * (110 if kind == 'lacquer' else 70)).astype(np.float32)
    out[:TOP, :, 3] = shade[:, None]
    return out


def engraved(height_hi, cover_hi, color):
    """Light a supersampled relief as gilt and bring it to screen resolution."""
    albedo = np.ones(height_hi.shape + (3,), np.float32) * np.array(color, np.float32)
    rgba = light_relief(cv2.GaussianBlur(height_hi, (0, 0), 0.5 * OSS), albedo, np.ones_like(height_hi) * 0.9, cover_hi)
    return cv2.resize(rgba, (height_hi.shape[1] // OSS, height_hi.shape[0] // OSS), interpolation=cv2.INTER_AREA)


def ridge(dist, width):
    """A rounded ridge of the given width along a distance field's zero line."""
    x = np.clip(1 - np.abs(dist) / (width / 2), 0, 1)
    return np.sqrt(x * (2 - x))


def border(kind):
    """One fine engraved border along the panel's top edge: two hairlines with
    a row of beads between them, broken at the centre by the temple sun."""
    hs, ws = 70 * OSS, W * OSS
    yy, xx = np.mgrid[0:hs, 0:ws].astype(np.float32) / OSS
    cx, cy = W / 2, TOP + 8
    gap = np.clip((np.abs(xx - cx) - 30) / 4, 0, 1)
    a = ridge(yy - (TOP + 3), 1.8) * gap
    b = ridge(yy - (TOP + 13), 1.1) * gap
    beads = np.zeros_like(yy)
    step = 18
    for x0 in np.arange(cx % step, W, step):
        if abs(x0 - cx) < 40:
            continue
        beads = np.maximum(beads, ridge(np.sqrt((xx - x0) ** 2 + (yy - (TOP + 8)) ** 2), 2.8))
    height = np.maximum(np.maximum(a, b * 0.8), beads * 0.9)
    disc, ray, ring = sun_masks((ws, hs), (cx * OSS, cy * OSS), 9 * OSS, 17 * OSS)
    dome = kit['dome']
    height = np.maximum(height, np.maximum(dome(disc, 6 * OSS) * 1.2 - ring * 0.3, dome(ray, 1.2 * OSS) * 0.8))
    cover = np.clip(height * 3, 0, 1)
    rgba = engraved(height, cover, GILT)
    # engraving is cut, not applied: a dark groove sits just under each line
    groove = np.zeros((70, W), np.float32)
    for y0, w0 in ((TOP + 5, 1.6), (TOP + 15, 1.0)):
        groove = np.maximum(groove, np.clip(1 - np.abs(np.arange(70)[:, None] - y0) / w0, 0, 1) * np.clip((np.abs(np.arange(W)[None, :] - cx) - 30) / 4, 0, 1))
    return rgba, groove


def niche(kind, role):
    """An engraved arch around a portrait set into the surface, and the shading
    that sinks the portrait into it."""
    x, y, w, h = SPEAKER if role == 'speaker' else LISTENER
    pad = 12
    Wn, Hn = (w + 2 * pad) * OSS, (h + 2 * pad) * OSS
    sdf, _, _ = closed_arch_sdf(Wn, Hn, inset=(pad - 7) * OSS)
    sdf = sdf / OSS
    height = ridge(sdf, 1.6)
    rgba = engraved(height.astype(np.float32), np.clip(height * 3, 0, 1).astype(np.float32), GILT)
    # recess: the space between the engraving and the portrait falls into shadow
    inner, _, _ = closed_arch_sdf(w + 2 * pad, h + 2 * pad, inset=pad)
    ring, _, _ = closed_arch_sdf(w + 2 * pad, h + 2 * pad, inset=pad - 7)
    recess = ((ring > 0) & (inner < 1)).astype(np.float32) * (0.55 if kind == 'lacquer' else 0.22)
    tint = np.array((60, 44, 28) if kind == 'vellum' else (0, 0, 0), np.float32) / 255
    shade = np.zeros((h + 2 * pad, w + 2 * pad, 4), np.float32)
    shade[..., :3] = tint
    shade[..., 3] = cv2.GaussianBlur(recess, (0, 0), 1.2)
    # inner shadow over the portrait's edge, heavier at the top left (light from there);
    # drawn over the portrait by the screen, so kept as its own image
    d = np.clip(inner / 16.0, 0, 1)
    yy, xx = np.mgrid[0:h + 2 * pad, 0:w + 2 * pad].astype(np.float32)
    bias = 0.75 + 0.25 * np.clip(1 - (xx + yy) / (w + h), 0, 1)
    over = np.zeros_like(shade)
    over[..., :3] = tint
    over[..., 3] = (inner > 0) * (1 - d) ** 2 * 0.55 * bias
    return rgba, shade, over, (x - pad, y - pad)


def lozenge(color, name, size=13):
    s = size * 4
    img = np.zeros((s, s), np.float32)
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float32) + 0.5
    d = (np.abs(xx - s / 2) + np.abs(yy - s / 2) * 1.35) / (s / 2)
    img = np.clip((1 - d) * 6, 0, 1)
    rgba = np.zeros((s, s, 4), np.float32)
    rgba[..., :3] = np.array(color, np.float32) / 255
    rgba[..., 3] = img * 0.95
    save(Image.fromarray((rgba * 255).astype('uint8')).resize((size, size), Image.LANCZOS), name)


def main():
    for kind in SURFACES:
        panel = surface(kind) / 255.0
        panel[..., 3] = panel[..., 3]
        edge, groove = border(kind)
        g = SURFACES[kind]['groove']
        top = panel[:70]
        top[..., :3] = top[..., :3] * (1 - groove[..., None] * 0.8) + np.array(g, np.float32)[None, None] / 255 * groove[..., None] * 0.8
        a = edge[..., 3:4]
        top[..., :3] = top[..., :3] * (1 - a) + edge[..., :3] * a
        top[..., 3] = np.maximum(top[..., 3], edge[..., 3])
        for role in ('speaker', 'listener'):
            line, shade, over, (nx, ny) = niche(kind, role)
            ny -= Y0
            hh, ww = shade.shape[:2]
            reg = panel[ny:ny + hh, nx:nx + ww]
            sa = shade[..., 3:4]
            reg[..., :3] = reg[..., :3] * (1 - sa * (reg[..., 3:4] > 0)) + shade[..., :3] * sa * (reg[..., 3:4] > 0)
            la = line[..., 3:4]
            reg[..., :3] = reg[..., :3] * (1 - la) + line[..., :3] * la
            save(Image.fromarray((np.clip(over, 0, 1) * 255).astype('uint8')), 'niche-shade-%s-%s.png' % (role, kind))
        save(Image.fromarray((np.clip(panel, 0, 1) * 255 + 0.5).astype('uint8')), 'panel-%s.png' % kind)
    lozenge((205, 176, 118), 'lozenge-gilt.png')
    lozenge((138, 99, 52), 'lozenge-ink.png')
    print('panel samples written to', UI.relative_to(VN))


if __name__ == '__main__':
    main()
