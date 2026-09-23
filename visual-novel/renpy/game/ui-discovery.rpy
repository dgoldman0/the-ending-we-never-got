# Look closer / Threads.
# Looking closer reframes the originating painting toward a detail, shows the
# detail at a useful size, and can bring a related detail alongside it, joined
# by a thread. Return resumes the exact line. Threads revisits the same views.

transform reframe(fx, fy, z):
    subpixel True
    xanchor fx yanchor fy xpos fx ypos fy
    zoom 1.0 blur 0
    easein (0.05 if persistent.reduced_motion else 1.6) zoom z blur 18

transform detail_arrive(delay=0.0):
    alpha 0.0 xoffset -18
    pause (0 if persistent.reduced_motion else delay)
    easein (0.05 if persistent.reduced_motion else 0.55) alpha 1.0 xoffset 0

transform thread_draw:
    crop_relative True
    crop (0, 0, 0.0, 1.0)
    easein (0.05 if persistent.reduced_motion else 0.9) crop (0, 0, 1.0, 1.0)

style detail_title:
    font ui_serif
    size 44
    color ui_ivory
style detail_caption:
    font ui_italic
    size 31
    color ui_ivory_soft
    line_spacing 6
style detail_note:
    font ui_serif
    size 33
    color ui_ivory
    line_spacing 8

init python:
    def view_detail(view, which):
        spec = connection_views[view]
        item = detail_views[spec[which]]
        title = spec.get(which + 'title', item['title'])
        caption = reading_text_filter(spec.get(which + 'caption', item['caption']))
        return item, title, caption

    def detail_box(item, max_w, max_h):
        """Frame size matching the image, never enlarged past twice its pixels."""
        w, h = renpy.image_size(item['image'])
        scale = min(max_w / float(w), max_h / float(h), 2.0)
        return int(w * scale), int(h * scale)

screen detail_card(view, which, width, delay=0.0, max_h=420):
    $ item, title, caption = view_detail(view, which)
    $ bw, bh = detail_box(item, width, max_h)
    vbox at detail_arrive(delay):
        spacing 14 xsize width
        fixed:
            xysize (bw, bh)
            add lighting_art(item['image']) xysize (bw, bh)
            add Frame("ui/frame-line.png", 6, 6) xysize (bw, bh)
        null height 4
        text title style "detail_title"
        text caption style "detail_caption" xmaximum width

screen look_closer(detail=None, connection=False, view=None):
    tag menu
    default current_view = view or inspection_context(detail, connection)
    default alongside = False
    on "show" action Function(open_view, current_view)
    $ spec = connection_views.get(current_view) if current_view else None
    if spec is None:
        use menu_frame(_("Look closer")):
            text _("Details you look at closely will gather here as you read.") style "menu_note"
    else:
        add Solid("#07090b")
        add lighting_art(spec['origin']) at reframe(spec['focus'][0], spec['focus'][1], spec['zoom']):
            xysize (1920, 1080)
        add Solid("#07090bc8")
        add "ui/title-shade.png" xysize (1920, 1080) alpha 0.7
        text "look closer" style "menu_label" xpos 110 ypos 76
        text spec['title'] style "menu_heading" xpos 110 ypos 112
        if not alongside:
            fixed:
                pos (110, 262) xysize (860, 700)
                use detail_card(current_view, 'first', 860)
        else:
            fixed:
                pos (110, 262) xysize (1700, 720)
                fixed:
                    xysize (760, 700)
                    use detail_card(current_view, 'first', 760)
                add "ui/thread-long.png" at thread_draw:
                    xpos 772 ypos 150 xsize 160
                fixed:
                    xpos 940 xysize (760, 700)
                    use detail_card(current_view, 'second', 760, 0.35)
                text reading_text_filter(spec['note']) style "detail_note" at detail_arrive(0.7):
                    xpos 0 ypos 640 xmaximum 1500
        vbox:
            xalign 1.0 xoffset -90 ypos 84 spacing 6
            textbutton _("Return to reading") id "menu_return" style "caps_button" text_size 25 xalign 1.0 action Return()
            textbutton _("All threads") id "open_threads" style "caps_button" text_size 22 xalign 1.0 action ShowMenu('threads')
        if not alongside:
            $ second_item, second_title, second_caption = view_detail(current_view, 'second')
            hbox:
                xpos 1060 ypos 420 spacing 16
                add "ctc_knot" yalign 0.5
                textbutton (_("Bring alongside: ") + second_title):
                    id "bring_alongside"
                    style "caps_button" text_size 25 text_color ui_gold_bright
                    action [Function(follow_view, current_view), SetScreenVariable('alongside', True)]
        key "game_menu" action Return()

screen threads():
    tag menu
    use menu_frame(_("Threads"), 'threads'):
        $ views = available_inspections()
        if not views:
            text _("Details you look at closely will gather here as you read.") style "menu_note"
        else:
            vbox:
                spacing 26
                for view in views:
                    $ spec = connection_views[view]
                    $ followed = view in followed_connections
                    $ first, first_title, first_caption = view_detail(view, 'first')
                    $ second, second_title, second_caption = view_detail(view, 'second')
                    button:
                        id ('thread_' + view)
                        style "empty"
                        action ShowMenu('look_closer', view=view)
                        hover_background Solid("#cdb07612")
                        padding (14, 10)
                        vbox:
                            spacing 10
                            hbox:
                                spacing 18
                                text spec['title'] font ui_serif size 36 color ui_ivory yalign 1.0
                                text (_("followed") if followed else _("looked at")) style "menu_label" size 18 color ui_dim yalign 0.8
                            hbox:
                                spacing 16
                                $ fw, fh = detail_box(first, 230, 108)
                                fixed:
                                    xysize (fw, fh)
                                    add lighting_art(first['image']) xysize (fw, fh)
                                    add Frame("ui/frame-line.png", 6, 6) xysize (fw, fh)
                                if followed:
                                    add "ui/thread-long.png" xsize 60 yalign 0.5
                                    $ sw, sh = detail_box(second, 230, 108)
                                    fixed:
                                        xysize (sw, sh)
                                        add lighting_art(second['image']) xysize (sw, sh)
                                        add Frame("ui/frame-line.png", 6, 6) xysize (sw, sh)
                                text (reading_text_filter(spec['note']) if followed else first_caption):
                                    font ui_italic size 24 color ui_dim xmaximum 520 yalign 0.5
