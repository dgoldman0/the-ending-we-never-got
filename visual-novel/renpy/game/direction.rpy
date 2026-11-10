# Direction: the camera over each painting.
#
# A scene has a few paintings and many lines, so one painting is on screen for
# a long time. The camera gives each line its own picture from the painting it
# is read over: the whole frame to establish a place, a closer framing on the
# person spoken to, a detail the narration names.
#
# The picture holds still. A new framing arrives on a cut (a very short
# dissolve) and does not move while its line is read. Gliding between
# framings and a slow push-in exist as an opt-in setting only: a whole
# screen that moves on every line can make a reader motion-sick.
#
# Turning pages fast is not reading. While the reader skips, or turns two
# lines in a row in well under a second, paintings are shown whole, as the
# game showed them before the camera, so nothing jumps between close framings
# at speed. The first line read at an ordinary pace is framed again.
#
# The paintings are never cropped on disk. A framing is a centre and a zoom
# on the 1920x1080 stage. tools/direct-shots.py finds each person's face in
# each painting, composes a framing on them (eyes in the upper third, room in
# front of the face, clear of the reading shade, no neighbour cut by the edge)
# and writes direction.json; framings and line choices made by hand are kept
# in art/direction/plan.json. The same tool draws every framing for review.
#
# Which framing a line takes is decided when the direction is built, not here:
# direction.json lists every line with its framing (a spoken line frames the
# person spoken to, since the speaker is already in the oval). The game looks
# the line up and moves the camera.
#
# Settings > Camera: Framed (the default), Gliding (the moving camera), or
# Whole paintings (every painting whole, as before the camera). Reduced
# motion keeps the framings and shortens every dissolve.

default shot_key = None
default persistent.still_frames = False
default persistent.camera_glide = False

define ui_shot_cut = motion(0.16)

