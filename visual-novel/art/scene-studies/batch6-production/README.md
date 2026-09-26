# Batch 6 production — 26 September 2026

Final source-art handoff against [the request](../../asset-request.md) at revision `3b482c8`. All nine new paintings are delivered. Of the 32 mandatory repair items (15–46), 31 are completed and **item 24 remains partial: Renn's trapped-leg/body geometry in S035 is still unresolved**. Orren's right-leg support in that picture is corrected. This is a source-art delivery, awaiting the integration team's in-game review.

The [delivery manifest](delivery-manifest.json) records 67 final PNGs: 58 repair outputs, including partial S035, and nine new paintings. It includes exact paths, dimensions, alpha ranges, SHA256 values and each asset's latest commit. The 12 opening repaints are in `art/repaints/` for integration; the other 55 PNGs are at their requested `renpy/game/art/scenes/` paths. Every delivered PNG decoded successfully and is opaque. All nine new paintings have a 16:9 delivery canvas of at least 1920×1080; individual studies record native generation sizes and any resampling.

## Completed groups

- **6110c32 — opening:** 12 same-basename repaints for items18/20/21/22; current base/runtime images preserved. Olan's right-hand anatomy, scholar/Mara identities, milk/carton, modern fabric and round carved arch. Layered masters, native/whole comparisons, independent review and exact exports recorded in batch6-opening.
- **f81e88d — river:** 7 source replacements for items25/27/28; summer windows, Lucan horns, boatman and Mara's left sword. Paired S030 roof aligned; current badges and protected faces/hands unchanged.
- **f2008ae — citadel:** 7 source replacements for items16/19/29/31. Crossbow and bow geometry, Mara's right guard/halo, winter view/torn coat/timber rail, stone surfaces. Native review rejected and corrected copied arm/hair fragments and a bad upper-sleeve insert before promotion. Optional S052 scabbard moves remain deferred.

- **5186f6f — northern:** S038 youthful Lucan/horns and S034 distinct paired-horn engineers, source heads preserved elsewhere; whole/native/peer/master checked.
- **3605900 — hall/wound:** S054 black joint wards and floor shadows, restrained torn RIGHT glove with all digits. Rejected hard mask edges repaired before promotion.
- **f3b6c18 — duel:** fresh reversed action and both grips, rigid spear outside shelter, sword at elbow, matching three-step dais; peer/native/master verified.
- **c43b21d — Bellweir:** eight scenes, items37/42/43/44/45/46; root and citadel peer checked whole/native before source promotion.
- **3a4db0b — bounded continuity:** S042 sheath/spokes and S046 intact hem complete; S035 Orren RIGHT support delivered as PARTIAL only. Renn unresolved.
- **984e5a5 — optional citadel:** S048 teal skirt/table support and S057 wagon shafts/loops, whole/native peer + exact reopened masters.

- **c62994f — Gray Scar:** six repaired source scenes; giant mother/young cats, northern horns, genuine crossbows, adult litter and complete party sheltered before the shut gate. S020 rebuilt from a fresh composition. Root/peer whole and native reviews, exact masters and source hashes recorded.
- **ca37719 — continuity and emblems:** S040 road-wide barrier with fitted original horse/rider masks; S042 paired twelve-ray shield suns and S044 eight-point northern star with restored top/bottom tips repaired locally. Whole/native/peer and master checks passed.

## New paintings and remaining limits

- **d872e01 — optional northern/market details:** S010 split flag/horn openings, S037 solid nearhorn, S043 winter-cap horns, S058 older Orren/matching cart wheel. Exact market lettering unchanged. S037 pre-existing alpha254 normalized to255 without RGB change.
- **910770c — new S057father:** Lucan covers his father’s exposed hand, distinct bearers and coherent adult litter; native core protected through peripheral framing.
- **70efb4d — new S053bend:** Mara holds a physical stair turn; two attackers, retreating wounded pair, correct guard/weapon sides and high-window flash.
- **afb81cb — new S054binding:** correct RIGHT-hand care/LEFT torn sleeve, incoming wounded, supportive Olan; mismatched composite rejected and complete regenerated frame rechecked.

