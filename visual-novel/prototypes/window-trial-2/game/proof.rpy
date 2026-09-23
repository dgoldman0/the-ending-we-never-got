init python:
    gui.init(1920, 1080)

define config.name = "The Ending We Never Got — An afternoon"
define config.version = "window-trial-2"
define config.save_directory = "tenwg-window-trial-2"
define config.check_conflicting_properties = True
define config.default_text_cps = 0
define config.has_sound = False
define config.has_music = False
define config.has_voice = False
define config.window = "hide"
define config.allow_skipping = False
define config.quit_action = Quit(confirm=False)
define config.enter_transition = Dissolve(.15)
define config.exit_transition = Dissolve(.15)
define _game_menu_screen = "proof_menu"
define build.name = "AnAfternoon"
define build.version = "trial-2"

default persistent.softened = False
default persistent.large_text = False
default composition = "nightglass"
default page_index = 0
default thread_seen = False

init python:
    pages = [
        (218, "window-packing", None, "Tessa sits by a window overlooking the convoy. Iven puts her bag beside her and starts packing a medical chest.", "tessa-question", "iven-listen"),
        (220, "window-packing", "Tessa", "You bought me an afternoon.", "tessa-question", "iven-listen"),
        (223, "window-packing", "Iven", "At least that.", "tessa-listen", "iven-listen"),
        (226, "convoy-mother", None, "Below, the mother who called from the next row in the infirmary approaches the wagons.", None, None),
        (228, "window-packing", "Tessa", "She’s still down there. What am I supposed to tell her?", "tessa-question", "iven-listen"),
        (231, "window-packing", "Iven", "Let me speak to her.", "tessa-listen", "iven-listen"),
        (234, "window-packing", "Tessa", "And tomorrow? They’ll send someone else to ask me.", "tessa-question", "iven-listen"),
        (237, "window-pause", None, "Iven sets the bottle back in the chest, leaving the lid open.", None, None),
        (239, "window-pause", "Iven", "I don’t know how to stop that.", "tessa-listen", "iven-admit"),
        (242, "convoy-guards", None, "Below, Mara assigns two of the soldiers who guarded Tessa’s room to the convoy.", None, None),
        (244, "window-pause", "Tessa", "Are you coming with me?", "tessa-question", "iven-listen"),
        (247, "window-pause", "Iven", "All the way there and back.", "tessa-listen", "iven-listen"),
        (250, "window-together", None, "She makes room on the sill. Iven sits with her, leaving the chest open.", None, None),
    ]

    def art(name):
        return "art/" + ("softened/" if persistent.softened else "") + name + ".png"

    def portrait(name, w, h):
        return Transform(art(name), xysize=(w,h))

    def lighting_toggle():
        persistent.softened = not persistent.softened
        renpy.save_persistent()
        renpy.restart_interaction()

    def remember_thread():
        renpy.store.thread_seen = True
        renpy.retain_after_load()
        renpy.restart_interaction()

    def type_toggle():
        persistent.large_text = not persistent.large_text
        renpy.save_persistent()
        renpy.restart_interaction()

    build.classify("game/ui/**.svg", None)
    build.classify("**/cache/**", None)
    build.classify("**/saves/**", None)
    build.classify("game/review.rpy*", None)
    build.classify("review/**", None)
    build.classify("tests/**", None)
    build.classify("art/**", None)
    build.classify("README.md", None)
    build.classify("*.sh", None)
    build.classify("**/*.log", None)

style default:
    font "fonts/EBGaramond12-Regular.ttf"
    size 42
    color "#eee8dd"

style button:
    padding (12, 8)
    background None
    hover_background "#ffffff10"

style button_text:
    font "fonts/ClearSans-Regular.ttf"
    size 25
    color "#abaeac"
    hover_color "#ffffff"
    selected_color "#e3bb86"
    insensitive_color "#565b5b"

style proof_small:
    font "fonts/ClearSans-Regular.ttf"
    size 22
    color "#a5aaa9"

