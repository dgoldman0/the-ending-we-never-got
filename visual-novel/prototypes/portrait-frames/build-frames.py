#!/usr/bin/env python3
"""Draw the portrait-treatment samples in code (prototype, not yet in the game).

Three ways to show a dialogue portrait without the arch, each for the speaker
and the (smaller, quieter) listener:

  vignette  no frame: the bust emerges from the shade, chest dissolving
  oval      a portrait miniature with a fine gilt rim, fading at its base
  halo      the same oval edged by a soft golden glow instead of a line
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
light_relief, GILT, ramp, sun_masks = kit['light_relief'], kit['GILT'], kit['ramp'], kit['sun_masks']
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
    # the halo: gilt light blooming from the oval's edge, outward and a little
    # inward, fading at the base like the portrait; drawn on a larger canvas
    m = 26
    W2, H2 = w + 2 * m, h + 2 * m
    x2, y2 = grid(W2, H2)
    d = dist(x2 - m, y2 - m)
    glow = np.where(d > 0, np.exp(-(d / 7.0) ** 2) * 0.30 + np.exp(-(d / 18.0) ** 2) * 0.10,
                    np.exp(-(d / 2.5) ** 2) * 0.32)
    glow *= base_fade(np.clip(y2 - m, 0, None), h, 0.62)
    colour = np.array([0.93, 0.80, 0.52], np.float32)
    save(np.dstack([np.ones_like(glow)[..., None] * colour, glow.astype(np.float32)]), 'halo-oval-%s.png' % role)


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


def deep_shade():
    """The reading shade in two deeper strengths: still gradients that start
    transparent above the portraits, never solid at the foot of the screen.
    Around the text line (y 874-980) the current shade is about 55% dark;
    'medium' is about 70% and 'strong' about 82%."""
    h = 560
    for name, stops in (('shade-medium.png', [(0, 0), (0.26, 24), (0.48, 150), (0.66, 186), (1, 200)]),
                        ('shade-strong.png', [(0, 0), (0.24, 30), (0.44, 176), (0.62, 212), (1, 225)])):
        alpha = ramp(h, stops) / 255.0
        save(np.dstack([np.zeros((h, 4, 3), np.float32), np.repeat(alpha[:, None], 4, 1)]), name)


def text_pool():
    """A soft dark pool behind the text block only, over the current shade;
    the rest of the band keeps the painting."""
    w, h = 1400, 420
    xx, yy = grid(w, h)
    r = np.sqrt(((xx - w * 0.47) / (w * 0.50)) ** 2 + ((yy - h * 0.52) / (h * 0.46)) ** 2)
    a = (1 - smoothstep((r - 0.22) / 0.78)) * 0.72
    save(np.dstack([np.zeros((h, w, 3), np.float32), a.astype(np.float32)]), 'shade-pool.png')


def shadow_tints():
    """Each graded painting's own shadow colour: the mean colour of its darkest
    fifth in the lower half, as a multiply factor about 30% bright, so the
    shade deepens the scene in its own hue instead of greying it."""
    import json
    tints = {}
    for path in sorted((VN / 'renpy/game/art/lit').glob('*.webp')):
        a = np.asarray(Image.open(path).convert('RGB').resize((480, 270)), np.float32) / 255
        low = a[135:].reshape(-1, 3)
        lum = low @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        dark = low[lum <= np.percentile(lum, 20)].mean(0) + 1e-3
        hue = dark / (dark @ np.array([0.2126, 0.7152, 0.0722], np.float32))
        hue = np.clip(hue, 0.75, 1.3)              # the scene's own hue, not a pushed one
        tints['art/lit/' + path.name] = [round(float(c), 3) for c in np.clip(hue * 0.20, 0.04, 0.4)]
    (UI / 'shadow-tints.json').write_text(json.dumps(tints))


def shade_masks():
    """Where the shade falls (white = full). 'band' spans the width like the
    current shade; 'shaped' is deepest behind the portrait and the text and
    fades toward the right and upward, with a lighter pool under the menu."""
    w, h = 1920, 1080
    xx, yy = grid(w, h)
    band = np.interp(yy, [690, 780, 860, 960, 1080], [0, 0.45, 0.85, 0.95, 1.0])
    left = np.sqrt(((xx - 720) / 1050) ** 2 + ((yy - 960) / 290) ** 2)
    shaped = (1 - smoothstep((left - 0.45) / 0.55)) * np.interp(yy, [680, 780, 870, 1080], [0, 0.5, 0.95, 1.0])
    corner = np.sqrt(((xx - 1830) / 330) ** 2 + ((yy - 1000) / 260) ** 2)
    shaped = np.maximum(shaped, (1 - smoothstep((corner - 0.3) / 0.7)) * 0.6)
    for name, m in (('band', band), ('shaped', shaped)):
        m = m.astype(np.float32)
        save(np.dstack([np.ones_like(m)] * 3 + [m]), 'mask-shade-%s.png' % name)
        f = m.astype(np.float32)
        save(np.dstack([np.ones_like(f)] * 3 + [f]), 'mask-focus-%s.png' % name)


def hairline():
    """A fine gilt line with a faint glow, fading out at both ends."""
    w, h = 1000, 7
    xx, yy = grid(w, h)
    core = np.exp(-((yy - 3.5) / 0.7) ** 2) * 0.95 + np.exp(-((yy - 3.5) / 2.2) ** 2) * 0.25
    ends = smoothstep(np.minimum(xx, w - xx) / 260)
    a = (core * ends).astype(np.float32)
    save(np.dstack([np.ones_like(a)[..., None] * np.array([0.86, 0.72, 0.46], np.float32), a]), 'hairline.png')


def to_lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def lens(lin, r):
    """A lens (disc) blur in linear light, so highlights bloom like a real
    out-of-focus lens rather than smearing like a Gaussian."""
    if r <= 0:
        return lin
    k = int(np.ceil(r)) * 2 + 1
    yy, xx = np.mgrid[0:k, 0:k].astype(np.float32) - k // 2
    disc = np.clip(r + 0.5 - np.sqrt(xx ** 2 + yy ** 2), 0, 1)
    return cv2.filter2D(lin, -1, disc / disc.sum(), borderType=cv2.BORDER_REFLECT)


def soft_masks():
    """The shade for the chosen treatment: deepest behind the portrait and the
    text, fading right and up (no pool under the menu, which is now hidden);
    and the pool behind the pop-up controls."""
    w, h = 1920, 1080
    xx, yy = grid(w, h)
    left = np.sqrt(((xx - 720) / 1050) ** 2 + ((yy - 960) / 290) ** 2)
    shaped = (1 - smoothstep((left - 0.45) / 0.55)) * np.interp(yy, [680, 780, 870, 1080], [0, 0.5, 0.95, 1.0])
    corner = np.sqrt(((xx - 1920) / 640) ** 2 + ((yy - 1080) / 740) ** 2)
    pool = (1 - smoothstep((corner - 0.32) / 0.68)).astype(np.float32)
    for name, m in (('soft', shaped.astype(np.float32)), ('controls', pool)):
        save(np.dstack([np.ones_like(m)] * 3 + [m]), 'mask-shade-%s.png' % name)
    return shaped.astype(np.float32), pool


def soft_paintings(shaped):
    """For each graded painting: a progressive lens blur that deepens toward
    the text (untouched above the shade), with the painting's grain restored
    so it never looks smeared; and an evenly blurred copy for the controls."""
    rng = np.random.default_rng(3)
    noise = cv2.GaussianBlur(rng.normal(0, 1, (1080, 1920)).astype(np.float32), (0, 0), 0.7)
    t = shaped * 4
    weights = [np.clip(1 - np.abs(t - i), 0, 1)[..., None] for i in range(5)]
    for sub in ('soft', 'blur'):
        (UI / sub).mkdir(parents=True, exist_ok=True)
    for path in sorted((VN / 'renpy/game/art/lit').glob('*-intense.webp')):
        src = np.asarray(Image.open(path).convert('RGB').resize((1920, 1080)), np.float32) / 255
        lin = to_lin(src)
        levels = [lin, lens(lin, 3), lens(lin, 7), lens(lin, 13), lens(lin, 20)]
        out = to_srgb(sum(w * l for w, l in zip(weights, levels)))
        lum = out @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        out = out + (noise * 0.045 * shaped * lum * (1 - lum))[..., None]
        Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype('uint8')).save(UI / 'soft' / path.name, quality=90, method=4)
        blur = to_srgb(lens(lin, 12))
        Image.fromarray((np.clip(blur, 0, 1) * 255 + 0.5).astype('uint8')).save(UI / 'blur' / path.name, quality=88, method=4)


def engraved_line(w, name, glow=True):
    """A hairline that reads on white and on black: a dark cut beneath, a gilt
    line and a faint highlight above, fading out at both ends."""
    h = 11
    xx, yy = grid(w, h)
    ends = smoothstep(np.minimum(xx, w - xx) / (w * 0.26))
    cut = np.exp(-((yy - 6.6) / 0.9) ** 2) * 0.55
    gilt = np.exp(-((yy - 5.2) / 0.75) ** 2)
    shine = np.exp(-((yy - 4.2) / 0.6) ** 2) * 0.35
    halo = np.exp(-((yy - 5.2) / 2.6) ** 2) * (0.22 if glow else 0)
    gold = np.array([0.86, 0.71, 0.44], np.float32)
    rgb = (gold * (gilt + halo)[..., None] + np.array([1.0, 0.95, 0.8], np.float32) * shine[..., None]
           + np.array([0.09, 0.06, 0.04], np.float32) * cut[..., None])
    a = np.clip(gilt + shine + halo + cut, 0, 1)
    rgb = rgb / np.maximum(a, 1e-4)[..., None]
    save(np.dstack([np.clip(rgb, 0, 1), (a * ends).astype(np.float32)]), name)


def trigger():
    """The controls' trigger: the temple's twelve-ray sun in gilt relief on a
    soft shadow, so it reads on white marble and in the dark; and the glow
    that breathes around it when something can be looked at more closely."""
    S = 44
    W = S * OSS
    disc, ray, ring = sun_masks((W, W), (W / 2, W / 2), W * 0.2, W * 0.42)
    dome = kit['dome']
    height = np.maximum(dome(disc, W * 0.12) * 1.2 - ring * 0.3, dome(ray, W * 0.03) * 0.8)
    cover = np.clip(disc + ray, 0, 1)
    albedo = np.ones(height.shape + (3,), np.float32) * GILT
    rgba = light_relief(cv2.GaussianBlur(height.astype(np.float32), (0, 0), 0.5 * OSS), albedo,
                        np.ones_like(height) * 0.9, cover.astype(np.float32))
    rgba = cv2.resize(rgba, (S, S), interpolation=cv2.INTER_AREA)
    xx, yy = grid(S, S)
    r = np.sqrt((xx - S / 2) ** 2 + (yy - S / 2 - 1) ** 2)
    shadow = np.exp(-(r / 13) ** 2) * 0.55
    a = rgba[..., 3] + shadow * (1 - rgba[..., 3])
    rgb = (rgba[..., :3] * rgba[..., 3:4] + np.array([0.05, 0.04, 0.03], np.float32) * (shadow * (1 - rgba[..., 3]))[..., None]) / np.maximum(a, 1e-4)[..., None]
    save(np.dstack([rgb, a]), 'ctl-sun.png')
    G = 96
    xx, yy = grid(G, G)
    r = np.sqrt((xx - G / 2) ** 2 + (yy - G / 2) ** 2)
    glow = (np.exp(-((r - 17) / 7) ** 2) * 0.55 + np.exp(-(r / 28) ** 2) * 0.25).astype(np.float32)
    save(np.dstack([np.ones_like(glow)[..., None] * np.array([0.98, 0.84, 0.55], np.float32), glow]), 'ctl-glow.png')


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
    deep_shade()
    text_pool()
    shadow_tints()
    shade_masks()
    hairline()
    shaped, _ = soft_masks()
    engraved_line(1000, 'hairline-engraved.png')
    engraved_line(150, 'ctl-underline.png', glow=False)
    trigger()
    soft_paintings(shaped)
    lozenge()
    print('portrait-frame samples written to', UI.relative_to(VN))


if __name__ == '__main__':
    main()
