# Title, game menu, saves, settings, history and dialogs.
# Menus sit over a blurred, darkened view of the reading position, so the
# story remains present behind them. Navigation is a quiet serif column.

transform title_drift:
    zoom 1.0 xalign 0.62 yalign 0.62
    easein (0.1 if persistent.reduced_motion else 48.0) zoom 1.07

transform candle_flicker:
    alpha 0.72
    block:
        easein 1.3 alpha 0.92
        easeout 0.9 alpha 0.64
        easein 1.7 alpha 0.86
        easeout 1.1 alpha 0.70
        repeat

transform menu_blur:
    blur 26

style nav_button is serif_button:
    padding (0, 5)
style nav_button_text is serif_button_text:
    size 38
    color ui_ivory_soft
    hover_color ui_gold_bright
    selected_color ui_gold_bright

style menu_heading:
    font ui_serif
    size 66
    color ui_ivory

style menu_label:
    font ui_caps
    size 22
    kerning 3.2
    color ui_gold

style menu_body:
    font ui_serif
    size 30
    color ui_ivory_soft
    line_spacing 8

style menu_note:
    font ui_italic
    size 26
    color ui_dim
    line_spacing 6

style reading_bar:
    xsize 480
    ysize 18
    left_bar Solid(ui_gold, ysize=2, yalign=0.5)
    right_bar Solid("#4a4d4e", ysize=2, yalign=0.5)
    thumb Solid(ui_gold_bright, xsize=4, ysize=18)
    thumb_offset 2

style choice_button is caps_button:
    padding (0, 6)
style choice_button_text is caps_button_text:
    size 25
    color ui_ivory_soft
    selected_color ui_gold_bright
    selected_hover_color ui_gold_bright

# ------------------------------------------------------------------ title

screen main_menu():
    tag menu
    # The painting and its candle drift together; the words sit on the dark
    # wall between the window and Tessa, lit from the side by the candle.
    fixed at title_drift:
        xysize (1920, 1080)
        add lighting_art('art/opening/cg/drawing-restart.png') xysize (1920, 1080)
        if not persistent.reduced_motion:
            add "ui/candle-glow.png" at candle_flicker:
                xanchor 0.5 yanchor 0.5 xpos 265 ypos 730 zoom 1.1
    add "ui/title-shade.png" xysize (1920, 1080) alpha 0.35
    vbox:
        xpos 452 ypos 150
        text "the original timeline" style "menu_label"
        null height 22
        text "The Ending\nWe Never Got" font ui_serif size 112 color ui_ivory line_spacing -14
        null height 30
        add "ui/thread-heading.png" xoffset -12
        null height 34
        if renpy.newest_slot() is not None:
            textbutton _("Continue") action Continue() style "serif_button" text_size 50 text_color ui_gold_bright text_hover_color "#fff1cf"
            textbutton _("Begin again") id "main_begin" action Start() style "caps_button" text_size 25
        else:
            textbutton _("Begin") id "main_begin" action Start() style "serif_button" text_size 50 text_color ui_gold_bright text_hover_color "#fff1cf"
        null height 10
        hbox:
            spacing 26
            textbutton _("Load") action ShowMenu('load') style "caps_button" text_size 23
            textbutton _("Settings") action ShowMenu('preferences') style "caps_button" text_size 23
            textbutton _("About") action ShowMenu('about') style "caps_button" text_size 23
            if not renpy.emscripten:
                textbutton _("Quit") action Quit(confirm=True) style "caps_button" text_size 23
    hbox:
        xpos 452 ypos 968 spacing 18
        text "light" style "menu_label" yalign 0.5 color ui_dim
        textbutton _("Intense") id "title_intense" style "caps_button" text_size 21:
            action SetField(persistent, 'intense_lighting', True)
            selected persistent.intense_lighting
        textbutton _("Softened") id "title_softened" style "caps_button" text_size 21:
            action SetField(persistent, 'intense_lighting', False)
            selected not persistent.intense_lighting
    text "A life interrupted." font ui_italic size 30 color ui_ivory_soft xalign 1.0 xoffset -70 ypos 972

# ------------------------------------------------------------- game menu

screen menu_backdrop():
    if main_menu:
        add lighting_art('art/opening/cg/drawing-restart.png') xysize (1920, 1080) at menu_blur
    elif staged_scene():
        fixed at menu_blur:
            use story_stage
    else:
        add page_ground(scene_light()) at menu_blur
    add Solid("#07090bd4")
    add "ui/title-shade.png" xysize (1920, 1080) alpha 0.55

