# S004 neutral exposure recovery — 25 September 2026

Request item 7 only: recover the hall, banners and pale clothing at neutral exposure while retaining the accepted left soldier's supported sling and free palm against his chest. The screenplay beat is the wounded audience applauding during Senn's introduction, before Tessa catches his sleeve; Olan and the same three unnamed soldiers remain in the same places and poses. Senn and Tessa are off camera. No camera, anatomy, costume, action or spatial changes are requested.

The delivered exposure repair can use retained source pixels instead of generating another painting. `renpy/game/art/base/rovel/cg/ceremony-applause.png` retains the neutral hall and people, including the earlier Olan hand repair; it predates only the corrected sling gesture. The old GIMP master `sling-repair.xcf` retains that exact accepted arm/sling component and its local mask. Recover the neutral source as the background and match only that local component to its exposure. References for neutral exposure: `renpy/game/art/rovel/cg/ceremony-refusal.png` and `ceremony-dais.png`.

Candidate and final inspection results will be appended after viewing the actual GIMP export.

## Assembly and review

No new generation was needed. The existing neutral base recovers actual hall, banner, skin and cloth pixels; lowering the blown-out delivery alone could not recover that detail. GIMP loads the existing sling master, hides its old background, inserts the retained neutral source at native size, and preserves the exact accepted sling layer/mask. Its local value curve is `(0,0), (32,18), (64,38), (96,56), (128,74), (160,94), (192,114), (224,140), (240,164), (248,190), (255,245)`, with master saturation reduced by 20 to avoid amplified pink in the sling. The exact operation is in `recover-exposure.scm`; the earlier generation prompt remains `../../prompts/rovel/applause-supported-sling.txt`.

The four-layer `exposure-recovery.xcf` retains the neutral source, the accepted masked sling with its matched exposure, the hidden original sling before tone matching, and the hidden overexposed background. Layer masks and all source content remain editable; it is not a flattened PNG wrapped in XCF.

Viewed the final GIMP export whole at 1200 px and native crops of the left soldier's arms, Olan's face/hand/shirt, and the right banner/marble. The hall now has beige marble veining and discernible architectural edges, the blue banners retain their hems, and shirt/sling folds remain visible. Window openings stay bright. The sling still supports the left forearm and the free right palm still meets his chest, without changing the accepted geometry or introducing an old-arm remnant.

Pixel verification at 1672×941: every RGBA pixel outside `(14,295)–(408,515)` is identical to the neutral source, including all of Olan, the other two men and the architecture. No whole-image resampling occurred. Reopening the XCF and exporting its visible layers reproduces the candidate RGBA pixels exactly.

Using explicit RGB thresholds rather than the request's approximate count: the prior delivery has 7.3284% exact-white pixels and 24.5429% pixels with all RGB channels at least 250; the recovery has 0% and 0.4476%, respectively. The supplied refusal and dais references have 1.9194% and 0.9811% near-white pixels. These measurements support exposure recovery but do not establish the game's visual quality.

Candidate PNG SHA-256: `590a6c5865c046282b0a8723fce39438fe2642197c1c79b1a63b6a1e23d640c1`.

Root inspected the actual candidate whole against the neutral refusal reference and the native sling crop: restored marble/banner/cloth detail; clean cuffs and palm-to-chest contact; contained injured forearm. After that review and the exact master check, the candidate replaced `art/repaints/ceremony-applause.png`. Runtime installation and grading remain outside this correction.
