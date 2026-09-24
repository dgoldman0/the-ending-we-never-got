# Asset request

Updated 23 September 2026, after the user rejected Tessa's layered ceremonial costume and the first start of batch 4 was stopped. The game takes new art without code changes: a file saved at its listed path appears in play once Claude has cropped and graded it. This file says what GPT makes next, where it stops, and what is queued behind that stop.

The user wants better portraits. The cast is being painted as head-and-shoulders busts, with **one painting per role**, so speaker and listener face each other without mirroring. Batches 1–3 came through with the format, direction and scale right every time; the faults were individual faces and clothes. So the batches are now much larger. **Batch 4 covers every portrait that doesn't depend on a Tessa costume, and Tessa's costume designs for the user to choose**, in parts with one stop at the end, and GPT checks its own work against the list below as it goes. Tessa's portraits in those costumes follow in batch 5. Scene paintings still need a written brief from the screenplay before generation, as [AGENTS.md](../AGENTS.md) requires. Nothing here approves an image or replaces the likeness, wardrobe and lighting references.

## Checked so far

- **Batch 1 (S001), checked 23 September.** Tessa's four and the petitioner passed. Senn's three were off-model, younger and leaner than his design and the painted Senn, and were repainted in batch 2. The S001 petition painting shows the petitioner as a different woman; see corrections.
- **Batch 2 (S002 and Senn again), checked 23 September.** All twelve pass. Tessa is the same girl in Mara's cloak and then without it; Mara matches her design and the Mara painted in S002; the new Senn is the heavier, older man in the paintings.
- **Batch 3 (S003), checked 23 September.** Played through every S003 line in the game. The priest, Olan, the mother and Iven's four match their designs and the S003 paintings, and every pair faces each other. Iven's apron is in all four paintings; it sits low on his chest, below the game's crop. The working-dress Tessa drifts toward a made-up look (shaped brows, eyeliner, fuller glossy lips, smoothed skin, fewer freckles, redder hair) against [her likeness reference](character-references/tessa/north-infirmary-face.png) and her batch 1 portraits, most in the two listening files and `tessa-resolute-working-speaking`; those three are repainted in part C below.
- **Batch 4, first start, stopped 23 September.** The user rejected Tessa's ceremonial costume when GPT's first drafts showed it at bust size: a pale green under-robe, an open blue coat and a white mantle read as "a shawl on a blue thing on a blueish thing", clothes stacked on clothes. The fault was the costume design, which this request had carried over unexamined, not GPT's painting. The partial work is kept in a git stash named "Batch 4 partial (GPT, stopped 23 Sep)" (currently `stash@{0}`). Four files in it were checked and pass: `iven-attentive-speaking`, `iven-attentive-listening` (Iven without the apron, matching batch 3) and `warden-speaking`, `warden-listening`. Restore those four, and nothing else, with:

  ```
  git checkout 'stash@{0}^3' -- visual-novel/renpy/game/art/portraits/iven-attentive-speaking.png visual-novel/renpy/game/art/portraits/iven-attentive-listening.png visual-novel/renpy/game/art/portraits/warden-speaking.png visual-novel/renpy/game/art/portraits/warden-listening.png
  ```

## Next for GPT: batch 4, in five parts, then stop

About seventy files: Tessa's costume designs first, then the S004–S005 portraits without Tessa, three Tessa repaints in her unchanged working dress, fourteen later cast sets and thirteen small-role sets. **Commit at the end of each part**, so the work survives an interrupted session. If the session has to end early, finish the current part, commit, and say which parts are done; Claude can check finished parts on their own. `python3 visual-novel/tools/check-staging.py --missing` lists what is still missing.

### Before painting: the self-check

These are the faults found so far. Check every file against them before saving it, and compare each finished set side by side before committing a part.

1. **The face matches the written design and the character in the paintings,** not merely the last portrait. Batch 1 made Senn younger and leaner than his design; batch 3 gave Tessa makeup.
2. **No makeup or glamour.** No eyeliner, shaped brows or glossy lips on anyone who wouldn't wear them. Keep freckles, uneven skin and ordinary features. For Tessa, compare every file with [the face reference](character-references/tessa/north-infirmary-face.png) and [her arrival portrait](../renpy/game/art/portraits/tessa-resolute-arrival-speaking.png).
3. **The clothes match the period and the design, and the design itself makes sense.** A costume should read as one outfit at bust size, not as layers stacked on the wearer. If a design written here looks wrong once it's painted, stop that file and say so; don't paint around it. That is how the ceremonial Tessa should have been caught.
4. **Each file is painted in its own direction.** `-speaking` looks toward screen right with lips parted mid-word; `-listening` looks toward screen left, not speaking. Never mirror: a flipped copy moves the hair part, horn shapes, clasps and badges to the wrong side.
5. **Both files of a set are plainly the same person in the same clothes,** with the same horns, scars and hair.
6. **Age is right.** Ada is eight; the apprentice is mid-teens; Tessa's ages are given with each costume.
7. **Horns follow each design.** Northern characters have individual horn shapes; the humans have none; helmets have openings for horns.
8. **The expression reads at 150 px wide,** the listener's window.

