#!/usr/bin/env python3
"""GIMP-only local finishing for two bounded Batch 8 Gray Scar follow-ups."""
from pathlib import Path
import json,subprocess
HERE=Path(__file__).resolve().parent

def q(v):return json.dumps(str(v))
def mask_layer(donor,scale,offset,title,polys,feather):
 lines=[f'(let* ((ly (car (gimp-file-load-layer RUN-NONINTERACTIVE im {q(donor)}))) (mask 0))','(gimp-image-insert-layer im ly 0 0)',f'(gimp-item-set-name ly {q(title)})',f'(gimp-layer-scale ly {scale[0]} {scale[1]} TRUE)',f'(gimp-layer-set-offsets ly {offset[0]} {offset[1]})','(set! mask (car (gimp-layer-create-mask ly ADD-BLACK-MASK)))','(gimp-layer-add-mask ly mask)']
 for i,p in enumerate(polys):
  flat=[v for pt in p for v in pt];lines += [f'(gimp-image-select-polygon im CHANNEL-OP-{"REPLACE" if i==0 else "ADD"} {len(flat)} (vector {" ".join(map(str,flat))}))']
 lines += [f'(gimp-selection-feather im {feather})','(gimp-context-set-foreground "white")','(gimp-edit-fill mask FOREGROUND-FILL)','(gimp-selection-none im)',')'];return lines

def brush_layer(title,lines,color,size):
 out=[f'(let* ((ly (car (gimp-layer-new im 1920 1080 RGBA-IMAGE {q(title)} 100 NORMAL-MODE))))','(gimp-image-insert-layer im ly 0 0)','(gimp-context-set-brush "2. Hardness 075")',f'(gimp-context-set-brush-size {size})',f'(gimp-context-set-foreground (list {" ".join(map(str,color))}))']
 for pts in lines:out += [f'(gimp-paintbrush-default ly {len(pts)} (vector {" ".join(map(str,pts))}))']
 out+=[')'];return out

def save(im,p):return f'(file-png-save RUN-NONINTERACTIVE {im} (car (gimp-image-get-active-layer {im})) {q(p)} {q(p)} 0 9 0 0 0 0 0)'

for name in ['s018-gray-scar-ferry-approach','s021-rescue']:
 d=HERE/name;s=d/'source.png';out=['(gimp-context-push)',f'(let* ((im (car (gimp-file-load RUN-NONINTERACTIVE {q(s)} {q(s)}))))','(gimp-item-set-name (car (gimp-image-get-active-layer im)) "Current source with Claude repairs")']
 if name.startswith('s018'):
  out += brush_layer('Complete left and right rear escort strings to both bow tips',[[1195.06,622.48,1190.3,643.0],[1291.36,654.82,1289.8,674.2]],[177,166,146],1.0)
  crops=[('bows-after.png',(1110,500,235,280))]
 else:
  out += mask_layer(d/'face-donor.png',[150,169],[722,229],'Iven lower face: clean-shaven, source eyes and hair protected',[[[773,277],[783,278],[793,278],[803,280],[803,290],[799,295],[791,297],[780,292],[773,285]]],0.7)
  out += mask_layer(d/'bow-donor.png',[180,245],[320,410],'Spent lower bow assembly: continuous string and cleared old diagonals',[[[339,535],[415,535],[463,572],[463,612],[340,614]]],1.6)
  crops=[('face-after.png',(720,230,120,135)),('bow-after.png',(320,410,180,245))]
 out += [f'(gimp-xcf-save RUN-NONINTERACTIVE im (car (gimp-image-get-active-layer im)) {q(d/"master.xcf")} {q(d/"master.xcf")})','(let* ((dup (car (gimp-image-duplicate im))))','(gimp-image-merge-visible-layers dup CLIP-TO-IMAGE)',save('dup',d/'candidate.png'),'(gimp-image-delete dup))']
 for fn,(x,y,w,h) in crops:
  out += ['(let* ((dup (car (gimp-image-duplicate im))))','(gimp-image-merge-visible-layers dup CLIP-TO-IMAGE)',f'(gimp-image-crop dup {w} {h} {x} {y})',save('dup',d/fn),'(gimp-image-delete dup))']
 out += ['(gimp-image-delete im))',f'(let* ((re (car (gimp-file-load RUN-NONINTERACTIVE {q(d/"master.xcf")} {q(d/"master.xcf")}))))','(gimp-image-merge-visible-layers re CLIP-TO-IMAGE)',save('re',d/'reopened.png'),'(gimp-image-delete re))','(gimp-context-pop)','(gimp-quit 0)']
 (d/'build.scm').write_text('\n'.join(out)+'\n')
 subprocess.run(['gimp','-i','-f','--no-splash','--new-instance','-b',f'(load "{d}/build.scm")'],check=True)
