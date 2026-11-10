#!/usr/bin/env python3
"""Find the people in every painting and draw the camera's framings for review.

The camera (renpy/game/direction.rpy) frames the person speaking, so it has to
know where each person's face is in each painting. This tool:

  find     detects the faces in every staged painting and names them by
           likeness to the cast's portraits, among the people of that scene
           (art/direction/faces.json keeps the detections).
  build    composes the framings and writes renpy/game/direction.json, the
           only file the game reads. What is decided by eye is kept in
           art/direction/plan.json and wins over what was found:
             "stages": {"<painting>": {
                 "people":  {"MARA": [388, 204, 56],  Mara's face is here: x, y, height
                                                      (the found face at that point takes the name)
                             "SENN": null},           do not frame this person
                 "look":    {"TESSA": 1},             she looks toward screen right (-1 left, 0 ahead)
                 "details": {"book": [800, 560, 1180, 760]},   a box of the painting to show
                 "shots":   {"table": [960, 600, 1.3]}}},      a framing set outright: centre x, y, zoom
             "lines":  {"16": {"655": "book", "669": "hold",
                               "680": {"shot": "TESSA", "move": "ease"}}}
           A spoken line with no entry frames the person spoken to (the
           speaker is in the oval), or the speaker when the listener has no
           framing here; narration frames the person it is about, or the whole
           painting; "hold" keeps the framing of the line before. build
           writes the framing every line takes into direction.json, and the
           game obeys that table.
  sheets   draws, for every painting with framings, the whole painting with
           each framing boxed and numbered faces, then each framing as the
           game shows it, with the reading shade over its lower third:
           renpy/test-output/direction/. Every framing is a composition and
           has to be looked at; a face in the right place can still be a bad
           picture.
  board    prints a scene's lines with the framing each one takes.
  stats    reports how often the picture changes across the game.

    python3 visual-novel/tools/direct-shots.py find
    python3 visual-novel/tools/direct-shots.py sheets --scenes 16 33
    python3 visual-novel/tools/direct-shots.py board 16

The detector and recogniser are OpenCV's YuNet and SFace models, expected in
visual-novel/.tools/models/ (ignored by git, like the Ren'Py SDK). They are
working tools only: nothing they produce is shown in the game except the
positions checked on the sheets. `find` needs them; `build`, `sheets` and
`board` work from the committed art/direction/faces.json without them.

  face_detection_yunet_2023mar.onnx
      https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx
      sha256 8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4
  face_recognition_sface_2021dec.onnx
      https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx
      sha256 0ba9fbfa01b5270c96627c4ef784da859931e02f04419c829e83484087c34e79
"""
from pathlib import Path
import argparse
import json
import re
import runpy
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

VN = Path(__file__).resolve().parents[1]
GAME = VN / 'renpy/game'
MODELS = VN / '.tools/models'
WORK = VN / 'art/direction'
FACES = WORK / 'faces.json'
PLAN = WORK / 'plan.json'
DIRECTION = GAME / 'direction.json'
OUT = VN / 'renpy/test-output/direction'

sys.path.insert(0, str(GAME))
import shotmath  # noqa: E402

DETECT_SCORE = 0.6
NAME_SCORE = 0.40          # likeness below this is not a naming
SPEAKER_SETS = {'WOMAN': 'petitioner'}      # speakers whose portrait set has another name


# ------------------------------------------------------------------ the plan

def story_pages():
    pages, scene, line = [], 0, 0
    speaker = None
    for raw in (GAME / 'story.rpy').read_text().splitlines():
        text = raw.strip()
        m = re.match(r'\$ current_scene = (\d+)', text)
        if m:
            scene = int(m.group(1)); continue
        m = re.match(r'\$ source_line = (\d+)', text)
        if m:
            line = int(m.group(1)); continue
        m = re.match(r'\$ scene_speaker = (.+)', text)
        if m:
            speaker = None if m.group(1) == 'None' else m.group(1).strip('"'); continue
        m = re.match(r'\$ source_page = (\d+)', text)
        if m:
            pages.append([scene, line, int(m.group(1)), speaker, ''])
            continue
        m = re.match(r'(?:cast\["[A-Z ]+"\] )?"(.*)"$', text)
        if m and pages and not pages[-1][4]:
            pages[-1][4] = m.group(1)
    return pages


def directed(lines, scene, line, page):
    entry = (lines.get(str(scene)) or {}).get(str(line) + ('.%d' % page if page else ''))
    if entry is None:
        return {}
    return entry if isinstance(entry, dict) else {'shot': entry}


