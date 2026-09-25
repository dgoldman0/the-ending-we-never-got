init offset = -2
init python:
    gui.init(1920, 1080)

define config.name = "The Ending We Never Got"
define config.version = "0.5.0-dev"
define config.check_conflicting_properties = True
define config.save_directory = "the-ending-we-never-got-original-v1"
define config.window = "auto"
define _game_menu_screen = "preferences"
define config.main_menu_music = None
define config.window_show_transition = None
define config.window_hide_transition = None
define config.has_sound = False
define config.has_music = False
define config.has_voice = False
define config.history_length = 250
define config.rollback_length = 200
define config.default_fullscreen = False
define config.default_afm_time = 15
# Skipping moves only through text already read (Ctrl or the Skip setting).
define config.allow_skipping = True

init python:
    # Skipping must never run on while the reader is elsewhere. Ren'Py binds
    # Tab to "toggle skip"; on Linux, leaving fullscreen with Alt+Tab can
    # deliver that Tab without the Alt, so the game skipped through every read
    # line while the reader worked in another window. Skipping stays on Ctrl
    # (held) and in Settings; Tab no longer toggles it. And whenever the game
    # window loses focus, skipping and auto-forward stop.
    config.keymap['toggle_skip'] = []

    def _stop_when_unfocused():
        interface = renpy.display.interface
        if interface is None:
            return
        if not (interface.keyboard_focused and interface.mouse_focused):
            if renpy.config.skipping:
                renpy.config.skipping = None
                renpy.restart_interaction()
            if _preferences.afm_enable:
                _preferences.afm_enable = False
                renpy.restart_interaction()

    config.periodic_callbacks.append(_stop_when_unfocused)
define config.thumbnail_width = 384
define config.thumbnail_height = 216
define build.name = "TheEndingWeNeverGot"
define build.version = "0.5.0-dev"

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
    # Painted portraits and their crops are grading sources; the game shows
    # the graded files in art/lit/.
    build.classify('game/art/portraits/**', None)
    build.classify('game/art/cast/**', None)
    build.classify('game/review-portraits.rpy', None)
    build.classify('game/review-portraits.rpyc', None)
    build.classify('game/tour.rpy', None)
    build.classify('game/tour.rpyc', None)
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
        build.classify('game/art/base/rovel/**', None)

    _configure_rovel_distribution()
