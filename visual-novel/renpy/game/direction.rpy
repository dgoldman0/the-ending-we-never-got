# Direction: the camera over each painting.
#
# A scene has a few paintings and many lines, so one painting is on screen for
# a long time. The camera gives each line its own picture from the painting it
# is read over: the whole frame to establish a place, a closer framing on the
# person speaking, a detail the narration names. Between framings of one
# painting it eases when they share most of their view and cuts, on a short
# dissolve, when they don't; while a line is read it creeps slowly in.
#
# The paintings are never cropped on disk. A framing is a centre and a zoom
# on the 1920x1080 stage. tools/direct-shots.py finds each person's face in
# each painting, composes a framing on them (eyes in the upper third, room in
# front of the face, clear of the reading shade, no neighbour cut by the edge)
# and writes direction.json; framings and line choices made by hand are kept
# in art/direction/plan.json. Lines take the speaker's framing unless directed
# otherwise. The same tool draws every framing for review.
#
# Settings > Camera chooses whom a spoken line favours (the speaker, or the
# person spoken to); Still shows every painting whole and unmoving, as the
# game did before. Reduced motion keeps the framings and drops the movement.

default shot_key = None
default shot_recent = []
default persistent.still_frames = False
# Whom a spoken line's framing favours: the speaker, or the person spoken to
# (the speaker is already shown in the oval). Both are kept so the two can be
# compared in play; the one not chosen is to be removed.
default persistent.camera_subject = 'speaker'

define ui_shot_cut = motion(0.34)

init -1 python:
    import json
    import math
    import time
    import shotmath

    DIRECTION = json.loads(renpy.file('direction.json').read())

    # The vignette graded into a painting sits at the painting's own corners,
    # which a close framing leaves behind; this much of it closes in again.
    CLOSE_VIGNETTE = {'ordinary': 0.17, 'night': 0.27, 'bright': 0.0}
    EASE_OVERLAP = 0.62      # framings sharing this much of their view ease; others cut

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

    def line_listener():
        """The person spoken to on the current line, where the game knows."""
        beat = current_rovel_beat()
        if beat:
            face = beat.get('listener')
            return face['who'] if face else None
        spec = _scene_spec() if current_scene > 5 else None
        if not spec or not scene_speaker:
            return None
        override = spec.get('lines', {}).get(str(source_line), {})
        return override.get('listener', default_listener(current_scene, source_line, scene_speaker))

    def line_direction(first, text=''):
        """(shot name, framing, move) for the line about to be read. first is
        true when the painting has just changed: it is seen whole, unless the
        line is directed otherwise. A line that is not directed takes its
        speaker's framing; narration takes the person it is about."""
        key = stage_key()
        if key is None or persistent.still_frames or stage_framing().get('text'):
            return 'wide', shotmath.WIDE, None
        shots = stage_shots(key)
        authored = directed_line()
        name, move = authored.get('shot'), authored.get('move')
        recent = list(store.shot_recent) if (not first and store.shot_key and store.shot_key[0] == key) else []
        previous = store.shot_key[1] if (not first and store.shot_key and store.shot_key[0] == key) else None
        if name is None and not first:
            if scene_speaker:
                name = scene_speaker
                if persistent.camera_subject == 'listener' and line_listener() in shots:
                    name = line_listener()
            else:
                name = shotmath.narration_shot(text, [n for n in shots if n.isupper()])
                if name and name.startswith('hold'):
                    name = shotmath.resolve_hold(name, recent, previous)
        elif name == 'hold':
            name = previous
        if name not in shots:
            name = 'wide'
        store.shot_recent = shotmath.remember(recent, name)
        return name, tuple(shots.get(name, shotmath.WIDE)), move

    class StageCamera(object):
        """Where the camera is now, and where it is going. Not saved: every
        line states its own framing, so a load or a rollback simply cuts."""

        OMEGA = 3.3           # an eased move settles in about a second and a half
        CREEP = shotmath.CREEP   # the slow push while a line is read
        CREEP_TIME = 18.0

        def __init__(self):
            self.target = shotmath.WIDE
            self.cur = [shotmath.WIDE[0], shotmath.WIDE[1], 0.0]     # centre, and log zoom
            self.vel = [0.0, 0.0, 0.0]
            self.key = None
            self.frame = None
            self.creep_from = 0.0
            self.busy = False
            self.moving = False
            self.freeze = False      # captures (tools/playthrough.py): no movement, the push held halfway

        def _time(self):
            interface = renpy.display.interface
            return getattr(interface, 'frame_time', None) or time.time()

        def _creep(self, now):
            if persistent.reduced_motion or persistent.still_frames:
                return 0.0
            if self.freeze:
                return self.CREEP * 0.5
            t = min(1.0, max(0.0, (now - self.creep_from) / self.CREEP_TIME))
            return self.CREEP * t * t * (3 - 2 * t)

        def _goal(self, now):
            cx, cy, z = shotmath.clamp((self.target[0], self.target[1], self.target[2] * (1 + self._creep(now))))
            return (cx, cy, math.log(z))

        def aim(self, key, framing, cut):
            now = self._time()
            if tuple(framing) != tuple(self.target):
                self.creep_from = now
            self.target = tuple(framing)
            self.key = key
            if cut or self.freeze:
                self.cur = list(self._goal(now))
                self.vel = [0.0, 0.0, 0.0]
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
                still = persistent.reduced_motion or persistent.still_frames or self.freeze
                self.moving = far > 0.03
                self.busy = self.moving or (not still and self._creep(t) < self.CREEP * 0.999)
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

    def direct_line(text=''):
        """Aim the camera for the line about to be read. Called before the
        painting change is noted, so `first` sees the painting change."""
        key = stage_key()
        first = stage_image() != store.last_stage_image
        name, framing, move = line_direction(first, text)
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
            if ease and not quick and not persistent.reduced_motion:
                stage_camera.aim(store.shot_key, framing, cut=False)
            else:
                stage_camera.aim(store.shot_key, framing, cut=True)
                if not quick:
                    renpy.transition(ui_shot_cut)