def load_plan():
    """Every page with the painting it is read over.
    [(scene, line, page, speaker, text, stage key)]"""
    staging = json.loads((GAME / 'staging.json').read_text())['scenes']
    beats = runpy.run_path(str(VN / 'tools/check-rovel-plan.py'), run_name='direction')['load_plan']()['ROVEL_BEATS']
    lines = load_authored().get('lines', {})
    plan = []
    for scene, line, page, speaker, text in story_pages():
        if scene <= 5:
            beat = beats.get((scene, line, page))
            key = 'stage:' + beat['stage_id'] if beat else None
        else:
            key = None
            for stage in staging[str(scene)].get('stages', []):
                if (GAME / stage['image']).is_file() and (key is None or (stage.get('from', 0), stage.get('page', 0)) <= (line, page)):
                    key = stage['image']
            other = directed(lines, scene, line, page).get('stage')
            if other and (GAME / other).is_file():
                key = other
        plan.append((scene, line, page, speaker, text, key))
    return plan, staging, beats


def portrait_key(path):
    """The graded portrait behind an S001-S005 plan path (ui-reading.rpy)."""
    stem = Path(path).stem
    if not path.startswith('art/rovel/portraits/'):
        return stem
    for suffix in ('-bright', '-night', '-ordinary'):
        if stem.endswith(suffix):
            stem = stem[:-len(suffix)]
            break
    for wardrobe in ('arrival-cloak', 'arrival', 'formal', 'working'):
        if stem.endswith('-' + wardrobe):
            return stem[:-len(wardrobe) - 1]
    return stem


class Roles(object):
    """Who is spoken to on each line, and whether the speaker has a portrait
    for the oval. These follow the game's own answers: staging.rpy
    (default_listener, staging_faces) from S006 on, the authored beats of
    rovel.rpy for S001-S005."""

    def __init__(self, staging, beats):
        self.staging, self.beats = staging, beats
        self.blocks = [scene['blocks'] for scene in json.loads((GAME / 'source-map.json').read_text())['scenes']]
        self.lit = json.loads((GAME / 'lit-assets.json').read_text()).get('portraits', {})

    def _ready(self, image):
        return bool(image) and (portrait_key(image) in self.lit or (GAME / image).is_file())

    def _file(self, entry, expression, role):
        if isinstance(entry, str):
            for name in (entry + '-' + expression, entry):
                if name in self.lit:
                    return 'art/portraits/' + name + '.png'
            return None
        if isinstance(entry, dict):
            path = entry.get(role) or entry.get('speaking')
            return path if path and (GAME / path).is_file() else None
        for candidate in entry:
            path = self._file(candidate, expression, role)
            if path:
                return path
        return None

    def default_listener(self, scene, line, speaker):
        blocks = self.blocks[scene - 1]
        here = next((i for i, block in enumerate(blocks) if block['line'] >= line), len(blocks))
        previous, action_since = None, False
        for block in reversed(blocks[:here]):
            who = block.get('speaker')
            if who and who != speaker:
                previous = who
                break
            if not who:
                action_since = True
        answer = blocks[here + 1].get('speaker') if here + 1 < len(blocks) else None
        answer = answer if answer != speaker else None
        if answer and (previous is None or action_since):
            previous = answer
        return previous

    def of(self, scene, line, page, speaker):
        """(the person spoken to, whether the speaker has a portrait)."""
        if not speaker:
            return None, False
        if scene <= 5:
            beat = self.beats.get((scene, line, page)) or {}
            return (beat.get('listener') or {}).get('who'), self._ready((beat.get('speaker') or {}).get('image'))
        spec = self.staging[str(scene)]
        override = spec.get('lines', {}).get(str(line), {})
        cast = spec.get('cast', {})
        image = self._file(cast[speaker], override.get('speaker_expression', 'speaking'), 'speaking') if cast.get(speaker) else None
        return override.get('listener', self.default_listener(scene, line, speaker)), self._ready(image)


_TAG = re.compile(r'\{[^}]*\}')
# Who a line opening on She or He can mean, from the screenplay and designs.
SHE = frozenset(('TESSA', 'MARA', 'ELIN', 'HEST', 'ADA', 'ORRA', 'VASK', 'ARCHIVIST', 'WOMAN', 'MOTHER', 'HEALER'))
HE = frozenset(('IVEN', 'SENN', 'OLAN', 'LUCAN', 'VALCAIR', 'ORREN', 'SERAT', 'MARREN', 'SCHOLAR', 'GOVERNOR',
                'MESSENGER', 'APPRENTICE', 'BARGEMAN', 'ESCORT', 'BOATMAN', 'FERRYMAN', 'PRIEST', 'WARDEN',
                'CAPTAIN', 'RUNNER', 'SURGEON', 'PICKET OFFICER'))


