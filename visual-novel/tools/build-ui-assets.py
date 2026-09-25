#!/usr/bin/env python3
"""Draw the reading interface's image components in code.

Every file under renpy/game/ui/ is produced here from geometry, gradients and
seeded noise; nothing is diffusion-generated. Rerun after changing a shape:

    python3 visual-novel/tools/build-ui-assets.py
"""
from pathlib import Path
import math

import cv2
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


# ---------------------------------------------------------------- ornament
# Relief ornament is modelled as a height field, then lit like metal: gilt
# relief (Blinn-Phong with a warm environment and ambient occlusion) on a
# celadon enamel ground. The vocabulary comes from the temple scenes: carved
# laurel, celadon inlay, and the twelve-ray sun at the keystone.

OSS = 3  # supersampling for relief


def smoothstep(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def dome(mask, radius):
    """Rounded relief rising over `radius` pixels from a mask's edge."""
    d = cv2.distanceTransform((mask > 0.5).astype(np.uint8), cv2.DIST_L2, 5)
    x = np.clip(d / max(radius, 1e-3), 0, 1)
    return np.sqrt(x * (2 - x))


def light_relief(height, albedo, metal, alpha, strength=5.0):
    gy, gx = np.gradient(height)
    n = np.dstack([-gx * strength, -gy * strength, np.ones_like(height)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    light = np.array([-0.55, -0.75, 0.9], np.float32)
    light /= np.linalg.norm(light)
    half = light + np.array([0, 0, 1.0], np.float32)
    half /= np.linalg.norm(half)
    ndl = np.clip((n * light).sum(2), 0, 1)
    ndh = np.clip((n * half).sum(2), 0, 1)
    spec = ndh ** 70 * (0.35 + 0.65 * metal)
    up = np.clip(-n[..., 1] * 0.5 + 0.5, 0, 1)[..., None]
    env = np.array([1.0, 0.92, 0.75], np.float32) * up ** 1.5 + np.array([0.12, 0.10, 0.08], np.float32) * (1 - up)
    ao = np.clip(1 - (cv2.GaussianBlur(height, (0, 0), 3 * OSS) - height) * 3.0, 0.35, 1)[..., None]
    m = metal[..., None]
    colour = (albedo * (0.28 + 0.9 * ndl[..., None]) * (1 - m * 0.55) + albedo * env * m * 0.9) * ao
    colour = colour + spec[..., None] * (albedo * m + (1 - m) * 0.9) * 1.1
    return np.dstack([np.clip(colour, 0, 1), alpha])


def arch_centreline(w, h, inset, step=0.7):
    r = w / 2.0 - inset
    cx = cy = w / 2.0
    points, y = [], float(h)
    while y > cy:
        points.append((cx - r, y))
        y -= step
    n = int(math.pi * r / step)
    for i in range(n + 1):
        a = math.pi + math.pi * i / n
        points.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    y = cy
    while y < h:
        points.append((cx + r, y))
        y += step
    return np.array(points, np.float32)


def leaf_polygon(p, direction, length, width, n=20):
    d = direction / (np.linalg.norm(direction) + 1e-6)
    perp = np.array([-d[1], d[0]])
    out = [tuple(p + d * (j / n) * length + perp * math.sin(math.pi * j / n) ** 0.9 * width / 2 * (1 - 0.25 * j / n))
           for j in range(n + 1)]
    out += [tuple(p + d * (j / n) * length - perp * math.sin(math.pi * j / n) ** 0.9 * width / 2 * (1 - 0.25 * j / n))
            for j in range(n, -1, -1)]
    return out


def laurel(size, path, spacing, leaf_len, leaf_w, angle, stem_w, stop):
    """Leaf pairs climbing both halves of a path toward its midpoint."""
    stem, leaves = Image.new('L', size, 0), Image.new('L', size, 0)
    ds, dl = ImageDraw.Draw(stem), ImageDraw.Draw(leaves)
    s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))])
    total, mid = s[-1], s[-1] / 2
    tangent = np.gradient(path, axis=0)
    tangent /= np.linalg.norm(tangent, axis=1, keepdims=True) + 1e-6
    for left in (True, False):
        end = mid - stop if left else mid + stop
        keep = s <= end if left else s >= end
        ds.line([tuple(q) for q in path[keep]], fill=255, width=max(1, int(stem_w)))
        sign = 1 if left else -1
        pos = (0.0 if left else total) + sign * spacing * 0.5
        while (pos < end) if left else (pos > end):
            i = min(int(np.searchsorted(s, pos)), len(path) - 1)
            t = tangent[i] * sign
            n = np.array([-t[1], t[0]])
            for side in (1, -1):
                a = math.radians(angle) * side
                dl.polygon(leaf_polygon(path[i], t * math.cos(a) + n * math.sin(a), leaf_len, leaf_w), fill=255)
            pos += sign * spacing
    return np.asarray(stem, np.float32) / 255, np.asarray(leaves, np.float32) / 255


