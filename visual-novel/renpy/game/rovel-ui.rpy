# Shared reading family. Source state selects performance; the screen owns layout.
init python:
    # Space remains a reading key when a footer control has mouse focus. Ren'Py's
    # unfocused dismissal retains its normal reveal/advance behavior.
    if 'K_SPACE' not in config.keymap['dismiss_unfocused']:
        config.keymap['dismiss_unfocused'].append('K_SPACE')

    def current_rovel_beat():
        return rovel_beat(current_scene, source_line, source_page) if 1 <= current_scene <= 5 else None

    def rovel_face_ready(face):
        return face is not None and renpy.loadable(face['image'])

    def narrative_save_name():
        chapter = chapter_names[current_chapter - 1] if current_chapter else ''
        return chapter + ' · ' + scene_location.split(' · ')[0]

    def rovel_save_context(data):
        data['chapter'] = chapter_names[current_chapter - 1] if current_chapter else ''
        data['place'] = scene_location

    config.save_json_callbacks.append(rovel_save_context)

    def rovel_slot_place(slot):
        place = FileJson(slot, 'place', empty='An empty place', missing='A saved moment')
        place = place.replace("'S ", "'s ")
        return place if len(place) <= 39 else place[:36].rsplit(' ', 1)[0] + '…'

screen rovel_stage(beat):
    $ stage = beat['stage']
    add lighting_art(stage['image']) xysize (1920,1080)
    for actor in stage['actors']:
        add lighting_art(actor['image']) xpos actor['x'] ypos actor['y'] xysize (actor['w'],actor['h'])

screen rovel_reading(who, what):
    $ beat = current_rovel_beat()
    $ speaking_face = beat.get('speaker') if beat else None
    $ listening_face = beat.get('listener') if beat else None
    $ dark_scene = current_scene == 2
    $ quiet_side = not who and current_scene == 2 and source_line >= 110
    $ hand_insert = not who and current_scene == 3 and source_line == 160
    $ applause_insert = not who and current_scene == 4 and source_line == 185
    $ steps_insert = not who and current_scene == 4 and source_line in (206,214)
    $ threshold_insert = not who and current_scene == 1 and source_line in (9,15,17)
    $ milk_insert = not who and current_scene == 1 and source_line == 11
    $ night_window_insert = not who and current_scene == 2 and source_line in (69,71)
    $ cloak_insert = not who and current_scene == 2 and source_line == 101
    $ shared_seat_insert = not who and current_scene == 5 and source_line == 250
    $ treatment_insert = not who and current_scene == 3 and source_line in (118,120,138,143,145,150,152)
    $ lower_insert = applause_insert or steps_insert or threshold_insert or milk_insert or treatment_insert or shared_seat_insert
    $ right_insert = steps_insert or threshold_insert or night_window_insert or treatment_insert or shared_seat_insert
    if quiet_side or hand_insert or lower_insert or night_window_insert or cloak_insert:
        window:
            id 'window'
            xpos (1050 if right_insert else 70) ypos (1015 if lower_insert else (265 if quiet_side else 145))
            yanchor (1.0 if lower_insert else 0.0)
            xsize (800 if (lower_insert or night_window_insert) else 660) yminimum 275
            background Frame('art/rovel/ui/quiet-surface.png',80,55,100,60)
            padding (60,48,90,48)
            text what:
                id 'what'
                font 'fonts/EBGaramond12-Regular.ttf'
                size (40 if persistent.large_text else 36)
                color ('#c6c7c3' if dark_scene else '#efe7d8')
                line_spacing 5
    else:
        window:
            id 'window'
            xpos 60 ypos 738 xsize 1800 ysize 280
            background (Frame('art/rovel/ui/reading-surface.png',260,55,100,145) if who else Frame('art/rovel/ui/quiet-surface.png',80,55,100,60))
            padding (0,0)
            if who:
                if rovel_face_ready(speaking_face):
                    add lighting_art(speaking_face['image']) xpos 36 ypos 20 xysize (240,240)
                text who:
                    id 'who'
                    xpos 310 ypos 29
                    font 'fonts/ClearSans-Medium.ttf'
                    size (29 if persistent.large_text else 25)
                    color ('#b8aa91' if dark_scene else '#d3b98b')
                    kerning 1.2
                text what:
                    id 'what'
                    xpos 310 ypos 77 xsize 1190
                    font 'fonts/EBGaramond12-Regular.ttf'
                    size (42 if persistent.large_text else 38)
                    line_spacing 5
                    color ('#c6c7c3' if dark_scene else '#efe7d8')
                if rovel_face_ready(listening_face):
                    add lighting_art(listening_face['image']) xpos 1550 ypos 72 xysize (160,160)
                    text listening_face['who'].title():
                        xpos 1630 ypos 225 xanchor 0.5
                        size (22 if persistent.large_text else 19) color '#a5a498'
            else:
                text what:
                    id 'what'
                    xpos 115 ypos 55 xsize 1565
                    font 'fonts/EBGaramond12-Regular.ttf'
                    size (41 if persistent.large_text else 37)
                    line_spacing 6
                    color ('#c6c7c3' if dark_scene else '#efe7d8')

screen rovel_inspection_origin(beat):
    # Render the authored scene again above the scrim, never a room-only
    # substitute or a cached screenshot from a different reading point.
    fixed:
        xysize (1920,1080)
        if beat:
            use rovel_stage(beat)
            # Compact exchanges remove the large stage cutouts. Preserve their
            # current performers in this context view as well as the setting.
            if beat.get('speaker'):
                $ origin_words = renpy.last_say().what or ''
                use rovel_reading(beat['speaker']['who'].title(), origin_words)
        else:
            # Later source coverage stays exactly as limited as the story view;
            # an inspection must not invent a different scene or cast for it.
            use story_stage

screen rovel_inspection_shell(title):
    $ inspection_beat = current_rovel_beat()
    if inspection_beat:
        use rovel_stage(inspection_beat)
    elif art_available():
        add lighting_art(scene_art) xysize (1920,1080)
    else:
        use original_backdrop
    add Solid('#070e16da')
    add Frame('art/rovel/ui/quiet-surface.png',80,55,100,60) xpos 50 ypos 125 xysize (1820,885)
    text title xpos 120 ypos 70 font 'fonts/EBGaramond12-Regular.ttf' size 62 color '#eee2cd'
    if current_scene:
        # The complete 16:9 origin remains recognizable above the comparison.
        # Keep the detail panels and Return target in their established places.
        text scene_location.replace("'S ", "'s "):
            xpos 560 ypos 78 xsize 360
            font 'fonts/ClearSans-Regular.ttf' size 25 color '#c5bba9'
            line_spacing 5
        add Solid('#a99370') xpos 968 ypos 10 xysize (356,202)
        fixed:
            xpos 970 ypos 12 xysize (352,198)
            clipping True
            fixed:
                at Transform(zoom=352.0/1920.0)
                xysize (1920,1080)
                use rovel_inspection_origin(inspection_beat)
    textbutton 'Return to story':
        id 'menu_return'
        xpos 1540 ypos 73 xsize 280
        action Return()
        style 'quiet_button'
    fixed:
        xpos 120 ypos 220 xsize 1680 ysize 760
        transclude
    key 'game_menu' action Return()
