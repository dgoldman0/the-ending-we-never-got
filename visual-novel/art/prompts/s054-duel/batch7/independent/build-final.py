from pathlib import Path
import json,math
R=Path.cwd();P=R/'visual-novel/art/scene-studies/s054-duel/batch7/independent';PR=R/'visual-novel/art/prompts/s054-duel/batch7/independent';S=R/'visual-novel/art/scene-studies/s054-duel/batch7';V=R/'visual-novel/art/scene-studies/batch7-cats-minor/duel-valcair-component/valcair-component.png';T=S/'tessa-component.png';ROOM=S/'13-empty-hall-near-pillar.png'
def q(x):return json.dumps(str(x))
def svg(name,body):
 f=P/name;f.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1672" height="941" viewBox="0 0 1672 941">'+body+'</svg>');return f
contacts=svg('contact-shadows.svg','<g fill="#151a20" opacity=".6"><ellipse cx="119" cy="884" rx="43" ry="8"/><ellipse cx="581" cy="859" rx="53" ry="7"/><ellipse cx="1076" cy="846" rx="76" ry="9"/><ellipse cx="1610" cy="886" rx="50" ry="9"/></g>')
impact=svg('pillar-impact-detail.svg','<g fill="#393b3b"><path d="M610 279l-10 -3 -8 4 5 6 8 -2Z"/><path d="M608 277l-3 -12 -2 0 3 12Z"/><path d="M601 280l-12 2 -3 3 15 -3Z"/><path d="M603 284l-4 13 2 -1 4 -12Z"/></g><g fill="#b7b2a9" stroke="#67665f" stroke-width=".6"><path d="M593 268l-5 -4 -2 4 4 3Z"/><path d="M609 259l3 -7 3 4 -3 5Z"/><path d="M583 282l-4 -2 -3 3 4 2Z"/><path d="M603 297l-3 4 3 3 3 -4Z"/></g>')
# A tiny local ripple; wider shelter texture remains a separate additive layer.
ripple=svg('glance-ripple.svg','<g fill="none" stroke="#fffdf8"><path d="M594 273Q603 276 610 286" stroke-width="1.2" opacity=".85"/><path d="M587 266Q603 270 615 290" stroke-width=".6" opacity=".55"/></g>')
sc=['(gimp-context-push)','(gimp-context-set-interpolation INTERPOLATION-CUBIC)',f'(let* ((img (car (gimp-file-load RUN-NONINTERACTIVE {q(ROOM)} {q(ROOM)}))))','(gimp-item-set-name (car (gimp-image-get-active-layer img)) "Empty throne hall with corrected near pillar — protected plate")']
records=[]
def add(path,name,poly=None,feather=.6,matrix=None,scale=None,offset=None,mode=None,opacity=None,shadow=False,blur=None,remove=None,gamma=None):
 records.append({'file':str(path.relative_to(R)),'name':name,'polygon':poly,'matrix':matrix,'scale':scale,'offset':offset,'opacity':opacity,'mode':mode,'remove':remove,'gamma':gamma})
 sc.extend([f'(let* ((ly (car (gimp-file-load-layer RUN-NONINTERACTIVE img {q(path)}))) (mask 0))','(gimp-image-insert-layer img ly 0 0)',f'(gimp-item-set-name ly {q(name)})','(gimp-layer-add-alpha ly)'])
 if poly:
  sc.extend(['(set! mask (car (gimp-layer-create-mask ly ADD-BLACK-MASK)))','(gimp-layer-add-mask ly mask)',f'(gimp-image-select-polygon img CHANNEL-OP-REPLACE {len(poly)*2} (vector '+ ' '.join(map(str,sum(poly,[])))+'))',f'(gimp-selection-feather img {feather})','(gimp-context-set-foreground "white")','(gimp-edit-fill mask FOREGROUND-FILL)','(gimp-selection-none img)','(gimp-layer-remove-mask ly MASK-APPLY)'])
 if remove:
  sc.extend(['(set! mask (car (gimp-layer-create-mask ly ADD-WHITE-MASK)))','(gimp-layer-add-mask ly mask)',f'(gimp-image-select-polygon img CHANNEL-OP-REPLACE {len(remove)*2} (vector '+ ' '.join(map(str,sum(remove,[])))+'))','(gimp-selection-feather img 0.8)','(gimp-context-set-foreground "black")','(gimp-edit-fill mask FOREGROUND-FILL)','(gimp-selection-none img)'])
 if gamma:sc.append(f'(gimp-levels ly HISTOGRAM-VALUE 0 255 {gamma} 0 255)')
 if shadow:sc.extend(['(gimp-layer-set-lock-alpha ly TRUE)','(gimp-context-set-foreground "#101319")','(gimp-edit-fill ly FOREGROUND-FILL)','(gimp-layer-set-lock-alpha ly FALSE)'])
 if matrix:sc.extend(['(gimp-item-transform-matrix ly '+ ' '.join(map(str,matrix))+' 0 0 1)','(gimp-layer-resize-to-image-size ly)'])
 if scale:sc.append(f'(gimp-layer-scale ly {scale[0]} {scale[1]} TRUE)')
 if offset:sc.append(f'(gimp-layer-set-offsets ly {offset[0]} {offset[1]})')
 if mode:sc.append(f'(gimp-layer-set-mode ly {mode})')
 if opacity is not None:sc.append(f'(gimp-layer-set-opacity ly {opacity})')
 if blur:sc.append(f'(plug-in-gauss-iir RUN-NONINTERACTIVE img ly {blur} TRUE TRUE)')
 sc.append(')')
