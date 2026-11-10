# Batch 9, item 82 — source-art handoff

Six current scene PNGs retain their existing screenplay moments. These repairs use the current runtime source art, with its prior local repairs, rather than older generation masters. No game data, crop, grade or direction tool was changed or run.

| File | Delivered repair | Layered master |
| --- | --- | --- |
| `s050-citadel-lower-stair.png` | Plain weathered grain replaces the repeated pier-face pattern; the small pale sleeve/sky edge is repaired without changing Olan's signal or the embrace. | `../s050-citadel-lower-stair/batch-9-a9pier.xcf` |
| `s052-citadel-inner-landing.png` | The right bronze leaf continues to the threshold. Floor grain replaces the dark stone sliver behind the runner's boot. | `../s052-citadel-inner-landing/batch-9-a9sliver.xcf` is the final composite; `batch-9-a9door1.xcf` preserves the preceding door repair. |
| `s052-entrance-ward.png` | The same right leaf reaches the floor through the dark ward, with no floating lower end. | `../s052-citadel-inner-landing/batch-9-a9door2.xcf` |
| `s053-bend.png` | The hall's high-window light is visible beyond the retreating blue soldiers; taller treads replace the shallow upper flight. **The flight still has more than ten risers: the requested count is unresolved.** | `../s053-bend/batch-9-a9stair.xcf` |
| `s054-lever.png` | Narrow masked repairs remove the beaded edge highlights on the carved-stone throne base and lever housing. | `../s054-throne-hall/batch-9-a9stone.xcf` |
| `s058-final.png` | The short fifth leg under the front chair is removed; its four grounded legs and stretchers remain. | `../s058-bellweir-market-spring/batch-9-a9chair.xcf` |

Built-in generation supplied the pier/sleeve, stone-edge, chair and stair detail renders. GIMP reduced those detail renders to their source areas and transferred only the specified regions through masks. The two bronze door repairs instead clone the existing leaf downward to the floor, and the runner repair clones nearby floor grain. Exact generation prompts remain under the corresponding scene's `art/prompts/` folder. Door clone offset is `(0,110)` with the mask ending at the threshold; floor clone offset is `(-80,-70)`.

Inspected every complete export before its detail crops, then the before/after pairs. Checked the chair's leg count and floor, bronze-to-threshold joins, the runner's boot clearance, Olan's sleeve edge and unchanged hand, the pier grain and seams, lever mechanism and adjacent boots, Mara's approach, the withdrawing soldiers' support and feet, and the high-window light. An earlier stair composite left polygon-shaped sky remnants round the soldiers and was replaced; those edges are absent from the selected export. The anonymous blue pair keeps its supporting action in the repainted flight. The stair's riser count remains a failed continuity check rather than an approved architectural match to S050. Every final XCF reopened in GIMP and reproduced its delivered 1920×1080 PNG exactly.

The optional figure, weapon-side, banner, shield/handrail, paving and brother-horn-alignment changes are left alone: they require additional work outside these small repairs. Source-art inspection does not establish connected game clearance. The remaining stair count belongs in the local-repair or framing handoff, not a new generation batch.
