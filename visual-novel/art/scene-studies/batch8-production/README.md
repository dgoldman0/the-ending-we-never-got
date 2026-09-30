# Batch 8 source-art handoff

29 September 2026. **Required Batch 8 source repairs delivered.** Seventeen required source repairs and one optional source repair are committed. The user’s subsequent “Proceed” explicitly authorized the four stair references; both remaining stair compositions are now complete at source-art level. Work follows items 62–73 in [the asset request](../../asset-request.md#next-for-gpt-batch-8-what-batch-7-left). The latest user decision keeps Serat's brother as the man already established in the five earlier paintings; the two mismatched paintings are repainted to match him.

All edits start from the current `renpy/game/art/scenes/` sources, retaining Claude's local fixes. Built-in imagegen supplies bounded donors and GIMP performs masks, placement and component correction. Neutral source PNGs replace their same-named files. Grading, runtime code, staging and connected in-game review belong to the next Claude pass; they have not been performed here.

## Delivery groups

| Group | Sources | Record |
| --- | --- | --- |
| Small continuity and surfaces | S034 cargo shed; S050 lower stair; S051 court; S058 final | [Four-source group](../batch8-minor-details/README.md), commit `33b1801` |
| Door wards, armour ward-light and stone | Both S052 paintings; S054 duel and lever | [Citadel group](../batch8-citadel-ward-lever/README.md), commit `1f552aa` |
| Rear crossbow strings and rescue | S018 approach; S021 rescue | [Two-source follow-up](../batch8-minor-details/README.md), commit `f2efe7c` |
| Brother and northern horns | S021 boat; S019 ferryhouse; S021 covered landing | [Gray Scar group](../batch8-gray-scar/README.md), commit `2834c4c` |
| Treatment brother, patient and bow | S021 Serat | [Treatment completion](../batch8-gray-scar/s021-serat/README.md), commit `4ffe762` |
| Return-view raised crossbow and horns | S021 Lucan returns | [Gray Scar completion](../batch8-gray-scar/README.md#return-view-completion), commit `cead5b7` |
| Stair fight and carrier identity | S053 bend: dry floor, open platform, bottleneck, retreat path and dark hair | [Completed S053](../batch8-stair/s053-completion/README.md), commit `f6f4c0e` (supersedes the partial `12d60fa`) |
| Morning landing | S055: broad open floor, dark stone and coherent side descent | [Completed S055](../batch8-stair/s055-morning-completion/README.md), commit `0d843dc` |
| Optional sentry horn variation | S057 father | [Two distant sentries](../batch8-optional-horns/README.md), commit `7cd2556` |

## Stair completion after explicit authorization

Items **64 and 72** are delivered. S053 now has a dry approach and open-sky platform, with broken shields closing the bypass beside Mara while leaving the floor and ascending steps behind her usable. S055 gives Mara a broad level floor continuing toward the viewer, dark weathered stone matching the preceding painting, and a side flight meeting the landing at one coherent straight edge. Root and separate reviewers inspected both final full compositions and native boundaries.

The first S053 heap crowded the retreat; a second bounded donor corrected it. A coarse source-preservation mask left old wall around the carrier's head; that outline was tightened to the hair. S055's first donor created sawtooth cutouts at the stair junction; a local correction and seam cleanup resolved them. Actual complete paintings determined those revisions. The earlier local architectural collages remain rejected diagnostic artifacts, not installed sources.

Automatic approval review initially rejected transferring the four named references to built-in imagegen. The user explicitly authorized that transfer with “Proceed”; no blocker remains. The image-tool filesystem helper still fails with `mountinfo path is not absolute`, so the authorized references were viewed inline and used through built-in conversation image input. No CLI/API fallback was used.

Saved final sources: [S053 bend](../../../renpy/game/art/scenes/s053-bend.png) and [S055 morning](../../../renpy/game/art/scenes/s055-citadel-lower-stair-morning.png). Exact prompts: [S053 architecture](../../prompts/batch8-stair/s053-completion.txt), [S053 retreat path](../../prompts/batch8-stair/s053-retreat-path.txt), [S055 architecture](../../prompts/batch8-stair/s055-morning-completion/01-architecture-correction.txt), [S055 side flight](../../prompts/batch8-stair/s055-morning-completion/02-side-flight-cheek.txt). Their linked scene records contain the editable GIMP masters, donors and native review evidence.

## Export verification

[delivery.json](delivery.json) lists every delivered source, its frozen original hash, final hash, native dimensions, changed-pixel bounds and editable master. The audit compares the untouched originals to commit `af94379`, then requires the installed source to equal both its candidate and freshly reopened master export. All eighteen source/master pairs pass; every source remains opaque at its original native size. Only neutral scene PNGs changed under `renpy/game/`. No game build or connected-play check is claimed.

## Review limits

Every delivered full composition and native correction region was inspected. Independent review found defects that were then removed: old brother-shoulder remnants, a residual ward-to-jamb gap, and a wrong background figure in a discarded ferryhouse donor. Technical checks confirm native opaque exports, unchanged protected regions and matching freshly reopened GIMP masters. These checks are source-art evidence, not user approval or a new claim that the whole game is complete or visually accepted.

Other optional items remain unchanged: S004 emblems, S049 table/sword, S052 sword hip, the duel's banner/pillar/spear-tip alternatives, S058 drawing/cobble changes and S040 barrier/cart texture. Their scene states and protected mechanics are retained. The optional S057 soldier-horn variation is delivered in the table above.
