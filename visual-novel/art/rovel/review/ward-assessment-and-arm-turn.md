# S003 assessment and arm turn — production and bounded review

17 September 2026. Component production and local visual review complete. Main-thread integration and connected-scene review remain pending; this record does not clear S003.

**Assessment, source 118.** After ward entry, Iven tends Olan's right hand. Two fingers are missing; corruption has crossed the morning mark toward the elbow. Blue healing has not begun and the wound edges still bleed. Visible close assessment cast: Iven, Olan and the older healer. Tessa and her escorts are elsewhere in the ward outside this composition. Preserve the current set and cast, with Iven supporting the hand and the older healer poised beside him. Remove blue light and its skin spill; introduce only restrained bleeding at the two existing missing-digit edges. No white light, new wound or added participant.

**Arm turn, source 150.** Following wrist-to-elbow purification and Iven touching cleared skin, Olan turns his right forearm so Tessa can reach the remaining dark patch beside the wound. His elbow remains supported by folded linen. The working pose rotates the hand from palm-up toward a dorsal/ulnar three-quarter view, exposing the edge where the right ring/little fingers are missing. Thumb, index and middle remain. Most forearm skin is clear; only the small final patch remains beside the existing wound. Tessa stays seated and works back toward it with white light. Iven stays beside her, the older healer and priest remain present, and Olan settles against the pillow. Repair the old duplicated jaw locally from the aligned first-purification source. No new wound, regrown digits or blue magic.

Use the built-in image tool only for bounded hand/action components, followed by GIMP masks and paired exposure grades. Existing whole CGs are local edit plates, not new likeness/style authority. No faces are sent for regeneration. Written character designs and Tessa's selected storm-infirmary likeness remain authoritative. Treatment clothing stays intact; Tessa has no ceremony badge or mantle yet. The palace ward uses ordinary uneasy light, distinct from the nearly blinding summoning register and dismal night.

The final review must compare both moments against the adjacent blue-treatment and purification views, inspect native hands/face crops and whole exports, and verify persisted layered masters. Reader-only blue/white detail crops follow only after their actual source image crops have been inspected for magic color, missing digits and corruption state. Main thread independently reviews before integration clearance.

## Production result

### Ward assessment

- Runtime pair: `renpy/game/art/rovel/cg/ward-assessment.png` and `renpy/game/art/softened/rovel/cg/ward-assessment.png`.
- Layered master: `art/rovel/masters/ward-assessment.xcf`. Ungraded composite: `art/rovel/raw/ward-assessment-composite.png`.
- The existing opening-sequence blue-healing master supplies the unchanged composition and cast. Aligned, naturally unlit local donors from `art/opening-sequence/raw/ward-conversation.png` restore Olan's palm and the older healer's resting arm/garment. Local room and coat texture masks remove the old blue halo and fingers without replacing faces. A small retained fingertip from `raw/blue-final.png` restores Iven's visible contact with Olan's palm while his other hand supports the linen.
- A separate transparent paint layer adds restrained bleeding at the existing missing-digit edges. No additional wound or injury was introduced. No transform was applied to the final palm donor. An earlier rotated-hand trial produced doubled tips and was discarded; an artificial-looking deglow trial was also discarded.
- Two bounded image-generation requests for this state returned output safety errors and produced no images, including a light-removal-only request. The final assessment uses the coherent unlit local sources and controlled GIMP masks instead. Prompt records remain in `art/prompts/rovel/ward-assessment-component.txt` and `ward-assessment-remove-light.txt`.

### Last patch / actual arm turn

- Runtime pair: `renpy/game/art/opening/cg/last-patch.png` and `renpy/game/art/softened/opening/cg/last-patch.png`.
- Layered master: `art/rovel/masters/last-patch-arm-turn.xcf`. Ungraded composite: `art/rovel/raw/last-patch-arm-turn-composite.png`.
- The existing last-patch master supplies the composition and downward treatment gaze. The built-in image tool generated only the local hand/forearm/action component from a face-free crop of `art/opening-sequence/raw/first-purification.png`. The selected component is preserved at `art/rovel/raw/last-patch-arm-turn-component.png`; its prompt is `art/prompts/rovel/last-patch-arm-turn-component.txt`.
- GIMP places that component through a contoured feathered mask. Separate clear-skin and patch masks move the remaining corruption beside the missing-digit edge rather than leaving it at the wrist. Earlier masks imported a pale rectangle and were corrected before the final review. A separate aligned first-purification jaw/neck donor removes the translucent duplicate without changing Olan's eyes, nose, mouth or expression.
- Olan's right hand now reads palm-down in three-quarter view, with the thumb and two surviving long fingers, exposing the last small branching patch near the missing ring/little-finger side. Tessa works over that patch with white light. The red morning mark remains and the rest of the visible forearm has cleared.

## Final pixel review and master check

Opened both whole exports for each state and their native hand/contact and face/neck crops. Assessment has no residual blue/white magic; corruption extends beyond the morning mark and restrained bleeding remains. The healer is at rest. Iven's supporting fingertip now visibly contacts the palm, resolving the ambiguous linen join flagged by the main thread. The arm-turn image has a distinct change in orientation from the preceding palm-up treatment; its final patch is near the wound and the duplicate jaw is gone. Faces were not sent for generation or recast.

The main thread separately viewed both ungraded compositions and the arm-turn native crop, found the source states and hand orientation legible, and requested the subsequent small assessment contact correction. Final graded assets still require its independent review in the connected scene. Source supporting-hand contact and exact arm angle are working staging choices, not extra screenplay facts.

Each master retains editable local donor layers, contour masks and the underlying original layers. Assessment also retains its separate bleeding paint layer. The top two layers are baked grade composites: `01 INTENSE` visible by default and `02 SOFTENED` hidden. Hide the first and show the second for Softened. Rebuild these two composites after editing lower layers; they are not live adjustment filters. The established ordinary-scene grade recipes were reapplied to the same corrected underlying composition for both variants.

Both XCF files were reopened in independent `gimp -n` processes and both lighting variants re-exported. All four runtime CG PNGs are pixel-identical to those reopened exports. Original raw files and old masters remain intact. Compared with the old Intense exports, changes are confined to assessment's action/garment area (x519–1231, y198–686) and last-patch's arm/neck area (x503–1459, y408–756); audited facial regions remain identical. Softened was rebuilt from the common ungraded composition and differs in some highlight values outside these local masks, so it is not represented as a strictly local pixel diff against the former Softened export. The new Softened whole frames were manually compared with the old one: the same identities and staging remain, with the corrected action and cleaner jaw.

## Reader comparison details

After manually opening all four actual crops, installed `art/rovel/details/treatment-blue.png` and `treatment-white.png` under `renpy/game/`, with identical-path variants beneath `art/softened/`. These are GIMP crops of the reviewed blue-healing and purification-cleared exports at x490, y440, width640, height300; neither crop generates new content.

Blue shows healing light above the damaged right hand while branching corruption remains across the forearm. White shows Tessa's treatment, Iven touching the cleared skin, and the same absent fingers. Paired crops use matching geometry and retain the meaningful difference in both lighting preferences. Reader-mode layout, captions, lighting-path integration and return behavior remain the main thread's runtime gate.

Scratch scripts and native crops are under `/tmp/source-gate-ward-states/`. `assessment-*-native-hand.png` and `last-patch-*-native-hand.png` expose the final contact/anatomy; corresponding `*-native-face.png` files expose cast/neck continuity. No shared code, source screenplay, unrelated runtime art or commit was changed in this bounded asset pass.
