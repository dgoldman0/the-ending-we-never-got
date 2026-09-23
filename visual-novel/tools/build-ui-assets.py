#!/usr/bin/env python3
"""Draw the reading interface's image components in code.

Every file under renpy/game/ui/ is produced here from geometry, gradients and
seeded noise; nothing is diffusion-generated. Rerun after changing a shape:

    python3 visual-novel/tools/build-ui-assets.py
"""
from pathlib import Path
import math

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / 'renpy/game/ui'
SS = 4  # supersampling for anti-aliased line work

GOLD = (205, 176, 118)
INK = (8, 11, 14)


def smooth(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def ramp(height, stops):
    """A 1-pixel-wide alpha ramp from (fraction, alpha) stops."""
    col = np.zeros(height, 'float32')
    for y in range(height):
        f = y / max(1, height - 1)
        for (f0, a0), (f1, a1) in zip(stops, stops[1:]):
            if f0 <= f <= f1:
                col[y] = a0 + (a1 - a0) * smooth((f - f0) / max(1e-6, f1 - f0))
                break
    return col


def save(image, name):
    path = UI / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if name.endswith('.webp'):
        image.save(path, quality=86, method=6)
    else:
        image.save(path, optimize=True)


def scrim():
    """Bottom reading shade. Scaled horizontally in the engine."""
    height = 560
    alpha = ramp(height, [(0, 0), (0.22, 18), (0.52, 128), (0.78, 205), (1, 232)])
    image = Image.new('RGBA', (4, height), INK + (0,))
    image.putalpha(Image.fromarray(np.repeat(alpha[:, None], 4, 1).clip(0, 255).astype('uint8')))
    save(image, 'scrim.png')
    # A soft left pool beneath the portraits, so faces emerge from shadow.
    w, h = 760, 460
    yy, xx = np.mgrid[0:h, 0:w].astype('float32')
    r = np.sqrt(((xx - 250) / 420) ** 2 + ((yy - h) / 380) ** 2)
    a = (1 - np.clip(r, 0, 1)) ** 1.6 * 150
    pool = Image.new('RGBA', (w, h), INK + (0,))
    pool.putalpha(Image.fromarray(a.clip(0, 255).astype('uint8')))
    save(pool, 'portrait-pool.png')


def arch_shape(w, h, inset=0.0):
    """Supersampled arch silhouette as an L image at w*SS x h*SS."""
    W, H = w * SS, h * SS
    m = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(m)
    i = inset * SS
    r = (W - 2 * i) / 2
    d.ellipse([i, i, W - i, i + 2 * r], fill=255)
    d.rectangle([i, i + r, W - i, H], fill=255)
    return m


def arch(w, h, name, feather=0.30):
    shape = arch_shape(w, h).resize((w, h), Image.LANCZOS)
    fade = Image.fromarray(np.repeat(ramp(h, [(0, 255), (1 - feather, 255), (1, 0)])[:, None], w, 1).astype('uint8'))
    # AlphaMask reads the mask's alpha channel, so the shape must be alpha.
    mask = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    mask.putalpha(ImageChops.multiply(shape, fade))
    save(mask, 'arch-mask-' + name + '.png')
    # Two hairlines: a firm outer thread and a faint inner one.
    lines = Image.new('L', (w * SS, h * SS), 0)
    for inset, width, level in ((0.6, 1.5, 230), (5.5, 0.9, 110)):
        outer = arch_shape(w, h, inset)
        inner = arch_shape(w, h, inset + width)
        ring = ImageChops.subtract(outer, inner).point(lambda v: v * level // 255)
        lines = ImageChops.lighter(lines, ring)
    lines = lines.resize((w, h), Image.LANCZOS)
    fade = Image.fromarray(np.repeat(ramp(h, [(0, 255), (1 - feather - 0.08, 255), (1 - 0.06, 0), (1, 0)])[:, None], w, 1).astype('uint8'))
    line_layer = Image.new('RGBA', (w, h), GOLD + (0,))
    line_layer.putalpha(ImageChops.multiply(lines, fade))
    save(line_layer, 'arch-line-' + name + '.png')
    # Dark backing with a soft interior light, behind a head-only portrait.
    yy, xx = np.mgrid[0:h, 0:w].astype('float32')
    r = np.sqrt(((xx - w * 0.5) / (w * 0.62)) ** 2 + ((yy - h * 0.40) / (h * 0.55)) ** 2)
    base = np.array((23, 27, 31), 'float32') * (1 - 0.55 * np.clip(r, 0, 1))[..., None]
    back = Image.fromarray(base.clip(0, 255).astype('uint8')).convert('RGBA')
    save(back, 'arch-back-' + name + '.png')
    # Shadow that closes in from the arch edges over the portrait itself.
    v = np.sqrt(((xx - w * 0.5) / (w * 0.56)) ** 2 + ((yy - h * 0.44) / (h * 0.60)) ** 2)
    shade = (np.clip(v - 0.50, 0, 0.5) / 0.5) ** 1.15 * 240
    vignette = Image.new('RGBA', (w, h), INK + (0,))
    vignette.putalpha(Image.fromarray(shade.clip(0, 255).astype('uint8')))
    save(vignette, 'arch-vignette-' + name + '.png')


def thread_line(length, name, knot=True, alpha=220, wave=0.8, color=GOLD):
    """An irregular gold thread, optionally starting with a small knot."""
    GOLD = color
    pad = 12
    W, H = (length + 2 * pad) * SS, 24 * SS
    image = Image.new('RGBA', (W, H), GOLD + (0,))
    d = ImageDraw.Draw(image)
    pts = [(pad * SS + i, H / 2 + math.sin(i / (37.0 * SS / 4)) * wave * SS)
           for i in range(0, length * SS, 3)]
    d.line(pts, fill=GOLD + (alpha,), width=int(1.25 * SS))
    if knot:
        cx, cy = pad * SS, H / 2
        d.ellipse([cx - 4.2 * SS, cy - 4.2 * SS, cx + 4.2 * SS, cy + 4.2 * SS], outline=GOLD + (alpha,), width=int(1.3 * SS))
        d.ellipse([cx - 1.7 * SS, cy - 1.7 * SS, cx + 1.7 * SS, cy + 1.7 * SS], fill=GOLD + (alpha,))
    save(image.resize((length + 2 * pad, 24), Image.LANCZOS), name)


def knot(size, name, alpha=235):
    W = size * SS
    image = Image.new('RGBA', (W, W), GOLD + (0,))
    d = ImageDraw.Draw(image)
    c = W / 2
    ring = size * 0.30 * SS
    d.ellipse([c - ring, c - ring, c + ring, c + ring], outline=GOLD + (alpha,), width=int(1.4 * SS))
    dot = size * 0.12 * SS
    d.ellipse([c - dot, c - dot, c + dot, c + dot], fill=GOLD + (alpha,))
    save(image.resize((size, size), Image.LANCZOS), name)


def rule(length, name, alpha=150):
    """Hairline that fades at both ends; used between menu groups."""
    a = np.array([smooth(min(x / (length * 0.18), (length - x) / (length * 0.18), 1.0)) * alpha
                  for x in range(length)], 'float32')
    image = Image.new('RGBA', (length, 2), GOLD + (0,))
    image.putalpha(Image.fromarray(np.repeat(a[None, :], 2, 0).astype('uint8')))
    save(image, name)


def page(name, base, grain, vignette, warmth=(0, 0, 0), seed=7):
    """Full-screen reading page: paper or ink with low-frequency mottling."""
    w, h = 1920, 1080
    rng = np.random.default_rng(seed)
    fine = rng.normal(0, 1, (h, w)).astype('float32')
    fine = np.array(Image.fromarray(((fine * 36) + 128).clip(0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.7)), 'float32') - 128
    low = rng.normal(0, 1, (12, 21)).astype('float32')
    low = np.array(Image.fromarray(((low * 50) + 128).clip(0, 255).astype('uint8')).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(70)), 'float32') - 128
    fibre = rng.normal(0, 1, (h // 6, w)).astype('float32')
    fibre = np.array(Image.fromarray(((fibre * 40) + 128).clip(0, 255).astype('uint8')).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur((2.5, 0.4))), 'float32') - 128
    arr = np.zeros((h, w, 3), 'float32') + np.array(base, 'float32') + np.array(warmth, 'float32')
    arr += (fine[..., None] * 0.07 + low[..., None] * 0.11 + fibre[..., None] * 0.035) * grain
    yy, xx = np.mgrid[0:h, 0:w].astype('float32')
    r = np.sqrt(((xx - w / 2) / (w * 0.60)) ** 2 + ((yy - h * 0.46) / (h * 0.66)) ** 2)
    arr *= (1 - vignette * np.clip(r - 0.42, 0, 1) ** 1.5)[..., None]
    save(Image.fromarray(arr.clip(0, 255).astype('uint8')), name)


def hshade(name, width, stops, height=4):
    """Horizontal shade, scaled vertically in the engine."""
    alpha = ramp(width, stops)
    image = Image.new('RGBA', (width, height), INK + (0,))
    image.putalpha(Image.fromarray(np.repeat(alpha[None, :], height, 0).clip(0, 255).astype('uint8')))
    save(image, name)


def text_pool(name, w, h, alpha=150):
    """Soft dark ellipse behind text placed inside a painting's own shadow."""
    yy, xx = np.mgrid[0:h, 0:w].astype('float32')
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a = (1 - np.clip(r, 0, 1)) ** 1.4 * alpha
    image = Image.new('RGBA', (w, h), INK + (0,))
    image.putalpha(Image.fromarray(a.clip(0, 255).astype('uint8')))
    save(image, name)


def frame_line(name, size=48, alpha=170):
    """A hairline gold border for detail images and save thumbnails."""
    image = Image.new('RGBA', (size, size), GOLD + (0,))
    d = ImageDraw.Draw(image)
    d.rectangle([0, 0, size - 1, size - 1], outline=GOLD + (alpha,), width=1)
    save(image, name)


def glow(size, name, color, alpha):
    yy, xx = np.mgrid[0:size, 0:size].astype('float32')
    r = np.sqrt((xx - size / 2) ** 2 + (yy - size / 2) ** 2) / (size / 2)
    a = (1 - np.clip(r, 0, 1)) ** 2.2 * alpha
    image = Image.new('RGBA', (size, size), color + (0,))
    image.putalpha(Image.fromarray(a.clip(0, 255).astype('uint8')))
    save(image, name)


def main():
    scrim()
    arch(236, 300, 'speaker')
    arch(150, 191, 'listener')
    thread_line(30, 'thread-name.png')
    thread_line(150, 'thread-heading.png')
    thread_line(150, 'thread-heading-ink.png', color=(122, 88, 46))
    thread_line(360, 'thread-long.png', knot=False, alpha=180, wave=1.2)
    knot(26, 'knot.png')
    knot(18, 'knot-small.png', alpha=220)
    rule(420, 'rule.png')
    rule(1100, 'rule-wide.png', alpha=120)
    # Pages follow the scene's light: day vellum, dusk slate, night ink.
    page('page-day.webp', (224, 215, 196), 1.5, 0.42)
    page('page-day-soft.webp', (199, 191, 174), 1.3, 0.38)
    page('page-dusk.webp', (35, 42, 51), 1.0, 0.55)
    page('page-dusk-soft.webp', (45, 52, 60), 1.0, 0.45)
    page('page-night.webp', (17, 19, 22), 0.9, 0.65)
    page('page-night-soft.webp', (30, 32, 35), 0.9, 0.5)
    page('menu-ground.webp', (13, 16, 19), 0.8, 0.55, seed=11)
    glow(420, 'candle-glow.png', (255, 196, 120), 120)
    hshade('title-shade.png', 1920, [(0, 214), (0.22, 170), (0.48, 40), (0.62, 0), (1, 0)])
    text_pool('text-pool.png', 900, 420)
    edge = Image.new('RGBA', (4, 220), (11, 16, 20, 0))
    edge.putalpha(Image.fromarray(np.repeat(ramp(220, [(0, 0), (1, 255)])[:, None], 4, 1).clip(0, 255).astype('uint8')))
    save(edge, 'edge-fade.png')
    frame_line('frame-line.png')
    print('UI components written to', UI.relative_to(ROOT.parent))


if __name__ == '__main__':
    main()
