# S043 Lucan head correction — 25 September 2026

Request item 10 corrects Lucan at the chart: the delivered scene had lighter, wavier hair, a different face, and no readable horns. The current `portraits/lucan-later-speaking.png` and Lucan's written design govern this correction; earlier positive scene-review prose does not establish his identity.

## Source and bounded purpose

Read the complete S043 river-provinces interaction and the adjoining mill-town aftermath and S044 extraction in `screenplay/original-timeline/source.fountain`. This is the winter wharf conversation before the rescue: Lucan and Serat have been repairing the hired fishing boat, the boatman reports Marren's transfer, and Lucan studies the chart. Lucan has healthy hands and no extraction wound yet. The chart, worktable, coat, leaning pose, all other people, boat, repair, low arch and light are retained.

The built-in image-generation tool painted a head component from a GIMP crop of the final scene, with the current later portrait as the sole identity reference. It restores near-black hair tied low for boat work, a long face with the reference brow, nose and broad mouth, and smooth dark backward horns close to the skull. The near horn is fully visible and the farther horn is partly occluded by the crown. The serious rightward attention and existing head angle are retained.

- Exact prompt: `art/prompts/s043-river-provinces/2026-09-25-lucan-head-correction.txt`.
- Editable mask/assembly recipe: `art/prompts/s043-river-provinces/2026-09-25-lucan-head-mask.scm`.
- Original generated component: `2026-09-25-lucan-head-component.png` (1254×1254).
- New layered master: `2026-09-25-lucan-head-correction-master.xcf` (1920×1080).
- Corrected final: `renpy/game/art/scenes/s043-river-provinces.png`, copied from the inspected candidate after root review.

The master retains all original scene layers and adds a separately named, feather-masked head layer. The component was scaled to the exact 320×320 source-crop size and placed at `(220, 100)`; the mask exposes only head, hair, horns and the upper-neck transition. No global grade or image resampling was applied. The source component is retained at generation resolution so the mask can be revised without regenerating the scene.

## Inspection and evidence

The producing agent compared the actual final scene and portrait, then inspected the corrected full composition and enlarged head comparison. The face now follows the reference's brow, straight nose and fuller mouth; horns read at full-scene size. No collar seam, doubled hair contour or bright mask fringe was found. This is a correction review, not approval of the connected game experience.

The old XCF was reopened before correction and its visible render exactly matched the delivered PNG. The corrected XCF was reopened after saving and its visible render exactly matched the candidate. Pixel differences from the old scene are limited to `[243, 146, 472, 365)`; every pixel outside that head/upper-neck rectangle is unchanged. These technical checks establish bounded editing and reproducibility, not likeness by themselves.

Root independently inspected the actual whole scene and native head directly against the current later portrait and passed the correction: face, brow, nose, mouth, tied near-black hair and backward horn agree; the neck joins the original coat and body naturally. The requested final scene PNG was then replaced with the inspected candidate. This bounded review is not user approval of the whole game. No crop/grade tools, staging, runtime code, shared canon or request ledger were changed.

## Provenance

Built-in generation source: `/home/kir/.codex/generated_images/01a0da4b-a0d3-7aa0-a5d9-0823b37fdafc/exec-0be5d143-1dc2-464e-9984-02e732d86267.png`.

SHA-256:

| File | Hash |
| --- | --- |
| Scene before correction | `5624bc817ecee8dbd2bc001e197f9a3f8329e59cca65691f5e32cc1fef35d9f7` |
| Later speaking portrait | `b35d1abba6dc079543155583ff3b89f7fe47ce4b3ab3b0b2e8ae6b2483dc5681` |
| Saved generated head component | `e54a60f92d4438b6c5ed53514350f6af60a500de6cb117f35d0bf5c04b58ed4a` |
| Corrected final PNG | `29487c086aa25c65b3ceda3c294bedf5f81f181e78cc75620bd603a048f30379` |