# Broad soft cast shadows and concentrated ground contact are actual separate layers.
add(T,'Tessa soft floor shadow',matrix=[.9703,-.55,489.665,-.06048,-.12,997.136],mode='MULTIPLY-MODE',opacity=18,shadow=True,blur=9)
add(V,'Valcair soft floor shadow',matrix=[1.02888,-.4,307.344,.08303,-.15,883.614],mode='MULTIPLY-MODE',opacity=18,shadow=True,blur=9)
add(contacts,'Four boot contact shadows',mode='MULTIPLY-MODE',opacity=62,blur=3)
# Existing actual near horn, smaller and behind the intact original crown. No face pixels transferred.
horn=[[1111,139],[1123,118],[1148,102],[1179,91],[1208,91],[1239,103],[1260,125],[1274,135],[1287,135],[1297,127],[1294,139],[1284,147],[1269,150],[1250,145],[1225,129],[1204,119],[1181,118],[1159,130],[1140,147],[1124,152]]
add(S/'09-spearman-foundation.png','Far heavy horn — rigid scaled original component behind crown',poly=horn,matrix=[.6,0,518,0,.6,17])
# Shortened forward weapon on the unchanged rigid source axis; foreground source hand covers it.
add(impact,'Bounded pillar crack and stone chips')
wood=[[399,243],[467,253],[467,265],[398,255]]
add(S/'09-spearman-foundation.png','Short real wooden shaft ahead of source grip',poly=wood,offset=[275,39])
head=[[162,218],[274,211],[300,225],[314,233],[314,242],[286,248],[173,229]]
add(S/'09-spearman-foundation.png','Real spearhead — shorter foregrip reach',poly=head,matrix=[.45144,-.015607,538.85,.015607,.45144,177.14])
add(V,'Exact Valcair source anatomy and remaining rigid shaft')
remove=[[590,394],[706,367],[714,474],[588,474],[588,442],[587,400]]
add(T,'Exact Tessa body — only original glove patch removed for rigid wrist rotation',remove=remove)
# Complete glove/pommel/grip/crossguard is a single rigid transform about wrist593420.
angle=math.radians(9.7);c=math.cos(angle);s=math.sin(angle);cx,cy=593,420
hand_matrix=[c,-s,cx-c*cx+s*cy,s,c,cy-s*cx-c*cy]
hand=[[589,396],[624,393],[629,374],[645,373],[666,389],[685,383],[701,413],[693,451],[664,456],[634,461],[612,467],[594,463],[591,444],[586,441]]
add(T,'Healthy right glove and entire hilt — rigid9.7deg wrist articulation',poly=hand,feather=.65,matrix=hand_matrix)
# Real existing sword steel, rigidly transformed. Blade axis continues the rotated hilt.
B=(252,568);E=(525,728);A=(673.3,419.2);Z=(1003,266)
vx,vy=E[0]-B[0],E[1]-B[1];wx,wy=Z[0]-A[0],Z[1]-A[1];den=vx*vx+vy*vy;a=(wx*vx+wy*vy)/den;b=(wy*vx-wx*vy)/den
blade_matrix=[a,-b,A[0]-a*B[0]+b*B[1],b,a,A[1]-b*B[0]-a*B[1]]
blade_poly=[[250,557],[279,575],[496,705],[526,728],[498,718],[277,592],[245,575]]
add(R/'visual-novel/renpy/game/art/scenes/s054-throne-hall.png','Existing arming-sword steel — rigid transform, edge at elbow and tip beyond',poly=blade_poly,feather=.45,matrix=blade_matrix)
# Organic white surface stays sparse; black is removed mathematically by Screen.
add(P/'shelter-light-donor.png','Organic white sanctuary light — additive surface',scale=[1672,923],offset=[13,48],mode='SCREEN-MODE',opacity=54)
add(ripple,'Tiny sanctuary glancing ripple by spearhead',mode='SCREEN-MODE',opacity=72,blur=.5)
# Black vapor uses Multiply so generated pale haze never whitens steel or skin.
ward=P/'black-ward-contact-donor.png';patch=[[0,0],[680,0],[720,440],[670,540],[0,540]]
for title,anchor,scale,opacity in [('Forward elbow blade rejection',(940,297),.19,92),('Rear elbow ward seam',(1320,353),.10,34),('Front knee ward seam',(1100,613),.09,30),('Rear knee ward seam',(1485,701),.08,30)]:
 x,y=anchor;tx=x-340*scale;ty=y-281*scale
 contact_patch=[[155,135],[585,135],[615,420],[590,470],[140,470]] if title.startswith('Forward') else patch
 add(ward,title,poly=contact_patch,feather=25,matrix=[scale,0,tx,0,scale,ty],mode='MULTIPLY-MODE',opacity=opacity,gamma=.40 if title.startswith('Forward') else .62)
