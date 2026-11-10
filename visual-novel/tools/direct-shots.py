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
                 "people":  {"TESSA": 3,              face number 3 is Tessa
                             "MARA": [388, 204, 56],  a face set by hand: x, y, height
                             "SENN": null},           do not frame this person
                 "look":    {"TESSA": 1},             she looks toward screen right (-1 left, 0 ahead)
                 "details": {"book": [800, 560, 1180, 760]},   a box of the painting to show
                 "shots":   {"table": [960, 600, 1.3]}}},      a framing set outright: centre x, y, zoom
             "lines":  {"16": {"655": "book", "669": "hold",
                               "680": {"shot": "TESSA", "move": "ease"}}}
           A line with no entry takes its speaker's framing; narration takes
           the whole painting; "hold" keeps the framing of the line before.
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
    FACES.write_text(json.dumps(known, sort_keys=True).replace('}, "', '},\n "') + '\n')
    build(known=known)


def load_authored():
    if PLAN.is_file():
        return json.loads(PLAN.read_text())
    return {'stages': {}, 'lines': {}}


def stage_people(key, known, authored):
    """({name: face}, every face in the painting) after the corrections."""
    entry = known.get(key) or {'faces': [], 'named': {}}
    faces = [tuple(face[:3]) for face in entry['faces']]
    people = {name: faces[index] for name, (index, _score) in entry['named'].items()}
    for name, value in ((authored['stages'].get(key) or {}).get('people') or {}).items():
        if value is None:
            people.pop(name, None)
        elif isinstance(value, int):
            for other in [n for n, face in people.items() if face == faces[value]]:
                people.pop(other)           # a face named by hand is taken from whoever was guessed there
            people[name] = faces[value]
        else:
            people[name] = tuple(value)
            faces.append(tuple(value))
    return people, faces


def build(args=None, known=None):
    """Compose every framing and write the game's direction.json. Faces,
    details and hand-set framings are given in the painting's own
    coordinates; a raised painting's lift is allowed for here."""
    known = known or (json.loads(FACES.read_text()) if FACES.is_file() else {})
    authored = load_authored()
    staging = json.loads((GAME / 'staging.json').read_text())['scenes']
    direction = {'_note': 'Camera framings and line direction for direction.rpy. Built by tools/direct-shots.py '
                          'from art/direction/ (faces.json and the hand-made plan.json); edit those, not this file. '
                          'A framing is [centre x, centre y, zoom] on the 1920x1080 stage.',
                 'stages': {}, 'lines': authored.get('lines', {})}
    for key in sorted(set(known) | set(authored['stages'])):
        spec = authored['stages'].get(key) or {}
        lift = stage_lift(key, staging)
        people, faces = stage_people(key, known, authored)
        people = {name: (f[0], f[1] - lift, f[2]) for name, f in people.items()}
        faces = [(f[0], f[1] - lift, f[2]) for f in faces]
        shots = {}
        for name, face in people.items():
            look = (spec.get('look') or {}).get(name)
            if look is None:
                look = shotmath.look_from(face, list(people.values()))
            shots[name] = shotmath.single(face, look, faces)
        for name, corners in (spec.get('details') or {}).items():
            x0, y0, x1, y1 = corners
            shots[name] = shotmath.detail(x0, y0 - lift, x1, y1 - lift)
        for name, framing in (spec.get('shots') or {}).items():
            shots[name] = shotmath.clamp((framing[0], framing[1] - lift, framing[2]))
        shots = {name: [round(f[0], 1), round(f[1], 1), round(f[2], 3)] for name, f in shots.items() if f[2] > 1.001}
        if shots:
            direction['stages'][key] = {'shots': shots}
    save_direction(direction)
    return direction


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


