import bpy, math
from mathutils import Vector
from pathlib import Path
root=Path('/home/kir/Documents/Projects/the-ending-we-never-got/visual-novel/art/scene-studies/s054-duel/batch6-grip-rebuild')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);return m
stone=mat('pale stone',(.38,.39,.38));blue=mat('Tessa blue gray',(.14,.22,.32));steel=mat('Valcair steel',(.22,.24,.25));skin=mat('hands face',(.48,.30,.20));glove=mat('brown glove',(.18,.1,.065));wood=mat('rigid wooden shaft',(.28,.13,.045));bright=mat('white ward',(.72,.85,1));silver=mat('sword steel',(.72,.77,.8));red=mat('Valcair red skirt',(.25,.07,.055))
def ell(n,p,sc,ma):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=p);o=bpy.context.object;o.name=n;o.scale=sc;o.data.materials.append(ma);return o

def rod(n,a,b,r,ma):
 v=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=r,depth=v.length,location=(Vector(a)+Vector(b))/2);o=bpy.context.object;o.name=n;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(ma);return o

def line(n,pts,r,ma):
 for j in range(len(pts)-1):rod(n+str(j),pts[j],pts[j+1],r,ma)

def cube(n,p,sc,ma):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.scale=sc;o.data.materials.append(ma);return o
# Ground and a column whose left side genuinely receives the spearhead.
cube('floor',(0,1,-.1),(12,12,.2),stone)
for p,r in [((1.12,0,2),.40),((3.6,3.4,2),.40),((3.6,5,2),.40)]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=r,depth=4,location=p);bpy.context.object.data.materials.append(stone)
for i in range(3):cube('low dais',(0,5.3+i*.25,.06*(i+1)),(3.7,1.9-i*.5,.12*(i+1)),stone)
# Woman: tilted torso, planted adult legs, right sword arm raised with neutral wrist.
T={'hips':(-.4,.45,.88),'chest':(-.25,.55,1.31),'neck':(-.23,.55,1.51),'head':(-.22,.57,1.64),
'rs':(-.113,.437,1.38),'re':(.15,.49,1.56),'rh':(.29,.71,1.77),
'ls':(-.387,.663,1.38),'le':(-.45,.84,1.12),'lh':(-.25,1.07,1.18),
'lk':(-.17,.78,.44),'lf':(0,.95,.06),'rk':(-.6,.23,.44),'rf':(-.8,0,.06)}
ell('Tessa torso',T['chest'],(.20,.14,.30),blue);ell('Tessa pelvis',T['hips'],(.20,.16,.16),blue);rod('Tessa neck',T['chest'],T['neck'],.085,skin);ell('Tessa head',T['head'],(.115,.095,.145),skin)
for a,b,r in [('rs','re',.07),('re','rh',.055),('ls','le',.07),('le','lh',.055),('hips','lk',.10),('lk','lf',.075),('hips','rk',.10),('rk','rf',.075)]:rod('Tessa '+a+' '+b,T[a],T[b],r,blue)
ell('Tessa RIGHT full sword grip',T['rh'],(.06,.055,.085),glove);ell('Tessa LEFT open palm',T['lh'],(.065,.025,.095),skin)
for k in ['lf','rf']:ell('Tessa grounded boot '+k,T[k],(.10,.18,.065),glove)
# Spearman: left-leading shoulder-elbow-hand order, rear right hand at hip.
V={'hips':(.8,1.9,.98),'chest':(.8,1.9,1.43),'neck':(.75,1.85,1.70),'head':(.70,1.79,1.85),
'ls':(.965,1.757,1.61),'le':(.85,1.47,1.61),'lh':(.62,1.24,1.52),
'rs':(.635,2.043,1.61),'re':(.45,2.30,1.34),'rh':(.55,2.05,1.32),
'lk':(.57,1.36,.48),'lf':(.35,1.15,.07),'rk':(1.06,2.07,.55),'rf':(1.25,2.30,.07)}
ell('Valcair torso',V['chest'],(.26,.20,.33),steel);ell('Valcair pelvis',V['hips'],(.25,.20,.18),red);rod('Valcair neck',V['chest'],V['neck'],.11,skin);ell('Valcair head',V['head'],(.125,.11,.16),skin)
for a,b,r in [('ls','le',.10),('le','lh',.085),('rs','re',.10),('re','rh',.08),('hips','lk',.14),('lk','lf',.10),('hips','rk',.14),('rk','rf',.10)]:rod('Valcair '+a+' '+b,V[a],V[b],r,steel)
ell('Valcair LEFT palm under stock',(.62,1.24,1.49),(.072,.07,.058),skin);ell('Valcair RIGHT rear drive grip',(.55,2.05,1.35),(.075,.07,.065),skin)
for k in ['lf','rf']:ell('Valcair grounded boot '+k,V[k],(.12,.20,.07),steel)
# Strict straight spear, aimed into the column tangent outside the woman.
D=(Vector(V['rh'])-Vector(V['lh'])).normalized();tip=Vector(V['lh'])-D*1.265;butt=Vector(V['rh'])+D*.60
rod('ONE RIGID SPEAR',tip+D*.22,butt,.022,wood)
rod('leaf spear head axis',tip,tip+D*.24,.04,silver)
ell('stone contact',tip,(.07,.05,.06),bright)
# Sword grip axis and tip actually reach lead elbow, separate from spear.
sh=Vector(T['rh']);contact=Vector(V['le']);sd=(contact-sh).normalized();guard=sh+sd*.085;pom=sh-sd*.12
rod('hilt grip',pom,guard,.028,glove);rod('blade from guard to elbow',guard,contact,.016,silver)
per=sd.cross(Vector((0,0,1))).normalized();rod('crossguard',guard-per*.105,guard+per*.105,.014,silver)
ell('elbow sword contact',contact,(.05,.05,.05),bright)
# Three thin guide arcs defining an open-topped partial sanctuary: it must not become a closed globe.
C=Vector((-.4,.45,1.05));R=.84
for theta in [math.radians(15),math.radians(45),math.radians(75)]:
 pts=[]
 for j in range(33):
  phi=math.radians(-70+j*4.6);pts.append(C+Vector((R*math.cos(phi)*math.sin(theta),R*math.cos(phi)*math.cos(theta),R*math.sin(phi))))
 line('partial shelter ribs',pts,.009,bright)
# Camera new three-quarter view.
bpy.ops.object.camera_add(location=(-7,1,2.65));cam=bpy.context.object;target=Vector((.10,1.08,1.07));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=4.75;bpy.context.scene.camera=cam
bpy.ops.object.light_add(type='AREA',location=(-3,-2,7));bpy.context.object.data.energy=1700;bpy.context.object.data.size=5
bpy.context.scene.world.color=(.22,.22,.22)
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.world.color=(.8,.8,.8);s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(root/'blocking.png');bpy.ops.wm.save_as_mainfile(filepath=str(root/'blocking.blend'));bpy.ops.render.render(write_still=True)
