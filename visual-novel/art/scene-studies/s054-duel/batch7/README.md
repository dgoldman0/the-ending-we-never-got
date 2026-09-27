# S054 duel — Batch 7, item 47

**Selected delivery:** [independent/delivery.png](independent/delivery.png), with [layered master](independent/delivery-master.xcf), [exact reopened export](independent/delivery-reopened.png), [production notes](independent/README.md) and [verification](independent/verification.json). Root and independent review cleared the actual whole/native deterministic composition before proportional export and source promotion. The historical files named `candidate.png`, `native-candidate.png`, `delivery-master.xcf` and `native-master.xcf` in this parent folder remain rejected diagnostics; only the selected files under `independent/` are the new delivery.

Brief before generation. Source lines 2058–2076: before the injury, Tessa advances with a sword in her healthy RIGHT gloved hand and white light in her bare LEFT. Valcair drives a rigid spear along the OUTSIDE of her sanctuary into a pillar; she cuts around the curve at his elbow, where BLACK ward light turns the blade. He then forces her toward the dais. Keep Tessa screen-left and Valcair screen-right, consistent with the surrounding S054 paintings. Both hands remain healthy. No arm/head intersections, no touching or merged feet.

Use the current throne-hall painting for architecture, neutral dawn light, three low dais risers, plain throne, actual faces, plain campaign coat and armor. Source facts and written character designs govern identity: Tessa about 23/165cm, warm light-brown skin/chestnut low ponytail/freckles; Valcair early 50s/193cm, medium-brown skin/black hair streaked silver/heavy backward ridged horns as a pair. Short sword glove and empty LEFT hip sheath; no elaborate cuffs or additional layers. Black ward visibly occupies armor joints; no tiny violet sparkle substitute.

The Batch 6 duel is archived as before.png for diagnosis, not supplied as the new action reference. Rebuild interacting arm/weapon/ward geometry together. A transparent dome must enclose Tessa from above her head to a visible floor perimeter, while its near edge admits her sword hand for the outward cut. The spear stays outside her silhouette and dome volume; its tip terminates in solid column stone with an identifiable impact. Neutral wrists, full wraps around handles, ordinary shoulder–elbow–wrist chains and one straight rigid shaft are required. Hands, impact, blade/elbow contact and faces stay above the lower reading shade.

No current source replacement until whole/native inspection, comparison to portraits and neighboring scenes, independent review, and exact reopened GIMP export. This is a candidate study, not a visual approval.

Original source SHA256: 158455f8068061d01406619e3334ee4793dee48bde37960c60f31f1c48c089a2

First free-form action draft rejected: shaft divided into disconnected segments behind Valcair, contact at wrist, questionable laterality. It is failure evidence only. Returning to fresh physically connected blocking; do not use the failed painting as a pose reference.

## User rejection and researched rebuild, 27 September

The user rejected the pose retained in 05-shell-donor and the assembled candidate. Those files are not approved or delivered. Earlier review established connected anatomy but failed to evaluate weapon mechanics: both elbows flare, wrists droop, and the spear reads as a bar across the waist. The thin blade and its tip contact show a thrust instead of the written cut. Preserving the hands during local revisions preserved the error. Rebuild both interacting poses rather than retain that constraint.

