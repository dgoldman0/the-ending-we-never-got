default current_scene = 0
default current_chapter = 1
default completed_scenes = 0
default source_line = 0
default source_page = 0
default scene_location = ""
default scene_heading = ""
default scene_art = None
default scene_art_alt = ""
default scene_speaker = None
default unlocked_round = 0
default viewed_evidence = set()
default findings = set()
# Legacy fields above remain readable in old saves; discovery uses these sets.
default inspected_details = set()
default followed_connections = set()
default ending_reached = False
default return_to_question = False

init python:
    import json
    source_map = json.loads(renpy.file('source-map.json').read())
    chapter_names = [c[1] for c in source_map['chapters']]
    # Each speaker reads over the painting in illustrated scenes and on the
    # typeset page elsewhere (ui-reading.rpy).
    cast = {name: ReaderVoice(name.title()) for name in source_map['speakers']}

    def art_available():
        return scene_art and renpy.loadable(scene_art)

    def scene_palette():
        # Graphic reading backdrop, not an illustration of a physical location.
        if 'Night' in scene_location or 'Dawn' in scene_location:
            return '#101d26'
        if current_chapter >= 6:
            return '#192b2d'
        return '#263d41'

    def scene_sprites():
        # Retired batch: its faces/poses must not reappear around replacement CGs.
        # New character performances need their own reviewed shot/state coverage.
        return []

    def scene_background(scene, line, page):
        # Legacy background availability only; this is not presentation clearance.
        name, description = None, ''
        if scene == 1:
            if line == 9:
                name = 'chamber-open'
                description = 'An open arch joins a cold modern street to the glaring pale temple. Its threshold meets the circle.'
            elif line < 15 or (line == 15 and page == 0):
                name = 'chamber-open-spill'
                description = 'The grocery bag and split milk carton lie just inside the threshold. The modern street remains visible.'
            else:
                name = 'chamber-closed'
                description = 'The return arch is sealed, newly cracked; the fallen groceries remain beside its threshold. Severe light fills the room.'
        elif scene == 2:
            name = ('apartment-barricaded' if line >= 108 else
                    'apartment-open' if 73 <= line < 106 else 'apartment-closed')
            description = 'A very dark apartment: cold window at left, small candle pool and a discarded ivory dress at the wardrobe.'
            description += {'apartment-open': ' The door is open to the guarded hall.',
                            'apartment-closed': ' The door is closed; the chair remains at the window.',
                            'apartment-barricaded': ' The chair now stands against the closed door.'}[name]
        elif scene == 3:
            name = 'palace-infirmary'
            description = 'Pale insistent daylight across the ward. Beds, curtains and basins leave a clear treatment aisle.'
        elif scene == 4:
            name = 'audience-hall'
            description = 'Harsh light fills the audience hall. Twelve-ray temple banners hang above the ceremonial chair and wounded spectators.'
        elif scene == 5:
            name = 'infirmary-window'
            description = 'A broad infirmary window sill overlooks the convoy. The medical chest is open; the travel bag rests at the far end of the sill.'
        return ('art/backgrounds/' + name + '.png', description) if name else (None, '')


label start:
    $ current_scene = 0
    $ current_chapter = 1
    $ completed_scenes = 0
    $ unlocked_round = 0
    $ viewed_evidence = set()
    $ findings = set()
    $ inspected_details = set()
    $ followed_connections = set()
    $ ending_reached = False
    $ return_to_question = False
    $ page_scene = 0
    $ page_index = 0
    $ last_stage_image = None
    jump s001

label chapter_card(number, title):
    if number == 1:
        return
    window hide
    hide screen story_stage
    $ renpy.transition(ui_scene_change)
    call screen chapter_title(number, title)
    $ last_stage_image = None
    return

label investigation_invitation(number):
    # Old source grouping boundaries no longer interrupt the reading.
    return

label original_ending:
    window hide
    hide screen story_stage
    $ nvl_clear()
    scene black
    with motion(1.8)
    $ ending_reached = True
    $ renpy.block_rollback()
    call screen ending_breath
    $ renpy.transition(motion(1.2))
    call screen final_question
    return

image black = Solid('#07090b')

screen story_stage():
    zorder -5
    if staged_scene():
        add Solid('#0b1014')
        $ beat = current_rovel_beat()
        $ shot = opening_shot()
        if beat:
            $ lift = stage_framing().get('lift', 0)
            fixed:
                yoffset -lift
                use rovel_stage(beat)
            if lift:
                add "ui/edge-fade.png" xsize 1920 ysize 220 ypos (1080 - lift - 220)
                add Solid('#0b1014') ypos (1080 - lift)
        elif opening_assets_available(shot):
            use opening_stage(shot)
        elif composed_scene():
            add lighting_art(composed_scene()) xysize (1920, 1080)
        elif art_available():
            add lighting_art(scene_art) xysize (1920, 1080)
    # Prose-only scenes are read on the typeset page (screen nvl).
