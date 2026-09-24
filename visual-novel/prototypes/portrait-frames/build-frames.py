#!/usr/bin/env python3
"""Draw the portrait-treatment samples in code (prototype, not yet in the game).

Three ways to show a dialogue portrait without the arch, each for the speaker
and the (smaller, quieter) listener:

  vignette  no frame: the bust emerges from the shade, chest dissolving
  oval      a portrait miniature with a fine gilt rim, fading at its base
  rect      a plain miniature with a hairline gilt rim, fading at its base

and a lacquer-toned version of the reading shade (deep celadon with grain,
the same fade as the current shade).

    python3 visual-novel/prototypes/portrait-frames/build-frames.py
"""
from pathlib import Path
import runpy

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
VN = HERE.parents[1]
UI = HERE / 'ui'
kit = runpy.run_path(str(VN / 'tools/build-ui-assets.py'), run_name='frames')
light_relief, GILT, ramp = kit['light_relief'], kit['GILT'], kit['ramp']
OSS = 3

SIZES = {'vignette': {'speaker': (270, 310), 'listener': (150, 172)},
         'oval': {'speaker': (224, 280), 'listener': (132, 165)},
         'rect': {'speaker': (208, 262), 'listener': (124, 156)}}


def smoothstep(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def save(array, name):
    UI.mkdir(parents=True, exist_ok=True)
    Image.fromarray((np.clip(array, 0, 1) * 255 + 0.5).astype('uint8')).save(UI / name, optimize=True)


def grid(w, h, scale=1):
    yy, xx = np.mgrid[0:h * scale, 0:w * scale].astype(np.float32) + 0.5
    return xx / scale, yy / scale


def base_fade(yy, h, start):
    """The lower part of a portrait dissolves into the shade: no hard bottom."""
    return 1 - smoothstep((yy / h - start) / (1 - start))


def rim(dist, w, h, fade_start):
    """A fine gilt ridge along a distance field's zero line, fading at the base."""
    xx, yy = grid(w, h, OSS)
    d = dist(xx, yy)
    x = np.clip(1 - np.abs(d) / 0.9, 0, 1)
    height = np.sqrt(x * (2 - x)).astype(np.float32)
    albedo = np.ones(height.shape + (3,), np.float32) * GILT
    rgba = light_relief(cv2.GaussianBlur(height, (0, 0), 0.5 * OSS), albedo, np.ones_like(height) * 0.9,
                        np.clip(height * 3, 0, 1).astype(np.float32))
    rgba = cv2.resize(rgba, (w, h), interpolation=cv2.INTER_AREA)
    _, y1 = grid(w, h)
    rgba[..., 3] *= base_fade(y1, h, fade_start) * 0.95
    return rgba


def vignette(role):
    w, h = SIZES['vignette'][role]
    xx, yy = grid(w, h)
    r = np.sqrt(((xx - w * 0.5) / (w * 0.5)) ** 2 + ((yy - h * 0.44) / (h * 0.56)) ** 2)
    mask = (1 - smoothstep((r - 0.70) / 0.30)) * base_fade(yy, h, 0.58)
    save(np.dstack([np.ones_like(mask)] * 3 + [mask]), 'mask-vignette-%s.png' % role)


def oval(role):
    w, h = SIZES['oval'][role]
    rx, ry = w / 2 - 3, h / 2 - 3

    def dist(x, y):
        r = np.sqrt(((x - w / 2) / rx) ** 2 + ((y - h / 2) / ry) ** 2)
        return (r - 1) * min(rx, ry)
    xx, yy = grid(w, h)
    inside = np.clip(0.5 - dist(xx, yy), 0, 1) * base_fade(yy, h, 0.70)
    save(np.dstack([np.ones_like(inside)] * 3 + [inside]), 'mask-oval-%s.png' % role)
    save(rim(dist, w, h, 0.66), 'rim-oval-%s.png' % role)


def rect(role):
    w, h = SIZES['rect'][role]

    def dist(x, y):
        return np.maximum(np.abs(x - w / 2) - (w / 2 - 3), np.abs(y - h / 2) - (h / 2 - 3))
    xx, yy = grid(w, h)
    inside = np.clip(0.5 - dist(xx, yy), 0, 1) * base_fade(yy, h, 0.70)
    save(np.dstack([np.ones_like(inside)] * 3 + [inside]), 'mask-rect-%s.png' % role)
    save(rim(dist, w, h, 0.66), 'rim-rect-%s.png' % role)


def lacquer_shade():
    """The reading shade in deep celadon lacquer instead of flat black, with a
    faint grain; the same fade as the current shade, so the painting shows."""
    w, h = 1920, 560
    alpha = ramp(h, [(0, 0), (0.22, 18), (0.52, 128), (0.78, 205), (1, 232)]) / 255.0
    rng = np.random.default_rng(9)
    grain = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 0.8) * 0.012
    low = cv2.resize(rng.normal(0, 1, (4, 16)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) * 0.008
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    base = np.array([0.075, 0.118, 0.112], np.float32) * (1 - t[..., None]) + np.array([0.035, 0.055, 0.056], np.float32) * t[..., None]
    rgb = base + (grain + low)[..., None]
    save(np.dstack([rgb, np.repeat(alpha[:, None], w, 1)]), 'shade-lacquer.png')


def lozenge():
    s = 13 * 4
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float32) + 0.5
    d = (np.abs(xx - s / 2) + np.abs(yy - s / 2) * 1.35) / (s / 2)
    rgba = np.zeros((s, s, 4), np.float32)
    rgba[..., :3] = np.array((205, 176, 118), np.float32) / 255
    rgba[..., 3] = np.clip((1 - d) * 6, 0, 1) * 0.95
    UI.mkdir(parents=True, exist_ok=True)
    Image.fromarray((rgba * 255).astype('uint8')).resize((13, 13), Image.LANCZOS).save(UI / 'lozenge-gilt.png')


def main():
    for role in ('speaker', 'listener'):
        vignette(role)
        oval(role)
        rect(role)
    lacquer_shade()
    lozenge()
    print('portrait-frame samples written to', UI.relative_to(VN))


if __name__ == '__main__':
    main()
