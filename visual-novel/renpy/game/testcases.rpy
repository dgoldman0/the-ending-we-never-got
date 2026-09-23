# Functional regression only. Captures require separate manual inspection and
# do not clear art, atmosphere, staging, UI beauty or connected-experience gates.
testsuite global:
    before testcase:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 60.0
        $ _test.screenshot_directory = 'test-output'
        $ persistent.large_text = False
        $ persistent.intense_lighting = True
        $ _preferences.text_cps = 0
        if not screen 'main_menu':
            run MainMenu(confirm=False)
    teardown:
        exit

testcase reading_and_discovery:
    assert screen 'main_menu'
    assert eval isinstance(cast, dict) and callable(cast['TESSA'])
    assert eval len(source_map['scenes']) == 58
    assert eval source_map['source_sha256'] == 'e5c4f7b0af53249752d2d747ebfe756bc084c76002040282d8b7cd93253a6c88'
    click id 'main_begin'
    assert screen 'say'
    assert not screen 'nvl'
    assert eval (current_scene, source_line, source_page) == (1, 9, 0)
    assert eval first_line_of_scene() and staged_scene()
    assert eval not available_details() and not inspected_details and not followed_connections
    keysym 'K_SPACE'
    assert eval source_line == 11
    keysym 'K_RETURN'
    assert eval source_line == 13 and not first_line_of_scene()
    move pos (960, 500)
    advance until eval source_line == 32
    assert eval current_rovel_beat()['speaker']['who'] == 'TESSA'
    assert eval current_rovel_beat()['listener']['who'] == 'SENN'
    # The principal pair stays in the room during compact exchanges.
    assert eval current_rovel_beat()['stage']['actors']
    advance until eval source_line == 110
    assert eval not available_inspections() and not closer_here()
    advance until eval source_line == 112
    assert eval current_scene == 2 and closer_here()
    assert eval stage_framing().get('text')
    click id 'look_closer'
    assert screen 'look_closer'
    assert eval inspected_details == {'drawing'} and not followed_connections
    assert id 'bring_alongside'
    click id 'bring_alongside'
    assert eval inspected_details == {'drawing', 'phone'} and followed_connections == {'home'}
    assert not id 'bring_alongside'
    assert eval (current_scene, source_line, source_page, completed_scenes) == (2, 112, 0, 1)
    click id 'menu_return'
    assert screen 'say'
    assert eval (current_scene, source_line, source_page) == (2, 112, 0)
    click 'Threads'
    assert screen 'threads'
    assert id 'thread_home'
    assert not id 'thread_treatment'
    click id 'thread_home'
    assert screen 'look_closer'
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
    assert eval stage_framing().get('lift') == 70
    advance until eval source_line == 15 and source_page == 0
    assert eval current_rovel_beat()['stage_id'] == 'return'
    keysym 'K_SPACE'
    assert eval (source_line, source_page) == (15, 1)
    assert eval current_rovel_beat()['stage_id'] == 'closure'
    keysym 'K_SPACE'
    assert eval (source_line, source_page) == (17, 0)
    advance until eval source_line == 24
    assert eval current_rovel_beat()['speaker']['who'] == 'WOMAN'
    assert eval rovel_face_ready(current_rovel_beat()['speaker'])
    advance until eval source_line == 35
    assert eval current_rovel_beat()['state']['soldiers'] == 'remain-blocking'
    assert eval {'TESSA', 'SENN'} <= set(current_rovel_beat()['present_cast'])
    advance until eval source_line == 54
    assert eval 'MARA' in current_rovel_beat()['present_cast']
    assert eval current_rovel_beat()['stage']['actors']
    assert eval rovel_face_ready(current_rovel_beat()['speaker']) and rovel_face_ready(current_rovel_beat()['listener'])
    advance until eval source_line == 90
    assert eval current_rovel_beat()['state']['candle'] == 'carried-by-tessa'
    advance until eval source_line == 101
    assert eval current_rovel_beat()['wardrobe'] == 'arrival'
    assert eval current_rovel_beat()['state']['cloak'] == 'on-floor'
    advance until eval source_line == 106
    assert eval current_rovel_beat()['cast'] == ['TESSA']
    advance until eval source_line == 108
    assert eval current_rovel_beat()['state']['phone'] == 'dead-on-table'
    advance until eval source_line == 112
    assert eval current_rovel_beat()['state']['right-hand'] == 'healthy'
    advance until eval source_line == 120
    assert eval current_rovel_beat()['state']['corruption'] == 'still-spreading'
    advance until eval source_line == 124
    assert eval current_rovel_beat()['speaker']['who'] == 'PRIEST'
    assert eval rovel_face_ready(current_rovel_beat()['speaker'])
    advance until eval source_line == 143
    assert eval current_rovel_beat()['state']['tessa'] == 'seated'
    advance until eval source_line == 160
    assert eval current_rovel_beat()['state']['right-fingers'] == 'two-missing'
    advance until eval source_line == 172
    assert eval current_rovel_beat()['state']['iven'] == 'at-family'
    assert eval current_rovel_beat()['state']['water'] == 'untouched'
    advance until eval source_line == 176
    assert eval current_rovel_beat()['wardrobe'] == 'formal'
    assert eval current_rovel_beat()['stage_id'] == 'ceremony-mantle'
    advance until eval source_line == 180
    assert eval current_rovel_beat()['speaker']['who'] == 'MESSENGER'
    assert eval current_rovel_beat()['listener']['who'] == 'ORRA'
    assert eval rovel_face_ready(current_rovel_beat()['speaker']) and rovel_face_ready(current_rovel_beat()['listener'])
    advance until eval source_line == 185
    assert eval current_rovel_beat()['state']['olan-applause'] == 'left-hand-on-thigh'
    advance until eval source_line == 198
    assert eval current_rovel_beat()['state']['sleeve-grip'] == 'retained'
    advance until eval source_line == 208
    assert eval not stage_framing()
    advance until eval source_line == 211
    assert eval current_rovel_beat()['speaker']['who'] == 'IVEN'
    assert eval current_rovel_beat()['listener']['who'] == 'TESSA'
    advance until eval source_line == 214
    assert eval current_rovel_beat()['state']['senn'] == 'yields-steps'
    advance until eval source_line == 218
    assert eval {'TESSA', 'IVEN'} <= set(current_rovel_beat()['cast'])
    advance until eval source_line == 242
    assert eval current_rovel_beat()['state']['soldiers'] == 'former-apartment-guards'
    advance until eval source_line == 247
    assert eval current_rovel_beat()['speaker']['who'] == 'IVEN'
    assert eval rovel_face_ready(current_rovel_beat()['speaker']) and rovel_face_ready(current_rovel_beat()['listener'])
    advance until eval source_line == 250
    assert eval current_rovel_beat()['state']['tessa'] == 'makes-room'
    assert eval current_rovel_beat()['state']['chest'] == 'open'
    advance until screen 'chapter_title'
    assert eval current_scene == 6 and completed_scenes == 5
    click id 'chapter_continue'
    assert screen 'nvl'
    assert not screen 'say'
    assert eval current_scene == 6 and current_rovel_beat() is None and not staged_scene()

