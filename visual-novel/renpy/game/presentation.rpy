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

screen original_backdrop():
    add Solid('#080f18')
    add Frame('art/rovel/ui/quiet-surface.png',80,55,100,60) xpos 45 ypos 90 xysize (1830,955)

style title_text:
    font 'fonts/EBGaramond12-Regular.ttf'
    size 96
    color '#eee3d3'
    line_spacing -4

style prose_text:
    font 'fonts/CharisSIL-Regular.ttf'
    size 32
    color '#e4ded3'
    line_spacing 9

style caption_text:
    font 'fonts/ClearSans-Regular.ttf'
    size 20
    color '#b8b3a5'
    kerning 1.4

style button:
    background None
    # Small controls need a quiet focus cue; compressing the reading ornament
    # into a page-number button produced a jagged, illegible mark.
    hover_background Solid('#c5ab7b16')
    selected_background Solid('#c5ab7b10')
    padding (18, 12)

style button_text:
    font 'fonts/ClearSans-Regular.ttf'
    size 26
    color '#cbc8bf'
    hover_color '#fff2d9'
    selected_color '#efd2a3'
    hover_underline True
    selected_underline True
    insensitive_color '#716f69'

style quiet_button is button:
    padding (15, 9)
style quiet_button_text is button_text:
    size 26

style hero_button is button:
    padding (24, 10)
    xsize 390
style hero_button_text is button_text:
    font 'fonts/EBGaramond12-Regular.ttf'
    size 47
    color '#f2dfbd'

style bar:
    ysize 8
    left_bar Solid('#baa988')
    right_bar Solid('#3c4646')
    thumb Solid('#eedec1', xsize=16, ysize=28)
    thumb_offset 8
style vscrollbar:
    xsize 5
    base_bar Solid('#293332')
    thumb Solid('#aca38c')
