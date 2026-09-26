"""Reopen delivery masters and export their exact visible pixels and mask unions for inspection."""
import json,pathlib,subprocess
from PIL import Image
here=pathlib.Path(__file__).resolve().parent;study=here.parents[1]/'scene-studies'/'batch6-opening';tmp=pathlib.Path('/tmp/batch6-opening-checks');tmp.mkdir(exist_ok=True)
r=json.loads((here/'recipes.json').read_text());code=[]
def q(x):return json.dumps(str(x))
for n in r:
 master=study/(n+'-master.xcf');w,h=Image.open(study/(n+'-candidate.png')).size
 code.append(f'''(let* ((im (car (gimp-file-load RUN-NONINTERACTIVE {q(master)} {q(master)}))) (layers (gimp-image-get-layers im)) (mi (car (gimp-image-new {w} {h} RGB))) (bg (car (gimp-layer-new mi {w} {h} RGBA-IMAGE "Black outside repair masks" 100 NORMAL-MODE))) (j 0) (l 0) (mask 0) (ml 0) (off 0) (merged 0))
(gimp-image-insert-layer mi bg 0 0)
(gimp-context-set-foreground '(0 0 0))
(gimp-edit-fill bg FOREGROUND-FILL)
(while (< j (car layers))
 (set! l (vector-ref (cadr layers) j))
 (set! mask (car (gimp-layer-get-mask l)))
 (if (> mask -1)
  (begin
   (set! off (gimp-drawable-offsets l))
   (set! ml (car (gimp-layer-new-from-drawable mask mi)))
   (gimp-image-insert-layer mi ml 0 0)
   (gimp-layer-set-offsets ml (car off) (cadr off))
   (gimp-layer-set-mode ml LIGHTEN-ONLY-MODE)))
 (set! j (+ j 1)))
(set! merged (car (gimp-image-merge-visible-layers mi CLIP-TO-IMAGE)))
(file-png-save2 RUN-NONINTERACTIVE mi merged {q(tmp/(n+'-mask.png'))} "mask" 0 9 0 0 0 0 0 0 0)
(set! merged (car (gimp-image-merge-visible-layers im CLIP-TO-IMAGE)))
(file-png-save2 RUN-NONINTERACTIVE im merged {q(tmp/(n+'-reopened.png'))} "reopened" 0 9 0 0 0 0 0 0 0)
(gimp-image-delete mi)
(gimp-image-delete im))''')
code.append('(gimp-quit 0)');script=here/'verify-masters.scm';script.write_text('\n'.join(code)+'\n')
subprocess.run(['gimp','-n','-i','--console-messages','-b',f'(load {q(script)})'],check=True)
