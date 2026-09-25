# S027 localized horn and sword correction — 25 September 2026

Item 8 of the resumed asset request. This corrects the existing painting only. The earlier review’s claim that the sword binding and horn continuity were satisfactory is superseded by the user’s correction.

## Brief before rendering

The complete gate exchange and adjacent S026/S028 action were read (source lines 1130–1171): at the healer’s request to the governor, Serat stands on his stick after his left-thigh injury; the gate is still shut; Hest waits with the letter; the food remains aboard Lucan’s launch. Mara’s sheathed sword has already been submitted to a binding cord at line 1130. The original camera, composition, daylight, poses, bodies, expressions, every other figure and all props remain fixed.

Add only the individual horn designs from current portraits and written designs: Serat’s short upright tapered temple horns with slight backward lean; the healer’s short charcoal temple horns with subtly ridged bases and rounded tapered ends; the governor’s small stout dark-brown temple horns curved gently back with blunt tips. Preserve current faces and hair apart from tiny physically necessary horn-root joins. Bind Mara’s existing hilt to the scabbard throat with continuous cord that blocks withdrawal and touches no wrist. Existing decorative-looking loops below the guard do not sufficiently show this mechanism.

Inspected the whole 1920 × 1080 delivered image, native head and sword crops and current Serat/healer/governor portraits before consulting the earlier favorable review. Use built-in generation for local correction components, then masked GIMP layers over the unchanged original. Generated donor images do not become a replacement full scene. The completed local correction is recorded below.

## Delivered correction

The corrected PNG replaces the same scene path, `renpy/game/art/scenes/s027-river-camp-gate.png`, at 1920 × 1080. No runtime, grading, staging or shared character data changed.

Built-in image generation produced two donors in cache `01a0da4b-59e3-7210-81fa-077eace0a01c`: `exec-0380b9e1-5bda-4dc5-ba1d-b957ebf4d5fc.png` (horn crop, 1665 × 944) and `exec-486b1173-24eb-4b57-bae6-dd9300e7b03e.png` (binding crop, 1086 × 1448). Both are retained here as `horn-donor-2026-09-25.png` and `sword-binding-donor-2026-09-25.png`; exact prompts and the executed GIMP recipe are in `art/prompts/s027-river-camp-gate/2026-09-25-*`.

`camp-gate-horns-binding-master.xcf` has the unchanged original scene and five independently masked correction layers: Serat’s two horns; the healer’s pair; the governor’s near horn; his far horn; and Mara’s binding. GIMP scales only donor components into the original canvas. The generator misplaced the governor’s second horn toward the back of his head, so that portion is excluded: his far temple horn comes directly from the current `governor-listening.png` portrait, without mirroring. No generated face or body is substituted. The original scene is reproducible from the retained `camp-gate-badge-master.xcf` using its established crop and NoHalo resample; this was checked against the pre-correction PNG before promotion.

Whole export and enlarged native-resolution horn/root and sword-contact views were inspected. The horn roots sit in existing scalp/hair, remain distinct by character and respect near/far occlusion. The cord has a closed grip turn, two continuous taut runs across the guard, scabbard-throat turns and a securing knot with short ends. It restrains withdrawal without touching Mara’s wrist. The original faces, poses, clothing, light, camera and other figures remain unchanged outside the local masks. The independent `correction_s004_exposure` reviewer inspected the actual complete candidate first, then the contacts, original scene and three current portraits, and found no blocking horn join, cord-mechanism, anatomy, seam or visible drift defect before same-path promotion.

The reopened corrected XCF reproduces the delivered RGBA pixels exactly. Only 2,941 of 2,073,600 pixels differ from the pre-correction export, all within the three local horn areas and sword binding. This verifies preservation boundaries, not overall game quality. Runtime grading and connected play remain outside this correction.

Pre-correction PNG SHA-256: `e06b4f3a215487fccae38eb90b2727a7888a52a169aac62b51b3db60f243ea04`.
Delivered PNG SHA-256: `ddae0e3e01f2234ea4413d9d36369d9265e3e58820723fd4fa0082da0564e6cd`.
