init offset = -2
init python:
    gui.init(1920, 1080)

define config.name = "The Ending We Never Got"
define config.version = "0.4.0-dev"
define config.check_conflicting_properties = True
define config.save_directory = "the-ending-we-never-got-original-v1"
define config.window = "auto"
define _game_menu_screen = "preferences"
define config.window_show_transition = None
define config.window_hide_transition = None
define config.enter_transition = None
define config.exit_transition = None
define config.end_game_transition = None
define config.has_sound = False
define config.has_music = False
define config.has_voice = False
define config.history_length = 250
define config.rollback_length = 200
define config.default_fullscreen = False
define config.default_text_cps = 0
define config.default_afm_time = 15
define config.allow_skipping = False
define config.thumbnail_width = 384
define config.thumbnail_height = 216
define build.name = "TheEndingWeNeverGot"
define build.version = "0.4.0-dev"

init python:
    # Only source-mapped opening art enters distribution; working variants stay local.
    import json
    opening_distribution_assets = json.loads(renpy.file('opening-assets.json').read())
    # Classification also controls directory traversal. Keep parent directories
    # before the deny rule, or the builder never reaches the allowed files.
    for directory in sorted({asset.rsplit('/', 1)[0] for asset in opening_distribution_assets}):
        build.classify('game/' + directory + '/', 'all')
    for asset in opening_distribution_assets:
        build.classify('game/' + asset, 'all')
    build.classify('game/art/opening/**', None)
    build.classify('game/art/sprites/**', None)
    build.classify('game/testcases.rpy', None)
    build.classify('game/testcases.rpyc', None)
    build.classify('game/rovel-review.rpy', None)
    build.classify('game/rovel-review.rpyc', None)
    build.classify('**/test-output/**', None)
    build.classify('**/saves/**', None)
    build.classify('review/**', None)
    build.classify('QA.md', None)
    build.classify('README.md', None)
    # Build patterns use first match; license exceptions precede exclusions.
    build.classify('game/fonts/*LICENSE*', 'all')
    build.classify('game/fonts/*NOTICE*', 'all')
    build.classify('game/fonts/Apache-2.0.txt', 'all')
    build.classify('**/*.txt', None)

init 20 python:
    def _configure_rovel_distribution():
        # This runs after descriptor/discovery/lighting initialization. Keep all
        # temporary names local: init Python otherwise shares the story store.
        required = set(rovel_required_assets())
        required.update(item['image'] for item in detail_views.values())
        required.update(path for path in renpy.list_files()
                        if path.startswith('art/rovel/ui/')
                        and path.lower().endswith(('.png', '.svg', '.webp')))
        required = {path for path in required if path.startswith('art/rovel/')}
        required.update(LIGHTING_VARIANTS[path] for path in tuple(required)
                        if path in LIGHTING_VARIANTS)
        directories = set()
        for path in required:
            pieces = path.split('/')
            directories.update('/'.join(pieces[:count]) for count in range(1, len(pieces)))
        # Directory traversal and first-match classification both matter. Only
        # referenced scene/portrait/detail files and runtime UI exports enter the
        # package; unused variants and editable masters stay outside it.
        for directory in sorted(directories, key=lambda path: (path.count('/'), path)):
            build.classify('game/' + directory + '/', 'all')
        for path in sorted(required):
            build.classify('game/' + path, 'all')
        build.classify('game/art/rovel/**', None)
        build.classify('game/art/softened/rovel/**', None)

    _configure_rovel_distribution()

default persistent.large_text = False
default persistent.reduced_motion = False
default persistent.art_descriptions = False

style default:
    font "fonts/ClearSans-Regular.ttf"
    size 28
    color "#ecede5"

style text:
    line_spacing 7

style button:
    background Solid("#1c3034")
    hover_background Solid("#355056")
    selected_background Solid("#4b6465")
    padding (22, 13)

style button_text:
    font "fonts/ClearSans-Regular.ttf"
    color "#d8e1dc"
    hover_color "#ffffff"
    selected_color "#ffffff"
    insensitive_color "#687779"
    size 28

style title_text:
    font "fonts/CharisSIL-Regular.ttf"
    size 72
    color "#f0eee3"

style prose_text:
    font "fonts/CharisSIL-Regular.ttf"
    size 32
    color "#efeee4"
    line_spacing 10

style caption_text:
    font "fonts/ClearSans-Medium.ttf"
    size 22
    color "#aabeba"
    kerning 1.2

style bar:
    ysize 16
    left_bar Solid("#bdcfbd")
    right_bar Solid("#35494b")
    thumb Solid("#eee7cd", xsize=24, ysize=30)
    thumb_offset 12

style vscrollbar:
    xsize 10
    base_bar Solid("#22383c")
    thumb Solid("#92a7a2")

style scrollbar:
    ysize 10
    base_bar Solid("#22383c")
    thumb Solid("#92a7a2")
