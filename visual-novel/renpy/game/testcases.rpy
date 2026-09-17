# Functional regression only. Captures require separate manual inspection and
# do not clear art, atmosphere, staging, UI beauty or connected-experience gates.
testsuite global:
    before testcase:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 12.0
        $ _test.screenshot_directory = 'test-output'
        $ persistent.large_text = False
        $ persistent.intense_lighting = True
        if not screen 'main_menu':
            run MainMenu(confirm=False)
    teardown:
        exit

testcase original_reading_and_discovery:
    assert screen 'main_menu'
    assert eval isinstance(cast, dict) and callable(cast['TESSA'])
    assert eval len(source_map['scenes']) == 58
    assert eval source_map['source_sha256'] == 'e5c4f7b0af53249752d2d747ebfe756bc084c76002040282d8b7cd93253a6c88'
    screenshot 'rovel-title.png'
    click id 'main_begin'
    assert screen 'say'
    assert not screen 'reading_intro'
    assert not screen 'chapter_title'
    assert eval (current_scene, source_line, source_page) == (1, 9, 0)
    assert eval not available_details() and not inspected_details and not followed_connections
    click id 'reading_continue'
    assert eval source_line == 11
    # Use a real reading key while Continue keeps pointer focus. The runner's
    # abstract `advance` queues only a focus-dependent `dismiss` event.
    keysym 'K_SPACE'
    assert eval source_line == 13
    move pos (960, 500)
    advance until eval source_line == 32
    assert eval current_rovel_beat()['speaker']['who'] == 'TESSA'
    assert eval current_rovel_beat()['listener']['who'] == 'SENN'
    screenshot 'rovel-bright-exchange.png'
    advance until eval source_line == 110
    assert eval not available_inspections()
    advance until eval source_line == 112
    assert eval current_scene == 2 and closer_here()
    screenshot 'rovel-first-night.png'
    click id 'look_closer'
    assert screen 'look_closer'
    assert eval inspected_details == {'drawing', 'phone'}
    assert eval followed_connections == {'home'}
    assert id 'thread_home'
    assert not id 'thread_treatment'
    assert not id 'thread_promise'
    assert not id 'bring_alongside'
    assert not id 'follow_connection'
    assert eval (current_scene, source_line, source_page, completed_scenes) == (2, 112, 0, 1)
    screenshot 'rovel-home-comparison.png'
    click id 'menu_return'
    assert screen 'say'
    assert eval (current_scene, source_line, source_page) == (2, 112, 0)
    click 'Threads'
    assert screen 'threads'
    click id 'thread_home'
    assert screen 'threads'
    keysym 'game_menu'
    assert screen 'say'
    assert eval (current_scene, source_line, source_page) == (2, 112, 0)
    keysym 'rollback'
    assert eval source_line == 110 and current_scene == 2
    assert eval not closer_here() and not available_details()