def narration_shot(text, names):
    """Whom a line of narration is about, when nothing is directed: a name;
    'hold:she', 'hold:he' or 'hold' when it opens on a pronoun and continues
    with someone already in the scene (see resolve_hold); None for the whole
    painting. names are the people who have a framing in this painting."""
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


def leading_name(text, names):
    """The person a line opens on ("Lucan reads the recall..."), or None."""
    plain = _TAG.sub('', text).replace('\u2019', "'").strip()
    for name in names:
        if re.match(re.escape(name.split()[-1]) + r'\b', plain, re.I):
            return name
    return None


def resolve_hold(kind, recent, previous):
    """Whom a pronoun-led line stays with. recent lists the people who last
    spoke or were last written about, latest first; previous is the framing
    before this line. She keeps to the latest woman, He to the latest man."""
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
    """recent with a person put first (two are kept)."""
    if not name or not name.isupper():
        return recent
    return [name] + [n for n in recent if n != name][:1]


def resolve(plan, direction, roles, lines, stage_faces=None, whole=None):
    """The framing every page takes: [(page, first on its painting, shot
    name, framing)]. A painting arrives whole. A spoken line frames the
    person spoken to, because the speaker is already in the oval; it frames
    the speaker only when the listener is not found in this painting or the
    speaker has no portrait; where the painting is already close on the
    listener it is shown whole. Narration frames the person it is about.
    plan.json's line choices win over all of these. Whatever is chosen, the
    picture changes only for a clearly different view (same_view): otherwise
    the framing on screen is held."""
    rows, key, previous, recent, held, run = [], None, None, [], None, 0
    for page in plan:
        scene, line, pg, speaker, text, stage = page
        if not stage:
            key = None
            continue
        first = stage != key
        if first:
            recent, previous, held, run = [], None, None, 0
        key = stage
        shots = stage_shots(direction['stages'].get(stage))
        people = [n for n in shots if n.isupper()]
        chosen = directed(lines, scene, line, pg)
        name = chosen.get('shot')
        subject = speaker
        if name == 'hold':
            name = previous
        elif name is None and not first:
            if speaker:
                listener, has_portrait = roles.of(scene, line, pg, speaker)
                if has_portrait and listener in shots:
                    name = listener
                elif has_portrait and listener in (whole or {}).get(stage, ()):
                    name = 'wide'              # the painting is already close on the person spoken to
                else:
                    name = speaker
            else:
                name = narration_shot(text, people)
                if name and name.startswith('hold'):
                    name = resolve_hold(name, recent, previous)
        if not speaker:
            subject = leading_name(text, people) or (name if name in people else None)
        if name not in shots:
            name = 'wide'
        framing = shots.get(name, shotmath.WIDE)
        composed = chosen.get('shot') in shots and not chosen['shot'].isupper()      # a hand-set framing, chosen for this line
        if held is not None and chosen.get('move') != 'cut' and not composed and \
                same_view(held[1], framing, (stage_faces or {}).get(stage, ())):
            name, framing = held                          # too alike to cut to: the picture holds
            # ... but not for ever. Where people stand too close together to
            # be framed apart, a close view is all the painting has; a line
            # of narration then goes back to the whole painting, as a scene
            # returns to its master shot for the action between speeches.
            if run >= LONG_HOLD and not speaker and 'shot' not in chosen and framing[2] > 1.001:
                name, framing = 'wide', shotmath.WIDE
        run = run + 1 if (held is not None and tuple(held[1]) == tuple(framing)) else 1
        held = (name, framing)
        recent = remember(recent, subject)
        previous = name
        rows.append((page, first, name, framing))
    return rows


def stage_files(key):
    """(image to search for faces, graded image the game shows)."""
    lit = json.loads((GAME / 'lit-assets.json').read_text())
    if key.startswith('stage:'):
        graded = lit['stages'][key[6:]]['original']
        return GAME / graded, GAME / graded
    return GAME / key, GAME / lit['images'][key]['original']


def stage_lift(key, staging):
    """How far the reading screen raises a painting (its subject clears the
    text). The camera works on the raised stage, so painting coordinates
    lose this much height."""
    if key.startswith('stage:'):
        match = re.search(r"'%s': dict\(lift=(\d+)\)" % re.escape(key[6:]), (GAME / 'ui-reading.rpy').read_text())
        return int(match.group(1)) if match else 0
    for spec in staging.values():
        for stage in spec.get('stages', []):
            if stage['image'] == key:
                return stage.get('framing', {}).get('lift', 0)
    return 0