init -1 python:
    import json
    import math
    import time
    import shotmath

    DIRECTION = json.loads(renpy.file('direction.json').read())

    # The vignette graded into a painting sits at the painting's own corners,
    # which a close framing leaves behind; this much of it closes in again.
    CLOSE_VIGNETTE = {'ordinary': 0.17, 'night': 0.27, 'bright': 0.0}
    EASE_OVERLAP = 0.62      # gliding only: framings sharing this much of their view ease; others cut
    RUSH = 0.6               # seconds; two lines in a row turned faster than this is flipping, not reading
    RUSH_ONE = 0.3           # one line turned faster than this is flipping too

    def stage_key():
        """The painting being read over: 'stage:<id>' for an authored opening
        stage, the image path for a staged painting, None on the typeset page."""
        beat = current_rovel_beat()
        if beat:
            return 'stage:' + beat['stage_id']
        stage = staging_stage() if current_scene > 5 else None
        return stage['image'] if stage else None

    def line_key():
        return str(source_line) + ('.%d' % source_page if source_page else '')

    def stage_shots(key):
        """{name: (centre x, centre y, zoom)} for a painting, as built and
        reviewed (tools/direct-shots.py)."""
        return (DIRECTION['stages'].get(key) or {}).get('shots') or {}

    def directed_line(scene=None, line=None, page=None):
        """What direction.json says about a line: {} when nothing."""
        if line is None:
            key = line_key()
        else:
            key = str(line) + ('.%d' % page if page else '')
        entry = (DIRECTION['lines'].get(str(current_scene if scene is None else scene)) or {}).get(key)
        if entry is None:
            return {}
        return entry if hasattr(entry, 'get') else {'shot': entry}

    def line_direction():
        """(shot name, framing, move) for the line about to be read, as
        direction.json gives it. A line it doesn't list, or a framing its
        painting doesn't have, is read over the whole painting."""
        key = stage_key()
        if key is None or persistent.still_frames or stage_framing().get('text'):
            return 'wide', shotmath.WIDE, None
        shots = stage_shots(key)
        authored = directed_line()
        name = authored.get('shot')
        if name not in shots:
            name = 'wide'
        return name, tuple(shots.get(name, shotmath.WIDE)), authored.get('move')

    class StageCamera(object):
        """Where the camera is now, and where it is going. Not saved: every
        line states its own framing, so a load or a rollback simply cuts."""

        # Gliding only. An eased move settles in about a second and a half;
        # the push goes in 3% over the time a line takes to read, then rests.
        OMEGA = 3.3
        PUSH, PUSH_TIME = 0.032, 18.0

        def __init__(self):
            self.target = shotmath.WIDE
            self.cur = [shotmath.WIDE[0], shotmath.WIDE[1], 0.0]     # centre, and log zoom
            self.vel = [0.0, 0.0, 0.0]
            self.key = None
            self.frame = None
            self.creep_from = 0.0
            self.busy = False
            self.moving = False
            self.freeze = False      # captures (tools/playthrough.py): every page at its own framing, unmoving
            self.notice_rush = True  # tests turn this off so fast advancing reaches a line's own framing
            self.line_time = 0.0     # when the last line arrived, and how long the one before it was kept
            self.last_dwell = 99.0

        def _time(self):
            interface = renpy.display.interface
            return getattr(interface, 'frame_time', None) or time.time()

        def gliding(self):
            return bool(persistent.camera_glide) and not (persistent.reduced_motion or persistent.still_frames or self.freeze)

        def _creep(self, now):
            if not self.gliding():
                return 0.0
            t = min(1.0, max(0.0, now - self.creep_from) / self.PUSH_TIME)
            return self.PUSH * t * t * (3 - 2 * t)

        def rushing(self):
            """True when this line arrives too soon after the last to have
            been read; also notes the time. Called once per line."""
            now = time.time()
            dwell, before = now - self.line_time, self.last_dwell
            self.line_time, self.last_dwell = now, dwell
            if self.freeze or not self.notice_rush:
                return False
            return bool(renpy.is_skipping()) or dwell < RUSH_ONE or (dwell < RUSH and before < RUSH)

        def snap(self):
            """Stop where the target is (a setting changed, or a cut)."""
            self.cur = list(self._goal(self._time()))
            self.vel = [0.0, 0.0, 0.0]

        def _goal(self, now):
            cx, cy, z = shotmath.clamp((self.target[0], self.target[1], self.target[2] * (1 + self._creep(now))))
            return (cx, cy, math.log(z))

        def aim(self, key, framing, cut):
            now = self._time()
            if tuple(framing) != tuple(self.target):
                self.creep_from = now
            self.target = tuple(framing)
            self.key = key
            if cut or not self.gliding():
                self.snap()
            self.busy = True

        def now(self):
            """(cx, cy, zoom) for the frame being drawn; every layer drawn in
            one frame gets the same answer."""
            t = self._time()
            if t != self.frame:
                dt = 0.0 if self.frame is None else min(0.1, max(0.0, t - self.frame))
                self.frame = t
                goal = self._goal(t)
                decay = math.exp(-self.OMEGA * dt)
                far = 0.0
                for i in range(3):
                    a = self.cur[i] - goal[i]
                    b = self.vel[i] + self.OMEGA * a
                    self.cur[i] = goal[i] + (a + b * dt) * decay
                    self.vel[i] = (b - self.OMEGA * (a + b * dt)) * decay
                    scale = 1.0 if i < 2 else 1000.0
                    far = max(far, abs(self.cur[i] - goal[i]) * scale, abs(self.vel[i]) * scale * 0.2)
                self.moving = far > 0.03
                self.busy = self.moving or (self.gliding() and t - self.creep_from < self.PUSH_TIME + 1.0)
            return shotmath.clamp((self.cur[0], self.cur[1], math.exp(self.cur[2])))

        def redraw(self):
            # every frame while it moves; the slow push needs far fewer
            if not self.busy:
                return None
            return 0 if self.moving else 1.0 / 30

    stage_camera = StageCamera()

    def _camera_function(trans, st, at):
        cx, cy, z = stage_camera.now()
        trans.subpixel = True
        trans.anchor = (0, 0)
        trans.zoom = z
        trans.pos = (absolute(960.0 - cx * z), absolute(540.0 - cy * z))
        return stage_camera.redraw()

    def camera_view(picture):
        """A 1920x1080 picture as the camera frames it."""
        return Fixed(Transform(picture, function=_camera_function), xysize=(1920, 1080))

    def _vignette_function(trans, st, at):
        z = stage_camera.now()[2]
        near = min(1.0, max(0.0, (z - 1.0) / 0.45))
        trans.alpha = CLOSE_VIGNETTE.get(current_register(), 0.0) * near * near * (3 - 2 * near)
        return stage_camera.redraw()

    def close_vignette():
        return Transform('ui/close-vignette.png', xysize=(1920, 1080), function=_vignette_function)

    def stage_canvas(depth=0):
        """The stage as one 1920x1080 picture: the graded painting, raised by
        its lift over the dark ground where it has one. depth 1-4 gives the
        same picture from the painting's focus levels (the reading shade)."""
        image, lift = shown_stage()
        if image is None:
            return None
        if depth:
            levels = (LIT.get('shade', {}).get(image) or {}).get('levels')
            if not levels:
                return None
            image = levels[depth - 1]
        layers = [Transform(image, xysize=(1920, 1080), yoffset=-lift)]
        if lift:
            layers.append(Transform('ui/edge-fade.png', xsize=1920, ysize=220, ypos=1080 - lift - 220))
            layers.append(Transform(Solid('#0b1014', xysize=(1920, lift)), ypos=1080 - lift))
        return Fixed(*layers, xysize=(1920, 1080))

    def stage_files(scene, line, page=0):
        """The graded painting a line is read over, with its focus levels."""
        if scene <= 5:
            beat = ROVEL_BEATS.get((scene, line, page))
            image = lit_stage(beat['stage_id']) if beat else None
        else:
            stage = staging_stage(scene, line, page)
            image = lighting_art(stage['image']) if stage else None
        if not image:
            return []
        return [image] + list((LIT.get('shade', {}).get(image) or {}).get('levels', []))

    camera_ahead = []

    def predict_ahead():
        """Have the engine load the next painting while this line is read, so
        a change of painting doesn't wait on its five files."""
        here = stage_files(current_scene, source_line, source_page)
        upcoming = []
        if not source_page:
            upcoming.append((current_scene, source_line, 1))      # a second page of this paragraph
        later = [b['line'] for b in source_map['scenes'][current_scene - 1]['blocks'] if b['line'] > source_line]
        upcoming += [(current_scene, line, 0) for line in later[:3]]
        if len(later) < 3 and current_scene < len(source_map['scenes']):
            opening = source_map['scenes'][current_scene]['blocks'][:1]
            upcoming += [(current_scene + 1, b['line'], 0) for b in opening]
        ahead = []
        for scene, line, page in upcoming:
            files = stage_files(scene, line, page)
            if files and files != here:
                ahead = files
                break
        if ahead != list(camera_ahead):
            if camera_ahead:
                renpy.stop_predict(*camera_ahead)
            if ahead:
                renpy.start_predict(*ahead)
            camera_ahead[:] = ahead

    def direct_line():
        """Aim the camera for the line about to be read. Called before the
        painting change is noted, so `first` sees the painting change."""
        predict_ahead()
        key = stage_key()
        first = stage_image() != store.last_stage_image
        name, framing, move = line_direction()
        if stage_camera.rushing():
            name, framing = 'wide', shotmath.WIDE        # whole paintings while pages are flipped through
        previous = store.shot_key
        store.shot_key = (key, name)
        quick = renpy.is_skipping() or renpy.in_rollback()
        if first or previous is None or previous[0] != key or stage_camera.key != previous:
            stage_camera.aim(store.shot_key, framing, cut=True)      # a new painting arrives on its own dissolve
        elif tuple(framing) == tuple(stage_camera.target):
            stage_camera.aim(store.shot_key, framing, cut=False)
        else:
            ease = shotmath.overlap(stage_camera.target, framing) >= EASE_OVERLAP
            ease = {'ease': True, 'cut': False}.get(move, ease)
            if ease and not quick and stage_camera.gliding():
                stage_camera.aim(store.shot_key, framing, cut=False)
            else:
                stage_camera.aim(store.shot_key, framing, cut=True)
                if not quick:
                    renpy.transition(ui_shot_cut)

    def set_camera(glide=False, whole=False):
        """Settings > Camera. The picture stops where it is headed."""
        persistent.camera_glide = glide
        persistent.still_frames = whole
        stage_camera.snap()
        renpy.restart_interaction()
