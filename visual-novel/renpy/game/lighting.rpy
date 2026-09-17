# Lighting is a reader preference, independent of story position and save state.
default persistent.intense_lighting = True

init python:
    import json
    LIGHTING_VARIANTS = json.loads(renpy.file('lighting-assets.json').read())

    def lighting_art(path):
        if persistent.intense_lighting:
            return path
        return LIGHTING_VARIANTS.get(path, path)
