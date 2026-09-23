#!/usr/bin/env python3
"""Grade every scene image into the three light registers, in both modes.

The original timeline's light is wrong on purpose, and it stays wrong for as
long as the scene is read; nothing fades back to comfort. Earlier grades got
there by flattening the whole tonal range (milky white, near-black), which
erased what people need to see. Here the light is distorted while local
detail is separated out (an edge-aware split in log luminance) and put back:

  bright    blinding at the light: white-hot clipped glare that spills over
            edges, red halation fringes, colour splitting toward the frame
            edges; figures stay contrasty and legible
  ordinary  never comfortable: sallow highlights and cold teal shade, retained
            silver (bleach bypass), uneven exposure with hot patches, window
            halation, a vignette closing in, fine grain
  night     dismal: large-scale light sunk toward the scene's own sources with
            a floor so shapes survive, cold blue-grey shade, warm sources
            glowing with halation, heavy vignette, grain

Softened uses the same operations at lower strength, so both modes always come
from one source and match exactly.

S001-S005 stages are composited from their layers (the Softened grades, which
are the least processed) before grading, so glare crosses figure edges the way
light does. Staging paintings for S006 onward are graded from the painting as
delivered. Outputs go to renpy/game/art/lit/ with lit-assets.json; the game
uses them automatically.

    python3 visual-novel/tools/grade-light.py          # grade what is missing
    python3 visual-novel/tools/grade-light.py --force  # regrade everything
"""
from pathlib import Path
import argparse
import json
import runpy

import cv2
import numpy as np
from PIL import Image

VN = Path(__file__).resolve().parents[1]
GAME = VN / 'renpy/game'
OUT = GAME / 'art/lit'
MANIFEST = GAME / 'lit-assets.json'
SIZE = (1920, 1080)
QUALITY = 90


# ------------------------------------------------------------ colour helpers

def to_lin(s):
    return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)


def to_srgb(l):
    l = np.clip(l, 0, 1)
    return np.where(l <= 0.0031308, l * 12.92, 1.055 * np.power(l, 1 / 2.4) - 0.055)


def lum(l):
    return l[..., 0] * 0.2126 + l[..., 1] * 0.7152 + l[..., 2] * 0.0722


SCALE = [1.0]  # blur radii are set for 1920 px wide images; smaller images scale them


def blur(x, sigma):
    sigma = max(0.8, sigma * SCALE[0])
    k = int(sigma * 3) * 2 + 1
    return cv2.GaussianBlur(x, (k, k), sigma, borderType=cv2.BORDER_REFLECT)


def box(x, r):
    return cv2.boxFilter(x, -1, (2 * r + 1, 2 * r + 1), normalize=True, borderType=cv2.BORDER_REFLECT)


def guided(i, r, eps):
    """He et al. guided filter, the image as its own guide (edge-aware smoothing)."""
    mean = box(i, r)
    var = box(i * i, r) - mean * mean
    a = var / (var + eps)
    b = mean - a * mean
    return box(a, r) * i + box(b, r)


def base_detail(l, sigma=14, eps=0.12):
    """Split log luminance into large-scale light (base) and texture (detail)."""
    lg = np.log(l + 1e-4).astype(np.float32)
    base = guided(lg, max(2, int(sigma * SCALE[0])), eps)
    return base, lg - base


def relight(lin, base_fn, detail_gain):
    """Tone the large-scale light with base_fn and keep local detail."""
    l = lum(lin) + 1e-4
    base, detail = base_detail(l)
    return lin * (np.exp(base_fn(base) + detail * detail_gain) / l)[..., None]


def hable(x):
    a, b, c, d, e, f = 0.15, 0.50, 0.10, 0.20, 0.02, 0.30
    return ((x * (a * x + c * b) + d * e) / (x * (a * x + b) + d * f)) - e / f


def overlay(a, b):
    return np.where(a < 0.5, 2 * a * b, 1 - 2 * (1 - a) * (1 - b))


def bleach(s, amount):
    """Retained silver: harder contrast, drained colour."""
    l = np.repeat(lum(s)[..., None], 3, axis=2)
    return s * (1 - amount) + np.clip(overlay(s, l), 0, 1) * amount


