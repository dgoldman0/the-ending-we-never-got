# Batch 8 stair continuity — items 64 and 72

**Current status:** the user explicitly authorized the four-reference transfer with “Proceed.” [S053 item 72 is now delivered](s053-completion/README.md), including the dry floor, open platform, bottleneck and preserved dark hair. S055 item 64 is undergoing final geometry correction. The earlier blocker and local trials below are historical.

Working corrections, not approval of the full game. Start from current runtime scenes carrying the batch 6/7 local repairs; preserve those figures and effects through masked GIMP composition. No grading, staging or UI changes.

## Brief before generation

S053, source lines 2052–2054: Tessa has entered the throne hall; Olan and Elin remain at the inner landing. Mara is alive at the exterior bend, sword in right hand and shield on left arm, closing the gap while her last uninjured human soldier supports a wounded man upstairs. Two northern attackers reach her from the left foreground. The wide dry flagstone landing and right ascending flight belong to S050; its top opens onto sky, not an enclosed corridor. Make the passage toward Mara only two men wide by adding broken shields across the otherwise open route beside her, leaving the retreat up the stair behind her usable. Give the carrier dark, longer tied hair so he cannot read as Olan. Preserve Mara, both attackers, both supported bodies, sword/shield handedness and local horn fixes. Predawn, winter, no new precipitation.

S055, source lines 2129–2131: Mara is dead on the defended bend after the pulse/cloth beat. Tessa in her campaign coat, wounded bandaged right hand, and Elin with the torn blouse sleeve kneel beside her; the grey-bearded human healer holds the cloth. Olan blocks Lucan, who keeps his dressed left arm against his ribs and wears the torn green coat. His two northern men and Orra's human guards remain on the side flight. Preserve these existing people, poses, expressions, clothes, horns and injury state. Extend flat landing floor from around Mara toward the camera: no raised slab or sheer drop in front of her feet. The stair down is at the landing's right side, separated by the timber handrail; upper flight rises behind Olan. Replace pale limestone with dry, dark weathered grey stone continuous with S050 and the immediately preceding s055-mara. Keep the snowy distance and overcast morning. Camera change is authorized but first try preserving exact cast registration.

Input roles: current runtime PNGs are edit targets and preservation sources. S050 / s055-mara are architecture, dry material and continuity references, not substitutes for the target state. Built-in imagegen supplies correction donors; GIMP owns native masks, restoration of unchanged regions and layered masters.

## Source pixel inspection

The morning target has a near-vertical foreground retaining wall instead of walkable landing, overly pale clean masonry, and pale fringes around figures. S053 visibly has reflective paving, an enclosed torchlit passage at the top and a large open floor strip to Mara's left (screen right). Both sources were viewed at 1920×1080 through GIMP JPEG review exports because view_image itself fails with the environment's mountinfo sandbox error.

## Local trials and generation access

The built-in generator could not read `referenced_image_paths`: the filesystem helper reports `mountinfo path is not absolute`. Native viewing used GIMP JPEG exports through a read-only shell display. Automatic approval review then rejected redisplaying those images specifically for built-in image generation, twice (second attempt supplied exact Batch 8 and AGENTS authorization). Reason: it required explicit permission to send these particular project assets to that destination. Root is handling the approval question. No generation succeeded in this subtask yet.

Two local GIMP architecture trials were made and **rejected before runtime installation**. `s053-bend-local` has visibly pasted shield fragments, incomplete platform masking and pale floor fringes around boots; it does not establish a convincing bottleneck. `s055-citadel-lower-stair-morning-local` demonstrates the intended broad floor direction but retains bright stone halos around cast, a stretched ground plane and obvious joining edges. These are diagnostic intermediates, not deliverables or model references. Their XCF masks are editable but not finished.

`s053-carrier-only` is the clean local partial correction: source auburn hair changes to charcoal brown inside its existing outline; body, face, hands, weapons, sky, floor and all other pixels remain unaffected. It does **not** complete item 72's geometry/material corrections. Source-before snapshots stay intact.

## Earlier safe partial — 29 September (superseded by the completion above)

The first carrier-only mask did **not** pass closer review: its all-hue adjustment darkened a sliver of blue background and left orange source hairs at the right rim. That earlier favorable assessment is superseded. The final master uses two hue-specific corrections (red/yellow only), a corrected hair outline and a separate original-ear/nape restoration layer. Inspected the final full 1920×1080 scene, native carrier crop and 4× edge comparison. No angular backdrop fringe or missed orange hair band remains, and the ear keeps its source skin colour.

The revised `s053-carrier-only.png` is installed at `renpy/game/art/scenes/s053-bend.png` as an explicitly partial item 72 repair. Only 2,324 pixels changed, within x1467–1536 / y29–77. Blue backdrop pixels (B−R > 10) have zero changes in the head review region. Reopened XCF export is pixel-identical; see `carrier-verification.json`. This establishes the small mask's integrity, not completion of the scene. S053 bottleneck, open platform and dry floor are still pending; item 64's morning image remains unchanged. No grading or runtime UI work was performed.
