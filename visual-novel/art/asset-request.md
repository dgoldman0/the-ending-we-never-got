# Asset request

Updated 23 September 2026, after the batch 4 check. The game takes new art without code changes: a file saved at its listed path appears in play once Claude has cropped and graded it. This file says what GPT makes next, where it stops, and what is queued behind that stop.

The user wants better portraits. The cast is being painted as head-and-shoulders busts, with **one painting per role**, so speaker and listener face each other without mirroring. Batches 1–3 came through with the format, direction and scale right every time; the faults were individual faces and clothes. So the batches are now much larger, in parts with one stop at the end, and GPT checks its own work against the list below as it goes. **Batch 5, the last portrait batch, is Tessa in the costumes the user chooses**; it starts once the user has chosen. Scene paintings still need a written brief from the screenplay before generation, as [AGENTS.md](../AGENTS.md) requires. Nothing here approves an image or replaces the likeness, wardrobe and lighting references.

## Checked so far

- **Batch 1 (S001), checked 23 September.** Tessa's four and the petitioner passed. Senn's three were off-model, younger and leaner than his design and the painted Senn, and were repainted in batch 2. The S001 petition painting shows the petitioner as a different woman; see corrections.
- **Batch 2 (S002 and Senn again), checked 23 September.** All twelve pass. Tessa is the same girl in Mara's cloak and then without it; Mara matches her design and the Mara painted in S002; the new Senn is the heavier, older man in the paintings.
- **Batch 3 (S003), checked 23 September.** Played through every S003 line in the game. The priest, Olan, the mother and Iven's four match their designs and the S003 paintings, and every pair faces each other. Iven's apron is in all four paintings; it sits low on his chest, below the game's crop. The working-dress Tessa drifts toward a made-up look (shaped brows, eyeliner, fuller glossy lips, smoothed skin, fewer freckles, redder hair) against [her likeness reference](character-references/tessa/north-infirmary-face.png) and her batch 1 portraits, most in the two listening files and `tessa-resolute-working-speaking`; those three are repainted in part C below.
- **Batch 4, first start, stopped 23 September.** The user rejected Tessa's layered ceremonial costume when GPT's first drafts showed it at bust size ("a shawl on a blue thing on a blueish thing"). The fault was the costume design, carried over unexamined, not GPT's painting. The partial work is kept in the git stash "Batch 4 partial (GPT, stopped 23 Sep)"; its four good files were restored into batch 4.
- **Batch 4, checked 23 September.** All 62 portraits and the costume proposals arrived. Played every line that uses them in the game, and compared each character's new files with the ones already in it. Every new face matches its written design, and the returning cast (Iven, Mara, Olan, Senn, Valcair, Orra, the messenger) matches their earlier portraits; every pair faces each other. The three Tessa repaints now match her likeness reference: freckles, natural brows, no makeup. That leaves her three S003 *speaking* files looking more polished than the listening files they alternate with, so they are repainted in batch 5. Claude fixed the crops locally: the face detector had locked onto a shirt collar or part of a face in `iven-harrow-speaking`, `iven-attentive-listening` and `olan-soldier-listening`, and had framed `iven-concerned-listening`, `olan-soldier-speaking` and four older portraits (Olan, Serat and two of Tessa's) tighter than the rest of their sets.

## Next for GPT: batch 5, Tessa's costumes and portraits, in four parts

Part A doesn't depend on any costume. Part B redesigns four of Tessa's costumes and **stops for the user to choose**. Parts C and D paint her portraits in the chosen costumes. Commit at the end of each part.

**Before sending:** the user still has to decide what sets the Saint's vestments apart (part B, item 1). Fill that in first.

### What the user decided about the batch 4 proposals

- **Ceremony: redo as Saint's attire.** The closed lapis robe reads as a good dress with a mantle behind it. The user expects the ceremony to put her in the Saint's vestments, not "a shawl on top of a nice dress"; her working and field clothes can be different. The direction is white and gold, the temple's own colours: a full-length sacred robe with the twelve-ray sun worked into it, and the white mantle as a heavy ceremonial cloak fastened across the chest with the badge, the main piece of the outfit rather than a shawl. Something beyond that should set the Saint apart, in keeping with the worldbuilding. It is not the summoning circle.
- **No green for Tessa.** Green is the northern side's colour in the written designs (Lucan, Serat, the northern captains, the governor); the human army wears blues, the temple white, cream, gold and lapis. The winter and field proposals were green only because the brief asked for outfits that differ from each other; make them differ by shape and trim instead.
- **Winter:** keep the one-piece lined coat with its own roll collar, in a human-side colour.
- **Gray Scar to Harrow:** too plain; only the small badge marks her as the Saint. Redesign.
- **Campaign:** the existing coat still stacks an ivory under-tunic with its own collar inside an open coat. Redesign as one garment.
- **Postwar:** the plum wrap robe stays as proposed.

### Before painting: the self-check

These are the faults found so far. Check every file against them before saving it, and compare each finished set side by side before committing a part.

