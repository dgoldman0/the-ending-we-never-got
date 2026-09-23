# Shared visual language for reading, pages, menus and discovery.
# Type is EB Garamond throughout: roman for speech, italic for stage action,
# true small caps for names and labels. Line work is a thin gold thread drawn
# in code (tools/build-ui-assets.py); there are no framed panels.

define ui_serif = "fonts/EBGaramond12-Regular.ttf"
define ui_italic = "fonts/EBGaramond12-Italic.ttf"
define ui_caps = "fonts/EBGaramondSC12-Regular.ttf"

define ui_ivory = "#eee6d6"
define ui_ivory_soft = "#d9cfbb"
define ui_gold = "#cdb076"
define ui_gold_bright = "#e7cf97"
define ui_dim = "#9f988a"
define ui_ink = "#2b2621"
define ui_ink_soft = "#5b5046"
define ui_ink_gold = "#8a6334"

default persistent.large_text = False
default persistent.reduced_motion = False
default persistent.art_descriptions = False

init -2 python:
    import re

    # Screenplay capitals (character introductions, written notices, the
    # phone screen) are set in true small caps. Every word is preserved;
    # only the letterforms change. A SUPER title becomes a time caption.
    _CAPS_RUN = re.compile(r"(?<![\w{\[])([A-Z][A-Z’'\-]+(?:[ \t]+[A-Z][A-Z’'\-]+)*)(?![a-z])")

    def _small_caps(match):
        run = match.group(1)
        if len(re.sub(r"[^A-Z]", "", run)) < 2:
            return run
        return "{font=" + ui_caps + "}" + run.lower() + "{/font}"

    _OPEN_DOUBLE = re.compile(r'(^|[\s(\[—])"')
    _OPEN_SINGLE = re.compile(r"(^|[\s(\[—])'")

    def typeset(text):
        """Screenplay typewriter marks become book punctuation."""
        text = text.replace(' -- ', '—').replace('--', '—')
        text = _OPEN_DOUBLE.sub(r'\1“', text).replace('"', '”')
        text = re.sub(r"(\w)'(\w)", r'\1’\2', text)
        text = _OPEN_SINGLE.sub(r'\1‘', text).replace("'", '’')
        return text

    def reading_text_filter(text):
        text = typeset(text)
        if text.startswith("SUPER: "):
            return "{#super}" + _CAPS_RUN.sub(_small_caps, text[7:])
        text = _CAPS_RUN.sub(_small_caps, text)
        return with_initial(text)

    _INITIAL_TAG = re.compile(r"\{image=initial_([A-Z])\}\{alt\}[A-Z]\{/alt\}")

    def plain_initial(text):
        """The text with its illuminated initial back as an ordinary letter."""
        return _INITIAL_TAG.sub(r"\1", text)

    def with_initial(text):
        """A scene read on the page opens with an illuminated initial: the
        first letter becomes a raised gilt capital set inline, and the letter
        itself stays in the text for self-voicing (alt tag) and history."""
        try:
            opening = (current_scene > 0 and not source_page and scene_speaker is None
                       and first_line_of_scene() and not staged_scene())
        except Exception:
            return text
        if not opening:
            return text
        letter, rest = split_initial(text)
        if not letter:
            return text
        return '{image=initial_' + letter + '}{alt}' + letter + '{/alt}' + rest

    def is_super_caption(what):
        return what.startswith("{#super}")

    def motion(duration):
        """A dissolve that collapses to a near cut under Reduced motion."""
        def transition(old_widget=None, new_widget=None):
            return Dissolve(0.06 if persistent.reduced_motion else duration)(
                old_widget=old_widget, new_widget=new_widget)
        return transition

    def text_size(standard):
        return int(round(standard * (1.14 if persistent.large_text else 1.0)))

define config.say_menu_text_filter = reading_text_filter

define ui_scene_change = motion(0.6)
define ui_page_turn = motion(0.45)
define ui_menu_fade = motion(0.22)

define config.enter_transition = ui_menu_fade
define config.exit_transition = ui_menu_fade
define config.intra_transition = motion(0.16)
define config.after_load_transition = ui_scene_change
define config.end_game_transition = motion(0.8)
define config.game_main_transition = motion(0.6)

# Text is revealed with a soft ink-like dissolve rather than typed out.
define config.default_textshader = "dissolve"
define config.default_text_cps = 52

# The reading knot that marks a finished line.
image ctc_knot:
    "ui/knot-small.png"
    yoffset 4
    alpha 0.0
    easein 0.35 alpha 1.0
    block:
        easein 1.1 alpha 0.45
        easeout 1.1 alpha 1.0
        repeat

transform ui_fade_in(t=0.35):
    alpha 0.0
    easein (0.05 if persistent.reduced_motion else t) alpha 1.0

transform ui_caption_life:
    alpha 0.0
    pause 0.4
    easein (0.05 if persistent.reduced_motion else 0.9) alpha 1.0
    pause 4.2
    easeout (0.05 if persistent.reduced_motion else 1.4) alpha 0.0

transform ui_hover_glow:
    on idle:
        easein 0.2 alpha 0.62
    on hover, selected_idle, selected_hover:
        easein 0.2 alpha 1.0
    on insensitive:
        easein 0.2 alpha 0.32

style default:
    font ui_serif
    size 30
    color ui_ivory
    layout "tex"

style caps_text:
    font ui_caps
    size 22
    color ui_gold
    kerning 2.4

style caps_button:
    background None
    padding (10, 6)
    focus_mask None
style caps_button_text:
    font ui_caps
    size 23
    kerning 2.4
    color ui_ivory
    hover_color ui_gold_bright
    selected_color ui_gold
    selected_hover_color ui_gold_bright
    insensitive_color "#7d776c"

style serif_button:
    background None
    padding (8, 6)
style serif_button_text:
    font ui_serif
    size 40
    color ui_ivory
    hover_color ui_gold_bright
    selected_color ui_gold
    insensitive_color "#7d776c"

style bar:
    ysize 22
    left_bar Frame(Solid(ui_gold), 0, 0)
    right_bar Frame(Solid("#3a3e40"), 0, 0)
    thumb Solid(ui_gold_bright, xsize=4, ysize=22)
    thumb_offset 2
    left_gutter 0
    right_gutter 0
    bar_vertical False

style vscrollbar:
    xsize 3
    base_bar Solid("#2c3134")
    thumb Solid(ui_gold)
    unscrollable "hide"
