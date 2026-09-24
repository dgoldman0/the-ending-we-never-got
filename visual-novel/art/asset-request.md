# Asset request

Updated 24 September 2026, after the user selected ceremonial option A. The game takes new art without code changes: a file saved at its listed path appears in play once Claude has cropped and graded it. This file says what GPT makes next, where it stops, and what is queued behind that stop.

The user wants better portraits. The cast is being painted as head-and-shoulders busts, with **one painting per role**, so speaker and listener face each other without mirroring. Batches 1–3 came through with the format, direction and scale right every time; the faults were individual faces and clothes. So the batches are now much larger, in parts, and GPT checks its own work against the list below as it goes. **Batch 5 is the rest of the game's art**: Tessa's last portraits, repaints of the opening, and every scene painting through the ending. Scene paintings still need a written brief from the screenplay before generation, as [AGENTS.md](../AGENTS.md) requires. Nothing here approves an image or replaces the likeness, wardrobe and lighting references.

## Checked so far

- **Batch 1 (S001), checked 23 September.** Tessa's four and the petitioner passed. Senn's three were off-model, younger and leaner than his design and the painted Senn, and were repainted in batch 2. The S001 petition painting shows the petitioner as a different woman; see corrections.
- **Batch 2 (S002 and Senn again), checked 23 September.** All twelve pass. Tessa is the same girl in Mara's cloak and then without it; Mara matches her design and the Mara painted in S002; the new Senn is the heavier, older man in the paintings.
- **Batch 3 (S003), checked 23 September.** Played through every S003 line in the game. The priest, Olan, the mother and Iven's four match their designs and the S003 paintings, and every pair faces each other. Iven's apron is in all four paintings; it sits low on his chest, below the game's crop. The working-dress Tessa drifts toward a made-up look (shaped brows, eyeliner, fuller glossy lips, smoothed skin, fewer freckles, redder hair) against [her likeness reference](character-references/tessa/north-infirmary-face.png) and her batch 1 portraits, most in the two listening files and `tessa-resolute-working-speaking`; those three were repainted in batch 4.
- **Batch 4, first start, stopped 23 September.** The user rejected Tessa's layered ceremonial costume when GPT's first drafts showed it at bust size ("a shawl on a blue thing on a blueish thing"). The fault was the costume design, carried over unexamined, not GPT's painting. The partial work is kept in the git stash "Batch 4 partial (GPT, stopped 23 Sep)"; its four good files were restored into batch 4.
- **Batch 4, checked 23 September.** All 62 portraits and the costume proposals arrived. Played every line that uses them in the game, and compared each character's new files with the ones already in it. Every new face matches its written design, and the returning cast (Iven, Mara, Olan, Senn, Valcair, Orra, the messenger) matches their earlier portraits; every pair faces each other. The three Tessa repaints now match her likeness reference: freckles, natural brows, no makeup. That leaves her three S003 *speaking* files looking more polished than the listening files they alternate with, so they are repainted in batch 5. Claude fixed the crops locally: the face detector had locked onto a shirt collar or part of a face in `iven-harrow-speaking`, `iven-attentive-listening` and `olan-soldier-listening`, and had framed `iven-concerned-listening`, `olan-soldier-speaking` and four older portraits (Olan, Serat and two of Tessa's) tighter than the rest of their sets.

## Next for GPT: batch 5, the rest of the game's art

The user wants at least a draft of the whole game, so this batch covers every image still missing: Tessa's costumes and portraits, the repaints of the opening's paintings, and a painting for every scene from S006 to the ending, with the key moments. It runs in five parts, about 120 images: 3 portrait repaints (part A), the costume designs (B), 20 Tessa portraits (C), 11 repaints of the opening's paintings (D), and 52 scene paintings with 28 key moments (E). **It stops once, after part B, for the user to choose Tessa's costumes**; everything after that depends on the choice. Then it runs to the end, committing after each part and each chapter.

Claude checks each commit in the game as it lands. Before starting each part or chapter, read **Repaints found during this batch** at the end of this section and do any listed there first.

### What the user decided about the batch 4 proposals

