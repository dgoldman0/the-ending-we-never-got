#!/usr/bin/env python3
"""Reproduce Batch 8 items 63, 65, 66 using GIMP masks and archived sources.

All raster scaling, selection, compositing and export is performed by GIMP.
Polygons use the 1200 x 675 inspection coordinate system, scaled to 1920 x 1080.
Sources are the archived current runtime PNGs, including Claude's local fixes.
"""
from pathlib import Path
import subprocess, json, sys
ROOT=Path(__file__).resolve().parents[1]
STUDY=ROOT/'art/scene-studies/batch8-citadel-ward-lever'
SCALE=1.6

def poly(points):
 return '#('+ ' '.join(str(round(v*SCALE,3)) for p in points for v in p)+')'
def select(points,op='CHANNEL-OP-ADD'):
 return f'(gimp-image-select-polygon img {op} {2*len(points)} {poly(points)})'
def layer(path,name,regions,exclude=(),feather=2,offset=(0,0),opacity=100):
 s=f'''(let* ((fix (car (gimp-file-load-layer RUN-NONINTERACTIVE img "{path}"))))
(gimp-image-insert-layer img fix 0 0)
(gimp-layer-scale fix 1920 1080 FALSE)
(gimp-layer-set-offsets fix {round(offset[0]*SCALE)} {round(offset[1]*SCALE)})
(gimp-item-set-name fix "{name}")
(gimp-layer-set-opacity fix {opacity})
(gimp-layer-set-composite-space fix LAYER-COLOR-SPACE-RGB-PERCEPTUAL)
(gimp-layer-set-blend-space fix LAYER-COLOR-SPACE-RGB-PERCEPTUAL)
(gimp-selection-none img)
'''
 for p in regions:s+=select(p)+'\n'
 for p in exclude:s+=select(p,'CHANNEL-OP-SUBTRACT')+'\n'
 if feather:s+=f'(gimp-selection-feather img {feather})\n'
 s+='(gimp-layer-add-mask fix (car (gimp-layer-create-mask fix ADD-SELECTION-MASK)))\n(gimp-selection-none img))\n'
 return s

def save(name,layers):
 d=STUDY/name
 s=f'(let* ((img (car (gimp-file-load RUN-NONINTERACTIVE "{d}/before.png" "{d}/before.png"))))\n(gimp-item-set-name (car (gimp-image-get-active-layer img)) "Untouched runtime source incl Claude fixes")\n'+''.join(layers)
 s+=f'''(gimp-xcf-save RUN-NONINTERACTIVE img (car (gimp-image-get-active-layer img)) "{d}/repair-master.xcf" "{d}/repair-master.xcf")
(let* ((flat (car (gimp-image-duplicate img))))
(gimp-image-flatten flat)
(file-png-save RUN-NONINTERACTIVE flat (car (gimp-image-get-active-drawable flat)) "{d}/candidate.png" "{d}/candidate.png" 0 9 0 0 0 0 0)
(gimp-image-scale flat 1200 675)
(file-jpeg-save RUN-NONINTERACTIVE flat (car (gimp-image-get-active-drawable flat)) "/tmp/batch8-citadel/{name}-candidate.jpg" "preview.jpg" 0.90 0 1 0 "" 0 1 0 0)
(gimp-image-delete flat))
(gimp-image-delete img))
'''
 return s

