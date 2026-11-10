# Batch 9 — generated source-art handoff

Delivered **30 runtime PNGs: thirteen repaired scenes, eight new scene paintings and nine new speaking portraits**. The required B7 skip is recorded below. Built-in imagegen supplied new paintings and repair regions; GIMP supplied controlled masks, local texture repairs, transparent canvas room and inspection previews. The files are saved at the requested runtime source paths and committed in their numbered groups. This is source-art delivery, with material failures and integration limits still open.

[`file-manifest.json`](file-manifest.json) records all thirty paths, dimensions, SHA256 hashes, input identities, review records and final layered masters. Part A records the starting PNG hashes from revision `9e2c408`. Exact prompts remain in [`../../prompts/`](../../prompts/). The nine portraits have a separate [reference and native-painting manifest](../portraits-batch-9/file-manifest.json).

## Remaining failures and limits

- **B7 `s015-book.png` is skipped.** The closed winter key does not show the garment beneath Tessa's coat. The request explicitly requires a skip in this case; no garment was invented. See the [skip record](../s015-book/README.md).
- **S053's stair still has more than ten risers.** The two-person approach and broken-shield heap are repaired, and high-window light is visible; the riser count does not match S050. A final trial using a countable ten-riser guide also failed and was excluded. See [item 82](../batch9-item-82/README.md). This needs local correction or restricted framing during integration.
- **All eight new landscapes are native 1672×941**, below the requested 1920×1080 minimum. They were delivered without upscaling. The existing Part A scenes retain their 1920×1080 canvases; only local repair regions were resampled into them.
- **Camera limits remain in B1–B6 and B8.** Background faces in B1 sit high; B2's supporting hands, B3's gutter and B5's bowl contacts sit lower than requested; B3's individual stubs are small; B4's Renn lacks a right margin; B6's stone is narrower than 250 px equivalent and its fist scale lacks a nearby hand comparison. B8's warning is exact but moved into the clear diagram field and reduced in size. The per-scene records give quantities and conditions. These are not cleared by the source-art inspection.
- The optional existing-asset changes were left alone, as recorded in item 82. No additional art batch is proposed.

## Part A — repaired existing paintings

All thirteen current PNGs retain the source compositions and previous local repairs outside the stated masks.

| Request group | Runtime source file(s) | Delivered work and review |
| --- | --- | --- |
| 1 / item 78 | `s019-gray-scar-ferryhouse.png` | Close-swept Lucan horns, slung crossbow and wall-tip wedge. [Review](../s019-gray-scar-ferryhouse/batch-9-review.md). |
| 2 / item 74 | `s021-lucan-returns.png` | Horns and level loaded bow, preserved beneath the subsequent passenger repairs. [Review](../s021-gray-scar-covered-landing/batch-9-item-74-review.md). |
| 3 / item 80 | `s021-serat.png` | Full back of Serat's skull, strap behind the ear. [Review](../s021-gray-scar-covered-landing/batch-9-item-80-review.md). |
| 4 / item 81 | `s034-return-cargo-shed.png` | Third guard's fitted horn cap and green collar. [Review](../s034-return-cargo-shed/batch-9-review.md). |
| 5 / item 75 | `s051-north-infirmary-court.png` | Foreshortened horizontal crossbow prod and string. [Review](../s051-north-infirmary-court/batch-9-review.md). |
| 6 / item 76 | `s021-gray-scar-covered-landing.png`, `s021-lucan-returns.png`, `s021-rescue.png` | Northern adult/child horns and the brown-capped northern boatman. [Review](../s021-gray-scar-covered-landing/batch-9-item-76-review.md). |
| 7 / item 79 | `s021-rescue.png` | Brother's raised temple horns and Serat's spent slung bow. [Review](../s021-gray-scar-covered-landing/batch-9-item-79-review.md). |
| 8 / item 77 | `s053-bend.png` | Fallen stone and broken shields narrow the approach in front of Mara. [Review](../s053-bend/batch-9-item-77-review.md). |
| 9 / item 82 | `s050-citadel-lower-stair.png`, `s052-citadel-inner-landing.png`, `s052-entrance-ward.png`, `s053-bend.png`, `s054-lever.png`, `s058-final.png` | Pier/sleeve edge, bronze leaves to threshold, floor sliver, stair/window repair, stone edge beading and fifth chair leg. Stair count remains unresolved. [Review](../batch9-item-82/README.md). |