- **Ceremony: redo as Saint's attire.** The closed lapis robe reads as a good dress with a mantle behind it. The user expects the ceremony to put her in the Saint's vestments, not "a shawl on top of a nice dress"; her working and field clothes can be different. The direction is white and gold, the temple's own colours: a full-length sacred robe with the twelve-ray sun worked into it, and a white ceremonial mantle fastened across the chest with the badge. The earlier heavy-cloak direction was rejected during batch 5; the robe and mantle must be elegant and light, as recorded below. Something should set the Saint apart from the temple's priests; the user selected the light fine-gold option A on 24 September. Not the summoning circle.
- **No green for Tessa.** Green is the northern side's colour in the written designs (Lucan, Serat, the northern captains, the governor); the human army wears blues, the temple white, cream, gold and lapis. The winter and field proposals were green only because the brief asked for outfits that differ from each other; make them differ by shape and trim instead.
- **Winter:** keep the one-piece lined coat with its own roll collar, in a human-side colour.
- **Gray Scar to Harrow:** too plain; only the small badge marks her as the Saint. Redesign.
- **Campaign:** the existing coat still stacks an ivory under-tunic with its own collar inside an open coat. Redesign as one garment.
- **Postwar:** the plum wrap robe stays as proposed.

### User corrections during batch 5

The standing ray collar is rejected: the rigid fins are hideous to the user. Do not finish or reuse that proposal. The heavy, bulky ceremonial robe direction is also rejected. The Saint's robe must be **elegant and light**: flowing white cloth, graceful drape, fine gold work and a clean silhouette. This supersedes the earlier heavy-cloak language and cancels the standing-collar option. On 24 September, the user selected **A: fine gold**, the light white robe and flowing white mantle in `saint-vestments-gold`. The banner alternative was not selected. Winter remains a practical winter coat.

### Before painting: the self-check

These are the faults found so far. Check every portrait and painting against them before saving it, and compare each finished set side by side before committing.

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

Commit part A.

### Part B: Tessa's costumes, then stop for the user

As in batch 4 part A, make for each costume a full-figure image on a neutral background (1024×1536 or larger) with a GIMP XCF, a bust view in the portrait framing, and a short `.md` in `art/character-keys/tessa/` giving the construction, the story period and your review. Keep the rule: one main garment per outfit with its own silhouette and neckline, only the layers the story needs, and every outfit distinguishable at bust size. Paint from the written design; don't feed in the rejected keys as clothing references.

1. **The Saint's vestments, two revised variants (S004–S005; the mantle again at the hearing, S016), Tessa at nineteen.** The user's correction during production requires elegant, light white-and-gold vestments: a full-length flowing sacred robe with the twelve-ray sun worked into it and a light, gracefully draped ceremonial mantle fastened across the chest with the badge. Avoid bulky shoulders, stiff collars and thick regular-robe fabric. Each surviving idea distinguishes the Saint from the cream-robed priests:
   - `saint-vestments-rays.md`: **rejected by the user during production.** The standing rays read as hideous fins, and the heavy robe was too bulky. Retain only as a rejected diagnostic; do not complete or reuse it.
   - `saint-vestments-gold.md`: **pure white and fine gold.** Light white cloth with fine gold thread spreading from the clasp across the mantle; graceful fluid folds and a clean silhouette, without dense heavy gold bands.
   - `saint-vestments-banner.md`: **the temple's banner colours in light fabric.** A slender flowing white robe and light mantle with lapis facing and the great gold sun on its back. Preserve elegance and fine drape; show the front silhouette and provide a separate back detail if needed to make the banner visible.

   Each must work in the story: Senn pins the badge and settles the cloak on her; at the hearing she wears the cloak over her winter coat, pulls it loose and leaves it across the book. No crown. She wears it against her will.
2. **Winter, `winter.md` (S014–S017), about twenty.** The batch 4 shape in a human-side colour, not green.
3. **Gray Scar to Harrow, `gray-scar-harrow.md` (S018–S037), about twenty to twenty-one.** One practical field garment with trousers and boots, repaired and worn, in a human-side colour, that still reads as the Saint's: carry the woven botanical trim of her working dress and the temple badge, not a plain work tunic.
4. **Campaign, `campaign-coat.md` (S038–S057), about twenty-three.** One coat closed to the throat with its own collar, no separate inner collar or shirt front showing; keep the blue-gray, the narrow worn borders, trousers, calf boots, short gloves and the sword belt at her left hip. War-worn face.

Commit part B, then **stop and ask the user to choose** a vestments variant and approve or reject the other three. Record the choices in **The user's costume choices** below, then continue. Redesign anything rejected the same way and stop again for it.

