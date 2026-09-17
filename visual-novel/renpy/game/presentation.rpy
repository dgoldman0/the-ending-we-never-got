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
        shot = opening_shot()
        if opening_ready(shot):
            return shot['alt']
        if side_reading():
            return 'Tessa leans over the welcome letter in her plain blue hoodie. Her right hand draws her mother’s chair. The dead phone lies beside the page; candlelight leaves most of the locked room in darkness.'
        if composed_scene():
            return 'Nineteen-year-old Tessa turns from the cracked, sealed arch toward Senn. Harsh light falls across both faces and the pale stone. She has not yet been given a cloak.'
        return scene_art_alt

# Vector UI assets contain only tonal scrims, not substitute illustrations.
screen original_backdrop():
    add 'art/cg/mothers-chair.png' xysize (1920, 1080)
    add Solid('#0b1216ed')

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
    hover_background Solid('#e0d3b31b')
    selected_background Solid('#e0d3b321')
    padding (18, 12)

style button_text:
    font 'fonts/ClearSans-Regular.ttf'
    size 26
    color '#cbc8bf'
    hover_color '#fff2d9'
    selected_color '#efd2a3'
    insensitive_color '#716f69'

style quiet_button is button:
    padding (15, 9)
style quiet_button_text is button_text:
    size 22

style hero_button is button:
    padding (0, 9)
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
