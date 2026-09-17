# One editorial surface: details remain alongside each other, with the reading
# scene behind the main-owned shell. Return/Escape always resume that exact beat.
# Child coordinates are relative to the shell's 1680 x 760 content area.
screen look_closer(detail=None, connection=False):
    tag menu
    default selected_view = inspection_context(detail, connection)
    on "show" action Function(inspect_surface, inspection_context(detail, connection))
    use rovel_inspection_shell('Look closer'):
        use rovel_inspection_content(selected_view)

screen threads():
    tag menu
    default selected_view = inspection_context()
    on "show" action Function(inspect_surface, inspection_context())
    use rovel_inspection_shell('Threads'):
        use rovel_inspection_content(selected_view)

screen rovel_inspection_content(selected_view=None):
    fixed:
        xysize (1680, 760)
        if not available_inspections():
            text 'Details will gather here as you read.':
                style 'rovel_detail_text'
                size (39 if persistent.large_text else 34)
                ypos 120 xsize 1200
        else:
            # These are direct views, not a menu stack. Newly available tabs
            # occupy reserved positions without moving existing targets.
            textbutton 'First night':
                id 'thread_home'
                style 'rovel_detail_button'
                text_size (36 if persistent.large_text else 31)
                xpos 0 ypos 0 xsize 500 ysize 76
                selected selected_view == 'home'
                action [Function(inspect_surface, 'home'), SetScreenVariable('selected_view', 'home')]
            if 'treatment' in available_inspections():
                textbutton 'Olan’s treatment':
                    id 'thread_treatment'
                    style 'rovel_detail_button'
                    text_size (36 if persistent.large_text else 31)
                    xpos 530 ypos 0 xsize 540 ysize 76
                    selected selected_view == 'treatment'
                    action [Function(inspect_surface, 'treatment'), SetScreenVariable('selected_view', 'treatment')]
            if 'promise' in available_inspections():
                textbutton 'The public promise':
                    id 'thread_promise'
                    style 'rovel_detail_button'
                    text_size (36 if persistent.large_text else 31)
                    xpos 1100 ypos 0 xsize 580 ysize 76
                    selected selected_view == 'promise'
                    action [Function(inspect_surface, 'promise'), SetScreenVariable('selected_view', 'promise')]

            fixed:
                ypos 96 xysize (1680, 664)
                if selected_view == 'home':
                    use rovel_home_details
                elif selected_view == 'treatment':
                    use rovel_treatment_details
                elif selected_view == 'promise':
                    use rovel_promise_details

screen rovel_detail_panel(detail, title=None, caption=None):
    $ item = detail_views[detail]
    fixed:
        xysize (810, 570)
        text (title or item['title']):
            style 'rovel_detail_heading'
            xsize 810 ypos 0
        add lighting_art(item['image']):
            xpos 0 ypos 66 xysize (810, 316) fit 'contain'
        text (caption or item['caption']):
            style 'rovel_detail_text'
            size (39 if persistent.large_text else 34)
            xpos 0 ypos 410 xsize 810

screen rovel_home_details():
    use rovel_detail_panel('drawing')
    fixed:
        xpos 870 xysize (810, 570)
        use rovel_detail_panel('phone')
    text 'A welcome letter on one side; her mother’s kitchen on the other.':
        style 'rovel_detail_note'
        size (38 if persistent.large_text else 34)
        ypos 590 xsize 1680

screen rovel_treatment_details():
    use rovel_detail_panel('treatment_blue')
    fixed:
        xpos 870 xysize (810, 570)
        use rovel_detail_panel('treatment_white')
    if 'promise' in available_inspections():
        textbutton 'Bring the ceremony alongside':
            id 'follow_public_promise'
            style 'rovel_detail_button'
            text_size (36 if persistent.large_text else 31)
            xpos 0 ypos 582 xsize 860 ysize 80
            action [Function(inspect_surface, 'promise'), SetScreenVariable('selected_view', 'promise')]

screen rovel_promise_details():
    use rovel_detail_panel('treatment_white', title='At the bedside',
        caption='The curse has cleared. Two fingers are still missing.')
    fixed:
        xpos 870 xysize (810, 570)
        use rovel_detail_panel('applause')
    text ('Senn: ' + detail_views['applause']['description']):
        style 'rovel_detail_note'
        size (38 if persistent.large_text else 34)
        ypos 558 xsize 1680

style rovel_detail_heading:
    font 'fonts/EBGaramond12-Regular.ttf'
    size 44
    color '#eadfca'

style rovel_detail_text:
    font 'fonts/CharisSIL-Regular.ttf'
    size 34
    color '#eee4d4'
    line_spacing 4

style rovel_detail_note:
    font 'fonts/EBGaramond12-Italic.ttf'
    size 34
    color '#d4c2a1'
    line_spacing 3

style rovel_detail_button:
    background Solid('#172429e8')
    hover_background Solid('#3b4645f2')
    selected_background Solid('#344348f2')
    padding (28, 12)

style rovel_detail_button_text:
    font 'fonts/ClearSans-Regular.ttf'
    size 31
    color '#cec6b5'
    hover_color '#ffffff'
    selected_color '#f6e1b5'
    yalign 0.5
