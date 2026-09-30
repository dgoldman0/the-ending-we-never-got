# S053 bend — Batch 8 item 72 completion

29 September 2026. Source-art correction only; Claude still grades and checks it in the game. The user explicitly approved using the four named stair references in the built-in image generator by replying “Proceed” to the transfer question. This supersedes the earlier approval blocker recorded in the parent stair study.

## Scene and correction

Source lines 2052–2054: Mara holds the bend so only two men can reach her, while her last uninjured soldier takes a wounded man upstairs. Olan is elsewhere. The same stair in S050 has dry weathered grey flagstones and an open platform at the top. Keep the current composition, Mara's right-hand sword and left-arm shield, both attackers and their horn repairs, and the original supported climbing pose. The current source already includes the earlier Batch 8 dark-hair correction.

The revised painting gives the lower landing dry matte stone, opens the upper flight to the predawn sky, and puts broken shields against the right side of the approach. The obstacle reaches beside Mara's rightmost boot; the floor behind her and left half of the ascending stair remain open. The first generated heap crowded the escape route and was rejected. The second donor moves that rear edge toward the wall, maintaining the foreground obstruction.

## Construction and review

Built-in imagegen supplied two architecture donors. Exact prompts: [initial architecture](../../../prompts/batch8-stair/s053-completion.txt) and [retreat-path correction](../../../prompts/batch8-stair/s053-retreat-path.txt). The references were inspected inline copies of the current S053/S050 sources, because the tool's local-file helper fails in this environment. No CLI/API fallback was used.

GIMP owns all raster resizing, compositing, masks and export. `master.xcf` contains the frozen source plus eleven separate masked layers for the sky, figure restoration, wreckage, ground and boot contacts. `edit-spec.json` and `build.scm` preserve that construction. The current source is `source.png`; the pre-batch version remains at `../source-before/s053-bend.png`.

Full and native inspection checked the approach width, clear retreat steps, dry floor, boot contacts, hair silhouettes and source weapons. Close review caught a strip of old wall around the carrier's head; the final source-preservation mask follows the actual hair boundary rather than an oversized polygon. A suspected extra climbing boot proved present in the source; the original lower bodies and step contacts were restored to remove donor drift. Foreground faces, hands, weapons, upper bodies, the carrier's hair interior and representative climbing-boot interiors remain pixel-identical to the frozen current source.

[verification.json](verification.json) records opaque 1920×1080 exports, protected-region comparisons and equality with the freshly reopened master. This is supporting asset evidence, not approval of the complete game. Root and a separate reviewer inspected the final complete painting and native correction boundaries. No remaining definite mask or staging defect was found in this bounded source review. The candidate is installed at `renpy/game/art/scenes/s053-bend.png`; in-game review remains with Claude.
