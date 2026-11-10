"""Framing arithmetic for the camera (direction.rpy), in plain Python.

A framing is (cx, cy, zoom): the point of the 1920x1080 stage that sits at the
centre of the screen, and how far the camera has moved in. The game and
tools/direct-shots.py both import this file, so a framing drawn on a review
sheet is the framing the game shows.

The lower third of the screen carries the reading shade and the text, so a
person is framed in the upper two thirds: eyes about 37% down the screen, with
room in front of the face in the direction they look.
"""

import re

W, H = 1920.0, 1080.0
WIDE = (W / 2, H / 2, 1.0)

FACE_HEIGHT = 0.185     # a face (brow to chin) takes this share of the screen height
FACE_Y = 0.37           # where the middle of the face sits, down the screen
LOOK_ROOM = 0.11        # how far off centre a face sits, away from where it looks
ZOOM_MAX = 1.85         # the paintings are 1920 px wide; closer than this goes soft
ZOOM_MIN = 1.12         # a "closer" framing that barely moves is not worth a cut
CREEP = 0.032           # the slow push while a line is read; a framing must hold through it


def clamp(framing):
    """The framing moved, if it must be, so the screen never leaves the stage."""
    cx, cy, z = framing
    z = max(1.0, z)
    half_w, half_h = W / 2 / z, H / 2 / z
    return (min(max(cx, half_w), W - half_w), min(max(cy, half_h), H - half_h), z)


def box(framing):
    """(x0, y0, x1, y1) of the stage the framing shows."""
    cx, cy, z = clamp(framing)
    return (cx - W / 2 / z, cy - H / 2 / z, cx + W / 2 / z, cy + H / 2 / z)


def overlap(a, b):
    """Shared area of two framings as a share of the smaller one's area."""
    ax0, ay0, ax1, ay1 = box(a)
    bx0, by0, bx1, by1 = box(b)
    w = min(ax1, bx1) - max(ax0, bx0)
    h = min(ay1, by1) - max(ay0, by0)
    if w <= 0 or h <= 0:
        return 0.0
    return w * h / min((ax1 - ax0) * (ay1 - ay0), (bx1 - bx0) * (by1 - by0))


def cuts(framing, face):
    """True when the framing would show a broken figure: an edge through a
    face, a face jammed against the edge, or a body hanging in from the top
    without its head. A face wholly inside is fine, and so is one clear of
    the frame to the side: a shoulder at the edge reads as foreground."""
    x0, y0, x1, y1 = box(framing)
    fx, fy, fh = face[:3]
    left, right, top, bottom = fx - 0.36 * fh, fx + 0.36 * fh, fy - 0.5 * fh, fy + 0.5 * fh
    if right + 0.22 * fh <= x0 or left - 0.22 * fh >= x1 or top >= y1:
        return False
    if bottom <= y0:
        return y0 - bottom < 2.6 * fh and x0 < fx < x1      # a headless body in the picture
    room = 0.2 * fh
    return not (left - room >= x0 and right + room <= x1 and top - 0.35 * fh >= y0 and bottom <= y1)


def breaks(framing, faces):
    """True when the framing, at rest or at the end of its slow push, cuts
    any of the faces."""
    pushed = (framing[0], framing[1], framing[2] * (1 + CREEP))
    return any(cuts(framing, face) or cuts(pushed, face) for face in faces)


def single(face, look=0, others=(), face_height=FACE_HEIGHT, zoom_max=ZOOM_MAX):
    """A framing on one person. face is (x, y, height) of the face on the
    stage; look is -1 when they look toward screen left, 1 toward screen
    right, 0 straight on. others are the other faces in the painting: the
    framing shifts, tightens or opens out until none of them is broken by its
    edge, the way a camera operator keeps a neighbour in the shot or out."""
    fx, fy, fh = face[:3]
    want = min(zoom_max, max(ZOOM_MIN, face_height * H / max(fh, 1.0)))
    near = [o for o in others if o[2] >= 30 and (abs(o[0] - fx) > 1 or abs(o[1] - fy) > 1)]
    zooms = [want]
    for n in range(1, 9):
        zooms += [want * 1.05 ** n, want / 1.06 ** n]
    best, best_cost = None, None
    for z in zooms:
        if not 1.0 <= z <= zoom_max / (1 + CREEP) * 1.0001:
            continue
        zoom_cost = 1.5 * abs(z / want - 1) if z < want else 0.9 * abs(z / want - 1)
        if best is not None and zoom_cost >= best_cost:
            continue
        view_w, view_h = W / z, H / z
        cx0, cy0 = fx + look * LOOK_ROOM * view_w, fy + (0.5 - FACE_Y) * view_h
        for ix in range(-18, 19):
            for iy in range(-6, 5):
                framing = clamp((cx0 + ix * view_w * 0.02, cy0 + iy * view_h * 0.02, z))
                x0, y0, x1, y1 = box(framing)
                sx, sy = (fx - x0) / (x1 - x0), (fy - y0) / (y1 - y0)
                # eyes in the upper part of the screen; a face near the top
                # of the painting itself can only sit higher
                high = 0.13 if y0 < 1.0 else 0.24
                if not (0.18 <= sx <= 0.82 and high <= sy <= 0.50) or y0 > fy - 1.0 * fh:
                    continue
                if breaks(framing, near):
                    continue
                cost = abs(framing[0] - cx0) / view_w + 1.4 * abs(framing[1] - cy0) / view_h + zoom_cost
                if best is None or cost < best_cost:
                    best, best_cost = framing, cost
    return best if best is not None else WIDE


