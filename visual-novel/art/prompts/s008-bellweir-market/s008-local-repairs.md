# S008 additions — GIMP local repairs and export

Built-in image generation; all four native outputs were 1672×941 despite requested 2560×1440. Final PNGs 1920×1080, GIMP 2.10 NoHalo whole-image resampling. No new native detail is claimed. No runtime grade/crop tools used.

Cache directory: `/home/kir/.codex/generated_images/01a0d813-b01b-7003-ac1a-13c396875d28/`.

## Fountain

Base `exec-0d29b805-e2eb-4931-a308-d79d4c9a7a24.png`; bounded generated arm repair `exec-a3f1f959-d365-4a01-9e40-c561f361924b.png`. The first hid Ada's left forearm/hand so its elbow looked amputated; the repair exposes the complete bent arm and hand near her collarbone. Keep base pixels outside a rectangle at native x985,y405,w188,h158, feather7px, used as a layer mask on the repair. Save meaningful two-layer `fountain-elbow-repair.xcf` before merging/export. Tessa's support wrist naturally passes behind the elbow; no invented extra hand.

## Bench drawing

Base `exec-bb6fa295-2595-43db-b384-a74da676f5d4.png`; gaze repair `exec-71914499-8696-48d8-8265-3832a9eebec9.png`. The first had Iven meeting Tessa's eyes; use only the repaired head region with native mask x1020,y130,w170,h182, feather8px. All bodies, hands, clothes, set and light retain base pixels.

The original ink sketch faced the viewer. In GIMP copy the interior of its page from the base, selection polygon `(861,568),(959,562),(985,625),(881,625)`, feather1px, convert floating selection to a separate layer, and turn the interior within its existing paper plane. The corner mapping is TL→BR, TR→BL, BR→TL, BL→TR. Use `gimp-item-transform-matrix` with the homogeneous matrix below; signs choose positive depth across the page:

```text
0.7703423986216156   0.3548856779831542  -105.95239943053879
1.0710127924025432  -0.6550164186996528  -68.56510539333917
0.0018014352794209904 0.00038628231917021754 -1.0
```

This is a local GIMP image transform, not a new generated drawing or a Python raster edit. An intermediate simple rectangular rotation visibly pasted over the paper; it was discarded in favor of this page-plane transformation. Retain the original page boundary, spine, pen and Tessa's hands. Save meaningful three-layer `bench-drawing-local-repairs.xcf` before merging/export.

Both final XCFs were reopened in a separate GIMP process and exported; RGBA pixel bytes match their delivered PNGs exactly. Full final composition and native repair areas were inspected after the final export. `new-coverage-comparison.jpg` is inspection-only: the three chronological paintings plus updated UI bounds.