**The user's costume choices, 24 September:** **A — fine gold is selected for the ceremony:** use [saint-vestments-gold](character-keys/tessa/saint-vestments-gold.md), including its lightweight removable white mantle. The lapis-banner alternative is not selected. The ray collar and bulky/heavy ceremonial silhouette remain rejected. **Winter, field and campaign still await the user's decision; selecting A does not approve those three.** The postwar plum wrap remains accepted.

**Delivery checkpoint:** Part A is committed in `34309eb`. The surviving Part B proposals and cross-review are collected in [the costume comparison](character-keys/tessa/batch-5-costume-review.md). The ceremonial choice is now recorded. The remaining winter, field and campaign decisions are pending; no approval of those designs is inferred from the ceremonial selection or source checks.

### Part C: Tessa's portraits in the chosen costumes (20 files)

#### S004 and S005, in the Saint's vestments (6 files)

Tessa is nineteen, in the chosen vestments, displayed against her will; the scene and people are as in batch 4 part B.

| File in `renpy/game/art/portraits/` | Who and moment | Looks toward | Used with these lines |
| --- | --- | --- | --- |
| `tessa-attentive-formal-speaking.png` | Tessa, quiet and grateful, then asking | screen right | "You bought me an afternoon." · "Are you coming with me?" |
| `tessa-attentive-formal-listening.png` | Tessa taking in what she's told | screen left | Senn: "Tomorrow our Saint leaves with the Bellweir convoy…" · Iven: "At least that." · "Let me speak to her." · "All the way there and back." |
| `tessa-hurt-formal-speaking.png` | Tessa betrayed and upset | screen right | "Tomorrow? You said I was coming to see Olan." · "She's still down there. What am I supposed to tell her?" |
| `tessa-hurt-formal-listening.png` | Tessa stung | screen left | Senn: "He's here. Sit down; they're trying to welcome you." · Iven: "I don't know how to stop that." |
| `tessa-resolute-formal-speaking.png` | Tessa confronting Senn | screen right | "Look at me. When did I agree to go?" |
| `tessa-resolute-formal-listening.png` | Tessa holding her ground | screen left | Senn: "We can talk afterward." |

#### The later Tessa sets (7 sets, 14 files)

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

Commit part C.

### Part D: repaints of the opening's paintings (11 files)

Save each new painting in `art/repaints/` under the file name given; Claude puts it into the game (these scenes are built from layers, so don't overwrite the files in `renpy/game/`). Keep each painting's composition, staging, camera and light sources, and change only what is listed. 1920×1080 or larger, neutral light, as the scene paintings below.

| New file in `art/repaints/` | Current painting | Change |
| --- | --- | --- |
| `ceremony-dais.png` | [ceremony-dais](../renpy/game/art/rovel/cg/ceremony-dais.png) | Tessa in the chosen vestments |
| `ceremony-mantle.png` | [ceremony-mantle](../renpy/game/art/rovel/cg/ceremony-mantle.png) | Tessa in the chosen robe as Senn settles the cloak on her shoulders |
| `ceremony-refusal.png` | [ceremony-refusal](../renpy/game/art/rovel/cg/ceremony-refusal.png) | the chosen vestments |
| `ceremony-refused-chair.png` | [ceremony-refused-chair](../renpy/game/art/rovel/cg/ceremony-refused-chair.png) | the chosen vestments |
| `ceremony-intervention.png` | [ceremony-intervention](../renpy/game/art/rovel/cg/ceremony-intervention.png) | the chosen vestments; keep Iven's boots and the step edge between him and the dais above y ≈ 820 of 1080, out of the reading shade |
| `ceremony-yield.png` | [ceremony-yield](../renpy/game/art/rovel/cg/ceremony-yield.png) | the same two changes |
| `window-packing.png`, `window-pause.png`, `window-together.png` | [window-packing](../renpy/game/art/rovel/cg/window-packing.png), [-pause](../renpy/game/art/rovel/cg/window-pause.png), [-together](../renpy/game/art/rovel/cg/window-together.png) | the chosen robe; read S005 in the screenplay (lines 216–251) and decide whether she still wears the cloak at the window after the ceremony, and say which in the commit |
| `pleading-mother.png`, `woman-release.png` | [pleading-mother](../renpy/game/art/opening/cg/pleading-mother.png), [woman-release](../renpy/game/art/opening/cg/woman-release.png) | the woman catching Senn's sleeve is the petitioner of her design and portrait: middle-aged, freckled, a reddish braid and a damp gray shawl, not dark curls in a bun and a brown shawl |

Commit part D.

### Part E: a painting for every scene, S006 to S058, chapter by chapter

One establishing painting per scene puts the scene on its picture, and the portraits carry the exchanges, as S005's window scene does. Some beats need their own image (the key moments at the end of each chapter's list). Work one chapter at a time, in story order, and commit each chapter.