screen menu_frame(title, current=None):
    use menu_backdrop
    text "the ending we never got" style "menu_label" xpos 110 ypos 76 color ui_dim
    vbox:
        style_prefix "nav"
        xpos 110 ypos 190 spacing 4
        textbutton (_("Return to the title") if main_menu else _("Return to reading")):
            id "menu_return"
            action Return()
            text_size 34
            text_color ui_gold
        null height 22
        if not main_menu:
            textbutton _("History") action ShowMenu('history') selected current == 'history'
            textbutton _("Threads") action ShowMenu('threads') selected current == 'threads'
            textbutton _("Save") action ShowMenu('save') selected current == 'save'
        textbutton _("Load") action ShowMenu('load') selected current == 'load'
        textbutton _("Settings") action ShowMenu('preferences') selected current == 'preferences'
        textbutton _("About") action ShowMenu('about') selected current == 'about'
        if not main_menu:
            null height 22
            textbutton _("Title screen") action MainMenu() text_size 30
    text title style "menu_heading" xpos 640 ypos 118
    add "ui/rule-wide.png" xpos 628 ypos 214
    frame:
        background None
        padding (0, 0)
        xpos 640 ypos 262 xsize 1180 ysize 770
        transclude
    key "game_menu" action Return()

# ------------------------------------------------------------------ saves

init python:
    def slot_title(slot):
        chapter = FileJson(slot, 'chapter', empty='', missing='')
        place = FileJson(slot, 'place', empty='', missing='')
        place = typeset(nice_title(place.replace(' · ', ' | ')).replace(' | ', ' · ')) if place else ''
        return chapter, place

screen save():
    tag menu
    use file_slots(_("Save your place"), True)

screen load():
    tag menu
    use file_slots(_("Return to a moment"), False)

screen file_slots(title, saving):
    use menu_frame(title, 'save' if saving else 'load'):
        vbox:
            spacing 26
            grid 3 2:
                spacing 34
                for slot in range(1, 7):
                    $ chapter, place = slot_title(slot)
                    $ used = FileLoadable(slot)
                    button:
                        id ('file_slot_' + str(slot))
                        style "empty"
                        xsize 372
                        hover_background Solid("#cdb07614")
                        action (FileSave(slot) if saving else FileLoad(slot))
                        sensitive (saving or used)
                        vbox:
                            spacing 10
                            fixed:
                                xysize (372, 210)
                                if used:
                                    add FileScreenshot(slot) xysize (372, 210)
                                else:
                                    add Solid("#ffffff08")
                                    text _("An empty place") font ui_italic size 26 color ui_dim align (0.5, 0.5)
                                add Frame("ui/frame-line.png", 6, 6) xysize (372, 210)
                            if used:
                                text (chapter or _("A saved moment")) style "menu_label" size 19
                                if place:
                                    text place font ui_serif size 27 color ui_ivory xmaximum 372
                                text FileTime(slot, format='%b %d · %H:%M', empty='') font ui_italic size 22 color ui_dim
            hbox:
                spacing 18
                for page in range(1, 6):
                    textbutton _ROMAN[page] action FilePage(str(page)) style "choice_button"
                textbutton _("Auto") action FilePage('auto') style "choice_button"
                textbutton _("Quick") action FilePage('quick') style "choice_button"
            if renpy.emscripten:
                text _("Saves stay in this browser. Use the ≡ menu at the top left to export a backup.") style "menu_note"

# --------------------------------------------------------------- settings

