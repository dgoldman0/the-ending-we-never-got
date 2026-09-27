# Batch 7 — Gray Scar trail, local cast repairs, and stair healer

Production corrections delivered for review; this is not a runtime/user approval. Starts from the current scene PNGs after the other team’s batch 6 repairs. Source hashes were checked against each `before.png` at HEAD `7337709` before promotion.

## S018 cats — item 48

Source lines 795–809: before the northerners arrive, four human soldiers carry an adult woman; Iven and her husband walk beside her. A mule and wrecked wagon block the turn ahead. Tessa catches the young cat dropping at a bearer while Mara drives the other back; the families run downhill to the timber ferryhouse.

The broad repaint keeps the established eight standing adults, their complexions and costume identities, camera relationship, full adult litter, four bearers and two cats. It replaces the sunny lakeside with grey gorge walls and conifers, puts the house visibly downhill, and places the obstruction at the turn ahead of Mara. Tessa’s pose turns toward the falling cat so a curved white shelter visibly catches its paws above the rear bearer. Her head was then corrected locally from the campaign-early portrait and selected storm face, with natural freckles, youthful facial volume and chestnut hair. Her ivory-backed botanical panels were restored in the same donor pass. This is a broad environment/action repaint, not a pixel-identical preservation of the old cast painting.

Native review caught Mara’s outer boot over the new drop; a separately generated ground patch makes a continuous trail under both boots and naturally occludes the nearest background figures. The final 3-layer master preserves the coherent new scene, local Tessa repair, and separate footing correction. The native canvas is 1672×941; the delivery is uniformly resampled to 1920×1081 and clipped by one bottom row.

Whole and native checks: all four litter grips, rigid poles, adult patient and husband, distinct Iven/bearers/Mara, white interception clear of the bearer’s head, Mara’s shield/sword contact and both boots. Gray Scar peer compared Tessa and the environment directly against the repaired S020 and found no continuity blocker. Root independently reopened the whole and native areas and cleared the candidate.

## S011 causeway — item 55

Source lines 488–512: Iven carries eight-year-old Ada; Hest holds six-year-old Renn. Renn now matches the smaller boy in the next sanctuary image: medium-brown skin, black curls, brick shirt, dark trousers and ankle boots. His whole body is about 20% smaller, with one raised arm reaching Hest’s preserved grip. The original mother, surrounding cast, repaired Mara and broken heron remain. An initial donor produced an extra arm and duplicate panel; it is labeled rejected and never used. Native review found remaining old curls beyond the first mask; the final expanded mask removes them completely.

The final 2-layer master changes 58,173 pixels only in bbox [1448,397,1659,791]. Whole/native review checked the old head/boot footprints, hand contact, face/skin consistency and scale against the sanctuary. Root independently cleared it.

## S034 cargo shed — item 56

Source lines 1370–1380: engineers work on the sealed wagons while guards keep Marren outside. Only three heads change. The rear engineer has a distinct broader face with the same original light warm complexion and a matched horn pair; a separate far-horn patch makes the second horn visible beyond his crown. Marren’s original face is retained beneath small rounded horns. The rear-facing guard’s cap has fitted horn openings. Cargo, foreground engineers, tools, axles, documents and all other source pixels remain.

The final 5-layer master changes 13,293 pixels within the three local head masks. Root compared the engineer’s original and revised native face to confirm that this did not recast his complexion, and cleared the horn pair, Marren and cap details.

## Technical evidence

`verification.json` records full SHA256 values and exact reopened-XCF checks. All three delivered PNGs are 1920×1080 RGBA and opaque throughout; reopened visible-layer exports reproduce every RGBA pixel. Technical agreement does not establish artistic or runtime acceptance. Prompts and GIMP assembly scripts are in `art/prompts/batch7-cats-minor/`.

## Additional scoped deliveries

- [S040 mill town](s040-mill-town/README.md), commit `37ce46a`: uneven barrier edge, grounded violet spill and restored radial wheel spokes. Five-layer master; both wardkeeper hands and face unchanged. Root whole/native review recorded.
- [S057 father](s057-father/README.md), commit `b997759`: six background northern cap/horn corrections. Seven-layer master; foreground figures, complexions, Lucan’s smooth horns, litter and human medical attendants unchanged. Root whole/native review recorded.
- [Stair healer portraits](stair-healer/README.md), item 61: independently painted right-speaking and left-listening human healer matching S055 Mara. Root and Gray Scar peer reviewed the whole pair, native alpha edges, and scene identity; source portraits are delivered. Own scene repairs were completed first; root clarified that unrelated duel repairs did not delay these source-independent portraits.

Each additional subgroup retains its own source snapshot where applicable, final candidate, reopened export, GIMP master, prompt/assembly files, exact RGBA checks and review notes. These checks do not establish runtime crop, grading or user approval.

## Local fix after delivery (Claude, 27 September 2026)

`s011-bellweir-causeway.png`: batch 6 took the scabbard off Mara's right hip, but a thin dark stroke of its tip was left across the rock beside her coat (about x 723-734, y 543-571). It is painted out from the rock and ground around it, without sampling her coat. BATCH7 table of `tools/local-repairs.py`; master `art/local-repairs/batch7-check/s011-bellweir-causeway.xcf`.
