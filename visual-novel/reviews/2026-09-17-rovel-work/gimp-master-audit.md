# Rovel GIMP master reproducibility audit

Snapshot: 2026-09-17T12:51:38.374806+00:00. Verification: 2026-09-17T12:58:43.075587+00:00.

**31 masters reopened successfully; all 146 RGBA comparisons were exact, covering 116 distinct runtime PNGs.** This verifies export reproducibility and asset structure only. It does not clear appearance, source continuity, anatomy, lighting impact, UI composition, or the connected scene gates.

## Method

- Copied the 31 then-existing `art/rovel/masters/*.xcf` files to `/tmp/rovel-master-audit/masters/`, recording SHA-256 values before auditing. Source masters and delivered PNGs were not changed.
- GIMP 2.10 reopened each copied master. A duplicated image was merged and exported with its saved visible layers; each named Intense/Softened grade and portrait variant was then selected and exported separately. The hidden quiet-panel layer was also exported in its intended stack.
- Runtime comparison inputs were copied to `/tmp` and hashed. Pillow/NumPy were used only to read RGBA pixels, dimensions, alpha ranges and differences, with no image editing.
- Compared every channel of every pixel after RGBA decoding. “Exact” includes alpha and RGB beneath transparency; matching file compression or metadata was not required.
- The 31 saved defaults, 114 named grade/variant states and one alternate UI state all matched. There were no missing comparison PNGs. Detailed hashes, layer names/visibility, masks, destinations and per-export results are in [gimp-master-audit.json](gimp-master-audit.json).

The named-grade export process ended with status 143 after all expected PNGs had been written. Every expected file decoded completely and all pixel comparisons passed; subsequent isolated GIMP invocations use `--new-instance` to prevent shared-instance shutdown interference. No cause beyond that possibility was established.

## Snapshot results

| Master | Native size | Saved visible default | Named paired/UI exports | Alpha range | Result |
| --- | --- | --- | ---: | --- | --- |
| `blue-healing-repair.xcf` | 1672 × 941 | `blue-healing.png` | 2 | 255–255 | Exact |
| `ceremony-applause.xcf` | 1672 × 941 | `ceremony-applause.png` | 2 | 255–255 | Exact |
| `ceremony-dais.xcf` | 1672 × 941 | `ceremony-dais.png` | 2 | 255–255 | Exact |
| `ceremony-intervention.xcf` | 1672 × 941 | `ceremony-intervention.png` | 2 | 255–255 | Exact |
| `ceremony-mantle.xcf` | 1672 × 941 | `ceremony-mantle.png` | 2 | 255–255 | Exact |
| `ceremony-orders.xcf` | 1672 × 941 | `ceremony-orders.png` | 2 | 255–255 | Exact |
| `ceremony-refusal.xcf` | 1672 × 941 | `ceremony-refusal.png` | 2 | 255–255 | Exact |
| `ceremony-refused-chair.xcf` | 1672 × 941 | `ceremony-refused-chair.png` | 2 | 255–255 | Exact |
| `ceremony-yield.xcf` | 1672 × 941 | `ceremony-yield.png` | 2 | 255–255 | Exact |
| `iven-attentive.xcf` | 512 × 512 | `iven-attentive-ordinary.png` | 4 | 0–254 | Exact |
| `iven-concerned.xcf` | 512 × 512 | `iven-concerned-ordinary.png` | 4 | 0–254 | Exact |
| `mara-controlled.xcf` | 512 × 512 | `mara-controlled-ordinary.png` | 6 | 0–254 | Exact |
| `mara-uneasy.xcf` | 512 × 512 | `mara-uneasy-ordinary.png` | 6 | 0–254 | Exact |
| `messenger.xcf` | 512 × 512 | `messenger-bright.png` | 2 | 0–254 | Exact |
| `mother.xcf` | 512 × 512 | `mother-ordinary.png` | 2 | 0–254 | Exact |
| `olan.xcf` | 512 × 512 | `olan-bright.png` | 4 | 0–254 | Exact |
| `orra.xcf` | 512 × 512 | `orra-bright.png` | 2 | 0–254 | Exact |
| `petitioner.xcf` | 512 × 512 | `petitioner-bright.png` | 2 | 0–254 | Exact |
| `priest.xcf` | 512 × 512 | `priest-ordinary.png` | 2 | 0–254 | Exact |
| `purification-cleared-repair.xcf` | 1672 × 941 | `purification-cleared.png` | 2 | 255–255 | Exact |
| `reading-surface.xcf` | 1600 × 438 | `reading-surface.png` | 1 | 0–255 | Exact |
| `senn-assuring.xcf` | 512 × 512 | `senn-assuring-bright.png` | 2 | 0–254 | Exact |
| `senn-evasive.xcf` | 512 × 512 | `senn-evasive-bright.png` | 2 | 0–254 | Exact |
| `senn-listening.xcf` | 512 × 512 | `senn-listening-bright.png` | 2 | 0–254 | Exact |
| `tessa-listening.xcf` | 512 × 512 | `tessa-listening-formal-ordinary.png` | 12 | 0–255 | Exact |
| `tessa-resolute.xcf` | 512 × 512 | `tessa-resolute-formal-ordinary.png` | 12 | 0–255 | Exact |
| `tessa-startled.xcf` | 512 × 512 | `tessa-startled-formal-ordinary.png` | 12 | 0–255 | Exact |
| `tessa-wounded.xcf` | 512 × 512 | `tessa-wounded-formal-ordinary.png` | 12 | 0–255 | Exact |
| `window-packing.xcf` | 1672 × 941 | `window-packing.png` | 2 | 255–255 | Exact |
| `window-pause.xcf` | 1672 × 941 | `window-pause.png` | 2 | 255–255 | Exact |
| `window-together.xcf` | 1672 × 941 | `window-together.png` | 2 | 255–255 | Exact |

