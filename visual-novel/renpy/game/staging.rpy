# Data-driven staging for the scenes after the authored S001-S005 plan.
#
# staging.json names each scene's painting(s) and the portrait set used for
# each speaker. A scene is read over its painting as soon as one of its stage
# files exists; until then it stays on the typeset page. Portraits appear when
# their files exist. Adding art therefore needs no code change: put the file
# at its planned path, then run tools/crop-portraits.py (portraits) and
# tools/grade-light.py (light registers, both modes).
#
# Scene entry:
#   "stages": [{"image": path, "from": first source line, "alt": description,
#               "page": page of that line's paragraph where it starts (default 0),
#               "framing": {"lift": px} or {"text": [x, y, width]}}]
#   (after changing a lift, run tools/grade-light.py: the blur band behind the
#   text is cut for the raised painting)
#   "cast":   {"SPEAKER": portrait set name, or {"speaking": path, "listening": path},
#              or a list of those, tried in order (a planned set, then a stand-in)}
#   "lines":  {"<source line>": {"speaker_expression": name,
#                                "listener": "NAME" or null,
#                                "listener_expression": name}}
# A set name resolves to art/portraits/<set>-<expression>.png, falling back
# to art/portraits/<set>.png. The listener defaults to the scene's most
# recent other speaker, unless action has intervened (people may have left or
# turned away) and another person answers straight after: then the one who
# answers. A line with no earlier speaker takes the one who answers it.

init -1 python:
    import json

    STAGING = json.loads(renpy.file('staging.json').read())['scenes']

    def _scene_spec(scene=None):
        return STAGING.get(str(current_scene if scene is None else scene))

    def staging_stage(scene=None, line=None, page=0):
        """The painting for this line and page, or None while the scene has
        no art. A stage can begin partway through a long paragraph."""
        spec = _scene_spec(scene)
        if not spec:
            return None
        at = (source_line, source_page) if line is None else (line, page)
        available = [stage for stage in spec.get('stages', []) if renpy.loadable(stage['image'])]
        if not available:
            return None
        chosen = available[0]
        for stage in available:
            if (stage.get('from', 0), stage.get('page', 0)) <= at:
                chosen = stage
        return chosen

    _listener_cache = {}

    def default_listener(scene, line, speaker):
        key = (scene, line, speaker)
        if key not in _listener_cache:
            blocks = source_map['scenes'][scene - 1]['blocks']
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
            _listener_cache[key] = previous
        return _listener_cache[key]

    def _portrait_file(entry, expression, role):
        # Ren'Py rebinds list and dict inside game code, so the entry is told
        # apart by behaviour: a set name (str), a role map (has .get), or a
        # sequence of candidates tried in order.
        if isinstance(entry, str):
            # A named set counts once its graded crop exists (the painted
            # source in art/portraits/ stays out of the distributed game).
            for name in (entry + '-' + expression, entry):
                if name in LIT.get('portraits', {}):
                    return 'art/portraits/' + name + '.png'
            return None
        if hasattr(entry, 'get'):
            path = entry.get(role) or entry.get('speaking')
            return path if path and renpy.loadable(path) else None
        for candidate in entry:
            path = _portrait_file(candidate, expression, role)
            if path:
                return path
        return None

    def staging_faces():
        """Speaker and listener portraits for the current staged line."""
        spec = _scene_spec()
        if not spec or not scene_speaker:
            return None, None
        cast = spec.get('cast', {})
        override = spec.get('lines', {}).get(str(source_line), {})
        speaker_face = listener_face = None
        if cast.get(scene_speaker):
            path = _portrait_file(cast[scene_speaker], override.get('speaker_expression', 'speaking'), 'speaking')
            if path:
                speaker_face = dict(who=scene_speaker, image=path, alt=scene_speaker.title() + '.')
        listener = override.get('listener', default_listener(current_scene, source_line, scene_speaker))
        if listener and cast.get(listener):
            path = _portrait_file(cast[listener], override.get('listener_expression', 'listening'), 'listening')
            if path:
                listener_face = dict(who=listener, image=path, alt=listener.title() + ' listens.')
        return speaker_face, listener_face
