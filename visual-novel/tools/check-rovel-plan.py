#!/usr/bin/env python3
"""Validate authored Rovel coverage and required assets without starting Ren'Py.

Default: missing scene/portrait/Softened files fail the asset gate. --plan-only
checks source/presentation invariants while still reporting those missing files;
it never grants image, UI or connected-experience clearance.
"""
from pathlib import Path
import argparse
import ast
import copy
import json
import re
import runpy
import sys
import textwrap

VN = Path(__file__).resolve().parents[1]
GAME = VN / 'renpy/game'


def load_plan():
    raw = (GAME / 'rovel.rpy').read_text()
    _, marker, body = raw.partition('init python:\n')
    assert marker, 'rovel.rpy needs its standalone init Python block'
    # Ren'Py init blocks share one store: top-level loop targets can overwrite
    # an existing Character map or cursor even though standalone execution works.
    protected = {
        'cast': {'TESSA': 'existing Character', 'SENN': 'existing Character'},
        'source_map': {'scenes': [{'id': 'existing-source'}]},
        'current_scene': 51, 'current_chapter': 9,
        'source_line': 1500, 'source_page': 2,
        'scene_speaker': 'existing-speaker', 'completed_scenes': 50,
    }
    before = copy.deepcopy(protected)
    namespace = {'__name__': 'rovel_plan_check', **protected}
    exec(compile(textwrap.dedent(body), 'rovel.rpy', 'exec'), namespace)
    for name, original in protected.items():
        assert namespace[name] is original and namespace[name] == before[name], (
            'Presentation initialization changed the shared game store: ' + name)
    return namespace


def source_pages():
    adapter = runpy.run_path(str(VN / 'tools/adapt_screenplay.py'),
                            run_name='rovel_source_adapter')
    story, manifest = adapter['adapt']()
    assert story == (GAME / 'story.rpy').read_text(), 'Generated story is stale'
    assert manifest == (GAME / 'source-map.json').read_text(), 'Source map is stale'
    result = {}
    scene = line = None
    speaker = None
    for raw in story.splitlines():
        match = re.fullmatch(r'    \$ (current_scene|source_line|source_page|scene_speaker) = (.+)', raw)
        if not match:
            continue
        name, encoded = match.groups()
        value = ast.literal_eval(encoded)
        if name == 'current_scene':
            scene = value
        elif name == 'source_line':
            line = value
        elif name == 'scene_speaker':
            speaker = value
        elif scene in range(1, 6):
            result[(scene, line, value)] = speaker
    return result


