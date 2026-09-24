# Development-only screen tour for manual visual review. It captures complete
# screens at 1920x1080; it is not a quality gate and is excluded from builds.
testcase ui_tour:
    # S006 and S007 keep their book-page captures for the page layout.
    $ book_pages(6, 7)
    $ _test.timeout = 40.0
    $ _preferences.text_cps = 0
    run Preference('display', 'fullscreen')
    pause 1.0
    $ _test.screenshot_directory = 'test-output/tour'
    screenshot '00-title.png'
    click id 'main_begin'
    pause 1.2
    screenshot '01-s001-arrival.png'
    advance until eval source_line == 22
    pause 1.0
    screenshot '02-s001-narration.png'
    advance until eval source_line == 32
    pause 1.0
    screenshot '03-s001-compact.png'
    advance until eval source_line == 81
    pause 1.0
    screenshot '04-s002-night-compact.png'
    advance until eval source_line == 112
    pause 1.0
    screenshot '05-s002-quiet.png'
    click id 'look_closer'
    pause 2.0
    screenshot '06-look-closer.png'
    click id 'bring_alongside'
    pause 2.0
    screenshot '06b-look-closer-alongside.png'
    click id 'menu_return'
    advance until eval source_line == 124
    pause 1.0
    screenshot '07-s003-priest.png'
    advance until eval source_line == 129
    pause 1.0
    screenshot '07b-s003-compact.png'
    advance until eval source_line == 187
    pause 1.0
    screenshot '08-s004-ceremony.png'
    advance until eval source_line == 228
    pause 1.0
    screenshot '09-s005-window.png'
    keysym 'game_menu'
    pause 0.6
    screenshot '10-settings.png'
    click 'Save'
    pause 0.6
    screenshot '11-save.png'
    click 'History'
    pause 0.6
    screenshot '12-history.png'
    click 'Threads'
    pause 0.6
    screenshot '13-threads.png'
    click id 'menu_return'
    advance until eval current_scene == 6
    pause 1.2
    screenshot '14-chapter-card.png'
    click id 'chapter_continue'
    pause 1.2
    screenshot '15-s006-page-first.png'
    advance until eval page_index == 1
    pause 1.2
    screenshot '16-s006-page-next.png'
    run Jump('s007')
    pause 1.0
    advance
    advance
    advance
    pause 1.2
    screenshot '17-s007-night-page.png'
    run Jump('s022')
    pause 1.0
    advance
    advance
    pause 1.2
    screenshot '18-s022-dusk-page.png'
    run Jump('s040')
    pause 1.2
    screenshot '19-s040-super.png'
    run Jump('original_ending')
    pause 3.2
    screenshot '20-ending-breath.png'
    click id 'ending_continue'
    pause 5.5
    screenshot '21-final-question.png'

testcase ui_tour_states:
    $ _test.timeout = 60.0
    $ _preferences.text_cps = 0
    run Preference('display', 'fullscreen')
    pause 1.0
    $ _test.screenshot_directory = 'test-output/tour'
    $ persistent.intense_lighting = False
    click id 'main_begin'
    advance until eval source_line == 32
    pause 1.0
    screenshot 's1-softened-compact.png'
    advance until eval source_line == 81
    pause 1.0
    screenshot 's2-softened-night.png'
    advance until eval source_line == 112
    click id 'look_closer'
    pause 2.2
    screenshot 's3-softened-closer.png'
    click id 'bring_alongside'
    pause 2.0
    screenshot 's4-softened-alongside.png'
    click id 'menu_return'
    $ persistent.intense_lighting = True
    $ persistent.large_text = True
    advance until eval source_line == 172
    click id 'look_closer'
    pause 2.2
    screenshot 's5-large-treatment-closer.png'
    click id 'bring_alongside'
    pause 2.0
    screenshot 's6-large-treatment-alongside.png'
    click id 'menu_return'
    advance until eval source_line == 203
    pause 1.0
    screenshot 's7-large-longline.png'
    run Jump('s016')
    pause 1.0
    advance repeat 6
    pause 1.0
    screenshot 's8-large-page.png'
    $ persistent.large_text = False
    keysym 'K_TAB'
    keysym 'K_TAB'
    pause 0.4
    screenshot 's9-keyboard-focus.png'
    keysym 'h'
    pause 0.6
    screenshot 's10-hidden.png'

testcase ui_tour_light:
    # The light registers, rendered frames and book pages (both modes).
    $ _test.timeout = 90.0
    $ _preferences.text_cps = 0
    $ _test.screenshot_directory = 'test-output/tour-light'
    run Preference('display', 'fullscreen')
    pause 1.0
    click id 'main_begin'
    advance until eval source_line == 32
    pause 1.2
    screenshot 'bright-intense.png'
    $ persistent.intense_lighting = False
    pause 1.0
    screenshot 'bright-softened.png'
    $ persistent.intense_lighting = True
    advance until eval source_line == 81
    pause 1.2
    screenshot 'night-intense.png'
    $ persistent.intense_lighting = False
    pause 1.0
    screenshot 'night-softened.png'
    $ persistent.intense_lighting = True
    advance until eval source_line == 112
    click id 'look_closer'
    click id 'bring_alongside'
    pause 2.2
    screenshot 'closer-night.png'
    click id 'menu_return'
    advance until eval source_line == 124
    pause 1.2
    screenshot 'ordinary-ward.png'
    advance until eval source_line == 228
    pause 1.2
    screenshot 'ordinary-window.png'
    run Jump('s006')
    pause 0.5
    click id 'chapter_continue'
    pause 1.2
    screenshot 'page-day-initial.png'
    run Jump('s010')
    pause 1.0
    advance until eval scene_speaker == 'VALCAIR'
    pause 1.2
    screenshot 'page-night-valcair.png'
    run Jump('s019')
    pause 1.0
    advance until eval scene_speaker == 'TESSA'
    pause 1.2
    screenshot 'page-day-lucan.png'