def sun_masks(size, centre, r_disc, r_ray, rays=12):
    """The temple's brass sun: a disc with twelve short rays and a raised ring."""
    disc, ray, ring = (Image.new('L', size, 0) for _ in range(3))
    cx, cy = centre
    ImageDraw.Draw(disc).ellipse([cx - r_disc, cy - r_disc, cx + r_disc, cy + r_disc], fill=255)
    rr = r_disc * 0.72
    ImageDraw.Draw(ring).ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=255, width=max(1, int(r_disc * 0.12)))
    dr = ImageDraw.Draw(ray)
    for i in range(rays):
        a = 2 * math.pi * i / rays - math.pi / 2
        half = math.pi / rays * 0.5
        dr.polygon([(cx + math.cos(a - half) * r_disc * 0.92, cy + math.sin(a - half) * r_disc * 0.92),
                    (cx + math.cos(a) * r_ray, cy + math.sin(a) * r_ray),
                    (cx + math.cos(a + half) * r_disc * 0.92, cy + math.sin(a + half) * r_disc * 0.92)], fill=255)
    return [np.asarray(m, np.float32) / 255 for m in (disc, ray, ring)]


GILT = np.array([0.84, 0.64, 0.33], np.float32)
CELADON = np.array([0.25, 0.40, 0.37], np.float32)


def arch_frame(w, h, name, band=0.072, bottom_fade=0.32, seed=4):
    """Gilt arch with a laurel garland on celadon enamel and a sun keystone."""
    W, H = w * OSS, h * OSS
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32) + 0.5
    r = W / 2.0
    d = np.where(yy >= r, r - np.abs(xx - W / 2.0), r - np.sqrt((xx - W / 2.0) ** 2 + (yy - r) ** 2))
    t = band * W
    u = np.clip(d / t, 0, 1)
    inside = ((d >= 0) & (d <= t)).astype(np.float32)
    outer = smoothstep(1 - np.abs(u - 0.08) / 0.08) * (u < 0.16)
    inner = smoothstep(1 - np.abs(u - 0.92) / 0.08) * (u > 0.84)
    field = ((u >= 0.16) & (u <= 0.84)).astype(np.float32)
    across = np.sin(np.pi * np.clip((u - 0.16) / 0.68, 0, 1))
    height = outer * 0.9 + inner * 0.6 + field * (0.08 + 0.06 * across)
    stem, leaves = laurel((W, H), arch_centreline(W, H, t * 0.5), spacing=t * 0.62, leaf_len=t * 0.52,
                          leaf_w=t * 0.24, angle=38, stem_w=t * 0.06, stop=t * 0.95)
    height = height + np.maximum(dome(stem * field, t * 0.03) * 0.45, dome(leaves * field, t * 0.09) * 0.7)
    disc, ray, ring = sun_masks((W, H), (W / 2, t * 0.52), t * 0.5, t * 0.82)
    height = np.maximum(height, np.maximum(dome(disc, t * 0.3) * 1.25 - ring * 0.25, dome(ray, t * 0.05) * 0.85))
    cover = np.clip(inside + disc + ray, 0, 1)
    raised = np.clip((height - 0.18) * 3.2, 0, 1)
    mottle = cv2.GaussianBlur(np.random.default_rng(seed).normal(0, 1, (H, W)).astype(np.float32), (0, 0), 3 * OSS)
    enamel = CELADON * (0.8 + 0.35 * across)[..., None] * (1 + mottle[..., None] * 0.08)
    albedo = enamel * (1 - raised[..., None]) + GILT * raised[..., None]
    fade = 1 - smoothstep((yy / H - (1 - bottom_fade)) / bottom_fade)
    rgba = light_relief(cv2.GaussianBlur(height.astype(np.float32), (0, 0), 0.6 * OSS), albedo, raised * 0.95, cover * fade)
    rgba = cv2.resize(rgba, (w, h), interpolation=cv2.INTER_AREA)
    save(Image.fromarray((np.clip(rgba, 0, 1) * 255 + 0.5).astype('uint8')), name)