testcase opening_scene_states:
    # This test must fail until all required stage, portrait and lighting files
    # exist. A descriptor or room plate alone is not performance coverage.
    assert eval not rovel_missing_assets()
    click id 'main_begin'
    assert eval current_rovel_beat()['stage_id'] == 'arrival'
    screenshot 'rovel-009-arrival.png'
    advance until eval source_line == 15 and source_page == 0
    assert eval current_rovel_beat()['stage_id'] == 'return'
    screenshot 'rovel-015-return.png'
    click id 'reading_continue'
    assert eval (source_line, source_page) == (15, 1)
    assert eval current_rovel_beat()['stage_id'] == 'closure'
    screenshot 'rovel-015-closure.png'
    keysym 'K_SPACE'
    assert eval (source_line, source_page) == (17, 0)
    move pos (960, 500)
    advance until eval source_line == 24
    assert eval current_rovel_beat()['speaker']['who'] == 'WOMAN'
    assert eval rovel_face_ready(current_rovel_beat()['speaker'])
    advance until eval source_line == 35
    assert eval current_rovel_beat()['state']['soldiers'] == 'remain-blocking'
    assert eval {'TESSA', 'SENN'} <= set(current_rovel_beat()['present_cast'])
    advance until eval source_line == 54
    assert eval 'MARA' in current_rovel_beat()['present_cast']
    assert eval not current_rovel_beat()['stage']['actors']
    assert eval rovel_face_ready(current_rovel_beat()['speaker']) and rovel_face_ready(current_rovel_beat()['listener'])
    screenshot 'rovel-054-promise.png'
    advance until eval source_line == 90
    assert eval current_rovel_beat()['state']['candle'] == 'carried-by-tessa'
    screenshot 'rovel-090-blocked-door.png'
    advance until eval source_line == 101
    assert eval current_rovel_beat()['wardrobe'] == 'arrival'
    assert eval current_rovel_beat()['state']['cloak'] == 'on-floor'
    advance until eval source_line == 106
    assert eval current_rovel_beat()['cast'] == ['TESSA']
    advance until eval source_line == 108
    assert eval current_rovel_beat()['state']['phone'] == 'dead-on-table'
    advance until eval source_line == 112
    assert eval current_rovel_beat()['state']['right-hand'] == 'healthy'
    screenshot 'rovel-112-drawing.png'
    advance until eval source_line == 120
    assert eval current_rovel_beat()['state']['corruption'] == 'still-spreading'
    advance until eval source_line == 124
    assert eval current_rovel_beat()['speaker']['who'] == 'PRIEST'
    assert eval rovel_face_ready(current_rovel_beat()['speaker'])
    advance until eval source_line == 143
    assert eval current_rovel_beat()['state']['tessa'] == 'seated'
    screenshot 'rovel-143-purification.png'
    advance until eval source_line == 160
    assert eval current_rovel_beat()['state']['right-fingers'] == 'two-missing'
    screenshot 'rovel-160-hand.png'
    advance until eval source_line == 172
    assert eval current_rovel_beat()['state']['iven'] == 'at-family'
    assert eval current_rovel_beat()['state']['water'] == 'untouched'
    advance until eval source_line == 176
    assert eval current_rovel_beat()['wardrobe'] == 'formal'
    assert eval current_rovel_beat()['stage_id'] == 'ceremony-mantle'
    screenshot 'rovel-176-ceremony.png'
    advance until eval source_line == 180
    assert eval current_rovel_beat()['speaker']['who'] == 'MESSENGER'
    assert eval current_rovel_beat()['listener']['who'] == 'ORRA'
    assert eval rovel_face_ready(current_rovel_beat()['speaker']) and rovel_face_ready(current_rovel_beat()['listener'])
    screenshot 'rovel-180-messenger.png'
    advance until eval source_line == 185
    assert eval current_rovel_beat()['state']['olan-applause'] == 'left-hand-on-thigh'
    advance until eval source_line == 198
    assert eval current_rovel_beat()['state']['sleeve-grip'] == 'retained'
    screenshot 'rovel-198-refusal.png'
    advance until eval source_line == 211
    assert eval current_rovel_beat()['speaker']['who'] == 'IVEN'
    assert eval current_rovel_beat()['listener']['who'] == 'TESSA'
    advance until eval source_line == 214
    assert eval current_rovel_beat()['state']['senn'] == 'yields-steps'
    advance until eval source_line == 218
    assert eval {'TESSA', 'IVEN'} <= set(current_rovel_beat()['cast'])
    screenshot 'rovel-218-window.png'
    advance until eval source_line == 242
    assert eval current_rovel_beat()['state']['soldiers'] == 'former-apartment-guards'
    advance until eval source_line == 247
    assert eval current_rovel_beat()['speaker']['who'] == 'IVEN'
    assert eval rovel_face_ready(current_rovel_beat()['speaker']) and rovel_face_ready(current_rovel_beat()['listener'])
    advance until eval source_line == 250
    assert eval current_rovel_beat()['state']['tessa'] == 'makes-room'
    assert eval current_rovel_beat()['state']['chest'] == 'open'
    screenshot 'rovel-250-together.png'
    advance until screen 'chapter_title'
    assert eval current_scene == 6 and completed_scenes == 5
    click id 'chapter_continue'
    assert screen 'say'
    assert eval current_scene == 6 and current_rovel_beat() is None