screen reaction(name, expression, active, x, y, pale=False):
    $ pw, ph = 240, 306
    add Solid("#101c25") pos (x+5,y+95) xysize (230,208)
    add AlphaMask(Transform(art(expression), xysize=(240,320)), "ui/arch-mask.png") pos (x,y)
    add "ui/arch-frame.png" pos (x,y)
    if active:
        add "ui/active.png" pos (x+31,y+313)
    text name pos (x+120,y+330) xanchor .5 size 24 font "fonts/ClearSans-Regular.ttf" color ("#56472f" if pale else ("#edcea0" if active else "#9ba7ad")) kerning 2

screen reading(p):
    modal True
    $ spoken = p[2] is not None
    $ size = 51 if persistent.large_text else 45
    add art(p[1]) xysize (1920,1080)
    button:
        xysize (1920,1080)
        background None
        hover_background None
        action Return(1)
        keyboard_focus False
    if composition == "vellum":
        add "ui/vellum.png"
        if spoken:
            use reaction("Tessa",p[4],p[2]=="Tessa",64,678,True)
            use reaction("Iven",p[5],p[2]=="Iven",1616,678,True)
        text (p[2] if spoken else "") pos (382,862) size 28 color "#745834" kerning 2
        text p[3] pos (382 if spoken else 270,912 if spoken else 882) xmaximum (1156 if spoken else 1380) size size line_spacing 3 color "#302e29"
    else:
        add "ui/nightglass.png"
        if spoken:
            use reaction("Tessa",p[4],p[2]=="Tessa",54,695)
            use reaction("Iven",p[5],p[2]=="Iven",302,695)
        text (p[2] if spoken else "THE INFIRMARY") pos (600 if spoken else 210,846) size (29 if spoken else 22) font "fonts/ClearSans-Regular.ttf" color "#dcc091" kerning 3
        text p[3] pos (600 if spoken else 210,903 if spoken else 896) xmaximum (1140 if spoken else 1460) size size line_spacing 4
    hbox:
        pos (1380,1022)
        spacing 23
        textbutton "Back" id "page_back" text_size 21 action Return(-1) sensitive page_index>0
        textbutton "Passage" text_size 21 action ShowMenu("passage")
        textbutton "Menu" text_size 21 action ShowMenu("proof_menu")
        textbutton "Next  ›" id "page_next" text_size 21 action Return(1)
    if page_index == 12:
        textbutton "Look closer  ◇" id "look_closer" pos (1460,772) text_size 27 action ShowMenu("closer")
    key ["K_SPACE", "K_RETURN", "K_KP_ENTER", "K_RIGHT"] action Return(1)
    key ["K_LEFT", "K_PAGEUP", "rollback"] action Return(-1)
    key "game_menu" action ShowMenu("proof_menu")

screen main_menu():
    tag menu
    add Solid("#172226")
    add Transform(Crop((30,0,1072,941), art("window-together")), xysize=(1230,1080)) pos (690,0)
    add Solid("#172226") xysize (690,1080)
    text "THE ENDING WE NEVER GOT" pos (80,104) style "proof_small" kerning 3
    text "An afternoon" pos (80,365) size 92
    text "Tessa & Iven\nThe infirmary, after the ceremony" pos (85,490) size 33 color "#aeb8b5" line_spacing 7
    text "Click or → to continue · ← to go back" pos (85,970) style "proof_small"
    textbutton "Begin reading   →" id "main_begin" pos (73,675) text_size 34 action Start()
    textbutton ("Lighting · Softened" if persistent.softened else "Lighting · Intense") pos (73,838) action Function(lighting_toggle)
    textbutton ("Type · Larger" if persistent.large_text else "Type · Standard") pos (73,894) action Function(type_toggle)