testcase page_reading:
    # Prose-only scenes read as typeset pages: a fresh page per scene, new pages
    # when full, and rollback/save/load keep the page contents.
    click id 'main_begin'
    run Jump('s006')
    pause 0.5
    assert screen 'chapter_title'
    click id 'chapter_continue'
    assert screen 'nvl'
    assert eval page_scene == 6 and page_index == 0 and len(nvl_list) == 1
    assert eval scene_light() == 'day'
    advance
    advance
    assert eval len(nvl_list) == 3 and page_index == 0
    advance until eval page_index == 1
    assert eval len(nvl_list) == 1
    keysym 'rollback'
    assert eval page_index == 0 and len(nvl_list) > 1
    advance until eval page_index == 1
    click 'Save'
    click id 'file_slot_3'
    if screen 'confirm':
        click id 'confirm_yes'
    click id 'menu_return'
    advance
    advance
    click 'Menu'
    click 'Load'
    click id 'file_slot_3'
    if screen 'confirm':
        click id 'confirm_yes'
    assert screen 'nvl'
    assert eval page_index == 1 and len(nvl_list) == 1
    run Jump('s007')
    pause 0.5
    assert eval scene_light() == 'night' and page_scene == 7 and page_index == 0 and len(nvl_list) == 1
    run Jump('s040')
    pause 0.5
    assert eval is_super_caption(nvl_list[-1][1])
    advance
    # A time caption heads its page; the scene continues beneath it.
    assert eval page_index == 0 and len(nvl_list) == 2