# S052 surface defects shared by the two states. Small source-texture repair
# masks cross the actual defect rather than tracing and preserving old remnants.
notch=[(638,137),(658,141),(678,143),(682,164),(665,166),(646,161)]
seam=[(670,157),(684,160),(685,224),(675,224)]
# Generated stone and cloth are kept only at the small seam itself.
landing_donor=STUDY/'s052-citadel-inner-landing/ward-donor.png'
shared=lambda:[layer(landing_donor,'Local pilaster notch and vertical paste seam', [notch,seam], exclude=[[(675,197),(686,195),(694,198),(695,206),(704,214),(698,218),(695,225),(684,235),(673,231),(669,218),(671,208)]], feather=3)]
landing=shared()
landing += [layer(landing_donor,'Thinning black ward across the entire doorway',[
 [(773,0),(1123,0),(1123,489),(1139,510),(1139,580),(1119,577),(775,547),(774,515),(789,487),(798,438),(797,363),(787,288),(772,267),(764,174),(753,163),(756,126),(776,75)]
],exclude=[[(693,116),(764,116),(764,183),(693,183)]],feather=2)]
landing += [layer(landing_donor,'Thinning ward edge meets actual stone jamb',[
 [(1133,508),(1152,509),(1153,582),(1115,578),(1115,565),(1133,565)]
],offset=(14,0),feather=3)]
landing += [layer(STUDY/'s052-citadel-inner-landing/before.png','Dark stone replaces pale old floor rim behind runner boot',[
 [(125,550),(159,538),(162,542),(159,546),(128,555)],
 [(209,536),(223,528),(256,515),(281,506),(285,512),(258,522),(226,535),(214,541)]
],offset=(-131,434),feather=3)]
ward=shared()
ward += [layer(STUDY/'s052-entrance-ward/before.png','Ward carried into right jamb; remove vertical cut',[
 [(1118,481),(1152,500),(1153,582),(1138,589),(1112,581),(1106,559)]
],offset=(45,0),feather=4)]
ward += [layer(landing_donor,'Cold ward threshold edge seated on stone',[
 [(774,537),(1122,568),(1122,580),(774,550)]
],feather=3),layer(landing_donor,'Threshold edge meets jamb without floor strip',[
 [(1105,565),(1153,569),(1153,585),(1105,582)]
],offset=(14,0),feather=4)]
# Lever material masks. Weapons, figures, metal lever and the steps remain source.
lever_donor=STUDY/'s054-lever/stone-donor.png'
lever=[layer(lever_donor,'Carved stone throne back and foot',[
 [(210,96),(264,25),(355,93),(363,264),(419,248),(425,340),(420,371),(429,391),(424,432),(428,471),(337,479),(209,421)]
],feather=2)]
lever += [layer(lever_donor,'Matte stone lever housing; metal pivot protected',[
 [(444,439),(463,429),(473,438),(518,452),(530,441),(530,431),(538,427),(593,437),(598,459),(598,586),(526,626),(442,570)]
],feather=2)]
lever += [layer(lever_donor,'Stone dais block front and side',[
 [(0,402),(202,459),(337,496),(443,526),(443,570),(526,601),(596,561),(699,450),(785,376),(798,348),(816,346),(806,378),(789,407),(712,480),(622,552),(565,611),(340,555),(181,510),(0,460)],
 [(584,212),(981,229),(981,267),(960,276),(957,244)]
],feather=2)]
# Exact source restores protect adjacent edges when resurfacing reaches them.
# Duel uses one independently positioned elbow effect and remaining local joints.
duel_donor=STUDY/'s054-duel/ward-donor.png'
duel=[layer(duel_donor,'Black ward repelling blade at extended elbow',[
 [(643,178),(671,170),(695,178),(718,201),(720,237),(706,267),(680,282),(655,260),(644,232)]
],offset=(-24,-3),feather=8)]
duel += [layer(duel_donor,'Black ward from shoulder waist knee and ankle joints',[
 [(837,160),(843,143),(870,116),(891,111),(909,121),(944,115),(969,130),(982,156),(966,183),(950,207),(925,217),(907,208),(900,180),(872,187)],
 [(929,226),(952,221),(980,219),(1021,224),(1037,244),(1039,277),(1025,302),(1007,320),(979,313),(959,293),(942,275)],
 [(827,285),(856,281),(886,292),(916,286),(953,289),(981,305),(1004,330),(1013,366),(1005,385),(983,374),(970,345),(945,335),(916,328),(881,334),(845,346),(813,353),(792,360),(776,385),(758,375),(770,342),(794,311)],
 [(758,408),(782,412),(799,421),(821,425),(835,446),(832,475),(814,492),(790,484),(772,472),(746,475),(730,462),(737,436)],
 [(1055,465),(1080,467),(1110,474),(1138,500),(1136,531),(1110,550),(1081,542),(1056,521),(1043,495)],
 [(764,529),(784,520),(803,537),(821,560),(820,586),(798,600),(780,590),(758,581),(746,559)],
 [(1112,567),(1136,563),(1160,577),(1187,592),(1194,625),(1185,641),(1159,631),(1134,614),(1114,607),(1104,587)]
],feather=8)]
# Retain the exact spear including the shaft in front of the energy, and retain
# the whole original sword except the immediate black contact at the elbow.
duel += [layer(STUDY/'s054-duel/before.png','Original spear and blade geometry protected',[
 [(435,195),(460,196),(484,202),(1107,294),(1115,297),(1114,305),(1106,304),(477,212),(447,207),(435,206)],
 [(469,296),(634,221),(645,217),(647,221),(478,308)]
],feather=0)]
duel += [layer(STUDY/'s054-duel/before.png','Original Valcair face hair and horns retained',[
 [(770,49),(930,44),(939,84),(921,119),(905,139),(877,144),(858,163),(838,173),(825,182),(810,170),(790,158),(781,138),(775,118)],
 [(777,92),(854,92),(854,183),(777,183)]
],feather=0)]
jobs={'s052-citadel-inner-landing':landing,'s052-entrance-ward':ward,'s054-lever':lever,'s054-duel':duel}
names=sys.argv[1:] or list(jobs)
scm='\n'.join(save(n,jobs[n]) for n in names)+'\n(gimp-quit 0)\n'
script=Path('/tmp/batch8-citadel/composite.scm');script.write_text(scm)
subprocess.run(['gimp-console-2.10','-n','-i','-d','-f','-b',f'(load "{script}")'],check=True)
print('Masked GIMP candidates saved: '+', '.join(names)+'. Runtime sources have not been replaced.')
