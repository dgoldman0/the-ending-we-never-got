# Attention belongs to the reader. These screens never move the story position.
screen look_closer(detail=None, connection=False):
    tag menu
    default selected_detail = detail if detail in available_details() else None
    default alongside = connection and bool(available_details())
    default unfold = connection and 'home' in followed_connections
    use menu_frame('Look closer'):
        if not available_details():
            text 'A detail may catch your attention as you read.' style 'prose_text'
        elif alongside:
            vbox:
                spacing 24
                text 'THE FIRST NIGHT  /  A ROOM REMEMBERED' style 'caption_text'
                hbox:
                    spacing 50
                    vbox:
                        xsize 760 spacing 16
                        text 'On the reverse of a welcome' font 'fonts/EBGaramond12-Regular.ttf' size 40
                        add lighting_art('art/opening/cg/detail-drawing.png') xysize (760, 265)
                    vbox:
                        xsize 760 spacing 16
                        text 'On the other side of the silence' font 'fonts/EBGaramond12-Regular.ttf' size 40
                        add lighting_art('art/opening/cg/detail-phone.png') xysize (455, 265)
                if unfold:
                    text '“MOM — DID YOU GET THE MILK?”' font 'fonts/EBGaramond12-Italic.ttf' size 40 color '#decaab'
                    text 'The last request from home was ordinary. Here, even the paper is the temple’s: a welcome letter turned over to make room for her mother’s kitchen. One side welcomes her into a life chosen for her. The other holds a place she is trying not to lose.' style 'prose_text' size (35 if persistent.large_text else 31) xsize 1450
                    text 'The drawing begins with somewhere her mother can sit.' font 'fonts/EBGaramond12-Italic.ttf' size 39 color '#e2d0af'
                else:
                    text 'The phone cannot reach home. On the page, she begins again.' style 'prose_text' xsize 1320
                    textbutton 'Follow this connection' id 'follow_connection':
                        action [Function(follow_home_thread), SetScreenVariable('unfold', True)]
                textbutton 'Back to the details' id 'back_to_details':
                    action [SetScreenVariable('alongside', False), SetScreenVariable('unfold', False)]
        elif selected_detail:
            $ detail_item = detail_views[selected_detail]
            hbox:
                spacing 65
                vbox:
                    xsize 1050 spacing 28
                    text 'THE FIRST NIGHT' style 'caption_text'
                    text detail_item['title'] font 'fonts/EBGaramond12-Regular.ttf' size 55 color '#e2d0af'
                    if selected_detail == 'drawing':
                        add lighting_art(detail_item['image']) xysize (1050, 366)
                    else:
                        add lighting_art(detail_item['image']) xysize (688, 400)
                    text detail_item['caption'] font 'fonts/EBGaramond12-Italic.ttf' size 38 color '#ddd1b9'
                    text detail_item['description'] style 'prose_text' size (34 if persistent.large_text else 30)
                vbox:
                    xsize 440 spacing 24
                    text 'A CONNECTION' style 'caption_text'
                    $ related = 'phone' if selected_detail == 'drawing' else 'drawing'
                    add lighting_art(detail_views[related]['image']) xsize 415 fit 'contain'
                    textbutton ('Bring the phone alongside' if related == 'phone' else 'Bring the drawing alongside'):
                        id 'bring_alongside'
                        xsize 440
                        action [Function(inspect_detail, related), SetScreenVariable('alongside', True)]
                    null height 40
                    textbutton 'The whole scene' id 'whole_scene' action SetScreenVariable('selected_detail', None)
        else:
            hbox:
                spacing 64
                fixed:
                    xsize 1120 ysize 660
                    add lighting_art('art/opening/cg/drawing-restart.png') xysize (1120, 630)
                    button:
                        xpos 498 ypos 551 xsize 205 ysize 54
                        background Solid('#0b1419de') hover_background Solid('#574b35ef')
                        action [Function(inspect_detail, 'drawing'), SetScreenVariable('selected_detail', 'drawing')]
                        text 'The torn page' size 23
                    button:
                        xpos 898 ypos 581 xsize 218 ysize 54
                        background Solid('#0b1419de') hover_background Solid('#574b35ef')
                        action [Function(inspect_detail, 'phone'), SetScreenVariable('selected_detail', 'phone')]
                        text 'The dead phone' size 23
                vbox:
                    xsize 400 spacing 23
                    text 'THE FIRST NIGHT' style 'caption_text'
                    text 'What remains\nof home' font 'fonts/EBGaramond12-Regular.ttf' size 51 color '#e2d0af'
                    textbutton 'The torn page' id 'inspect_drawing' action [Function(inspect_detail, 'drawing'), SetScreenVariable('selected_detail', 'drawing')]
                    textbutton 'The dead phone' id 'inspect_phone' action [Function(inspect_detail, 'phone'), SetScreenVariable('selected_detail', 'phone')]
                    null height 30
                    textbutton 'Threads' action ShowMenu('threads')

screen threads():
    tag menu
    use menu_frame('Threads'):
        if not available_details():
            text 'Connections will gather here as you read.' style 'prose_text'
        else:
            vbox:
                spacing 32
                text 'THE FIRST NIGHT' style 'caption_text'
                hbox:
                    spacing 80
                    button:
                        id 'thread_drawing'
                        xsize 690 ysize 240
                        action [Function(inspect_detail, 'drawing'), ShowMenu('look_closer', detail='drawing')]
                        vbox:
                            spacing 23
                            add lighting_art('art/opening/cg/detail-drawing.png') xysize (570, 198)
                            text 'The torn page' font 'fonts/EBGaramond12-Regular.ttf' size 38
                    text '—' ypos 72 font 'fonts/EBGaramond12-Regular.ttf' size 50 color '#b39d78'
                    button:
                        id 'thread_phone'
                        xsize 610 ysize 260
                        action [Function(inspect_detail, 'phone'), ShowMenu('look_closer', detail='phone')]
                        vbox:
                            spacing 20
                            add lighting_art('art/opening/cg/detail-phone.png') xysize (341, 198)
                            text 'The dead phone' font 'fonts/EBGaramond12-Regular.ttf' size 38
                if 'home' in followed_connections:
                    textbutton 'A room remembered' id 'thread_home':
                        style 'hero_button' xsize 800
                        action ShowMenu('look_closer', detail='drawing', connection=True)
                    text 'A welcome turned over. A place she is trying not to lose.' font 'fonts/EBGaramond12-Italic.ttf' size 35 color '#c8bba3'
                else:
                    textbutton 'Bring them together' id 'thread_connect':
                        action ShowMenu('look_closer', detail='drawing', connection=True)