### The format

Unchanged since batch 1, matching the Lucan and Valcair busts ([example](../renpy/game/art/portraits/lucan-early-speaking.png)).
- Square, 1254×1254 or larger, with a transparent background.
- Head, shoulders and upper chest in three-quarter view. The face, hairline to chin, is about a third of the image height, with clear space above the head and on both sides for the game's crop.
- Even, neutral light with no strong colour cast; the game adds each scene's glare or darkness. Keep hands out of frame, with no text, frame or border.
- Paint from the written design. Use an existing portrait or painting only as an identity reference, and never edit a rejected file into its replacement.

### Part A: Tessa's costumes, for the user to choose

The user's rule: **each outfit is one main garment with its own silhouette and neckline, not a stack of layers.** Add only the layers the story needs, and make a mantle or cloak read as part of the outfit, not a shawl on top. Her outfits must look different from each other from the chest up, because that is all the dialogue portraits show. The rejected ceremonial key and the reasons are in [ceremonial-saint.md](character-keys/tessa/ceremonial-saint.md) and [the wardrobe audit](character-keys/tessa/wardrobe-redesign.md). The working dress stays as it is: it closes at the neck with its ivory yoke, and the user liked it.

For each costume below, make:
- a full-figure image on a neutral background, 1024×1536 or larger, with a GIMP XCF;
- **a bust view** in the portrait framing above (head, shoulders and upper chest, three-quarter view), so the user can judge it at the size the game shows;
- a short `.md` beside the existing keys in `art/character-keys/tessa/`, giving the construction, the story period and your review against the rule above.

Tessa's face follows the self-check: the reference face, no makeup. Paint from the written design; don't feed in the rejected keys or old portraits as clothing references.

1. **The ceremonial robe, `ceremonial-robe.md` (S004–S005; the mantle again at the hearing, S016).** In the screenplay Senn pins the temple badge to her coat and settles the white mantle over it; at the hearing she sits in the mantle, then pulls it loose and leaves it across the book. Design one closed, full-length robe in lapis brocade: long sleeves, closed from collar to hem, a high collar worked in gold botanical embroidery, and a woven waistband that belongs to it. Nothing shows underneath: no under-robe at the neck, down the front or at the cuffs. The white mantle with gold borders is part of the outfit: it fastens at the collar or shoulders and falls behind her, framing the robe, never wrapped across her chest. It must be easy to settle over her and to pull loose. The small brass badge with twelve rays sits on the left chest of the robe. No crown or jewellery. Tessa is nineteen and wearing it against her will. The S004–S005 paintings keep the lapis and gold, so Claude can correct them to the chosen robe in GIMP.
2. **Winter, `winter.md` (S014–S017, the first winter and the hearing), about twenty.** One heavy lined robe-coat closed to the throat, in the same woven tradition as the working dress, with warmth built into it (a lined collar or hood of its own, cuffs she can work in) rather than a coat over a robe under a cloak. At the hearing (S016) the white mantle goes over it, so it must take the mantle cleanly.
3. **Gray Scar to Harrow, `gray-scar-harrow.md` (S019–S037), about twenty to twenty-one.** One practical field garment: a shorter closed robe-coat or tunic with trousers and boots (the user wants trousers allowed, especially in the trenches), mended places and resoled boots, the temple badge still on it at Gray Scar. More worn and capable than at nineteen.
4. **Postwar, `postwar-clothes.md` (S058), about twenty-three.** Softer clothes she chose herself in the adopted world's tradition, with closures she can manage one-handed (a side wrap, toggles), and the pale soft brace on her right hand. Not the old cardigan. The war shows in her: drawn face, tired eyes, weathered skin, less tended hair, as [AGENTS.md](../AGENTS.md) and [age and wardrobe](character-keys/age-and-wardrobe.md) describe.
5. **The campaign coat: a bust view only.** The existing [campaign key](character-keys/tessa/campaign-saint.md) closes at the neck with a standing collar and is still a proposal. Paint a bust view of it (about twenty-three, war-worn, before the final assault) so the user can judge it at portrait size, and note whether a separate shirt collar shows above the coat.

