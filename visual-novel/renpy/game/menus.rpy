screen main_menu():
    tag menu
    add Solid('#10252b')
    if renpy.loadable('art/backgrounds/apartment-closed.png'):
        add 'art/backgrounds/apartment-closed.png' xysize (1920, 1080)
        add 'art/sprites/tessa-cloaked-dark.png' xpos 915 ypos 40 xysize (930, 1395)
    add Solid('#10252bf5') xsize 830 ysize 1080
    vbox:
        xpos 100 ypos 90 xsize 680 spacing 18
        text 'THE ORIGINAL TIMELINE' style 'caption_text'
        text 'The Ending\nWe Never Got' style 'title_text'
        null height 12
        textbutton 'Begin' id 'main_begin' action Start() xsize 500
        textbutton 'Continue' action Continue() sensitive renpy.can_load('1-1') or renpy.newest_slot() is not None xsize 500
        textbutton 'Load a saved game' action ShowMenu('load') xsize 500
        textbutton 'Settings' action ShowMenu('preferences') xsize 500
        textbutton 'About this edition' action ShowMenu('about') xsize 500
        textbutton 'Quit' action Quit(confirm=True) xsize 500
    text 'A story of home, obligation, and what survives.' xpos 100 ypos 970 size 23 color '#b2c2b9'

screen menu_frame(title):
    add Solid('#101f26')
    add Solid('#1c3339') xpos 0 ypos 0 xsize 340 ysize 1080
    vbox:
        xpos 38 ypos 75 xsize 270 spacing 17
        text 'THE ENDING\nWE NEVER GOT' font 'fonts/CharisSIL-Regular.ttf' size 31
        null height 40
        textbutton 'Return' id 'menu_return' action Return() xfill True
        if not main_menu:
            textbutton 'Save' action ShowMenu('save') xfill True
            textbutton 'History' action ShowMenu('history') xfill True
            textbutton 'Investigate' action ShowMenu('investigation') sensitive unlocked_round > 0 xfill True
        textbutton 'Load' action ShowMenu('load') xfill True
        textbutton 'Settings' action ShowMenu('preferences') xfill True
        textbutton 'About' action ShowMenu('about') xfill True
        if not main_menu:
            textbutton 'Title screen' action MainMenu() xfill True
    text title xpos 410 ypos 64 font 'fonts/CharisSIL-Regular.ttf' size 57
    add Solid('#436061') xpos 410 ypos 151 xsize 1420 ysize 2
    frame:
        background None
        xpos 410 ypos 188 xsize 1420 ysize 820
        padding (0, 0)
        transclude

screen save():
    tag menu
    use file_slots('Save', True)

screen load():
    tag menu
    use file_slots('Load', False)

screen file_slots(title, saving):
    use menu_frame(title):
        vbox:
            spacing 25
            text 'Choose a slot. Saves keep your story position and your investigation together.' size 25 color '#bdcfc6'
            grid 3 2:
                spacing 24
                for slot in range(1, 7):
                    button:
                        id ('file_slot_' + str(slot))
                        xsize 445 ysize 300
                        action (FileSave(slot) if saving else FileLoad(slot))
                        vbox:
                            spacing 6
                            add FileScreenshot(slot) xysize (395, 222)
                            text FileTime(slot, format='%b %d, %H:%M', empty='Empty slot') size 23
            hbox:
                spacing 15
                for page in range(1, 6):
                    textbutton str(page) action FilePage(str(page)) xsize 78
                textbutton 'Auto' action FilePage('auto')

screen preferences():
    tag menu
    use menu_frame('Reading settings'):
        vbox:
            spacing 28 xsize 1300
            text 'Display' style 'caption_text'
            hbox:
                spacing 16
                textbutton 'Window' action Preference('display', 'window')
                textbutton 'Fullscreen' action Preference('display', 'fullscreen')
            text 'Text size' style 'caption_text'
            hbox:
                spacing 16
                textbutton 'Standard' action SetField(persistent, 'large_text', False) selected not persistent.large_text
                textbutton 'Larger' action SetField(persistent, 'large_text', True) selected persistent.large_text
            text 'Text speed  ·  far right shows each line immediately' style 'caption_text'
            bar:
                value Preference('text speed')
                xsize 780 ysize 24
                left_bar Solid('#bdcfbd') right_bar Solid('#35494b')
                thumb Solid('#eee7cd', xsize=24, ysize=30)
            hbox:
                spacing 16
                textbutton 'Reduced motion' action ToggleField(persistent, 'reduced_motion')
                textbutton 'Image descriptions' action ToggleField(persistent, 'art_descriptions')
                textbutton 'Self-voicing' action Preference('self voicing', 'toggle')
            text 'Keyboard: Space / Enter advances; Page Up rolls back; Esc returns or opens the menu. Use the arrow keys to focus controls and Enter to activate them. Press V to toggle self-voicing.' style 'prose_text'
            text 'There are no timed choices, hidden hotspots or flashing effects. Scene brightness is intentional; menus and dialogue stay on opaque dark panels.' color '#aabeba' size 25

screen history():
    tag menu
    use menu_frame('Previously read'):
        viewport:
            mousewheel True draggable True scrollbars 'vertical'
            yinitial 1.0
            vbox:
                spacing 25 xsize 1330
                if not _history_list:
                    text 'Your reading history will appear here.' style 'prose_text'
                for h in _history_list:
                    vbox:
                        spacing 8
                        if h.who:
                            text h.who size 24 color '#d9c699'
                        text h.what font 'fonts/CharisSIL-Regular.ttf' size (36 if persistent.large_text else 30) substitute False

screen about():
    tag menu
    use menu_frame('About this edition'):
        viewport:
            mousewheel True draggable True scrollbars 'vertical'
            vbox:
                xsize 1310 spacing 26
                text 'The Ending We Never Got' style 'title_text' size 48
                text 'Original timeline · first playable edition · [config.version]' color '#d9c699'
                text 'The complete original screenplay, from the summoning to Bellweir, followed by the question to the reader. Optional investigations explore events and history without changing the cast’s knowledge or the original outcome.' style 'prose_text'
                text 'This edition combines illustrated moments with prose scenes. Most scene illustrations, performance, music and sound are still in development. The continuation beyond the final question is not included.' style 'prose_text'
                text 'Story: dgoldman0’s The Ending We Never Got, Rebuild 11. Adaptation and interface developed in this repository. Working illustrations use the built-in image-generation tool, with recorded GIMP edits and visual reviews.' style 'prose_text'
                text 'Engine: Ren’Py 8.5.3. Type: Charis SIL (SIL Open Font License) and Clear Sans (Apache 2.0). Font licenses and notices accompany this edition.' size 27
                textbutton 'Ren’Py license information' action OpenURL('https://www.renpy.org/doc/html/license.html')

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid('#071017e8')
    frame:
        xalign 0.5 yalign 0.5 xsize 1050
        background Solid('#20353b') padding (50, 45)
        vbox:
            spacing 35
            text message style 'prose_text'
            hbox:
                spacing 25
                textbutton 'Confirm' id 'confirm_yes' action yes_action
                textbutton 'Cancel' id 'confirm_no' action no_action
    key 'game_menu' action no_action

screen notify(message):
    zorder 150
    frame:
        xpos 30 ypos 25 background Solid('#172f36') padding (25, 18)
        text message size 25
    timer 3 action Hide('notify')
