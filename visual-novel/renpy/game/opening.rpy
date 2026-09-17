# Beat-specific staging. Source text remains generated from the screenplay.
init python:
    OPENING_ROOT = 'art/opening/'

    def opening_actor(name, x, y=75, width=700, height=1050):
        return dict(image=OPENING_ROOT+'sprites/'+name+'.png', x=x, y=y, w=width, h=height)

    def opening_cg(name, alt, anchors=None, reading=None):
        return dict(image=OPENING_ROOT+'cg/'+name+'.png', actors=[], anchors=anchors or {},
                    alt=alt, reading=reading)

    def opening_shot():
        if current_scene == 1:
            if source_line == 9:
                return opening_cg('arrival', 'Tessa steps across a modern store threshold into the glaring temple, carrying her groceries and phone. Kneeling strangers watch. The scholar stands at a separate lever station across the room, leaving the arch clear.')
            if source_line == 11:
                return opening_cg('milk-impact', 'The paperboard carton has split at its bottom corner. Milk connects the tear to the spill over the circle and Tessa’s sneakers. Her bag lies beside her at the threshold.')
            if source_line == 13:
                return opening_cg('phone-message', 'In Tessa’s right hand, her green-cased phone shows her mother’s message asking about the milk. The fallen groceries and modern sidewalk remain beyond it.')
            if source_line == 15 and source_page == 0:
                return opening_cg('attempted-return', 'Tessa runs back toward the arch, reaching for the modern store as it twists away. Her groceries stay at the landing point; the scholar reaches for his remote lever.')
            if source_line in (15,17,19):
                return opening_cg('closure', 'Tessa reaches the sealed stone with her left palm, phone in her right hand. The scholar holds the lever fully down in its separate bay. Cracks spread across the arch.',
                                  {'TESSA':(92,1010,820)})
            if source_line in (22,24):
                return opening_cg('pleading-mother', 'A worried mother catches Senn’s sleeve. A guard approaches her while two porters carry a patient biting a folded cloth through the gallery.',
                                  {'WOMAN':(92,1010,820)})
            if source_line == 27:
                return opening_cg('woman-release', 'The guard guides the mother aside. She has released Senn’s sleeve; the injured patient passes behind them on a stretcher.')
            if 29 <= source_line <= 50:
                tessa = 'tessa-refusal-bright' if source_line in (40,43,46,49) else 'tessa-question-bright'
                background = 'arch-guards-raised' if source_line < 35 else 'arch-conversation'
                return dict(image=OPENING_ROOT+'bg/'+background+'.png',
                            actors=[opening_actor(tessa,100), opening_actor('senn-speaking-bright',1120,60)],
                            anchors={'TESSA':(92,1010,820),'SENN':(1010,1010,820)},
                            alt='Tessa faces Senn near the sealed arch. Both remain visible through their exchange. The soldiers bar the approach to the scholar; their shields '+('are raised.' if source_line < 35 else 'have lowered, but the men stay in place.'))
            if source_line in (52,54,57):
                tessa = 'tessa-phone-bright' if source_line == 52 else 'tessa-question-bright'
                return dict(image=OPENING_ROOT+'bg/arch-conversation.png',
                            actors=[opening_actor('mara-cloak-corrected-bright',780,140,620,930),
                                    opening_actor('senn-speaking-bright',1280,70,620,930),
                                    opening_actor(tessa,50,75,700,1050)],
                            anchors={'TESSA':(92,1010,820),'SENN':(1010,1010,820)},
                            alt='Tessa retries the call, then questions Senn’s promise. Mara has approached holding the folded gray cloak; she has not put it on Tessa yet.')
            if source_line in (60,62):
                return opening_cg('stretcher-passes', 'Mara guides Tessa aside by the upper arm while carrying the folded cloak. Porters pass behind them. The crowd gathers at the sealed arch; Tessa appeals to Senn.',
                                  {'TESSA':(92,1010,820)})
            if source_line == 65:
                return opening_cg('unanswered-cloak', 'Mara settles the gray cloak on Tessa’s shoulders. Tessa waits with her phone in her hands while Senn turns away toward the scholar.')
        if current_scene == 2:
            if source_line in (69,71):
                return opening_cg('apartment-window', 'Tessa stands on the window chair, raising her phone toward the night sky. The ivory dress lies discarded below the wardrobe. Carts crowd the distant infirmary beneath an enormous winged silhouette.',
                                  reading=(800,500,950))
            if 73 <= source_line <= 88:
                return dict(image=OPENING_ROOT+'bg/apartment-open.png',
                            actors=[opening_actor('tessa-cloaked-night',70),opening_actor('mara-supper-night',1100,40)],
                            anchors={'TESSA':(92,1010,820),'MARA':(1010,1010,820)},
                            alt='Tessa has climbed down from the window chair. Mara stands near the open door holding a covered supper plate. The hall guard remains beyond her.')
        return None

    def opening_ready(shot):
        return shot and renpy.loadable(shot['image']) and all(renpy.loadable(a['image']) for a in shot['actors'])

    def dialogue_position(who):
        shot = opening_shot()
        if shot and scene_speaker in shot['anchors']:
            return shot['anchors'][scene_speaker]
        # This general treatment will be replaced by shot-specific anchors as
        # other scenes receive their actual cast and compositions.
        if scene_speaker in ('SENN','MARA','IVEN','LUCAN','OLAN'):
            return (1010,1010,820)
        return (92,1010,820)

screen opening_stage(shot):
    add shot['image'] xysize (1920,1080)
    for actor in shot['actors']:
        add actor['image']:
            xpos actor['x'] ypos actor['y']
            xysize (actor['w'],actor['h'])

screen composed_reading(who,what):
    if who:
        $ bx,by,bw = dialogue_position(who)
        window:
            id 'window'
            xpos bx ypos by yanchor 1.0 xsize bw yminimum 155
            background Frame('art/opening/ui/speech.png',55,45,55,45)
            padding (43,26,43,24)
            vbox:
                spacing 12
                text who id 'who' font 'fonts/ClearSans-Medium.ttf' size 21 color '#e4c897' kerning 1.8
                text what id 'what' font 'fonts/CharisSIL-Regular.ttf' size (36 if persistent.large_text else 32) color '#f3e9d6' line_spacing 5 xsize (bw-86)
    else:
        $ shot = opening_shot()
        $ reading_x,reading_y,reading_w = (shot.get('reading') if shot and shot.get('reading') else ((96,575,650) if current_scene == 2 and source_line >= 110 else (300,1010,1320)))
        $ dark_reading = current_scene == 2
        window:
            id 'window'
            xpos reading_x ypos reading_y yanchor 1.0 xsize reading_w
            background Frame('art/opening/ui/speech.png' if dark_reading else 'art/opening/ui/narration.png',55,45,55,45)
            padding (48,32)
            text what id 'what' font 'fonts/CharisSIL-Regular.ttf' size (35 if persistent.large_text else 31) color ('#e2d8c8' if dark_reading else '#292a29') line_spacing 7 xsize (reading_w-96)
