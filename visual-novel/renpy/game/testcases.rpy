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

testcase opening_art_states:
    click id 'main_begin'
    click id 'begin_reading'
    click id 'chapter_continue'
    assert eval source_line == 9
    screenshot '13-open-worlds.png'
    advance until eval source_line == 11
    screenshot '14-landing-props.png'
    advance until eval source_line == 15 and source_page == 0
    assert eval scene_art.endswith('chamber-open-spill.png')
    advance until eval source_line == 17
    assert eval scene_art.endswith('chamber-closed.png')
    advance until eval source_line == 54
    assert eval scene_sprites()[0][0] == 'tessa-phone-bright'
    screenshot '15-phone-before-cloak.png'
    advance until eval source_line == 69
    assert eval scene_art.endswith('apartment-closed.png')
    advance until eval source_line == 103
    assert eval scene_sprites()[0][0] == 'tessa-phone-dark'
    advance until eval source_line == 106
    assert eval scene_art.endswith('apartment-closed.png')
    advance until eval source_line == 108
    assert eval scene_art.endswith('apartment-barricaded.png')
    screenshot '16-chair-moved.png'
    advance until eval source_line == 135
    screenshot '17-first-treatment.png'
    advance until eval source_line == 200
    screenshot '18-ceremony.png'
    advance until eval source_line == 244
    screenshot '19-afternoon.png'

testcase save_knowledge_and_rollback:
    click id 'main_begin'
    click id 'begin_reading'
    click id 'chapter_continue'
    advance until eval source_line == 32
    click 'Save'
    click id 'file_slot_5'
    if screen 'confirm':
        click id 'confirm_yes'
    assert eval renpy.can_load('1-5')
    screenshot '20-save-slots.png'
    click id 'menu_return'
    advance until screen 'inquiry_invitation'
    click id 'open_inquiry'
    click id 'evidence_phone'
    assert eval 'phone' in viewed_evidence
    click id 'back_to_material'
    click id 'evidence_promise'
    click id 'back_to_material'
    click id 'evidence_olan'
    click id 'back_to_material'
    click id 'evidence_public_role'
    click id 'back_to_material'
    click id 'compare_evidence'
    click id 'answer_1'
    click 'Save'
    click id 'file_slot_6'
    if screen 'confirm':
        click id 'confirm_yes'
    click 'Load'
    click id 'file_slot_5'
    if screen 'confirm':
        click id 'confirm_yes'
    assert screen 'say'
    assert eval source_line == 32
    assert eval not viewed_evidence and unlocked_round == 0
    click 'Load'
    click id 'file_slot_6'
    if screen 'confirm':
        click id 'confirm_yes'
    assert screen 'inquiry_invitation'
    assert eval 'phone' in viewed_evidence and unlocked_round == 1
    assert eval 'limits' in findings
    click id 'continue_story'
    click id 'chapter_continue'
    advance until eval source_line == 256
    keysym 'rollback'
    assert eval source_line < 256

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

