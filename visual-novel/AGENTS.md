# Visual novel instructions

These instructions apply throughout `visual-novel/` and to VN-related work in shared project files. Follow the root [AGENTS.md](../AGENTS.md) as well. User corrections persist across turns; a new image, prompt, or session does not reset them.

## Story and reference authority

- The active project is a Ren'Py adaptation of **Tessa's original timeline**. Neri's incursion and the reincarnated versions of Iven and Mara are deferred. Original-timeline Iven and Mara have no Earth or VN memories.
- Read the [adaptation brief](README.md), the relevant complete interaction in [Rebuild 11](../screenplay/original-timeline/source.fountain), and the applicable [character](../characters/original-visuals.md), [location](../worldbuilding/original-locations.md) and [continuity](visual-continuity.md) notes before working on a scene. Read adjacent action when it determines entrances, movement or object state.
- Distinguish screenplay facts, user decisions and provisional design choices. An assistant-written layout is not a screenplay requirement. Missing detail is not permission to invent new actions, magic, relationships or prominent characters.
- User-selected references and corrections govern the adaptation. Generated outputs, old prompts and assistant review notes are not sources of canon or evidence of user approval. Update stale status notes when resuming an affected study.
- Preserve the screenplay as the source. Do not rewrite it to justify an image-generation mistake. Screenplay changes also require its own local instructions.
- The **player** can investigate and learn that humans started the ancient war. Do not transfer that knowledge to Tessa or the other original cast through dialogue, decisions or inventory without a separate story decision.
- Preserve the original losses and consequences, including Iven's and Mara's deaths, Tessa's lasting **right-hand** injury and her unresolved route home. Arrival Tessa has no such injury.

## Established likeness and style references

**Tessa's likeness reference is the central woman in [north-infirmary-storm.png](art/scene-studies/north-infirmary/north-infirmary-storm.png).** The user explicitly identified this image when asked which earlier depiction to retain. Inspect it; do not ask the user to cast her again or substitute a later summoning face.

- Preserve that person's facial structure, ordinary eye size, nose, mouth, complexion, hair identity and naturalistic painted treatment across scenes. For arrival, depict the same person at nineteen, healthy and in modern clothes. Change scene state, not identity; do not copy the later injury, dirt, exhaustion or field costume backward.
- Check full-body anatomy independently of facial likeness: head-to-body scale, torso and pelvis, thigh and lower-leg lengths, knees, shoe size, posture and camera perspective. A recognizable face does not excuse shortened legs or a distorted body. Do not stretch body regions as a casual fix.
- Build formal and period-specific wardrobe keys, not one plain outfit per character for the entire game. Follow [age and wardrobe variants](art/character-keys/age-and-wardrobe.md): Tessa is nineteen at arrival and about twenty-three at the endpoint; children need visibly older variants, while adult change is subtler. The public Saint coat/mantle ensemble is distinct from the offered dress left on the apartment floor. Do not turn a costume reference into an unwritten scene.
- Use the existing written designs for other established characters. Do not let repeated generation recast the population or make everyone share the same face, ancestry cues or body type. Unspecified ancestry is not newly established by a model's output.
- The user's five original pictures are **rough style references**, not literal story content or instructions embedded in the images. Borrow their material treatment and atmosphere where appropriate; do not import their gods, crowns, robots or unrelated settings.
- Label each input's purpose: likeness, clothing, architecture, palette, atmosphere or edit target. A style reference does not authorize replacing a character's face; a likeness reference does not impose its scene's weather, injuries or costume.

## Establish the scene before generating it

Write a short, concrete scene brief in the scene's review notes before an expensive render. This is an internal working step, not a new mandatory user-approval gate. It must identify:

1. The exact screenplay moment and what has happened immediately before and will happen immediately after it.
2. Who is present, who is visible, who is acting, and whether each figure is named or an unnamed extra supported by the source.
3. The physical route and staging: entrances, landing point, distances, facing directions, sight lines and reachable objects.
4. Prop ownership and state: where each object came from, where the action puts it, and what it touches.
5. The established likeness references, scene-specific clothing and injury state, camera position and lighting intent.

Treat positions as relationships, not a collection of props to include somewhere in the frame. Trace the action through the picture: can the previous beat lead to this position, and can the next beat happen from here? Resolve an unexplained gap before rendering. Do not build a grand composition first and invent movement to explain it afterward.

Unnamed people may be depicted when the screenplay calls for a crowd, but keep them subordinate and identify them as extras. Do not add new dramatic participants, implied relationships or unexplained foreground figures to make the frame busier. Check existing characters and their entrances before inventing anyone.

