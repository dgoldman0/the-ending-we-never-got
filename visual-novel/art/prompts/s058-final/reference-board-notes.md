# S058 shared casting references

Prepared and visually inspected on 26 September 2026 before Chapter 10 release. These are reference collages, not new character designs or delivered story paintings.

`cast-reference-board.jpg` contains only the six people visible in the planned market base: Tessa, Elin, Orren, Hest and the two apprentices. It combines the current postwar/later portraits, the first apprentice portrait, a bounded second-apprentice crop from `s029-barge.png`, the user-approved full postwar wrap and a bounded S008 Elin clothing crop. The old scenes were inspected for continuity but no whole scene, Iven or Mara face appears in the board. Portrait expressions and incidental source poses are not instructions for the final action.

`children-reference-panel.jpg` is separate for the final interior. Ada's current earlier portrait establishes her individual face and plaits; Renn's actual S011 crop establishes his loose curls, medium-brown skin and Orren-like long chin. Ada must become roughly 11–12 and Renn roughly 9 in the ending, with older facial proportions, longer limbs and changed clothing fit. The earlier pictures are not endpoint age references. Both apprentices must likewise be visibly older while remaining distinct individuals.

Root and final-scene producer coordinated spring clothing before generation: Orren's waistcoat is neutral warm brown, not northern green; Elin wears repaired intact pale sleeves, her ocher jacket and dark teal skirt as in S008 personal home clothes, with no field cloak. Tessa wears the approved one-piece dusty-mulberry wrap with two wooden toggles at anatomical LEFT, a pale soft RIGHT hand/wrist brace leaving fingers exposed, and low oxblood shoes. Her LEFT hand performs healthy actions. Do not add a Saint badge, undershirt, second collar, shawl, belt or campaign weapon.

The full source used is `source.fountain` lines 2175–2215. The final image selects 2213, inside the bakery, after the drawings are closed and the letter signed. The main board supports the separate earlier market moment too; the children panel must not be used to accidentally add Ada and Renn to that exterior composition.

`build-reference-boards.py` reproduces both boards with Pillow solely as labeled inspection/reference collages. It does not edit production scene assets. Source crop coordinates are retained in the script.

## Actual scene inputs and components

Chapter 10 was released after Chapter 09 commit `4ff6912`. The final interior waited for the first actual market source before generation. `actual-market-state-reference.jpg` contains only the three limited shared-clothing/cast crops of the retained `s058-bellweir-market-spring/market-source.png`; no fountain, books, wrong shoes or cane grip were used as action references. The initial interior generation used the main-six board, separate children panel, and this market crop board in that order. `01-offered-chair.txt` is the exact built-in generation prompt.

The generated interior source was 1672×941. `02-local-state-and-guide.scm` keeps the original painting and adds independent warm-brown waistcoat, clean reply-paper and two-toggle correction layers. Its framing guide uniformly scales the complete original composition to1190×670 and places it at(350,80) on1920×1080. `03-environment-extension.txt` used that guide as the sole image input. The guide was first generated before the final stronger warm-brown/two-toggle corrections, then regenerated from the exact final local layers for reproducibility; those two later local fixes are copied above the donor in the final master.

`05-two-toggle-detail.txt` used the inspection-only crop `third-toggle-input-reference.png` (original native box340,450–440,575, displayed400×500). The generated component repairs only the lowest unwanted third fastening; the upper two wooden bars and original torso/pose remain. The input crop/boards are reference preparation, not production bitmap edits. All final production compositing, masks, color correction, resizing and PNG export were performed in GIMP through the saved Script-Fu recipes.

The original pre-toggle/pre-final-warmth room-extension guide is restored exactly by `03-original-extension-input.scm` and retained as `environment-extension-input-guide.png`. The image actually displayed to the built-in tool was the1440px inspection version, `environment-extension-input-reference.jpg` (JPEG quality93). The final delivery master uses the later corrected local layers above the room donor, so restoring this historical input does not change the delivered painting.
