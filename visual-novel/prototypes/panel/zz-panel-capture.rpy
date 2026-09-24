# Prototype capture, NOT part of the game: prototypes/panel/sample.py copies
# this in to screenshot the same lines with the current screen and the panels.
testcase panel_current:
    $ _test.timeout = 240.0
    $ _preferences.text_cps = 0
    $ _test.screenshot_directory = 'test-output/panel'
    run Preference('display', 'fullscreen')
    pause 1.0
    click id 'main_begin'
    advance until eval (current_scene, source_line) == (2, 75)
    pause 0.8
    screenshot 'current-s002.png'
    run Jump('s004')
    pause 0.5
    advance until eval (current_scene, source_line) == (4, 211)
    pause 0.8
    screenshot 'current-s004.png'
    run Jump('s008')
    pause 0.5
    advance until eval (current_scene, source_line) == (8, 352)
    pause 0.8
    screenshot 'current-s008.png'
    run Jump('s023')
    pause 0.5
    advance until eval (current_scene, source_line) == (23, 1012)
    pause 0.8
    screenshot 'current-s023.png'

testcase panel_samples:
    $ _test.timeout = 240.0
    $ _preferences.text_cps = 0
    $ _test.screenshot_directory = 'test-output/panel'
    run Preference('display', 'fullscreen')
    pause 1.0
    click id 'main_begin'
    advance until eval (current_scene, source_line) == (2, 75)
    pause 0.8
    $ panel_style = 'lacquer'
    $ renpy.restart_interaction()
    pause 0.6
    screenshot 'lacquer-s002.png'
    $ panel_style = 'vellum'
    $ renpy.restart_interaction()
    pause 0.6
    screenshot 'vellum-s002.png'
    run Jump('s004')
    pause 0.5
    advance until eval (current_scene, source_line) == (4, 211)
    pause 0.8
    $ panel_style = 'lacquer'
    $ renpy.restart_interaction()
    pause 0.6
    screenshot 'lacquer-s004.png'
    $ panel_style = 'vellum'
    $ renpy.restart_interaction()
    pause 0.6
    screenshot 'vellum-s004.png'
    run Jump('s008')
    pause 0.5
    advance until eval (current_scene, source_line) == (8, 352)
    pause 0.8
    $ panel_style = 'lacquer'
    $ renpy.restart_interaction()
    pause 0.6
    screenshot 'lacquer-s008.png'
    $ panel_style = 'vellum'
    $ renpy.restart_interaction()
    pause 0.6
    screenshot 'vellum-s008.png'
    run Jump('s023')
    pause 0.5
    advance until eval (current_scene, source_line) == (23, 1012)
    pause 0.8
    $ panel_style = 'lacquer'
    $ renpy.restart_interaction()
    pause 0.6
    screenshot 'lacquer-s023.png'
    $ panel_style = 'vellum'
    $ renpy.restart_interaction()
    pause 0.6
    screenshot 'vellum-s023.png'
