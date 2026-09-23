# Data-driven staging for the scenes after the authored S001-S005 plan.
#
# staging.json names each scene's painting(s) and the portrait set used for
# each speaker. A scene is read over its painting as soon as one of its stage
# files exists; until then it stays on the typeset page. Portraits appear when
# their files exist. Adding art therefore needs no code change: put the file
# at its planned path (and its Softened twin under art/softened/), then run
# tools/portrait-faces.py for new portraits.
#
# Scene entry:
#   "stages": [{"image": path, "from": first source line, "alt": description,
#               "framing": {"lift": px} or {"text": [x, y, width]}}]
#   "cast":   {"SPEAKER": portrait set name, or {"speaking": path, "listening": path}}
#   "lines":  {"<source line>": {"speaker_expression": name,
#                                "listener": "NAME" or null,
#                                "listener_expression": name}}
# A set name resolves to art/portraits/<set>-<expression>.png, falling back
# to art/portraits/<set>.png. The listener defaults to the scene's most
# recent other speaker.

init -1 python:
    import json

    STAGING = json.loads(renpy.file('staging.json').read())['scenes']

    def _scene_spec(scene=None):
        return STAGING.get(str(current_scene if scene is None else scene))

    def staging_stage(scene=None, line=None):
        """The painting for this line, or None while the scene has no art."""
        spec = _scene_spec(scene)
        if not spec:
            return None
        line = source_line if line is None else line
        available = [stage for stage in spec.get('stages', []) if renpy.loadable(stage['image'])]
        if not available:
            return None
        chosen = available[0]
        for stage in available:
            if stage.get('from', 0) <= line:
                chosen = stage
        return chosen

    _previous_cache = {}

    def previous_other_speaker(scene, line, speaker):
        key = (scene, line, speaker)
        if key not in _previous_cache:
            found = None
            for block in source_map['scenes'][scene - 1]['blocks']:
                if block['line'] >= line:
                    break
                who = block.get('speaker')
                if who and who != speaker:
                    found = who
            _previous_cache[key] = found
        return _previous_cache[key]

    def _portrait_file(entry, expression, role):
        # Game code sees Ren'Py's revertable dict type as `dict`, so test for
        # the string case: a set name. Otherwise it maps roles to files.
        if not isinstance(entry, str):
            path = entry.get(role) or entry.get('speaking')
            return path if path and renpy.loadable(path) else None
        for name in (entry + '-' + expression, entry):
            path = 'art/portraits/' + name + '.png'
            if renpy.loadable(path):
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
        listener = override.get('listener', previous_other_speaker(current_scene, source_line, scene_speaker))
        if listener and cast.get(listener):
            path = _portrait_file(cast[listener], override.get('listener_expression', 'listening'), 'listening')
            if path:
                listener_face = dict(who=listener, image=path, alt=listener.title() + ' listens.')
        return speaker_face, listener_face
