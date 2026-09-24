# Local GIMP rescue repairs

Input: native1672×941 `exec-25c301ea-d101-42e8-b288-efa36408ebdb.png` from the built-in cache recorded in the scene brief. Final framing is already part of this generated input. Keep the generated original as a separate layer.

- Duplicate the full scene for one local navy-cloth repair. With `2. Hardness 050`, size13, clone from original source(666,274) to old glow center(667,260). An initial healing trial retained an unwanted pale spot; the final uses the cloth clone instead.
- Copy the original glow through an ellipse(660,251,16,18), feather2, to a separate layer placed at(629,251). It now sits on Mara's anatomical left shoulder in the back view, matching her already-correct left shield. Keep the same glow rather than inventing another effect.
- Copy only clear river texture from(1510,375,162,150), uniformly handled as an environmental texture and scaled to202×139, placed at(1470,239). Mask it with the polygon(1490,258),(1510,248),(1592,246),(1638,245),(1643,239),(1660,239),(1661,246),(1672,246),(1672,374),(1501,374),(1496,346),(1485,339),(1485,282),(1490,258), feather5. This removes the unrequested distant third boat and its shadow while retaining the two required craft, shore and nearby posts. This non-body texture transform does not alter any character anatomy.
- GIMP NoHalo resample the full image to1920×1080, save the four-layer `rescue-local-repairs.xcf`, then merge/export the PNG. Inspect the actual final frame and native shoulder/water boundaries. Reopen the saved master and compare its visible export pixel-for-pixel to the delivery.
