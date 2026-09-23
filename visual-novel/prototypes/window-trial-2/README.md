# An afternoon — second bounded trial

**Status: failed; abandoned before a playable exchange.** Archived 23 September 2026. Only the two initial comparisons below exist, and they repeat the proof's dominant problems: a wash over the lower third, small portrait thumbnails (now in arched frames) and clip-art ornament. The runtime art is byte-identical to the rejected proof's. The raw Tessa sheet in `art/raw/` was generated but never integrated; it is not an approved likeness or portrait reference. See the [window failure review](../../reviews/2026-09-23-window-failure/README.md).

Originally in progress, authorized 17 September 2026 after the external VN review. The first window proof at `4001475` was rejected for stripping the ambition from the interface; this sibling preserves that rejected attempt and does not change the main runtime.

## Scope and brief

Original screenplay S005, lines 218–250: after the public ceremony has committed Tessa to tomorrow’s convoy, Iven packs a chest while she questions what the promise will cost. He puts the bottle down, admits his limits, then promises to accompany her and sits beside her. The next source scene is the convoy camp five weeks later; outside this trial.

Tessa is nineteen, healthy and uninjured, wearing the celadon underrobe, long lapis brocade coat, woven waistband, white/gold mantle, ivory slippers and brass twelve-ray temple badge. Her face is governed by the selected storm-infirmary woman, aged back to nineteen; the ceremonial key supplies clothing only. Iven is twenty-six, medium-brown skin, thick black curls, long face/wide nose, olive coat and open linen collar. His working key and written design establish identity/clothing.

Tessa occupies the left window seat looking right; Iven stands at a reachable open medical chest to her right, then sits on the space she makes. Her bag stays beside her, distinct from his medical equipment. The view down into the service yard accounts for the mother and the later cutaway to Mara assigning the two guards. The chest remains open after the final action. Harsh ordinary afternoon light, with a persistent Softened alternative.

The five existing scene paintings are being reassessed as scene components; they are not accepted style or likeness inputs for generation. Initial whole-screen comparisons use the existing four portraits strictly as temporary layout material. Compare complete screens before generating replacements.

Two different approaches: translucent pale manuscript with portraits flanking the reading field, and mineral-blue ink with paired arched reaction paintings emerging from a feathered reading field. Both retain the full scene and integrated character acting. No rollout beyond this exchange.

## Initial comparison, before new portrait generation

The browser renders in `review/comparisons/*-initial.png` were opened at 1280×720. The pale surface fights the already bright window/ivory mantle and separates the reactions across the entire reading field. Its utility contrast also fails. The dark treatment keeps both people close to the line and lets the brightly lit staging remain dominant, but the first wash has a visible upper boundary and the decorative sprigs read as flat clip art. Develop the dark composition with a continuous wash and more carefully drawn ornament; the existing small images are still temporary. This is a working selection, not visual acceptance.

The first attempt to inspect these compositions used native desktop tests. Ten abandoned native test processes from the earlier proof were found consuming roughly one core each; they ignored SIGTERM and were explicitly killed after their command lines were verified. Further visual inspection uses a single headless Chromium instance against the web build, closed in `finally`, with a process timeout. Builds use a dummy SDL display. Do not run unbounded native test previews on the user's desktop.
