#!/usr/bin/env python3
"""Reconstruct Batch 8 minor repairs as GIMP layers and hand-shaped masks."""
from pathlib import Path
import json, subprocess, sys
HERE=Path(__file__).resolve().parent
specs={
's034-return-cargo-shed':dict(crop=[1660,160,220,380],donor='guard-donor.png',layers=[
 ('Third northern guard: green cap and compact horn',[[[157,91],[181,90],[182,126],[163,125],[157,118]]],0.8),
 ('Third northern guard: green coat',[[[171,154],[183,151],[183,251],[173,263],[166,243],[170,217],[170,196],[164,186],[167,171]]],0.8)]),
's050-citadel-lower-stair':dict(crop=[1170,625,440,305],donor='stone-donor.png',layers=[
 ('Pier base and step end: remove old diamond surface',[[[72,3],[179,2],[179,109],[147,114],[145,169],[171,173],[171,233],[73,235]]],1.8)]),
's051-north-infirmary-court':dict(crop=[300,390,320,170],donor='crossbow-hand-donor.png',layers=[
 ('Level crossbow: edge-on bow, restored stone, and articulated hands',[[[20,18],[108,13],[122,26],[216,53],[229,53],[254,56],[277,70],[280,91],[290,108],[252,116],[249,148],[227,163],[187,155],[154,154],[142,146],[144,129],[135,117],[92,117],[20,110]]],1.5)]),
's058-final':dict(crop=[430,615,1100,460],donor='floor-donor.png',layers=[
 ('Floor continuation behind chair and stool',[[[585,175],[620,177],[1040,125],[1050,345],[1005,399],[820,414],[591,387]]],8.0),
 ('Floor beside Tessa table leg',[[[266,95],[281,105],[287,164],[280,193],[266,192]]],2.5),
 ('Floor beside stool leg at Orren boot',[[[560,63],[582,69],[594,95],[590,130],[563,130]]],2.0)
 ],protect=[
 [[596,0],[886,0],[889,178],[877,197],[845,208],[803,209],[631,183],[609,181]],
 [[615,152],[650,165],[651,202],[638,357],[629,365],[610,360],[604,349]],
 [[800,175],[841,178],[838,282],[833,391],[821,399],[800,393],[797,280]],
 [[682,182],[718,187],[714,293],[704,299],[684,295]],
 [[757,189],[786,191],[785,258],[776,265],[756,260]],
 [[872,140],[898,140],[904,305],[898,319],[879,320],[871,307]],
 [[643,249],[803,278],[807,305],[642,279]],
 [[708,218],[874,246],[879,265],[709,237]],
 [[642,241],[680,211],[695,222],[656,258]],
 [[834,272],[873,241],[879,263],[835,301]],
 [[880,46],[1019,39],[1026,104],[994,124],[885,110]],
 [[912,92],[937,99],[936,199],[928,208],[915,205]],
 [[956,107],[979,107],[990,262],[981,274],[962,271]],
 [[992,95],[1011,89],[1025,214],[1018,225],[1003,224]],
 [[933,162],[999,156],[1004,175],[933,180]]
 ])}
def quoted(p): return json.dumps(str(p))
def poly_select(im,polys,ox,oy):
 lines=[]
 for i,p in enumerate(polys):
  pts=[v for x,y in p for v in (x+ox,y+oy)]
  lines.append(f'(gimp-image-select-polygon {im} CHANNEL-OP-{"REPLACE" if i==0 else "ADD"} {len(pts)} (vector {" ".join(map(str,pts))}))')
 return lines
def save_png(im,path):
 q=quoted(path)
 return f'(file-png-save RUN-NONINTERACTIVE {im} (car (gimp-image-get-active-layer {im})) {q} {q} 0 9 0 0 0 0 0)'
# The donor matches the lower furniture silhouette; broad old-source masks
# retained old floor fringes, so retain the coherent lower-region donor.
specs['s058-final'].pop('protect')
for name,s in specs.items():
 if len(sys.argv)>1 and name not in sys.argv[1:]: continue
 d=HERE/name;ox,oy,w,h=s['crop'];q=quoted(d/'source.png')
 lines=['(gimp-context-push)',f'(let* ((img (car (gimp-file-load RUN-NONINTERACTIVE {q} {q}))))','(gimp-item-set-name (car (gimp-image-get-active-layer img)) "Current source, Claude repairs preserved")']
 for title,polys,feather in s['layers']:
  lines += [f'(let* ((ly (car (gimp-file-load-layer RUN-NONINTERACTIVE img {quoted(d/s["donor"])}))) (mask 0))','(gimp-image-insert-layer img ly 0 0)',f'(gimp-item-set-name ly {quoted(title)})',f'(gimp-layer-scale ly {w} {h} TRUE)',f'(gimp-layer-set-offsets ly {ox} {oy})','(set! mask (car (gimp-layer-create-mask ly ADD-BLACK-MASK)))','(gimp-layer-add-mask ly mask)']
  lines += poly_select('img',polys,ox,oy)
  lines += [f'(gimp-selection-feather img {feather})','(gimp-context-set-foreground "white")','(gimp-edit-fill mask FOREGROUND-FILL)','(gimp-selection-none img)',')']
 if 'protect' in s:
  lines += [f'(let* ((ly (car (gimp-file-load-layer RUN-NONINTERACTIVE img {quoted(d/"source.png")}))) (mask 0))','(gimp-image-insert-layer img ly 0 0)','(gimp-item-set-name ly "Protected original furniture silhouettes")','(set! mask (car (gimp-layer-create-mask ly ADD-BLACK-MASK)))','(gimp-layer-add-mask ly mask)']
  lines += poly_select('img',s['protect'],ox,oy)
  lines += ['(gimp-selection-feather img 0.45)','(gimp-context-set-foreground "white")','(gimp-edit-fill mask FOREGROUND-FILL)','(gimp-selection-none img)',')']
 lines += [f'(gimp-xcf-save RUN-NONINTERACTIVE img (car (gimp-image-get-active-layer img)) {quoted(d/"master.xcf")} {quoted(d/"master.xcf")})','(let* ((dup (car (gimp-image-duplicate img))))','(gimp-image-merge-visible-layers dup CLIP-TO-IMAGE)',save_png('dup',d/'candidate.png'),f'(gimp-image-crop dup {w} {h} {ox} {oy})',save_png('dup',d/'after-native.png'),'(gimp-image-delete dup))','(gimp-image-delete img))',f'(let* ((re (car (gimp-file-load RUN-NONINTERACTIVE {quoted(d/"master.xcf")} {quoted(d/"master.xcf")}))))','(gimp-image-merge-visible-layers re CLIP-TO-IMAGE)',save_png('re',d/'reopened.png'),'(gimp-image-delete re))','(gimp-context-pop)','(gimp-quit 0)']
 (d/'edit-spec.json').write_text(json.dumps(s,indent=2)+'\n')
 (d/'build.scm').write_text('\n'.join(lines)+'\n')
 subprocess.run(['gimp','-i','-d','-f','--no-splash','--new-instance','-b',f'(load "{d}/build.scm")'],check=True)
