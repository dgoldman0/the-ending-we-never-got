# Local healthy-thigh repair

The accepted corrected1672×941 scene has the anatomicalLEFT near leg properly splinted, but a small wrap at the far RIGHT thigh could suggest another injury. Built-in `right-wrap-removal.txt` generated clean skin/blanket continuation. To preserve all other approved pixels, GIMP used that output ONLY through a2px-feathered polygon mask with native vertices `(1158,495),(1215,495),(1255,496),(1290,532),(1255,542),(1180,543),(1160,528)`.

Pixel comparison against the accepted corrected source confirms all changed native pixels are confined to bbox`(1157,494)–(1291,544)`. No faces, hands, near-left splint, report, garments or room geometry changed. Full/native inspection found no visible patch edge; far thigh continues naturally into the loose pelvis blanket.

The two meaningful layers—accepted source and masked local patch—were scaled together by GIMP NoHalo to1920×1080 and saved as `art/scene-studies/s025-royal-infirmary-corridor/local-wrap-repair.xcf`. Reopened XCF visible export matches delivered PNG RGB bytes exactly. Native source remained1672×941; delivery scaling does not add native detail.
