testsuite global:
    before testcase:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 12.0
        $ _test.screenshot_directory = 'test-output'
        $ persistent.large_text = False
        if not screen 'main_menu':
            run MainMenu(confirm=False)
    teardown:
        exit

testcase original_reading_and_discovery:
    assert screen 'main_menu'
    screenshot 'v2-title.png'
    click id 'main_begin'
    click id 'begin_reading'
    click id 'chapter_continue'
    assert eval not available_details()
    advance until eval source_line == 32
    screenshot 'v2-bright-exchange.png'
    assert eval not available_details()
    advance until eval source_line == 112
    assert eval current_scene == 2
    assert eval closer_here()
    screenshot 'v2-first-night.png'
    click id 'look_closer'
    assert screen 'look_closer'
    click id 'inspect_drawing'
    assert eval inspected_details == {'drawing'}
    screenshot 'v2-drawing.png'
    click id 'bring_alongside'
    assert eval inspected_details == {'drawing', 'phone'}
    click id 'follow_connection'
    assert eval followed_connections == {'home'}
    assert eval source_line == 112 and source_page == 0 and completed_scenes == 1
    screenshot 'v2-connection.png'
    click id 'menu_return'
    assert screen 'say'
    assert eval source_line == 112 and current_scene == 2
    click 'Threads'
    click id 'thread_home'
    assert screen 'look_closer'
    click id 'menu_return'
    keysym 'rollback'
    assert eval source_line == 110
    assert eval not closer_here()
    assert eval not available_details()

testcase opening_scene_states:
    click id 'main_begin'
    click id 'begin_reading'
    click id 'chapter_continue'
    assert eval opening_ready(opening_shot())
    screenshot 'opening-009-arrival.png'
    advance until eval source_line == 11
    assert eval opening_ready(opening_shot())
    screenshot 'opening-011-milk.png'
    advance until eval source_line == 13
    screenshot 'opening-013-phone.png'
    advance until eval source_line == 15 and source_page == 0
    screenshot 'opening-015-return.png'
    advance until eval source_line == 19
    screenshot 'opening-019-closed.png'
    advance until eval source_line == 24
    screenshot 'opening-024-mother.png'
    advance until eval source_line == 27
    assert eval opening_ready(opening_shot())
    screenshot 'opening-027-release.png'
    advance until eval source_line == 32
    screenshot 'opening-032-raised.png'
    advance until eval source_line == 35
    screenshot 'opening-035-lowered.png'
    advance until eval source_line == 49
    screenshot 'opening-049-refusal.png'
    advance until eval source_line == 52
    assert eval opening_ready(opening_shot())
    screenshot 'opening-052-call.png'
    advance until eval source_line == 54
    screenshot 'opening-054-promise.png'
    advance until eval source_line == 62
    screenshot 'opening-062-mother-message.png'
    advance until eval source_line == 65
    screenshot 'opening-065-cloak.png'
    advance until eval source_line == 69
    assert eval opening_ready(opening_shot())
    screenshot 'opening-069-window.png'
    advance until eval source_line == 81
    assert eval opening_ready(opening_shot())
    screenshot 'opening-081-night-exchange.png'


testcase discovery_save_and_restore:
    click id 'main_begin'
    click id 'begin_reading'
    click id 'chapter_continue'
    advance until eval source_line == 112
    click 'Save'
    click id 'file_slot_5'
    if screen 'confirm':
        click id 'confirm_yes'
    click id 'menu_return'
    click id 'look_closer'
    click id 'inspect_phone'
    click id 'bring_alongside'
    click id 'follow_connection'
    click 'Save'
    click id 'file_slot_6'
    if screen 'confirm':
        click id 'confirm_yes'
    click 'Load'
    click id 'file_slot_5'
    if screen 'confirm':
        click id 'confirm_yes'
    assert screen 'say'
    assert eval source_line == 112
    assert eval not inspected_details and not followed_connections
    click 'Menu'
    click 'Load'
    click id 'file_slot_6'
    if screen 'confirm':
        click id 'confirm_yes'
    assert screen 'say'
    assert eval source_line == 112
    assert eval inspected_details == {'phone', 'drawing'} and followed_connections == {'home'}
    click 'Threads'
    assert id 'thread_home'
    screenshot 'v2-threads-restored.png'
    click id 'menu_return'
    click 'Menu'
    click 'Larger'
    click id 'menu_return'
    screenshot 'v2-larger-reading.png'
    click 'History'
    screenshot 'v2-history.png'
    keysym 'game_menu'
    assert screen 'say'


testcase original_ending_without_discovery:
    click id 'main_begin'
    click id 'begin_reading'
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 50.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 50.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 50.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 50.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 50.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 50.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 50.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 50.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 50.0
    click id 'chapter_continue'
    advance until screen 'ending_breath' timeout 50.0
    assert eval current_scene == 58 and completed_scenes == 58
    assert eval not inspected_details and not followed_connections
    assert eval ending_reached
    assert not screen 'final_question'
    click id 'ending_continue'
    assert screen 'final_question'
    screenshot 'v2-final-question.png'
    click id 'ending_title'
    click id 'main_begin'
    assert eval not ending_reached and not followed_connections