def split_tone(s, high, low, amount):
    l = lum(s)[..., None]
    w = np.clip((l - 0.2) / 0.6, 0, 1)
    tint = np.array(low, np.float32) * (1 - w) + np.array(high, np.float32) * w
    return s * (1 - amount) + s * tint * amount


def aberration(s, k):
    """Colour splitting that grows with the square of the distance from centre."""
    if k <= 0:
        return s
    h, w = s.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2.0, h / 2.0
    r2 = ((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2
    out = s.copy()
    for channel, sign in ((0, 1.0), (2, -1.0)):
        scale = 1.0 + sign * k * r2
        out[..., channel] = cv2.remap(s[..., channel], cx + (xx - cx) / scale, cy + (yy - cy) / scale,
                                      cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return out


def halation(lin, threshold, strength, tint=(1.0, 0.40, 0.20)):
    """Film halation: a red-orange rim around bright edges."""
    hot = np.maximum(lum(lin) - threshold, 0)
    return ((blur(hot, 5) * 0.55 + blur(hot, 16) * 0.45) * strength)[..., None] * np.array(tint, np.float32)


def glow(lin, threshold, strength, tint):
    hot = np.maximum(lin - threshold, 0)
    return (blur(hot, 8) * 0.35 + blur(hot, 36) * 0.35 + blur(hot, 120) * 0.4) * strength * np.array(tint, np.float32)


def uneven(shape, seed, amount):
    """A low-frequency exposure field: some places too hot, some too dim."""
    rng = np.random.default_rng(seed)
    h, w = shape[:2]
    field = cv2.resize(rng.normal(0, 1, (4, 7)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
    field = blur(field, 80)
    field /= (np.abs(field).max() + 1e-6)
    return (1 + field * amount)[..., None]


def vignette(s, amount, start=0.45):
    h, w = s.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    return s * (1 - amount * np.clip(r - start, 0, 1) ** 1.3)[..., None]


def grain(s, amount, seed=11):
    rng = np.random.default_rng(seed)
    h, w = s.shape[:2]
    noise = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 0.7)
    l = lum(np.clip(s, 0, 1))
    return s + (noise * amount * 4 * l * (1 - l))[..., None]


# ------------------------------------------------------------ the registers

def bright(src, k):
    lin0 = to_lin(src) * uneven(src.shape, 3, 0.10 * k)
    _, detail0 = base_detail(lum(lin0) + 1e-4)
    lin = lin0 * (1 + 0.9 * k)
    hot = np.maximum(lin - 0.95, 0)
    spill = (blur(hot, 4) * 0.3 + blur(hot, 14) * 0.35 + blur(hot, 45) * 0.35 + blur(hot, 130) * 0.3) * 1.6 * k
    lin = lin + spill * np.array([1.0, 0.98, 0.93], np.float32)
    lin = lin + halation(lin, 0.9, 1.3 * k)
    out = hable(lin * 2.0) / hable(3.4 * 2.0)
    lo = lum(out) + 1e-4
    _, detail_after = base_detail(lo)
    restore = np.clip(detail0 * (1.15 + 0.15 * k) - detail_after, -1.2, 1.2)
    out = out * np.exp(restore * np.clip((0.97 - lo) / 0.3, 0, 1))[..., None]
    l = lum(out)[..., None]
    whiten = np.clip((l - 0.72) / 0.25, 0, 1) ** 1.5 * 0.85 * k
    out = out * (1 - whiten) + l * whiten * np.array([1.0, 0.985, 0.95], np.float32)
    s = split_tone(to_srgb(out), (1.02, 1.0, 0.96), (0.9, 0.96, 1.05), 0.35 * k)
    return grain(aberration(np.clip(s, 0, 1), 0.003 * k), 0.016 * k)


def ordinary(src, k):
    lin = to_lin(src) * (1 + 0.25 * k) * uneven(src.shape, 5, 0.2 * k)
    g = glow(lin, 0.7, 0.9 * k, (1.0, 0.98, 0.84))
    lin = relight(lin, lambda b: b * (1 + 0.12 * k), 1.1 + 0.1 * k)
    lin = lin + g + halation(lin, 0.62, 0.8 * k)
    s = bleach(to_srgb(lin), 0.4 * k)
    s = split_tone(s, (1.05, 1.05, 0.82), (0.78, 0.97, 1.0), 0.72 * k)
    s = vignette(s, 0.38 * k)
    return grain(aberration(np.clip(s, 0, 1), 0.0025 * k), 0.02 * k)


def night(src, k):
    lin = to_lin(src) * uneven(src.shape, 7, 0.22 * k)
    l = lum(lin) + 1e-4
    top = np.log(np.percentile(l, 99.8))
    depth = 1 + 0.5 * k
    floor = np.log(0.0035)
    lin = relight(lin, lambda b: np.maximum(top + (b - top) * depth, floor + 0.3 * (b - top)), 1.25 + 0.15 * k)
    g = glow(lin, 0.28, 1.4 * k, (1.0, 0.64, 0.32))
    lin = lin + g + halation(lin, 0.22, 0.9 * k, (1.0, 0.35, 0.18))
    s = bleach(to_srgb(lin), 0.25 * k)
    s = split_tone(s, (1.1, 0.95, 0.76), (0.60, 0.80, 1.22), 0.75 * k)
    s = vignette(s, 0.6 * k, 0.4)
    return grain(aberration(np.clip(s, 0, 1), 0.0025 * k), 0.025 * k)


# Portraits get the colour of their register (no spatial glare: they are close
# views set inside the frames, not part of the painted scene).

def portrait_bright(rgb, k):
    lin = to_lin(rgb) * (1 + 0.9 * k)
    out = hable(lin * 2.0) / hable(3.4 * 2.0)
    l = lum(out)[..., None]
    whiten = np.clip((l - 0.72) / 0.25, 0, 1) ** 1.5 * 0.85 * k
    out = out * (1 - whiten) + l * whiten * np.array([1.0, 0.985, 0.95], np.float32)
    s = split_tone(to_srgb(out), (1.02, 1.0, 0.96), (0.9, 0.96, 1.05), 0.35 * k)
    return grain(s, 0.012 * k)


def portrait_ordinary(rgb, k):
    s = bleach(to_srgb(to_lin(rgb) * (1 + 0.25 * k)), 0.4 * k)
    return grain(split_tone(s, (1.05, 1.05, 0.82), (0.78, 0.97, 1.0), 0.72 * k), 0.015 * k)


def portrait_night(rgb, k):
    s = bleach(to_srgb(to_lin(rgb) * (1 - 0.5 * k)), 0.25 * k)
    return grain(split_tone(s, (1.1, 0.95, 0.76), (0.60, 0.80, 1.22), 0.75 * k), 0.02 * k)


PORTRAIT_REGISTERS = {'bright': portrait_bright, 'ordinary': portrait_ordinary, 'night': portrait_night}
PORTRAIT_FOLDERS = ('art/cast',)  # GIMP crops from tools/crop-portraits.py

STRENGTH = {'intense': 1.0, 'softened': 0.45}
REGISTERS = {name: {mode: (lambda s, f=fn, k=k: f(s, k)) for mode, k in STRENGTH.items()}
             for name, fn in (('bright', bright), ('ordinary', ordinary), ('night', night))}
REGISTERS['night-detail'] = {mode: (lambda s, k=k: night(s, k * 0.4)) for mode, k in STRENGTH.items()}


# ------------------------------------------------------------ what to grade

def neutral(path, variants):
    """The least processed source: the Softened grade where one exists."""
    return variants.get(path, path)


def load_rgba(path, size=None):
    image = Image.open(GAME / path).convert('RGBA')
    return image.resize(size, Image.LANCZOS) if size else image


def compose(stage, variants):
    canvas = load_rgba(neutral(stage['image'], variants), SIZE)
    for actor in stage['actors']:
        layer = load_rgba(neutral(actor['image'], variants), (actor['w'], actor['h']))
        canvas.alpha_composite(layer, (actor['x'], actor['y']))
    return canvas.convert('RGB')


def plan_items():
    """(key, register, compose function) for every image the game stages."""
    variants = json.loads((GAME / 'lighting-assets.json').read_text())
    checker = runpy.run_path(str(VN / 'tools/check-rovel-plan.py'), run_name='light_plan')
    beats = checker['load_plan']()['ROVEL_BEATS']
    items, seen = [], set()
    for beat in beats.values():
        stage = beat['stage']
        if beat['stage_id'] in seen:
            continue
        seen.add(beat['stage_id'])
        items.append(('stage:' + beat['stage_id'], beat['grade'], lambda s=stage: compose(s, variants)))

    staging = json.loads((GAME / 'staging.json').read_text())['scenes']
    for spec in staging.values():
        for stage in spec.get('stages', []):
            if (GAME / stage['image']).is_file() and 'image:' + stage['image'] not in seen:
                seen.add('image:' + stage['image'])
                items.append(('image:' + stage['image'], spec.get('grade', 'ordinary'),
                              lambda p=stage['image']: load_rgba(p, SIZE).convert('RGB')))

    # Discovery details, their origin paintings and the title painting. A detail
    # is a close-up meant to be seen: its register applies at lower strength.
    single = {
        'art/opening/cg/detail-drawing.png': 'night', 'art/opening/cg/detail-phone.png': 'night-detail',
        'art/opening/cg/drawing-restart.png': 'night', 'art/opening/cg/purification-cleared.png': 'ordinary',
        'art/rovel/details/treatment-blue.png': 'ordinary', 'art/rovel/details/treatment-white.png': 'ordinary',
        'art/rovel/details/applause-hand.png': 'bright', 'art/rovel/cg/ceremony-applause.png': 'bright',
    }
    for path, register in single.items():
        if 'image:' + path not in seen:
            seen.add('image:' + path)
            items.append(('image:' + path, register,
                          lambda p=path: load_rgba(neutral(p, variants)).convert('RGB')))
    return items


def output_path(key, mode):
    kind, name = key.split(':', 1)
    stem = name if kind == 'stage' else name[len('art/'):].rsplit('.', 1)[0].replace('/', '--')
    return 'art/lit/%s-%s.webp' % (stem, mode)


def grade_portraits(force):
    """Every neutral portrait in every register and mode, alpha kept."""
    out, graded = {}, 0
    (OUT / 'portraits').mkdir(parents=True, exist_ok=True)
    for folder in PORTRAIT_FOLDERS:
        for path in sorted((GAME / folder).glob('*.png')):
            entry = out.setdefault(path.stem, {})
            image = None
            for register, fn in PORTRAIT_REGISTERS.items():
                for mode, k in STRENGTH.items():
                    target = 'art/lit/portraits/%s-%s-%s.webp' % (path.stem, register, mode)
                    entry.setdefault(register, {})[mode] = target
                    if force or not (GAME / target).is_file():
                        if image is None:
                            image = np.asarray(Image.open(path).convert('RGBA'), np.float32) / 255.0
                        rgb = np.clip(fn(image[..., :3], k), 0, 1)
                        rgba = np.dstack([rgb, image[..., 3]])
                        Image.fromarray((rgba * 255 + 0.5).astype('uint8')).save(GAME / target, quality=QUALITY, method=6)
                        graded += 1
    return out, graded


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true', help='regrade existing outputs')
    parser.add_argument('--portraits', action='store_true', help='grade portraits only; keep the scene manifest')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.portraits:
        manifest = json.loads(MANIFEST.read_text())
        manifest['portraits'], graded = grade_portraits(args.force)
        MANIFEST.write_text(json.dumps(manifest, indent=1, sort_keys=True) + '\n')
        print('%d portraits in the plan, %d files graded now.' % (len(manifest['portraits']), graded))
        return
    manifest = {'stages': {}, 'images': {}, 'registers': {}}
    graded = 0
    for key, register, source in plan_items():
        paths = {mode: output_path(key, mode) for mode in ('intense', 'softened')}
        if args.force or not all((GAME / p).is_file() for p in paths.values()):
            image = np.asarray(source(), dtype=np.float32) / 255.0
            SCALE[0] = max(image.shape[:2]) / 1920.0
            for mode, path in paths.items():
                graded_image = np.clip(REGISTERS[register][mode](image), 0, 1)
                Image.fromarray((graded_image * 255 + 0.5).astype('uint8')).save(GAME / path, quality=QUALITY, method=6)
            graded += 1
        kind, name = key.split(':', 1)
        manifest['stages' if kind == 'stage' else 'images'][name] = paths
        manifest['registers'][name] = register
    manifest['portraits'], portrait_count = grade_portraits(args.force)
    MANIFEST.write_text(json.dumps(manifest, indent=1, sort_keys=True) + '\n')
    total = len(manifest['stages']) + len(manifest['images'])
    print('%d images in the plan, %d graded now; manifest written.' % (total, graded))


if __name__ == '__main__':
    main()