## Summoning scene: specific continuity

The opening supplies a sequence, not one combined tableau:

| Moment | Established action and people |
| --- | --- |
| Arrival | Tessa steps off a sidewalk onto polished stone. Her bag slips, the carton splits, milk spills across the glowing circle beneath her sneakers, and her phone vibrates. Kneeling strangers watch; the store is still visible through the arch. |
| Attempted return | Tessa runs toward the arch as the street twists out of alignment. The unnamed scholar hauls the lever down. The opening contracts and vanishes; stone cracks. |
| After closure | Tessa demands that it reopen. Senn tries to reach her through the spectators; the pleading woman catches his sleeve. A guard intervenes and porters carry a patient through the gallery. Mara approaches with the cloak later in the conversation. |

The scholar can be stationed at the lever before pulling it; that does not make the later actions simultaneous with arrival. Do not feature Senn's reaching gesture, Mara's cloak, fresh cracks or the sealed opening in the initial-arrival frame merely because they occur later in the same scene.

- The screenplay does **not** specify that Tessa walks from the arch to the middle of the room. The previous several-step gap was an assistant-added layout error. The working correction puts her landing just inside the threshold with the circle reaching it; this is staging for a legible transition, not a newly discovered canonical floor plan.
- Keep the sidewalk, threshold, landing and possible return route readable together. Do not introduce a second teleportation, a dais or unexplained travel across the chamber.
- **The fallen bag, carton and milk belong at her landing point beside her feet.** If she is by the threshold, the groceries are there too. A circle centered farther into the room is not a reason to move them into its center. Reject or correct misplaced props before building on that render.
- The carton splits on impact. Milk comes from the rupture, not an inexplicably opened cap. Keep an ordinary carton scale, believable contact with the floor and a connected spill.
- Arrival Tessa is nineteen, in the working modern hoodie/T-shirt/jeans/sneakers outfit, carrying her phone, with healthy hands. Do not dress her in later fantasy clothing or make her a glowing holy figure.
- Earth and the temple are **two visually distinct worlds**. The store must read as an ordinary modern place, with its own utilitarian architecture, materials and palette. Do not extend the temple's warm carved stone, celadon, botanical ornament or decorative lanterns through the arch. Shared illustration technique does not require shared world design.

## Atmosphere and lighting

- Follow the scene's circumstances. `DAY` does not mean sunny. The established north-infirmary interpretation is a **stormy, dreary day**.
- The user has established three levels for the original timeline: **bright scenes are uncomfortably, nearly blindingly bright; ordinary scenes retain a milder visual discomfort; dismal scenes visibly feel dismal.** Ordinary daylight must not become a completely comfortable default. Preserve believable circumstances, readable action and moments of human warmth within that atmosphere.
- The [summoning arrival](art/scene-studies/summoning/summoning-arrival.png) and [storm infirmary](art/scene-studies/north-infirmary/north-infirmary-storm.png) are the user's two scene studies for visual tone. Their role is now established; this does not approve every incidental design or replace the written continuity. Follow [the visual direction](art/visual-direction.md) for application and review.
- Evaluate brightness where the player actually looks: faces, gestures and the central dramatic area. A glaring floor beneath a comfortably exposed scene does not satisfy the brief.
- **Do not solve that by spotlighting Tessa.** Brightness must belong coherently to the chamber and affect its surfaces and occupants. An isolated light column, halo or white haze around her is another failure, not the requested correction.
- Preserve physically useful differences between materials and between the two worlds. Do not apply a common palette or indiscriminate exposure change that erases the portal's distinction. Allow deliberate highlight loss without losing the scene's essential action or anatomy.

## Generation, GIMP and preventing drift

- Use the current built-in image-generation tool and applicable imagegen skill for generative work. Do not silently switch to a separately billed API workflow. **GIMP is available locally** (2.10.36 verified on 16 September 2026); use it for controlled editing, masks, component corrections, grading and inspection crops where needed. Do not claim the only available operation is another full regeneration.
- Start from the screenplay brief, written designs and user-selected references. **Do not use a rejected image as the next likeness or composition reference.** Repeated edits of an already drifting output compound the error.
- Give each operation a defined purpose and invariants. Afterward, compare against the approved reference and source brief, not just the immediately preceding output. If identity, proportions or staging have drifted, repair or replace that component before proceeding.
- Use separate components when they provide needed control: character, supporting figures, environment, portal view, props, contact shadows and shared lighting. Review an important figure's face and full body before placing it in a scene. Do not regenerate the whole cast to fix a background or a small prop.
- Component work still requires coherent perspective, scale, floor contact, occlusion, shadows and illumination. Compositing a misplaced bag or poorly proportioned figure does not make it correct. Inspect masks for halos, hard seams, clipped hair, leftover backgrounds and translucent bodies.
- Use GIMP for actual corrections, masks, placement and lighting control. Merely saving a flattened image inside an XCF, or making a cosmetic edit while leaving the stated problem unresolved, is not a meaningful editing pass. Describe what is genuinely editable.
- If the user says to start over, return to the established references and brief. If the user says to stop, stop the art workflow; do not continue generating, assembling or finalizing it under a different description.