def scene_people(scene, staging, beats):
    """{name: portrait set prefix} for everyone with a portrait in a scene."""
    people = {}
    if scene <= 5:
        for (s, _line, _page), beat in beats.items():
            if s == scene:
                for role in ('speaker', 'listener'):
                    if beat.get(role):
                        who = beat[role]['who']
                        people[who] = SPEAKER_SETS.get(who, who.split()[0].lower())
        return people
    for who, entry in staging[str(scene)].get('cast', {}).items():
        entries = entry if isinstance(entry, list) else [entry]
        for item in entries:
            if isinstance(item, str):
                people[who] = item.split('-')[0]
                break
            if isinstance(item, dict):
                path = item.get('speaking') or item.get('listening')
                if path:
                    people[who] = Path(path).name.split('-')[0]
                    break
    return people


# ------------------------------------------------------------------ finding

class Finder(object):
    def __init__(self):
        cv2.setNumThreads(4)
        self.detector = cv2.FaceDetectorYN.create(str(MODELS / 'face_detection_yunet_2023mar.onnx'), '', (320, 320),
                                                  DETECT_SCORE, 0.3, 500)
        self.recogniser = cv2.FaceRecognizerSF.create(str(MODELS / 'face_recognition_sface_2021dec.onnx'), '')
        self.gallery = {}
        for path in sorted((GAME / 'art/cast').glob('*.png')):
            image = cv2.imread(str(path))
            found = self.faces(image)
            if found:
                face = max(found, key=lambda f: f[2] * f[3])
                self.gallery.setdefault(path.stem.split('-')[0], []).append(self.feature(image, face))

    def faces(self, image):
        h, w = image.shape[:2]
        self.detector.setInputSize((w, h))
        _n, found = self.detector.detect(image)
        return [] if found is None else [f for f in found]

    def feature(self, image, face):
        f = self.recogniser.feature(self.recogniser.alignCrop(image, face)).flatten()
        return f / (np.linalg.norm(f) + 1e-9)

    def likeness(self, feature, prefix):
        return max((float(np.dot(feature, g)) for g in self.gallery.get(prefix, [])), default=0.0)


def find(args):
    from scipy.optimize import linear_sum_assignment
    plan, staging, beats = load_plan()
    WORK.mkdir(parents=True, exist_ok=True)
    known = json.loads(FACES.read_text()) if FACES.is_file() else {}
    stages = {}
    for scene, _line, _page, _speaker, _text, key in plan:
        if key:
            stages.setdefault(key, set()).add(scene)
    finder = None
    for key, scenes in sorted(stages.items()):
        source, _graded = stage_files(key)
        stamp = source.stat().st_mtime
        if key in known and known[key].get('stamp') == stamp and not args.force:
            continue
        finder = finder or Finder()
        image = cv2.imread(str(source))
        if image.shape[1] != 1920:
            image = cv2.resize(image, (1920, 1080), interpolation=cv2.INTER_AREA)
        candidates = {}
        for scene in scenes:
            candidates.update(scene_people(scene, staging, beats))
        found = [f for f in finder.faces(image) if f[3] >= 20]
        found.sort(key=lambda f: -f[2] * f[3])
        names = sorted(candidates)
        scores = np.zeros((len(found), len(names)), np.float32)
        wanted = set(candidates.values())
        for i, face in enumerate(found):
            feature = finder.feature(image, face)
            # someone from another scene's cast who looks more like this face
            # than anyone here does (Olan in the hall, Mara by the arch)
            stranger = max((finder.likeness(feature, prefix) for prefix in finder.gallery if prefix not in wanted), default=0.0)
            for j, name in enumerate(names):
                like = finder.likeness(feature, candidates[name])
                scores[i, j] = like if like + 0.04 >= stranger else 0.0
        entry = {'stamp': stamp, 'faces': [], 'named': {}}
        for face in found:
            x, y, w, h = [float(v) for v in face[:4]]
            entry['faces'].append([round(x + w / 2), round(y + h / 2), round(h), round(float(face[-1]), 2)])
        if len(found) and len(names):
            rows, cols = linear_sum_assignment(-scores)
            for i, j in zip(rows, cols):
                if scores[i, j] >= NAME_SCORE:
                    entry['named'][names[j]] = [int(i), round(float(scores[i, j]), 2)]
        known[key] = entry
        print('%-58s %d faces  %s' % (key, len(found), ' '.join('%s=%d(%.2f)' % (n, v[0], v[1]) for n, v in sorted(entry['named'].items()))))
    for key in [k for k in known if k not in stages]:
        del known[key]                  # a painting no longer read over
    FACES.write_text(json.dumps(known, sort_keys=True).replace('}, "', '},\n "') + '\n')
    build(known=known)


