# Asset request — after the interface pass

Requested 23 September 2026, at the end of the interface and infrastructure rounds. The game can now take new art without code changes. Put a file at its listed path and the scene switches from the typeset page to illustrated reading, with portraits beside the text. This list says what to make, in priority order, and what the interface requires of each image.

Scene art still needs a written brief before generation, and a review of the finished screens, as [AGENTS.md](../AGENTS.md) requires. This request does not approve any image, and it does not replace the likeness, wardrobe and lighting references.

## First rendered batch — 23 September 2026

The first three queued sets now have speaking/listening PNGs at the paths below: `lucan-early`, `valcair` (field armor), and `lucan-later`. See the [six portraits, prompts and inspection record](scene-studies/portraits-first-batch/README.md). They are working assets, not user-approved scene coverage. Book pages now show the speaker and listener in the left margin, so these portraits appear in S010 and S018 onward even before those scenes have paintings.

The Valcair request needed a wardrobe split: S010/S054 use the rendered armored `valcair` set; S023/S033/S046 now await `valcair-private`, in charcoal wool with dark-red lining and a plain clasp. Do not reuse armor in those private interiors.

## How files plug in

| Kind | Path under `renpy/game/` | Size | After adding |
| --- | --- | --- | --- |
| Scene painting | `art/scenes/<file>.png` | 16:9, at least 1920×1080; 2560×1440 preferred | run `python3 visual-novel/tools/grade-light.py` |
| Portrait | `art/portraits/<set>-speaking.png`, `<set>-listening.png` | square, at least 1024×1024, head and shoulders | run `python3 visual-novel/tools/crop-portraits.py`, then `grade-light.py --portraits` |
| Extra expression | `art/portraits/<set>-<expression>.png` | as above | name it for a line in `staging.json` |

**Deliver neutral images.** `grade-light.py` renders every painting and portrait into its light register, bright, ordinary or night, in both Intense and Softened. The distortion is part of the image and it's permanent: glare, halation, sallow cast, sunk night light. It isn't a fade. So paint the scene's real light, with its direction, sources and time of day, in even, readable exposure. Don't bake in blinding glare or crushed darkness, and don't make a separate Softened version. The register comes from `grade` in `staging.json`; change it there if a scene's brief calls for a different one.

`python3 visual-novel/tools/check-staging.py --missing` lists every file still awaited. [staging.json](../renpy/game/staging.json) maps each scene to its paintings and portrait sets. To add a second painting within a scene, add a stage with the source line where it begins (`"from"`). That's a data edit, not code.

## What the interface requires of the art

**Paintings**
- **Keep key action out of the bottom strip.** On every line, the bottom fifth of the screen (below about y = 840 of 1080) sits under the reading shade. Faces, hands, contact points and plot props belong above it.
- **Keep the lower-left corner clear during conversations.** Portraits occupy roughly x 116–516, y 744–1044. Nothing essential should sit there in a scene built for dialogue.
- **Leave room at the top.** The game can lift a painting up to about 70 px to clear the text, so no face should touch the top edge.
- **Leave a quiet area where it helps.** A quiet dark area, such as one side of a night interior, lets a single line sit inside the picture (the S002 drawing beats do this).
- **Paint the light, not the grade.** Place windows, lamps and candles so the register has sources to work with: bright glare spills from real openings, night warmth from real flames. The light column below is only a default from the scene heading; set the register in each scene's brief.

**Portraits**
- **Head and shoulders, with room to crop.** `crop-portraits.py` crops every portrait in GIMP to one composition: a closed laurel window, the face 62% of the crop's height with its top at 21%, and a little space on the side the face looks toward. Paint the head and shoulders, with clothing, well inside the canvas so there is material around the face on every side. A transparent or plain dark background both work.
- **Paint the whole bust.** The S001–S005 heads were painted without shoulders, so their crops end in bare neck and shadow. GPT's Lucan and Valcair busts, painted with coat and shoulders, crop better.
- **Mind the direction of gaze.** The speaker frame sits left of the listener frame, with the text to the right of both. Make `-speaking` a three-quarter view looking toward screen right and `-listening` looking toward screen left, so the pair face each other. The game mirrors a portrait that faces the wrong way, but a mirrored face flips its hair part and badges, so correct painting is better.
- **Use ordinary, even light.** The game grades portraits into each scene's register and mode. On book pages they appear in the left margin at the same sizes.
- **Take identity, age and wardrobe from the references.** Use [the character designs](../../characters/original-visuals.md), [character keys](character-keys/README.md) and [age/wardrobe variants](character-keys/age-and-wardrobe.md). Tessa's face comes from the storm-infirmary study.

## Priority 1 — portraits

