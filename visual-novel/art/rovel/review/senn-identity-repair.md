# Senn local identity repair — S004

Status: working correction; no scene or sequence clearance. Main-thread review found a narrower face and loosely curled hair appearing between S001 / the original head sheet and S004. The original head sheet is the identity source for this correction; the current ceremony heads are edit targets only.

Senn remains late fifties, rounded face and build, light-brown skin, brown eyes, full sandy-gray crown brushed back, and a carefully tended short beard. No increased recession, baldness, youthful recasting or permanent sneer. The original S001 pleading-woman composition independently confirms the rounded face and brushed-back hair; it supplies no new action to S004.

Only his head/hair/neck transition may change in six existing shots: mantle (176), public dais announcement (183/187), sleeve refusal (190–195), refusal beside the empty chair (198–203), Orra's intervention with Iven below (206–211), and Senn yielding the steps (214). Preserve pose angle, eyeline, each source-specific expression, room, robes, hands, grips, body proportions, other faces, all cast positions and prop repairs. Use native head crops as edit targets, the same initial face reference for every operation, then GIMP masks over existing editable masters before rebuilding both scene grades. Compare to the original identity rather than the previous generated repair.

Bright daylight must continue across the corrected head and surrounding occupants. Intense and Softened versions derive from the same local correction; scene grading remains shared. All final native crops, whole composites, unchanged regions, XCF reopen exports and main-thread sequence review remain required.

## Local correction and manual review completed

The built-in image tool produced six separate head components. Each operation used its own ungraded scene crop as the pose/edit target and the same crop of `raw/senn-expressions-v1.png` as identity reference. No repaired head was used to generate another, and no full scene or other character was regenerated. Prompts are `art/prompts/rovel/senn-*-head-repair.txt`; generated components are `art/rovel/raw/senn-*-head-repair.png`.

GIMP scaled each component to its exact source crop dimensions and applied a two-pixel feathered contour mask covering the head and immediate neck transition. Existing source layers and previous local repairs were retained. Both scene grades were rebuilt with the original shared bright-scene grading. The delivered PNG paths remain `renpy/game/art/rovel/cg/ceremony-*.png` and their matching `art/softened/rovel/cg/` paths.

The six current editable masters are `art/rovel/masters/ceremony-*-identity-repair.xcf`. The corresponding masters without `-identity-repair` preserve the pre-correction state and are superseded for these six runtime PNGs. Within each new master, the prior grade layers are explicitly labeled `PRE-IDENTITY-REPAIR` and hidden; the source, existing prop/costume/hand corrections, and local Senn mask remain editable. The two new top grade layers reproduce the delivery. Editing the underlying mask requires rebuilding those grade composites, not merely exposing an old grade.

I opened each of the twelve final whole compositions and each of the twelve final native head crops, alongside the original head reference. Observations:

| Scene | Native head crop | Final observation |
| --- | --- | --- |
| Mantle | 280 × 290 | Full cheek volume and rounded nose replace the gaunter face. Down-left attention toward Tessa remains; the hairline, ear, beard and collar transition show no obvious seam at native size. Both people share the intense scene glare. |
| Dais | 135 × 150 | The same broader face reads at the distant shot size; the slightly lifted chin and public-speaking mouth remain legible. Head-to-body scale remains natural, and the crown is full rather than progressively recessed. |
| Refusal | 300 × 290 | Right-facing profile preserves the downward eyeline. The nose, cheek and jaw now follow the original rounded identity; smooth backward hair replaces the large curled locks. No duplicate jaw or exposed old head edge is apparent. |
| Refused chair | 182 × 180 | The profile remains consistent with the preceding refusal close-up. Tessa's sleeve grip, empty chair and the bodies are preserved; the head does not appear enlarged or detached from the neck. |
| Intervention | 170 × 165 | The fuller face, short beard and brushed-back crown remain consistent while Senn looks left. Orra, Iven and Tessa retain their prior performance and positions. No patch edge is apparent against the pale wall. |
| Yield | 135 × 145 | The more frontal turn keeps the same broad cheek/nose structure and late-fifties age; the mouth and eyes carry controlled unease. The head is lit with the surrounding group, without a separate spotlight. |

These are local asset observations, not approval of the complete scenes or the connected game. Main-thread independent review and the connected sequence review remain required. The distant heads contain only roughly 100–150 native pixels vertically; that limits fine facial detail even though the source components are larger. Hair retains a natural gentle wave, not a rigidly straight helmet.

## Reproducibility and unchanged-region checks

All six new masters reopened in isolated GIMP instances. Their saved visible Intense layers and separately enabled Softened layers reproduce the twelve delivered PNGs **exactly in every RGBA pixel**. Each export remains 1672 × 941 with alpha 255 throughout. Comparisons against the pre-correction runtime PNGs show **zero changed pixels outside the bounded local head crops** in both grades. This confirms that the distant cast, all hands, body poses, stairs, badges and other scene regions were preserved; it is not a substitute for the manual appearance checks above.

[Verification evidence](senn-identity-repair-verification.json) records crop coordinates, contour polygons, changed-pixel bounds, runtime/master hashes, alpha ranges and all twelve reopen comparisons. Scratch scripts and the pre-correction comparison copies were kept in `/tmp` rather than main project folders. `tools/finish-rovel.scm` was read for the existing grading functions and was not edited.