def load_authored():
    if PLAN.is_file():
        return json.loads(PLAN.read_text())
    return {'stages': {}, 'lines': {}}


def stage_people(key, known, authored):
    """({name: face}, every face in the painting) after the corrections. A
    name given a position takes the found face at that position (and that
    face's exact box), whoever was guessed there; with no found face near, it
    stands as given."""
    entry = known.get(key) or {'faces': [], 'named': {}}
    faces = [tuple(face[:3]) for face in entry['faces']]
    people = {name: faces[index] for name, (index, _score) in entry['named'].items()}
    for name, value in ((authored['stages'].get(key) or {}).get('people') or {}).items():
        if value is None:
            people.pop(name, None)
            continue
        if isinstance(value, int):                     # an older plan: the face's number
            value = faces[value]
        x, y, h = value[:3]
        near = [f for f in faces if abs(f[0] - x) <= 0.6 * max(h, f[2]) and abs(f[1] - y) <= 0.6 * max(h, f[2])]
        face = min(near, key=lambda f: (f[0] - x) ** 2 + (f[1] - y) ** 2) if near else tuple(value[:3])
        for other in [n for n, f in people.items() if f == face]:
            people.pop(other)                          # the face is taken from whoever was guessed there
        people[name] = face
        if not near:
            faces.append(face)
    return people, faces


LONG_HOLD = 3           # pages a close framing is held before narration returns to the whole painting


def principals(framing, faces):
    """Who a framing shows: the faces whole inside it that are at least 0.6
    of the largest one's size (people in the background don't count)."""
    x0, y0, x1, y1 = shotmath.box(framing)
    inside = [f for f in faces if x0 <= f[0] <= x1 and y0 <= f[1] <= y1 and not shotmath.cuts(framing, f)]
    if not inside:
        return frozenset()
    largest = max(f[2] for f in inside)
    return frozenset((round(f[0]), round(f[1])) for f in inside if f[2] >= 0.6 * largest)


def same_view(a, b, faces=()):
    """True when two framings of a painting are too alike to cut between.
    The picture holds still (direction.rpy), so a change between two such
    framings would be a jump of part of a frame, which reads as a glitch, not
    as a new picture. They are alike when they are much the same size and
    either share more than 70% of their view, or share more than half of it
    and show the same people. Two sides of a table that share the person
    sitting between them are different views; two framings of the same three
    people are one."""
    a, b = tuple(a), tuple(b)
    if a == b:
        return True
    if max(a[2], b[2]) / min(a[2], b[2]) >= 1.25:
        return False
    shared = shotmath.overlap(a, b)
    return shared > 0.70 or (shared > 0.50 and principals(a, faces) == principals(b, faces))


def merge_alike(shots, faces):
    """People who stand close together get framings a part of a frame apart.
    Framings that are the same view become one framing between them, held: a
    two-shot composed for both, not for whoever spoke first."""
    groups = []
    for name in sorted(shots):
        for group in groups:
            if all(same_view(shots[name], shots[other], faces) for other in group):
                group.append(name)
                break
        else:
            groups.append([name])
    merged = dict(shots)
    for group in groups:
        if len(group) < 2:
            continue
        zoom = min(shots[n][2] for n in group)
        mean = shotmath.clamp((sum(shots[n][0] for n in group) / len(group),
                               sum(shots[n][1] for n in group) / len(group), zoom))
        if shotmath.breaks(mean, [f for f in faces if f[2] >= 30]):
            mean = min((shots[n] for n in group), key=lambda f: f[2])      # the widest of them was checked
        for name in group:
            merged[name] = mean
    return merged


