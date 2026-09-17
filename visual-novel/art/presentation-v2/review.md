# Original-route presentation replacement

**Status: rejected by the user, 16 September 2026. Substantial work remains.** This checkpoint does not pass scene or presentation review. The user identified missing sprites and performances, empty scenery carrying dialogue/action, an inadequate UI, missing speaker-positioned dialogue boxes and an obstructive opening lever placement. The isolated inspections recorded below did not adequately review the connected playthrough. In particular, disabling older sprites left scenes without the cast their prose describes. Earlier favorable observations are limited historical inspection notes, not clearance to reuse these assets as an approved baseline.

Follow the [revised completion gates](../../presentation-redesign.md#scene-completion-gates). The current instruction is to commit the unfinished work and discuss the requirements before further production.

Scope: the original playthrough. No post-Yes interface work. The first replacement sample integrates new scene art, reading/utility screens and an actual Look closer connection. This record distinguishes individual scene coverage from the still-unfinished full-route art production.

## Scene briefs before generation

### S002 — the mother's chair, source lines 108–112

Mara has left with the rejected gray cloak; the door is locked, and Tessa's phone battery has died. She has pushed the chair against the door. She draws her mother's kitchen on the reverse of the temple welcome letter, tears the paper with her pen, and starts again with her mother's chair. Tessa alone is visible. No Mara, Iven, Senn, extra visitor or ghost.

Tessa is nineteen, with healthy hands, wearing her faded blue hoodie, cream T-shirt and jeans, no cloak, brace or Saint costume. Likeness: the user-selected north-infirmary face, interpreted as the healthy arrival age. She draws with her anatomical right hand. The dark-green phone lies dark beside the paper. The window chair is at the door; she sits on the second wooden chair specified in the room's working furnishings. Candlelight reaches the hand, paper and part of the face; the cold room remains very dark. No magical aura or later-war exhaustion. The modern ballpoint is a visual choice the user accepted as something she could have brought with her; the screenplay itself only specifies a pen.

Camera: intimate oblique view across the writing surface, Tessa on the right, open negative space/window darkness to the left. Her attention is on the ordinary chair she is trying to remember. Mood: acute homesickness and stubborn concentration, not ornamental sadness. Full composition is a story CG; a crop of the drawing becomes an inspectable detail. The title may use this same authored moment with separate framing and a text scrim, never a pasted-in portrait.

### S001 — after the arch closes, source lines 29–49

The return opening has vanished and cracked. Tessa has reached it and asked for it to reopen. Senn approaches after the pleading woman is drawn aside; soldiers block the route toward the scholar. Tessa and Senn are the focal participants; supported guards/porters can remain subordinate in the depth. No Mara's cloak yet. Tessa is nineteen in modern arrival clothes with uninjured hands. Senn reads late fifties in cream/wheat robes, short tended sandy-gray beard and thinning hair, with limited twelve-ray sun embroidery. He does not touch or hold her.

Camera: an asymmetric medium encounter near the now-sealed threshold. Tessa turns from the failed exit toward Senn; they look at each other at plausible distance. Groceries remain near the threshold, not at the center of the room. The source transition before this exchange will need its own arrival/open-arch and closing-action shots.

Light: painful, nearly blinding dawn reflected broadly through pale stone, affecting both people and central gestures. Preserve modeled facial planes and believable shadow directions. Earth is no longer visible after closure. No isolated beam on Tessa, bloom around her body, or uniform white veil.

## Review status

The Senn head edit (prompt 04, tool output `exec-ad5b4e34-cf04-45d3-a6be-815514778b63.png`) is **rejected by the user** for divergence toward baldness. It also changed facial volume and apparent age. It is not copied into runtime or used as a reference. The pre-edit head in `raw/sealed-arch.png` remains the base for this shot; the remaining correction is local GIMP lighting. Senn has a written working design, but no separately user-selected likeness key; his older runtime sprite belongs to the rejected batch.

## Implemented checkpoint scope — not cleared

Two beat-specific CGs, the reading/title/utility interface and the first-night Look closer / Threads sample are implemented. This is partial coverage, not a finished opening sequence or full-route visual pass. The complete original screenplay and ending remain in place. No post-Yes artwork or interface has been developed.

The current wiring is recorded in [manifest.json](manifest.json); it is not an approved reuse whitelist. Old character cutouts are disabled, creating missing cast coverage around the two CGs. The arrival action, Mara's exchange and the remaining performances still need replacement production. Neither restoring inconsistent cutouts without review nor leaving absent characters is an acceptable final solution.

### Mother's chair

- Compared the face to the selected storm-infirmary crop; the younger cheek volume and healthy hands suit arrival Tessa. Viewed the final full frame, native face, pen grip, left hand, paper, phone and their contact with the table.
- The first generation inherited ornament on the hoodie and exaggerated the tear. GIMP masks use the corrected plain cotton clothing and a smooth cream letter with a short slit while retaining the original face, hands and room.
- A clone/heal attempt left a visible rectangular paper patch. It was discarded. The final small generated paper component contains no face or body; a registered, feathered mask removes the premature counter sketch beside the restarted chair. The master retains the original and each correction separately.
- The modern blue pen remains: the user accepted it as something she could have had with her. That is a visual continuity choice, not a source-established origin for the pen.
- Runtime use begins at **line 112**, after the tear and restart. The left-side text leaves her face, hands, page and phone visible. In-browser views at 1440×900 and 1280×720 show legible prose and reachable controls. The image is a held scene illustration, not a new sprite or a complete apartment sequence.

### Sealed arch

- Viewed full composition and both faces at native resolution. Tessa and Senn share eye contact; the arch is sealed and cracked; modern clothes and healthy hands are preserved. The frame excludes the groceries and lever rather than moving them into invented positions. No Mara or cloak appears prematurely.
- The head-edit output is rejected as recorded above. The delivered image retains the **pre-edit** face, hairline, hands and geometry. GIMP applies a broad reflected-light mask across both figures and the pale room; no regenerated head is composited in.
- Expanded the light mask after a first pass favored Tessa over Senn. The delivered face planes, gesturing hand and pale room all participate in the severe light. Eyes and mouths remain legible. This is a working shot, not a newly approved character key.

### Interface and discovery

- Replaced the boxed title/sidebar system with an authored title composition, full-screen scene presentation, restrained controls, and shared typography across utility screens.
- Actual pixel review caught a vertical SVG gradient that obscured the bright illustration and a settings slider that pushed controls off screen. Corrected explicit gradient percentages and bar dimensions, then reopened the browser screens.
- Look closer enlarges actual details from the scene. A related detail can be placed alongside the first, followed into a short editorial passage, and revisited through Threads. The earlier milk message is quoted from the screenplay. No new character actions, ancient documents, quiz answers or character-knowledge disclaimers are added.
- The ancient-origin reveal and remaining discovery connections still require writing and illustration; removing the old quizzes does not count as completing that material.

See [QA](../../renpy/QA.md) for separate source, native-state and browser checks. Manual inspection and a commit do not imply user approval of the replacement.
