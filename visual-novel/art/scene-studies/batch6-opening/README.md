# Batch 6 — opening repairs 18, 20–22

Completed and promoted to `art/repaints/`, 26 September 2026. Started from the current neutral copies under `renpy/game/art/base/`; deliver same basenames under `art/repaints/`, without changing the base or runtime files. Current Iven coat and forearm fixes remain intact outside explicit masks.

Read source lines 7–71 (complete summoning interaction) and 121–187 (complete first treatment), character designs, location and visual-continuity notes. Existing illustrations have fixed camera, character positions and exposure; local repair donors are masked into those original pixels.

- **18:** Olan has lost his RIGHT ring and little fingers. Preserve thumb, index and middle, established dressing, other hand, ordinary skin after cleansing and corruption before it. Repair `rested-hand`, `treatment-pause`, `after-first-treatment`, `treatment-white`, `treatment-blue`. The first three show the hand resting; the latter two show the palm up. Do not mistake a healer's supporting fingers for Olan's.
- **20:** Clean-shaven summoning scholar in his forties; medium-brown skin, straight black tied hair, soot-gray forearm sleeve covers. Match current `scholar-speaking` while keeping actual lever grips, head angles and robe construction in `arrival`, `attempted-return`, `closure`.
- **21:** Split carton spills milk across circle immediately at impact. Maintain that wet floor state through `attempted-return` and `closure`; preserve carton and bag positions. On `phone-message`, move blue band to the carton's opposite end to match `milk-impact`, without changing phone/message/hand.
- **22:** Mara is 32, broad shoulders, olive-brown skin, square jaw, slightly heavy hazel eyes, strong bent nose and dark-brown braided hair pinned low. Match `mara-controlled-speaking`, keeping each actual expression/pose/collar. `stretcher-passes`, `unanswered-cloak`, `ward-entrance`. Additionally, `stretcher-passes` must have the round carved sealed arch seen in `closure` and plain cotton cream T-shirt, blue zip hoodie, dark denim jeans; no brocade on Tessa's modern clothes. The gray wool offered cloak remains gray.

Review whole frames first, then native detail and reference likeness; inspect every mask boundary. Compare source and final RGBA for zero changes beyond authorized local masks. Reopen each layered XCF and compare its rendered pixels to the delivered PNG. Root and peer review are required before claiming cleared delivery. No connected runtime clearance is implied.

## Actual finishing and review

The adjacent `unanswered-cloak` arch also had the pointed/bare shape. Root explicitly authorized the same bounded architectural repair there, preserving the figures. Both shots now agree with the round carved sealed arch in `closure`.

Built-in image generation supplied tightly framed local donors; GIMP supplied every production transform, mask, layered master and PNG export. The sources retain their original dimensions, rather than being upscaled. `rested-hand` is the existing exact crop of `treatment-pause` at (780, 428), so those views share the same hand correction and match exactly in the affected region.

The first `ward-entrance-mara-donor.png` shifted Mara's head pitch and collar. It is rejected and retained only as a diagnostic component; the actual recipe uses `ward-entrance-head-donor.png`, generated from a tighter target with the original closed mouth and downward head angle. Early hand masks also produced edge remnants; the final masks remove the extra digits and keep the other people's hands distinct. The blue close-up mask was reduced to the missing-digit area after root identified a contact-edge notch.

Producing-agent review covered every whole candidate and all changed regions at native size, against current scholar/Mara portraits, original modern clothing and the arch/carton continuity. The river agent independently reviewed all twelve candidates: whole scenes, native faces/forearm covers, milk and packaging, Mara and architecture, all five hand views. It found no remaining blocker in the requested repairs. Root then reviewed the final whole scenes, native hands, faces, sleeve covers and prop corrections, and cleared all twelve for delivery. All twelve same-basename PNGs are now copied to `art/repaints/`; `delivery-files.json` records source and delivered hashes. Base and runtime files were not changed. The other team still handles integration, grading and connected reading review.

`verification.json` records all twelve candidates: original dimensions, fully opaque pixels, zero changed pixels outside the actual GIMP layer masks, and exact RGBA agreement after reopening each layered XCF. The untouched neutral base files remain the integration source for other work. These checks establish export/mask integrity, not in-game presentation clearance.

- `opening-comparison.jpg` indexes the twelve complete candidates.
- `hand-review.jpg`, `mara-review.jpg`, `scholar-review.jpg`, `scholar-sleeves-review.jpg` and `prop-review.jpg` compare native local details and likeness references.
- Exact prompts, donor placements, masks and reproducible GIMP recipes: `../../prompts/batch6-opening/`.