screen proof_menu():
    tag menu
    modal True
    add Solid("#111c20f8")
    text "An afternoon" pos (250,170) size 74
    vbox:
        pos (250,310)
        spacing 15
        textbutton "Return to reading" id "menu_return" action Return()
        textbutton "Passage" action ShowMenu("passage")
        textbutton "Threads" action ShowMenu("threads")
        textbutton ("Lighting · Softened" if persistent.softened else "Lighting · Intense") id "lighting" action Function(lighting_toggle)
        textbutton ("Type · Larger" if persistent.large_text else "Type · Standard") id "type" action Function(type_toggle)
        textbutton "Save this place" id "proof_save" action QuickSave(message="Place saved")
        textbutton "Load saved place" id "proof_load" action QuickLoad(confirm=False)
        textbutton "Back to title" action MainMenu(confirm=False)
    vbox:
        pos (1100,325)
        spacing 18
        text "COMPOSITION STUDIES" style "proof_small" kerning 2
        textbutton "01 · Nightglass" action SetVariable("composition", "nightglass")
        textbutton "02 · Vellum" action SetVariable("composition", "vellum")
    key "game_menu" action Return()

screen passage():
    tag menu
    add Solid("#172226")
    text "The passage so far" pos (300,95) size 64
    viewport:
        pos (300,215)
        xysize (1320,700)
        mousewheel True
        draggable True
        scrollbars "vertical"
        vbox:
            spacing 26
            for p in pages[:page_index+1]:
                if p[2]:
                    text p[2] style "proof_small" color "#d6ac77"
                text p[3] size 38 xmaximum 1220
    textbutton "Return to reading" pos (288,970) action ShowMenu("proof_menu")

screen finished():
    modal True
    add Solid("#111c20e8")
    text "An afternoon" align (.5,.37) size 88
    text "The end of this passage" align (.5,.48) size 34 color "#aeb8b5"
    textbutton "Read again" align (.5,.62) action Return()
    textbutton "Title" align (.5,.72) action MainMenu(confirm=False)

screen closer():
    tag menu
    modal True
    default connected = False
    add Solid("#172226")
    text "The open chest" pos (192,65) size 68
    if not connected:
        add Transform(Crop((1070,225,600,640), art("window-together")), xysize=(690,736)) pos (615,175)
        textbutton "Follow the thread  →" id "follow_thread" pos (1350,740) action [SetScreenVariable("connected",True), Function(remember_thread)]
    else:
        use chest_connection
    textbutton "Return to reading" id "closer_return" pos (180,985) action Return()
    textbutton ("Softened" if persistent.softened else "Intense") pos (1575,85) action Function(lighting_toggle)
    key "game_menu" action Return()

screen chest_connection():
    add Transform(Crop((955,300,710,639), art("window-packing")), xysize=(678,610)) pos (220,210)
    add Transform(Crop((180,100,900,810), art("window-together")), xysize=(678,610)) pos (990,210)
    text "His hands were busy." pos (220,840) size 36 color "#b9c1bc"
    text "She makes room beside her." pos (990,840) size 36 color "#b9c1bc"
    text "He cannot stop tomorrow’s departure. For this moment, the packing can wait." pos (220,910) size 35 xmaximum 1440

screen threads():
    tag menu
    add Solid("#172226")
    text "Threads" pos (192,65) size 68
    if thread_seen:
        text "The open chest" pos (220,155) style "proof_small" color "#d6ac77"
        use chest_connection
    else:
        text "Connections you follow through Look closer will gather here." pos (220,400) size 42 xmaximum 1280
    textbutton "Return to reading" id "threads_return" pos (180,985) action Return()
    key "game_menu" action Return()

label start:
    $ page_index = 0
    while True:
        if page_index == 0 or pages[page_index][1] != pages[max(0,page_index-1)][1]:
            with Dissolve(.22)
        call screen reading(pages[page_index])
        if _return == -1:
            $ page_index = max(0,page_index-1)
        elif page_index < len(pages)-1:
            $ page_index += 1
        else:
            call screen finished
            $ page_index = 0

screen notify(message):
    zorder 100
    text message align (.5,.1) size 30
    timer 2.0 action Hide("notify")
