# Asset request

Updated 23 September 2026, after the batch 1 check. The game takes new art without code changes: a file saved at its listed path appears in play once Claude has cropped and graded it. This file says what GPT makes next, where it stops, and what is queued behind that stop.

The user wants better portraits. The S001–S005 cast is being repainted as head-and-shoulders busts, with **one painting per role**, so speaker and listener face each other without mirroring. GPT works one batch at a time, and each batch ends with a stop so Claude can check it in the game before the next one starts. Scene paintings still need a written brief from the screenplay before generation, as [AGENTS.md](../AGENTS.md) requires. Nothing here approves an image or replaces the likeness, wardrobe and lighting references.

## Batch 1: checked 23 September 2026

Claude cropped and graded the eight S001 portraits and checked them in the game at both window sizes, in S001's bright light and Softened:

- **Tessa's four pass.** She is the storm-infirmary woman at nineteen, the same person in all four, with the hoodie right. Each looks the right way, and the expressions read at listener size.
- **Senn's three need repainting.** His clothing and hair are right and he isn't balding, but he reads younger and leaner than his design and than the Senn painted in the same S001 scenes: a handsome man in his early fifties instead of a heavier, rounder-faced man in his late fifties. He's in batch 2 below.
- **The petitioner passes.** She follows her written design (reddish braid, damp gray shawl). The S001 painting of her shows a dark-haired woman in a brown shawl instead; that's the painting's error, listed under corrections.

## Next for GPT: batch 2, the S002 portraits and Senn again, then stop

Twelve portraits. Nine are for S002, the first night: Mara brings supper to the apartment, and Tessa asks to be taken somewhere high enough to get a phone signal, then tries to leave. Three replace batch 1's Senn.

