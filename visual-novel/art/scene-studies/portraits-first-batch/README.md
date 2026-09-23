# First queued portrait sets — 23 September 2026

Requested: render the first few requests in `art/asset-request.md`. Bounded scope: the first three Priority 1 sets, Lucan early, Valcair and Lucan later, speaking and listening views. These are portrait components, not completed scene coverage or a new interface direction.

## Pre-render briefs

All six: square transparent head-and-upper-shoulder paintings; generous headroom including horns, ordinary natural eye size, face around half the image height, eyes around 45% down, lower crop through clothed upper chest. Speaking faces screen right; listening faces screen left. Mildly insistent ordinary light, no baked location, UI, frame or text. Match the written designs and existing working character keys; these keys are not user-selected likenesses. No hands or independent prop interaction in these compositions.

**Lucan early:** mid-twenties northern prince, uninjured. The S018–S024 encounter (source 793–1070) establishes practical urgency, distrust that permits cooperation, concern for Serat, and defiance of his father. Before speaking at the ferryhouse he has returned a child to her mother and supports a wounded man; afterward he negotiates passage and returns for the human litter. Those actions belong in future scene paintings, not these isolated portraits. Dark bottle-green riding coat and pale shirt; no crown, shoulder weapon or field seal in the portrait. Speaking: focused, earnest assertion, slight natural mouth opening; listening: searching attention, mouth closed. Gaze room makes the offscreen interlocutor legible. One baseline pair does not cover the later laughing drawing or acute Harrow grief.

**Valcair:** apparent early fifties, broad-built northern ruler and Lucan's father, medium-brown skin, weathered face, close beard, silver through dark hair, larger backward-swept black horns. S010 (434–484) establishes deliberate military command; S023 (1008–1053) and S046 (1784–1842) contrast paternal concern with coercion. Render the field/armor state from the existing working key: dark steel over charcoal wool with restrained dark-red collar lining, no crown, spear, active ward or invented scar. Speaking: controlled authority rather than a sneer; listening: measured scrutiny. Private-room wool variants are a separate outstanding wardrobe request; this field pair must not stand for those scenes.

**Lucan later:** the same man, modestly older within his twenties, carrying fatigue and pressure after Harrow. S038 (1555–1592): probes Marren's account, Vask interrupts, he leaves without the copy. S046: confronts his father, refuses the offered dry coat, leaves. Bottle-green coat and pale shirt remain; cloth is worn, grooming less tended, eyes tired, face slightly drawn. Speaking: quiet insistence; listening: hurt, guarded concentration without a stock scowl. No invented facial scar or gray aging. Crop excludes forearms; neither invent nor erase the left-forearm wound that begins only at S044. Later torn sleeve, dressing and guarded ribs still require scene-specific coverage.

## Review

Status: **component-reviewed working assets; scene integration pending; not user approval**. All six selected exports are 1254×1254 RGBA PNGs with real transparency, generated with the built-in image tool. The first attempt to pass local reference paths failed in the sandbox; visible native crops of the same working keys supplied the references. No external API or GIMP finishing was used.

| Set | Speaking | Listening |
| --- | --- | --- |
| Lucan early | [PNG](../../../renpy/game/art/portraits/lucan-early-speaking.png) | [PNG](../../../renpy/game/art/portraits/lucan-early-listening.png) |
| Valcair, field armor | [PNG](../../../renpy/game/art/portraits/valcair-speaking.png) | [PNG](../../../renpy/game/art/portraits/valcair-listening.png) |
| Lucan later | [PNG](../../../renpy/game/art/portraits/lucan-later-speaking.png) | [PNG](../../../renpy/game/art/portraits/lucan-later-listening.png) |

[Exact generation and refinement prompts](../../prompts/portraits-first-batch/) · [State/provenance manifest](manifest.json) · [Runtime frame captures](review/).

**Corrections made:** the first later-Lucan renders looked too close to his early condition. Targeted edits deepen the eye-socket shadows, redden tired eyelids and draw the cheeks while retaining his face and twenties age range. Automatic face boxes then cut the horns out of the UI. Six manual framing overrides in `portrait-faces.json` restore headroom, horn tips and clothed shoulders. No portrait pixels were stretched or cropped to hide those problems.

**Actual inspection:** opened all selected full PNGs, native face/horn/hair-alpha detail against grey, and all twelve complete 1920×1080 Ren’Py frame captures (viewed at 1280×720). Each capture places the same asset at the production speaker and listener sizes, using the unchanged `say` screen and arch masks. Intense and Softened are both represented. The neutral review background is deliberately not a scene painting; these are component-fit checks, not a connected passage or scene-lighting review.

**Visible findings:** Lucan's open-mouth speaking views turn right; the closed-mouth listening views turn left. The broader mouth, long nose, brown complexion and restrained horns remain consistent with his working key. Later views have visible under-eye exhaustion, most legible at speaker size. Valcair's larger horns, silver hair, beard and heavier shoulders distinguish father from son. All final frames retain headroom and transition through clothing into the bottom shade. Native hair edges have no conspicuous solid-background fringe. Listener expressions remain subtler at 150 px width, and final scene lighting/performance combinations still need review with their paintings.

**Wardrobe split:** the armored Valcair pair is assigned only to S010 and S054. `staging.json` now requests `valcair-private` for S023/S033/S046; charcoal-wool speaking/listening portraits remain to make. No private portrait or new story action was invented to complete the table.

**Checks:** `portrait-faces.py` completes with six deliberate new overrides; `check-staging.py` passes. The isolated Ren’Py capture completes with twelve screenshots and no assertions; it is not a regression or artistic test. The existing `staging_pipeline` regression separately passes all 12 assertions. Ordinary-light portraits intentionally share their source PNG across both lighting settings, as the asset request allows. No scene paintings, UI redesign, package rebuild or full-route visual clearance is included.
