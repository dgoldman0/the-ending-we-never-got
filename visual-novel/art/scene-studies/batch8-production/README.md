# Batch 8 source-art handoff

29 September 2026. **Partial delivery: two required stair compositions remain blocked.** Fifteen required source repairs, one optional source repair and the separate carrier-hair portion of item 72 are committed. Work follows items 62–73 in [the asset request](../../asset-request.md#next-for-gpt-batch-8-what-batch-7-left). The latest user decision keeps Serat's brother as the man already established in the five earlier paintings; the two mismatched paintings are repainted to match him.

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
| Partial carrier identity | S053 bend: hair only | [Stair partial and rejected geometry trials](../batch8-stair/README.md#final-safe-partial--29-september), commit `12d60fa` |
| Optional sentry horn variation | S057 father | [Two distant sentries](../batch8-optional-horns/README.md), commit `7cd2556` |

## Required work still blocked

Items **64 and 72** require two coherent stair compositions: the dark dry open landing around Mara in S055 morning, and S053's narrowed approach, dry floor and open upper platform. The local geometry trials were rejected because they visibly pasted architecture together and retained stone fringes. They were not installed. [Prepared briefs, exact prompts and diagnostic trials](../batch8-stair/README.md) record the intended correction.

Automatic approval review rejected transferring the four named stair references to the built-in image generator, twice, requiring explicit user authorization for that transfer. The root requested permission while continuing unaffected work. The four files are `s053-bend.png`, `s055-citadel-lower-stair-morning.png`, `s050-citadel-lower-stair.png` and `s055-mara.png`. No answer has yet been received. The general image-tool filesystem helper also fails with `mountinfo path is not absolute`; permitted work used read-only inline source views and built-in conversation image input, never a separately billed CLI/API fallback.

## Export verification

[delivery.json](delivery.json) lists every delivered source, its frozen original hash, final hash, native dimensions, changed-pixel bounds and editable master. The audit compares the untouched originals to commit `af94379`, then requires the installed source to equal both its candidate and freshly reopened master export. All seventeen source/master pairs pass; every source remains opaque at its original native size. Only neutral scene PNGs changed under `renpy/game/`. No game build or connected-play check is claimed.

## Review limits

Every delivered full composition and native correction region was inspected. Independent review found defects that were then removed: old brother-shoulder remnants, a residual ward-to-jamb gap, and a wrong background figure in a discarded ferryhouse donor. Technical checks confirm native opaque exports, unchanged protected regions and matching freshly reopened GIMP masters. These checks are source-art evidence, not user approval or a new claim that the whole game is complete or visually accepted.

Other optional items remain unchanged: S004 emblems, S049 table/sword, S052 sword hip, the duel's banner/pillar/spear-tip alternatives, S058 drawing/cobble changes and S040 barrier/cart texture. Their scene states and protected mechanics are retained. The optional S057 soldier-horn variation is delivered in the table above.