1. **The face matches the written design and the character in the paintings,** not merely the last portrait. Batch 1 made Senn younger and leaner than his design; batch 3 gave Tessa makeup.
2. **No makeup or glamour.** No eyeliner, shaped brows or glossy lips on anyone who wouldn't wear them. Keep freckles, uneven skin and ordinary features. For Tessa, compare every file with [the face reference](character-references/tessa/north-infirmary-face.png) and [her arrival portrait](../renpy/game/art/portraits/tessa-resolute-arrival-speaking.png).
3. **The clothes match the period and the design, and the design itself makes sense.** A costume should read as one outfit at bust size, not as layers stacked on the wearer. If a design written here looks wrong once it's painted, stop that file and say so; don't paint around it. That is how the ceremonial Tessa should have been caught.
4. **Each file is painted in its own direction.** `-speaking` looks toward screen right with lips parted mid-word; `-listening` looks toward screen left, not speaking. Never mirror: a flipped copy moves the hair part, horn shapes, clasps and badges to the wrong side.
5. **Both files of a set are plainly the same person in the same clothes,** with the same horns, scars and hair.
6. **Age is right.** Tessa's ages are given with each set.
7. **Horns follow each design.** Northern characters have individual horn shapes; the humans have none; helmets have openings for horns.
8. **The expression reads at 150 px wide,** the listener's window.
9. **Colours keep sides apart.** Green is the northern side's; don't put Tessa or the human cast in it.

### The format

Unchanged since batch 1, matching the Lucan and Valcair busts ([example](../renpy/game/art/portraits/lucan-early-speaking.png)).
- Square, 1254×1254 or larger, with a transparent background.
- Head, shoulders and upper chest in three-quarter view. The face, hairline to chin, is about a third of the image height, with clear space above the head and on both sides for the game's crop.
- Even, neutral light with no strong colour cast; the game adds each scene's glare or darkness. Keep hands out of frame, with no text, frame or border.
- Paint from the written design. Use an existing portrait or painting only as an identity reference, and never edit a rejected file into its replacement.

### Part A: three S003 repaints, working dress unchanged (3 files)

The batch 4 repaints brought Tessa's S003 listening files back to her likeness reference. Repaint the three S003 speaking files the same way, so she doesn't change between lines: no liner, natural straight brows, ordinary lips, freckles kept, chestnut hair not red. Keep each file's moment and direction from batch 3 and the working dress exactly as it is. Use [the face reference](character-references/tessa/north-infirmary-face.png) and the new [`tessa-resolute-working-speaking`](../renpy/game/art/portraits/tessa-resolute-working-speaking.png) as identity references.

- `tessa-startled-working-speaking.png`: "I've never done this on a person."
- `tessa-hurt-working-speaking.png`: "And if they brought the wrong person?"
- `tessa-attentive-working-speaking.png`: "And his fingers?"

### Part B: four costume redesigns, then stop for the user

As in batch 4 part A, make for each a full-figure image on a neutral background (1024×1536 or larger) with a GIMP XCF, a bust view in the portrait framing, and a short `.md` in `art/character-keys/tessa/` giving the construction, the story period and your review. Keep the rule: one main garment per outfit with its own silhouette and neckline, only the layers the story needs, and every outfit distinguishable at bust size. Paint from the written design; don't feed in the rejected keys as clothing references.

