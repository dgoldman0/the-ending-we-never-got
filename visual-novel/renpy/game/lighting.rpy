# The original timeline's light is fixed at the Softened strength: the user
# removed the Intense mode and the lighting setting on 24 September 2026.
# Stage II (after the player answers Yes; not yet built) is to use regular,
# undistorted light.
#
# Scene images come from tools/grade-light.py, which renders each one into
# its light register with the distortion baked in and permanent: bright
# (white-hot spilling glare, halation, colour splitting at the edges),
# ordinary (sallow light, cold shade, bleach bypass, uneven exposure,
# vignette) or night (sunk light, cold shade, glowing warm sources). Nothing
# fades back to comfort. lit-assets.json maps stages and images to the graded
# files for each mode.

init -1 python:
    import json
    LIGHTING_VARIANTS = json.loads(renpy.file('lighting-assets.json').read())
    LIT = json.loads(renpy.file('lit-assets.json').read())

    LIGHT_MODE = 'softened'

    def light_mode():
        return LIGHT_MODE

    def lit_stage(stage_id):
        """The graded composite for an authored stage, or None."""
        entry = LIT['stages'].get(stage_id)
        return entry[light_mode()] if entry else None

    def lighting_art(path):
        entry = LIT['images'].get(path)
        if entry:
            return entry[light_mode()]
        if path in LIGHTING_VARIANTS:
            return LIGHTING_VARIANTS[path]
        # New art follows a convention: its Softened twin mirrors the path
        # under art/softened/. Without a twin the Intense file is used.
        if path.startswith('art/') and not path.startswith('art/softened/'):
            twin = 'art/softened/' + path[4:]
            if renpy.loadable(twin):
                return twin
        return path

    def current_register():
        """bright, ordinary or night for the scene being read."""
        beat = current_rovel_beat()
        if beat:
            return beat.get('grade', 'ordinary')
        spec = _scene_spec() if current_scene > 5 else None
        return (spec or {}).get('grade', 'ordinary')

    # Gilt ornament (portrait frames, the speaker rail) catches the scene's
    # light: hotter and paler in glare, dim and warm by candle.
    _FRAME_LIGHT = {
        ('bright', 'intense'): lambda: BrightnessMatrix(0.07) * SaturationMatrix(0.8),
        ('bright', 'softened'): lambda: BrightnessMatrix(0.03) * SaturationMatrix(0.92),
        ('ordinary', 'intense'): lambda: TintMatrix('#ecebd9') * SaturationMatrix(0.85),
        ('night', 'intense'): lambda: TintMatrix('#8f7f6c') * SaturationMatrix(0.8),
        ('night', 'softened'): lambda: TintMatrix('#b8aa98') * SaturationMatrix(0.9),
    }

    def frame_light():
        make = _FRAME_LIGHT.get((current_register(), light_mode()))
        return make() if make else None