Commit part A before going on. Don't paint Tessa's portraits in any of these costumes; that is batch 5, after the user chooses.

### Part B: S004 and S005 without Tessa (6 new files, 2 restored)

In S004, Senn presents Tessa at the Saint ceremony and announces that she leaves with the Bellweir convoy tomorrow; she refuses in front of the hall, and Iven tells Marshal Orra he hasn't cleared her to travel. In S005 Tessa and Iven sit in the infirmary window seat and she asks him to come with her. Match the people and clothes to the S004–S005 paintings ([ceremony](../renpy/game/art/rovel/cg/ceremony-refusal.png), [window](../renpy/game/art/rovel/cg/window-together.png)). `iven-attentive-speaking` and `iven-attentive-listening` come back from the stash.

| File in `renpy/game/art/portraits/` | Who and moment | Looks toward | Used with these lines |
| --- | --- | --- | --- |
| `iven-attentive-speaking.png` | Iven gentle, making a promise | screen right | "At least that." · "Let me speak to her." · "All the way there and back." |
| `iven-attentive-listening.png` | Iven listening closely | screen left | Orra: "Saye. Is she ready to travel?" · Tessa: "You bought me an afternoon." · "Are you coming with me?" |
| `iven-concerned-speaking.png` | Iven standing up to the marshal; then honest about his limits | screen right | "I haven't cleared her for anything, Marshal." · "I don't know how to stop that." |
| `iven-concerned-listening.png` | Iven worried for her | screen left | "She's still down there…" · "And tomorrow? They'll send someone else to ask me." |
| `orra-speaking.png` | Orra, blunt and practical | screen right | "Saye. Is she ready to travel?" |
| `orra-listening.png` | Orra hearing bad news | screen left | Messenger: "One of the new ward anchors, Marshal. The curse got through this one too." |
| `messenger-speaking.png` | The messenger, urgent, out of breath | screen right | the same line |
| `senn-evasive-speaking.png` | Senn smoothly putting her off | screen right | "We can talk afterward." |

- **Iven, twenty-six,** as in batch 3 but **without the apron**: the olive knee-length coat, open over an ivory open-neck linen shirt.
- **Orra, early fifties, the marshal.** Sturdy, dark-brown skin, close-cropped graying hair, dark eyes, a full unsmiling mouth. A deep blue military coat with three brass collar bars; she has come from the convoy yard, so gloves and some road dust, not ceremony. Match [her current head crop](../renpy/game/art/cast/orra.png).
- **The messenger.** Young, pale skin, dark curls, a brown riding cape, holding a ward stone out of frame. Match [his current head crop](../renpy/game/art/cast/messenger.png).
- **Senn,** the batch 2 Senn: late fifties, rounded, thinning sandy-gray hair, short beard, cream robe with sunburst embroidery at the collar. Use [`senn-assuring-speaking`](../renpy/game/art/portraits/senn-assuring-speaking.png) as his identity reference.

### Part C: three Tessa repaints, working dress unchanged

Replace these at the same paths. Paint each from the references named here; don't edit the batch 3 file. Keep each file's moment and direction from batch 3, and the working dress exactly as it is: the blue-gray robe-coat with the ivory botanical yoke and front borders over the ivory under-robe.

| File | What changes | Identity reference |
| --- | --- | --- |
| `tessa-attentive-working-listening.png` | Remove the made-up look: no liner, natural straight brows, ordinary lips, freckles kept, chestnut hair not red | [face reference](character-references/tessa/north-infirmary-face.png) and [arrival portrait](../renpy/game/art/portraits/tessa-resolute-arrival-listening.png) |
| `tessa-hurt-working-listening.png` | the same | the same |
| `tessa-resolute-working-speaking.png` | the same | [face reference](character-references/tessa/north-infirmary-face.png) and [arrival portrait](../renpy/game/art/portraits/tessa-resolute-arrival-speaking.png) |

### Part D: the recurring cast later in the story (14 sets, 28 files)

Each set is `<set>-speaking.png` (looks toward screen right) and `<set>-listening.png` (looks toward screen left). The game shows them on the typeset book pages at once, and in the scenes once their paintings arrive. The clothes and faces come from [the character designs](../../characters/original-visuals.md); read the entry before painting.

