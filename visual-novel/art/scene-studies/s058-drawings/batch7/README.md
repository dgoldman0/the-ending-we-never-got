# Batch 7 — S058 drawings, optional viewpoint repair

Source 2175–2215 read before generation. Tessa, about23, sits on the fountain rim facing out into Bellweir square, looks at the kitchen drawing and Iven's S008 hair-up sketch, then closes the packet. This is the same over-lap viewpoint and the same LEFT grip/RIGHT soft brace. Current source contains Claude's removal of an accidental moustache from Iven; preserve every drawing/board/hand/fabric pixel. The discrepancy is the basin/rim ahead of her, which implies she has turned to face the fountain.

Change only background beyond the lap and drawing board to matching market-square paving at the existing camera angle and neutral light. The fountain is behind the camera; no basin or new furniture ahead. Generated donor is only a background component, merged through GIMP masks traced to the foreground silhouettes. Protected-region equality for all paper, drawings, board, fingers, brace and costume is required. Inspect full view and native edge joins; exact reopened editable master before any source promotion.

Current source SHA256: 991ff56021c23916dde1bd09828d3f4a662c358bfb13ae4b934445e9dea91248


## Delivered composite and independent review

`candidate.xcf` contains the generated clean market paving underneath the **original current source foreground**, with a hand-traced alpha mask. Neither drawing, the wood board, either hand, the right soft brace nor the plum costume was generated or RGB-painted. The first coarse silhouette retained unwanted gray background fringes; Citadel retraced the native boundaries, then Cats/minor independently refined the remaining right knuckle/brace/sleeve edge. `candidate-before-final-fringe.png` is a diagnostic prior export, not the delivery. The initial `background-donor.png` contains generated foreground and was not used as foreground; `clean-paving-plate.png` supplies the replacement background only.

Root independently inspected the final whole composition and native left hand/forearm, paper top, right knuckles/brace and lower sleeve V before clearing delivery. The foreground core of 1,437,648 pixels is exactly unchanged; protected drawing/hand/brace/board/costume regions show zero changed pixels. Only silhouette-edge alpha transitions and the background change. Ten antialiased edge pixels round to 255 in the separate mask export while retaining 1–4level blend differences in the XCF projection; these lie on the boundary, not the protected interior. `verification.json` records that distinction, hashes, opaque dimensions and exact XCF re-export equality. `final-fringe-review.md` records the independent mask review. This production review does not replace user or runtime acceptance.

The foreground input in `compose.scm` is the immutable `before.png`, hash-checked against the recorded pre-repair source, so rerunning the mask cannot use the newly composited background as input.