def build(args=None, known=None):
    """Compose every framing and write the game's direction.json. Faces,
    details and hand-set framings are given in the painting's own
    coordinates; a raised painting's lift is allowed for here."""
    known = known or (json.loads(FACES.read_text()) if FACES.is_file() else {})
    authored = load_authored()
    staging = json.loads((GAME / 'staging.json').read_text())['scenes']
    direction = {'_note': 'Camera framings, and the framing every line takes, for direction.rpy. Built by '
                          'tools/direct-shots.py from art/direction/ (faces.json and the hand-made plan.json); edit '
                          'those and rebuild, not this file. A framing is [centre x, centre y, zoom] on the 1920x1080 stage.',
                 'stages': {}, 'lines': {}}
    seen = {}                # every painting's faces, for telling who a framing shows
    whole = {}               # per painting, the people the whole painting is the framing of
    for key in sorted(set(known) | set(authored['stages'])):
        spec = authored['stages'].get(key) or {}
        lift = stage_lift(key, staging)
        people, faces = stage_people(key, known, authored)
        people = {name: (f[0], f[1] - lift, f[2]) for name, f in people.items()}
        faces = [(f[0], f[1] - lift, f[2]) for f in faces]
        seen[key] = [f for f in faces if f[2] >= 30]
        shots = {}
        for name, face in people.items():
            look = (spec.get('look') or {}).get(name)
            if look is None:
                look = shotmath.look_from(face, list(people.values()))
            shots[name] = shotmath.single(face, look, faces)
        shots = merge_alike(shots, faces)
        # A framing on people that moves in by less than a quarter is the same
        # picture as the whole painting with its edges lost (same_view): those
        # people are shown by the whole painting instead.
        whole[key] = sorted(name for name, f in shots.items() if f[2] < 1.25)
        shots = {name: f for name, f in shots.items() if f[2] >= 1.25}
        for name, corners in (spec.get('details') or {}).items():
            x0, y0, x1, y1 = corners
            shots[name] = shotmath.detail(x0, y0 - lift, x1, y1 - lift)
        for name, framing in (spec.get('shots') or {}).items():
            shots[name] = shotmath.clamp((framing[0], framing[1] - lift, framing[2]))
        shots = {name: [round(f[0], 1), round(f[1], 1), round(f[2], 3)] for name, f in shots.items() if f[2] > 1.001}
        if shots:
            direction['stages'][key] = {'shots': shots}
    # Every line with the framing it takes; the game looks lines up here and
    # decides nothing itself.
    plan, _staging, beats = load_plan()
    chosen = authored.get('lines', {})
    rows = resolve(plan, direction, Roles(staging, beats), chosen, seen, whole)
    table = {}
    for (scene, line, pg, _speaker, _text, _stage), _first, name, _framing in rows:
        entry = dict(directed(chosen, scene, line, pg))        # a hand-chosen painting or move stays
        entry['shot'] = name
        table.setdefault(str(scene), {})[str(line) + ('.%d' % pg if pg else '')] = name if len(entry) == 1 else entry
    direction['lines'] = table
    save_direction(direction)
    return direction, rows


def save_direction(direction):
    """direction.json with one painting, and one scene's lines, to a line."""
    out = ['{', ' "_note": %s,' % json.dumps(direction.get('_note', '')), ' "stages": {']
    stages = sorted(direction['stages'].items())
    for n, (key, spec) in enumerate(stages):
        out.append('  %s: %s%s' % (json.dumps(key), json.dumps(spec, sort_keys=True), ',' if n < len(stages) - 1 else ''))
    out += [' },', ' "lines": {']
    lines = sorted(direction['lines'].items(), key=lambda kv: int(kv[0]))
    for n, (scene, spec) in enumerate(lines):
        ordered = sorted(spec.items(), key=lambda kv: float(kv[0]))
        body = ', '.join('%s: %s' % (json.dumps(k), json.dumps(v, sort_keys=True)) for k, v in ordered)
        out.append('  %s: {%s}%s' % (json.dumps(scene), body, ',' if n < len(lines) - 1 else ''))
    out += [' }', '}']
    DIRECTION.write_text('\n'.join(out) + '\n')
    json.loads(DIRECTION.read_text())


# ------------------------------------------------------------------ framings

def stage_shots(spec):
    return {name: tuple(framing) for name, framing in ((spec or {}).get('shots') or {}).items()}


def board(args):
    _direction, rows = build()
    for (scene, line, pg, speaker, text, key), first, name, framing in rows:
        if scene in args.scene:
            if first:
                print('\n== %s' % key)
            print('%4d%s %-8s %-10s z%.2f  %s' % (line, '.%d' % pg if pg else '  ', (speaker or '')[:8], name, framing[2], text[:86]))


