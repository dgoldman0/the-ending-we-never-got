# Original timeline only. No post-question presentation is implemented here.
init python:
    def composed_scene():
        if current_scene == 1 and 29 <= source_line <= 49 and renpy.loadable('art/cg/sealed-arch.png'):
            return 'art/cg/sealed-arch.png'
        if current_scene == 2 and source_line >= 112:
            return 'art/cg/mothers-chair.png'
        return None

    def side_reading():
        return current_scene == 2 and source_line >= 112

    def current_art_description():
        beat = current_rovel_beat()
        if beat:
            faces = [face['alt'] for face in (beat.get('speaker'), beat.get('listener')) if face]
            return beat['stage']['alt'] + (' ' + ' '.join(faces) if faces else '')
        shot = opening_shot()
        if opening_assets_available(shot):
            return shot['alt']
        if side_reading():
            return 'Tessa leans over the welcome letter in her plain blue hoodie. Her right hand draws her mother’s chair. The dead phone lies beside the page; candlelight leaves most of the locked room in darkness.'
        if composed_scene():
            return 'Nineteen-year-old Tessa turns from the cracked, sealed arch toward Senn. Harsh light falls across both faces and the pale stone. She has not yet been given a cloak.'
        return scene_art_alt