Research: Jennifer Landels, [Attacks of the Spear](https://www.academieduello.com/blog/attacks-of-the-spear/), explicitly permits palms-down thrusts; palm direction alone is not proof of failure. Jakub Dobi, [Interpretation of Fiore dei Liberi’s Spear Plays](https://bop.unibe.ch/apd/article/download/7703/10659/30396), pp.134–136, photographed by Sándor Dobi, illustrates a staggered stance, forward arm along the shaft and a naturally bent rear arm by the torso. The inspection/reference crop is mirrored only to match screen direction. It is posture evidence, never a character or costume reference.

Next candidate uses those arm/body relationships and a proportionate one-handed sword with edge contact near its outer third at Valcair’s forward elbow. Tessa's healthy RIGHT hand grips; bare LEFT maintains the grounded dome. The spear remains outside the dome into the pillar. Preserve faces, costumes and room from their actual references, not the rejected action pose.

## Component attempts and current status

- 07 improved body stance but hid the forward grip and still aimed a sword tip at a fist; rejected.
- 08 replaced the forward hand by a folded-back arm and malformed joint; rejected as a complete scene. Tessa’s intact, correctly handed figure is used only as a separated component.
- 09-spearman-foundation is a separate single-actor pose from the photographed reference. Parent and independent reviewer inspected the actual forearm/wrist alignment, fingers, staggered legs and floor contacts. It is a useful component, not a complete scene.
- 10 silently replaced that verified arm during addition of Tessa; rejected.
- 11-composition-guide is a GIMP assembly of the verified spear actor, Tessa's source component and a separately oriented rigid blade. The initial rough Tessa mask has clipped boot/coat edges; `tessa-component.png` and its XCF now provide a precisely traced replacement, including full soles and coat hem. The complete guide still lacks the required spear/pillar/shelter geometry; it is not deliverable.
- 11-matted-composition-guide is a failed automatic extraction experiment: it introduced transparent body regions and must not be used.
- 12 preserves more useful hands and an edge-led cut, but leaves the shaft intersecting the dome beside Tessa's head. It is rejected.

An independently composed alternative was made in `independent/` and rejected. A finished scene must be selected by inspecting the actual full interaction, not by inheriting the individual component checks. None of those rejected attempts was promoted.

## Deterministic assembly — selected after review

The independently rendered alternative also failed the forward elbow and sphere depth. It is labeled rejected inside `independent/`. The selected assembly retains the independently checked 09 spear actor and exact Tessa component. Both reviewers converged on a nearer middle-ground pillar: shorten only the unheld forward spear length so the point stops before Tessa, leaving both arms and grips unchanged. The sword passes in front of that pillar and contacts the true forward elbow with its outer cutting edge; its tip continues past contact. The spear is deliberately gripped close to the head after the forward thrust. Its length change must be reviewed as a prop change, not concealed as a mask-only edit.

The old files named `candidate.png`, `native-candidate.png`, `delivery-master.xcf` and `native-master.xcf` are the rejected 05-derived assembly, retained for diagnosis. Their names do not confer delivery status.

Root inspected `independent/deterministic-guide.png` and cleared its geometric direction for component assembly. The subsequent generation produced ONLY an empty hall plate with the middle-ground column at the guide position; figure pixels, hands, weapon mechanics and effects are separately controlled in GIMP. This guide clearance does not establish final scene quality.

The completed native assembly was reviewed by root and an independent reviewer at SHA256 `df48f5df6e74d8cebe8dfa38e6d4fd8e4cca3e7eb5504d4579b1a707e4029daf`. They checked the complete arm chains and grips, straight hilt/blade axis, pillar impact before Tessa’s silhouette, floor-grounded shelter, blade-edge contact at the true elbow with the tip beyond, visible black ward contact, faces/horns/costumes, clean masks and feet. The final GIMP delivery preserves those layers and uses a uniform scale to the source canvas. This records inspection of the source asset; connected runtime/presentation acceptance remains separate.

## Local fix after delivery (Claude, 27 September 2026)

The delivered duel hung three blue banners bearing the temple's gold twelve-ray sun in Valcair's throne hall: the human side's emblem in the northern capital. None of the other S054 paintings shows banners, so they keep their place and take the northern colours instead of being painted out of the architecture. `tools/local-repairs.py` (the `banner` step in its BATCH7 table) fills each sun from the plain field around it, keeps the gold trim, turns the blue field the northern green of the S011 flag in its own light and folds, and draws the white eight-point star with its vertical split where the sun was. Each banner's outline is a Segment Anything mask (`art/local-repairs/masks/banner-*--s054-duel.png`); the layered master is `art/local-repairs/batch7-check/s054-duel.xcf`. Only banner pixels change. The side banners hang at a slant, so their stars are narrow and their splits thinner (a first version's split was as wide as the vertical points, which then read as two slivers; the batch 7 check caught it).
