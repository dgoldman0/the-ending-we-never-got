# Gray Scar — three new Batch 6 moments

Delivered: all three paintings have completed producing-agent, root and opening-peer whole/native review, passed exact master verification, and are saved at the requested source paths. This is neutral source art, not runtime or presentation clearance.

The complete source interaction was read before generation: original-timeline source lines 795–1020, with the preceding approach context. The pre-generation brief is [../new-moments-brief.md](../new-moments-brief.md); exact generation prompts and GIMP recipes are in [the scoped prompt folder](../../../prompts/batch6-gray-scar/new-moments/).

| Requested painting | Moment and physical action | Current candidate |
| --- | --- | --- |
| `s018-cats.png` | 795–808: Tessa arrests one wolf-sized young feline at the human litter; Mara drives the other back with her left shield, sword in her right hand. Four separate blue bearers support two continuous poles and a full adult patient. | [Candidate](s018-cats-candidate.png) |
| `s021-serat.png` | 913–934: five distinct actors beneath the rock, Serat supported by his brother while Iven and Tessa treat his anatomical left thigh. Lucan kneels beside him. The giant feline remains behind the closed gate. | [Candidate](s021-serat-candidate.png) |
| `s021-boat.png` | 937–952: nine adults aboard the broad ferry, two full adult patient supports, Tessa between them, Iven binding the same left thigh, Lucan steadying Serat. The northern family boat separates upstream. | [Candidate](s021-boat-candidate.png) |

These are three fresh scene compositions, with meaningful local GIMP corrections. They are not pixel-preserving revisions of the earlier six delivered paintings. The new paintings preserve the earlier sequence's cast, patient, plaid, equipment, giant/young feline distinction, summer setting and left-thigh injury.

## Final local work

- The trail scene was rebuilt in a broadside view after the first diagonal attempts fused or omitted bearers. Its four corner grips are now legible; the far-head forearm/hand has a dedicated masked component. The near pole terminates beyond its bearer's grip, leaving an open gap to Mara's sword hand. A short dark-haired bearer remains distinct from Mara while retaining the original warm complexion across face, neck and gripping hand. Her brief sandy-hair trial was darkened locally back to the original presentation.
- The first treatment generation omitted Serat's brother and injured the wrong leg; it was rejected. The fresh frontal five-person arrangement makes the anatomical left leg unambiguous. Local masks restore Lucan's short backward horn silhouette and move his hand onto his own knee. His brother's rounder face, low-tied dark hair and warm-tan complexion follow the actual rescue depiction and remain the same in the boat painting.
- The human patient's husband is hornless. An unsuccessful clone treatment was removed and replaced with a natural hair donor; it is not present in the final projection. Northern actors retain their individual horns. The recurring boatman follows his actual deep-brown, gray-bearded, dark-capped, ocher-coated portrait.
- Tessa wears one closed field tunic, with the approved ivory-backed botanical yoke, center band, cuffs and hem. The treatment/boat panel correction uses registration against unchanged scene features and masked GIMP layers. Face, hands, legs and physical action were protected. No extra garment layers were added.
- Fixed twelve-ray temple suns and eight-ray vertically divided northern stars are separate editable layers, with local cloth repairs beneath them.

## Review evidence

[Whole comparison](three-new-moments-comparison.jpg) · [Trail native action](s018-cats-native.jpg) · [Treatment native action](s021-serat-native.jpg) · [Boat native action](s021-boat-native.jpg) · [Final small corrections](final-small-corrections-native.jpg).

The root reviewed the three foundations whole and requested the recorded local corrections. The opening peer reviewed the treatment/boat foundations and found no additional anatomy, support or oar-pivot blocker, while explicitly withholding final clearance until the local corrections were complete. The root subsequently viewed all three current whole candidates, all three native boards and the final small-correction board, and cleared the load paths, cast continuity, left-thigh treatment, horn/skin/costume identities, rowing pivot and cloth masks. The opening peer then reviewed the current whole paintings and native evidence and independently cleared the four pole grips, adult scale, sword gap, shield ownership, skin continuity, treatment hands, support surfaces and masked joins. Both final clearances apply to the exact hashes in the delivery manifest.

The producing agent inspected each latest whole candidate, then the exact native contacts and component boundaries. The far-head grip, pole termination, Mara's shield/sword ownership, adult patient lengths, Serat's left thigh, five-person support group, nine-person boat capacity, oar pivot, recurring identities and cloth masks were examined. This does not substitute for the other team's review in the game.

## Files and technical verification

Each painting has a genuinely layered `*-master.xcf` and a corresponding `*-native-master.xcf`. Native masters retain the original generation resolution; final masters use uniform enlargement followed by a one-pixel bottom crop to deliver 1920×1080 without compressing bodies along one axis. Final projections are RGBA and fully opaque, alpha 255 throughout. Each exact final XCF was reopened independently and its projected RGBA bytes matched the candidate PNG exactly. See [verification.json](verification.json), [delivery-files.json](delivery-files.json), and [cloth-registration.json](cloth-registration.json).

Failed foundations and intermediate components are retained only for provenance. Files containing `failed` in their names, initial foundation files and pre-finish inspection boards are not delivery assets or approved character references. The delivered PNGs and their matching current candidates/final masters are the final group for the other team to grade and check in the game. The operative source-of-truth for likeness/costume remains the character keys, actual portrait references, source screenplay and user corrections.

Only the three requested neutral scene PNGs were added to the source-art directory. No source screenplay, shared canon, runtime code, staging, grading or UI files were changed.


**Checked in the game, 26 September 2026 (Claude).** All three moments play at their lines (795, 913, 937). One fault was found and fixed locally: in `s021-serat.png` a second, partly hidden head (horn, curls, cheek and ear) sat behind Serat's own, between him and his brother. It is painted out as the brother's coat in the shadow of Serat's head (7154 px; `tools/local-repairs.py`, DOUBLES, with its layered master in `art/local-repairs/doubles/`). The delivered file is kept in `art/local-repairs/originals/`.
