# Batch 7 — neutral source-art delivery

**22 repaired scene sources and two new portrait sources**, covering required items 47–61 and selected optional fixes. Request baseline: `8d6f4e4`, the other team’s completed Batch 6 integration and new request. The complete file list, hashes, dimensions, GIMP masters and exact reopened exports are in [delivery-manifest.json](delivery-manifest.json).

This delivery changes neutral source art at the requested existing paths, plus the new healer portraits. It does not change screenplay, runtime code, staging, cropping or grading. The pre-existing root `AGENTS.md` modification is excluded.

## Delivered groups

| Commit | Files / request items | Review and preservation |
| --- | --- | --- |
| `7337709` | S051 right hand; S052 pair stone; S053 defended bend (49,58,60) | Root whole/native; mask overlap on Tessa’s fingers and Olan’s hair caught and removed; S053 blade and far horn repaired before promotion. |
| `86e9974` | S018 cats, S011 Renn, S034 engineers/doorway (48,55,56) | Root whole/native and independent Gray Scar comparison; litter-bearer interception, downhill house/gorge, Mara’s footing and small Renn checked. |
| `37ce46a` | S040 barrier/wheel (optional) | Root whole/native; wardkeeper’s hand retained after removing a donor halo. |
| `b997759` | S057 sentry horns/caps (59) | Root whole/native; foreground bearers, their complexions, Lucan and litter unchanged. |
| `facc215` | S050 stone/hand seam, S055 morning stone, S058 floor gaps (60 + optional S050) | Root whole/native; stone, feet, furniture, dressings, coat tear and rail checked. |
| `949bf01` | Stair healer speaking/listening (61) | Separate directions, human source-scene identity, root whole/native and independent review. |
| `f20741e` | Seven Gray Scar paintings (50–54,59; optional family boat/patient hair) | Root whole/native plus independent horn/patient review; functional crossbows, paired Lucan horns, adult litters and Serat’s distinct dark-skinned brother. |
| `f642b2a` | S054 lever (57), S058 drawings (optional) | Connected three-step dais; Valcair’s uphill reach and horns; Tessa’s injured RIGHT hand and bare LEFT lever grip. Drawings face outward over paving; both reviewers caught and corrected mask fringes. |
| `2e99f11` | Immutable pre-repair citadel inputs | Scripts now reopen the recorded starting snapshots; no further source-pixel change. |
| `72a624b` | S054 duel (47) | Rebuilt from independently checked figure components, with root and peer whole/native review of the same final image; straight hilt/blade, valid grips, pillar impact outside the grounded shelter, black ward at the actual elbow contact. |

`b3e01c7` is a diagnostic checkpoint, not a duel delivery. The early duel files named `candidate.png` and `delivery-master.xcf` in the parent study directory remain rejected. Use the selected [independent delivery](../s054-duel/batch7/independent/README.md), [PNG](../s054-duel/batch7/independent/delivery.png) and [layered master](../s054-duel/batch7/independent/delivery-master.xcf).

## What changed in the duel

The rejected revisions had preserved the faulty interaction. The replacement retains a separately checked spear stance and Tessa’s correctly handed figure; their room, weapons, shelter, contact shadows and black ward are editable components in GIMP. The spear’s unheld forward section is deliberately shorter, stopping at a nearer pillar before reaching her head or palm. The sword passes in front of that pillar and its outer cutting edge meets the forward elbow, with the point extending past contact. A small rigid rotation of the complete glove and hilt aligns the handle with the straight blade; it does not redraw the fingers. Valcair retains two heavy backward horns and his black-and-silver hair.

Root and an independent reviewer inspected the same native image (`df48f5df…4029daf`), including both grips, cuff/guard/pommel alignment, elbow contact, shelter path, pillar depth, foot contacts and mask edges. The native assembly is 1672×941; delivery uses one uniform scale factor on both axes and a final canvas trim to 1920×1080. It is not a claim of newly generated native 1920 detail.

## Optional carryovers

Completed: S040 barrier/wheel; families in the first S021 boat; the patient’s light-brown hair across S019/S020; outward-facing S058 drawings; S050’s hand seam.

Deferred: S004 emblems and the S049/S052 scabbard moves. Earlier emblem attempts flattened decorated fabric, and the destination hips are obscured by people or the table. The S049 table support remains: its current shape plausibly reads as a rear corner leg, so no member was removed without a clear structural case. These optional items are not marked fixed.

## Verification and next owner

Every delivered source matches its recorded reopened GIMP export. Scenes are opaque 16:9: 21 at 1920×1080; S057 father retains its existing 2240×1260. Both healer portraits are transparent 1394×1394. The manifest records baseline hashes and changed-pixel bounds; subgroup records describe protected areas. Full reblocks such as S053 and the duel intentionally change broad areas. The lever retains source face/hand details through uniform transforms, so those are not claimed byte-identical after resampling. The drawings preserve 1,437,648 foreground interior pixels exactly.

Generation used the built-in image tool; actual masks, assembly, corrections and exports use GIMP. Prompts are under [batch7-cats-minor](../../prompts/batch7-cats-minor/), [batch7-gray-scar](../../prompts/batch7-gray-scar/), [batch7-citadel](../../prompts/batch7-citadel/), [s054-duel/batch7](../../prompts/s054-duel/batch7/) and [s058-drawings/batch7](../../prompts/s058-drawings/batch7/). Masters and subgroup observations remain alongside their scene studies.

**Stopped at the end of Batch 7.** The other team performs cropping, grading and connected in-game review before the next request. Source-level visual review and an exact export do not establish runtime or user approval.
