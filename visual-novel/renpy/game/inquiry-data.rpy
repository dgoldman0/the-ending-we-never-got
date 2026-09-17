# Source-backed first-night inspection. Historical material is separately authored
# production work; the rejected quizzes and invented evidence cards are removed.
init python:
    detail_views = {
        'drawing': {
            'title': 'The torn page',
            'image': 'art/opening/cg/detail-drawing.png',
            'caption': 'A kitchen interrupted. A chair begun again.',
            'description': 'A short tear cuts the abandoned attempt. In a clean corner, blue pen lines begin a wooden kitchen chair. The paper belongs to the temple; the room she draws does not.',
        },
        'phone': {
            'title': 'The dead phone',
            'image': 'art/opening/cg/detail-phone.png',
            'caption': 'The last thing her mother asked for was milk.',
            'description': 'The same dark-green case. The screen is now black. Her mother’s message arrived before the opening closed; every call since has failed.',
        },
    }

    def available_details():
        return ['drawing', 'phone'] if current_scene > 2 or (current_scene == 2 and source_line >= 112) else []

    def closer_here():
        return current_scene == 2 and source_line >= 112

    def inspect_detail(detail):
        if detail in available_details():
            inspected_details.add(detail)
            renpy.retain_after_load()

    def follow_home_thread():
        if available_details():
            inspected_details.update(('drawing', 'phone'))
            followed_connections.add('home')
            renpy.retain_after_load()
