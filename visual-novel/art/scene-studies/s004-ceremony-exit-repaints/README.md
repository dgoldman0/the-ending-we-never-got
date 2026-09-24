# S004 — refused chair, intervention and yielding the steps

Batch 5 Part D repaint briefs. The user selected the fine-gold vestments and authorized continuation on 24 September. These three sources will be saved in `art/repaints/`; the layered runtime scenes remain untouched. Generation released after the Part C commit `2a19f9a`; no runtime scene files are changed.

## Shared scene and invariants

Read the complete audience-hall interaction in `screenplay/original-timeline/source.fountain`, lines 174–215, plus the current paintings, cast designs, audience-hall location and prop continuity. Senn has placed the badge and white mantle on Tessa and publicly announced a departure she never agreed to. She challenges him instead of accepting the ceremonial chair. Orra intervenes; Iven is below the dais carrying **Tessa's bag**, then starts up when Orra signals him. The bag is not newly redefined as his medical bag.

The source paintings govern their camera side, established cast positions, individual faces, chair, stairs, flowers, banners, audience and window direction. Their rejected blue layered Tessa clothing is only an edit target. Tessa's selected storm-infirmary likeness and the accepted fine-gold costume key govern the replacement: nineteen, healthy hands, ordinary brown eyes, natural brows/freckles and brown chestnut ponytail. One light flowing white full-length robe, its shallow round neckline and fine gold ornament, with the lightweight removable white mantle fastened across her upper chest by the twelve-ray brass sun. No blue underlayer, bulky roll collar, stiff ray fins or crown. The mantle falls continuously from shoulders and clasp, with plausible folds around the existing arm action.

Senn remains the sandy-gray-haired, short-bearded man in cream temple robes. Orra remains the sturdy dark-skinned woman with short graying hair and blue military coat, about fifty. Iven remains the young medium-brown-skinned man with short unruly black curls, long limbs and brown practical coat/boots. The latest instruction reserves green clothing for the northern side; older written olive wording does not authorize a green human coat. Preserve the source's muted warm-brown appearance and its construction.

Keep the same bright-day window direction and architectural materials, but deliver neutral exposure with readable faces and cloth; runtime grading will recreate the uncomfortable light. No invented magic, new named people, added symbols, dialogue or signage. Output each painting at 2560×1440 if available, otherwise at least 1920×1080, 16:9. Full heads and approximately 70px top margin in 1080-equivalent coordinates. Important faces/hands and the physical step relations remain above the lower fifth, with no decisive action in the lower-left portrait area.

## `ceremony-refused-chair.png`

**Exact beat:** after Senn tells her to sit, Tessa steps around the ceremonial chair, still holding his sleeve, and asks, “Look at me. When did I agree to go?” Senn's deferral and Orra's entrance follow.

**Visible action and route:** preserve Senn on the left, the empty ornate chair between them in the lower middle, Tessa on its right, both on the same dais. Her extended hand holds his sleeve at a reachable point; the sleeve must run continuously to Senn's arm and not become the mantle. Her body stays outside the chair's footprint, with room to step around it. The supporting audience remains subordinate at the edge; do not add Iven or Orra prominently to this closer beat.

**Change:** replace Tessa's obsolete layered blue costume with the chosen light white-and-gold robe and mantle, preserving her stance, refusal, hand contact, camera relationship and the visible dais. Neutralize overexposure while retaining window direction. Allow only enough camera breathing room to keep full heads and robe silhouette legible.

## `ceremony-intervention.png`

**Exact beat:** Orra has stepped onto the dais and asks whether Tessa is ready to travel; Iven, waiting below with the bag, answers that he has not cleared her for anything. Senn and Tessa remain beside the unoccupied chair.

**Visible action and route:** Iven stands on the lower hall floor, screen left, facing up toward Orra. Orra stands on the dais left of the chair. Senn and Tessa stand together to its right, with the existing sleeve/arm relationship retained. Preserve a continuous set of step risers between Iven's floor and Orra's feet; Orra is not floating and Iven is not suddenly on the dais.