| Set | Who, age and clothes | Speaking moment | Listening moment |
| --- | --- | --- | --- |
| `valcair-private` | Valcair, the northern king, early fifties, the same face as [his armoured portrait](../renpy/game/art/portraits/valcair-speaking.png): black horns swept back and ridged at the roots, silver-streaked hair bound at the nape, short close beard. Charcoal wool with dark red lining and a heavy plain clasp; no armour. | Night in his private rooms, quiet and dangerous: "You attacked an escort." | Hearing out Vask's or Lucan's report, still and unreadable |
| `vask` | General Vask, a woman in her mid-forties. Broad, muscular, tawny skin, rectangular face, deep-set brown eyes, iron-gray hair cropped short around compact dark horns that curve outward then back. Dark plum field coat under steel shoulder and torso protection; three narrow silver bars beneath a split-star pin. | Brisk and certain: "Sign this and the crews can leave." | Coolly weighing what she hears |
| `marren` | Marren, the stores clerk, early forties. Slight, pale brown skin, narrow face, thinning dark hair, brown eyes, small rounded horns above the ears. Faded brown clerk's coat, cream shirt. | Frightened, justifying himself: "The repairs were certified. I entered them." | Anxious, braced for blame |
| `elin` | Elin Orr, twenty-two, scholar. Compact, deep-brown skin, round cheeks tapering to a small chin, dark eyes, tightly curled black hair in a short twist with one curl escaping at the forehead. Ochre-brown wool jacket over a pale linen blouse. | Alert and probing: "Was the book already like this when you used it?" | Curious, taking it all in |
| `elin-later` | Elin three or four years on, in the field: the same face, a knee-length rain cloak over the ochre jacket. | Urgent and decisive: "Now, Tessa." | Intent, thinking ahead |
| `hest` | Hest, the baker, late thirties. Broad build, deep warm-brown skin, broad nose, dark eyes, black curls under a rust-coloured headscarf. Blue work dress. | Urgent: "Orren went for the apprentices. The blue door, by the steps!" | Worried, holding herself together |
| `orren` | Orren, the baker, early forties. Long face and long chin with a short pale scar beneath it, medium-brown skin, brown eyes. Faded burgundy knitted cap, collarless shirt, green-brown waistcoat. | Warm and wry: "His mother would have brought him back by the ear." | Kindly attentive |
| `boatman` | Lucan's boatman, late forties. Deep-brown skin, graying beard, low backward horns, salt-stiff dark cap, heavy ochre waterproofed coat. | Laconic warning: "Two boats. You can't outrun them in this." | Patient, sceptical |
| `mara-campaign` | Mara, about thirty-five, the same face as [her batch 2 portraits](../renpy/game/art/portraits/mara-controlled-speaking.png): squared jaw, heavy-lidded hazel eyes, dark braided hair pinned low. Slate-blue military coat over mail, shoulder protection, the blue ward at the left shoulder, brass captain's bar at the collar; the coat is mended. After Iven's death. | Raw and controlled: "The boards were going. I couldn't hold you both." | Grieving but on duty |
| `mara-citadel` | Mara before the assault on the citadel: the same kit, fully armed, forearm guards on. | Steady, tender under it: "I'll come when he calls." | Holding Tessa's eyes, not arguing |
| `serat` | Serat, Lucan's lieutenant, early thirties. Broad, dark umber skin, black close-cropped hair, amber-brown eyes, blunt nose, short horns rising close to the temples. Dark green padded uniform, steel shoulder guards, split-star badge. | Firm, defending the ward: "They aren't taking anyone out of this ward." | Alert, ready |
| `ada` | Ada, eight. Brown skin, round face, black curls in two short plaits. Mustard dress over a washable shirt. A child, not a small adult. | A broad grin, telling a joke: "He says you can grow people new heads." | Small and worried: "Will Dad know where we've gone?" |
| `iven-harrow` | Iven, about twenty-eight, at Harrow Ford: the olive coat worn and travel-stained, no apron and no cape. | Practical and warm, then straining in the rescue: "Take him, Hest. I've got his foot clear." | Easy attention before the crossing |
| `olan-soldier` | Olan four years on, as a soldier: the batch 3 Olan's face, a little older, in a blue-gray padded soldier's coat and repaired mail. | Confident, disagreeing on tactics: "The stair's right." | Weighing the plan |

### Part E: the small speaking roles (13 sets, 26 files)

Same format, one speaking and one listening file each. These people speak a line or four; the listening file shows them attending to the main cast. `warden-speaking` and `warden-listening` come back from the stash.