screen preferences():
    tag menu
    use menu_frame(_("Settings"), 'preferences'):
        hbox:
            spacing 90
            vbox:
                xsize 540 spacing 12
                text "reading" style "menu_label"
                null height 4
                text _("Text size") style "menu_body"
                hbox:
                    spacing 22
                    textbutton _("Standard") style "choice_button" action SetField(persistent, 'large_text', False) selected not persistent.large_text
                    textbutton _("Larger") style "choice_button" action SetField(persistent, 'large_text', True) selected persistent.large_text
                null height 8
                text _("Text speed") style "menu_body"
                bar value Preference('text speed') style "reading_bar"
                text _("All the way right shows each line at once.") style "menu_note" size 22
                null height 8
                text _("Automatic reading") style "menu_body"
                bar value Preference('auto-forward time') style "reading_bar"
                hbox:
                    spacing 22
                    textbutton _("Off") style "choice_button" action Preference('auto-forward', 'disable') selected not _preferences.afm_enable
                    textbutton _("On") style "choice_button" action Preference('auto-forward', 'enable') selected _preferences.afm_enable
                null height 8
                text _("Skipping") style "menu_body"
                hbox:
                    spacing 22
                    textbutton _("Read text only") style "choice_button" action Preference('skip', 'seen') selected not _preferences.skip_unseen
                    textbutton _("All text") style "choice_button" action Preference('skip', 'all') selected _preferences.skip_unseen
            vbox:
                xsize 540 spacing 12
                text "light" style "menu_label"
                null height 4
                hbox:
                    spacing 22
                    textbutton _("Intense") id "lighting_intense" style "choice_button":
                        action SetField(persistent, 'intense_lighting', True)
                        selected persistent.intense_lighting
                    textbutton _("Softened") id "lighting_softened" style "choice_button":
                        action SetField(persistent, 'intense_lighting', False)
                        selected not persistent.intense_lighting
                text _("Softened reduces glare and opens deep shadow in every scene, portrait and page. Change it at any time.") style "menu_note" size 23
                null height 18
                text "display" style "menu_label"
                hbox:
                    spacing 22
                    textbutton _("Window") style "choice_button" action Preference('display', 'window')
                    textbutton _("Fullscreen") style "choice_button" action Preference('display', 'fullscreen')
                null height 18
                text "access" style "menu_label"
                textbutton _("Reduced motion") style "choice_button" action ToggleField(persistent, 'reduced_motion')
                textbutton _("Image descriptions") style "choice_button" action ToggleField(persistent, 'art_descriptions')
                textbutton _("Self-voicing") style "choice_button" action Preference('self voicing', 'toggle')
                null height 14
                text _("Space, Enter or a click turns the page; Page Up or the wheel goes back; H hides the words; Escape opens this menu.") style "menu_note" size 22

# ---------------------------------------------------------------- history

screen history():
    tag menu
    predict False
    use menu_frame(_("Previously"), 'history'):
        viewport:
            mousewheel True draggable True scrollbars "vertical" yinitial 1.0
            side_xsize 1180
            vbox:
                xsize 1120 spacing 20
                if not _history_list:
                    text _("The story will leave its words here.") style "menu_note"
                for h in _history_list:
                    if h.who:
                        fixed:
                            xsize 1120 yfit True
                            text h.who.lower() font ui_caps size 22 kerning 2.6 color ui_gold xpos 150 xanchor 1.0 ypos 8
                            text plain_initial(h.what) font ui_serif size text_size(31) color ui_ivory xpos 176 xmaximum 940 line_spacing 7 substitute False
                    else:
                        text plain_initial(h.what) font ui_italic size text_size(31) color ui_ivory_soft xpos 176 xmaximum 940 line_spacing 7 substitute False

# ------------------------------------------------------------------ about

screen about():
    tag menu
    use menu_frame(_("About"), 'about'):
        viewport:
            mousewheel True draggable True scrollbars "vertical"
            vbox:
                xsize 1080 spacing 26
                text _("The original timeline") font ui_italic size 44 color ui_gold_bright
                text _("A young woman is taken from home and asked to save a world she never chose.") style "menu_body" size 34
                text _("Story by dgoldman0, adapted from Rebuild 11, from the summoning through the complete Bellweir ending.") style "menu_body"
                text _("In development. The complete original story can be read; its illustrations are still being made, so later scenes are set as pages of text. Look closer and Threads begin on the first night.") style "menu_note"
                text _("Illustrations: image generation with local GIMP editing. Interface drawn in code. Engine: Ren’Py 8.5.3. Type: EB Garamond (SIL Open Font License). Licences accompany this edition.") style "menu_note"
                textbutton _("Ren’Py licence information") style "choice_button" action OpenURL('https://www.renpy.org/doc/html/license.html')

# ---------------------------------------------------------------- dialogs

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid("#05070ae6")
    vbox:
        align (0.5, 0.46) spacing 40 xmaximum 1100
        text message font ui_serif size 42 color ui_ivory text_align 0.5 xalign 0.5
        hbox:
            xalign 0.5 spacing 70
            textbutton _("Confirm") id "confirm_yes" style "caps_button" text_size 26 action yes_action
            textbutton _("Cancel") id "confirm_no" style "caps_button" text_size 26 action no_action
    key "game_menu" action no_action

screen notify(message):
    zorder 150
    text message at ui_fade_in(0.25):
        font ui_caps size 22 kerning 2.6 color ui_gold_bright xpos 72 ypos 44
        outlines [(absolute(3), "#00000050", 0, 0)]
    timer 2.6 action Hide('notify')

screen skip_indicator():
    zorder 100
    text _("skipping read text") font ui_caps size 21 kerning 2.6 color ui_gold xpos 72 ypos 44 at ui_fade_in(0.2)