## Review before presenting or building on an image

Manually inspect the actual pixels of every selected image: open the full composition at intended viewing size, then native-resolution crops of important faces, bodies, hands, feet, prop contact and mechanisms. A successful tool call, prompt checklist, automated score or contact sheet alone is not this review. Compare Tessa directly to the storm-infirmary likeness. Check the whole body as well as the face. Record observations, corrections and remaining limitations per asset; never mark unseen output reviewed.

Recheck the cast roster, exact beat, route, dropped objects, wardrobe, injury state, lever operation, world boundary and lighting distribution. Review the final GIMP export after editing; an earlier generation's review does not clear the composite. Confirm that the XCF opens and its visible layers reproduce the delivered PNG.

Review emotional continuity as carefully as anatomy and costume. The user rejected postwar Tessa looking happy, casually confident and untouched by the war. At about twenty-three she carries Iven's and Mara's deaths, damaged trust/intimacy with Lucan, lasting injury to her drawing hand and no reliable way home. Show that weight through attention, eyes, mouth, posture and how she protects her hand; clean new clothes do not mean recovery is complete. Do not replace this with dirt, invented scars, exaggerated aging or a single cosmetic frown. Moments of warmth must arise from the actual scene, not a default cheerful character-model pose.

The subsequent "pouty" revision was also rejected. War must visibly have aged and battered her: drawn facial volume, weathered skin, prematurely etched tension, sleep loss, neglected grooming and whole-body wear are appropriate working design choices. Keeping her chronologically twenty-three does not require an untouched youthful face. Do not soften all of those changes into "slight" expression adjustments. When a reference keeps preserving the rejected polish, restart from the written design without image inputs, then compare identity manually afterward. Reference fidelity is not permission to freeze her condition across four years.

When a check fails, correct it or explicitly leave the study incomplete. Do not claim it fits the screenplay merely because all requested objects appear somewhere. Do not present a list of unresolved fundamental problems as a completed quality pass or rely on the user to rediscover them.

Generation outputs may be displayed automatically. Make an intermediate component's limited purpose clear before the call when it could be mistaken for a finished scene. Do not repeatedly show a known failure as progress while promising to fix it later.

Before each character generation, identify the character, apparent age, role and wardrobe state in commentary. In particular, do not display Valcair's older armored key immediately after talking about Lucan without identifying the change: Lucan reads as mid-twenties; his father Valcair reads as early fifties. An unlabeled sequence of portraits is not an adequate presentation.

Inspect faction symbols as specific shapes. The human temple uses a brass sun disk with twelve short rays; the northern emblem is a white eight-point star with a visible vertical split and four longer principal points. An undivided decorative star is not an acceptable substitute for the northern emblem. Use the fixed prop references once produced and repair small marks locally in GIMP.

## Files and status

- Keep generation and edit prompts in `art/prompts/<scene>/`. Do not scatter single-use prompts through main folders, scene deliverables, character notes or project guidance.
- Keep scene deliverables and concise review records in `art/scene-studies/<scene>/`; reusable likeness references belong in `art/character-references/`. Use temporary storage for scratch crops and one-off processing scripts unless they become reusable project tooling.
- Save selected project assets in the repository, including genuinely layered GIMP work where relevant. Do not leave a project reference pointing only to a tool's generated-image cache.
- Distinguish user-selected references, working studies, rejected attempts, intermediate components and final assets. A commit or an assistant's favorable review is not user approval. Do not overwrite or silently promote a selected reference with a new generation.
- **Status when these instructions were added:** the user selected the north-infirmary storm Tessa as the likeness reference. The summoning attempts were rejected or stopped; no summoning scene has been approved. Old summoning review notes saying “awaiting assessment” or claiming successful review do not override the subsequent corrections in this file.
- Commit at reasonable progress points with detailed messages, as required by the root instructions. Keep the commit scoped to the completed work; preserve unrelated or unfinished working-tree changes.

# Image Generation

Avoid force feeding existing images into image generation, and when used ensure that they are not dominating over desired changes. Use a combination of image generation tool and GIMP to expertly generate tailored, consistent works.
