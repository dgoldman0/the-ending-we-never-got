# S005 local colour continuity correction

Applied after the three final generated exports and the pause-only skirt repair were frozen. These are **GIMP corrections**, not new image-generation calls.

Each final 1920 × 1080 PNG now has a same-stem XCF in `art/repaints/` with three real editable layers:
1. Original frozen final painting, including the existing pause skirt repair.
2. A duplicate with **Hue/Saturation: all hues −12°, lightness 0, saturation −5**, restricted to a refined coat-only layer mask. This shifts Iven's olive cloth to warm brown without changing his garment construction, embroidery or lighting values. Mask polygons follow each pose, with 2 px feathering and explicit forearm/background exclusions.
3. A duplicate with **Hue/Saturation: red hue range only, hue 0, lightness 0, saturation −12**, restricted to Tessa's face with an 8 px feather. This restrains the red cast without smoothing skin, repainting facial structure or removing freckles. Hair, robe, neck, lap hands and scene stay outside that local skin mask.

Exact mask coordinates and parameters are preserved in `local-colour-masks.json`. The XCF masks remain independently editable; this is not a flattened painting merely wrapped in XCF.

Reviewed the three complete final frames together and enlarged the coat edges, inner lapels, forearms and Tessa faces. The first mask pass left a narrow olive lapel and was refined; an initial stronger hue shift was reduced to the final −12° above to avoid a red-brown cast. The final coat reads warm brown in all three poses while cloth texture, seam relief and shadow structure remain. The face correction is intentionally restrained and does not alter facial geometry or painted detail.

Reopened all three XCFs and independently re-exported them; their visible-layer pixels match each final PNG exactly. Compared protected Tessa robe/lap/lower-body and medical-chest regions against the frozen sources: unchanged. The pause-only extra-skirt-sun removal remains in its original base. Iven's bottle is still held above the chest in packing, returned with hands at the chest in pause, and left in the open chest when he sits in together. No new garment, prop, pose or light source was introduced. Source review does not establish later in-game crop or grading clearance.
