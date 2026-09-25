# S004 sling correction — 25 September 2026

Request item 5 corrects only the left soldier. The production source remains `renpy/game/art/rovel/cg/ceremony-applause.png`; the delivered replacement is `art/repaints/ceremony-applause.png`, at the unchanged 1672×941 framing. Claude owns installation and the existing Olan hand detail.

Built-in image generation painted the corrected forearms and sling from an inspection crop of the source, native bounds `(0,60)–(415,770)`, displayed at 622×1065. Exact prompt: `applause-supported-sling.txt`. Selected component: `/home/kir/.codex/generated_images/01a0d814-3271-7403-844a-00f9e9794cac/exec-a4f39ea9-2ce2-439e-bcf8-5200bbd3178b.png`.

GIMP scaled this component to 415×710 with NoHalo and positioned it at `(0,60)` over the untouched original. A two-pixel-feathered polygon mask restricts it to the arms, sling and the old forearm silhouette:

```
177,296 206,298 230,310 265,307 278,342 288,383 318,399
354,408 389,417 407,445 403,475 379,497 353,511 204,514
160,510 103,508 100,502 80,503 60,504 40,502 30,488
22,472 17,453 15,437 19,422 25,408 31,400 38,389 45,379
53,374 71,381 101,380 121,370 135,363 149,354 161,345
177,296
```

The meaningful two-layer master is `art/scene-studies/ceremony-applause/sling-repair.xcf`: original image and masked arm/sling component. The first mask retained a ghost of the old cuff under the free elbow; the final mask removes that remnant. Whole image and enlarged native arms were inspected again after the correction.

The injured anatomical left forearm now rests inside the sling, with a still supported hand. His free right palm is against his upper chest. The face, hair, uniform above/below the correction, Olan, the other soldiers, surrounding hall, overall light and framing retain original pixels. Exact RGB difference bounds are `(14,295)–(408,515)`; every pixel outside that local arm repair is identical. All of Olan and every pixel at x≥408 are identical. Reopening the XCF and re-exporting reproduces the final RGBA pixels exactly. No whole-image generation drift was installed, and no scene-wide resampling was performed.

PNG SHA-256: `717a3ae78c549478811d7e204ade8eed86ceb045420592ecb8c9cd83b1898d90`.

Source review is separate from Claude's in-game check.

Independent root review of final whole image and native crop passed: coherent supported injured forearm and distinct free palm-to-chest; no old cuff or arm remnant. Root independently confirmed the changed bounding box is confined to the soldier. The 959×1641 generated component was downsampled locally in GIMP; the 1672×941 source painting itself was not resized.
