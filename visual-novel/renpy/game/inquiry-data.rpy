# Reader attention only: these functions never alter the screenplay position,
# character knowledge, or outcome. The first-summoning history is separate work.
init python:
    detail_views = {
        'drawing': {
            'title': 'The torn page',
            'image': 'art/opening/cg/detail-drawing.png',
            'caption': 'Her mother’s chair begins in a clean corner of the temple’s welcome letter.',
            'description': 'A tear crosses the first attempt. She has turned the welcome over to draw her mother’s kitchen.',
        },
        'phone': {
            'title': 'The dead phone',
            'image': 'art/opening/cg/detail-phone.png',
            'caption': '“MOM — DID YOU GET THE MILK?”',
            'description': 'Her mother’s last message. Now the battery is dead.',
        },
        'treatment_blue': {
            'title': 'Blue healing',
            'image': 'art/rovel/details/treatment-blue.png',
            'caption': 'The bleeding edges close. The darkness keeps spreading.',
            'description': 'The older healer treats Olan’s right hand. The corruption has passed the line marked that morning.',
        },
        'treatment_white': {
            'title': 'White purification',
            'image': 'art/rovel/details/treatment-white.png',
            'caption': 'The darkness recedes. The missing fingers do not return.',
            'description': 'Tessa clears the corruption; Iven can touch ordinary skin again. Olan moves the fingers he has left.',
        },
        'applause': {
            'title': 'Before the crowd',
            'image': 'art/rovel/details/applause-hand.png',
            'caption': 'Olan claps his good hand against his thigh.',
            'description': '“Tomorrow our Saint leaves with the Bellweir convoy. You have seen what she can do. The curse can be broken.”',
        },
    }

    def discovery_reached(scene, line):
        # Source position belongs to the save. No persistent/global unlocks can
        # leak later material into an earlier save or a new playthrough.
        return current_scene > scene or (current_scene == scene and source_line >= line)

    def available_details():
        result = []
        if discovery_reached(2, 112):
            result.extend(('drawing', 'phone'))
        if discovery_reached(3, 172):
            result.extend(('treatment_blue', 'treatment_white'))
        if discovery_reached(4, 187):
            result.append('applause')
        return result

    def available_inspections():
        details = available_details()
        return [view for view, required in (
            ('home', 'drawing'), ('treatment', 'treatment_white'),
            ('promise', 'applause')) if required in details]

    def closer_here():
        # Invitation belongs to a quiet beat, never a forced scene interruption.
        return (current_scene, source_line) in ((2, 112), (3, 172), (5, 250))

    def inspection_context(detail=None, connection=False):
        # Legacy ShowMenu calls can still name drawing/phone or connection=True.
        requested = {
            'drawing': 'home', 'phone': 'home', 'home': 'home',
            'treatment_blue': 'treatment', 'treatment_white': 'treatment',
            'treatment': 'treatment', 'applause': 'promise', 'promise': 'promise',
        }.get(detail)
        if isinstance(connection, str) and connection in ('home', 'treatment', 'promise'):
            requested = connection
        elif connection is True and requested is None:
            requested = 'home'
        views = available_inspections()
        if requested in views:
            return requested
        return views[-1] if views else None

    def inspect_detail(detail):
        if detail in available_details():
            inspected_details.add(detail)
            renpy.retain_after_load()

    def follow_home_thread():
        if 'drawing' in available_details():
            inspected_details.update(('drawing', 'phone'))
            followed_connections.add('home')
            renpy.retain_after_load()

    def follow_treatment_thread():
        if 'treatment_white' in available_details():
            inspected_details.update(('treatment_blue', 'treatment_white'))
            followed_connections.add('treatment')
            renpy.retain_after_load()

    def follow_public_promise():
        if 'applause' in available_details():
            inspected_details.update(('treatment_white', 'applause'))
            followed_connections.add('promise')
            renpy.retain_after_load()

    # Each view reframes its originating painting toward the detail (focus is
    # a fraction of the 1920x1080 frame), then can bring a related detail
    # alongside it. Opening a view records the first detail; bringing the
    # second alongside records the connection. Nothing is graded or required.
    connection_views = {
        'home': dict(title='The first night', origin='art/opening/cg/drawing-restart.png',
                     focus=(0.60, 0.85), zoom=1.55, first='drawing', second='phone',
                     note='A welcome letter on one side; her mother’s kitchen on the other.'),
        'treatment': dict(title='Olan’s treatment', origin='art/opening/cg/purification-cleared.png',
                          focus=(0.45, 0.62), zoom=1.35, first='treatment_blue', second='treatment_white',
                          note='Blue healing closed the wound; only the white light cleared the curse. Neither returned his fingers.'),
        'promise': dict(title='The public promise', origin='art/rovel/cg/ceremony-applause.png',
                        focus=(0.50, 0.55), zoom=1.3, first='treatment_white', second='applause',
                        firsttitle='At the bedside', firstcaption='The curse has cleared. Two fingers are still missing.',
                        note='Senn, to the hall: “Tomorrow our Saint leaves with the Bellweir convoy. You have seen what she can do. The curse can be broken.”'),
    }

    def open_view(view):
        """Opening a view records attention to its first detail."""
        if view in available_inspections():
            inspect_detail(connection_views[view]['first'])

    def follow_view(view):
        """Bringing the related detail alongside records the connection."""
        if view in available_inspections():
            {'home': follow_home_thread, 'treatment': follow_treatment_thread,
             'promise': follow_public_promise}[view]()

    def inspect_surface(view):
        # Legacy entry point retained for old saves' screen state.
        open_view(view)
