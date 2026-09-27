#!/usr/bin/env python3
"""Write a reproducible GIMP batch script; raster edits occur only in GIMP."""
import json,sys
from pathlib import Path
spec=json.loads(Path(sys.argv[1]).read_text()); out=Path(spec['output_dir']);root=Path.cwd()
def q(s): return json.dumps(str(root/s))
sc=['(gimp-context-push)',f'(let* ((img (car (gimp-file-load RUN-NONINTERACTIVE {q(Path(spec["source"]))} {q(Path(spec["source"]))}))))']
sc+=['(gimp-item-set-name (car (gimp-image-get-active-layer img)) "Current source — protected base")']
for edit in spec['edits']:
 p=Path(edit['donor']);w,h=edit['scale'];x,y=edit['offset']; pts=edit['polygon']; vals=' '.join(map(str,sum(pts,[])))
 sc +=[f'(let* ((ly (car (gimp-file-load-layer RUN-NONINTERACTIVE img {q(p)}))) (mask 0))', '(gimp-image-insert-layer img ly 0 0)',f'(gimp-item-set-name ly {json.dumps(edit["name"])})',f'(gimp-layer-scale ly {w} {h} TRUE)',*((['(gimp-item-transform-flip-simple ly ORIENTATION-HORIZONTAL TRUE 0)'] if edit.get('flip') else [])),f'(gimp-layer-set-offsets ly {x} {y})','(set! mask (car (gimp-layer-create-mask ly ADD-BLACK-MASK)))','(gimp-layer-add-mask ly mask)',f'(gimp-image-select-polygon img CHANNEL-OP-REPLACE {len(pts)*2} (vector {vals}))',f'(gimp-selection-feather img {edit.get("feather",3)})','(gimp-context-set-foreground "white")','(gimp-edit-fill mask FOREGROUND-FILL)','(gimp-selection-none img)',')']
sc += [f'(gimp-xcf-save RUN-NONINTERACTIVE img (car (gimp-image-get-active-layer img)) {q(out/"master.xcf")} {q(out/"master.xcf")})', '(let* ((dup (car (gimp-image-duplicate img))) (flat (car (gimp-image-merge-visible-layers dup CLIP-TO-IMAGE))))',f'(file-png-save RUN-NONINTERACTIVE dup flat {q(out/"candidate.png")} {q(out/"candidate.png")} 0 9 0 0 0 0 0)','(gimp-image-delete dup))','(gimp-image-delete img))',f'(let* ((re (car (gimp-file-load RUN-NONINTERACTIVE {q(out/"master.xcf")} {q(out/"master.xcf")}))) (flat (car (gimp-image-merge-visible-layers re CLIP-TO-IMAGE))))',f'(file-png-save RUN-NONINTERACTIVE re flat {q(out/"reopened.png")} {q(out/"reopened.png")} 0 9 0 0 0 0 0)','(gimp-image-delete re))','(gimp-context-pop)','(gimp-quit 0)']
(out/'build.scm').write_text('\n'.join(sc)+'\n')