def who_is_shown(resolved):
    """For the spoken lines: how many pictures hold the person spoken to (as
    the game works it out), with or without the speaker, how many are the
    whole painting, and how many are something else: a line with nobody to
    answer it, or a framing chosen by hand."""
    known = json.loads(FACES.read_text()) if FACES.is_file() else {}
    authored = load_authored()
    _plan, staging, beats = load_plan()
    roles = Roles(staging, beats)
    both = listener_only = whole = other = 0
    for (scene, line, pg, speaker, _text, stage), _first, _name, framing in resolved:
        if not speaker:
            continue
        if tuple(framing)[2] <= 1.001:
            whole += 1
            continue
        listener, _portrait = roles.of(scene, line, pg, speaker)
        people, _faces = stage_people(stage, known, authored)
        lift = stage_lift(stage, staging)
        x0, y0, x1, y1 = shotmath.box(tuple(framing))

        def held(name):
            face = people.get(name)
            return bool(face) and x0 <= face[0] <= x1 and y0 <= face[1] - lift <= y1

        if held(listener) and held(speaker):
            both += 1
        elif held(listener):
            listener_only += 1
        else:
            other += 1
    return ('%d the person spoken to alone, %d with the speaker also in the picture, %d the whole painting, '
            '%d another choice (nobody to answer, or set by hand).' % (listener_only, both, whole, other))


def stats(args=None):
    """How often the picture changes: the measure the camera exists for.
    Every change in the table is a clear one (resolve holds the picture
    between framings that are the same view)."""
    _direction, resolved = build()
    rows = [(page[0], page[5], name, tuple(framing), bool(page[3])) for page, _first, name, framing in resolved]
    paintings = pictures = 1
    held, painting_run, longest_painting, holds = 1, 1, 1, []
    for a, b in zip(rows, rows[1:]):
        painting_run = painting_run + 1 if a[1] == b[1] else 1
        longest_painting = max(longest_painting, painting_run)
        paintings += a[1] != b[1]
        if a[1] == b[1] and a[3] == b[3]:
            held += 1
            continue
        holds.append((held, a[0], a[1].rsplit('/', 1)[-1], a[2]))
        pictures, held = pictures + 1, 1
    holds.append((held, rows[-1][0], rows[-1][1].rsplit('/', 1)[-1], rows[-1][2]))
    n = float(len(rows))
    whole = sum(1 for r in rows if r[3][2] <= 1.001)
    spoken = [r for r in rows if r[4]]
    print('%d pages over paintings: %d shown whole, %d framed closer.' % (len(rows), whole, len(rows) - whole))
    print('Spoken lines: %d, of which %d over the whole painting.' % (len(spoken), sum(1 for r in spoken if r[3][2] <= 1.001)))
    print('A new painting every %.2f pages (longest stay on one painting: %d pages).' % (n / paintings, longest_painting))
    print('A different picture every %.2f pages.' % (n / pictures))
    spread = {}
    for h in holds:
        spread[min(h[0], 7)] = spread.get(min(h[0], 7), 0) + 1
    print('Pictures by how many pages they hold (7 = seven or more): '
          + ', '.join('%d: %d' % kv for kv in sorted(spread.items())))
    print('Longest holds: ' + ', '.join('%d pages S%03d %s %s' % h for h in sorted(holds, reverse=True)[:10]))
    print('Who a spoken line shows: ' + who_is_shown(resolved))
    named = sum(len(v['shots']) for v in _direction['stages'].values())
    distinct = sum(len({tuple(f) for f in v['shots'].values()}) for v in _direction['stages'].values())
    print('%d named framings over %d paintings make %d different framings (people standing together share one).'
          % (named, len(_direction['stages']), distinct))


FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
COLOURS = [(255, 214, 102), (120, 220, 255), (255, 140, 170), (160, 255, 150), (255, 170, 90), (200, 170, 255), (255, 255, 255)]


def render_shot(graded, framing, size, shade):
    x0, y0, x1, y1 = shotmath.box(framing)
    tile = graded.resize(size, Image.LANCZOS, box=(x0, y0, x1, y1))
    if shade is not None:
        tile = Image.composite(Image.new('RGB', size, (12, 12, 14)), tile, shade)
    return tile


