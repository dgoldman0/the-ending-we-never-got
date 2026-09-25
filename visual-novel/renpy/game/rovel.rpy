# Authored presentation, independent of the generated screenplay and its cursor.
# Asset presence is not an art/experience clearance. Existing opening images are
# rejected working components until individually reassessed in the new sequence.
init python:
    import copy

    def _build_rovel_plan():
        # Ren'Py init Python shares its store with the game. Keep all temporary
        # names (especially cast) local; only return the completed descriptors.
        ROVEL_GRADES = {1: 'bright', 2: 'night', 3: 'ordinary', 4: 'bright', 5: 'ordinary'}
        def _rovel_actor(name, x, y=75, width=700, height=1050):
            return dict(image='art/opening/sprites/' + name + '.png',
                        x=x, y=y, w=width, h=height)

        def _rovel_stage(image, alt, actors=()):
            return dict(image=image, actors=list(actors), alt=alt,
                        review='unreviewed-in-rovel')

        def _rovel_old_cg(name, alt):
            return _rovel_stage('art/opening/cg/' + name + '.png', alt)

        def _rovel_new_cg(name, alt):
            return _rovel_stage('art/rovel/cg/' + name + '.png', alt)

        ROVEL_STAGES = {
            'arrival': _rovel_old_cg('arrival', 'Tessa steps from the ordinary modern sidewalk onto temple stone just inside the arch. Her grocery bag and phone are still in her hands; the separate lever bay leaves her return route clear.'),
            'milk': _rovel_old_cg('milk-impact', 'The fallen carton splits beside Tessa’s sneakers at the landing point. Milk runs from its rupture across the circle. The grocery bag remains at the threshold.'),
            'message': _rovel_old_cg('phone-message', 'Tessa’s phone displays her mother’s request for milk; the modern street remains visible through the arch.'),
            'return': _rovel_old_cg('attempted-return', 'Tessa runs for the arch as the modern street twists out of alignment. Her groceries remain at the threshold; the scholar reaches for the lever in the separate operating bay.'),
            'closure': _rovel_old_cg('closure', 'Tessa reaches the sealed arch with the phone still in her hand. The scholar holds the remote lever down. New cracks surround the lost opening.'),
            'petition': _rovel_old_cg('pleading-mother', 'A woman catches Senn’s sleeve to ask for her daughter. A guard approaches while porters carry a patient through the gallery.'),
            'release': _rovel_old_cg('woman-release', 'The guard draws the woman aside; the patient passes on a stretcher, biting a folded cloth.'),
            'stretcher': _rovel_old_cg('stretcher-passes', 'Mara draws Tessa aside by the arm to let a stretcher pass. Mara still carries the cloak; the crowd gathers at the sealed arch.'),
            'cloak': _rovel_old_cg('unanswered-cloak', 'Senn turns toward the scholar while Tessa waits for an answer. Mara settles the cloak around Tessa.'),
            'night-window': _rovel_old_cg('apartment-window', 'Tessa stands on the chair at the open window, raising her phone. The offered dress lies on the floor. Infirmary carts and a huge winged silhouette are outside.'),
            'night-blocked': _rovel_old_cg('blocked-doorway', 'Mara has set down the second supper plate and blocks Tessa’s way into the hall. Tessa carries the candle; a guard waits outside.'),
            'night-cloak': _rovel_old_cg('cloak-discarded', 'Tessa has returned the candle to the table and dropped the cloak at Mara’s feet. Mara looks toward the hall guard.'),
            'night-chair': _rovel_old_cg('chair-barricade', 'Tessa drags the window chair against the locked door. The dead phone lies on the table; Mara and the cloak have gone.'),
            'night-drawing': _rovel_old_cg('drawing-letter', 'Tessa draws her mother’s kitchen on the reverse of the welcome letter with her healthy right hand. Her pen tears the paper.'),
            'night-restart': _rovel_old_cg('drawing-restart', 'In a clean corner of the same torn sheet, Tessa starts again with her mother’s chair. Her dead phone remains beside the letter.'),
            'ward-entry': _rovel_old_cg('ward-entrance', 'Mara brings Tessa into the occupied ward. A porter removes a name card and draws a curtain. Iven tends Olan’s right hand near the older healer.'),
            'ward-assessment': _rovel_new_cg('ward-assessment', 'Iven tends Olan’s injured right hand before the older healer begins. Two fingers are missing; the wound edges still bleed and dark corruption has spread beyond the morning mark toward his elbow. No blue or white light is present.'),
            'ward-blue': _rovel_old_cg('blue-healing', 'Two fingers are missing from Olan’s right hand. Blue healing closes the bleeding edges while dark discoloration continues beyond the ink mark toward his elbow.'),
            'ward-unlit': _rovel_old_cg('ward-standing-unlit', 'The priest ushers Tessa to Olan’s bed. Iven stays beside her; the older healer waits. Tessa has not yet formed the white light.'),
            'ward-lit': _rovel_old_cg('ward-standing-light', 'A small white light trembles between Tessa’s hands. Iven remains beside her; Olan brings his injured right arm toward its edge.'),
            'ward-purification': _rovel_old_cg('first-purification', 'Tessa now sits on the stool beside Iven and brings white light over Olan’s wrist. Iven touches skin as the discoloration clears.'),
            'ward-last-patch': _rovel_old_cg('last-patch', 'Olan turns his arm; Tessa works back toward the last dark patch beside the wound. He settles against the pillow.'),
            'ward-cleared': _rovel_old_cg('purification-cleared', 'The corruption is gone. Tessa’s light lingers over the two missing fingers; the older healer brings a fresh dressing.'),
            'ward-hand': _rovel_old_cg('rested-hand', 'Olan’s dressed right hand rests on the blanket. The remaining fingers relax; the missing fingers have not returned.'),
            'ward-pause': _rovel_old_cg('treatment-pause', 'A mother calls from the next row beside her awake daughter. Tessa starts to rise; Iven remains beside her and asks to see the daughter first.'),
            'ward-water': _rovel_old_cg('after-first-treatment', 'Iven has brought water and gone to the family. Tessa sits beside sleeping Olan with the cup untouched.'),
            'ceremony-mantle': _rovel_new_cg('ceremony-mantle', 'Senn pins the badge to Tessa’s white Saint’s robe and settles the light white mantle over it beneath the sunburst banners.'),
            'ceremony-orders': _rovel_new_cg('ceremony-orders', 'At the hall door, Orra holds out written orders while the messenger offers her a blackened ward stone.'),
            'ceremony-dais': _rovel_new_cg('ceremony-dais', 'Senn and Tessa have reached the dais beside the empty chair. Senn faces the audience; Orra watches from the hall door outside this view.'),
            'ceremony-applause': _rovel_new_cg('ceremony-applause', 'Standing among the wounded, Olan claps his good left hand against his thigh. His injured right hand still lacks two fingers.'),
            'ceremony-refusal': _rovel_new_cg('ceremony-refusal', 'Tessa grips Senn’s sleeve and stays standing beside the ceremonial chair. Her attention is on him, while applause continues.'),
            'ceremony-refused-chair': _rovel_new_cg('ceremony-refused-chair', 'Tessa has stepped to the side of the empty ceremonial chair while keeping her right hand on Senn’s left sleeve. He has turned toward her; the refusal changes her position, not her grip.'),
            'ceremony-intervention': _rovel_new_cg('ceremony-intervention', 'Orra stands on the dais and addresses Iven, who remains entirely below the steps holding Tessa’s bag. Tessa and Senn stand above him beside the unused chair. Iven has not been called up yet.'),
            'ceremony-yield': _rovel_new_cg('ceremony-yield', 'After Iven refuses to clear Tessa for travel, Orra signals him up. Senn moves aside to yield the steps, and Iven can begin ascending with Tessa’s bag. Tessa remains standing beside the unused chair.'),
            'window-packing': _rovel_new_cg('window-packing', 'Tessa sits at the infirmary window. Her bag is beside her; Iven starts packing the medical chest. The convoy waits below.'),
            'convoy-mother': _rovel_new_cg('convoy-mother', 'Seen from the infirmary window, the mother who called from the next row approaches the convoy wagons.'),
            'window-pause': _rovel_new_cg('window-pause', 'Iven sets the bottle back in the medical chest and leaves the lid open. He is beside Tessa at the window and has not yet sat with her.'),
            'convoy-guards': _rovel_new_cg('convoy-guards', 'Below the infirmary window, Mara assigns two soldiers who previously guarded Tessa’s apartment to the convoy.'),
            'window-together': _rovel_new_cg('window-together', 'Tessa has made room on the sill and Iven sits beside her. Her bag remains nearby, and the medical chest stays open.'),
        }

        # Retained stages are explicit working components, not approved references.
        def _rovel_arch_stage(tessa, raised=False, mara=False):
            actors = [_rovel_actor(tessa, 100), _rovel_actor('senn-speaking-bright', 1120, 60)]
            if mara:
                actors = [_rovel_actor('mara-cloak-corrected-bright', 780, 140, 620, 930),
                          _rovel_actor('senn-speaking-bright', 1280, 70, 620, 930),
                          _rovel_actor(tessa, 50)]
            return _rovel_stage('art/opening/bg/' + ('arch-guards-raised' if raised else 'arch-conversation') + '.png',
                                'Tessa faces Senn by the sealed arch. Soldiers remain between her and the scholar. Their shields are ' + ('raised.' if raised else 'lowered.') + (' Mara has approached with the folded cloak.' if mara else ''), actors)

        ROVEL_STAGES.update({
            'arch-raised': _rovel_arch_stage('tessa-question-bright', raised=True),
            'arch-question': _rovel_arch_stage('tessa-question-bright'),
            'arch-refusal': _rovel_arch_stage('tessa-refusal-bright'),
            'arch-call': _rovel_arch_stage('tessa-phone-bright', mara=True),
            'arch-promise': _rovel_arch_stage('tessa-question-bright', mara=True),
            'night-exchange': _rovel_stage('art/opening/bg/apartment-open.png',
                'Tessa has climbed down from the window chair. Mara holds another covered plate near the open door. A guard waits in the hall.',
                [_rovel_actor('tessa-cloaked-night', 70), _rovel_actor('mara-supper-night', 1100, 40)]),
            'night-alone': _rovel_stage('art/opening/bg/apartment-locked.png',
                'Mara and the cloak have gone. The door has shut; Tessa stands alone with her phone. Both plates remain untouched.',
                [_rovel_actor('tessa-refusal-night', 660, 65)]),
        })

        ROVEL_BEATS = {}

        def _rovel_wardrobe(scene, line):
            if scene == 2:
                return 'arrival-cloak' if line < 101 else 'arrival'
            return {1: 'arrival', 3: 'working', 4: 'formal', 5: 'formal'}[scene]

        def _rovel_portrait(person, expression, scene, line):
            if person is None:
                return None
            wardrobe = _rovel_wardrobe(scene, line) if person == 'TESSA' else 'source-scene'
            suffix = '-' + wardrobe if person == 'TESSA' else ''
            return dict(who=person, image='art/rovel/portraits/' + expression + suffix + '-' + ROVEL_GRADES[scene] + '.png',
                        expression=expression, wardrobe=wardrobe, framing='face-only-no-costume-or-props',
                        alt=person.title() + ': ' + expression.replace('-', ' ') + '.',
                        review='unreviewed')

        def _rovel_present_cast(scene, line):
            # Presence supplies context beyond a deliberate camera/portrait crop.
            # It does not imply all these people are visible in every composition.
            if scene == 1:
                cast = ['TESSA', 'SCHOLAR', 'STRANGERS']
                if line >= 22:
                    cast += ['SENN', 'WOMAN', 'GUARD', 'PORTERS', 'PATIENT']
                if line >= 29:
                    cast += ['SOLDIERS']
                if line >= 52:
                    cast += ['MARA']
                return cast
            if scene == 2:
                return ['TESSA'] + (['MARA', 'GUARD'] if 73 <= line < 106 else [])
            if scene == 3:
                cast = ['TESSA', 'IVEN', 'OLAN', 'MARA', 'OLDER HEALER', 'PORTER']
                if line >= 122:
                    cast += ['PRIEST']
                if line >= 162:
                    cast += ['MOTHER', 'DAUGHTER']
                return cast
            if scene == 4:
                cast = ['TESSA', 'SENN', 'CROWD', 'WOUNDED']
                if line >= 178:
                    cast += ['ORRA', 'MESSENGER']
                if line >= 185:
                    cast += ['OLAN']
                if line >= 206:
                    cast += ['IVEN']
                return cast
            return ['TESSA', 'IVEN'] + (['MOTHER'] if line >= 226 else []) + (['MARA', 'TWO SOLDIERS'] if line >= 242 else [])

        def _rovel_record(scene, line, stage, cast, mode='action', speaker=None,
                          listener=None, page=0, hold=None, focus=None, state=None):
            key = (scene, line, page)
            if key in ROVEL_BEATS:
                raise ValueError('Duplicate Rovel page: ' + repr(key))
            stage_descriptor = copy.deepcopy(ROVEL_STAGES[stage])
            # Compact exchanges keep the staged people in the room; the portraits
            # beside the text add the close view. An empty stage behind floating
            # faces was a rejected failure (principal pair absent from the scene).
            framing = (focus or ('Compact speaker and listener against their established setting; other present figures need not be duplicated in portrait frames.'
                                if mode == 'compact' else 'The staged composition carries the action; narration does not remove its people.'))
            ROVEL_BEATS[key] = dict(
                id='s%03d_%03d_%d' % key, source=key, mode=mode,
                stage=stage_descriptor, stage_id=stage, cast=list(cast),
                present_cast=sorted(set(_rovel_present_cast(scene, line)) | set(cast)),
                framing=framing,
                speaker=_rovel_portrait(*(speaker or (None, None)), scene, line),
                listener=_rovel_portrait(*(listener or (None, None)), scene, line),
                hold=hold, focus=focus, state=state or {},
                grade=ROVEL_GRADES[scene], wardrobe=_rovel_wardrobe(scene, line),
                review='unreviewed-in-rovel')

        # S001: arrival, return and closure are separate states; Mara enters at 52.
        for line, stage, cast, focus in (
            (9, 'arrival', ('TESSA', 'SCHOLAR', 'STRANGERS'), None),
            (11, 'milk', ('TESSA',), 'Insert of the landing; spectators and control are outside the crop.'),
            (13, 'message', ('TESSA',), 'Phone insert, with the open modern world still contextualized.'),
            (15, 'return', ('TESSA', 'SCHOLAR', 'STRANGERS'), None),
            (17, 'closure', ('TESSA', 'SCHOLAR'), None),
            (22, 'petition', ('SENN', 'WOMAN', 'GUARD', 'PORTERS', 'PATIENT'), 'Cut from Tessa at the arch to the interruption preventing Senn reaching her.'),
            (27, 'release', ('WOMAN', 'GUARD', 'PORTERS', 'PATIENT'), 'The passing patient and woman occupy this cutaway; Tessa remains at the arch.'),
            (60, 'stretcher', ('TESSA', 'MARA', 'PORTERS', 'PATIENT', 'CROWD'), None),
            (65, 'cloak', ('TESSA', 'MARA', 'SENN', 'SCHOLAR'), None),
        ):
            _rovel_record(1, line, stage, cast, focus=focus)
        _rovel_record(1, 15, 'closure', ('TESSA', 'SCHOLAR'), page=1,
                      state={'arch': 'closed', 'lever': 'down', 'groceries': 'threshold'})
        _rovel_record(1, 19, 'closure', ('TESSA', 'SCHOLAR'), mode='compact', speaker=('TESSA', 'tessa-startled'),
                      hold='Her demand follows reaching the empty opening; the scholar continues holding the lever down.')
        _rovel_record(1, 24, 'petition', ('SENN', 'WOMAN', 'GUARD', 'PORTERS', 'PATIENT'), mode='compact',
                      speaker=('WOMAN', 'petitioner'), listener=('SENN', 'senn-listening'),
                      hold='The woman keeps his sleeve until the guard draws her aside at 27.')
        for line, stage, speaker, listener in (
            (29, 'arch-raised', ('SENN', 'senn-assuring'), ('TESSA', 'tessa-startled')),
            (32, 'arch-raised', ('TESSA', 'tessa-startled'), ('SENN', 'senn-listening')),
            (37, 'arch-question', ('TESSA', 'tessa-startled'), ('SENN', 'senn-listening')),
            (40, 'arch-refusal', ('SENN', 'senn-assuring'), ('TESSA', 'tessa-resolute')),
            (43, 'arch-refusal', ('TESSA', 'tessa-resolute'), ('SENN', 'senn-listening')),
            (46, 'arch-refusal', ('SENN', 'senn-assuring'), ('TESSA', 'tessa-resolute')),
            (49, 'arch-refusal', ('TESSA', 'tessa-resolute'), ('SENN', 'senn-evasive')),
            (54, 'arch-promise', ('SENN', 'senn-assuring'), ('TESSA', 'tessa-startled')),
            (57, 'arch-promise', ('TESSA', 'tessa-startled'), ('SENN', 'senn-evasive')),
            (62, 'stretcher', ('TESSA', 'tessa-startled'), ('SENN', 'senn-evasive')),
        ):
            cast = ('TESSA', 'SENN', 'SOLDIERS', 'SCHOLAR') + (('MARA',) if line >= 52 else ())
            _rovel_record(1, line, stage, cast, mode='compact', speaker=speaker, listener=listener,
                          hold='The exchange holds its geography; expressions carry the change in attention.')
        _rovel_record(1, 35, 'arch-question', ('TESSA', 'SENN', 'SOLDIERS', 'SCHOLAR'),
                      state={'shields': 'lowered', 'soldiers': 'remain-blocking'})
        _rovel_record(1, 52, 'arch-call', ('TESSA', 'SENN', 'MARA', 'SOLDIERS', 'SCHOLAR'),
                      state={'cloak': 'carried-by-mara', 'phone': 'retry-no-service'})

        # S002: guards remain beyond the threshold; cloak/phone/chair state changes
        # follow action, not the presence or absence of a dialogue speaker.
        for line, stage, cast, focus, state in (
            (69, 'night-window', ('TESSA',), None, {'chair': 'at-window', 'phone': 'raised', 'cloak': 'worn'}),
            (71, 'night-window', ('TESSA',), 'The dress is in the same established room; Tessa remains on the window chair.', {'dress': 'on-floor'}),
            (73, 'night-exchange', ('TESSA', 'MARA', 'GUARD'), None, {'chair': 'at-window', 'plate': 'carried-by-mara'}),
            (90, 'night-blocked', ('TESSA', 'MARA', 'GUARD'), None, {'plate': 'on-table', 'candle': 'carried-by-tessa'}),
            (101, 'night-cloak', ('TESSA', 'MARA', 'GUARD'), None, {'candle': 'on-table', 'cloak': 'on-floor'}),
            (106, 'night-alone', ('TESSA',), 'Mara has left with the cloak; the guard is outside the locked door.', {'door': 'locked', 'cloak': 'gone-with-mara'}),
            (108, 'night-chair', ('TESSA',), None, {'chair': 'blocking-door', 'phone': 'dead-on-table'}),
            (110, 'night-drawing', ('TESSA',), 'Hand, paper and phone matter here; no other person is in the room.', {'drawing': 'kitchen-torn', 'right-hand': 'healthy'}),
            (112, 'night-restart', ('TESSA',), 'Hold the new beginning rather than introducing another person or scene.', {'drawing': 'mothers-chair', 'right-hand': 'healthy'}),
        ):
            _rovel_record(2, line, stage, cast, mode=('quiet' if line in (69, 71, 106, 110, 112) else 'action'), focus=focus, state=state)
        for line, stage, speaker, listener in (
            (75, 'night-exchange', ('TESSA', 'tessa-resolute'), ('MARA', 'mara-controlled')),
            (78, 'night-exchange', ('MARA', 'mara-controlled'), ('TESSA', 'tessa-listening')),
            (81, 'night-exchange', ('TESSA', 'tessa-resolute'), ('MARA', 'mara-controlled')),
            (84, 'night-exchange', ('MARA', 'mara-controlled'), ('TESSA', 'tessa-resolute')),
            (87, 'night-exchange', ('TESSA', 'tessa-resolute'), ('MARA', 'mara-uneasy')),
            (92, 'night-blocked', ('TESSA', 'tessa-resolute'), ('MARA', 'mara-controlled')),
            (95, 'night-blocked', ('MARA', 'mara-controlled'), ('TESSA', 'tessa-wounded')),
            (98, 'night-blocked', ('TESSA', 'tessa-wounded'), ('MARA', 'mara-uneasy')),
            (103, 'night-cloak', ('TESSA', 'tessa-wounded'), ('MARA', 'mara-uneasy')),
        ):
            _rovel_record(2, line, stage, ('TESSA', 'MARA', 'GUARD'), mode='compact', speaker=speaker, listener=listener,
                          hold='The doorway relationship and object state hold until the next written action.')

        # S003: the older healer uses blue light; Tessa's white light follows it.
        ward_cast = ('TESSA', 'IVEN', 'OLAN', 'PRIEST', 'OLDER HEALER')
        for line, stage, cast, focus, state in (
            (116, 'ward-entry', ward_cast + ('MARA', 'PORTER'), None, {'badge': 'absent'}),
            (118, 'ward-assessment', ('IVEN', 'OLAN', 'OLDER HEALER'), 'Close assessment view before blue healing; Tessa and her escorts remain in the ward outside the crop.', {'right-fingers': 'two-missing', 'corruption': 'beyond-morning-mark', 'wound-edges': 'bleeding', 'blue-healing': 'not-yet-started', 'tessa-light': 'absent'}),
            (120, 'ward-blue', ('IVEN', 'OLAN', 'OLDER HEALER'), 'The healer’s hands and Olan’s arm establish the limit of blue healing.', {'blue-healing': 'closes-edges', 'corruption': 'still-spreading'}),
            (122, 'ward-unlit', ward_cast, None, {'tessa-light': 'absent'}),
            (127, 'ward-lit', ward_cast, None, {'tessa-light': 'white-trembling'}),
            (138, 'ward-lit', ward_cast, None, {'olan-arm': 'drawn-closer'}),
            (143, 'ward-purification', ward_cast, None, {'tessa': 'seated', 'corruption': 'clearing-at-wrist'}),
            (145, 'ward-purification', ward_cast, None, {'iven-touch': 'cleared-skin'}),
            (150, 'ward-last-patch', ward_cast, None, {'corruption': 'last-patch-near-wound'}),
            (152, 'ward-cleared', ward_cast, None, {'corruption': 'gone', 'right-fingers': 'two-missing'}),
            (160, 'ward-hand', ('TESSA', 'OLAN'), 'Resting-hand insert retains Tessa’s attention without adding a standing portrait over the hand.', {'right-fingers': 'two-missing', 'corruption': 'gone'}),
            (162, 'ward-pause', ('TESSA', 'IVEN', 'OLAN', 'MOTHER', 'DAUGHTER'), None, {'mother': 'next-row'}),
            (167, 'ward-pause', ('TESSA', 'IVEN', 'OLAN', 'MOTHER', 'DAUGHTER'), None, {'tessa': 'starting-to-rise'}),
            (172, 'ward-water', ('TESSA', 'OLAN', 'IVEN', 'MOTHER', 'DAUGHTER'), 'Iven has gone to the next-row family; he is not still beside Tessa.', {'iven': 'at-family', 'water': 'untouched', 'olan': 'falling-asleep'}),
        ):
            _rovel_record(3, line, stage, cast, mode=('quiet' if line in (160, 172) else 'action'), focus=focus, state=state)
        for line, stage, speaker, listener, cast in (
            (124, 'ward-unlit', ('PRIEST', 'priest'), ('TESSA', 'tessa-listening'), ward_cast),
            (129, 'ward-lit', ('TESSA', 'tessa-startled'), ('IVEN', 'iven-attentive'), ward_cast),
            (132, 'ward-lit', ('IVEN', 'iven-attentive'), ('TESSA', 'tessa-listening'), ward_cast),
            (135, 'ward-lit', ('TESSA', 'tessa-wounded'), ('IVEN', 'iven-concerned'), ward_cast),
            (140, 'ward-lit', ('OLAN', 'olan'), ('TESSA', 'tessa-listening'), ward_cast),
            (147, 'ward-purification', ('OLAN', 'olan'), ('TESSA', 'tessa-listening'), ward_cast),
            (154, 'ward-cleared', ('TESSA', 'tessa-listening'), ('IVEN', 'iven-concerned'), ward_cast),
            (157, 'ward-cleared', ('IVEN', 'iven-concerned'), ('TESSA', 'tessa-wounded'), ward_cast),
            (164, 'ward-pause', ('MOTHER', 'mother'), ('TESSA', 'tessa-listening'), ('TESSA', 'IVEN', 'OLAN', 'MOTHER', 'DAUGHTER')),
            (169, 'ward-pause', ('IVEN', 'iven-attentive'), ('TESSA', 'tessa-listening'), ('TESSA', 'IVEN', 'OLAN', 'MOTHER', 'DAUGHTER')),
        ):
            _rovel_record(3, line, stage, cast, mode='compact', speaker=speaker, listener=listener,
                          hold='The source treatment state stays visible while attention changes between speaker and listener.')

        # S004: ceremony performers are required; the room plate is not coverage.
        for line, stage, cast, focus, state in (
            (176, 'ceremony-mantle', ('TESSA', 'SENN'), None, {'badge': 'attached', 'mantle': 'being-settled'}),
            (178, 'ceremony-orders', ('ORRA', 'MESSENGER'), 'Cut to the hall door; Tessa and Senn remain elsewhere in the hall.', {'orders': 'held-by-orra', 'stone': 'offered-by-messenger'}),
            (183, 'ceremony-dais', ('TESSA', 'SENN', 'CROWD'), 'The camera follows Tessa and Senn onto the platform; Orra looks toward them from the hall door outside this view.', {'tessa': 'brought-onto-dais'}),
            (185, 'ceremony-applause', ('OLAN', 'WOUNDED'), 'The crowd insert specifically preserves Olan’s changed right hand.', {'olan-applause': 'left-hand-on-thigh', 'right-fingers': 'two-missing'}),
            (190, 'ceremony-refusal', ('TESSA', 'SENN', 'CROWD'), None, {'tessa': 'catches-senn-sleeve'}),
            (198, 'ceremony-refused-chair', ('TESSA', 'SENN', 'CROWD'), None, {'tessa': 'steps-around-chair', 'sleeve-grip': 'retained'}),
            (206, 'ceremony-intervention', ('TESSA', 'SENN', 'ORRA', 'IVEN', 'CROWD'), None, {'orra': 'on-dais', 'iven': 'below-dais', 'bag': 'with-iven'}),
            (214, 'ceremony-yield', ('TESSA', 'SENN', 'ORRA', 'IVEN', 'CROWD'), None, {'orra': 'signals-iven-up', 'senn': 'yields-steps', 'iven': 'called-up', 'bag': 'with-iven'}),
        ):
            _rovel_record(4, line, stage, cast, focus=focus, state=state)
        for line, stage, speaker, listener, cast in (
            (180, 'ceremony-orders', ('MESSENGER', 'messenger'), ('ORRA', 'orra'), ('ORRA', 'MESSENGER')),
            (187, 'ceremony-dais', ('SENN', 'senn-assuring'), ('TESSA', 'tessa-listening'), ('TESSA', 'SENN', 'ORRA', 'CROWD')),
            (192, 'ceremony-refusal', ('TESSA', 'tessa-wounded'), ('SENN', 'senn-listening'), ('TESSA', 'SENN', 'CROWD')),
            (195, 'ceremony-refusal', ('SENN', 'senn-assuring'), ('TESSA', 'tessa-wounded'), ('TESSA', 'SENN', 'CROWD')),
            (200, 'ceremony-refused-chair', ('TESSA', 'tessa-resolute'), ('SENN', 'senn-evasive'), ('TESSA', 'SENN', 'CROWD')),
            (203, 'ceremony-refused-chair', ('SENN', 'senn-evasive'), ('TESSA', 'tessa-resolute'), ('TESSA', 'SENN', 'CROWD')),
            (208, 'ceremony-intervention', ('ORRA', 'orra'), ('IVEN', 'iven-attentive'), ('TESSA', 'SENN', 'ORRA', 'IVEN', 'CROWD')),
            (211, 'ceremony-intervention', ('IVEN', 'iven-concerned'), ('TESSA', 'tessa-listening'), ('TESSA', 'SENN', 'ORRA', 'IVEN', 'CROWD')),
        ):
            _rovel_record(4, line, stage, cast, mode='compact', speaker=speaker, listener=listener,
                          hold='The formal public arrangement persists; the named listener registers the line.',
                          state=({'orra': 'on-dais', 'iven': 'below-dais', 'bag': 'with-iven'} if line in (208, 211) else None))

        # S005: exterior inserts are editorial cuts, not the player travelling.
        for line, stage, cast, focus, state in (
            (218, 'window-packing', ('TESSA', 'IVEN'), None, {'bag': 'beside-tessa', 'chest': 'being-packed', 'iven': 'standing'}),
            (226, 'convoy-mother', ('MOTHER',), 'View from their window; Tessa and Iven remain upstairs and are intentionally outside this insert.', {'mother': 'approaching-wagons'}),
            (237, 'window-pause', ('TESSA', 'IVEN'), None, {'bottle': 'back-in-chest', 'chest': 'open', 'iven': 'standing'}),
            (242, 'convoy-guards', ('MARA', 'TWO SOLDIERS'), 'View from the same window; Tessa and Iven remain upstairs.', {'soldiers': 'former-apartment-guards', 'mara': 'assigning-convoy'}),
            (250, 'window-together', ('TESSA', 'IVEN'), None, {'tessa': 'makes-room', 'iven': 'sits-beside-her', 'chest': 'open', 'bag': 'beside-tessa'}),
        ):
            _rovel_record(5, line, stage, cast, mode=('quiet' if line in (218, 237, 250) else 'action'), focus=focus, state=state)
        for line, stage, speaker, listener in (
            (220, 'window-packing', ('TESSA', 'tessa-listening'), ('IVEN', 'iven-attentive')),
            (223, 'window-packing', ('IVEN', 'iven-attentive'), ('TESSA', 'tessa-listening')),
            (228, 'window-packing', ('TESSA', 'tessa-wounded'), ('IVEN', 'iven-concerned')),
            (231, 'window-packing', ('IVEN', 'iven-attentive'), ('TESSA', 'tessa-listening')),
            (234, 'window-packing', ('TESSA', 'tessa-wounded'), ('IVEN', 'iven-concerned')),
            (239, 'window-pause', ('IVEN', 'iven-concerned'), ('TESSA', 'tessa-wounded')),
            (244, 'window-pause', ('TESSA', 'tessa-listening'), ('IVEN', 'iven-attentive')),
            (247, 'window-pause', ('IVEN', 'iven-attentive'), ('TESSA', 'tessa-listening')),
        ):
            _rovel_record(5, line, stage, ('TESSA', 'IVEN'), mode='compact', speaker=speaker, listener=listener,
                          hold='Iven remains standing by the open chest until Tessa makes room at 250; the listener stays visible.')
        return ROVEL_BEATS

    ROVEL_BEATS = _build_rovel_plan()

    def rovel_beat(scene=None, line=None, page=None):
        """Return a detached descriptor; no story, knowledge or asset mutation."""
        key = (current_scene if scene is None else scene,
               source_line if line is None else line,
               source_page if page is None else page)
        beat = ROVEL_BEATS.get(key)
        return copy.deepcopy(beat) if beat is not None else None

    def rovel_required_assets(scene=None):
        """Scene components required by authored beats, not a clearance."""
        paths = set()
        for key, beat in ROVEL_BEATS.items():
            if scene is not None and key[0] != scene:
                continue
            paths.add(beat['stage']['image'])
            paths.update(actor['image'] for actor in beat['stage']['actors'])
            paths.update(beat[role]['image'] for role in ('speaker', 'listener') if beat[role])
        return sorted(paths)

    def rovel_missing_assets(loadable=None, variants=None):
        """List missing files/pairs explicitly; callers must not hide the result."""
        if loadable is None:
            loadable = renpy.loadable
        if variants is None:
            variants = LIGHTING_VARIANTS
        missing = []
        for path in rovel_required_assets():
            if not loadable(path):
                missing.append(path)
            alternate = variants.get(path)
            if not alternate:
                missing.append('Base mapping: ' + path)
            elif not loadable(alternate):
                missing.append(alternate)
        return sorted(set(missing))
