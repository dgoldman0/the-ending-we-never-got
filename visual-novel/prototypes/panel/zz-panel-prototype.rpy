# Prototype: the reading panel samples. NOT part of the game.
# prototypes/panel/sample.py copies this file (and the panel art) into the game
# only while it captures sample screens, then removes it. It replaces the stage
# say screen with a panel version:
#   - the lower band is a real surface (lacquer or vellum) with one fine
#     engraved border across its width, instead of a shade over the painting;
#   - the speaker's portrait is set into the surface as an engraved niche, not
#     a free-standing laurel frame; the listener sits in a smaller niche at the
#     far end of the panel, across the text, not beside the speaker;
#   - no pointer rule; the name is set above the text as a rubric;
#   - a small lozenge replaces the continue knot, which read as a (R) sign.
init offset = 10

default panel_style = 'lacquer'
define PANEL_TEXT_X = 424
define PANEL_TEXT_W = 1030
define LISTENER_POS = (1490, 846)
define PANEL_TEXT_TOP = 872

image ctc_knot:
    ConditionSwitch("panel_style == 'vellum'", "panel/lozenge-ink.png", "True", "panel/lozenge-gilt.png")
    yoffset 3
    alpha 0.0
    easein 0.35 alpha 1.0
    block:
        easein 1.1 alpha 0.45
        easeout 1.1 alpha 1.0

init python:
    def panel_portrait(face, role, grade=None):
        """The portrait alone, masked to its arch, for a niche in the panel."""
        w, h = PORTRAIT_SIZES[role]
        key = portrait_choice(face['image'], role) or portrait_key(face['image'])
        want = 'right' if role == 'speaker' else 'left'
        flip = PORTRAIT_CROPS['facing'].get(key, want) != want
        scale = max(w / CROP_SIZE[0], h / CROP_SIZE[1])
        cw, ch = int(round(CROP_SIZE[0] * scale)), int(round(CROP_SIZE[1] * scale))
        head = Transform(portrait_source(face['image'], role), xysize=(cw, ch), xzoom=(-1.0 if flip else 1.0),
                         xpos=(w - cw) // 2, ypos=(h - ch) // 2)
        return AlphaMask(Fixed(head, xysize=(w, h)), 'ui/window-mask-' + role + '.png')

    def panel_text_top(what, who):
        t = Text(what, style='stage_speech' if who else 'stage_action', size=text_size(38), xmaximum=PANEL_TEXT_W)
        height = renpy.render(t, PANEL_TEXT_W, 4000, 0, 0).height
        lines = max(1, int(round(height / float(text_size(STAGE_LINE)))))
        return PANEL_TEXT_TOP - max(0, lines - 3) * text_size(STAGE_LINE)

screen say(who, what):
    $ beat = current_rovel_beat()
    $ framing = stage_framing()
    $ speaker, listener = stage_faces(who)
    $ grade = beat.get('grade') if beat else (_scene_spec() or {}).get('grade')
    $ heading = first_line_of_scene()
    $ vellum = panel_style == 'vellum'
    $ ink = ui_ink if vellum else ui_ivory
    $ soft = ui_ink_soft if vellum else ui_ivory_soft
    $ rubric = ui_ink_gold if vellum else ui_gold
    $ outline = [] if vellum else [(absolute(2), "#00000040", 0, 1)]
    if framing.get('text'):
        $ tx, ty, tw = framing['text']
        add "ui/text-pool.png" pos (tx - 170, ty - 150)
        if heading:
            text scene_heading_line() style "stage_heading" pos (tx, ty - 58)
        text what id "what" pos (tx, ty) xmaximum tw size text_size(38)
    else:
        $ top = panel_text_top(what, who)
        # vellum is paper, so it only dims a little at night; lacquer and gilt take the scene's light
        $ panel_art = "panel/panel-%s.png" % panel_style
        if vellum:
            add Transform(panel_art, matrixcolor=BrightnessMatrix(-0.10 if grade == 'night' else 0.0) * SaturationMatrix(0.92 if grade == 'night' else 1.0)) pos (0, 736)
        else:
            add lit_ornament(panel_art) pos (0, 736)
        if portrait_ready(speaker):
            add panel_portrait(speaker, 'speaker', grade) pos (120, 800)
            add "panel/niche-shade-speaker-%s.png" % panel_style pos (108, 788)
        if portrait_ready(listener):
            add panel_portrait(listener, 'listener', grade) pos LISTENER_POS
            add "panel/niche-shade-listener-%s.png" % panel_style pos (LISTENER_POS[0] - 12, LISTENER_POS[1] - 12)
        if heading:
            text scene_heading_line() style "stage_heading" color rubric outlines [] pos (PANEL_TEXT_X, top - 92)
        if who:
            text who.lower() id "who" pos (PANEL_TEXT_X, top - 50) color rubric outlines []
        text what id "what" pos (PANEL_TEXT_X, top) xmaximum PANEL_TEXT_W size text_size(38) color (ink if who else soft) outlines outline
    use quick_menu('day' if vellum else 'stage')