testcase discovery_treatment_and_promise:
    click id 'main_begin'
    advance until eval source_line == 169
    assert eval available_inspections() == ['home']
    assert eval not inspected_details and not followed_connections
    advance until eval source_line == 172
    assert eval available_inspections() == ['home', 'treatment'] and closer_here()
    click id 'look_closer'
    assert screen 'look_closer'
    assert eval followed_connections == {'treatment'}
    assert eval inspected_details == {'treatment_blue', 'treatment_white'}
    assert id 'thread_treatment'
    assert not id 'thread_promise'
    screenshot 'rovel-treatment-comparison.png'
    keysym 'game_menu'
    assert screen 'say'
    assert eval (current_scene, source_line, source_page, completed_scenes) == (3, 172, 0, 2)
    advance until eval source_line == 185
    assert eval 'promise' not in available_inspections()
    advance until eval source_line == 187
    assert eval available_inspections() == ['home', 'treatment', 'promise']
    assert eval not closer_here()
    click 'Threads'
    assert screen 'threads'
    assert eval followed_connections == {'treatment', 'promise'}
    assert eval 'applause' in inspected_details and 'home' not in followed_connections
    click id 'thread_treatment'
    assert id 'follow_public_promise'
    click id 'follow_public_promise'
    assert not id 'follow_public_promise'
    screenshot 'rovel-public-promise.png'
    click id 'thread_home'
    assert eval followed_connections == {'home', 'treatment', 'promise'}
    click id 'menu_return'
    assert screen 'say'
    assert eval (current_scene, source_line, source_page) == (4, 187, 0)
    keysym 'rollback'
    assert eval source_line == 185 and 'promise' not in available_inspections()
    advance until eval source_line == 250
    assert eval closer_here()
    click id 'look_closer'
    assert screen 'look_closer'
    assert id 'thread_promise'
    click id 'menu_return'
    assert eval (current_scene, source_line, source_page) == (5, 250, 0)

testcase discovery_save_and_restore:
    click id 'main_begin'
    advance until eval source_line == 112
    click 'Save'
    click id 'file_slot_5'
    if screen 'confirm':
        click id 'confirm_yes'
    click id 'menu_return'
    click id 'look_closer'
    assert eval followed_connections == {'home'}
    click id 'menu_return'
    click 'Save'
    click id 'file_slot_6'
    if screen 'confirm':
        click id 'confirm_yes'
    click 'Settings'
    click 'Larger'
    click id 'lighting_softened'
    click 'Load'
    click id 'file_slot_5'
    if screen 'confirm':
        click id 'confirm_yes'
    assert screen 'say'
    assert eval (current_scene, source_line, source_page) == (2, 112, 0)
    assert eval not inspected_details and not followed_connections
    assert eval persistent.large_text and not persistent.intense_lighting
    click 'Menu'
    click 'Load'
    click id 'file_slot_6'
    if screen 'confirm':
        click id 'confirm_yes'
    assert screen 'say'
    assert eval (current_scene, source_line, source_page) == (2, 112, 0)
    assert eval inspected_details == {'phone', 'drawing'} and followed_connections == {'home'}
    assert eval persistent.large_text and not persistent.intense_lighting
    click 'Threads'
    assert screen 'threads'
    assert id 'thread_home'
    screenshot 'rovel-threads-restored.png'
    keysym 'game_menu'
    assert screen 'say'
    assert eval source_line == 112
    keysym 'rollback'
    assert eval source_line == 110 and not available_inspections()
    assert eval persistent.large_text and not persistent.intense_lighting
    click 'History'
    screenshot 'rovel-history.png'
    keysym 'game_menu'
    assert screen 'say'
    assert eval source_line == 110

testcase original_ending_without_discovery:
    # All 58 scenes remain traversable without inspecting anything. This tests
    # ordering through the question; the still-missing Yes affordance is not cleared.
    click id 'main_begin'
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
    assert eval current_chapter == 10
    click id 'chapter_continue'
    advance until screen 'ending_breath' timeout 50.0
    assert eval current_scene == 58 and completed_scenes == 58
    assert eval _history_list[-1].what == 'Inside, Orren moves a chair to make room. Tessa takes it.'
    assert eval not inspected_details and not followed_connections
    assert eval ending_reached
    assert not screen 'final_question'
    click id 'ending_continue'
    assert screen 'final_question'
    screenshot 'rovel-final-question.png'
    click id 'ending_title'
    click id 'main_begin'
    assert screen 'say'
    assert eval (current_scene, source_line, source_page) == (1, 9, 0)
    assert eval not ending_reached and not followed_connections and not inspected_details