## Layer structure and limits

- Thirteen scene/repair masters reproduce 26 scene PNGs at 1672 × 941 with alpha 255 throughout. Scene grades are saved independently; the two healer repairs retain grouped, masked local source repairs for each grade.
- Seventeen portrait masters reproduce 88 portrait PNGs at 512 × 512. Portrait masks and original expression crops remain present. Tessa alpha spans 0–255. The other portraits span 0–254, so even their most opaque pixels retain about 0.4% transparency; this small inherited alpha characteristic is recorded, not treated as aesthetic approval.
- `reading-surface.xcf` reopens with the original reading surface visible. Enabling its quiet-panel repair layer reproduces `quiet-surface.png` exactly. Both UI exports are 1600 × 438 with alpha spanning 0–255; no lighting alternate is intended for these reading surfaces.
- The saved portrait default is the final named Intense variant, not every wardrobe/lighting state at once: Tessa formal-ordinary, Iven/Mara ordinary, Senn bright, Olan bright, priest/mother ordinary, and other supporting figures bright.
- Grade layers that bake a corrected composite are reproducible, but they are not procedural adjustment layers. If an underlying repair changes, the corresponding grade composites and both PNGs need rebuilding. Merely toggling an old top grade will continue displaying its baked pixels.

## Snapshot boundary

- Masters changed after the snapshot: none at verification time.
- New masters excluded because they arrived after the snapshot: `last-patch-arm-turn.xcf`, `ward-assessment.xcf`.
- Runtime comparison files changed since the audit copy: none at verification time.
- New or subsequently edited masters require another reopen/export comparison. This audit does not cover the older opening masters outside `art/rovel/masters/`, discovery-detail derivations without their own masters, or later route assets.

## Later identity correction

After this fixed snapshot audit, the six Senn ceremony masters were superseded for runtime delivery by sibling `*-identity-repair.xcf` masters. Their twelve revised exports received a separate successful reopen/pixel audit recorded in [the Senn repair review](../../art/rovel/review/senn-identity-repair.md). The original 146 comparisons above describe the earlier snapshot, not the subsequently corrected runtime pixels.