1. **The Saint's vestments, `saint-vestments.md` (S004–S005; the mantle again at the hearing, S016), Tessa at nineteen.** Follow the user's direction above: white and gold, a full-length sacred robe with the twelve-ray sun worked into it, and a heavy white ceremonial cloak fastened across the chest with the badge as the main piece. What sets the Saint apart: **[the user's choice goes here]**. It must still work in the story: Senn pins the badge and settles the mantle on her; at the hearing she wears the mantle over her winter coat, pulls it loose and leaves it across the book. Keep it clearly different from Senn's cream priest's robes with sunburst collar and cuffs. No crown. She is wearing it against her will.
2. **Winter, `winter.md` (S014–S017), about twenty.** The batch 4 shape in a human-side colour, not green.
3. **Gray Scar to Harrow, `gray-scar-harrow.md` (S019–S037), about twenty to twenty-one.** One practical field garment with trousers and boots, repaired and worn, in a human-side colour, that still reads as the Saint's: carry the woven botanical trim of her working dress and the temple badge, not a plain work tunic.
4. **Campaign, `campaign-coat.md` (S040–S054), about twenty-three.** One coat closed to the throat with its own collar, no separate inner collar or shirt front showing; keep the blue-gray, the narrow worn borders, trousers, calf boots, short gloves and the sword belt at her left hip. War-worn face.

Commit part B, then **stop and ask the user to choose.** Record the choices here, then continue with parts C and D.

### Part C: S004 and S005 in the Saint's vestments (6 files)

Tessa is nineteen, in the chosen vestments, displayed against her will; the scene and people are as in batch 4 part B.

| File in `renpy/game/art/portraits/` | Who and moment | Looks toward | Used with these lines |
| --- | --- | --- | --- |
| `tessa-attentive-formal-speaking.png` | Tessa, quiet and grateful, then asking | screen right | "You bought me an afternoon." · "Are you coming with me?" |
| `tessa-attentive-formal-listening.png` | Tessa taking in what she's told | screen left | Senn: "Tomorrow our Saint leaves with the Bellweir convoy…" · Iven: "At least that." · "Let me speak to her." · "All the way there and back." |
| `tessa-hurt-formal-speaking.png` | Tessa betrayed and upset | screen right | "Tomorrow? You said I was coming to see Olan." · "She's still down there. What am I supposed to tell her?" |
| `tessa-hurt-formal-listening.png` | Tessa stung | screen left | Senn: "He's here. Sit down; they're trying to welcome you." · Iven: "I don't know how to stop that." |
| `tessa-resolute-formal-speaking.png` | Tessa confronting Senn | screen right | "Look at me. When did I agree to go?" |
| `tessa-resolute-formal-listening.png` | Tessa holding her ground | screen left | Senn: "We can talk afterward." |

### Part D: the later Tessa sets (7 sets, 14 files)

Each set is `<set>-speaking.png` (looks toward screen right) and `<set>-listening.png` (looks toward screen left), in the chosen costume for its period. She ages from nineteen to about twenty-three and the war shows more in each: drawn cheeks, tired eyes, weathered skin, less tended hair, never glamour. Iven dies at Harrow (S035); Mara dies on the citadel stair (S055); the right-hand injury comes in the throne hall (S054).

| Set | Age, costume and state | Speaking moment | Listening moment |
| --- | --- | --- | --- |
| `tessa-winter` | About twenty, the winter costume; the first winter, searching for a way home | Pressing and hurt: "You knew I wanted to leave." · "And you stood in the door." | Taking in what Elin found about the passage |
| `tessa-campaign-early` | About twenty, the Gray Scar to Harrow costume with the badge, capable and tired; rescues on the river | Urgent and in charge: "Bring her here, beside the litter. The others too." · "Even if it's bad, tell her. Please." | Steady, listening for what's needed |
| `tessa-harrow` | About twenty-one, the same costume wet and dirty from the bridge, in the hours after Iven's death | Raw, accusing: "You said you'd be with us." · "I know about the boards!" | Stunned, barely holding on |
| `tessa-campaign` | About twenty-three, the campaign costume, before the final assault; Iven is dead, Mara alive | Steady and hard: "Why did you sign it?" · "I want Iven." | Listening as a commander, guarded |
| `tessa-citadel` | The morning of the assault: the campaign costume with short gloves and sword belt, hair tied tight, stair dust; both hands still healthy | Pleading, then cold: "When he calls, you come up. Promise me." · "Your seal was on the bridge." | Tense, listening for danger |
| `tessa-injured` | After the throne hall and on the stair where she finds Mara: the same clothes torn and dirty, her right hand wounded and kept out of frame; shock and grief, no triumph | Barely voiced: "Mara." · "That's the one I draw with." | Numb, hearing the surgeon |
| `tessa-postwar` | About twenty-three, the postwar clothes, the brace on her right hand kept out of frame; visibly aged by the war, grieving, no smile | Quiet, determined: "Does it say whether the pages are there?" · "Don't go without me when they answer." | Listening, far away |

### Save, commit, then stop

1. Save each file at its path, and the prompts in `art/prompts/portraits-batch-5/` (part B's in `art/prompts/characters/`).
2. Before each commit, lay the part's files side by side with Tessa's earlier portraits and her face reference, and go through the self-check.
3. Commit at the end of each part, naming the files in the message.
4. **Stop after part B for the user's choices, and again after part D.** Don't run the crop or grading tools, and don't change game code, data or other documents. Tell the user batch 5 is ready for Claude to check.

**How Claude checks it.** `tools/review-portraits.py` crops and grades every portrait, plays each line that uses them in the game headless, and lays out contact sheets of the lines and side-by-side sheets of each character, new files marked. Claude then looks at the sheets and full screens.

## Queued behind the check

**Already done:** every portrait set except Tessa's batch 5 files: the S001–S005 cast, `lucan-early`, `lucan-later`, `valcair` and the 27 later sets of batch 4.

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
5. **Nine S004–S005 paintings show the rejected ceremonial outfit** (the open lapis coat over the pale green under-robe): `ceremony-dais`, `-intervention`, `-mantle`, `-refusal`, `-refused-chair` and `-yield`, and `window-packing`, `-pause` and `-together`. White-and-gold vestments are a change of the whole figure, not a recolour, so they need repainting in the chosen vestments once the user has chosen. For the window scene, decide from the screenplay whether she is still wearing the mantle afterward.
6. **Existing paintings are a little soft.** S001–S005 are 1672×941, upscaled to 1080p. Regenerate new work at 1920×1080 or larger.

## Needed, but not images

- **Look closer beyond the first three threads needs writing before art.** The R02–R05 threads in [investigation.md](../investigation.md) need authored material before any detail images are made.
- **The game has no sound.** Music, ambience and sound effects don't exist yet.
- **The final "Yes" is deferred.** The response to the final question stays deferred, as the brief says.
