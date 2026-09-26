# Functional regression only. Captures require separate manual inspection and
# do not clear art, atmosphere, staging, UI beauty or connected-experience gates.
init python:
    _held_stages = {}

    def book_pages(*scenes):
        """Read these scenes as typeset book pages whatever paintings exist,
        so the page tests keep working as scene art arrives."""
        for number in scenes:
            key = str(number)
            _held_stages.setdefault(key, STAGING[key]['stages'])
            STAGING[key]['stages'] = []

    def restore_stages():
        for key, stages in _held_stages.items():
            STAGING[key]['stages'] = stages
        _held_stages.clear()

testsuite global:
    before testcase:
        $ restore_stages()
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 60.0
        $ _test.screenshot_directory = 'test-output'
        $ persistent.large_text = False
        $ _preferences.text_cps = 0
        # Captures are 1920x1080 in the 1920x1080 virtual display.
        if eval not _preferences.fullscreen:
            run Preference('display', 'fullscreen')
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
    # Hiding the words (H) leaves the painting: the stage lives on the image layer.
    keysym 'h'
    assert eval renpy.get_screen('story_stage', layer='master') is not None
    assert not screen 'say'
    keysym 'h'
    assert screen 'say'
    advance until eval source_line == 110
    assert eval not available_inspections() and not closer_here()
    advance until eval source_line == 112
    assert eval current_scene == 2 and closer_here()
    assert eval stage_framing().get('text')
    click id 'reading_controls'
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
    click id 'reading_controls'
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
    # S006 now opens on its painting, staged from staging.json, not the opening's beat plan.
    assert screen 'say'
    assert not screen 'nvl'
    assert eval current_scene == 6 and current_rovel_beat() is None and staged_scene()

testcase page_reading:
    # Prose-only scenes read as typeset pages: a fresh page per scene, new pages
    # when full, and rollback/save/load keep the page contents.
    $ book_pages(6, 7, 40)
    click id 'main_begin'
    run Jump('s006')
    pause 0.5
    assert screen 'chapter_title'
    click id 'chapter_continue'
    assert screen 'nvl'
    assert eval page_scene == 6 and page_index == 0 and len(nvl_list) == 1
    assert eval scene_light() == 'day'
    keysym 'h'
    assert eval renpy.get_screen('story_stage', layer='master') is not None
    assert not screen 'nvl'
    keysym 'h'
    assert screen 'nvl'
    advance
    advance
    assert eval len(nvl_list) == 3 and page_index == 0
    advance until eval page_index == 1
    assert eval len(nvl_list) == 1
    keysym 'rollback'
    assert eval page_index == 0 and len(nvl_list) > 1
    advance until eval page_index == 1
    click id 'reading_controls'
    click 'Save'
    click id 'file_slot_3'
    if screen 'confirm':
        click id 'confirm_yes'
    click id 'menu_return'
    advance
    advance
    click id 'reading_controls'
    click id 'open_menu'
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
    click id 'reading_controls'
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
    click id 'reading_controls'
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
    click id 'reading_controls'
    click id 'look_closer'
    assert screen 'look_closer'
    click id 'menu_return'
    assert eval (current_scene, source_line, source_page) == (5, 250, 0)

testcase discovery_save_and_restore:
    click id 'main_begin'
    advance until eval source_line == 112
    click id 'reading_controls'
    click 'Save'
    click id 'file_slot_5'
    if screen 'confirm':
        click id 'confirm_yes'
    click id 'menu_return'
    click id 'reading_controls'
    click id 'look_closer'
    click id 'bring_alongside'
    assert eval followed_connections == {'home'}
    click id 'menu_return'
    click id 'reading_controls'
    click 'Save'
    click id 'file_slot_6'
    if screen 'confirm':
        click id 'confirm_yes'
    click 'Settings'
    click 'Larger'
    click 'Load'
    click id 'file_slot_5'
    if screen 'confirm':
        click id 'confirm_yes'
    assert screen 'say'
    assert eval (current_scene, source_line, source_page) == (2, 112, 0)
    assert eval not inspected_details and not followed_connections
    assert eval persistent.large_text
    click id 'reading_controls'
    click id 'open_menu'
    click 'Load'
    click id 'file_slot_6'
    if screen 'confirm':
        click id 'confirm_yes'
    assert screen 'say'
    assert eval (current_scene, source_line, source_page) == (2, 112, 0)
    assert eval inspected_details == {'phone', 'drawing'} and followed_connections == {'home'}
    assert eval persistent.large_text
    click id 'reading_controls'
    click 'Threads'
    assert screen 'threads'
    assert id 'thread_home'
    keysym 'game_menu'
    assert screen 'say'
    assert eval source_line == 112
    keysym 'rollback'
    assert eval source_line == 110 and not available_inspections()
    click id 'reading_controls'
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
    click id 'reading_controls'
    click id 'look_closer'
    assert eval persistent.large_text and inspected_details == {'drawing'}
    click id 'menu_return'
    assert eval source_line == 112 and source_page == 0
    advance until eval source_line == 124
    screenshot 'large-priest.png'
    advance until eval source_line == 187
    screenshot 'large-announcement.png'
    click id 'reading_controls'
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

