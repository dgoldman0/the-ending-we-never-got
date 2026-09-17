# Blue-healing garment seam — local GIMP repair

17 September 2026. Scoped correction only; independent main-thread review and the connected scene gate remain pending.

The older healer's apron/upper sleeve had a horizontal composite boundary at y=357. The old master pasted a rectangle from `opening-sequence/raw/blue-final.png` beneath the differently positioned upper garment in `raw/blue-healing.png`. Both original XCFs and all raw images were inspected and preserved.

The [new master](../masters/blue-healing-repair.xcf) retains the existing runtime Intense and Softened scene plates. Only the garment join and the immediately adjacent curtain are repaired from the same `raw/blue-final.png` source. GIMP 2.10.36 applies a local garment alignment (`x′ = x − 0.3y + 130`, `y′ = y`), an editable contour mask, and a separately masked untransformed curtain clone. No generated replacement or whole-frame re-render was used. The mask excludes faces, bare arms, hands and magic. The original ordinary Intense and Softened exposure recipes are retained separately.

The XCF contains two named lighting groups; enable only one. Each has the preserved scene plate, a graded garment layer with an editable contour mask, and a curtain source layer with its own editable mask. The raw donor is retained as a hidden, ungraded, untransformed source layer. These are editable local repairs; the existing cast in the retained plates is not falsely represented as separately editable sprites. The saved default is Intense.

Both full 1672×941 runtime exports and native 620×510 garment/treatment crops were opened after export. The sleeve reaches the unchanged healing forearm, the apron top/straps read continuously, and the previous rectangular cut and stray shoulder fragment are absent. Both light settings received this review. The master was then reopened; Intense and Softened exports from its saved layers match their delivered PNG pixels exactly.

Read-only pixel comparison against the pre-repair exports found all changes within x=648–1231, y=198–430. Checked regions covering Iven's and Olan's faces, the healer's face/neck interior, her bare forearm and blue light, Olan's injured right arm, Iven's supporting hands, and Olan's rail-gripping hand have zero changed pixels. Nothing outside the local garment/curtain region changed. These checks supplement the visual review; they do not clear source blocking, UI or connected performance.

Delivered files are `renpy/game/art/opening/cg/blue-healing.png` and its paired `art/softened/opening/cg/blue-healing.png`. The working script and original-export backups remain in `/tmp/source-gate-blue-repair/`; final inspection crops are `final-intense-native-crop.png` and `final-softened-native-crop.png` there. No other scene, original master, raw source or lighting metadata was changed by this repair.
