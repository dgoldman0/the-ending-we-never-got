# Batch 8: citadel ward, duel ward-light, lever stone

Delivered 29 September 2026, limited to request items 63, 65 and 66. Current runtime source paintings are the starting point, with Claude's Batch 7 corrections retained.

## Scene briefs

S052 (screenplay 2027–2047): Tessa works on the black ward from behind Olan's shield; Elin crouches beside him and a runner arrives from the stair. The hall is visible through the thinning barrier across the full open bronze doorway. The tower recharges it; Tessa removes her left glove and presses her palm to the frame before squeezing through. These two existing compositions retain those distinct states, the cast, camera, weather and lighting. Repair ward coverage and paste remnants locally. The sword is an optional local correction only if its left-hip suspension can be established without disturbing the figures.

S054 duel (2072): Valcair drives the spear along the outside of Tessa's shelter into the pillar, and she cuts around its curve at his elbow. Black ward-light wells from articulated armour joints, strongest where it repels the sword at the extended elbow. Preserve existing spear, shelter, blade, bodies, horn pairs, and northern green banners. Optional changes are secondary to preserving that established mechanics.

S054 lever (2100–2102): Valcair has fallen at the lowest step and is reaching toward his spear on the dais. Tessa, right hand wounded and held to her chest, leans her weight through her left hand on the release behind the throne. The entrance ward fades. Resurface the throne, raised dais block and lever pedestal as carved stone; keep the lever hardware, geometry, steps, weapons, both figures and Tessa's corrected chestnut hair. The previous throne-hall painting supplies material and ward-light references only.

## Method

Built-in image generation makes local donor components. GIMP masks, compositing and native review crops constrain the final correction. Each master retains the untouched current source plus separately masked donor layers. No grading, interface or staging changes.

## Final review and delivery

- **S052, thinning ward:** black currents now extend across the entire opening while columns and throne remain visible through them. The luminous threshold line reaches the actual right stone jamb. Local masks remove the pilaster notch, sleeve/hair paste seam and pale old floor rim behind the runner's rear boot. The final floor repair uses a narrow stone-texture sample; the initial broader floor patches were discarded after native inspection exposed an unwanted bright shard. The cast and gloved-hand state are retained.
- **S052, closed ward:** the same narrow seam repair is retained without transferring the earlier gloved hand. Original black ward texture closes the right corner, with a thin luminous threshold edge seating the barrier against the stone. The old hard cut and uncovered strip of floor are gone.
- **S054, duel:** black ward-light wells from the armour joints, with the strongest local coil at the extended elbow where the blade is repelled. The original spear and blade geometry is protected over the local donor, and the original face, hair and horns are retained. The whole Tessa/shelter/pillar side and Claude's green banners remain unchanged.
- **S054, lever:** the throne, dais block faces and lever pedestal now have irregular grey mineral texture, shallow cracks and worn stone edges. The regular stud rows and pedestal diamond are gone. The metal lever mechanism, cast, weapons, steps and Tessa's chestnut hair remain.

Every final full composition and native repair crop was inspected. A second agent reviewed all four candidates and found the thinning ward still ending short of the right jamb; the final narrow extension removed that gap, and the reviewer rechecked the corner at native resolution. This is source-art inspection, not a graded or in-game review.

Each `repair-master.xcf` opens with 4–5 genuinely editable source, donor and repair layers, with individual masks. Flattening freshly reopened masters reproduces all four delivered PNGs exactly; see [verification.json](verification.json). The records include source hashes, final hashes and measured unchanged face/hand/colour-fix regions. The [reproduction script](../../../tools/batch8-citadel-ward-lever.py) accepts scene names to rebuild a subset. [Exact prompts and input provenance](../../prompts/batch8-citadel-ward-lever/) are retained.

The four files replace their same-named sources in `renpy/game/art/scenes/`. No light grading, interface, staging or gameplay code was changed. Claude's crop/grade/play pass remains next. Optional S052 sword relocation and the duel's banners, pillar/floor-ring relation and spear-tip clearance were left unchanged to avoid disturbing approved blocking.

## Local fix after delivery (Claude, 30 September 2026)

`s052-entrance-ward.png`: the ward's lower right corner was a flat black block whose hard diagonal top cut across the open door leaf, which ended in mid-air above the threshold. The ward's own streaks from beside it fill the corner and come in gradually over the leaf's lower end, so the leaf fades into the ward. BATCH8 table of `tools/local-repairs.py`; master `art/local-repairs/batch8-check/s052-entrance-ward.xcf`.