- All mandatory repair groups delivered except **Renn's pose in S035 (item24)**. Two built-in image-tool moderation refusals yielded no child-repair image. Orren's RIGHT support half is delivered; S035 remains explicitly incomplete.
- **7b68819 — new S058drawings:** actual kitchen/welcome-letter reverse and S008 hair-up bench sketch, LEFT packet grip/RIGHT brace, native drawings and hands protected through framing.
- **b70c759 — S057 user correction:** restore the original right bearer’s dark complexion and natural black hair while keeping a distinct mature face. Earlier pale/redheaded result is explicitly rejected and superseded. Face/neck/untouched arms compared; only bounded head/neck changed.
- **cbce2d0 — three new Gray Scar moments:** s018-cats/s021-serat/s021-boat; four carried grips, adult patient, LEFT-thigh care and downstream human boat, matching faces/complexions/clothes and genuine weapon construction.
- **7f1ca7f — new S054strike:** LEFT sword beneath raised arm, short torn RIGHT glove, failing black ward/white glare, plain campaign sleeves and three continuous low risers.
- **a666d88 — new S054lever:** hinged mechanism worked with LEFT hand, RIGHT glove’s dorsal tear preserved, falling entrance ward/covered landing, separate fallen king/spear/sword, plain throne and correct badge.

- Optional **S004 entire emblem group deferred**, documented in a8b7761: replacements visibly disrupted cloth folds/focus; no source changed.
- Optional S049/S052 scabbard relocation and ambiguous S049 table support deferred because bounded changes would disrupt actors or remove a plausible structural support.
- All nine requested source PNGs are delivered under `renpy/game/art/scenes/`. Every delivered group received whole/native and independent review, with observations and export checks in its study. Technical export checks are supporting evidence, not visual acceptance.

## User corrections during this batch

The user rejected **both** the spear and sword grips in the S054 attempts. Root's successive local action edits failed: folded-back arms, disconnected/bent shafts, restored body crossings and inadequate sword contact. None were promoted. Treat the existing picture as identity/wardrobe/place reference, not binding action geometry. The user explicitly authorized starting over where needed and reinforced that sophisticated GIMP compositing still requires genuinely compatible pieces and visual judgment. The duel was rebuilt from fresh physical blocking and delivered in f3b6c18 after whole/native/peer review; rejected local action experiments remain unpromoted.

The user also caught an unnecessary complexion recast in the S057 bearer repair. The lead had explicitly requested a redheaded replacement while removing a duplicate Serat face; this was a production judgment error, not unavoidable generator drift. b70c759 restores his original dark complexion and black hair with a distinct face. Identity corrections must preserve complexion and continuity with unchanged skin.

The user asked whether the S054 lever was the summoning-chamber control. They are separate source-authored mechanisms: the opening lever closes the passage to Earth, while the citadel release opens the hall's entrance ward. The user liked the narrative echo of someone closing Tessa's escape and her later opening the way for others, then resumed this batch. That response establishes approval of the narrative connection, not a new physical design. The freestanding pedestal and exposed hinge in S054 remain the production team's interpretation of the release behind the throne; the screenplay does not specify their construction.

Current source PNGs are authoritative: the other team's coat, skin, hair, ear, badge, scabbard and lettering fixes supersede old generation masters. Opening repairs go under art/repaints. No game-code/staging/grading/sharedcanon/request edits. Root AGENTS.md has an unrelated pre-existing edit and remains untouched.

Review whole compositions and native contacts, compare recurring scenes, retain meaningful GIMP layers and exact reopened pixels. Alpha/protected-region checks support visual review; they cannot clear bad anatomy, masks or action. Art delivery is not runtime/whole-route experience clearance.

## Handoff checks

A final independent read-only audit mapped every mandatory request item and delivered optional repair to the manifest: 49 mandatory repair outputs, nine optional repair outputs and nine new paintings. The 67 paths exactly match the output PNGs changed between request revision `3b482c8` and source-art commit `a666d88`. S035 alone is marked partial. Committed batch changes stay within prompts, studies, repaints and source scenes.

The [nine-moment contact sheet](new-moments-review.jpg) and [six-frame throne-hall comparison](hall-continuity-review.jpg) were refreshed from the final delivered source PNGs after `a666d88`, including the corrected S057 bearer's complexion and S054 lever glove tear. They are inspection artifacts, not runtime screenshots. The lead compared full final scenes as well as native contacts during production; the sheets support recurring costume/injury/room review. Screenshots of the actual reading interface and route-wide experience remain for integration review. No grading or runtime code/staging was changed in this batch.

S035 remains a required follow-up: the RIGHT support half is delivered, but Renn's pinned-leg/body geometry is not repaired. Two built-in image-generation output-moderation failures produced no child repair. No source improvement is claimed for Renn and no workaround/alternate generation service was used. Optional S004 emblems, S049/S052 scabbard relocations and the ambiguous S049 table support remain unmodified.

Rejected local duel action experiments are retained in `../s054-duel/batch6/` with explicit rejected/superseded status; the actual delivered duel is `../s054-duel/batch6-grip-rebuild/`. Other rejected components remain clearly labelled in their production studies. Preserve this distinction when retrieving assets.