**For each scene, write the brief first.** Before painting, write a short brief in `art/scene-studies/sNNN-<name>/README.md`, as [AGENTS.md](../AGENTS.md) requires: the exact screenplay moment (with line numbers in [the screenplay](../../screenplay/original-timeline/source.fountain)) and what comes just before and after; who is present and visible, and whether each is named or an extra; where everyone stands and faces, and how they got there; who holds which props; each person's clothes and injuries for the period, and the light. Read the scene in the screenplay, the [location notes](../../worldbuilding/original-locations.md) and the [character designs](../../characters/original-visuals.md). Then paint from the brief, and add a line to the brief saying what you checked in the finished painting.

**People.** Use each character's portrait for that period as the identity and clothing reference; [staging.json](../renpy/game/staging.json) names the set for each scene (for example `iven-harrow` in S032–S035). Tessa's clothes by period: the working dress in S006–S013 (as in [`tessa-resolute-working-speaking`](../renpy/game/art/portraits/tessa-resolute-working-speaking.png)); the chosen winter coat in S014–S017, with the Saint's cloak over it at the hearing (S016); the chosen field outfit in S018–S037; the chosen campaign coat in S038–S054; the same torn and dirty in S055–S057, her right hand wounded; the postwar clothes in S058 with the brace on her right hand. Keep the northern side in greens and the human side in blues, as in the portraits. Extras are subordinate and don't change the story.

**Composition, so the painting works under the reading interface.**
- 16:9, 1920×1080 or larger; 2560×1440 preferred.
- Keep faces, hands, contact points and plot props above the bottom fifth (y ≈ 840 of 1080), which sits under the reading shade.
- Keep the lower-left corner (about x 116–516, y 748–1004) free of anything important; the portrait windows sit there.
- Leave room at the top; the game can lift a painting up to about 70 px.
- Paint real light with visible sources, in even, readable exposure. Don't bake in glare or darkness; the game renders each scene into its light register (bright, ordinary or night), permanently distorted, in Intense and Softened.

**Places that recur stay recognizable** across states: the Bellweir market is intact (S008), destroyed (S011) and rebuilt (S058). The [intact heron study](scene-studies/bellweir-heron/README.md) is a working reference for the first. The palace infirmary, the Harrow bridge and the citadel stair recur too.

#### The establishing paintings (53 scenes, 52 files)

Save each at `renpy/game/art/scenes/` under the name given; S053 continues S050 on the same stair and reuses its painting. The light column is only a default from the scene heading; set it in the brief.

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

#### The key moments (28 files)

These beats fail as one held painting. Save each in `renpy/game/art/scenes/` with the name given, paint it within its chapter, and put the screenplay line it belongs to in the scene's brief; Claude adds it to the game as a stage of its scene at that line.

| File | Scene | Moment |
| --- | --- | --- |
| `s009-boat-drawing.png` | S009 | Tessa drawing Iven's portrait on the boat |
| `s009-rowing.png` | S009 | Tessa learning to row with Mara |
| `s011-sanctuary.png` | S011 | Tessa's sanctuary light over the evacuation on the causeway |
| `s011-boots-and-cap.png` | S011 | the cut to the boots, the cap and the search portrait |
| `s016-hearing-door.png` | S016 | the hearing seen across the room: the door, Mara, Orra and Senn placed as the screenplay stages them |
| `s021-rescue.png` | S021 | the rescue's geography: ferryhouse, bank, gate, shelter and the two boats |
| `s021-lucan-returns.png` | S021 | Lucan turning back for the litter, held as a decision |
| `s029-cap.png`, `s029-leg-support.png`, `s029-launch.png`, `s029-quarry-refusal.png`, `s029-barge.png` | S029 | the montage of successive visits, one small view each |
| `s030-laughing-portrait.png` | S030 | the laughing-portrait interaction |
| `s035-collapse.png` | S035 | the midspan collapse of the bridge |
| `s035-iven.png` | S035 | Iven below the failing boards, her light failing beneath him |
| `s036-south-bank.png` | S036 | the southern remnant of the bridge and the confrontation on the bank |
| `s037-coat.png` | S037 | Tessa beside the screen, Iven's coat across her knees, fitting the torn sleeve to its shoulder |
| `s041-wardkeeper.png` | S041 | the wardkeeper at the tower |
| `s042-cart.png` | S042 | the cart aftermath and the sword that won't sheathe |
| `s042-mara-hand.png` | S042 | Tessa taking Mara's hand |
| `s043-seasons.png` | S043 | the river provinces through three seasons, as one painting in three panels or three views |
| `s050-guard.png` | S050 | Tessa fastening Mara's trembling forearm guard |
| `s052-entrance-ward.png` | S052 | the entrance ward, and Tessa's left glove coming off |
| `s054-duel.png` | S054 | the throne-hall fight, Valcair's black ward-light at his armour's joints |
| `s054-wound.png` | S054 | the right-hand wound and the sword changing to her left hand |
| `s055-mara.png` | S055 | finding Mara on the stair |
| `s056-hand.png` | S056 | the hand examination, anchored by the [storm-infirmary study](scene-studies/north-infirmary/north-infirmary-storm.png) |
| `s058-final.png` | S058 | the final Bellweir interaction before the fade and the question |

