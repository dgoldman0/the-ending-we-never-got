# Focused development gate. Captures are inspected manually, not image approval.
testcase rovel_layout_gate:
    click id 'main_begin'
    assert eval current_scene == 1 and source_line == 9
    advance until eval source_line == 32
    screenshot 'rovel-compact-standard.png'
    $ persistent.large_text = True
    screenshot 'rovel-compact-larger.png'
    advance until eval source_line == 81
    screenshot 'rovel-night-compact.png'
    advance until eval source_line == 112
    screenshot 'rovel-quiet-drawing.png'
    click id 'look_closer'
    screenshot 'rovel-first-night-inspection.png'
    click id 'menu_return'
    assert eval source_line == 112 and current_scene == 2