| Set | Who | Speaking moment |
| --- | --- | --- |
| `warden` | The convoy warden, human: lean, medium-brown skin, short black hair, reed-coloured rain cape. | Practical: "We've closed the high road after a crag cat took a mule." |
| `archivist` | Temple archivist, human: older woman, pale olive skin, short silver hair, dark red wool gown. | Dry refusal: "Your master can ask for the original." |
| `scholar` | The summoning scholar, human: slender man in his forties, medium-brown skin, straight black hair tied back, soot-gray sleeve covers. | Defensive: "You're not supposed to have that." |
| `ferryman` | The Gray Scar ferryman, human: older, pale skin, thick gray beard, red knitted cap. | Urgent: "If we reach that gate, I can lock them out." |
| `picket-officer` | Rovel picket officer, human: dark skin, short hair, narrow moustache, fitted blue military coat with a stiff collar. | Stern: "Your sword. Leave it on the boards." |
| `apprentice` | Hest's first apprentice, mid-teens: slim, tawny skin, short straight dark hair, long nose, checked neckcloth over a gray quarry tunic. | A flat refusal: "No." Later, grieving: "He always said he'd run away to sea." |
| `governor` | Northern camp governor: heavyset, middle-aged, tan skin, small horns, well-kept green coat. | Officious: "The boat stays for the week." |
| `camp-healer` | Northern camp healer: middle-aged woman, tan skin, short horns, black hair, brown apron. | Urgent: "Three more have the blackening. I need her today." |
| `bargeman` | Northern barge owner: older, dark skin, blunt horns, broad-brimmed felt hat, tar-marked cuffs. | Stubborn: "My license feeds six people." |
| `escort` | Young northern escort: light-brown skin, close-cut hair, horns, plain steel helmet with openings for the horns. | Rigid: "He's under the general's orders." |
| `departing-captain` | Northern captain leaving the citadel: tall, tan skin, gray braid, narrow horns, heavy green coat. | Grim: "Give him the clerk. We can still get our wounded north." |
| `runner` | Human runner at the citadel: young adult, brown skin, close-cropped hair, blue-gray field coat, winded and dirty from the stair. | Breathless: "Captain Venn is losing men." |
| `surgeon` | The surgeon who examines Tessa's hand, human: middle-aged woman, pale skin, auburn hair tied back, clean undyed apron. | Careful and honest: "I can repair some of it… we have to give it time." |

### Save, commit, then stop

1. Save each file at its path, and the prompts in `art/prompts/portraits-batch-4/`. Part A goes in `art/character-keys/tessa/`, with its prompts in `art/prompts/characters/`.
2. Before each commit, lay the part's files side by side and go through the self-check.
3. Commit at the end of each part, naming the files in the message.
4. **Stop after part E.** Don't run the crop or grading tools, and don't change game code, data or other documents. Tell the user batch 4 is ready for Claude to check, with any files that didn't pass the self-check and any design that looked wrong once painted.

**How Claude checks it.** `tools/review-portraits.py` crops and grades every portrait, plays each line that uses them in the game headless, and lays out contact sheets of the lines and side-by-side sheets of each character's new files. A whole batch takes about ten minutes to render. Claude then looks at the sheets and full screens, and lists any file that fails as a repaint at the head of batch 5.

## Queued behind the check

**Batch 5: Tessa in her chosen costumes (20 files), and whatever fails in batch 4.** Once the user has chosen the part A costumes:
- the six S004–S005 ceremonial portraits: `tessa-attentive-formal`, `tessa-hurt-formal` and `tessa-resolute-formal`, each `-speaking` and `-listening`;
- `tessa-winter`, `tessa-campaign-early`, `tessa-harrow`, `tessa-campaign`, `tessa-citadel`, `tessa-injured` and `tessa-postwar`, one speaking and one listening file each.

Tessa ages from 19 to about 23 across them and carries more war wear in each; `tessa-injured` and `tessa-postwar` show the right-hand injury.

**Already done:** `lucan-early`, `lucan-later` and `valcair` (field armour).

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
5. **The S004–S005 paintings show the rejected ceremonial costume:** the open lapis coat over the pale green under-robe, with the mantle. Once the user has chosen the new robe, Claude corrects these paintings in GIMP to match it (closing the front, removing the under-robe, adjusting the mantle), and lists any that can't be corrected locally.
6. **Existing paintings are a little soft.** S001–S005 are 1672×941, upscaled to 1080p. Regenerate new work at 1920×1080 or larger.

## Needed, but not images

- **Look closer beyond the first three threads needs writing before art.** The R02–R05 threads in [investigation.md](../investigation.md) need authored material before any detail images are made.
- **The game has no sound.** Music, ambience and sound effects don't exist yet.
- **The final "Yes" is deferred.** The response to the final question stays deferred, as the brief says.
