# Prototype: portrait-treatment samples. NOT part of the game.
# prototypes/portrait-frames/sample.py copies this file (and its art) into the
# game only while it captures sample screens, then removes it. It replaces the
# stage say screen with the old layout on the old gradient, except:
#   - the arch windows are replaced by one of three treatments (frame_style):
#     'vignette' (no frame, the bust dissolves into the shade), 'oval' (a
#     miniature with a fine gilt rim) or 'rect' (a hairline-rimmed miniature);
#     each fades at its base, so nothing cuts across the chest;
#   - the listener is smaller and quieter, at the far end of the line, not
#     glancing from the next frame over;
#   - no pointer rule under the name; a lozenge replaces the continue knot;
#   - shade_style 'lacquer' tints the gradient deep celadon with a faint grain.
init offset = 10

default frame_style = 'oval-halo'
default shade_style = 'plain'
define FRAME_TEXT_X = 424
define FRAME_TEXT_W = 1030
define FRAME_TEXT_TOP = 874
define FRAME_LISTENER_POS = (1500, 850)

image ctc_knot:
    "frames/lozenge-gilt.png"
    yoffset 3
    alpha 0.0
    easein 0.35 alpha 1.0
    block:
        easein 1.1 alpha 0.45
        easeout 1.1 alpha 1.0

init python:
    FRAME_SIZES = {'vignette': {'speaker': (270, 310), 'listener': (150, 172)},
                   'oval': {'speaker': (224, 280), 'listener': (132, 165)},
                   'oval-bare': {'speaker': (224, 280), 'listener': (132, 165)},
                   'oval-halo': {'speaker': (224, 280), 'listener': (132, 165)},
                   'rect': {'speaker': (208, 262), 'listener': (124, 156)}}
    FRAME_SPEAKER_POS = {'vignette': (98, 738), 'oval': (118, 750), 'oval-bare': (118, 750),
                         'oval-halo': (118, 750), 'rect': (126, 758)}
    # speaker_only: the person spoken to is in the painting, so no listener portrait
    speaker_only = True

    def framed_portrait(face, role):
        w, h = FRAME_SIZES[frame_style][role]
        key = portrait_choice(face['image'], role) or portrait_key(face['image'])
        want = 'right' if role == 'speaker' else 'left'
        flip = PORTRAIT_CROPS['facing'].get(key, want) != want
        scale = max(w / CROP_SIZE[0], h / CROP_SIZE[1])
        cw, ch = int(round(CROP_SIZE[0] * scale)), int(round(CROP_SIZE[1] * scale))
        head = Transform(portrait_source(face['image'], role), xysize=(cw, ch), xzoom=(-1.0 if flip else 1.0),
                         xpos=(w - cw) // 2, ypos=(h - ch) // 2)
        shape = 'oval' if frame_style.startswith('oval') else frame_style
        image = AlphaMask(Fixed(head, xysize=(w, h)), 'frames/mask-%s-%s.png' % (shape, role))
        if frame_style == 'oval-halo':
            image = Fixed(Transform(lit_ornament('frames/halo-oval-%s.png' % role), xpos=-26, ypos=-26),
                          image, xysize=(w, h))
        elif frame_style in ('oval', 'rect'):
            image = Fixed(image, lit_ornament('frames/rim-%s-%s.png' % (frame_style, role)), xysize=(w, h))
        if role == 'listener':
            image = Transform(image, alpha=0.84, matrixcolor=SaturationMatrix(0.8) * BrightnessMatrix(-0.03))
        return image

    def frame_text_top(what, who):
        t = Text(what, style='stage_speech' if who else 'stage_action', size=text_size(38), xmaximum=FRAME_TEXT_W)
        height = renpy.render(t, FRAME_TEXT_W, 4000, 0, 0).height
        lines = max(1, int(round(height / float(text_size(STAGE_LINE)))))
        return FRAME_TEXT_TOP - max(0, lines - 3) * text_size(STAGE_LINE)

screen say(who, what):
    $ beat = current_rovel_beat()
    $ framing = stage_framing()
    $ speaker, listener = stage_faces(who)
    $ grade = beat.get('grade') if beat else (_scene_spec() or {}).get('grade')
    $ heading = first_line_of_scene()
    if framing.get('text'):
        $ tx, ty, tw = framing['text']
        add "ui/text-pool.png" pos (tx - 170, ty - 150)
        if heading:
            text scene_heading_line() style "stage_heading" pos (tx, ty - 58)
        text what id "what" pos (tx, ty) xmaximum tw size text_size(38)
    else:
        $ top = frame_text_top(what, who)
        # shading samples: the current shade; a deeper gradient; the current
        # shade plus a soft pool behind the text; the deeper gradient plus a
        # soft shadow around the letters. None is solid.
        if shade_style in ('medium', 'strong'):
            add "frames/shade-%s.png" % shade_style xsize 1920 ysize 560 ypos 520
        else:
            add "ui/scrim.png" xsize 1920 ysize 560 ypos 520 alpha scrim_strength(beat)
        if shade_style == 'pool-shadow':
            add "frames/shade-pool.png" pos (FRAME_TEXT_X - 380, top - 170)
        if portrait_ready(speaker):
            add "ui/portrait-pool.png" pos (0, 620)
            add framed_portrait(speaker, 'speaker') pos FRAME_SPEAKER_POS[frame_style]
        if portrait_ready(listener) and not speaker_only:
            add framed_portrait(listener, 'listener') pos FRAME_LISTENER_POS
        if heading:
            text scene_heading_line() style "stage_heading" pos (FRAME_TEXT_X, top - 100)
        if who:
            text who.lower() id "who" pos (FRAME_TEXT_X, top - 50)
        if shade_style == 'pool-shadow':
            text what id "what" pos (FRAME_TEXT_X, top) xmaximum FRAME_TEXT_W size text_size(38) outlines [(absolute(12), "#00000022", 0, 2), (absolute(7), "#00000040", 0, 2), (absolute(3), "#00000066", 0, 1), (absolute(1), "#0000007a", 0, 0)]
        else:
            text what id "what" pos (FRAME_TEXT_X, top) xmaximum FRAME_TEXT_W size text_size(38)
    use quick_menu('stage')
