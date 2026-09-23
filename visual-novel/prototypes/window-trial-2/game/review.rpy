define _test.screenshot_directory = "review"

testcase comparisons:
    click id "main_begin"
    click id "page_next"
    pause 0.3
    click id "page_next"
    pause 0.3
    click id "page_next"
    pause 0.3
    click id "page_next"
    pause 0.3
    run SetVariable("composition", "nightglass")
    pause 0.4
    screenshot "comparisons/01-nightglass-initial.png"
    run SetVariable("composition", "vellum")
    pause 0.4
    screenshot "comparisons/02-vellum-initial.png"


testcase passage_review:
    run SetVariable("thread_seen",False)
    run SetVariable("composition", "nightglass")
    run SetField(persistent,"softened",False)
    run SetField(persistent,"large_text",False)
    click id "main_begin"
    assert eval page_index == 0
    screenshot "final/intense-00.png"
    click id "page_next"
    pause 0.3
    assert eval page_index == 1
    screenshot "final/intense-01.png"
    click id "page_next"
    pause 0.3
    assert eval page_index == 2
    screenshot "final/intense-02.png"
    click id "page_next"
    pause 0.3
    assert eval page_index == 3
    screenshot "final/intense-03.png"
    click id "page_next"
    pause 0.3
    assert eval page_index == 4
    screenshot "final/intense-04.png"
    click id "page_next"
    pause 0.3
    assert eval page_index == 5
    screenshot "final/intense-05.png"
    click id "page_next"
    pause 0.3
    assert eval page_index == 6
    screenshot "final/intense-06.png"
    click id "page_next"
    pause 0.3
    assert eval page_index == 7
    screenshot "final/intense-07.png"
    click id "page_next"
    pause 0.3
    assert eval page_index == 8
    screenshot "final/intense-08.png"
    click id "page_next"
    pause 0.3
    assert eval page_index == 9
    screenshot "final/intense-09.png"
    click id "page_next"
    pause 0.3
    assert eval page_index == 10
    screenshot "final/intense-10.png"
    click id "page_next"
    pause 0.3
    assert eval page_index == 11
    screenshot "final/intense-11.png"
    click id "page_next"
    pause 0.3
    assert eval page_index == 12
    screenshot "final/intense-12.png"
    click id "look_closer"
    assert screen "closer"
    screenshot "final/closer.png"
    click id "follow_thread"
    assert eval thread_seen
    screenshot "final/connection.png"
    click id "closer_return"
    assert eval page_index == 12
    run ShowMenu("threads")
    assert screen "threads"
    click id "threads_return"
    assert eval page_index == 12
    run QuickSave(message="Place saved")
    click id "page_back"
    pause 0.3
    assert eval page_index == 11
    run QuickLoad(confirm=False)
    pause 0.5
    assert eval page_index == 12 and thread_seen
    run ShowMenu("proof_menu")
    click id "lighting"
    click id "type"
    click id "menu_return"
    assert eval persistent.softened and persistent.large_text and page_index == 12
    pause 0.3
    screenshot "final/soft-large-12.png"
    click id "page_back"
    pause 0.3
    assert eval page_index == 11
    screenshot "final/soft-large-11.png"
    click id "page_back"
    pause 0.3
    assert eval page_index == 10
    screenshot "final/soft-large-10.png"
    click id "page_back"
    pause 0.3
    assert eval page_index == 9
    screenshot "final/soft-large-09.png"
    click id "page_back"
    pause 0.3
    assert eval page_index == 8
    screenshot "final/soft-large-08.png"
    click id "page_back"
    pause 0.3
    assert eval page_index == 7
    screenshot "final/soft-large-07.png"
    click id "page_back"
    pause 0.3
    assert eval page_index == 6
    screenshot "final/soft-large-06.png"
    click id "page_back"
    pause 0.3
    assert eval page_index == 5
    screenshot "final/soft-large-05.png"
    click id "page_back"
    pause 0.3
    assert eval page_index == 4
    screenshot "final/soft-large-04.png"
    click id "page_back"
    pause 0.3
    assert eval page_index == 3
    screenshot "final/soft-large-03.png"
    click id "page_back"
    pause 0.3
    assert eval page_index == 2
    screenshot "final/soft-large-02.png"
    click id "page_back"
    pause 0.3
    assert eval page_index == 1
    screenshot "final/soft-large-01.png"
    click id "page_back"
    pause 0.3
    assert eval page_index == 0
    screenshot "final/soft-large-00.png"
    run SetField(persistent,"softened",False)
    run SetField(persistent,"large_text",False)
    run MainMenu(confirm=False)
    assert screen "main_menu"
    screenshot "final/title.png"
