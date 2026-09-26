# S038 — Make Marren's existing horn pair readable

Preflight recorded 26 September 2026; completed after Chapter10, as documented below. Updated asset-request item 14 is a minor bounded correction **after Chapter 10**. At preflight no image had been changed for this item. The requested rule is to skip a correction that would disturb the finished painting; the scene's camera, composition, exposure, face and all other people remain protected.

The scene is still source 1578, Vask emerging from the inner office before Marren answers Lucan. Full source 1555–1602 and adjacent material were read. No later transfer, reply, new document or new action is added. Marren keeps his narrow pale-brown face, thinning dark hair, small rounded horns, brown clerk coat and existing expression/pose.

## Actual inspected condition

Opened the current 1920×1080 `renpy/game/art/scenes/s038-northern-stores-office.png` whole, then Marren's native head `(785,145)–(930,335)`, and compared directly with `renpy/game/art/portraits/marren-speaking.png`. The corrected scene contains small horn surfaces but they largely merge into the gray-brown hair at ordinary reading size. The portrait has a clearly bounded rounded near horn above the ear and a visible far horn by the other temple. The receiving team's item 14 supersedes the earlier favorable readability claim; unchanged likeness and clean export alone did not make both horns legible.

## Bounded proposed operation

Start from the existing `office-horns-correction-master.xcf` and its `marren-horns-correction.scm` recipe, retaining the prior scene and both local horn layers. Improve only the exposure, visible outer contour and root occlusion of those actual portrait-shaped horns. Expose a little more of the rounded surfaces through locally adjusted hair coverage if necessary; do not grow them into Lucan's swept horns or Vask's larger curls. Their light must match the window and remain ordinary material, not glowing white highlights. Do not alter the forehead, eyes, nose, mouth, ears, age, hairline beyond the immediate horn roots, head angle, body or wardrobe.

Prefer a controlled GIMP mask/placement adjustment using the retained portrait-source horn surfaces; another whole-face generation is neither required nor appropriate. If the intended visibility cannot be obtained without changing Marren's face or making the horn scale depart from his portrait, leave the finished scene intact and report that limit as the request permits. Preserve the existing tiny far-side occlusion rather than painting a floating horn outside the skull.

## References and acceptance

- Current delivered scene, opened whole and at native head size.
- `marren-speaking.png`, the actual current horn and face design; compare both sides directly rather than substituting generic horns.
- `office-horns-correction-master.xcf`, retained local layers for the already completed item 9.
- `office-local-master.xcf`, prior full scene preserved underneath.
- `art/prompts/s038-northern-stores-office/marren-horns-correction.scm`, existing reproducible correction path.
- Existing scene README and `characters/original-visuals.md`, for source 1578 and identity constraints.

After any edit, open the complete painting at normal reading size before enlarging the head. Both horns should read as horn surfaces at that size, not merely become countable at extreme zoom. Then inspect root attachment, shadow, hair occlusion, portrait-specific shape and all edges at native resolution. Verify no pixels outside a tight two-horn/root region changed, reopen the meaningful layered master against the final PNG, and obtain independent comparison. This was the preflight acceptance rule; the completed correction and actual review follow.


## Completed bounded correction

The old portrait masks discarded parts of the actual rounded surfaces: the near mask clipped its outer contour, while the far mask extended above the real tip but ended before its lower root. Root and the independent reviewer inspected the actual1254px portrait and retraced both surfaces. `horn-visibility.scm` rebuilds from the retained original office master, uses the existing0.22 uniform scale and identical attachment transforms, and applies a restrained local value curve only to those two masks. No new generation, horn enlargement or face replacement was used.

Root viewed the full1920×1080 painting reduced to reading size before the native before/after comparison. The independent reviewer then compared the same actual final whole/native pixels with the portrait: the near horn is a separate rounded tan surface in dark hair, and the far horn remains a smaller but visibly distinct surface beside the opposite temple. Roots stay attached without halos or glowing outlines.

Exactly366 pixels differ from the item9 delivery, all within the two small horn regions; combined bounding box `(828,180)–(906,204)`. Pixels outside those regions, including the complete central face, are unchanged. The final meaningful three-layer `office-horn-visibility-master.xcf` contains the unchanged scene foundation and two independently masked portrait horn surfaces. Its fresh-open export exactly reproduces all delivered RGBA pixels; the promoted PNG also exactly equals the reviewed candidate. This source-art correction does not claim runtime or user approval.