testcase discovery_treatment_and_promise:
    click id 'main_begin'
    advance until eval source_line == 169
    assert eval available_inspections() == ['home']
    assert eval not inspected_details and not followed_connections
    advance until eval source_line == 172
    assert eval available_inspections() == ['home', 'treatment'] and closer_here()
    click id 'look_closer'
    assert screen 'look_closer'
    assert eval inspected_details == {'treatment_blue'} and not followed_connections
    click id 'bring_alongside'
    assert eval followed_connections == {'treatment'}
    assert eval inspected_details == {'treatment_blue', 'treatment_white'}
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
    assert id 'thread_home' and id 'thread_treatment' and id 'thread_promise'
    assert eval followed_connections == {'treatment'}
    click id 'thread_promise'
    assert screen 'look_closer'
    click id 'bring_alongside'
    assert eval followed_connections == {'treatment', 'promise'} and 'applause' in inspected_details
    click id 'open_threads'
    assert screen 'threads'
    click id 'thread_home'
    click id 'bring_alongside'
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
    click id 'bring_alongside'
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
    keysym 'game_menu'
    assert screen 'say'
    assert eval source_line == 112
    keysym 'rollback'
    assert eval source_line == 110 and not available_inspections()
    click 'History'
    assert screen 'history'
    keysym 'game_menu'
    assert screen 'say'
    assert eval source_line == 110

testcase original_ending_without_discovery:
    # All 58 scenes remain traversable without inspecting anything. This tests
    # ordering through the question; the still-missing Yes affordance is not cleared.
    $ _test.timeout = 200.0
    click id 'main_begin'
    advance until screen 'chapter_title' timeout 200.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 200.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 200.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 200.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 200.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 200.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 200.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 200.0
    click id 'chapter_continue'
    advance until screen 'chapter_title' timeout 200.0
    assert eval current_chapter == 10
    click id 'chapter_continue'
    advance until screen 'ending_breath' timeout 200.0
    assert eval current_scene == 58 and completed_scenes == 58
    assert eval _history_list[-1].what == 'Inside, Orren moves a chair to make room. Tessa takes it.'
    assert eval not inspected_details and not followed_connections
    assert eval ending_reached
    assert not screen 'final_question'
    click id 'ending_continue'
    assert screen 'final_question'
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
    screenshot 'large-promise.png'
    advance until eval source_line == 112
    click id 'look_closer'
    assert eval persistent.large_text and inspected_details == {'drawing'}
    click id 'menu_return'
    assert eval source_line == 112 and source_page == 0
    advance until eval source_line == 124
    screenshot 'large-priest.png'
    advance until eval source_line == 187
    screenshot 'large-announcement.png'
    click 'Threads'
    assert id 'thread_promise'
    click id 'menu_return'
    assert eval (current_scene, source_line, source_page) == (4, 187, 0)
    run Jump('s007')
    pause 0.5
    advance
    advance
    screenshot 'large-page.png'
    assert eval persistent.large_text

testcase lighting_preference:
    click id 'title_softened'
    assert eval not persistent.intense_lighting
    click id 'title_intense'
    assert eval persistent.intense_lighting
    click 'Settings'
    click id 'lighting_softened'
    assert eval not persistent.intense_lighting
    click id 'menu_return'
    click id 'main_begin'
    assert eval lighting_art(current_rovel_beat()['stage']['image']).startswith('art/softened/')
    advance until eval source_line == 54
    assert eval all(lighting_art(current_rovel_beat()[role]['image']).startswith('art/softened/rovel/') for role in ('speaker', 'listener'))
    screenshot 'softened-cast.png'
    click 'Menu'
    click id 'lighting_intense'
    click id 'menu_return'
    assert eval source_line == 54 and source_page == 0 and persistent.intense_lighting
    assert eval lighting_art(current_rovel_beat()['speaker']['image']) == current_rovel_beat()['speaker']['image']
    advance until eval source_line == 90
    click 'Menu'
    click id 'lighting_softened'
    click id 'menu_return'
    assert eval source_line == 90 and not persistent.intense_lighting
    screenshot 'softened-doorway.png'
    advance until eval source_line == 112
    click id 'look_closer'
    assert eval all(lighting_art(detail_views[detail]['image']).startswith('art/softened/') for detail in ('drawing', 'phone'))
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
    click 'Menu'
    click id 'lighting_softened'
    click id 'menu_return'
    advance until eval source_line == 176
    assert eval lighting_art(current_rovel_beat()['stage']['image']).startswith('art/softened/rovel/')
    run Jump('s007')
    pause 0.5
    assert eval page_ground(scene_light()) == 'ui/page-night-soft.webp'