| File in `renpy/game/art/portraits/` | Who and moment | Looks toward | Used with these lines |
| --- | --- | --- | --- |
| `tessa-resolute-arrival-cloak-speaking.png` | Tessa pressing, restless, determined to get a signal | screen right | "That tower over there. Can you take me up?" · "We've got candles." · "I just want to make a call. You can come with me." |
| `tessa-resolute-arrival-cloak-listening.png` | Tessa unconvinced, already looking for another way | screen left | Mara: "The stairs aren't lit." |
| `tessa-attentive-arrival-cloak-listening.png` | Tessa listening, hopeful, holding on to Mara's answer | screen left | Mara: "In the morning. I'll have to find someone with a key." |
| `tessa-hurt-arrival-cloak-listening.png` | Tessa stung: she has just been told she's confined | screen left | Mara: "I have orders to keep you in this room tonight." |
| `tessa-hurt-arrival-cloak-speaking.png` | Tessa asking, her voice close to breaking | screen right | "And tomorrow?" |
| `tessa-hurt-arrival-speaking.png` | Tessa, cloak gone, cold and bitter, handing it back | screen right | "Take that with you." |
| `mara-controlled-speaking.png` | Mara level and polite, giving nothing | screen right | "In the morning. I'll have to find someone with a key." · "The stairs aren't lit." · "I have orders to keep you in this room tonight." |
| `mara-controlled-listening.png` | Mara hearing the requests, composed, already refusing | screen left | "That tower over there. Can you take me up?" · "I just want to make a call." |
| `mara-uneasy-listening.png` | Mara unable to answer; her eyes go toward the guard | screen left | "We've got candles." · "And tomorrow?" · "Take that with you." |
| `senn-assuring-speaking.png` | Senn, patient and persuasive (replaces batch 1's) | screen right | as in batch 1 |
| `senn-attentive-listening.png` | Senn, courteous, measured attention (replaces batch 1's) | screen left | as in batch 1 |
| `senn-evasive-listening.png` | Senn composed, eyes sliding away (replaces batch 1's) | screen left | as in batch 1 |

**The people**
- **Tessa, nineteen, the same girl as batch 1.** Match her face, hair and hoodie to [her batch 1 portraits](../renpy/game/art/portraits/tessa-resolute-arrival-speaking.png). In the first six rows ("arrival-cloak") she wears Mara's gray wool cloak over the hoodie, draped over her shoulders with its hood down. In "Take that with you" she has pulled the cloak off, so she's back in the plain hoodie. It's night and she's exhausted and frightened: a little more drawn than in S001, hair coming loose. "Hurt" means emotionally hurt; she has no injury.
- **Mara, thirty-two, captain.** Medium olive-brown skin, squared jaw, slightly heavy eyelids, hazel eyes, a strong nose with a modest bend, and thick dark-brown hair braided and pinned low at the nape. She wears her slate-blue military coat buttoned to a stand collar, with a narrow brass captain's bar at the collar and a white shirt collar showing. She should read as an adult in her thirties, not an elderly veteran, and match the Mara painted in [the S002 scenes](../renpy/game/art/lit/night-exchange-softened.webp). Her control is courteous, not cold; the unease shows only in her eyes.
- **Senn, late fifties.** Keep batch 1's robes and brushed-back gray hair, but paint the man in his design: a rounded build, a fuller, heavier face with soft jowls, and a fuller short gray-white beard. He should read as the same man painted in [the S001 scenes](../renpy/game/art/softened/opening/cg/pleading-mother.png), older and heavier than batch 1's. Still not balding.

**The format** is unchanged from batch 1, matching GPT's Lucan and Valcair busts ([example](../renpy/game/art/portraits/lucan-early-speaking.png)).
- Square, 1254×1254 or larger, with a transparent background.
- Head, shoulders and upper chest, in three-quarter view. The face, hairline to chin, is about a third of the image height, with clear space above the head and on both sides so the game's crop has room.
- `-speaking` files look toward screen right, lips parted mid-word. `-listening` files look toward screen left, not speaking.
- **Paint each file in its own direction.** A mirrored copy flips the face, the hair and the clasp, and the user finds mirrored portraits awkward.
- Even, neutral light with no strong color cast; the game adds each scene's glare or darkness. Keep hands out of frame, with no text, frame or border.
- Expressions must still read at 150 px wide, the size of the listener's window.

**Save, then stop**
1. Save the twelve files at the paths above, replacing batch 1's three Senn files, and the prompts in `art/prompts/portraits-batch-2/`.
2. Compare them side by side before finishing: Tessa against her batch 1 portraits, and each character's files for the same face, clothes, light and scale, each looking the right way.
3. **Stop there.** Don't start batch 3, don't run the crop or grading tools, and don't change game code, data or other documents. Tell the user batch 2 is ready for Claude to check.

## Queued behind the check

Each batch ends with the same stop. Claude releases the next batch after checking the last, adding a detailed brief like batch 2's. `python3 visual-novel/tools/check-staging.py --missing` lists every file still awaited, by batch. In these names, "hurt" means emotionally hurt; Tessa has no injury before the final campaign.

**Batch 3: S003, the first treatment, and the Bellweir pages (14 files).** Tessa wears the early working dress seen in the S003 paintings. Iven wears his olive coat with the cream treatment apron. The priest, Olan and the mother complete the scene. `tessa-resolute-working-speaking` and `olan-listening` serve later chapters.
- `tessa-attentive-working-speaking`, `tessa-attentive-working-listening`, `tessa-startled-working-speaking`, `tessa-hurt-working-speaking`, `tessa-hurt-working-listening`, `tessa-resolute-working-speaking`
- `iven-attentive-treatment-speaking`, `iven-attentive-treatment-listening`, `iven-concerned-treatment-speaking`, `iven-concerned-treatment-listening`
- `priest-speaking`, `olan-speaking`, `olan-listening`, `mother-speaking`

**Batch 4: S004 and S005, the ceremony and the window (14 files).** Tessa wears the formal Saint coat, mantle and twelve-ray badge. Iven wears his olive coat without the apron. Orra, the messenger and one more Senn complete the set.
- `tessa-attentive-formal-speaking`, `tessa-attentive-formal-listening`, `tessa-hurt-formal-speaking`, `tessa-hurt-formal-listening`, `tessa-resolute-formal-speaking`, `tessa-resolute-formal-listening`
- `iven-attentive-speaking`, `iven-attentive-listening`, `iven-concerned-speaking`, `iven-concerned-listening`
- `orra-speaking`, `orra-listening`, `messenger-speaking`, `senn-evasive-speaking`

**After batch 4: portrait sets for S006 onward.** These follow the same format, one `-speaking` and one `-listening` painting per set. The game uses a set once its scene has a painting, and on book pages right away: the speaker in the left margin, the listener in the right.

| Portrait set | Scenes | Lines | Status |
| --- | --- | ---: | --- |
| `lucan-early` | S018–S036 (13) | 36 | done |
| `valcair` (field armor) / `valcair-private` | S010–S054 (5) | 28 | armor done; private awaited |
| `lucan-later` | S038–S057 (8) | 23 | done |
| `tessa-harrow` | S032–S037 (4) | 20 | costume to design first |
| `vask` | S010–S057 (4) | 19 |  |
| `tessa-campaign` | S040–S049 (4) | 16 |  |
| `tessa-campaign-early` | S019–S030 (6) | 15 | costume to design first |
| `marren` | S038–S048 (4) | 12 |  |
| `elin` | S008–S016 (4) | 11 |  |
| `hest` | S011–S037 (4) | 9 |  |
| `tessa-winter` | S014–S017 (3) | 9 | costume to design first |
| `elin-later` | S040–S058 (5) | 7 |  |
| `boatman` | S021–S043 (3) | 6 |  |
| `orren` | S008–S058 (5) | 5 |  |
| `mara-campaign` | S036–S049 (5) | 5 |  |
| `scholar` | S013 (1) | 4 |  |
| `governor` | S027 (1) | 4 |  |
| `serat` | S045–S051 (3) | 4 |  |
| `tessa-citadel` | S050–S054 (3) | 4 |  |
| `tessa-injured` | S055–S056 (2) | 4 |  |
| `picket-officer` | S022 (1) | 3 |  |
| `tessa-postwar` | S058 (1) | 3 | costume to design first |
| `ada` | S008–S014 (2) | 2 |  |
| `apprentice` | S026–S030 (2) | 2 |  |
| `camp-healer` | S027–S055 (2) | 2 |  |
| `bargeman` | S031 (1) | 2 |  |
| `iven-harrow` | S032–S035 (2) | 2 |  |
| `departing-captain` | S047 (1) | 2 |  |
| `mara-citadel` | S050 (1) | 2 |  |
| `warden` | S006 (1) | 1 |  |
| `archivist` | S012 (1) | 1 |  |
| `ferryman` | S019 (1) | 1 |  |
| `escort` | S044 (1) | 1 |  |
| `runner` | S052 (1) | 1 |  |
| `surgeon` | S056 (1) | 1 |  |

- **Show age and wear.** Tessa ages from 19 to about 23; later sets show accumulated war wear, as `AGENTS.md` describes. `tessa-injured` and `tessa-postwar` carry the right-hand injury; earlier sets keep both hands healthy.
- **Some Tessa costumes need design first.** The winter, Gray Scar–Harrow and postwar costumes are marked still to develop in [the character designs](../../characters/original-visuals.md).
- **Small roles can wait.** The speaker's name still identifies them without a portrait. `camp-healer` covers the S027 and S055 healers; split it if S055's healer is a separate attendant.

**Then: one establishing painting per scene.** One painting per scene is the baseline: it puts the scene on its picture, with portraits carrying the exchanges, as S005's window scene does. S053 continues S050 on the same stair, so it reuses that painting.

| File (`art/scenes/`) | Scene | Place and time | Default light | Speakers |
| --- | --- | --- | --- | --- |
| `s006-convoy-camp.png` | S006 | Convoy Camp · Afternoon | ordinary | Iven, Mara, Tessa, Warden |
| `s007-roadside-inn.png` | S007 | Roadside Inn · Night | dismal (night) | Iven, Mara, Tessa |
| `s008-bellweir-market.png` | S008 | Bellweir · Market Square · Day | ordinary | Ada, Elin, Iven, Orren, Tessa |
| `s009-bellweir-river.png` | S009 | River below Bellweir · Late Afternoon | ordinary | Iven, Mara, Tessa |
| `s010-bellweir-hills.png` | S010 | Hills above Bellweir · Night | dismal (night) | Valcair, Vask |
| `s011-bellweir-causeway.png` | S011 | Bellweir · East Causeway · Night | dismal (night) | Hest, Iven, Mara, Tessa |
| `s012-temple-reading-room.png` | S012 | Temple Reading Room · Night | dismal (night) | Archivist |
| `s013-summoning-chamber-later.png` | S013 | Summoning Chamber · Later | ordinary | Elin, Scholar |
| `s014-relief-warehouse.png` | S014 | Relief Warehouse · Winter Morning | ordinary | Ada, Hest, Tessa |
| `s015-elin-lodging.png` | S015 | Elin's Lodging · Day | ordinary | Elin, Tessa |
| `s016-council-room.png` | S016 | Palace Council Room · Day | ordinary | Elin, Mara, Orra, Senn, Tessa |
| `s017-council-corridor.png` | S017 | Palace Council Corridor · Continuous | ordinary | Mara, Tessa |
| `s018-gray-scar-ferry-approach.png` | S018 | Gray Scar · Ferry Approach · Afternoon | ordinary | Lucan, Mara |
| `s019-gray-scar-ferryhouse.png` | S019 | Old Ferryhouse · Continuous | ordinary | Ferryman, Lucan, Mara, Tessa |
| `s020-gray-scar-riverbank.png` | S020 | Gray Scar · Riverbank · Continuous | ordinary | — |
| `s021-gray-scar-covered-landing.png` | S021 | Gray Scar · Covered Landing · Continuous | ordinary | Boatman, Iven, Lucan, Tessa |
| `s022-river-picket.png` | S022 | Rovel River Picket · Dusk | ordinary | Iven, Lucan, Mara, Picket Officer, Tessa |
| `s023-northern-field-quarters.png` | S023 | Northern Field Quarters · Night | dismal (night) | Lucan, Valcair |
| `s024-northern-wharf.png` | S024 | Northern Wharf · Morning | ordinary | Boatman, Lucan |
| `s025-royal-infirmary-corridor.png` | S025 | Royal Infirmary · Corridor · Day | ordinary | Mara, Orra, Tessa |
| `s026-quarry-loading-ramp.png` | S026 | Quarry Camp · Loading Ramp · Day | ordinary | Apprentice, Lucan |
| `s027-river-camp-gate.png` | S027 | River Camp · Gate · Day | ordinary | Governor, Healer, Lucan, Tessa |
| `s028-river-camp-infirmary.png` | S028 | River Camp · Infirmary · Continuous | ordinary | Hest, Orren |
| `s029-river-camps-visits.png` | S029 | River Camps · Successive Visits | ordinary | — |
| `s030-river-camp-infirmary-evening.png` | S030 | River Camp · Infirmary · Evening | ordinary | Apprentice, Lucan, Orren, Tessa |
| `s031-grain-wharf.png` | S031 | Northern Grain Wharf · Autumn Morning | ordinary | Bargeman, Lucan |
| `s032-harrow-bridge.png` | S032 | Harrow Ford · Covered Bridge · Day | ordinary | Iven, Lucan, Tessa |
| `s033-valcair-war-room.png` | S033 | Valcair's War Room · Night | dismal (night) | Valcair, Vask |
| `s034-return-cargo-shed.png` | S034 | Return-cargo Shed · Before Dawn | ordinary | — |
| `s035-harrow-bridge-crossing.png` | S035 | Harrow Ford · Covered Bridge · Day | ordinary | Iven, Lucan, Orren, Tessa |
| `s036-harrow-south-bank.png` | S036 | Harrow Ford · South Bank · Late Afternoon | ordinary | Lucan, Mara, Tessa |
| `s037-relief-camp.png` | S037 | Relief Camp · Night | dismal (night) | Hest, Mara, Tessa |
| `s038-northern-stores-office.png` | S038 | Northern Stores Office · Two Weeks after Harrow | ordinary | Lucan, Marren, Vask |
| `s039-northern-river-town.png` | S039 | Northern River Town · Weeks Later | ordinary | — |
| `s040-mill-town.png` | S040 | Occupied Mill Town · Winter · Day | ordinary | Elin, Mara, Tessa |
| `s041-curse-tower.png` | S041 | Curse Tower · Continuous | ordinary | — |
| `s042-mill-town-later.png` | S042 | Mill Town · Later | ordinary | Mara, Tessa |
| `s043-river-provinces.png` | S043 | River Provinces · Changing Seasons | ordinary | Boatman, Lucan |
| `s044-upper-stores-landing.png` | S044 | Upper Stores · River Landing · Dawn | ordinary | Escort, Lucan, Marren |
| `s045-citadel-north-infirmary.png` | S045 | Citadel · North Infirmary · Morning | ordinary | Lucan, Marren, Serat |
| `s046-valcair-private-room.png` | S046 | Valcair's Private Room · Night | dismal (night) | Lucan, Valcair |
| `s047-citadel-north-infirmary-before-dawn.png` | S047 | Citadel · North Infirmary · Before Dawn | ordinary | Captain, Lucan, Serat |
| `s048-examination-tent.png` | S048 | Forward Camp · Examination Tent · Day | ordinary | Elin, Marren, Tessa |
| `s049-command-tent.png` | S049 | Forward Command Tent · Night | dismal (night) | Elin, Mara, Olan, Orra, Tessa |
| `s050-citadel-lower-stair.png` | S050 | Citadel · Lower Stair · Pre-dawn | ordinary | Mara, Tessa |
| `s051-north-infirmary-court.png` | S051 | Citadel · North Infirmary Court · Dawn | ordinary | Serat |
| `s052-citadel-inner-landing.png` | S052 | Citadel · Inner Landing · Dawn | ordinary | Elin, Runner, Tessa |
| s050-citadel-lower-stair.png (reused) | S053 | Citadel · Lower Stair · Continuous | ordinary | — |
| `s054-throne-hall.png` | S054 | Citadel · Throne Hall · Continuous | ordinary | Tessa, Valcair |
| `s055-citadel-lower-stair-morning.png` | S055 | Citadel · Lower Stair · Morning | ordinary | Healer, Lucan, Tessa |
| `s056-north-infirmary.png` | S056 | North Infirmary · Day | ordinary | Surgeon, Tessa |
| `s057-citadel-lower-gate.png` | S057 | Citadel · Lower Gate · Evening | ordinary | Lucan, Vask |
| `s058-bellweir-market-spring.png` | S058 | Bellweir · Market Square · Spring Day | ordinary | Elin, Orren, Tessa |


Places that recur must stay recognizable across states: the Bellweir market is intact (S008), destroyed (S011) and rebuilt (S058). The [intact heron study](scene-studies/bellweir-heron/README.md) is a working reference for the first.


**Then: key-moment paintings.** Some beats fail as one held painting. They need their own images, added as extra stages in `staging.json`, each with a scene brief written from the screenplay first. From the [outline](../outline.md):

- **S009:** Iven's portrait drawing on the boat; learning to row with Mara.
- **S011:** the sanctuary over the evacuation; the cut to the boots, cap and search portrait.
- **S016:** the hearing needs door and speaker staging across the room, not a single view.
- **S021:** the rescue geography (ferryhouse, bank, gate, shelter, two boats); Lucan's return for the litter as a held decision beat.
- **S029 and S043:** the montages need a few small views each (cap, leg support, launch, quarry refusal, barge; then the three seasons).
- **S030:** the laughing-portrait interaction.
- **S035–S036:** the intact crossing, the midspan collapse and the southern remnant; Iven's death; the held sleeve and coat afterward.
- **S041–S042:** the wardkeeper; the cart aftermath, the unsheathable sword and Tessa taking Mara's hand.
- **S050:** Tessa fastening Mara's trembling guard.
- **S052–S054:** the entrance ward and the throne-hall fight in a few legible states, including the right-hand wound and the sword changing to her left hand.
- **S055:** finding Mara.
- **S056:** the hand examination, anchored by the storm-infirmary study.
- **S058:** the final Bellweir interaction and the fade before the question.

## Reference: how the game uses the files

| Kind | Path under `renpy/game/` | Size | Then Claude runs |
| --- | --- | --- | --- |
| Portrait | `art/portraits/<name>.png` | square, at least 1254×1254, head and shoulders | `tools/crop-portraits.py`, then `tools/grade-light.py --portraits` |
| Scene painting | `art/scenes/<file>.png` | 16:9, at least 1920×1080; 2560×1440 preferred | `tools/grade-light.py` |

- **Deliver neutral images.** `grade-light.py` renders every painting and portrait into its light register, bright, ordinary or night, in both Intense and Softened. The distortion is permanent in the image. So paint real light with its direction and sources in even, readable exposure. Don't bake in glare or darkness, and don't make Softened versions.
- **Portraits are cropped, not cut out.** `crop-portraits.py` crops each painted bust in GIMP to one composition: the face 46% of the crop's height, the head centred on its silhouette with a little headroom above the hair and a little room on the side it looks toward, so hair, collar and shoulders show. The crop sits in a closed laurel window, 228×256 for the speaker and 150×168 for the listener.
- **Names decide direction.** A `-speaking` file must look toward screen right and a `-listening` file toward screen left. [portrait-plan.json](../renpy/game/portrait-plan.json) maps the S001–S005 plan's expressions to these names; [staging.json](../renpy/game/staging.json) names each later scene's paintings and portrait sets.
- **Stand-ins go as files arrive.** Until a scene's painted portraits exist, the game shows the old head crops, mirrored where needed. Each new file replaces its stand-in.

## Reference: composition rules for scene paintings

- **Keep key action out of the bottom strip.** On every line, the bottom fifth of the screen (below about y = 840 of 1080) sits under the reading shade. Faces, hands, contact points and plot props belong above it.
- **Keep the lower-left corner clear during conversations.** The portrait windows occupy about x 116–516, y 748–1004.
- **Leave room at the top.** The game can lift a painting up to about 70 px to clear the text, so no face should touch the top edge.
- **Leave a quiet area where it helps.** A quiet dark area, such as one side of a night interior, lets a single line sit inside the picture, as the S002 drawing beats do.
- **Paint the light, not the grade.** Place windows, lamps and candles so the register has sources to work with. The light column in the painting table is only a default from the scene heading; set the register in each scene's brief.

## Corrections to existing art

Found while building and reviewing the new screens:

1. **Done locally:** the dead-phone detail was nearly black. Look closer details are now graded at reduced strength, so the phone's edge and dead screen read while the image stays nocturnal.
2. **The arrival foot meets the text.** In `art/opening/cg/arrival.png`, Tessa's landing foot sits where the reading text begins, and the game lifts the painting 70 px to compensate. A recomposition with the foot higher would remove the lift.
3. **Iven's position below the dais falls under the text.** In `art/rovel/cg/ceremony-intervention.png` and `ceremony-yield.png`, Iven's boots and the step edge between him and the dais sit under the reading shade, so the staging point is weakened. Lifting the painting cut off Orra's and Senn's heads instead, so the fix belongs in the painting: keep the step edge above y ≈ 820.
4. **The petitioner is painted as a different woman.** In `art/opening/cg/pleading-mother.png` and `woman-release.png`, the woman who catches Senn's sleeve has dark curly hair in a bun and a brown shawl. Her design, and her portrait, give her a reddish braid and a damp gray shawl. Correct the paintings to the design.
5. **Existing paintings are a little soft.** S001–S005 are 1672×941, upscaled to 1080p. Regenerate new work at 1920×1080 or larger.

## Needed, but not images

- **Look closer beyond the first three threads needs writing before art.** The R02–R05 threads in [investigation.md](../investigation.md) need authored material before any detail images are made.
- **The game has no sound.** Music, ambience and sound effects don't exist yet.
- **The final "Yes" is deferred.** The response to the final question stays deferred, as the brief says.
