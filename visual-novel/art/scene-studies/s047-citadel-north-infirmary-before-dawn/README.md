# S047 — North infirmary receiving room, before dawn

Production resumed after correction checkpoint `50e4d86`, 25 September 2026. This uses the reviewed S045 ward; no runtime changes.

## Exact beat

Source 1843–1878, selected **1845**: Lucan has returned from Valcair and finds Serat plus FOUR captains waiting. Through the open door orderlies move beds away from the windows. This is before the gray-braided captain and another officer leave, before Serat brings the sergeant, and before the plan/letters. Exactly SIX foreground officers: Lucan, Serat, departing gray-braided captain, other departing officer, shorter broad-horned cropped-beard remaining captain, long-faced swept-horned high-tied-hair remaining captain. Northern orderlies beyond the doorway are subordinate.

Lucan keeps his own damp, worn green coat and dressed LEFT forearm, sleeve cut away; his father's clean coat stayed behind. All faces and horn designs match current portraits or the written minor-cast designs. No Tessa, Mara, Marren confession, magic effect, daylight attack, already-laid map, letter-writing or duplicate Lucan.

## Shared room and proposed view

Use S045's actual reviewed main ward and wide west stone arch. Camera in the west receiving room looks east through that arch into the ward. Six adults have distinct footprints in a generous approximately 7×6 m receiving room, with a clear passage beside them. Lucan has just entered at picture left; Serat is opposite him; the four captains form a loose incomplete arc, not a posed straight lineup. The departing gray-braided captain addresses Lucan while the two remaining captains exchange a concerned look. Through the arch, two northern orderlies roll/carry one supported bed from the south windows (picture right beyond the door) toward the inner aisle. Keep bed legs, bearing points and people separated; no bed clipping through the doorway.

Match actual S045 warm-gray stone arch, celadon lower limewash, restrained botanical jamb detail, plain timber beds, linen shelf and gray floor. Court/window positions remain fixed. Predawn blue outside with modest practical lamps, readable neutral source exposure. The river exit stays separate from the west attack front. Later S051 uses the covered court and laundry flank, not the assault stair.

16:9, request 2560×1440, minimum delivery 1920×1080 with actual native size disclosed. Keep key faces, dressed arm, hands and movement contacts above the reading shade and ≥70 px equivalent headroom. No generation before S045 review locks the actual set.

## Review

Complete: actual S045 set and whole/native S047 reference comparisons, source checks, peer review and root review are recorded below. This does not clear runtime placement or grading.

## Actual production and final candidate

Built-in generation established six distinct officers and the reverse ward view; root inspected the actual first whole image and confirmed the cast/set. The initial image incorrectly bandaged Lucan's healthy RIGHT wrist. An isolated local sleeve generation replaces only that area with the worn green sleeve and narrow cream cuff, retaining his existing bare hand and every other original scene pixel. His LEFT dressing remains unchanged. GIMP stores that bounded operation in `sleeve-master.xcf`; it is not a whole-figure repaint.

The first composition lacked adequate horn headroom and lower supports. A protected uniform reframe supplied wider room margins and completed natural legs/boots. A second thin-margin extension completed the captain's clipped near toe. GIMP restored the original six-officer acting and bed-handling area from the sleeve-corrected source, with the final protection mask excluding an old cropped-table remnant revealed by the wider view. The final bodies have separate floor contacts and a usable aisle. All six officers and both distant orderlies have visible individual horn silhouettes; the orderlies' small horns were checked enlarged from actual native pixels.

Sources are retained here. Built-in cache session `01a0da4b-1412-7500-8638-0d6c419778eb`: initial `exec-62cc1287-091e-4aab-9aae-4d334895d3cb.png`; healthy sleeve `exec-04a33dba-cb72-41dc-b980-a79005f38fca.png`; wider margins `exec-fd4430ff-9d86-406e-83ac-cd1b52acb687.png`; toe/outer strips `exec-aa6bcf68-f113-4502-b899-0ef22dab9631.png`. Exact prompts and GIMP scripts are in `art/prompts/s047-citadel-north-infirmary-before-dawn/`. Calls used the built-in tool with inspected inline references because its local-file reader failed; no fallback API.

All wide generations are natively **1672×941**, despite requesting 2560×1440. The final layered canvas is 1728×972. GIMP uniformly scales the original corrected action to 1066×600 at (325,58), matching measured registration against the completed margins, and finally scales the assembled 1728×972 view to 1920×1080 with NoHalo. These operations do not add native detail or stretch body regions. `ward-master.xcf` separates the tiny toe/side completion, protected first full-figure frame and protected original action; `sleeve-master.xcf` separately preserves the original scene and editable local sleeve mask.

Whole and native inspection covered individual heads/horns, LEFT dressing, healthy RIGHT cuff/hand, captain gesture, orderlies' bed-frame grips, clear arch route, table-remnant removal, six standing supports and the completed toe. Root reviewed the actual final candidate and passed these bounded source-art points. This painting captures the initial gathering only; departed captains, plans, letters and the later attack belong to later source beats, not this image.

## Final verification and independent review

The reopened `ward-master.xcf` reproduces both the native assembly and final PNG exactly; the reopened `sleeve-master.xcf` reproduces the sleeve-corrected source exactly. The local healthy-sleeve operation changes only pixels within original bounds (167,611)–(310,779); every original RGBA pixel outside those bounds is unchanged before the uniform reframe. Pure-white RGB pixels occupy approximately 0.0000482% of the final image.

Independent peer review inspected the actual final whole image and native contacts, then compared the current Lucan, Serat, departing-captain and Valcair portraits. It confirmed Lucan + Serat + FOUR captains: the gray-braided foreground speaker matches the departing captain's narrow face, small goatee/stubble and rear-swept horns; the dark-umber close-cropped officer is Serat with compact upright temple horns. This completed comparison supersedes an earlier naming slip in the peer's report. The review also confirmed healthy RIGHT sleeve/hand, dressed LEFT forearm, distinct horn roots, supported boots, grounded bed handlers and their hands at the frame, with a plausible passage through the arch. Root independently passed the actual final whole/native candidate.

Promoted to `renpy/game/art/scenes/s047-citadel-north-infirmary-before-dawn.png`, 1920×1080. SHA-256: `4165722188dc067441fa453946d609a8e0dd93de1a91eca8d212b5af3b846473`. Runtime grading/placement remains a separate check.
