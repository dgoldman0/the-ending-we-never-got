#!/usr/bin/env python3
"""Audit preloaded web art, paired lighting, and bytes against current sources.

File presence, valid export and matching bytes are technical checks. They do not
clear source staging, likeness, lighting quality, UI or connected-experience gates.
"""
import ast
import json
from pathlib import Path
import re
import runpy
import textwrap
from zipfile import BadZipFile, ZipFile

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'renpy/game'


def required_assets(game=GAME):
    expected = set(json.loads((game / 'opening-assets.json').read_text()))
    expected.update(path.relative_to(game).as_posix()
                    for path in (game / 'art/interface-original').iterdir()
                    if path.is_file())

    # Reuse the descriptor loader with its shared-store isolation checks, not a
    # second manually maintained list that could omit a newly authored performer.
    checker = runpy.run_path(str(ROOT / 'tools/check-rovel-plan.py'),
                             run_name='web_rovel_asset_check')
    plan = checker['load_plan']()
    expected.update(plan['rovel_required_assets']())

    # The discovery definitions are literal authored data. Read that assignment
    # without executing screens, opening the game, or changing discovery state.
    _, marker, body = (game / 'inquiry-data.rpy').read_text().partition('init python:\n')
    if not marker:
        raise ValueError('Cannot locate authored discovery asset definitions')
    tree = ast.parse(textwrap.dedent(body))
    details = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == 'detail_views'
                for target in node.targets):
            details = ast.literal_eval(node.value)
            break
    if details is None:
        raise ValueError('Missing literal detail_views asset definitions')
    expected.update(item['image'] for item in details.values())

    # Runtime UI is not graded like scene art. Scan its declared paths as well
    # as exported files, so a missing required frame cannot disappear from audit.
    ui_pattern = re.compile(r"art/rovel/ui/[A-Za-z0-9_./-]+\.(?:png|svg|webp)")
    for script in game.glob('*.rpy'):
        expected.update(ui_pattern.findall(script.read_text()))
    expected.update(path.relative_to(game).as_posix()
                    for path in (game / 'art/rovel/ui').glob('*')
                    if path.is_file() and path.suffix.lower() in ('.png', '.svg', '.webp'))

    # The code-drawn reading interface (tools/build-ui-assets.py).
    expected.update(path.relative_to(game).as_posix()
                    for path in (game / 'ui').glob('*') if path.is_file())
    # Staging art for S006 onward, whatever has arrived, with Softened twins.
    for folder in ('art/scenes', 'art/portraits', 'art/softened/scenes', 'art/softened/portraits'):
        if (game / folder).is_dir():
            expected.update(path.relative_to(game).as_posix()
                            for path in (game / folder).glob('*.png'))

    variants = json.loads((game / 'lighting-assets.json').read_text())
    # Preserve the older packaged treatments; new unused pose variants remain
    # excluded by the explicit Rovel distribution rules.
    legacy_variants = {path: alternate for path, alternate in variants.items()
                       if not path.startswith('art/rovel/')}
    expected.update(legacy_variants)
    expected.update(legacy_variants.values())
    scene_assets = {path for path in expected
                    if path.startswith(('art/opening/', 'art/rovel/'))
                    and '/ui/' not in path}
    active_variants = {path: variants[path] for path in expected if path in variants}
    expected.update(active_variants.values())
    return expected, scene_assets, active_variants


def audit_assets(game, package_path, expected, scene_assets, variants):
    errors = []
    for path in sorted(scene_assets):
        if path not in variants:
            errors.append('Missing Softened mapping: ' + path)
        elif path.startswith('art/rovel/') and not variants[path].startswith('art/softened/rovel/'):
            errors.append('Rovel Softened path is outside its runtime folder: ' + path)

    for path in sorted(expected):
        if not (game / path).is_file():
            errors.append('Missing source asset: ' + path)
    for path, alternate in sorted(variants.items()):
        if (game / path).is_file() and (game / alternate).is_file():
            if (game / path).read_bytes() == (game / alternate).read_bytes():
                errors.append('Identical Intense/Softened files: ' + path)

    if not package_path.is_file():
        errors.append('Missing web package: ' + str(package_path))
        return errors
    try:
        with ZipFile(package_path) as package:
            names = set(package.namelist())
            for path in sorted(expected):
                member = 'game/' + path
                if member not in names:
                    errors.append('Missing from preloaded game.zip: ' + path)
                elif (game / path).is_file() and package.read(member) != (game / path).read_bytes():
                    errors.append('Stale packaged bytes; rebuild: ' + path)
    except BadZipFile:
        errors.append('Invalid web package: ' + str(package_path))
    return errors


def main():
    expected, scene_assets, variants = required_assets()
    errors = audit_assets(GAME, ROOT / 'builds/web/game.zip',
                          expected, scene_assets, variants)
    if errors:
        raise SystemExit('Web asset gate failed:\n' + '\n'.join(errors))
    print(f'Web package contains all {len(expected)} required art files with current source bytes, '
          f'including {len(variants)} distinct lighting pairs.')
    print('This does not clear visual or connected-experience gates.')


if __name__ == '__main__':
    main()