def closed_arch_sdf(W, H, inset=0.0):
    """Signed distance (positive inside) to a closed arch: a semicircle over a
    rectangle, with a flat foot."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32) + 0.5
    r = W / 2.0 - inset
    cx, cy = W / 2.0, W / 2.0
    side = np.where(yy >= cy, r - np.abs(xx - cx), r - np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2))
    return np.minimum(side, (H - inset) - yy), yy, xx


def closed_arch_path(W, H, inset, step=0.7):
    """Centre-line of a closed arch band: from the foot's centre, left along the
    foot, up the left side, over the top, down the right, back to the centre."""
    r = W / 2.0 - inset
    cx = cy = W / 2.0
    bottom = H - inset
    pts = []
    x = cx
    while x > cx - r:
        pts.append((x, bottom)); x -= step
    y = bottom
    while y > cy:
        pts.append((cx - r, y)); y -= step
    n = int(math.pi * r / step)
    for i in range(n + 1):
        a = math.pi + math.pi * i / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    y = cy
    while y < bottom:
        pts.append((cx + r, y)); y += step
    x = cx + r
    while x > cx:
        pts.append((x, bottom)); x -= step
    return np.array(pts, np.float32)


def window_frame(w, h, role, band=0.075, seed=4):
    """A closed laurel window for a close portrait: the wreath is tied at the
    foot and meets the twelve-ray sun at the crown; a recess shadow falls on
    the portrait from the upper left. Also writes the portrait mask and ground."""
    W, H = w * OSS, h * OSS
    t = band * W
    d, yy, xx = closed_arch_sdf(W, H)
    u = np.clip(d / t, 0, 1)
    inside = ((d >= 0) & (d <= t)).astype(np.float32)
    outer = smoothstep(1 - np.abs(u - 0.08) / 0.08) * (u < 0.16)
    inner = smoothstep(1 - np.abs(u - 0.92) / 0.08) * (u > 0.84)
    field = ((u >= 0.16) & (u <= 0.84)).astype(np.float32)
    across = np.sin(np.pi * np.clip((u - 0.16) / 0.68, 0, 1))
    height = outer * 0.9 + inner * 0.6 + field * (0.08 + 0.06 * across)
    path = closed_arch_path(W, H, t * 0.5)
    stem, leaves = laurel((W, H), path, spacing=t * 0.62, leaf_len=t * 0.52, leaf_w=t * 0.24,
                          angle=38, stem_w=t * 0.06, stop=t * 0.95)
    # keep the foot's centre clear for the tie
    foot = np.hypot(xx - W / 2.0, yy - (H - t * 0.5)) < t * 0.9
    stem, leaves = stem * (~foot), leaves * (~foot)
    height = height + np.maximum(dome(stem * field, t * 0.03) * 0.45, dome(leaves * field, t * 0.09) * 0.7)
    disc, ray, ring = sun_masks((W, H), (W / 2, t * 0.52), t * 0.5, t * 0.82)
    tie = Image.new('L', (W, H), 0)
    ImageDraw.Draw(tie).ellipse([W / 2 - t * 0.34, H - t * 0.84, W / 2 + t * 0.34, H - t * 0.16], fill=255)
    tie = np.asarray(tie, np.float32) / 255
    height = np.maximum(height, np.maximum(dome(disc, t * 0.3) * 1.25 - ring * 0.25, dome(ray, t * 0.05) * 0.85))
    height = np.maximum(height, dome(tie, t * 0.3) * 1.0)
    cover = np.clip(inside + disc + ray, 0, 1)
    raised = np.clip((height - 0.18) * 3.2, 0, 1)
    mottle = cv2.GaussianBlur(np.random.default_rng(seed).normal(0, 1, (H, W)).astype(np.float32), (0, 0), 3 * OSS)
    enamel = CELADON * (0.8 + 0.35 * across)[..., None] * (1 + mottle[..., None] * 0.08)
    albedo = enamel * (1 - raised[..., None]) + GILT * raised[..., None]
    frame = light_relief(cv2.GaussianBlur(height.astype(np.float32), (0, 0), 0.6 * OSS), albedo, raised * 0.95, cover)
    # recess shadow on the portrait, heavier toward the upper left (light comes from there)
    di = d - t
    shadow = np.clip(1 - di / (t * 0.9), 0, 1) ** 1.6 * (di > -1)
    shadow = shadow * (0.75 + 0.25 * ((xx < W / 2) | (yy < W / 2)))
    shade = np.dstack([np.zeros((H, W, 3), np.float32), np.clip(shadow * 0.55, 0, 1) * (di > 0)])
    out = shade.copy()
    a = frame[..., 3:4]
    out[..., :3] = frame[..., :3] * a + shade[..., :3] * (1 - a)
    out[..., 3:4] = a + shade[..., 3:4] * (1 - a)
    save(to_image(out, (w, h)), 'window-frame-' + role + '.png')
    # the portrait lives inside the band's inner edge (slight overlap under the band)
    mask = np.clip((d - t * 0.85) / OSS, 0, 1)
    m = Image.new('RGBA', (W, H), (255, 255, 255, 0))
    m.putalpha(Image.fromarray((mask * 255).astype('uint8')))
    save(m.resize((w, h), Image.LANCZOS), 'window-mask-' + role + '.png')


def speech_rail(length, name, height=26):
    """A gilt rail for the speaker's name: a bead and two laurel leaves at the
    left, then a rod that tapers into a fading thread."""
    W, H = length * OSS, height * OSS
    cy = H * 0.5
    rod = Image.new('L', (W, H), 0)
    dr = ImageDraw.Draw(rod)
    start, end = 34 * OSS, W - 2 * OSS
    steps = 400
    for i in range(steps):
        x0 = start + (end - start) * i / steps
        x1 = start + (end - start) * (i + 1) / steps
        u = i / steps
        thick = (2.6 * OSS) * (1 - smoothstep((u - 0.45) / 0.55) * 0.8)
        dr.rectangle([x0, cy - thick / 2, x1, cy + thick / 2], fill=255)
    rod = np.asarray(rod, np.float32) / 255
    bead = Image.new('L', (W, H), 0)
    br = 5.5 * OSS
    bx = 20 * OSS
    ImageDraw.Draw(bead).ellipse([bx - br, cy - br, bx + br, cy + br], fill=255)
    bead = np.asarray(bead, np.float32) / 255
    leaves = Image.new('L', (W, H), 0)
    dl = ImageDraw.Draw(leaves)
    for side in (1, -1):
        a = math.radians(32) * side
        direction = np.array([math.cos(a), math.sin(a)])
        dl.polygon(leaf_polygon(np.array([bx + br * 0.6, cy]), direction, 15 * OSS, 6.5 * OSS), fill=255)
    leaves = np.asarray(leaves, np.float32) / 255
    height_map = np.maximum.reduce([dome(rod, 1.5 * OSS) * 0.7, dome(bead, br) * 1.1, dome(leaves, 2.2 * OSS) * 0.75])
    cover = np.clip(rod + bead + leaves, 0, 1)
    xx = np.arange(W, dtype=np.float32)[None, :] / W
    fade = 1 - smoothstep((xx - 0.55) / 0.45)
    albedo = np.broadcast_to(GILT, (H, W, 3)).copy()
    rgba = light_relief(cv2.GaussianBlur(height_map.astype(np.float32), (0, 0), 0.5 * OSS), albedo,
                        np.full((H, W), 0.95, np.float32), cover * fade, strength=4.0)
    rgba = cv2.resize(rgba, (length, height), interpolation=cv2.INTER_AREA)
    save(Image.fromarray((np.clip(rgba, 0, 1) * 255 + 0.5).astype('uint8')), name)


# ------------------------------------------------------------ page ornament
# Book pages (scenes without paintings yet) get printed ornament: a double
# rule around the text block with laurel corners, a laurel rule under the
# scene title, and an illuminated initial for each scene's first narration.

SERIF = str(ROOT / 'renpy/game/fonts/EBGaramond12-Regular.ttf')
INK_PRINT = np.array([0.23, 0.19, 0.15], np.float32)


def sprig_masks(size, origin, direction, length, pairs=3, leaf=0.34, angle=40, stem=1.4):
    """A short laurel sprig: a stem with leaf pairs and a terminal leaf."""
    W, H = size
    stem_img, leaf_img = Image.new('L', (W, H), 0), Image.new('L', (W, H), 0)
    d = np.array(direction, np.float32)
    d /= np.linalg.norm(d)
    o = np.array(origin, np.float32)
    tip = o + d * length
    ImageDraw.Draw(stem_img).line([tuple(o), tuple(tip)], fill=255, width=max(1, int(stem)))
    dl = ImageDraw.Draw(leaf_img)
    n = np.array([-d[1], d[0]])
    for i in range(pairs):
        p = o + d * length * (0.22 + 0.62 * i / max(1, pairs - 1))
        for side in (1, -1):
            a = math.radians(angle) * side
            dl.polygon(leaf_polygon(p, d * math.cos(a) + n * math.sin(a), length * leaf, length * leaf * 0.42), fill=255)
    dl.polygon(leaf_polygon(tip - d * length * 0.05, d, length * leaf * 0.9, length * leaf * 0.38), fill=255)
    return np.asarray(stem_img, np.float32) / 255, np.asarray(leaf_img, np.float32) / 255


def flat(mask, colour, alpha=1.0):
    rgba = np.dstack([np.broadcast_to(colour, mask.shape + (3,)), np.clip(mask, 0, 1) * alpha])
    return rgba


def gilt(mask, radius, strength=4.0):
    height = dome(mask, radius)
    albedo = np.broadcast_to(GILT, mask.shape + (3,)).copy()
    return light_relief(cv2.GaussianBlur(height.astype(np.float32), (0, 0), 0.5 * OSS), albedo,
                        np.full(mask.shape, 0.95, np.float32), np.clip(mask, 0, 1), strength=strength)


def to_image(rgba, size):
    rgba = cv2.resize(rgba.astype(np.float32), size, interpolation=cv2.INTER_AREA)
    return Image.fromarray((np.clip(rgba, 0, 1) * 255 + 0.5).astype('uint8'))


def page_frame(name, gilded, box=(290, 56, 1630, 1030)):
    """Double rule around the text block with laurel sprigs at the corners."""
    W, H = 1920 * OSS, 1080 * OSS
    lines = Image.new('L', (W, H), 0)
    dl = ImageDraw.Draw(lines)
    x0, y0, x1, y1 = (v * OSS for v in box)
    gap = 7 * OSS
    dl.rectangle([x0, y0, x1, y1], outline=255, width=int(1.6 * OSS))
    dl.rectangle([x0 + gap, y0 + gap, x1 - gap, y1 - gap], outline=255, width=int(0.8 * OSS))
    mask = np.asarray(lines, np.float32) / 255
    # clear the corners for the sprigs
    for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        yy, xx = np.ogrid[0:H, 0:W]
        mask = mask * (np.hypot(xx - cx, yy - cy) > 30 * OSS)
    leaves = np.zeros_like(mask)
    stems = np.zeros_like(mask)
    for (cx, cy), (dx, dy) in (((x0, y0), (1, 1)), ((x1, y0), (-1, 1)), ((x0, y1), (1, -1)), ((x1, y1), (-1, -1))):
        for direction in ((dx, 0), (0, dy)):
            st, lf = sprig_masks((W, H), (cx + dx * 4 * OSS, cy + dy * 4 * OSS), direction, 46 * OSS, pairs=3)
            stems, leaves = np.maximum(stems, st), np.maximum(leaves, lf)
        dot = Image.new('L', (W, H), 0)
        ImageDraw.Draw(dot).ellipse([cx - 5 * OSS, cy - 5 * OSS, cx + 5 * OSS, cy + 5 * OSS], fill=255)
        leaves = np.maximum(leaves, np.asarray(dot, np.float32) / 255)
    ornament = np.maximum(stems, leaves)
    if gilded:
        rgba = gilt(np.maximum(mask, ornament), 1.8 * OSS)
        rgba[..., 3] *= 0.85
    else:
        rgba = flat(np.maximum(mask, ornament), INK_PRINT, 0.72)
    save(to_image(rgba, (1920, 1080)), name)


def page_rule(name, gilded, length=260, height=30):
    """A laurel sprig that runs into a tapering rule, under a scene title."""
    W, H = length * OSS, height * OSS
    cy = H / 2
    stem, leaves = sprig_masks((W, H), (6 * OSS, cy), (1, 0), 70 * OSS, pairs=3, angle=38)
    line = Image.new('L', (W, H), 0)
    dl = ImageDraw.Draw(line)
    for i in range(300):
        u = i / 300
        x = 70 * OSS + (W - 76 * OSS) * u
        th = 1.6 * OSS * (1 - 0.75 * u)
        dl.rectangle([x, cy - th / 2, x + (W - 76 * OSS) / 300 + 1, cy + th / 2], fill=255)
    fade = 1 - smoothstep((np.arange(W, dtype=np.float32)[None, :] / W - 0.55) / 0.45)
    mask = np.maximum.reduce([stem, leaves, np.asarray(line, np.float32) / 255 * fade])
    rgba = gilt(mask, 1.6 * OSS) if gilded else flat(mask, INK_PRINT, 0.85)
    save(to_image(rgba, (length, height)), name)


def initials(size=128):
    """Illuminated initials A-Z: a raised gilt letter on celadon enamel inside a
    beaded gilt border, with laurel sprigs in the corners."""
    from PIL import ImageFont
    font = ImageFont.truetype(SERIF, int(size * 0.78 * OSS))
    W = H = size * OSS
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    edge = np.minimum.reduce([xx, yy, W - 1 - xx, H - 1 - yy])
    border = ((edge < 7 * OSS) & (edge >= 0)).astype(np.float32)
    bead_track = ((edge > 2.2 * OSS) & (edge < 4.8 * OSS)).astype(np.float32)
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        glyph = Image.new('L', (W, H), 0)
        dg = ImageDraw.Draw(glyph)
        box = dg.textbbox((0, 0), letter, font=font)
        gw, gh = box[2] - box[0], box[3] - box[1]
        dg.text(((W - gw) / 2 - box[0], (H - gh) / 2 - box[1] + 2 * OSS), letter, font=font, fill=255)
        g = np.asarray(glyph, np.float32) / 255
        stems = np.zeros((H, W), np.float32)
        leaves = np.zeros((H, W), np.float32)
        for cx, cy, dx, dy in ((10, 10, 1, 1), (size - 10, 10, -1, 1), (10, size - 10, 1, -1), (size - 10, size - 10, -1, -1)):
            st, lf = sprig_masks((W, H), (cx * OSS, cy * OSS), (dx, dy), 22 * OSS, pairs=2, leaf=0.42, angle=42, stem=1.2 * OSS)
            stems, leaves = np.maximum(stems, st), np.maximum(leaves, lf)
        field = 1 - border
        height = (border * 0.55 + dome(bead_track, 1.2 * OSS) * 0.3 + field * 0.08
                  + dome(np.maximum(stems, leaves) * field, 1.4 * OSS) * 0.35 + dome(g, 2.6 * OSS) * 1.2)
        raised = np.clip(np.maximum.reduce([border, np.maximum(stems, leaves) * field, g]), 0, 1)
        mottle = cv2.GaussianBlur(np.random.default_rng(ord(letter)).normal(0, 1, (H, W)).astype(np.float32), (0, 0), 3 * OSS)
        enamel = CELADON * (0.9 + mottle[..., None] * 0.07)
        albedo = enamel * (1 - raised[..., None]) + GILT * raised[..., None]
        rgba = light_relief(cv2.GaussianBlur(height.astype(np.float32), (0, 0), 0.5 * OSS), albedo, raised * 0.95,
                            np.ones((H, W), np.float32), strength=4.5)
        save(to_image(rgba, (size, size)), 'initials/' + letter + '.png')


# ------------------------------------------------------------ reading, 24 September
# Chosen by the user after the panel and arch samples (prototypes/portrait-frames):
# the speaker alone in an oval with a soft golden halo, fading at its base; the
# scene's own shadow behind the text (the per-painting blur and colour come from
# tools/grade-light.py), an engraved hairline, and the controls hidden behind a
# small gilt sun.

OVAL = (224, 280)


def oval_portrait():
    """The oval's mask and its golden halo, both fading toward the base so
    nothing cuts across the chest."""
    w, h = OVAL
    rx, ry = w / 2 - 3, h / 2 - 3

    def dist(x, y):
        return (np.sqrt(((x - w / 2) / rx) ** 2 + ((y - h / 2) / ry) ** 2) - 1) * min(rx, ry)

    def base_fade(y, start):
        return 1 - smoothstep((y / h - start) / (1 - start))

    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32) + 0.5
    inside = np.clip(0.5 - dist(xx, yy), 0, 1) * base_fade(yy, 0.70)
    save(Image.fromarray((np.dstack([np.ones_like(inside)] * 3 + [inside]) * 255 + 0.5).astype('uint8')), 'oval-mask.png')
    m = 26
    yy, xx = np.mgrid[0:h + 2 * m, 0:w + 2 * m].astype(np.float32) + 0.5
    d = dist(xx - m, yy - m)
    halo = np.where(d > 0, np.exp(-(d / 7.0) ** 2) * 0.30 + np.exp(-(d / 18.0) ** 2) * 0.10, np.exp(-(d / 2.5) ** 2) * 0.32)
    halo = (halo * base_fade(np.clip(yy - m, 0, None), 0.62)).astype(np.float32)
    rgb = np.ones(halo.shape + (3,), np.float32) * np.array([0.93, 0.80, 0.52], np.float32)
    save(Image.fromarray((np.dstack([rgb, halo]) * 255 + 0.5).astype('uint8')), 'oval-halo.png')


def reading_shade_masks():
    """Where the scene's shadow falls behind the text (deepest behind the
    portrait and the words, fading right and up) and behind the open controls
    (a pool at the lower right). White is full."""
    w, h = 1920, 1080
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32) + 0.5
    left = np.sqrt(((xx - 720) / 1050) ** 2 + ((yy - 960) / 290) ** 2)
    shade = (1 - smoothstep((left - 0.45) / 0.55)) * np.interp(yy, [680, 780, 870, 1080], [0, 0.5, 0.95, 1.0])
    corner = np.sqrt(((xx - 1920) / 640) ** 2 + ((yy - 1080) / 740) ** 2)
    pool = 1 - smoothstep((corner - 0.32) / 0.68)
    for name, m in (('reading-shade-mask.png', shade), ('controls-pool-mask.png', pool)):
        m = m.astype(np.float32)
        save(Image.fromarray((np.dstack([np.ones_like(m)] * 3 + [m]) * 255 + 0.5).astype('uint8')), name)


def engraved_line(w, name, glow=True):
    """A hairline that reads on white and on black: a dark cut beneath, a gilt
    line and a faint highlight above, fading out at both ends."""
    h = 11
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32) + 0.5
    ends = smoothstep(np.minimum(xx, w - xx) / (w * 0.26))
    cut = np.exp(-((yy - 6.6) / 0.9) ** 2) * 0.55
    gilt = np.exp(-((yy - 5.2) / 0.75) ** 2)
    shine = np.exp(-((yy - 4.2) / 0.6) ** 2) * 0.35
    halo = np.exp(-((yy - 5.2) / 2.6) ** 2) * (0.22 if glow else 0)
    rgb = (np.array([0.86, 0.71, 0.44], np.float32) * (gilt + halo)[..., None]
           + np.array([1.0, 0.95, 0.8], np.float32) * shine[..., None]
           + np.array([0.09, 0.06, 0.04], np.float32) * cut[..., None])
    a = np.clip(gilt + shine + halo + cut, 0, 1)
    rgb = rgb / np.maximum(a, 1e-4)[..., None]
    save(Image.fromarray((np.dstack([np.clip(rgb, 0, 1), a * ends]) * 255 + 0.5).astype('uint8')), name)


def controls_sun():
    """The controls' trigger: the temple's twelve-ray sun in gilt relief on a
    soft shadow, so it reads on white marble and in the dark; and the glow that
    breathes around it when something can be looked at more closely."""
    S = 44
    W = S * OSS
    disc, ray, ring = sun_masks((W, W), (W / 2, W / 2), W * 0.2, W * 0.42)
    height = np.maximum(dome(disc, W * 0.12) * 1.2 - ring * 0.3, dome(ray, W * 0.03) * 0.8)
    cover = np.clip(disc + ray, 0, 1)
    albedo = np.ones(height.shape + (3,), np.float32) * GILT
    rgba = light_relief(cv2.GaussianBlur(height.astype(np.float32), (0, 0), 0.5 * OSS), albedo,
                        np.ones_like(height) * 0.9, cover.astype(np.float32))
    rgba = cv2.resize(rgba, (S, S), interpolation=cv2.INTER_AREA)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32) + 0.5
    shadow = np.exp(-(np.sqrt((xx - S / 2) ** 2 + (yy - S / 2 - 1) ** 2) / 13) ** 2) * 0.55
    a = rgba[..., 3] + shadow * (1 - rgba[..., 3])
    rgb = (rgba[..., :3] * rgba[..., 3:4] + np.array([0.05, 0.04, 0.03], np.float32)
           * (shadow * (1 - rgba[..., 3]))[..., None]) / np.maximum(a, 1e-4)[..., None]
    save(Image.fromarray((np.dstack([np.clip(rgb, 0, 1), a]) * 255 + 0.5).astype('uint8')), 'controls-sun.png')
    G = 96
    yy, xx = np.mgrid[0:G, 0:G].astype(np.float32) + 0.5
    r = np.sqrt((xx - G / 2) ** 2 + (yy - G / 2) ** 2)
    glow_ = (np.exp(-((r - 17) / 7) ** 2) * 0.55 + np.exp(-(r / 28) ** 2) * 0.25).astype(np.float32)
    rgb = np.ones(glow_.shape + (3,), np.float32) * np.array([0.98, 0.84, 0.55], np.float32)
    save(Image.fromarray((np.dstack([rgb, glow_]) * 255 + 0.5).astype('uint8')), 'controls-glow.png')


def lozenge(name, color=(205, 176, 118), size=13):
    """The mark at the end of a finished line (the old ring read as a (R) sign)."""
    s = size * 4
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float32) + 0.5
    d = (np.abs(xx - s / 2) + np.abs(yy - s / 2) * 1.35) / (s / 2)
    rgba = np.zeros((s, s, 4), np.float32)
    rgba[..., :3] = np.array(color, np.float32) / 255
    rgba[..., 3] = np.clip((1 - d) * 6, 0, 1) * 0.95
    save(Image.fromarray((rgba * 255).astype('uint8')).resize((size, size), Image.LANCZOS), name)


def main():
    scrim()
    window_frame(228, 256, 'speaker')
    window_frame(150, 168, 'listener')
    speech_rail(1060, 'speech-rail.png')
    page_frame('page-frame-ink.png', gilded=False)
    page_frame('page-frame-gilt.png', gilded=True)
    page_rule('page-rule-ink.png', gilded=False)
    page_rule('page-rule-gilt.png', gilded=True)
    initials()
    thread_line(30, 'thread-name.png')
    thread_line(150, 'thread-heading.png')
    thread_line(150, 'thread-heading-ink.png', color=(122, 88, 46))
    thread_line(360, 'thread-long.png', knot=False, alpha=180, wave=1.2)
    knot(26, 'knot.png')
    knot(18, 'knot-small.png', alpha=220)
    rule(420, 'rule.png')
    rule(1100, 'rule-wide.png', alpha=120)
    # Pages follow the scene's light: day vellum, dusk slate, night ink, at the
    # original timeline's light (the gentler set; the harsher one was retired
    # with the Intense mode on 24 September 2026).
    page('page-day.webp', (199, 191, 174), 1.3, 0.38)
    page('page-dusk.webp', (45, 52, 60), 1.0, 0.45)
    page('page-night.webp', (30, 32, 35), 0.9, 0.5)
    page('menu-ground.webp', (13, 16, 19), 0.8, 0.55, seed=11)
    glow(420, 'candle-glow.png', (255, 196, 120), 120)
    hshade('title-shade.png', 1920, [(0, 214), (0.22, 170), (0.48, 40), (0.62, 0), (1, 0)])
    text_pool('text-pool.png', 900, 420)
    edge = Image.new('RGBA', (4, 220), (11, 16, 20, 0))
    edge.putalpha(Image.fromarray(np.repeat(ramp(220, [(0, 0), (1, 255)])[:, None], 4, 1).clip(0, 255).astype('uint8')))
    save(edge, 'edge-fade.png')
    frame_line('frame-line.png')
    oval_portrait()
    reading_shade_masks()
    engraved_line(1000, 'reading-hairline.png')
    engraved_line(150, 'controls-underline.png', glow=False)
    controls_sun()
    lozenge('lozenge.png')
    lozenge('lozenge-ink.png', color=(138, 99, 52))
    print('UI components written to', UI.relative_to(ROOT.parent))


if __name__ == '__main__':
    main()