testcase original_timeline_light:
    # The original timeline has one light mode, 'original', and no lighting
    # setting (user decision, 24 September 2026). The old title and Settings
    # buttons (then named Intense and Softened) are gone.
    assert not id 'title_intense'
    assert not id 'title_softened'
    click 'Settings'
    assert not id 'lighting_intense'
    assert not id 'lighting_softened'
    click id 'menu_return'
    click id 'main_begin'
    assert eval light_mode() == 'original'
    assert eval stage_image().endswith('-original.webp') and current_register() == 'bright'
    advance until eval source_line == 54
    assert eval all(portrait_source(current_rovel_beat()[role]['image'], role).endswith('-bright-original.webp') for role in ('speaker', 'listener'))
    # The painted portraits replace the old heads, named for the role.
    assert eval painted_portrait_name(current_rovel_beat()['speaker']['image'], 'speaker') == 'senn-assuring-speaking'
    assert eval painted_portrait_name(current_rovel_beat()['listener']['image'], 'listener') == 'tessa-startled-arrival-listening'
    screenshot 'original-light-cast.png'
    advance until eval source_line == 112
    click id 'reading_controls'
    click id 'look_closer'
    assert eval all(lighting_art(detail_views[detail]['image']).endswith('-original.webp') for detail in ('drawing', 'phone'))
    click id 'menu_return'
    advance until eval source_line == 176
    assert eval stage_image().endswith('-original.webp')
    run Jump('s007')
    pause 0.5
    assert eval page_ground(scene_light()) == 'ui/page-night.webp'

testcase skipping_stops_when_unfocused:
    # Leaving the window (Alt+Tab) must not let skipping run on, and Tab no
    # longer toggles skipping.
    click id 'main_begin'
    assert eval not config.keymap['toggle_skip']
    $ renpy.config.skipping = 'fast'
    $ renpy.display.interface.keyboard_focused = False
    pause 0.3
    assert eval not renpy.config.skipping
    $ renpy.display.interface.keyboard_focused = True

testcase staging_pipeline:
    # Art placed at a planned path turns a page scene into an illustrated one,
    # with portraits resolved from the scene's cast and the default listener.
    $ book_pages(6)
    click id 'main_begin'
    $ _planned_stages = list(STAGING['6']['stages'])
    run Jump('s006')
    pause 0.5
    click id 'chapter_continue'
    assert screen 'nvl'
    assert eval not staged_scene()
    $ STAGING['6']['stages'] = [{'image': 'art/rovel/cg/convoy-guards.png', 'from': 0, 'alt': 'Test stage.'}]
    advance
    assert screen 'say'
    assert not screen 'nvl'
    assert eval staged_scene() and stage_image() == 'art/rovel/cg/convoy-guards.png'
    assert eval current_art_description() == 'Test stage.'
    # Her line opens the scene's dialogue, so the listener is Mara, who answers it.
    advance until eval scene_speaker == 'TESSA'
    assert eval stage_faces('Tessa')[1]['who'] == 'MARA'
    assert eval stage_faces('Tessa')[0]['image'].endswith('tessa-resolute-working-ordinary.png')
    advance
    assert eval scene_speaker == 'MARA'
    assert eval stage_faces('Mara')[0]['image'].endswith('mara-controlled-ordinary.png')
    assert eval stage_faces('Mara')[1]['who'] == 'TESSA'
    # Her painted portrait (batch 2) replaces the old head crop as soon as it exists.
    assert eval portrait_source(stage_faces('Mara')[0]['image'], 'speaker') == 'art/lit/portraits/mara-controlled-speaking-ordinary-original.webp'
    $ STAGING['6']['stages'] = _planned_stages

testcase listener_follows_the_scene:
    # When someone has left and another answers, the listener is the one who
    # answers: Orra is gone by Tessa's line in S025; Mara replies.
    $ book_pages(25)
    click id 'main_begin'
    run Jump('s025')
    pause 0.5
    advance until eval scene_speaker == 'TESSA'
    assert eval source_line == 1085 and staging_faces()[1]['who'] == 'MARA'

testcase page_portraits_and_initials:
    # Book pages show the speaker (and listener) in the margin and open each
    # scene with an illuminated initial; history keeps the plain letter.
    $ book_pages(19)
    click id 'main_begin'
    run Jump('s019')
    pause 0.5
    assert eval nvl_list and '{image=initial_T}' in nvl_list[-1][1]
    advance until eval scene_speaker == 'LUCAN'
    assert eval staging_faces()[0]['image'] == 'art/portraits/lucan-early-speaking.png'
    advance until eval scene_speaker == 'TESSA'
    # Her painted Gray Scar set (batch 5) replaces the earlier stand-in.
    assert eval staging_faces()[0]['image'] == 'art/portraits/tessa-campaign-early-speaking.png'
    assert eval staging_faces()[1]['image'] == 'art/portraits/lucan-early-listening.png'
    assert eval portrait_source(staging_faces()[1]['image']).startswith('art/lit/portraits/lucan-early-listening-')
    assert eval any(plain_initial(h.what).startswith('Tessa catches') for h in _history_list)
