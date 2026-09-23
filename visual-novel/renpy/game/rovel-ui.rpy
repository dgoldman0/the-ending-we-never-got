# Authored S001-S005 stage beats. Reading screens live in ui-reading.rpy.
init python:
    # Space remains a reading key when a footer control has mouse focus. Ren'Py's
    # unfocused dismissal retains its normal reveal/advance behavior.
    if 'K_SPACE' not in config.keymap['dismiss_unfocused']:
        config.keymap['dismiss_unfocused'].append('K_SPACE')

    def current_rovel_beat():
        return rovel_beat(current_scene, source_line, source_page) if 1 <= current_scene <= 5 else None

    def rovel_face_ready(face):
        return face is not None and renpy.loadable(face['image'])

    def narrative_save_name():
        chapter = chapter_names[current_chapter - 1] if current_chapter else ''
        return chapter + ' · ' + scene_location.split(' · ')[0]

    def rovel_save_context(data):
        data['chapter'] = chapter_names[current_chapter - 1] if current_chapter else ''
        data['place'] = scene_location

    config.save_json_callbacks.append(rovel_save_context)

    def rovel_slot_place(slot):
        place = FileJson(slot, 'place', empty='An empty place', missing='A saved moment')
        place = place.replace("'S ", "'s ")
        return place if len(place) <= 39 else place[:36].rsplit(' ', 1)[0] + '…'

screen rovel_stage(beat):
    $ stage = beat['stage']
    add lighting_art(stage['image']) xysize (1920,1080)
    for actor in stage['actors']:
        add lighting_art(actor['image']) xpos actor['x'] ypos actor['y'] xysize (actor['w'],actor['h'])
