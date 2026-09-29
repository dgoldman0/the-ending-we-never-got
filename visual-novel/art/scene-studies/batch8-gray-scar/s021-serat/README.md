# S021 Serat: Batch 8 local repairs

The source is the current runtime painting, including Claude's local corrections. The lead's initial pass aligns Serat's younger brother with the established man: medium-brown skin, narrow face, tied straight dark hair, temple horns, stand-collar green uniform and crossed straps. The brother's existing leaning support pose stays. The mask was widened before finishing to remove an old shoulder remnant at approximately x947–959, y139–153.

## Exact scene and finishing scope

At the Gray Scar covered landing, the adult cat has struck the closed gate and reaches a paw through its bars. Lucan's spent crossbow rests against the gatepost. Iven compresses and binds Serat's injured left thigh while Tessa slows the bleeding; Serat sags against his brother. The human woman lies on her litter nearby with her husband. The cat remains outside the gate; Serat will shortly be carried onto the second boat.

Two dedicated local crop edits finish items 69 and 71:

- The distant patient's grey head covering is replaced by uncovered light-brown hair. Her face, pose, husband's hands, blankets and litter remain.
- The bow arc is modestly shortened around the fixed stock, leaving a visible gap before the cat's paw. The string rests straight between the tips in its spent state. The old tip is removed, the paw remains unchanged, and a source layer protects the wooden stock at the mounting.

The earlier partial patient layer was removed. `edit-spec.json` and `build.scm` now reconstruct a five-layer master: untouched current source, brother correction, patient hair, crossbow limbs/string and protected stock. `pre-finishing.png` and `pre-finishing-edit-spec.json` preserve the lead's earlier candidate and exact widened brother mask. Only the two small finishing regions differ from that candidate.

## Review and verification

The complete final composition and native patient, bow/paw and brother crops were inspected. The patient has brown strands instead of a grey band; her face is unchanged. The bow ends before the paw with a clean intervening background and a single straight string. No duplicate tip, new cat horn, floating old weapon or shoulder fragment is visible in this bounded review.

Freshly reopening `master.xcf` reproduces `candidate.png` exactly. [finishing-verification.json](finishing-verification.json) records hashes and zero changed pixels in the protected brother/shoulder area, the cat's head and rounded-ear region, the paw centre and the patient's face interior. It also confirms zero changes outside the two finishing regions relative to the lead's candidate.

The exact finishing prompts are [patient hair](../../../prompts/batch8-gray-scar/s021-serat-patient-hair.txt) and [bow/paw gap](../../../prompts/batch8-gray-scar/s021-serat-bow-paw.txt). Built-in image generation supplied the two donors from inspected GIMP crops using visible conversation image inputs; GIMP performed all mask, placement, compositing and export work. No CLI/API fallback, grading, staging or interface change was made. In-game review remains with Claude.

A second agent inspected the final full composition and native crops: the uncovered brown hair, separated bow/paw and corrected brother shoulder had no remaining definite mask or anatomy defect. The verified candidate now replaces `renpy/game/art/scenes/s021-serat.png` (29 September 2026). This is a bounded source-art review, not user approval or an in-game pass.
