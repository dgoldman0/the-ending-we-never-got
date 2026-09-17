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
    cast = {name: Character(name.title(), who_color='#d9c699') for name in source_map['speakers']}

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
    jump s001

label chapter_card(number, title):
    if number == 1:
        return
    window hide
    hide screen story_stage
    call screen chapter_title(number, title)
    return

label investigation_invitation(number):
    # Old source grouping boundaries no longer interrupt the reading.
    return

label original_ending:
    window hide
    hide screen story_stage
    scene black
    if not persistent.reduced_motion:
        with Dissolve(0.8)
    $ ending_reached = True
    $ renpy.block_rollback()
    call screen ending_breath
    call screen final_question
    return

image black = Solid('#080f13')

screen reading_intro():
    modal True
    use original_backdrop
    add Solid('#baa17a') xpos 260 ypos 305 xsize 70 ysize 2
    vbox:
        xpos 260 ypos 354 xsize 1300 spacing 30
        text "A life interrupted." style "title_text"
        text "Click, Space or Enter to turn the page. Escape opens the menu." style "prose_text"
        text "When a detail stays with you, look closer." font 'fonts/EBGaramond12-Italic.ttf' size 38 color '#d5c8af'
        text "War, bereavement and lasting injury." size 22 color '#a8a799'
        null height 15
        textbutton "Begin" id "begin_reading" action Return() style 'hero_button'

screen chapter_title(number, title):
    modal True
    use original_backdrop
    add Solid('#9e8965') xalign 0.5 ypos 343 xsize 1 ysize 56
    vbox:
        xalign 0.5 ypos 439 spacing 18
        text "[number:02d]" style 'caption_text' xalign 0.5
        text title style 'title_text' xalign 0.5
        null height 72
        textbutton "Continue" id "chapter_continue" action Return() xalign 0.5

screen story_stage():
    zorder -5
    add Solid('#0b1419')
    $ beat = current_rovel_beat()
    $ shot = opening_shot()
    if beat:
        use rovel_stage(beat)
    elif opening_assets_available(shot):
        use opening_stage(shot)
    elif composed_scene():
        add lighting_art(composed_scene()) xysize (1920, 1080)
    elif art_available():
        # Legacy coverage is still being replaced; never put old cutouts on a new CG.
        fixed:
            xsize 1920 ysize 1080 clipping True
            add lighting_art(scene_art) xysize (1920, 1080)
            for sprite, pos in scene_sprites():
                if renpy.loadable('art/sprites/' + sprite + '.png'):
                    add lighting_art('art/sprites/' + sprite + '.png'):
                        xcenter int(1920 * pos) ypos 60
                        xysize ((1320, 1980) if current_scene in (3, 4, 5) or (current_scene == 2 and 90 <= source_line < 101) else (830, 1245))
    else:
        # Honest prose coverage. No substitute portrait or unrelated scene study.
        add Solid('#111b20')
        add Solid('#ac9873') xpos 160 ypos 325 xsize 65 ysize 2
        vbox:
            xpos 160 ypos 390 xsize 1480 spacing 24
            text chapter_names[current_chapter-1] style 'caption_text'
            text scene_location.replace(' · ', '\n') font 'fonts/EBGaramond12-Regular.ttf' size 75 color '#c7c6b9'
    # The scene itself carries place; retain the label in image descriptions.

screen say(who, what):
    use rovel_reading(who,what)
    if persistent.art_descriptions and (art_available() or composed_scene()):
        frame:
            background Solid('#0b1419ed')
            xpos 950 ypos 110 xsize 860 padding (24, 20)
            text current_art_description() size 23 color '#e8dfcf'
    use quick_menu

screen quick_menu():
    zorder 100
    add Solid('#080f13f5') ypos 1018 ysize 62
    textbutton 'Back' xpos 70 ypos 1023 xsize 135 action Rollback() style 'quiet_button'
    textbutton 'History' xpos 218 ypos 1023 xsize 155 action ShowMenu('history') style 'quiet_button'
    textbutton 'Look closer':
        id 'look_closer'
        xpos 390 ypos 1023 xsize 230
        action (ShowMenu('look_closer') if closer_here() else None)
        style 'quiet_button'
    textbutton 'Threads':
        xpos 638 ypos 1023 xsize 175
        action (ShowMenu('threads') if available_details() else None)
        style 'quiet_button'
    textbutton 'Save' xpos 830 ypos 1023 xsize 135 action ShowMenu('save') style 'quiet_button'
    textbutton 'Menu' xpos 986 ypos 1023 xsize 145 action ShowMenu('preferences') style 'quiet_button'
    textbutton 'Continue  ›':
        id 'reading_continue'
        xpos 1630 ypos 1023 xsize 245
        action Return()
        style 'quiet_button'

screen ending_breath():
    modal True
    add Solid('#080f13')
    # A separate interaction absorbs the advance that follows the final scene.
    textbutton 'Continue' id 'ending_continue' action Return() xalign 0.5 yalign 0.86

screen final_question():
    modal True
    add Solid('#080f13')
    text 'Do you wish to save Tessa?':
        font 'fonts/CharisSIL-Regular.ttf'
        size 62
        xalign 0.5 yalign 0.45
    textbutton 'Return to title' id 'ending_title' action MainMenu(confirm=False):
        xalign 0.5 yalign 0.87
    # Response outcomes are intentionally not fabricated. This is the requested
    # endpoint; no choice promises a continuation that does not exist.