sc.extend([f'(gimp-xcf-save RUN-NONINTERACTIVE img (car (gimp-image-get-active-layer img)) {q(P/"deterministic-master.xcf")} {q(P/"deterministic-master.xcf")})','(let* ((dup (car (gimp-image-duplicate img))) (flat (car (gimp-image-merge-visible-layers dup CLIP-TO-IMAGE))))',f'(file-png-save RUN-NONINTERACTIVE dup flat {q(P/"deterministic-native.png")} {q(P/"deterministic-native.png")} 0 9 0 0 0 0 0)','(gimp-image-delete dup))','(gimp-image-delete img))',f'(let* ((re (car (gimp-file-load RUN-NONINTERACTIVE {q(P/"deterministic-master.xcf")} {q(P/"deterministic-master.xcf")}))) (flat (car (gimp-image-merge-visible-layers re CLIP-TO-IMAGE))))',f'(file-png-save RUN-NONINTERACTIVE re flat {q(P/"deterministic-reopened.png")} {q(P/"deterministic-reopened.png")} 0 9 0 0 0 0 0)','(gimp-image-delete re))','(gimp-context-pop)','(gimp-quit 0)'])
(PR/'deterministic-final.scm').write_text('\n'.join(sc)+'\n');(P/'deterministic-spec.json').write_text(json.dumps({'native_size':[1672,941],'base':str(ROOM.relative_to(R)),'layers':records,'review_ledger':'See independent/README.md for the reviewed export hash; a new recipe run requires output verification.'},indent=2)+'\n')
