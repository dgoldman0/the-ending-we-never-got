from pathlib import Path
import json
root=Path.cwd();p=root/'visual-novel/art/scene-studies/s054-duel/batch7/independent';src=root/'visual-novel/art/scene-studies/s054-duel/batch7';pr=root/'visual-novel/art/prompts/s054-duel/batch7/independent'
def svg(name,body):
 f=p/name;f.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1672" height="1000" viewBox="0 0 1672 1000">'+body+'</svg>');return f
bg=svg('guide-background.svg','<rect width="1672" height="1000" fill="#a7a8aa"/><path d="M0 800H1672M0 900H1672M800 610L100 1000M800 610L1550 1000" stroke="#87888a" stroke-width="1"/><text x="25" y="35" fill="#242526" font-size="22">GEOMETRY GUIDE ONLY — preserved character pixels; provisional pillar, floor and weapons</text>')
pillar=svg('guide-pillar.svg','<path d="M520 0H615V766H520Z" fill="#73777b" stroke="#494b4d" stroke-width="2"/><path d="M525 0H542V766H525Z" fill="#919497"/><ellipse cx="566" cy="775" rx="59" ry="18" fill="#55595b"/><path d="M507 765H626V787H507Z" fill="#696d70" stroke="#494b4d" stroke-width="2"/>')
pole=svg('guide-forward-spear.svg','<path d="M674 289L737 298" stroke="#563c25" stroke-width="9"/><path d="M609 279L643 277L675 285L676 293L641 292Z" fill="#b8bec1" stroke="#434c52" stroke-width="2"/><path d="M610 279L674 289" stroke="#dde3e5" stroke-width="1"/>')
dome=svg('guide-dome.svg','<path d="M20 870A370 720 0 0 1 760 870" fill="#f7fcff" fill-opacity=".035" stroke="#e2f7ff" stroke-width="3"/><ellipse cx="390" cy="870" rx="370" ry="45" fill="none" stroke="#e2f7ff" stroke-width="3"/>')
blade=svg('guide-sword.svg','<path d="M666 397L1020 262L670 409Z" fill="#c9d5de" stroke="#445866" stroke-width="1"/><path d="M668 403L1020 262" stroke="#f9fbfc" stroke-width="2"/>')
ward=svg('guide-elbow-ward.svg','<ellipse cx="931" cy="301" rx="26" ry="27" fill="none" stroke="#252131" stroke-width="5" opacity=".65"/>')
body=[[1070,168],[1078,126],[1100,104],[1180,86],[1240,96],[1280,136],[1305,126],[1290,154],[1250,170],[1265,190],[1320,198],[1364,241],[1370,302],[1378,354],[1370,392],[1430,497],[1485,616],[1536,706],[1580,786],[1645,840],[1648,894],[1600,905],[1578,863],[1550,820],[1510,783],[1452,713],[1412,690],[1340,715],[1270,750],[1200,712],[1176,656],[1130,607],[1150,737],[1154,810],[1143,849],[1095,858],[995,858],[995,829],[1061,804],[1073,735],[1076,654],[1045,604],[1068,556],[1127,520],[1147,465],[1110,430],[1090,393],[1100,377],[1100,342],[1100,292]]
arm=[[696,261],[732,258],[768,267],[873,260],[904,256],[917,264],[940,278],[1010,248],[1097,231],[1129,272],[1098,322],[1038,347],[958,352],[908,328],[807,319],[745,321],[701,310],[691,290]]
shaft=[[700,279],[1562,409],[1564,427],[697,299]]
def q(x):return json.dumps(str(x))
sc=['(gimp-context-push)',f'(let* ((img (car (gimp-file-load RUN-NONINTERACTIVE {q(bg)} {q(bg)}))))']
def layer(path,name):
 sc.extend([f'(let* ((ly (car (gimp-file-load-layer RUN-NONINTERACTIVE img {q(path)}))))','(gimp-image-insert-layer img ly 0 0)',f'(gimp-item-set-name ly {q(name)})',')'])
layer(pillar,'Provisional middle-ground pillar behind Tessa')
sc.extend([f'(let* ((ly (car (gimp-file-load-layer RUN-NONINTERACTIVE img {q(src/"09-spearman-foundation.png")}))) (mask 0))','(gimp-image-insert-layer img ly 0 0)','(gimp-item-set-name ly "09 exact Val pose — coarse guide mask only")','(set! mask (car (gimp-layer-create-mask ly ADD-BLACK-MASK)))','(gimp-layer-add-mask ly mask)'])
for i,pts in enumerate([body,arm,shaft]):sc.append(f'(gimp-image-select-polygon img CHANNEL-OP-{"REPLACE" if i==0 else "ADD"} {len(pts)*2} (vector '+ ' '.join(map(str,sum(pts,[])))+'))')
sc.extend(['(gimp-context-set-foreground "white")','(gimp-edit-fill mask FOREGROUND-FILL)','(gimp-selection-none img)',')'])
layer(pole,'Shortened forward spear — unchanged axis and gripping hands')
layer(src/'tessa-component.png','Exact Tessa alpha scale1 offset0')
layer(dome,'Provisional grounded dome — floor390870 radius370')
layer(blade,'Rigid blade from guard to forward elbow — visible point beyond')
layer(ward,'Elbow contact marker only')
sc.extend([f'(gimp-xcf-save RUN-NONINTERACTIVE img (car (gimp-image-get-active-layer img)) {q(p/"deterministic-guide.xcf")} {q(p/"deterministic-guide.xcf")})','(let* ((dup (car (gimp-image-duplicate img))) (flat (car (gimp-image-merge-visible-layers dup CLIP-TO-IMAGE))))',f'(file-png-save RUN-NONINTERACTIVE dup flat {q(p/"deterministic-guide.png")} {q(p/"deterministic-guide.png")} 0 9 0 0 0 0 0)','(gimp-image-delete dup))','(gimp-image-delete img))','(gimp-context-pop)','(gimp-quit 0)'])
(pr/'deterministic-guide.scm').write_text('\n'.join(sc)+'\n')