The source PNGs are in [`../../../renpy/game/art/scenes/`](../../../renpy/game/art/scenes/). The per-item records describe the complete-screen comparisons, native detail inspection and exact master/export comparisons actually performed.

## Part B — new moments

Each linked brief was written from its screenplay sequence before generation and now includes the finished-painting inspection and camera limits.

| Item | Delivered file | Screenplay line(s) | Brief and inspection |
| --- | --- | --- | --- |
| B1 | `s035-water.png` | 1438–1447 | [The water closes](../s035-water/README.md): Mara holds Tessa on sound south stone, empty water/debris below, Lucan on the surviving northern stone approach. |
| B2 | `s036-sapling.png` | 1514 | [The northern family](../s036-sapling/README.md): mother and son with the wrapped pear sapling beside the recovered father. |
| B3 | `s012-cut-pages.png` | 541 | [Four cut leaves](../s012-cut-pages/README.md): Elin alone, original book, four repaired stubs and translations under one lamp. |
| B4 | `s011-blue-door.png` | 504–509 | [Orren's lantern](../s011-blue-door/README.md): the alley, family and weakening arch before the roof falls, tile beside Iven. |
| B5 | `s006-bowls.png` | 287 | [The burned portion](../s006-bowls/README.md): three bowls, Tessa's exchange and Iven fetching spoons. |
| B6 | `s026-stone.png` | 1126 | [The chalked stone](../s026-stone/README.md): ORREN readable, no readable invented bed number. |
| B7 | **Skipped** | 608–627 | [Winter wardrobe dependency](../s015-book/README.md). |
| B8 | `s047-plan.png` | 1871–1875 | [The plan and letters](../s047-plan/README.md): exact warning, two letters, correct bandaged left forearm. |
| B9 | `s049-bag.png` | 1986 | [Iven's bag](../s049-bag/README.md): raised fastening, healthy short gloves, healer, wagons and left-hip sword. |

The three `scene-reference-pairs-*.png` sheets compare the reference on the left with the delivered scene on the right: B3/B4, B5/B6 and B8/B9 respectively. These are inspection reductions; the source exports retain their native dimensions.

## Part C — speaking portraits

All nine requested files are in [`../../../renpy/game/art/portraits/`](../../../renpy/game/art/portraits/). The [portrait review](../portraits-batch-9/README.md) names each file and expression, with same-set comparisons, all five Tessa faces against the selected reference, and [224×280 oval inspection](../portraits-batch-9/oval-inspection-224x280.png). Each native 1254-square painting is preserved exactly on a 1440-square RGBA canvas with 93 transparent pixels added per edge. No painted pixels were upscaled or expression-edited.

## Verification and integration state

Read the relevant screenplay sequences, character designs, period keys and recurring location notes. Inspected complete paintings and portraits, reference comparisons and native faces, hands, props, horns, weapons, geometry and local repair edges. Selected layered masters were reopened in GIMP and their composites matched the delivered PNGs exactly. All thirty runtime files decode; file counts, dimensions, hashes, portrait alpha, portrait pixel preservation and the absence of B7 were checked. These checks establish file integrity and the recorded source-art observations; the failed count and composition checks remain open above.

No production crop, grading or direction tool was run. Game code, staging data, source screenplay and the asset request were unchanged. No connected playthrough or finished-game visual clearance is claimed. Integration still needs the specified crop/grade/face-finding work and inspection of each changed scene under its actual lines, portraits, text and camera framings. Commits remain local.
