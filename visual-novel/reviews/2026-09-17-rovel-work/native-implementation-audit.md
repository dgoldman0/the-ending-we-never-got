# Bounded native implementation audit

This is code/geometry evidence, not art or complete-experience clearance.

## Defects resolved and verified

- Continue hover swallowed Space: parent added Space to dismiss_unfocused. Native assertions now advance with Space while Continue remains hovered and with Enter.
- Settings help collided with the decorative bottom border; nav crossed the top frame. Parent compacted right-column typography and moved the frame. Latest pixels show contained text and nav above the frame.
- Save timestamp extended outside its card. Parent now centers the complete native384x216 thumbnail in484x216. Latest filled slot [160,240,514,337] contains context [175,478,453,39] and date [175,524,123,34], leaving19px bottom padding.

## Verification

- All66 S001-S003 source pages were traversed in Standard and Larger:132 actual reading states at1280x720. Story text stayed within reading surfaces and above footer; required speaker/listener faces were ready.
- Bounded full native rerun after keyboard/settings fixes:3cases,32assertions passed.
- Final focused utility run after final save-thumbnail correction:1case,2assertions passed.
- Single Begin starts at source(1,9,0), exact first-night discovery return preserves(2,112,0), Threads/History/Settings return preserves source position, and native save context identifies Royal Temple / Summoning Chamber / Dawn.
- Six longest actual source pages were rendered separately with real fonts and geometry; narration ended at most y937 and dialogue y911, above footer y1018. This is text capacity evidence only for later scenes.
- Manually opened title, settings, save, discovery, and selected S001-S003 exchange composites. In opened Senn/Mara/priest/mother/Tessa composites, no obvious face-interior alpha holes or rectangular background remnants at playing size. This does not clear every portrait or full-resolution masks.

## Evidence

- measurements.jsonl (latest matching labels supersede earlier reruns)
- captures/final-save-context.png
- captures/final-title-settings.png
- captures/final-story-settings-larger.png
- capacity.json
- before-fixes-captures/ and before-fixes-measurements.jsonl

Existing geometry-summary.json predates the final save-card correction; its four save text-overflow records are superseded by the latest final-save-context measurement.

## Limits

No S004/S005 art or route traversal, browser review, all-portrait review, or full experience clearance. No placeholders were introduced. No product edits or commits were made during this isolated audit. Main independently reviewed its blue-healing seam fix.
