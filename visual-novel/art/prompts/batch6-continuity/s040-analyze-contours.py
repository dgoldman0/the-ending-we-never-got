"""Analyze source silhouettes into vector contours; production pixels/masks are rendered by GIMP."""
from pathlib import Path
import json,cv2,numpy as np
p=Path('visual-novel/art/scene-studies/batch6-continuity/s040-mill-town')
im=cv2.imread(str(p/'before.png'));x0,y0,x1,y1=755,255,1230,685;roi=im[y0:y1,x0:x1]
labels=np.zeros(roi.shape[:2],np.uint8);spec=json.loads((p/'source-mask-points.json').read_text())
for n in ['horse','tessa','elin']:cv2.fillPoly(labels,[np.array(spec[n],np.int32)-[x0,y0]],cv2.GC_PR_FGD)
for x,y,a,b in [(817,382,875,456),(949,383,995,424),(970,461,1027,528),(994,311,1021,344),(1059,325,1094,350),(1080,410,1119,488),(1102,478,1141,520)]:cv2.rectangle(labels,(x-x0,y-y0),(a-x0,b-y0),cv2.GC_FGD,-1)
cv2.line(labels,(1109-x0,356-y0),(1164-x0,310-y0),cv2.GC_FGD,5)
cv2.ellipse(labels,(1160-x0,383-y0),(17,8),-15,0,360,cv2.GC_FGD,-1)
# Read-only color analysis identifies pale winter masonry in the open bays, not mane or blue sleeve.
for xa,ya,xb,yb in [(790,278,949,370),(909,380,946,475),(943,410,975,441),(1047,344,1064,359)]:
 region=roi[ya-y0:yb-y0,xa-x0:xb-x0];pale=(region[:,:,2]>127)&(region[:,:,1]>115)&(region[:,:,0]>105)
 v=labels[ya-y0:yb-y0,xa-x0:xb-x0];v[pale]=cv2.GC_BGD
cv2.grabCut(roi,labels,None,np.zeros((1,65),np.float64),np.zeros((1,65),np.float64),10,cv2.GC_INIT_WITH_MASK)
fg=np.where((labels==1)|(labels==3),255,0).astype(np.uint8)
contours,hierarchy=cv2.findContours(fg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE);paths=[]
for i,c in enumerate(contours):
 if abs(cv2.contourArea(c))<2:continue
 c=cv2.approxPolyDP(c,.4,True).reshape(-1,2);par=hierarchy[0][i][3];depth=0
 while par!=-1:depth+=1;par=hierarchy[0][par][3]
 if len(c)>=3:paths.append({'depth':depth,'points':(c+[x0,y0]).tolist()})
(p/'analyzed-source-contours.json').write_text(json.dumps(paths,indent=2)+'\n');print(len(paths),'contours',sum(len(q['points']) for q in paths),'vertices')
s=f'''(let* ((dir "{p.resolve()}") (im (car (gimp-file-load RUN-NONINTERACTIVE (string-append dir "/repair-master.xcf") (string-append dir "/repair-master.xcf")))) (ly (car (gimp-image-get-layer-by-name im "Original source foreground: analyzed and refined vector contours"))) (mask (car (gimp-layer-get-mask ly))))
(gimp-selection-all im) (gimp-context-set-foreground '(0 0 0)) (gimp-edit-fill mask FOREGROUND-FILL) (gimp-selection-none im)
'''
for path in sorted(paths,key=lambda q:q['depth']):
 pts=path['points'];col='255 255 255' if path['depth']%2==0 else '0 0 0'
 s+=f'(gimp-image-select-polygon im CHANNEL-OP-REPLACE {len(pts)*2} #('+ ' '.join(str(n) for pt in pts for n in pt)+f'))\n(gimp-selection-feather im 0.6) (gimp-context-set-foreground \'({col})) (gimp-edit-fill mask FOREGROUND-FILL) (gimp-selection-none im)\n'
s+='''(gimp-xcf-save RUN-NONINTERACTIVE im ly (string-append dir "/repair-master.xcf") (string-append dir "/repair-master.xcf"))
(let ((out (car (gimp-image-merge-visible-layers im CLIP-TO-IMAGE)))) (file-png-save2 RUN-NONINTERACTIVE im out (string-append dir "/candidate.png") (string-append dir "/candidate.png") 0 9 0 0 0 0 0 0 0)) (gimp-image-delete im))
(gimp-quit 0)
''';Path('visual-novel/art/prompts/batch6-continuity/s040-refined-contour-mask.scm').write_text(s)