def detail(x0, y0, x1, y1, zoom_max=1.8):
    """A framing that shows a hand-drawn box of the stage: the box is kept
    inside the upper two thirds of the screen, above the reading shade."""
    w, h = max(x1 - x0, 1.0), max(y1 - y0, 1.0)
    z = min(zoom_max, W / w * 0.86, H * 0.60 / h)
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2 + (0.5 - 0.36) * H / max(z, 1.0)
    return clamp((cx, cy, max(1.0, z)))


def look_from(face, others):
    """Which way a person most likely looks: toward the others in the picture."""
    xs = [o[0] for o in others if o is not face]
    if not xs:
        return 0
    mean = sum(xs) / len(xs)
    return 1 if mean > face[0] + 40 else -1 if mean < face[0] - 40 else 0


_TAG = re.compile(r'\{[^}]*\}')
# Who a line opening on She or He can mean, from the screenplay and designs.
SHE = frozenset(('TESSA', 'MARA', 'ELIN', 'HEST', 'ADA', 'ORRA', 'VASK', 'ARCHIVIST', 'WOMAN', 'MOTHER'))
HE = frozenset(('IVEN', 'SENN', 'OLAN', 'LUCAN', 'VALCAIR', 'ORREN', 'SERAT', 'MARREN', 'SCHOLAR', 'GOVERNOR',
                'MESSENGER', 'APPRENTICE', 'BARGEMAN', 'ESCORT', 'BOATMAN', 'FERRYMAN'))


def narration_shot(text, names):
    """The framing a line of narration takes when none is directed: the name
    of the person the sentence is about; 'hold:she', 'hold:he' or 'hold' when
    it opens on a pronoun and continues with someone already framed (see
    resolve_hold); None for the whole painting. names are the people who have
    a framing in this painting. Text tags and case are ignored, so the game
    (which sees typeset text) and the review tool (which sees the screenplay)
    agree."""
    plain = _TAG.sub('', text).replace('\u2019', "'").strip()
    sentences = [part for part in re.split(r'[.!?]+\s+', plain) if part.strip()]
    found = []
    for name in names:
        match = re.search(r'\b' + re.escape(name.split()[-1]) + r'\b', plain, re.I)
        if match:
            found.append((match.start(), name))
    found.sort()
    if len(sentences) > 2 or len(found) > 2:
        return None
    if found and found[0][0] == 0:
        return found[0][1]
    opening = plain.lower()
    if opening.startswith(('she ', 'her ')):
        return 'hold:she'
    if opening.startswith(('he ', 'his ')):
        return 'hold:he'
    if opening.startswith(('they ', 'their ')):
        return 'hold'
    if len(found) == 1:
        return found[0][1]
    return None


def resolve_hold(kind, recent, previous):
    """Who a pronoun-led line stays with. recent lists the people framed on
    this painting, latest first; previous is the framing before this line.
    She keeps to the latest woman framed, He to the latest man; a person whose
    pronoun isn't recorded is kept when they were the latest."""
    if kind == 'hold':
        return previous
    want, other = (SHE, HE) if kind == 'hold:she' else (HE, SHE)
    for name in recent[:2]:
        if name in want:
            return name
    if recent and recent[0] not in other:
        return recent[0]
    return None


def remember(recent, name):
    """recent with a newly framed person put first (two are kept)."""
    if not name or not name.isupper():
        return recent
    return [name] + [n for n in recent if n != name][:1]
