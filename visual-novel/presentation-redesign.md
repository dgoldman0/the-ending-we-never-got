# Presentation redesign

Status: the user rejected the first playable game's interface, UX and artwork on 16 September 2026. The interaction direction in [Look closer / Threads](investigation.md) is accepted. The visual solutions below are the next development brief, not approved replacement designs. No replacement presentation is implemented by this document.

## What remains established

Rebuild 11 drives the story through the complete original ending and the separate question **“Do you wish to save Tessa?”** Preserve the cast, ages, wardrobe chronology, injury continuity and source actions. Preserve the selected storm-infirmary Tessa likeness and the user's rough references. Bright scenes must approach painful brightness across the dramatic area; ordinary scenes retain discomfort; dismal scenes must feel deeply dismal. Review quality must improve without diluting those requirements.

The existing source adaptation, save/rollback infrastructure and local web export can support the replacement. Their technical operation does not make the visual experience acceptable. The current runtime assets remain on disk for comparison; their presence and earlier review records confer no approval.

## Audit of the current presentation

Reopened the actual title, summoning, apartment, ceremony and discovery captures. The findings concern what the player sees across those screens, not whether individual files were generated or exported successfully.

| Area | Observed problem | Required change |
| --- | --- | --- |
| Title | A solid panel of equally weighted rectangular buttons occupies nearly half the screen beside an enlarged dialogue sprite. It introduces the software's controls before establishing the novel's atmosphere. | Compose the title as an intentional opening image with deliberate typography and clear priority for starting/continuing. Secondary functions need less visual weight. A dedicated title composition must not invent a story event. |
| Reading screen | The image is a framed rectangle inside another field of dark space. Location labels, dialogue and a distant control row break the screen into disconnected strips. A short line leaves a large empty band. | Design illustration and reading area together. Give the dramatic image substantially more presence; place readable prose and unobtrusive controls within that composition. Test short dialogue, long narration and larger text, not only a convenient sample sentence. |
| Character performance | Repeated standing poses and fixed expressions carry exchanges with changing emotions. Oversized crops substitute for staging; figures disappear on narrated action. | Plan shots around dramatic beats. Use purposeful expression, gaze and pose changes, reaction views and action illustrations. Hold continuity when prose resumes. Choose close framing for dramatic reasons rather than to hide an unproduced action or incorrect hands. |
| Art integration | Individually detailed figures read as cutouts placed against separately made rooms. Comparable exposure alone does not establish common space, depth or contact. | Establish camera, scale, perspective, occlusion, directional light and material response for each composite. Review a figure in its intended shot before extending that figure's asset family. |
| Rendering | Smooth, highly finished-looking faces and dense repeated surface detail coexist with weak staging. The ceremony's raised values wash out facial form and make its ornaments compete for attention. | Direct painting, edge detail and texture toward the dramatic focus. Preserve natural facial structure, tactile materials and purposeful variation. Brightness must arise from a convincing severe light environment; a uniform whitening curve is insufficient. The dark register likewise needs intelligible spatial lighting rather than a uniform dark overlay. |
| Interface identity | Heavy teal blocks, repeated boxed buttons and several similar text levels look generic. Discovery adds a second column of navigation before the material itself. | Develop a restrained interface informed by the world's materials and visual vocabulary. Establish a clear type hierarchy, spacing and interaction language across title, reading, Threads, history, saves and settings. More ornament or a different font alone does not solve the composition. |
| Discovery experience | Long explanation cards state conclusions and editorial limits; answer choices test recall. Character-knowledge disclaimers expose production rules. | Implement visual inspection and connected discovery under the accepted interaction contract. Show the detail and its relationship before explaining a conclusion. Keep internal rules out of the experience. |
| Coverage and rhythm | Most of the route is unillustrated; opening action is frequently left as an empty location plate. A long technically traversable route was treated as a presentation milestone. | Build a coherent representative sequence to the intended standard, then plan scene-specific production against it. Missing scenes remain explicit production work; generic portraits and location cards cannot stand in for completion. |

Representative rejected captures: [title](renpy/review/28-packaged-title.png), [bright ceremony](renpy/review/18-ceremony.png), [dark apartment](renpy/review/12-apartment.png), [discovery](renpy/review/21-origin-context.png). These are audit evidence, not visual references for the replacement.

## Direction to develop

The scene should command attention first. Typography and controls should feel deliberately placed within the novel's presentation, with readable text and visible keyboard focus. Explore a larger, immersive illustration field with a restrained reading region; settle exact layout, typography, material treatment and transitions in the running game. No specific new art style or final interface layout is approved by this brief.

Develop one consistent visual language across title, dialogue, narrative action, close inspection, connections and utility screens. Keep utility navigation concise and predictable. Retain history, save/load, larger text, reduced motion and descriptive access. Inspection targets need keyboard/list equivalents and clearly discoverable affordances; attention should be rewarded without pixel hunting.

Treat brightness as scene direction. Shape space with source light, reflected light, cast shadows, glare, material differences and selective loss of detail. In a bright scene, faces and gestures must participate in that painful environment while retaining the essential anatomy and action. In darkness, limited practical light must support staging and emotional attention. A better painting must not silently normalize the user's requested extremes.

The built-in image generator and GIMP are both available. Start replacements from source briefs, written designs and selected references. Use GIMP for meaningful masks, local repair, compositing and controlled lighting; retain editable sources. Repeated full-scene generation and unexamined global grading are not substitutes for art direction. Do not use the rejected runtime batch as its own identity/style standard.

## Next development sequence

1. **Shot and interface composition:** design the title and connected summoning-to-apartment reading sequence together. Identify the action, reaction and object inserts needed by the screenplay before producing assets. Test the reading layout with real short and long lines. Layout studies must be explicitly labeled as such.
2. **Finished visual sample:** produce and integrate a representative bright exchange and dark exchange with the correct participants, active expressions, staging and lighting. Carry a short stretch of narration and dialogue so the sample demonstrates continuity rather than one flattering screenshot.
3. **Actual discovery sample:** build one inspect → related detail → connection → return interaction. The cut binding, translations and earlier promise offer a source-backed candidate after those scenes have been encountered. Exact selection and presentation remain development choices; do not reveal later evidence early or invent the missing pages' contents.
4. **Browser review:** inspect the integrated result at 1280×720 and a larger browser window, including larger text, keyboard focus, controls, menu return and image/detail readability. Check the three lighting registers across the eventual sample set. Test saving after a discovery and returning to the same place after reload separately from aesthetic review.
5. **Production expansion:** apply the demonstrated visual language to the remaining cast and scenes, with explicit action/expression/age/outfit coverage. Preserve scene-specific direction; a template that makes every encounter look identical has failed even if its assets are consistent.

These are work stages, not approval requests. The current user instruction locks the discovery concept and calls for a broader presentation reset; it does not approve an unseen replacement or settle the unresolved ancient history.

## How to judge the next build

A functioning screen is the starting condition. Review whether attention goes to the intended dramatic detail, whether the figures inhabit the room, whether a reaction belongs to the actual line, whether moving between reading and inspection feels natural, and whether the complete screen has a deliberate visual identity. Read the sequence at ordinary pace rather than examining only isolated assets.

Keep technical, source-continuity and aesthetic findings separate. Record specific visible defects and corrections. Reopen final GIMP exports and inspect actual in-game composites; do not clear them by counting assets, matching source keywords, saving an XCF, or citing passing traversal tests. Earlier favorable assistant review does not override the user's rejection.
