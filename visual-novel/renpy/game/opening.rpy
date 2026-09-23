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
            if 90 <= source_line <= 99:
                return opening_cg('blocked-doorway', 'Mara has set down the second plate and blocks the doorway. Tessa holds the candle in her left hand and phone in her right. The guard remains in the hall.',
                                  {'TESSA':(92,1010,820),'MARA':(1010,1010,820)})
            if source_line in (101,103):
                return opening_cg('cloak-discarded', 'The candle is back on the table. Tessa has dropped the cloak at Mara’s feet; Mara looks toward the hall guard instead of answering.',
                                  {'TESSA':(92,560,730)}, reading=(52,715,490))
            if source_line == 106:
                return dict(image=OPENING_ROOT+'bg/apartment-locked.png',
                            actors=[opening_actor('tessa-refusal-night',660,65)], anchors={},
                            alt='Mara and the cloak have gone. The door has shut. Tessa stands alone, still holding the phone; both supper plates remain untouched.')
            if source_line == 108:
                return opening_cg('chair-barricade', 'Tessa pushes the window chair against the locked door. Her dead phone now lies flat on the table. The other chair stays at the table.', reading=(95,565,700))
            if source_line in (110,112):
                return opening_cg('drawing-letter' if source_line == 110 else 'drawing-restart',
                                  'With her healthy right hand, Tessa draws on the reverse of the welcome letter. A small tear interrupts the kitchen; she starts her mother’s chair in a clean corner. The dead phone lies beside the paper.', reading=(96,575,650))
        if current_scene == 3:
            if source_line == 116:
                return opening_cg('ward-entrance', 'Mara leads Tessa through the occupied ward. At the far end a porter removes a name card and closes a curtain. Iven and the older healer tend Olan beside them.')
            if source_line in (118,120):
                return opening_cg('blue-healing', 'Iven supports Olan’s injured right hand. Blue healing closes the missing-finger edges while the dark branching discoloration passes the ink boundary toward his elbow. His left hand grips the bed rail.')
            if 122 <= source_line <= 140:
                return opening_cg('ward-standing-unlit' if source_line < 127 else 'ward-standing-light',
                                  'Tessa stands in the aisle beside Olan’s bed, with Iven beside her. The priest gestures from behind; the older healer waits across the bed. '+('Tessa has not formed the light yet.' if source_line < 127 else 'A small white light trembles between her hands. Olan extends his injured right hand toward its edge.'),
                                  {'PRIEST':(92,1010,760),'TESSA':(92,1010,820),
                                   'IVEN':(620,1010,820),'OLAN':(1010,1010,820)})
            if source_line in (143,145,147):
                return opening_cg('first-purification', 'Now seated beside Iven, Tessa holds white light over Olan’s wrist. Cleared skin reaches Iven’s fingertips; discoloration remains nearer the elbow.',
                                  {'OLAN':(1010,1010,820)})
            if source_line == 150:
                return opening_cg('last-patch', 'Olan has turned his arm. Tessa works back toward the last dark patch beside the wound; the rest of the arm is clear.')
            if source_line in (152,154,157):
                return opening_cg('purification-cleared', 'The corruption is gone. Tessa’s light lingers over the two missing fingers. She looks to Iven; the older healer holds the fresh dressing ready.',
                                  {'TESSA':(92,1010,820),'IVEN':(720,1010,820)})
            if source_line == 160:
                return opening_cg('rested-hand', 'Olan’s injured right hand rests on the blanket, freshly dressed. The remaining fingers have relaxed. The corruption is gone; the missing fingers have not returned.', reading=(96,355,650))
            if source_line in (162,164,167,169):
                return opening_cg('treatment-pause', 'A mother calls from the next row beside her awake daughter. Tessa leans forward to rise; Iven is still beside her and asks her to wait. No light remains in her hands.',
                                  {'MOTHER':(860,1010,820),'IVEN':(630,1010,820)})
            if source_line == 172:
                return opening_cg('after-first-treatment', 'Tessa sits with the cup of water untouched while Olan falls asleep. Iven has gone to the mother and daughter in the next row. The arm is clear; the missing fingers remain dressed.')
        return None

    def opening_assets_available(shot):
        return shot and renpy.loadable(shot['image']) and all(renpy.loadable(a['image']) for a in shot['actors'])

screen opening_stage(shot):
    add lighting_art(shot['image']) xysize (1920,1080)
    for actor in shot['actors']:
        add lighting_art(actor['image']):
            xpos actor['x'] ypos actor['y']
            xysize (actor['w'],actor['h'])
