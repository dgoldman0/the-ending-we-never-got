# Local checkerboard correction

The original full scene is retained. Both imagegen attempts returned incorrect board grids; `generation.txt` is the scene prompt and `board-edit.txt` records the rejected targeted retry. The retry was not composited into the final painting.

GIMP 2.10.36 local repair, before delivery scaling:

- Rectified the original board texture into a temporary 576 × 512 image for sampling.
- Built a 512 × 512 playing surface with exactly eight rows and columns of 64 px squares, using clean light and dark painted-wood patches from that original image. No flat-color vector grid or new scene texture was introduced.
- Copied the original round painted ivory/dark counters with feathered selections onto a separate layer. Five ivory and five dark counters occupy dark squares; the front rank is empty. Their sparse position is a staging choice, not a specified canonical move.
- Perspective-transformed the grid and counter layers into the existing board inset at native corners TL (924,633), TR (1173,643), BL (848,721), BR (1178,741). The changed native bounding box is exactly (848,633)–(1178,741). Outside it, including all characters, hands, key, cups and the board’s wood border, RGB pixels match the original generation.
- Final three-layer master: original scene / repaired painted-wood 8×8 grid / ten round counters. Scaled the complete layered image once with GIMP NoHalo to 1920 × 1080 from native 1672 × 941 and exported PNG. No exposure, grade or crop change.

Counter square coordinates, zero-based (row, column); top-left square is light:

- Ivory: (1,2), (2,3), (3,0), (3,6), (2,7).
- Dark: (4,1), (4,5), (5,2), (5,6), (6,3).

All listed sums are odd, so all counters are on dark squares. At delivery scale the nearest counter remains above y840. The lower wood border may enter the shaded bottom fifth; it contains no counter, key or hand contact.

Final reopened-XCF pixel comparison: **exact RGB byte match** between the final PNG and an independently reopened/re-exported XCF.
