testsuite global:
    before testcase:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 8.0
        $ _test.screenshot_directory = 'test-output'
        if not screen 'main_menu':
            run MainMenu(confirm=False)
    teardown:
        exit

testcase opening_ui:
    assert screen 'main_menu'
    screenshot '01-title.png'
    click id 'main_begin'
    assert screen 'reading_intro'
    click id 'begin_reading'
    click id 'chapter_continue'
    advance until eval source_line == 29
    assert eval art_available()
    screenshot '02-arrival.png'
    advance until eval source_line == 32
    screenshot '03-reading.png'
    click 'Settings'
    click 'Larger'
    screenshot '04-settings.png'
    click id 'menu_return'
    screenshot '05-large-reading.png'
    click 'History'
    screenshot '06-history.png'
    keysym 'game_menu'
    assert screen 'say'
    advance until eval source_line == 78
    assert eval current_scene == 2
    screenshot '12-apartment.png'

testcase first_inquiry:
    click id 'main_begin'
    click id 'begin_reading'
    click id 'chapter_continue'
    advance until screen 'inquiry_invitation'
    assert eval completed_scenes == 5
    assert eval unlocked_round == 1
    assert eval available_cases() == ['limits']
    click id 'open_inquiry'
    screenshot '07-inquiry.png'
    click id 'evidence_phone'
    screenshot '08-evidence.png'
    click id 'back_to_material'
    click id 'evidence_promise'
    click id 'back_to_material'
    click id 'evidence_olan'
    click id 'back_to_material'
    click id 'evidence_public_role'
    click id 'back_to_material'
    click id 'compare_evidence'
    click id 'answer_0'
    assert eval 'limits' not in findings
    screenshot '09-comparison.png'
    click id 'answer_1'
    assert eval 'limits' in findings
    screenshot '10-finding.png'
    click id 'menu_return'
    assert screen 'inquiry_invitation'
    assert eval current_scene == 5

testcase complete_route:
    click id 'main_begin'
    click id 'begin_reading'
    # Actual traversal, not a jump to the ending.
    click id 'chapter_continue'
    advance until screen 'inquiry_invitation'
    click id 'continue_story'
    click id 'chapter_continue'
    advance until screen 'chapter_title'
    click id 'chapter_continue'
    advance until screen 'inquiry_invitation'
    click id 'continue_story'
    click id 'chapter_continue'
    advance until screen 'chapter_title'
    click id 'chapter_continue'
    advance until screen 'inquiry_invitation'
    click id 'continue_story'
    click id 'chapter_continue'
    advance until screen 'chapter_title'
    click id 'chapter_continue'
    advance until screen 'inquiry_invitation'
    click id 'continue_story'
    click id 'chapter_continue'
    advance until screen 'inquiry_invitation'
    click id 'continue_story'
    click id 'chapter_continue'
    advance until screen 'chapter_title'
    click id 'chapter_continue'
    advance until screen 'ending_breath'
    assert eval completed_scenes == 58
    assert eval not findings
    click id 'ending_continue'
    assert screen 'final_question'
    screenshot '11-ending.png'
    click id 'ending_title'
    click id 'main_begin'
    assert eval unlocked_round == 0
    assert eval not viewed_evidence
    assert eval not ending_reached
