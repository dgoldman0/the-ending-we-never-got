# Batch 8 — small continuity and surface corrections

29 September 2026. Four neutral source corrections are delivered at their existing `renpy/game/art/scenes/` paths. These began from the current files, including Claude's repairs. They are local art corrections, not a new grade, runtime build, connected-play verdict or user approval.

| Delivered source | Visible correction | Changed pixels |
| --- | --- | --- |
| `s034-return-cargo-shed.png` | The third guard at the doorway edge has a bottle-green cap and coat shoulder, with a compact visible horn. The door occludes his far temple. Marren and the nearer guard stay unchanged. | 0.119% |
| `s050-citadel-lower-stair.png` | Two pier-base blocks and the left end of the bottom step have rough grey stone in place of the old diamond pattern. The mask ends at mortar boundaries. | 1.086% |
| `s051-north-infirmary-court.png` | Lucan's level crossbow is seen side-on: a compact edge-on front bow fitting and horizontal string planes replace the tall D and its diagonal strings. His grip hand has separate bent fingers and the upper hand a natural thumb. | 1.237% |
| `s058-final.png` | Large worn flagstones continue behind the foreground chair/stool and at the two smaller leg-adjacent remnants. The old rectangular mosaic patches are removed. | 5.942% |

Each folder retains the current input, selected built-in imagegen donor, hand-shaped GIMP mask specification, actual layered XCF, exported candidate, reopened export, native before/after crops and `verification.json`. The visible XCF exports were reopened and pixel-compared with the delivered PNGs. Complete inputs and final exports, native crops and donor placement scale were visually inspected. Changes are confined to the recorded bounds; all other pixels remain exactly equal to the current input.

S058's first attempt to restore the old furniture silhouettes also restored narrow old-floor fringes. The final version uses the matching lower-furniture donor inside the local floor mask; the full upper furniture, figures and broader room remain the source. S050's first crop ended within a block; its final donor was extended to the actual mortar joint before delivery.

Generation used the built-in tool. Filesystem attachments and `view_image` failed in the environment's `mountinfo` helper; inspection used read-only inline image derivatives, and generation used that conversation image. All actual component scaling, masks, assembly and export were performed in GIMP. Exact prompts are in `art/prompts/batch8-minor-details/`. `build.py` reproduces these four masters and their exports without altering runtime sources.

## Completed Gray Scar follow-ups

The root agent subsequently assigned and received two additional current-source corrections:

- `s018-gray-scar-ferry-approach.png`: finish the two rear escorts' lower string halves, joining the existing nuts to the opposite limb tips. This is a separate editable 1 px GIMP brush layer; only those thin paths change.
- `s021-rescue.png`: remove Iven's moustache/stubble with a lower-face mask while protecting his source eyes, hair and coat; give the spent crossbow a straight relaxed string between its tips. An initial mixed string repair left tiny stubs, so the final mask uses one coherent lower-bow assembly. Upper stock and floor contact are preserved.

`build-followups.py` reproduces these masters. Both full final paintings and their native crops were inspected, with magnified checks of the very small face and string regions. Reopened XCF exports match the delivered sources exactly. These follow-ups carry the same neutral-source-only limitations as the initial group.