testcase opening_large_text:
    click 'Settings'
    click 'Larger'
    click id 'menu_return'
    click id 'main_begin'
    assert eval persistent.large_text
    advance until eval source_line == 54
    screenshot 'rovel-large-promise.png'
    advance until eval source_line == 92
    screenshot 'rovel-large-doorway.png'
    advance until eval source_line == 101
    screenshot 'rovel-large-cloak.png'
    advance until eval source_line == 112
    click id 'look_closer'
    assert eval persistent.large_text and followed_connections == {'home'}
    screenshot 'rovel-large-home.png'
    click id 'menu_return'
    assert eval source_line == 112 and source_page == 0
    advance until eval source_line == 124
    screenshot 'rovel-large-priest.png'
    advance until eval source_line == 140
    screenshot 'rovel-large-olan.png'
    advance until eval source_line == 164
    screenshot 'rovel-large-mother.png'
    advance until eval source_line == 172
    click id 'look_closer'
    screenshot 'rovel-large-treatment.png'
    click id 'menu_return'
    advance until eval source_line == 187
    screenshot 'rovel-large-announcement.png'
    click 'Threads'
    assert id 'thread_promise'
    screenshot 'rovel-large-public-promise.png'
    click id 'menu_return'
    assert eval (current_scene, source_line, source_page) == (4, 187, 0)
    advance until eval source_line == 250
    screenshot 'rovel-large-window.png'
    assert eval persistent.large_text

testcase lighting_preference:
    click 'Settings'
    assert eval persistent.intense_lighting
    click id 'lighting_softened'
    assert eval not persistent.intense_lighting
    screenshot 'rovel-settings-softened.png'
    click id 'menu_return'
    screenshot 'rovel-title-softened.png'
    click id 'main_begin'
    assert eval lighting_art(current_rovel_beat()['stage']['image']).startswith('art/softened/')
    screenshot 'rovel-arrival-softened.png'
    advance until eval source_line == 54
    assert eval all(lighting_art(current_rovel_beat()[role]['image']).startswith('art/softened/rovel/') for role in ('speaker', 'listener'))
    screenshot 'rovel-cast-softened.png'
    click 'Menu'
    click id 'lighting_intense'
    click id 'menu_return'
    assert eval source_line == 54 and source_page == 0 and persistent.intense_lighting
    assert eval lighting_art(current_rovel_beat()['speaker']['image']) == current_rovel_beat()['speaker']['image']
    screenshot 'rovel-cast-intense.png'
    advance until eval source_line == 90
    screenshot 'rovel-doorway-intense.png'
    click 'Menu'
    click id 'lighting_softened'
    click id 'menu_return'
    assert eval source_line == 90 and not persistent.intense_lighting
    screenshot 'rovel-doorway-softened.png'
    advance until eval source_line == 112
    click id 'look_closer'
    assert eval all(lighting_art(detail_views[detail]['image']).startswith('art/softened/') for detail in ('drawing', 'phone'))
    screenshot 'rovel-home-softened.png'
    click id 'menu_return'
    click 'Save'
    click id 'file_slot_4'
    if screen 'confirm':
        click id 'confirm_yes'
    click 'Settings'
    click id 'lighting_intense'
    click 'Load'
    click id 'file_slot_4'
    if screen 'confirm':
        click id 'confirm_yes'
    assert screen 'say'
    assert eval source_line == 112 and persistent.intense_lighting
    assert eval followed_connections == {'home'}
    click 'Menu'
    click id 'lighting_softened'
    click id 'menu_return'
    advance until eval source_line == 172
    click id 'look_closer'
    assert eval all(lighting_art(detail_views[detail]['image']).startswith('art/softened/rovel/') for detail in ('treatment_blue', 'treatment_white'))
    screenshot 'rovel-treatment-softened.png'
    click id 'menu_return'
    advance until eval source_line == 176
    assert eval lighting_art(current_rovel_beat()['stage']['image']).startswith('art/softened/rovel/')
    screenshot 'rovel-ceremony-softened.png'
    advance until eval source_line == 250
    assert eval lighting_art(current_rovel_beat()['stage']['image']).startswith('art/softened/rovel/')
    click id 'look_closer'
    assert eval lighting_art(detail_views['applause']['image']).startswith('art/softened/rovel/')
    screenshot 'rovel-public-promise-softened.png'
    click id 'menu_return'
    assert eval (current_scene, source_line, source_page) == (5, 250, 0)
