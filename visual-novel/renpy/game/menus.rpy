screen main_menu():
    tag menu
    add 'art/opening/cg/drawing-restart.png' xysize (1920, 1080)
    add 'art/opening/ui/title-ornament.svg'
    text 'THE ORIGINAL TIMELINE' xpos 156 ypos 242 style 'caption_text'
    text 'The Ending\nWe Never Got':
        xpos 146 ypos 307 xsize 780
        style 'title_text' size 116
    vbox:
        xpos 138 ypos 664 spacing 10
        if renpy.newest_slot() is not None:
            textbutton 'Continue' action Continue() style 'hero_button'
            textbutton 'Begin again' id 'main_begin' action Start()
        else:
            textbutton 'Begin' id 'main_begin' action Start() style 'hero_button'
        hbox:
            spacing 8
            textbutton 'Load' action ShowMenu('load') style 'quiet_button'
            textbutton 'Settings' action ShowMenu('preferences') style 'quiet_button'
            textbutton 'About' action ShowMenu('about') style 'quiet_button'
    text 'A life interrupted.' xpos 156 ypos 967:
        font 'fonts/EBGaramond12-Italic.ttf' size 29 color '#b6ad9b'
    if not renpy.emscripten:
        textbutton 'Quit' action Quit(confirm=True) xpos 1730 ypos 958 style 'quiet_button'

screen menu_frame(title):
    use original_backdrop
    hbox:
        xpos 145 ypos 26 spacing 16
        if not main_menu:
            textbutton 'History' action ShowMenu('history') style 'quiet_button'
            textbutton 'Threads' action ShowMenu('threads') style 'quiet_button'
            textbutton 'Save' action ShowMenu('save') style 'quiet_button'
        textbutton 'Load' action ShowMenu('load') style 'quiet_button'
        textbutton 'Settings' action ShowMenu('preferences') style 'quiet_button'
        textbutton 'About' action ShowMenu('about') style 'quiet_button'
        if not main_menu:
            textbutton 'Title screen' action MainMenu() style 'quiet_button'
    text title xpos 160 ypos 105 font 'fonts/EBGaramond12-Regular.ttf' size 70 color '#eee3d3'
    textbutton ('Return to title' if main_menu else 'Return to story'):
        id 'menu_return'
        action Return()
        xalign 0.91 ypos 112 style 'quiet_button'
    frame:
        background None
        xpos 160 ypos 240 xsize 1600 ysize 790
        padding (0, 0)
        transclude

screen save():
    tag menu
    use file_slots('Save your place', True)

screen load():
    tag menu
    use file_slots('Return to a moment', False)

screen file_slots(title, saving):
    use menu_frame(title):
        vbox:
            spacing 23
            grid 3 2:
                spacing 24
                for slot in range(1, 7):
                    button:
                        id ('file_slot_' + str(slot))
                        xsize 514 ysize 305
                        padding (10, 10)
                        action (FileSave(slot) if saving else FileLoad(slot))
                        background Solid('#ffffff07')
                        hover_background Solid('#cfb38724')
                        vbox:
                            spacing 10
                            add FileScreenshot(slot) xysize (494, 247)
                            text FileTime(slot, format='%b %d · %H:%M', empty='An empty place') size 21 color '#bdb6a6'
            hbox:
                spacing 10
                for page in range(1, 6):
                    textbutton str(page) action FilePage(str(page)) xsize 62
                textbutton 'Auto' action FilePage('auto')
            if renpy.emscripten:
                text 'Saves stay in this browser. Use its top-left menu to export a backup.' size 21 color '#b0ada3'

screen preferences():
    tag menu
    use menu_frame('Reading settings'):
        hbox:
            spacing 145
            vbox:
                xsize 720 spacing 24
                text 'TEXT' style 'caption_text'
                hbox:
                    spacing 12
                    textbutton 'Standard' action SetField(persistent, 'large_text', False) selected not persistent.large_text
                    textbutton 'Larger' action SetField(persistent, 'large_text', True) selected persistent.large_text
                text 'Text speed' size 26
                bar value Preference('text speed') style 'bar' xsize 650 ysize 24
                text 'Move all the way right to show each line at once.' size 22 color '#b6b0a2'
                null height 25
                text 'ACCESS' style 'caption_text'
                textbutton 'Reduced motion' action ToggleField(persistent, 'reduced_motion')
                textbutton 'Image descriptions' action ToggleField(persistent, 'art_descriptions')
                textbutton 'Self-voicing' action Preference('self voicing', 'toggle')
            vbox:
                xsize 695 spacing 28
                text 'DISPLAY' style 'caption_text'
                hbox:
                    spacing 12
                    textbutton 'Window' action Preference('display', 'window')
                    textbutton 'Fullscreen' action Preference('display', 'fullscreen')
                null height 25
                text 'AT YOUR PACE' style 'caption_text'
                text 'Space or Enter turns the page. Page Up returns to an earlier line. Escape opens or closes the menu.' style 'prose_text'
                text 'Arrow keys move between controls; Enter selects. Press V for self-voicing. Look closer offers the same details through labeled controls and the image.' size 26 color '#bdb7ab' line_spacing 9

screen history():
    tag menu
    use menu_frame('Previously read'):
        viewport:
            mousewheel True draggable True scrollbars 'vertical'
            yinitial 1.0
            vbox:
                spacing 29 xsize 1470
                if not _history_list:
                    text 'The story will leave its words here.' style 'prose_text'
                for h in _history_list:
                    vbox:
                        spacing 9
                        if h.who:
                            text h.who size 22 color '#c6ab7d'
                        text h.what font 'fonts/CharisSIL-Regular.ttf' size (36 if persistent.large_text else 30) substitute False

screen about():
    tag menu
    use menu_frame('The Ending We Never Got'):
        viewport:
            mousewheel True draggable True scrollbars 'vertical'
            vbox:
                xsize 1420 spacing 28
                text 'The original timeline' font 'fonts/EBGaramond12-Italic.ttf' size 46 color '#d8c6a6'
                text 'A young woman is taken from home and asked to save a world she never chose.' style 'prose_text'
                text 'Story by dgoldman0. Adapted from Rebuild 11, from the summoning through the complete Bellweir ending.' style 'prose_text'
                text 'In development. This edition contains the complete original story; illustration coverage is still being rebuilt. Look closer and Threads begin with the first night.' size 27 color '#bdb7ab'
                text 'Illustrations use the built-in image-generation tool and local GIMP editing. Engine: Ren’Py 8.5.3. Type: EB Garamond and Charis SIL (SIL Open Font License), Clear Sans (Apache 2.0). Licenses accompany this edition.' size 25 color '#bdb7ab'
                textbutton 'Ren’Py license information' action OpenURL('https://www.renpy.org/doc/html/license.html')

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid('#080f14ed')
    frame:
        xalign 0.5 yalign 0.5 xsize 1050
        background Solid('#172023') padding (60, 50)
        vbox:
            spacing 36
            text message style 'prose_text'
            hbox:
                spacing 30
                textbutton 'Confirm' id 'confirm_yes' action yes_action
                textbutton 'Cancel' id 'confirm_no' action no_action
    key 'game_menu' action no_action

screen notify(message):
    zorder 150
    frame:
        xpos 45 ypos 35 background Solid('#101a21ee') padding (25, 18)
        text message size 24
    timer 3 action Hide('notify')