# Traverse the same screenplay with every optional finding, including origin.
testcase investigated_route:
    click id 'main_begin'
    click id 'begin_reading'
    # Actual traversal, not a jump to the ending.
    click id 'chapter_continue'
    advance until screen 'inquiry_invitation'
    click id 'open_inquiry'
    click id 'case_limits'
    click id 'evidence_phone'
    click id 'back_to_material'
    click id 'evidence_promise'
    click id 'back_to_material'
    click id 'evidence_olan'
    click id 'back_to_material'
    click id 'evidence_public_role'
    click id 'back_to_material'
    click id 'compare_evidence'
    click id 'answer_1'
    assert eval 'limits' in findings
    click id 'menu_return'
    assert screen 'inquiry_invitation'
    click id 'continue_story'
    click id 'chapter_continue'
    advance until screen 'chapter_title'
    click id 'chapter_continue'
    advance until screen 'inquiry_invitation'
    click id 'open_inquiry'
    click id 'case_return'
    click id 'evidence_cut_pages'
    click id 'back_to_material'
    click id 'evidence_scholar'
    click id 'back_to_material'
    click id 'evidence_hearing'
    click id 'back_to_material'
    click id 'compare_evidence'
    click id 'answer_0'
    assert eval 'return' in findings
    click id 'case_origin'
    assert eval readable_evidence('origin') == ['h_first']
    assert eval not case_ready('origin')
    click id 'evidence_h_first'
    click id 'back_to_material'
    click id 'menu_return'
    assert screen 'inquiry_invitation'
    click id 'continue_story'
    click id 'chapter_continue'
    advance until screen 'chapter_title'
    click id 'chapter_continue'
    advance until screen 'inquiry_invitation'
    click id 'open_inquiry'
    click id 'case_river'
    click id 'evidence_portrait'
    click id 'back_to_material'
    click id 'evidence_launch'
    click id 'back_to_material'
    click id 'evidence_grain'
    click id 'back_to_material'
    click id 'compare_evidence'
    click id 'answer_2'
    assert eval 'river' in findings
    click id 'case_origin'
    click id 'evidence_h_memory'
    click id 'back_to_material'
    click id 'menu_return'
    assert screen 'inquiry_invitation'
    click id 'continue_story'
    click id 'chapter_continue'
    advance until screen 'chapter_title'
    click id 'chapter_continue'
    advance until screen 'inquiry_invitation'
    click id 'open_inquiry'
    click id 'case_harrow'
    click id 'evidence_inspection'
    click id 'back_to_material'
    click id 'evidence_order'
    click id 'back_to_material'
    click id 'evidence_cargo'
    click id 'back_to_material'
    click id 'evidence_aftermath'
    click id 'back_to_material'
    click id 'compare_evidence'
    click id 'answer_0'
    assert eval 'harrow' in findings
    click id 'case_origin'
    click id 'evidence_h_distrust'
    click id 'back_to_material'
    click id 'menu_return'
    assert screen 'inquiry_invitation'
    click id 'continue_story'
    click id 'chapter_continue'
    advance until screen 'inquiry_invitation'
    click id 'open_inquiry'
    click id 'case_witness'
    click id 'evidence_marren'
    click id 'back_to_material'
    click id 'evidence_plans'
    click id 'back_to_material'
    click id 'evidence_letter'
    click id 'back_to_material'
    click id 'compare_evidence'
    click id 'answer_1'
    assert eval 'witness' in findings
    click id 'case_origin'
    click id 'evidence_h_origin'
    screenshot '21-origin-context.png'
    click id 'back_to_material'
    click id 'compare_evidence'
    screenshot '22-origin-comparison.png'
    click id 'answer_2'
    assert eval 'origin' in findings
    screenshot '23-origin-finding.png'
    click id 'menu_return'
    assert screen 'inquiry_invitation'
    click id 'continue_story'
    click id 'chapter_continue'
    advance until screen 'chapter_title'
    click id 'chapter_continue'
    advance until screen 'ending_breath'
    assert eval completed_scenes == 58
    assert eval len(findings) == 6 and len(viewed_evidence) == 21
    click id 'ending_continue'
    assert screen 'final_question'
    screenshot '24-ending-with-findings.png'
    click id 'ending_title'
    click id 'main_begin'
    assert eval unlocked_round == 0
    assert eval not viewed_evidence
    assert eval not ending_reached

testcase small_window_keyboard:
    $ renpy.set_physical_size((1280, 720))
    pause 0.2
    screenshot '25-small-title.png'
    move pos (1910, 1060)
    keysym 'K_DOWN'
    keysym 'K_RETURN'
    assert screen 'reading_intro'
    click id 'begin_reading'
    click id 'chapter_continue'
    advance until eval source_line == 32
    click 'Settings'
    click 'Larger'
    click 'Image descriptions'
    click 'Reduced motion'
    screenshot '26-small-settings.png'
    keysym 'game_menu'
    assert screen 'say'
    assert eval source_line == 32
    screenshot '27-small-description.png'
    click 'Settings'
    click 'Image descriptions'
    click 'Reduced motion'
    click id 'menu_return'
    $ renpy.set_physical_size((1740, 978))
