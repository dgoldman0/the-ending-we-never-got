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
        # Dialogue portraits, not frozen depictions of narrated physical action.
        # Each tuple is a reviewed period/pose/light state and portrait position.
        if not scene_speaker:
            return []
        if current_scene == 1 and source_line >= 19:
            tessa = 'tessa-phone' if source_line >= 52 else 'tessa-arrival'
            result = [(tessa + '-bright', .27)]
            if source_line >= 29:
                result.append(('senn-ceremonial-bright', .72))
            return result
        if current_scene == 2 and 75 <= source_line <= 104:
            tessa = 'tessa-cloaked' if source_line < 101 else 'tessa-phone'
            return [(tessa + '-dark', .27), ('mara-indoor-dark', .72)]
        if current_scene == 3:
            return [('tessa-first-treatment-ordinary', .27), ('iven-treatment-ordinary', .72)]
        if current_scene == 4 and 187 <= source_line <= 204:
            return [('tessa-ceremony-bright', .27), ('senn-ceremonial-bright', .72)]
        if current_scene == 4 and source_line == 211:
            return [('iven-treatment-bright', .53)]
        if current_scene == 5:
            return [('iven-treatment-ordinary', .27), ('tessa-ceremony-ordinary', .72)]
        return []

    def scene_background(scene, line, page):
        # A reviewed whitelist. No fallback to old studies or the wrong period.
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

    def mark_evidence(eid):
        viewed_evidence.add(eid)
        # Investigation edits occur inside a menu interaction. Preserve them
        # when loading a save made before that interaction returns to script.
        renpy.retain_after_load()

    def resolve_case(case_id, answer):
        case = cases[case_id]
        if answer == case['answer']:
            findings.add(case_id)
            renpy.retain_after_load()
        # A Function screen action must return None: a bool would end the
        # interaction and eject the reader before feedback can be displayed.

label start:
    $ current_scene = 0
    $ current_chapter = 1
    $ completed_scenes = 0
    $ unlocked_round = 0
    $ viewed_evidence = set()
    $ findings = set()
    $ ending_reached = False
    $ return_to_question = False
    call screen reading_intro
    jump s001

label chapter_card(number, title):
    window hide
    hide screen story_stage
    call screen chapter_title(number, title)
    return

label investigation_invitation(number):
    window hide
    hide screen story_stage
    call screen inquiry_invitation(number)
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
    add Solid('#101f26')
    vbox:
        xpos 330 ypos 215 xsize 1260 spacing 34
        text "THE ORIGINAL TIMELINE" style "caption_text"
        text "A life interrupted." style "title_text"
        text "Read at your own pace. Click, press Space or Enter to advance. Mouse wheel up or Page Up revisits earlier lines; Esc opens the menu." style "prose_text"
        text "Between chapters, you can examine what you have seen. Investigation belongs to you, the reader. It does not change what Tessa or her companions know, and time does not pass while you investigate." style "prose_text"
        text "The story includes war, bereavement and lasting injury." color '#aabeba'
        textbutton "Begin" id "begin_reading" action Return()

screen chapter_title(number, title):
    modal True
    add Solid('#101f26')
    vbox:
        xalign 0.5 yalign 0.45 spacing 22
        text "CHAPTER [number:02d]" style 'caption_text' xalign 0.5
        text title style 'title_text' xalign 0.5
        null height 45
        textbutton "Continue" id "chapter_continue" action Return() xalign 0.5

screen story_stage():
    zorder -5
    add Solid('#0e1c23')
    if art_available():
        fixed:
            xpos 190 ypos 76 xsize 1540 ysize 700
            clipping True
            add scene_art xysize (1540, 867) ypos -62
            for sprite, pos in scene_sprites():
                if renpy.loadable('art/sprites/' + sprite + '.png'):
                    add ('art/sprites/' + sprite + '.png'):
                        xcenter int(1540 * pos) ypos 50
                        # Close portraits keep treatment and sleeve-grip hands
                        # outside the frame; these are not action tableaux.
                        xysize ((1240, 1860) if current_scene in (3, 4, 5) or (current_scene == 2 and 90 <= source_line < 101) else (690, 1035))
    else:
        add Solid(scene_palette()) xpos 100 ypos 110 xsize 1720 ysize 610
        add Solid('#78968b') xpos 150 ypos 165 xsize 3 ysize 68
        vbox:
            xpos 195 ypos 168 xsize 1450 spacing 23
            text chapter_names[current_chapter-1].upper() style 'caption_text'
            text scene_location.replace(' · ', '\n'):
                font 'fonts/CharisSIL-Regular.ttf'
                size 48
                color '#d8dfd3'
    text "[current_chapter:02d]  /  [chapter_names[current_chapter-1]]" xpos 100 ypos 29 style 'caption_text'
    if art_available():
        text scene_location xpos 100 ypos 784 style 'caption_text'

screen say(who, what):
    style_prefix 'say'
    window:
        id 'window'
        background Solid('#0e1c23')
        xpos 100 ypos 826 xsize 1720 ysize 200
        if who:
            text who id 'who' xpos 36 ypos 3 size 25 color '#d9c699' font 'fonts/ClearSans-Medium.ttf'
        text what:
            id 'what'
            xpos 36 ypos (44 if who else 15)
            xsize 1620
            size (36 if persistent.large_text else 30)
            font 'fonts/CharisSIL-Regular.ttf'
            line_spacing 7
    if art_available() and persistent.art_descriptions:
        frame:
            background Solid('#0e1c23ef')
            xpos 360 ypos 642 xsize 1200 padding (20, 14)
            text scene_art_alt size 24
    use quick_menu

screen quick_menu():
    zorder 100
    hbox:
        xpos 120 ypos 1026 spacing 12
        textbutton 'Back' action Rollback() style 'quiet_button'
        textbutton 'History' action ShowMenu('history') style 'quiet_button'
        textbutton 'Investigate' action ShowMenu('investigation') sensitive unlocked_round > 0 style 'quiet_button'
        textbutton 'Save' action ShowMenu('save') style 'quiet_button'
        textbutton 'Load' action ShowMenu('load') style 'quiet_button'
        textbutton 'Settings' action ShowMenu('preferences') style 'quiet_button'
    text 'CLICK / SPACE TO CONTINUE' xpos 1480 ypos 1041 size 18 color '#8fa7a5'

style quiet_button is button:
    background None
    hover_background Solid('#233940')
    padding (15, 7)
style quiet_button_text is button_text:
    size 23

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
