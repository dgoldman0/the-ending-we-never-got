# Reading presentation.
# Illustrated scenes: the painting stays whole. Behind the text it falls softly
# out of focus and into its own shadow colour; the speaker alone appears in an
# oval with a golden halo (the person spoken to is in the painting). The
# controls wait behind a small gilt sun. Chosen by the user on 24 September
# 2026 from the samples in prototypes/portrait-frames.
# Prose-only scenes: a typeset page, like a printed play, whose paper follows
# the scene's light (day vellum, dusk slate, night ink).

default page_scene = 0
default page_index = 0
default last_stage_image = None

define PAGE_X = 560
define PAGE_W = 980
define PAGE_FIRST_TOP = 372
define PAGE_NEXT_TOP = 150
define PAGE_BOTTOM = 1010
define PAGE_GAP = 20

define STAGE_TEXT_X = 424
define STAGE_TEXT_W = 1030
define SOFT_TOP = 640
define STAGE_TEXT_TOP = 874
define STAGE_LINE = 53

init -1 python:
    import json
    import math

    # Shot-specific framing where the painting's key action meets the reading
    # band: 'lift' raises the painting (the dark shade fills beneath it), and
    # 'text' moves quiet lines into the painting's own shadow.
    STAGE_FRAMING = {
        # Tessa's landing foot clears the scene heading; her hair clears the top.
        'arrival': dict(lift=70),
        'night-drawing': dict(text=(440, 250, 600)),
        'night-restart': dict(text=(440, 250, 600)),
    }

    def stage_framing():
        beat = current_rovel_beat()
        if beat:
            return STAGE_FRAMING.get(beat.get('stage_id'), {})
        stage = staging_stage() if current_scene > 5 else None
        return stage.get('framing', {}) if stage else {}

    _staged = []

    def staged_scene(scene=None):
        """Scenes with authored beats, or with staging art on disk, are read
        over their paintings; the rest are read on the typeset page."""
        if not _staged:
            _staged.append(frozenset(key[0] for key in ROVEL_BEATS))
        n = current_scene if scene is None else scene
        return n in _staged[0] or staging_stage(n, 0) is not None

    _LIGHT_WORDS = (('PRE-DAWN', 'dusk'), ('BEFORE DAWN', 'dusk'), ('DAWN', 'dusk'),
                    ('DUSK', 'dusk'), ('EVENING', 'dusk'), ('NIGHT', 'night'))

    def scene_light(scene=None):
        """Page tone from the screenplay's time of day; CONTINUOUS/LATER inherit."""
        n = current_scene if scene is None else scene
        while n > 0:
            time = source_map['scenes'][n - 1]['heading'].rsplit(' - ', 1)[-1]
            if time in ('CONTINUOUS', 'LATER'):
                n -= 1
                continue
            for word, light in _LIGHT_WORDS:
                if word in time:
                    return light
            return 'day'
        return 'day'

    _MINOR = {'of', 'the', 'and', 'below', 'above', 'after', 'before', 'to', 'in', 'on', 'at'}

    def nice_title(text):
        words = text.lower().split()
        out = []
        for i, word in enumerate(words):
            if i and word in _MINOR:
                out.append(word)
            else:
                out.append(word[:1].upper() + word[1:])
        return ' '.join(out)

    def _heading_parts(scene=None):
        n = current_scene if scene is None else scene
        if not n:
            return [], ''
        body = re.sub(r'^(INT\.|EXT\.) ', '', source_map['scenes'][n - 1]['heading'])
        parts = body.split(' - ')
        if len(parts) == 1:
            return parts, ''
        return parts[:-1], parts[-1]

    def scene_place_name(scene=None):
        places, _time = _heading_parts(scene)
        return ' · '.join(nice_title(p) for p in places)

    def scene_time_name(scene=None):
        _places, time = _heading_parts(scene)
        return nice_title(time) if time else ''

    _ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']

    def chapter_label(chapter=None):
        chapter = current_chapter if chapter is None else chapter
        if not chapter:
            return ''
        return (_ROMAN[chapter] + ' · ' + chapter_names[chapter - 1]).lower()

    def scene_heading_line():
        time = scene_time_name()
        line = chapter_label() + '   ·   ' + scene_place_name().lower()
        return line + ('  ·  ' + time.lower() if time else '')

    def first_line_of_scene():
        if not current_scene or source_page:
            return False
        blocks = source_map['scenes'][current_scene - 1]['blocks']
        return bool(blocks) and blocks[0]['line'] == source_line

    # Page measurement uses the same styles and widths as the page screen.
    _height_cache = {}

    def entry_height(who, what):
        key = (bool(who), what, persistent.large_text)
        if key not in _height_cache:
            if is_super_caption(what):
                style, size = 'page_super', text_size(30)
            else:
                style, size = ('page_speech' if who else 'page_action'), text_size(36)
            t = Text(what, style=style, size=size, xmaximum=PAGE_W)
            _height_cache[key] = renpy.render(t, PAGE_W, 4000, 0, 0).height + PAGE_GAP
        return _height_cache[key]

    def page_has_room(who, what):
        top = PAGE_FIRST_TOP if store.page_index == 0 else PAGE_NEXT_TOP
        used = sum(entry_height(e[0], e[1]) for e in (store.nvl_list or []) if e)
        return top + used + entry_height(who, what) <= PAGE_BOTTOM

    class PageCharacter(NVLCharacter):
        """NVL entries that start a fresh page per scene and when full."""

        def do_add(self, who, what, multiple=None):
            NVLCharacter.do_add(self, who, what, multiple=multiple)
            if store.page_scene != current_scene:
                nvl_clear()
                store.page_scene = current_scene
                store.page_index = 0
                renpy.transition(ui_page_turn)
            elif store.nvl_list and (is_super_caption(what) or not page_has_room(who, what)):
                nvl_clear()
                store.page_index += 1
                renpy.transition(ui_page_turn)

    def stage_image():
        beat = current_rovel_beat()
        if beat:
            return lit_stage(beat['stage_id']) or beat['stage']['image']
        shot = opening_shot()
        if opening_assets_available(shot):
            return shot['image']
        staged = staging_stage() if current_scene > 5 else None
        return composed_scene() or (scene_art if art_available() else None) or (staged['image'] if staged else None)

    def stage_faces(who):
        """Speaker and listener portraits: authored beats first, then staging."""
        if not who:
            return None, None
        beat = current_rovel_beat()
        if beat:
            return beat.get('speaker'), beat.get('listener')
        return staging_faces()

    def note_stage_change():
        image = stage_image()
        if image != store.last_stage_image:
            store.last_stage_image = image
            renpy.transition(ui_scene_change)

    class ReaderVoice(object):
        """One speaker, read over the painting or on the page by scene."""

        def __init__(self, name):
            self.name = name
            self.stage = Character(name, kind=adv, ctc='ctc_knot', ctc_position='nestled',
                                   who_style='stage_name',
                                   what_style='stage_speech' if name else 'stage_action')
            self.page = PageCharacter(name, kind=nvl, ctc='ctc_knot', ctc_position='nestled',
                                      who_style='page_name',
                                      what_style='page_speech' if name else 'page_action')

        def current(self):
            return self.stage if staged_scene() else self.page

        def __call__(self, what, *args, **kwargs):
            if staged_scene():
                if store.nvl_list:
                    nvl_clear()
                store.page_scene = 0
                note_stage_change()
            else:
                store.last_stage_image = None
            return self.current()(what, *args, **kwargs)

        def predict(self, what):
            return self.current().predict(what)

        def __getattr__(self, attribute):
            if attribute in ('name', 'stage', 'page') or attribute.startswith('__'):
                raise AttributeError(attribute)
            return getattr(self.current(), attribute)

    # The speaker's portrait. Every portrait is a rectangular crop of its
    # painting, made in GIMP to one composition (tools/crop-portraits.py), so
    # heads share a scale and eye line; it is shown in an oval that fades at
    # its base, with a soft golden halo. Only the speaker is shown.
    PORTRAIT_OVAL = (224, 280)
    PORTRAIT_POS = {'speaker': (118, 750)}
    CROP_SIZE = (408.0, 466.0)
    PORTRAIT_CROPS = json.loads(renpy.file('portrait-crops.json').read())

    PORTRAIT_PLAN = json.loads(renpy.file('portrait-plan.json').read())

    def portrait_parts(path):
        """(expression, wardrobe) behind an S001-S005 plan path such as
        art/rovel/portraits/tessa-startled-arrival-bright.png; other portrait
        paths are already a single named portrait: (stem, None)."""
        stem = path.rsplit('/', 1)[-1].rsplit('.', 1)[0]
        if not path.startswith('art/rovel/portraits/'):
            return stem, None
        for suffix in ('-bright', '-night', '-ordinary'):
            if stem.endswith(suffix):
                stem = stem[:-len(suffix)]
                break
        for wardrobe in ('arrival-cloak', 'arrival', 'formal', 'working'):
            if stem.endswith('-' + wardrobe):
                return stem[:-len(wardrobe) - 1], wardrobe
        return stem, None

    def portrait_key(path):
        """The old head crop behind a plan path (the interim stand-in)."""
        return portrait_parts(path)[0]

    def painted_portrait_name(path, role):
        """The role-specific painted portrait for a plan path, e.g.
        tessa-startled-arrival-speaking, or None for a named portrait."""
        if not path.startswith('art/rovel/portraits/'):
            return None
        expression, wardrobe = portrait_parts(path)
        mood = PORTRAIT_PLAN['aliases'].get(expression, expression)
        if wardrobe is None:
            wardrobe = PORTRAIT_PLAN['wardrobe'].get(expression.split('-')[0], {}).get(str(current_scene))
        return '-'.join(part for part in (mood, wardrobe, 'speaking' if role == 'speaker' else 'listening') if part)

    def portrait_choice(path, role):
        """The graded portrait to show. A painted portrait named for its role
        faces the right way; until one exists the old head crop stands in."""
        lit = LIT.get('portraits', {})
        for key in (painted_portrait_name(path, role), portrait_key(path)):
            if key and key in lit:
                return key
        return None

    def portrait_ready(face):
        return face is not None and (portrait_key(face['image']) in LIT.get('portraits', {})
                                     or renpy.loadable(face['image']))

    def portrait_source(path, role='speaker'):
        """The portrait graded into the scene's light register and mode."""
        key = portrait_choice(path, role)
        if key:
            return LIT['portraits'][key][current_register()][light_mode()]
        return lighting_art(path)

    def lit_ornament(image):
        """Gilt ornament takes the scene's light too."""
        matrix = frame_light()
        return Transform(image, matrixcolor=matrix) if matrix is not None else image

    def portrait_cameo(face, role='speaker', grade=None, facing=None):
        """The portrait in its oval with a golden halo. `facing` is the direction
        the head should look; by default the speaker looks right, toward the text."""
        w, h = PORTRAIT_OVAL
        key = portrait_choice(face['image'], role) or portrait_key(face['image'])
        want = facing or ('right' if role == 'speaker' else 'left')
        # Only the interim head crops can face the wrong way; painted portraits
        # are named for their role and never need mirroring.
        flip = PORTRAIT_CROPS['facing'].get(key, want) != want
        scale = max(w / CROP_SIZE[0], h / CROP_SIZE[1])
        cw, ch = int(round(CROP_SIZE[0] * scale)), int(round(CROP_SIZE[1] * scale))
        head = Transform(portrait_source(face['image'], role), xysize=(cw, ch), xzoom=(-1.0 if flip else 1.0),
                         xpos=(w - cw) // 2, ypos=(h - ch) // 2)
        return Fixed(Transform(lit_ornament('ui/oval-halo.png'), xpos=-26, ypos=-26),
                     AlphaMask(Fixed(head, xysize=(w, h)), 'ui/oval-mask.png'), xysize=(w, h))

    def shown_stage():
        """The graded painting on screen now, and how far it is lifted."""
        beat = current_rovel_beat()
        if beat:
            image = lit_stage(beat['stage_id'])
            return (image, stage_framing().get('lift', 0)) if image else (None, 0)
        if current_scene > 5 and staging_stage():
            return lighting_art(staging_stage()['image']), stage_framing().get('lift', 0)
        return None, 0

    def _shadow_tint(image, mask):
        r, g, b = (LIT.get('shade', {}).get(image) or {}).get('tint', (0.2, 0.19, 0.18))
        colour = Solid((int(r * 255), int(g * 255), int(b * 255), 255), xysize=(1920, 1080))
        return Transform(AlphaMask(colour, mask), blend='multiply')

    def reading_shade():
        """Behind the text the painting falls softly out of focus (a lens blur
        made per painting by tools/grade-light.py) and into its own shadow
        colour, multiplied so it keeps its hue. A band made for a raised
        painting already starts where the focus falls away on screen."""
        image, lift = shown_stage()
        layers = []
        shade = LIT.get('shade', {}).get(image) if image else None
        if shade:
            layers.append(Transform(shade['soft'], ypos=SOFT_TOP - lift + shade.get('lift', 0)))
            if lift:
                # the raised painting's lower edge fades into the dark beneath it
                layers.append(Transform('ui/edge-fade.png', xsize=1920, ysize=220, ypos=1080 - lift - 220))
        layers.append(_shadow_tint(image, 'ui/reading-shade-mask.png'))
        return Fixed(*layers, xysize=(1920, 1080))

    def controls_pool():
        """Behind the open controls: the painting blurred and deepened in its
        own shadow colour, in a soft pool at the corner."""
        image, lift = shown_stage()
        layers = []
        if image:
            soft = Transform(image, xysize=(1920, 1080), yoffset=-lift, blur=16)
            layers.append(AlphaMask(Fixed(soft, xysize=(1920, 1080)), 'ui/controls-pool-mask.png'))
        layers.append(_shadow_tint(image, 'ui/controls-pool-mask.png'))
        return Fixed(*layers, xysize=(1920, 1080))

    _top_cache = {}

    def stage_text_top(what, who):
        """Long passages grow upward so the last line keeps its place."""
        key = (what, bool(who), persistent.large_text)
        if key not in _top_cache:
            style = 'stage_speech' if who else 'stage_action'
            t = Text(what, style=style, size=text_size(38), xmaximum=STAGE_TEXT_W)
            height = renpy.render(t, STAGE_TEXT_W, 4000, 0, 0).height
            lines = max(1, int(round(height / float(text_size(STAGE_LINE)))))
            _top_cache[key] = STAGE_TEXT_TOP - max(0, lines - 3) * text_size(STAGE_LINE)
        return _top_cache[key]

    def page_ground(light):
        return 'ui/page-' + light + '.webp'

    def page_colors(light):
        if light == 'day':
            return dict(ink=ui_ink, soft=ui_ink_soft, gold=ui_ink_gold,
                        rule='ui/page-rule-ink.png', frame='ui/page-frame-ink.png')
        return dict(ink=ui_ivory, soft=ui_ivory_soft, gold=ui_gold,
                    rule='ui/page-rule-gilt.png', frame='ui/page-frame-gilt.png')

    def split_initial(what):
        """(letter, rest) for an illuminated hanging initial, or (None, what).
        Leading text tags (small caps runs) stay with the rest of the text."""
        i, prefix = 0, ''
        while what.startswith('{', i):
            j = what.find('}', i)
            if j < 0:
                break
            prefix += what[i:j + 1]
            i = j + 1
        if i < len(what) and what[i].isalpha() and what[i].upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            return what[i].upper(), prefix + what[i + 1:]
        return None, what

    # On book pages the speaker sits in the left margin, looking toward the page.
    PAGE_PORTRAIT_POS = {'speaker': (33, 250)}

define narrator = ReaderVoice(None)

init python:
    # Inline illuminated initials, raised on the first line of a page scene.
    # The box is one line tall so the line keeps its height; the tile draws
    # upward into the space above the paragraph, its foot on the first line.
    for _letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        renpy.image('initial_' + _letter, Fixed(
            Transform('ui/initials/' + _letter + '.png', zoom=0.7, ypos=-44),
            xysize=(93, 46)))

style stage_speech:
    font ui_serif
    size 38
    color ui_ivory
    line_spacing 9
    layout "subtitle"
    outlines [(absolute(6), "#0000001c", 0, 1), (absolute(3), "#00000038", 0, 1), (absolute(1), "#0000004d", 0, 0)]

style stage_action is stage_speech:
    font ui_italic
    color ui_ivory_soft

style stage_name:
    font ui_caps
    size 28
    kerning 3.0
    color ui_gold_bright
    outlines [(absolute(4), "#00000030", 0, 1), (absolute(2), "#00000040", 0, 0)]

style page_speech:
    font ui_serif
    size 36
    line_spacing 11
    color ui_ink

style page_action is page_speech:
    font ui_italic

style page_name:
    font ui_caps
    size 25
    kerning 2.6
    text_align 1.0

style page_super:
    font ui_caps
    size 30
    kerning 4.0
    xalign 0.5
    text_align 0.5
    xsize PAGE_W

style page_chapter:
    font ui_caps
    size 24
    kerning 3.6

style page_place:
    font ui_serif
    size 64
    line_spacing -6

style page_time:
    font ui_italic
    size 36

style page_running:
    font ui_caps
    size 21
    kerning 3.0

style controls_button:
    padding (18, 7, 18, 9)
    xalign 1.0
    hover_foreground Transform("ui/controls-underline.png", xalign=1.0, yalign=1.0, xoffset=-6)
    selected_foreground Transform("ui/controls-underline.png", xalign=1.0, yalign=1.0, xoffset=-6)
style controls_button_text:
    font ui_caps
    size 26
    kerning 3.4
    color "#e9e0cfe6"
    hover_color ui_gold_bright
    insensitive_color "#e9e0cf55"
    text_align 1.0
    outlines [(absolute(4), "#00000026", 0, 1), (absolute(2), "#00000040", 0, 0)]

style stage_heading:
    font ui_caps
    size 23
    kerning 3.2
    color ui_gold
    outlines [(absolute(4), "#00000030", 0, 1), (absolute(2), "#00000040", 0, 0)]

# ---------------------------------------------------------------- stage mode

screen say(who, what):
    $ framing = stage_framing()
    $ speaker, listener = stage_faces(who)
    $ heading = first_line_of_scene()
    if framing.get('text'):
        # A quiet line set inside the painting's own shadow.
        $ tx, ty, tw = framing['text']
        add "ui/text-pool.png" pos (tx - 170, ty - 150)
        if heading:
            text scene_heading_line() style "stage_heading" pos (tx, ty - 58)
        text what id "what" pos (tx, ty) xmaximum tw size text_size(38)
    else:
        $ top = stage_text_top(what, who)
        add reading_shade()
        add lit_ornament("ui/reading-hairline.png") pos (330, top - 129)
        if portrait_ready(speaker):
            add portrait_cameo(speaker, 'speaker') pos PORTRAIT_POS['speaker']
        if heading:
            text scene_heading_line() style "stage_heading" pos (STAGE_TEXT_X, top - 100)
        if who:
            text who.lower() id "who" pos (STAGE_TEXT_X, top - 50)
        text what id "what" pos (STAGE_TEXT_X, top) xmaximum STAGE_TEXT_W size text_size(38)
    if persistent.art_descriptions and current_art_description():
        frame:
            background Solid("#0b1014e8")
            xpos 1110 ypos 60 xsize 750 padding (28, 22)
            text current_art_description() size 24 color ui_ivory_soft line_spacing 5 font ui_serif
    use reading_controls('stage')

# The reading controls stay out of the picture: a small gilt sun at the lower
# right opens them, and breathes when something can be looked at more closely.
# Open, they rise over a soft pool of the scene's own shadow, in small
# capitals; the one under the pointer gains an engraved underline. A click
# anywhere else closes them without turning the page.
default controls_open = False

transform controls_rise:
    alpha 0.0 yoffset 12
    easein 0.28 alpha 1.0 yoffset 0

transform controls_breathe:
    alpha 0.25
    block:
        easein 1.4 alpha 0.9
        easeout 1.4 alpha 0.25
        repeat

init python:
    def controls_then(action):
        return [SetVariable('controls_open', False), action]

screen reading_controls(light='stage'):
    zorder 50
    $ closer = closer_here()
    $ ink = light == 'day'
    if controls_open:
        button:
            xysize (1920, 1080)
            background None
            action SetVariable('controls_open', False)
        if not ink and staged_scene():
            add controls_pool()
        vbox at controls_rise:
            style_prefix "controls"
            xalign 1.0 xoffset -52 yalign 1.0 yoffset -96 spacing 0
            $ idle = ui_ink_soft if ink else "#e9e0cfe6"
            $ hover = ui_ink_gold if ink else ui_gold_bright
            $ outlines = [] if ink else [(absolute(4), "#00000026", 0, 1), (absolute(2), "#00000040", 0, 0)]
            textbutton _("Back") action controls_then(Rollback()) text_color idle text_hover_color hover text_outlines outlines
            textbutton _("History") action controls_then(ShowMenu('history')) text_color idle text_hover_color hover text_outlines outlines
            if closer:
                textbutton _("Look closer") id "look_closer" action controls_then(ShowMenu('look_closer')) text_color hover text_hover_color hover text_outlines outlines
            textbutton _("Threads") action (controls_then(ShowMenu('threads')) if available_details() else None) text_color idle text_hover_color hover text_outlines outlines
            textbutton _("Save") action controls_then(ShowMenu('save')) text_color idle text_hover_color hover text_outlines outlines
            textbutton _("Load") action controls_then(ShowMenu('load')) text_color idle text_hover_color hover text_outlines outlines
            textbutton _("Settings") id "open_menu" action controls_then(ShowMenu('preferences')) text_color idle text_hover_color hover text_outlines outlines
    if closer and not controls_open:
        add "ui/controls-glow.png" at controls_breathe pos (1920 - 58 - 48, 1080 - 50 - 48)
    imagebutton:
        id "reading_controls"
        idle Transform(lit_ornament("ui/controls-sun.png"), alpha=(1.0 if (controls_open or closer) else 0.75))
        hover lit_ornament("ui/controls-sun.png")
        pos (1920 - 58 - 22, 1080 - 50 - 22)
        action ToggleVariable('controls_open')
        alt _("Reading controls")

# ----------------------------------------------------------------- page mode

screen nvl(dialogue, items=None):
    $ light = scene_light()
    $ c = page_colors(light)
    add c['frame']
    $ speaker, listener = staging_faces()
    if portrait_ready(speaker):
        add portrait_cameo(speaker, 'speaker') pos PAGE_PORTRAIT_POS['speaker']
    if page_index == 0:
        vbox:
            xpos PAGE_X ypos 108
            text chapter_label() style "page_chapter" color c['gold']
            null height 8
            text scene_place_name() style "page_place" color c['ink']
            if scene_time_name():
                text scene_time_name() style "page_time" color c['soft']
            null height 16
            add c['rule'] xoffset -8
    else:
        text (chapter_label() + '  ·  ' + scene_place_name().lower()) style "page_running" color c['soft'] xpos PAGE_X ypos 84
    vbox:
        xpos PAGE_X ypos (PAGE_FIRST_TOP if page_index == 0 else PAGE_NEXT_TOP)
        spacing PAGE_GAP
        for d in dialogue:
            if is_super_caption(d.what):
                text d.what id d.what_id color c['gold'] size text_size(30) font ui_caps kerning 4.0 xsize PAGE_W text_align 0.5
            elif d.who:
                fixed:
                    xsize PAGE_W yfit True
                    text d.who.lower() id d.who_id style "page_name" color c['gold'] xpos -30 xanchor 1.0 ypos 9 size text_size(25)
                    text d.what id d.what_id style "page_speech" color c['ink'] size text_size(36) xmaximum PAGE_W
            else:
                text d.what id d.what_id style "page_action" color c['soft'] size text_size(36) xmaximum PAGE_W
    use reading_controls(light)

# ------------------------------------------------------- chapter and ending

screen chapter_title(number, title):
    modal True
    $ light = scene_light()
    $ c = page_colors(light)
    add page_ground(light)
    vbox at ui_fade_in(0.9):
        xalign 0.5 yalign 0.44 spacing 0
        text ("chapter " + _ROMAN[number].lower()) style "page_chapter" color c['gold'] xalign 0.5
        null height 22
        text title font ui_serif size 104 color c['ink'] xalign 0.5
        null height 30
        add c['rule'] xalign 0.5
    button:
        id "chapter_continue"
        xysize (1920, 1080)
        background None
        action Return()
    key "dismiss" action Return()
    timer 3.8 action Return()

screen ending_breath():
    modal True
    add Solid("#07090b")
    add "ui/knot.png" at ui_fade_in(2.4) align (0.5, 0.52)
    button:
        id "ending_continue"
        xysize (1920, 1080)
        background None
        action Return()
    key "dismiss" action Return()

screen final_question():
    modal True
    add Solid("#07090b")
    text "Do you wish to save Tessa?" at ui_fade_in(2.6):
        font ui_serif size 72 color ui_ivory align (0.5, 0.44)
    textbutton _("Return to the title") at ui_fade_in(4.5):
        id "ending_title"
        style "caps_button"
        text_color ui_ivory_soft
        text_hover_color ui_gold_bright
        align (0.5, 0.86)
        action MainMenu(confirm=False)
    # Response outcomes are intentionally not fabricated. This is the requested
    # endpoint; no choice promises a continuation that does not exist.