def sheets(args):
    _plan, staging, _beats = load_plan()
    direction, resolved = build()
    known = json.loads(FACES.read_text()) if FACES.is_file() else {}
    used = {}       # stage -> {shot name: number of pages}
    order, speakers = [], {}
    for (scene, _line, _pg, speaker, _text, key), _first, name, _framing in resolved:
        if key not in used:
            order.append((scene, key))
        used.setdefault(key, {})
        used[key][name] = used[key].get(name, 0) + 1
        if speaker:
            speakers.setdefault(key, set()).add(speaker)
    OUT.mkdir(parents=True, exist_ok=True)
    tw, th = 480, 270
    mask = Image.open(GAME / 'ui/reading-shade-mask.png').getchannel('A').resize((tw, th), Image.LANCZOS).point(lambda a: int(a * 0.62))
    font, small = ImageFont.truetype(FONT, 15), ImageFont.truetype(FONT, 12)
    rows = []
    for scene, key in order:
        if args.scenes and scene not in args.scenes:
            continue
        spec = direction['stages'].get(key) or {}
        shots = stage_shots(spec)
        if not shots and not args.all:
            continue
        source, graded_path = stage_files(key)
        graded = Image.open(graded_path).convert('RGB').resize((1920, 1080), Image.LANCZOS)
        lift = stage_lift(key, staging)
        if lift:                                   # the stage as the game shows it, raised
            canvas = Image.new('RGB', (1920, 1080), (11, 16, 20))
            canvas.paste(graded, (0, -lift))
            graded = canvas
        whole = graded.resize((tw, th), Image.LANCZOS)
        draw = ImageDraw.Draw(whole)
        for n, face in enumerate((known.get(key) or {}).get('faces', [])):
            x, y, h = face[0] * tw / 1920, (face[1] - lift) * th / 1080, face[2] * th / 1080
            draw.ellipse((x - h * 0.45, y - h * 0.55, x + h * 0.45, y + h * 0.55), outline=(255, 255, 255), width=1)
            draw.text((x + h * 0.5, y - h * 0.6), str(n), fill=(255, 255, 255), font=small)
        names = sorted(shots, key=lambda n: (-used[key].get(n, 0), n))
        tiles = [(whole, 'whole  %d pages (%d as the whole)' % (sum(used[key].values()), used[key].get('wide', 0)), (255, 255, 255))]
        for n, name in enumerate(names):
            colour = COLOURS[n % len(COLOURS)]
            x0, y0, x1, y1 = [v * tw / 1920 for v in shotmath.box(shots[name])]
            draw.rectangle((x0, y0, x1 - 1, y1 - 1), outline=colour, width=2)
            tiles.append((render_shot(graded, shots[name], (tw, th), mask),
                          '%s  z%.2f  %d pages' % (name, shots[name][2], used[key].get(name, 0)), colour))
        missing = sorted(s for s in speakers.get(key, ()) if s not in shots)
        title = 'S%03d  %s%s' % (scene, key, '   NO FRAMING FOR: ' + ', '.join(missing) if missing else '')
        rows.append((title, tiles))
    for old in OUT.glob('framings-*.jpg'):
        old.unlink()
    per_row, rows_per_sheet = 4, 6
    lines = []
    for title, tiles in rows:
        for start in range(0, len(tiles), per_row):
            lines.append((title if start == 0 else '', tiles[start:start + per_row]))
    for n in range(0, len(lines), rows_per_sheet):
        group = lines[n:n + rows_per_sheet]
        sheet = Image.new('RGB', (per_row * tw, len(group) * (th + 44)), (14, 14, 16))
        draw = ImageDraw.Draw(sheet)
        for r, (title, tiles) in enumerate(group):
            y = r * (th + 44)
            draw.text((6, y + 3), title, fill=(235, 235, 235), font=font)
            for c, (tile, label, colour) in enumerate(tiles):
                sheet.paste(tile, (c * tw, y + 22))
                draw.text((c * tw + 6, y + 24 + th), label, fill=colour, font=small)
        target = OUT / ('framings-%02d.jpg' % (n // rows_per_sheet + 1))
        sheet.save(target, quality=88)
    print('%d paintings, %d sheets in %s' % (len(rows), (len(lines) + rows_per_sheet - 1) // rows_per_sheet, OUT))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('find', help='detect and name faces; write people to direction.json')
    p.add_argument('--force', action='store_true', help='search every painting again')
    p.set_defaults(run=find)
    p = sub.add_parser('build', help='compose the framings and write the game\'s direction.json')
    p.set_defaults(run=build)
    p = sub.add_parser('sheets', help='draw every framing for review')
    p.add_argument('--scenes', type=int, nargs='*')
    p.add_argument('--all', action='store_true', help='include paintings with no framings')
    p.set_defaults(run=sheets)
    p = sub.add_parser('stats', help='how often the picture changes')
    p.set_defaults(run=stats)
    p = sub.add_parser('board', help="print a scene's lines and framings")
    p.add_argument('scene', type=int, nargs='+')
    p.set_defaults(run=board)
    args = parser.parse_args()
    args.run(args)


if __name__ == '__main__':
    main()
