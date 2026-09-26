"""Build local GIMP masks from the documented donor recipes; no raster manipulation here."""
import json,pathlib,subprocess,sys
here=pathlib.Path(__file__).resolve().parent
study=here.parents[1]/'scene-studies'/'batch6-temple-emblems'
root=here.parents[3]
def q(s):return json.dumps(str(s))
recipes=json.loads((here/'recipes.json').read_text())
for name,r in recipes.items():
 if len(sys.argv)>1 and name not in sys.argv[1:]:continue
 base=study/name/'before.png'
 out=study/name/'candidate.png';master=study/name/'repair-master.xcf'
 cmds=[f'(let* ((im (car (gimp-file-load RUN-NONINTERACTIVE {q(base)} {q(base)}))) (l 0) (mask 0) (out 0) (base 0))', '(gimp-item-set-name (car (gimp-image-get-active-layer im)) "Current neutral original — unchanged")']
 if r.get('normalize_alpha'):
  cmds += ['(set! l (car (gimp-image-get-active-layer im)))','(set! mask (car (gimp-layer-create-mask l ADD-ALPHA-TRANSFER-MASK)))','(gimp-layer-add-mask l mask)','(gimp-layer-remove-mask l MASK-DISCARD)']
 cmds += ['(set! base (car (gimp-image-get-active-layer im)))']
 for c in r['components']:
  w,h=c['size'];x,y=c.get('offset',[0,0])
  if 'color' in c:
   col=' '.join(str(v) for v in c['color'])
   cmds += [f'(set! l (car (gimp-layer-new im {w} {h} RGBA-IMAGE {q(c["name"])} 100 NORMAL-MODE)))','(gimp-image-insert-layer im l 0 0)',f"(gimp-context-set-foreground '({col}))",'(gimp-edit-fill l FOREGROUND-FILL)',f'(gimp-layer-set-offsets l {x} {y})']
  else:
   path=study/'components'/c['file']
   cmds += [f'(set! l (car (gimp-file-load-layer RUN-NONINTERACTIVE im {q(path)})))','(gimp-image-insert-layer im l 0 0)']
   if 'source_crop' in c:
    cx,cy,cw,ch=c['source_crop'];cmds += [f'(gimp-layer-resize l {cw} {ch} {-cx} {-cy})']
   cmds += [f'(gimp-layer-scale l {w} {h} TRUE)',f'(gimp-layer-set-offsets l {x} {y})',f'(gimp-item-set-name l {q(c["name"])})']
  if 'blur' in c:cmds += [f'(plug-in-gauss-iir RUN-NONINTERACTIVE im l {c["blur"]} TRUE TRUE)']
  if 'brightness' in c:cmds += [f'(gimp-brightness-contrast l {c["brightness"][0]} {c["brightness"][1]})']
  if 'perspective' in c:
   pts=' '.join(str(v) for point in c['perspective'] for v in point)
   cmds += ['(gimp-context-set-transform-resize TRANSFORM-RESIZE-ADJUST)',f'(set! l (car (gimp-item-transform-perspective l {pts})))']
  if 'mode' in c:cmds += [f'(gimp-layer-set-mode l {c["mode"]})']
  if 'opacity' in c:cmds += [f'(gimp-layer-set-opacity l {c["opacity"]})']
  cmds += ['(set! mask (car (gimp-layer-create-mask l ADD-BLACK-MASK)))','(gimp-layer-add-mask l mask)']
  if 'source_gold_mask' in c:
   mx,my,mw,mh=c['source_gold_mask'];col=' '.join(str(v) for v in c.get('gold_color',[185,160,108]))
   cmds += ['(gimp-context-set-sample-threshold-int 44)',f"(gimp-image-select-color im CHANNEL-OP-REPLACE base '({col}))",f'(gimp-image-select-rectangle im CHANNEL-OP-INTERSECT {mx} {my} {mw} {mh})','(gimp-selection-grow im 2)','(gimp-selection-feather im 1.4)',"(gimp-context-set-foreground '(255 255 255))",'(gimp-edit-fill mask FOREGROUND-FILL)','(gimp-selection-none im)']
  for poly in c.get('polygons',[]):
   coords=' '.join(str(v) for p in poly for v in p)
   cmds += [f'(gimp-image-select-polygon im CHANNEL-OP-REPLACE {len(poly)*2} #({coords}))',f'(gimp-selection-feather im {c.get("feather",1.5)})','(gimp-context-set-foreground \'(255 255 255))','(gimp-edit-fill mask FOREGROUND-FILL)','(gimp-selection-none im)']
 cmds += [f'(gimp-xcf-save RUN-NONINTERACTIVE im l {q(master)} {q(master)})','(set! out (car (gimp-image-merge-visible-layers im CLIP-TO-IMAGE)))',f'(file-png-save2 RUN-NONINTERACTIVE im out {q(out)} {q(out)} 0 9 0 0 0 0 0 0 0)','(gimp-image-delete im))','(gimp-quit 0)']
 script=here/(name+'.scm');script.write_text('\n'.join(cmds)+'\n')
 subprocess.run(['gimp','-n','-i','--console-messages','-b',f'(load {q(script)})'],check=True)
 print(name,'built',flush=True)