#### Chapters

Commit after each chapter's briefs, paintings and key moments.

| Chapter | Scenes |
| --- | --- |
| 02 Bellweir | S006–S009 |
| 03 The broken promise | S010–S017 |
| 04 Gray Scar | S018–S025 |
| 05 Across the river | S026–S031 |
| 06 Harrow | S032–S037 |
| 07 After Harrow | S038–S043 |
| 08 The witness | S044–S049 |
| 09 The citadel | S050–S057 |
| 10 Bellweir again | S058 |

### Save, commit, then stop

1. Save each file at its path. Prompts go in `art/prompts/portraits-batch-5/` for portraits, `art/prompts/characters/` for costumes and `art/prompts/<scene>/` for paintings.
2. Before each commit, lay the part's or chapter's images side by side and go through the self-check; for scenes, also against each brief.
3. Commit at the end of each part and each chapter, naming the files in the message.
4. **Stop after part B for the user's costume choices, and again at the end.** Don't run the crop or grading tools, and don't change game code, data or other documents. Tell the user when the batch is done, with any image that didn't pass the self-check.

**How Claude checks it.** Portraits: `tools/review-portraits.py` crops, grades and plays each line that uses them. Paintings: Claude grades them into their light registers, plays each scene in the game with its portraits and text over it, and checks the composition rules and the brief. Anything that fails goes into the list below while you work.

### Repaints found during this batch

None yet.

## Queued behind the check

**Already done:** every portrait set except Tessa's, and the S001–S005 scene paintings apart from the repaints in part D. After batch 5 the game has art for every scene; what remains is below under "Needed, but not images".

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
3. **In batch 5, part D: Iven's position below the dais falls under the text.** In `art/rovel/cg/ceremony-intervention.png` and `ceremony-yield.png`, Iven's boots and the step edge between him and the dais sit under the reading shade, so the staging point is weakened. Lifting the painting cut off Orra's and Senn's heads instead, so the fix belongs in the painting: keep the step edge above y ≈ 820.
4. **In batch 5, part D: the petitioner is painted as a different woman.** In `art/opening/cg/pleading-mother.png` and `woman-release.png`, the woman who catches Senn's sleeve has dark curly hair in a bun and a brown shawl. Her design, and her portrait, give her a reddish braid and a damp gray shawl. Correct the paintings to the design.
5. **In batch 5, part D: nine S004–S005 paintings show the rejected ceremonial outfit** (the open lapis coat over the pale green under-robe): `ceremony-dais`, `-intervention`, `-mantle`, `-refusal`, `-refused-chair` and `-yield`, and `window-packing`, `-pause` and `-together`. White-and-gold vestments are a change of the whole figure, not a recolour, so they need repainting in the chosen vestments once the user has chosen. For the window scene, decide from the screenplay whether she is still wearing the mantle afterward.
6. **Existing paintings are a little soft.** S001–S005 are 1672×941, upscaled to 1080p. Regenerate new work at 1920×1080 or larger.

## Needed, but not images

- **Look closer beyond the first three threads needs writing before art.** The R02–R05 threads in [investigation.md](../investigation.md) need authored material before any detail images are made.
- **The game has no sound.** Music, ambience and sound effects don't exist yet.
- **The final "Yes" is deferred.** The response to the final question stays deferred, as the brief says.
