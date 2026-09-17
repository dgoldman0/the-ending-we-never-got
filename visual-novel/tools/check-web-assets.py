#!/usr/bin/env python3
"""Check the actual web package, not merely files available to native Ren'Py."""
import json
from pathlib import Path
from zipfile import ZipFile

root = Path(__file__).resolve().parents[1]
game = root / 'renpy' / 'game'
expected = json.loads((game / 'opening-assets.json').read_text())
expected += [p.relative_to(game).as_posix() for p in (game / 'art/interface-original').iterdir() if p.is_file()]
variants = json.loads((game / 'lighting-assets.json').read_text())
missing_variants = [name for name in expected if name.startswith('art/opening/') and '/ui/' not in name and name not in variants]
if missing_variants:
    raise SystemExit('Scene art lacks a softened-lighting counterpart:\n' + '\n'.join(missing_variants))
identical_variants = [name for name, alternate in variants.items()
                      if (game / name).read_bytes() == (game / alternate).read_bytes()]
if identical_variants:
    raise SystemExit('Lighting counterparts are identical; export a real alternate:\n' + '\n'.join(identical_variants))
expected = sorted(set(expected) | set(variants) | set(variants.values()))
with ZipFile(root / 'builds/web/game.zip') as package:
    names = set(package.namelist())
    missing = [name for name in expected if 'game/' + name not in names]
if missing:
    raise SystemExit('Required art missing from the preloaded web package:\n' + '\n'.join(missing))
print(f'Web package contains all {len(expected)} required art assets, including both lighting modes.')
