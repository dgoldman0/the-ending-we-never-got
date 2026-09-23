# Lighting is a reader preference, independent of story position and save state.
default persistent.intense_lighting = True

init python:
    import json
    LIGHTING_VARIANTS = json.loads(renpy.file('lighting-assets.json').read())

    def lighting_art(path):
        if persistent.intense_lighting:
            return path
        if path in LIGHTING_VARIANTS:
            return LIGHTING_VARIANTS[path]
        # New art follows a convention: its Softened twin mirrors the path
        # under art/softened/. Without a twin the Intense file is used.
        if path.startswith('art/') and not path.startswith('art/softened/'):
            twin = 'art/softened/' + path[4:]
            if renpy.loadable(twin):
                return twin
        return path
