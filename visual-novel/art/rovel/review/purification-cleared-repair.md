# Purification-cleared jaw/neck fragment — local GIMP repair

17 September 2026. Scoped correction; independent main-thread review and the connected scene gate remain pending.

Inspected both `opening-sequence` purification-cleared masters, the first-purification master, and both raw images. The translucent second jaw/neck is already present in `raw/purification-cleared.png`. The coherent `raw/first-purification.png` aligns at the same coordinates and supplies the repair without moving or reshaping the head.

The [new master](../masters/purification-cleared-repair.xcf) has separate Intense and Softened groups. Each retains the full pre-repair scene and an independently graded first-purification source layer with an editable local mask. The raw donor remains hidden, ungraded and untransformed. The mask repairs only the lower jaw/neck and its immediate blend boundary; it does not import the earlier treatment state or Tessa's earlier gaze. The saved default is Intense. Original masters and raw files remain untouched.

Both final whole 1672×941 exports and native 350×390 face/neck crops were opened. The jaw now continues into one coherent neck, without the translucent duplicate. The mouth, gaze, hair and expression remain as before; the cleared arm and missing fingers remain in their existing state. Intense and Softened retain their separate original exposure recipes. Reopening the XCF and exporting each lighting group reproduces the corresponding delivered PNG pixels exactly.

Read-only comparisons confine changes to x=1263–1461, y=407–546. The mask intentionally changes the defective lower-jaw/neck pixels and their boundary. Separate checks of Olan's eyes/brows, nose, mouth, hair/forehead and ear find zero changed pixels. Tessa, Iven, the older healer and priest, the cleared right arm, supporting hands, white light and Olan's rail hand also have zero changed pixels. These checks do not clear the scene's blocking, transition or UI gates.

Delivered runtime files are `renpy/game/art/opening/cg/purification-cleared.png` and its paired `art/softened/opening/cg/purification-cleared.png`. Script, original-export backups and final native crops are in `/tmp/source-gate-purification-repair/`. No last-patch asset, other runtime art, code, original source/master or lighting metadata was changed by this correction.
