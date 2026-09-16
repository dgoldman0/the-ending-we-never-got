screen inquiry_invitation(number):
    modal True
    add Solid('#101f26')
    vbox:
        xpos 330 ypos 220 xsize 1260 spacing 30
        text 'A MOMENT TO CONSIDER' style 'caption_text'
        text ['Promises and limits', 'What was known?', 'The cost of cooperation', 'Harrow: event and account', 'What can be relied on?'][number-1] style 'title_text' size 58
        text 'You can examine what you have learned, compare details, or continue the story. These inquiries remain available from the reading menu. Time does not pass here.' style 'prose_text'
        hbox:
            spacing 24
            textbutton 'Investigate' id 'open_inquiry' action ShowMenu('investigation')
            textbutton 'Continue the story' id 'continue_story' action Return()

screen investigation():
    tag menu
    default selected_case = available_cases()[0] if available_cases() else None
    default selected_evidence = None
    default show_question = False
    default feedback = ''
    use menu_frame('Investigation'):
        if selected_case is None:
            text 'Inquiries open at the first chapter’s end.' style 'prose_text'
        else:
            $ case = cases[selected_case]
            hbox:
                spacing 30
                vbox:
                    xsize 340 spacing 14
                    text 'YOUR READING NOTES' style 'caption_text'
                    for cid in available_cases():
                        textbutton (('Done: ' if cid in findings else '') + cases[cid]['title']):
                            id ('case_' + cid)
                            xfill True
                            selected cid == selected_case
                            action [SetScreenVariable('selected_case', cid), SetScreenVariable('selected_evidence', None), SetScreenVariable('show_question', False), SetScreenVariable('feedback', '')]
                    null height 16
                    text 'The story’s people know only what their scenes establish.' size 23 color '#aabeba'
                vbox:
                    xsize 1030 spacing 18
                    text case['title'] font 'fonts/CharisSIL-Regular.ttf' size 42
                    if not selected_evidence and not show_question:
                        text 'Examine the material, then compare what it supports.' size 25 color '#bdcfc6'
                        for eid in readable_evidence(selected_case):
                            textbutton (('Read · ' if eid in viewed_evidence else '') + evidence[eid]['title']):
                                xfill True
                                id ('evidence_' + eid)
                                action [Function(mark_evidence, eid), SetScreenVariable('selected_evidence', eid)]
                        if unlocked_round < case.get('resolve_round', case['round']):
                            text 'This inquiry continues after later chapters. Your earlier material stays available.' size 25 color '#aabeba'
                        else:
                            textbutton 'Compare the evidence' id 'compare_evidence':
                                sensitive case_ready(selected_case)
                                action SetScreenVariable('show_question', True)
                            if not case_ready(selected_case):
                                text 'Open each item above to make the comparison.' size 23 color '#aabeba'
                        if selected_case in findings:
                            text 'Finding established' color '#d9c699' size 25
                    elif selected_evidence:
                        $ item = evidence[selected_evidence]
                        text item['source'] style 'caption_text'
                        viewport:
                            id 'evidence_scroll'
                            ysize 570 mousewheel True draggable True scrollbars 'vertical'
                            vbox:
                                xsize 970 spacing 24
                                text item['title'] font 'fonts/CharisSIL-Regular.ttf' size 38
                                text item['body'] font 'fonts/CharisSIL-Regular.ttf' size (34 if persistent.large_text else 29) line_spacing 9
                                frame:
                                    background Solid('#233b40') padding (22, 19)
                                    text item['detail'] size (31 if persistent.large_text else 27) color '#d4dfce'
                        textbutton 'Back to material' id 'back_to_material' action SetScreenVariable('selected_evidence', None)
                    else:
                        viewport:
                            ysize 655 mousewheel True draggable True scrollbars 'vertical'
                            vbox:
                                spacing 22 xsize 970
                                if selected_case in findings:
                                    text 'ESTABLISHED' style 'caption_text' color '#d9c699'
                                    text case['finding'] style 'prose_text' size (36 if persistent.large_text else 31)
                                    text 'The limit of this finding' style 'caption_text'
                                    text case['limit'] style 'prose_text' size (34 if persistent.large_text else 29)
                                else:
                                    text case['question'] style 'prose_text'
                                    for ai, answer in enumerate(case['options']):
                                        textbutton answer:
                                            selected False
                                            xfill True text_size (31 if persistent.large_text else 27)
                                            id ('answer_' + str(ai))
                                            action [Function(resolve_case, selected_case, ai), SetScreenVariable('feedback', '' if ai == case['answer'] else case['hint'])]
                                    if feedback:
                                        text feedback size 27 color '#d9c699'
                                    textbutton 'Walk me through it' id 'guided_explanation' action [Function(resolve_case, selected_case, case['answer']), SetScreenVariable('feedback', '')]
                        textbutton 'Back to material' id 'back_to_comparison' action [SetScreenVariable('show_question', False), SetScreenVariable('feedback', '')]