**Changes:** chosen vestments for Tessa; pull the camera back enough that Iven's complete boots, their floor contact and the step edge lie above y820 in 1080-equivalent coordinates (above 1093 in 1440). Keep his whole body proportionate rather than shortening the legs. The lower fifth becomes quiet floor. Preserve relative locations, viewing side, empty chair, bag hanging from Iven's existing grip, audience and architecture. Retain about 70px above the highest head in 1080-equivalent coordinates. The old scene's glare is not baked into the new source.

## `ceremony-yield.png`

**Exact beat:** Orra signals Iven up and Senn has to yield the steps. Iven begins to climb from the lower floor while Senn looks toward the audience, leaving the approach open. This follows the intervention painting; it is not another disconnected arrangement.

**Visible action and route:** preserve Iven at screen left, bag in his existing hand, one boot planted on the hall floor and the other reaching a distinct first step. Orra stands above him and extends an open inviting hand. The chair stays empty between Orra and Senn; Senn and Tessa remain to its right. Keep the stairs wide enough for Iven's next step and the robe/coat hems clear of the foot contacts. Orra does not grab him; his raised foot does not float over a flat stage.

**Changes:** chosen vestments for Tessa; pull back consistently with intervention so both Iven boots and all explanatory step edges are above y820 of 1080, leaving quiet lower floor. Preserve the source camera side, ordering and gestures, with complete heads, readable bag/hand contact and distinct level change. Tessa looks unsettled rather than grateful for an unwanted public ceremony.

## Required output review

Inspect each full export first, then native faces, Tessa's neckline/clasp/fabric, hands and sleeve or bag contacts. For intervention and yield, inspect both Iven boots, leg proportions and the unbroken stair planes, and check them under a lower-fifth reading shade. Compare all three costumes and cast faces to the same keys and the neighboring ceremony repaints. A generated image is not yet a runtime or user approval. Record actual edits and any remaining defects after generation. Exact prompts belong in `art/prompts/s004-ceremony-exit-repaints/`.

## Delivered refused-chair and yield reviews

`ceremony-refused-chair.png`: the first costume edit left Senn too close to the upper edge. A focused framing edit added room above the whole cast while retaining the reachable grip on his connected sleeve, empty chair and the two standing positions. Opened the final whole composition, then native Senn/Tessa faces, sleeve grip and Tessa's free hand. Tessa has the selected fine-gold shallow neckline, centered mantle clasp and thin white drape; the obsolete blue ensemble is gone.

`ceremony-yield.png`: a combined costume/framing instruction produced a good costume change but ignored the precomposed pullback. Kept that painting, used GIMP to fit it uniformly to 1104×621 at 284,30 on the native 1672×941 transparent canvas, and used a separate built-in outpainting call for the empty surrounding hall/floor. The final lowest boot lies near y718 at 1080 delivery, the raised boot near y623. Both clear the y748 top of the actual portrait window (x116–516,y748–1004), as well as y820. Inspected the image beneath a guide for both occupied UI regions. The lower boot has hall-floor contact; the raised sole meets a distinct stair tread; Orra's two feet remain on the higher dais and her hand invites Iven up. Native face, bag grip and hand crops were inspected. This is source-composition evidence, not an in-game clearance.

**Native-resolution limitation:** built-in calls returned 1672×941 despite the 2560×1440 request. Both selected PNGs were minimally resampled in GIMP with NoHalo interpolation to the required 1920×1080. This adds no native painted detail. Exact original and follow-up prompts are in `art/prompts/s004-ceremony-exit-repaints/`.

**Intervention:** the first wider outpaint and a 20px upward translation cleared y820 but still overlapped the actual lower-left portrait window. Root took ownership of the further framing correction; its final review and master/export verification are to be recorded by root. Do not treat the earlier y820-only check as full interface clearance.

### Final intervention framing

The root correction puts the complete Iven boot contacts around y700 on the1920×1080 delivery, above both the y820 reading threshold and the y748 portrait-window boundary. It uniformly reduces the existing scene, fills only newly exposed hall/floor space, and retains the original cast/cloth on a masked upper GIMP layer. A rejected outpaint truncated the foreground spectator robes; the selected extension carries their opaque cloth beyond the bottom edge. The source-sized inset and extended background are separately editable in ceremony-intervention-reframe.xcf. Final delivery was inspected with both exclusion guides; runtime assembly remains with Claude.