Portraits turn page scenes into conversations the moment a scene has any painting. S006–S011 already reuse the S001–S005 portraits of Tessa, Iven and Mara, whose wardrobe and age still match. S016 reuses Tessa's formal portraits and Senn's.

| Portrait set | Scenes | Lines |
| --- | --- | ---: |
| `lucan-early` | S018–S036 (13) | 36 |
| `valcair` / `valcair-private` | S010–S054 (5; armor rendered, private pending) | 28 |
| `lucan-later` | S038–S057 (8) | 23 |
| `tessa-harrow` | S032–S037 (4) | 20 |
| `vask` | S010–S057 (4) | 19 |
| `tessa-campaign` | S040–S049 (4) | 16 |
| `tessa-campaign-early` | S019–S030 (6) | 15 |
| `marren` | S038–S048 (4) | 12 |
| `elin` | S008–S016 (4) | 11 |
| `hest` | S011–S037 (4) | 9 |
| `tessa-winter` | S014–S017 (3) | 9 |
| `elin-later` | S040–S058 (5) | 7 |
| `boatman` | S021–S043 (3) | 6 |
| `orren` | S008–S058 (5) | 5 |
| `mara-campaign` | S036–S049 (5) | 5 |
| `scholar` | S013 (1) | 4 |
| `governor` | S027 (1) | 4 |
| `serat` | S045–S051 (3) | 4 |
| `tessa-citadel` | S050–S054 (3) | 4 |
| `tessa-injured` | S055–S056 (2) | 4 |
| `picket-officer` | S022 (1) | 3 |
| `tessa-postwar` | S058 (1) | 3 |
| `ada` | S008–S014 (2) | 2 |
| `apprentice` | S026–S030 (2) | 2 |
| `camp-healer` | S027–S055 (2) | 2 |
| `bargeman` | S031 (1) | 2 |
| `iven-harrow` | S032–S035 (2) | 2 |
| `departing-captain` | S047 (1) | 2 |
| `mara-citadel` | S050 (1) | 2 |
| `warden` | S006 (1) | 1 |
| `archivist` | S012 (1) | 1 |
| `ferryman` | S019 (1) | 1 |
| `escort` | S044 (1) | 1 |
| `runner` | S052 (1) | 1 |
| `surgeon` | S056 (1) | 1 |


Notes:
- **Lucan is the second most frequent speaker** (59 lines) and has no portrait. He comes first.
- **Several Tessa periods need wardrobe design before portraits.** `original-visuals.md` marks the winter costume (`tessa-winter`), the Gray Scar–Harrow intermediate costume (`tessa-campaign-early`, `tessa-harrow`) and the postwar clothes (`tessa-postwar`) as still to develop.
- **Show age and wear.** Tessa ages from 19 to about 23. Later sets must show accumulated war wear, as `AGENTS.md` describes.
- **The injury lands in the later sets.** `tessa-injured` and `tessa-postwar` carry the right-hand injury. The earlier sets keep both hands healthy.
- **Splitting sets is a data edit.** `camp-healer` covers the S027 and S055 healers. Split it if S055's healer is a separate attendant.
- **Roles with one to four lines can wait.** The name above the text still identifies the speaker without a portrait.

## Priority 2 — one establishing painting per scene

One painting per scene is the baseline. It puts every scene on its picture, with portraits carrying the exchanges, as S005's window scene does. S053 continues S050 on the same stair, so it reuses that painting.

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

## Priority 3 — key-moment paintings

Some beats fail as one held painting. They need their own images, added as extra stages in `staging.json`. Each needs a scene brief written from the screenplay first. From the [outline](../outline.md):

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

## Corrections to existing art

Found while building and reviewing the new screens:

1. **Done locally:** the dead-phone detail was nearly black. Look closer details are now graded at reduced strength, so the phone's edge and dead screen read while the image stays nocturnal.
2. **The arrival foot meets the text.** In `art/opening/cg/arrival.png`, Tessa's landing foot sits where the reading text begins, and the game lifts the painting 70 px to compensate. A recomposition with the foot higher would remove the lift.
3. **Iven's position below the dais falls under the text.** In `art/rovel/cg/ceremony-intervention.png` and `ceremony-yield.png`, Iven's boots and the step edge between him and the dais sit under the reading shade, so the staging point is weakened. Lifting the painting cut off Orra's and Senn's heads instead, so the fix belongs in the painting: keep the step edge above y ≈ 820.
4. **Existing paintings are a little soft.** S001–S005 are 1672×941, upscaled to 1080p. Regenerate new work at 1920×1080 or larger.

## Needed, but not images

- **Look closer beyond the first three threads needs writing before art.** The R02–R05 threads in [investigation.md](../investigation.md) need authored material before any detail images are made.
- **The game has no sound.** Music, ambience and sound effects don't exist yet.
- **The final "Yes" is deferred.** The response to the final question stays deferred, as the brief says.