def check_plan(plan):
    beats = plan['ROVEL_BEATS']
    get = plan['rovel_beat']
    expected = source_pages()
    missing = sorted(set(expected) - set(beats))
    extra = sorted(set(beats) - set(expected))
    assert not missing and not extra, f'Coverage mismatch: missing={missing}; extra={extra}'
    assert len(expected) == 95, 'Review source paging changes before changing this milestone'

    for key, source_speaker in expected.items():
        beat = get(*key)
        assert beat['source'] == key, key
        assert beat['review'] == 'unreviewed-in-rovel', 'A descriptor cannot clear an experience'
        assert beat['mode'] in ('compact', 'action', 'quiet'), key
        assert beat['stage']['image'] and beat['stage']['alt'] and beat['framing'], key
        assert beat['cast'] and set(beat['cast']) <= set(beat['present_cast']), key
        assert beat['grade'] == {1: 'bright', 2: 'night', 3: 'ordinary', 4: 'bright', 5: 'ordinary'}[key[0]], key
        actual_speaker = beat['speaker']['who'] if beat['speaker'] else None
        assert actual_speaker == source_speaker, (key, actual_speaker, source_speaker)
        if source_speaker:
            assert beat['mode'] == 'compact', key
            assert not beat['stage']['actors'], 'Compact exchange must not restore giant fixed-gesture cutouts'
        else:
            assert beat['mode'] != 'compact' and beat['speaker'] is None, key
        for role in ('speaker', 'listener'):
            portrait = beat[role]
            if not portrait:
                continue
            assert portrait['who'] in beat['cast'], (key, role, portrait['who'])
            assert portrait['framing'] == 'face-only-no-costume-or-props', key
            if portrait['who'] == 'TESSA':
                assert '-' + beat['wardrobe'] + '-' in portrait['image'], (key, portrait['image'])
        if beat['speaker'] and beat['listener']:
            assert beat['speaker']['who'] != beat['listener']['who'], key
        for forbidden in ('anchors', 'reading_x', 'reading_y', 'reading_w', 'dialogue_position'):
            assert forbidden not in beat, 'Reading geometry belongs to the stable screen, not speaker data'

    # No mutable descriptor returned to a screen may leak into another reading
    # point or survive rollback as a separately advanced presentation cursor.
    snapshot = copy.deepcopy(beats)
    sample = get(1, 54, 0)
    sample['cast'].clear()
    sample['stage']['image'] = 'not-a-real-stage'
    sample['speaker']['expression'] = 'mutated'
    assert beats == snapshot, 'Lookup leaked mutable global presentation data'
    assert get(6, 254, 0) is None, 'Rovel must not silently cover the unproduced later route'
    assert get(1, 15, 2) is None, 'An unmapped source page must stay explicitly unmapped'
    assert get(1, 15, 0)['stage_id'] == 'return'
    assert get(1, 15, 1)['stage_id'] == 'closure'
    assert get(1, 15, 1)['state']['groceries'] == 'threshold'

    # A participant cannot be introduced by whichever portrait happens to exist.
    assert all('MARA' not in beat['present_cast'] for key, beat in beats.items()
               if key[0] == 1 and key[1] < 52)
    assert {'TESSA', 'SENN', 'MARA'} <= set(get(1, 54, 0)['present_cast'])
    assert all('MARA' not in beat['cast'] for key, beat in beats.items()
               if key[0] == 2 and key[1] >= 106)
    assert get(2, 98, 0)['wardrobe'] == 'arrival-cloak'
    assert get(2, 101, 0)['wardrobe'] == 'arrival'
    assert get(2, 108, 0)['state']['phone'] == 'dead-on-table'
    assert get(2, 108, 0)['state']['chair'] == 'blocking-door'
    assert get(2, 112, 0)['state']['right-hand'] == 'healthy'

    # The known dangerous continuity boundaries stay explicit in the plan.
    assert get(3, 118, 0)['stage_id'] == 'ward-assessment'
    assert get(3, 118, 0)['state']['blue-healing'] == 'not-yet-started'
    assert get(3, 118, 0)['state']['wound-edges'] == 'bleeding'
    assert get(3, 118, 0)['stage']['image'] != get(3, 120, 0)['stage']['image']
    assert get(3, 120, 0)['stage_id'] == 'ward-blue'
    assert get(3, 120, 0)['state']['corruption'] == 'still-spreading'
    assert get(3, 122, 0)['state']['tessa-light'] == 'absent'
    assert get(3, 127, 0)['state']['tessa-light'] == 'white-trembling'
    assert get(3, 143, 0)['state']['tessa'] == 'seated'
    assert get(3, 152, 0)['state']['right-fingers'] == 'two-missing'
    assert get(3, 172, 0)['state']['iven'] == 'at-family'
    assert get(3, 172, 0)['state']['water'] == 'untouched'
    assert all(beat['wardrobe'] == 'working' for key, beat in beats.items() if key[0] == 3)
    assert all(beat['wardrobe'] == 'formal' for key, beat in beats.items() if key[0] in (4, 5))
    assert get(4, 180, 0)['speaker']['who'] == 'MESSENGER'
    assert get(4, 180, 0)['listener']['who'] == 'ORRA'
    assert get(4, 185, 0)['state']['olan-applause'] == 'left-hand-on-thigh'
    assert get(4, 198, 0)['state']['sleeve-grip'] == 'retained'
    for line in (206, 208, 211):
        assert get(4, line, 0)['stage_id'] == 'ceremony-intervention'
        assert get(4, line, 0)['state']['iven'] == 'below-dais'
        assert get(4, line, 0)['state']['bag'] == 'with-iven'
    assert get(4, 214, 0)['stage_id'] == 'ceremony-yield'
    assert get(4, 214, 0)['state']['iven'] == 'called-up'
    assert get(4, 214, 0)['state']['senn'] == 'yields-steps'
    assert get(4, 211, 0)['stage']['image'] != get(4, 214, 0)['stage']['image']
    assert get(5, 226, 0)['cast'] == ['MOTHER'] and get(5, 226, 0)['focus']
    assert get(5, 242, 0)['state']['soldiers'] == 'former-apartment-guards'
    assert get(5, 250, 0)['state'] == {
        'tessa': 'makes-room', 'iven': 'sits-beside-her',
        'chest': 'open', 'bag': 'beside-tessa',
    }
    assert get(5, 247, 0)['listener']['who'] == 'TESSA'
    assert 'standing' in get(5, 247, 0)['hold']

    # Missing assets/pairs must be visible in the gate result, never interpreted
    # as permission to display a cast-free fallback or an ungraded portrait.
    assets = plan['rovel_required_assets']()
    assert assets == sorted(set(assets)) and assets
    assert set(plan['rovel_required_assets'](5)) <= set(assets)
    assert plan['rovel_required_assets'](6) == []
    absent = plan['rovel_missing_assets'](loadable=lambda path: False, variants={})
    assert set(assets) <= set(absent)
    assert {'Softened mapping: ' + path for path in assets} <= set(absent)
    pairs = {path: 'soft/' + path for path in assets}
    assert not plan['rovel_missing_assets'](loadable=lambda path: True, variants=pairs)
    return expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan-only', action='store_true',
                        help='Validate source/descriptor structure; report but do not fail on missing art.')
    args = parser.parse_args()
    plan = load_plan()
    pages = check_plan(plan)
    counts = {scene: sum(key[0] == scene for key in pages) for scene in range(1, 6)}
    print('Source/descriptor structure verified: 95 pages; scene counts ' + json.dumps(counts))
    variants = json.loads((GAME / 'lighting-assets.json').read_text())
    missing = plan['rovel_missing_assets'](loadable=lambda path: (GAME / path).is_file(), variants=variants)
    identical = [path for path in plan['rovel_required_assets']()
                 if path in variants and (GAME / path).is_file()
                 and (GAME / variants[path]).is_file()
                 and (GAME / path).read_bytes() == (GAME / variants[path]).read_bytes()]
    if missing or identical:
        print('ASSET GATE FAILED: required production is incomplete.')
        for path in missing:
            print('  Missing: ' + path)
        for path in identical:
            print('  Identical Intense/Softened files: ' + path)
        print('Visual, UI and connected-experience gates remain UNREVIEWED.')
        return 0 if args.plan_only else 1
    print('Required files/pairs exist; visual, UI and connected-experience gates remain UNREVIEWED.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except AssertionError as exc:
        print('PLAN GATE FAILED: ' + str(exc), file=sys.stderr)
        sys.exit(1)