class Shots(object):
    """Walks the pages as the game does (direction.rpy: line_direction)."""

    def __init__(self, direction):
        self.direction = direction
        self.key = self.previous = None
        self.recent = []

    def line(self, page):
        scene, line, pg, speaker, text, key = page
        first = key != self.key
        if first:
            self.recent, self.previous = [], None
        self.key = key
        shots = stage_shots(self.direction['stages'].get(key))
        name = directed(self.direction['lines'], scene, line, pg).get('shot')
        if name is None and not first:
            if speaker:
                name = speaker
            else:
                name = shotmath.narration_shot(text, [n for n in shots if n.isupper()])
                if name and name.startswith('hold'):
                    name = shotmath.resolve_hold(name, self.recent, self.previous)
        elif name == 'hold':
            name = self.previous
        if name not in shots:
            name = 'wide'
        self.recent = shotmath.remember(self.recent, name)
        self.previous = name
        return first, name, shots.get(name, shotmath.WIDE)


def board(args):
    plan, _staging, _beats = load_plan()
    walk = Shots(build())
    for page in plan:
        scene, line, pg, speaker, text, key = page
        if not key:
            walk.key = None
            continue
        first, name, framing = walk.line(page)
        if scene in args.scene:
            if first:
                print('\n== %s' % key)
            print('%4d%s %-8s %-10s z%.2f  %s' % (line, '.%d' % pg if pg else '  ', (speaker or '')[:8], name, framing[2], text[:86]))


def stats(args=None):
    """How often the picture changes: the measure the camera exists for."""
    plan, _staging, _beats = load_plan()
    walk = Shots(build())
    rows = []
    for page in plan:
        if not page[5]:
            walk.key = None
            continue
        _first, name, framing = walk.line(page)
        rows.append((page[0], page[5], name, tuple(framing), bool(page[3])))
    pictures, held, holds = 1, 1, []
    for a, b in zip(rows, rows[1:]):
        if a[1] == b[1] and a[3] == b[3]:
            held += 1
        else:
            holds.append((held, a[0], a[1].rsplit('/', 1)[-1], a[2]))
            pictures, held = pictures + 1, 1
    holds.append((held, rows[-1][0], rows[-1][1].rsplit('/', 1)[-1], rows[-1][2]))
    paintings, held, longest = 1, 1, 1
    for a, b in zip(rows, rows[1:]):
        held = held + 1 if a[1] == b[1] else 1
        paintings += a[1] != b[1]
        longest = max(longest, held)
    whole = sum(1 for r in rows if r[3][2] <= 1.001)
    spoken = [r for r in rows if r[4]]
    print('%d pages over paintings: %d shown whole, %d framed closer.' % (len(rows), whole, len(rows) - whole))
    print('Spoken lines: %d, of which %d over the whole painting.' % (len(spoken), sum(1 for r in spoken if r[3][2] <= 1.001)))
    print('The picture changes every %.2f pages (every %.2f with the paintings alone; longest hold then %d pages).'
          % (len(rows) / float(pictures), len(rows) / float(paintings), longest))
    print('Longest holds now: ' + ', '.join('%d pages S%03d %s %s' % h for h in sorted(holds, reverse=True)[:6]))


FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
COLOURS = [(255, 214, 102), (120, 220, 255), (255, 140, 170), (160, 255, 150), (255, 170, 90), (200, 170, 255), (255, 255, 255)]


def render_shot(graded, framing, size, shade):
    x0, y0, x1, y1 = shotmath.box(framing)
    tile = graded.resize(size, Image.LANCZOS, box=(x0, y0, x1, y1))
    if shade is not None:
        tile = Image.composite(Image.new('RGB', size, (12, 12, 14)), tile, shade)
    return tile


def sheets(args):
    plan, staging, _beats = load_plan()
    direction = build()
    known = json.loads(FACES.read_text()) if FACES.is_file() else {}
    used = {}       # stage -> {shot name: number of pages}
    order, speakers = [], {}
    walk = Shots(direction)
    for page in plan:
        scene, _line, _pg, speaker, _text, key = page
        if not key:
            walk.key = None
            continue
        _first, name, _framing = walk.line(page)
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
