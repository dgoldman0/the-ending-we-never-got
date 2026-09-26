import bpy, math
from mathutils import Vector
from pathlib import Path
root=Path('/home/kir/Documents/Projects/the-ending-we-never-got/visual-novel/art/scene-studies/s054-strike')
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

cube('floor',(0,1,-.1),(8,9,.2),stone)
for y,z,dep in [(1.05,.075,.4),(1.45,.15,.4),(2.8,.225,2.3)]:cube('three low dais steps',(0,y,z),(5,dep,z*2),stone)
cube('throne seat',(0,3.05,.78),(.8,.75,.65),stone);cube('plain high throne back',(0,3.35,1.30),(.9,.12,1.65),stone)
for x in [-2.4,2.4]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.3,depth=4.5,location=(x,1,2.25));bpy.context.object.data.materials.append(stone)
T={'hips':(.32,.70,.80),'chest':(.15,.70,1.16),'neck':(.15,.70,1.37),'head':(.15,.70,1.52),
'ls':(.15,.47,1.27),'le':(.31,.01,.99),'lh':(-.05,.30,1.15),
'rs':(.15,.93,1.27),'re':(.39,.97,1.00),'rh':(.07,.79,1.22),
'lk':(.25,.30,.40),'lf':(.15,.05,.07),'rk':(.58,.90,.40),'rf':(.72,1.12,.07)}
V={'hips':(-.50,1.04,.69),'chest':(-.46,1.09,1.23),'neck':(-.46,1.1,1.56),'head':(-.46,1.10,1.71),
'rs':(-.46,.82,1.43),'re':(-.13,.60,1.50),'rh':(.15,.47,1.29),
'ls':(-.46,1.36,1.43),'le':(-.64,1.54,1.08),'lh':(-.40,1.68,.76),
'rk':(-.40,.75,.30),'rf':(-.35,.22,.07),'lk':(-.78,.84,.31),'lf':(-.95,.35,.07)}
for name,A,ma in [('Tessa',T,blue),('Valcair',V,steel)]:
 ell(name+' torso',A['chest'],(.22,.19,.30),ma);ell(name+' pelvis',A['hips'],(.22,.18,.16),ma);rod(name+' neck',A['chest'],A['neck'],.085,skin);ell(name+' head',A['head'],(.115,.105,.145),skin)
 for a,b,r in [('rs','re',.075),('re','rh',.06),('ls','le',.075),('le','lh',.06),('hips','lk',.115),('lk','lf',.085),('hips','rk',.115),('rk','rf',.085)]:rod(name+a+b,A[a],A[b],r,ma)
 for k in ['lf','rf']:ell(name+'boot'+k,A[k],(.12,.18,.07),glove)
 for k in ['rh','lh']:ell(name+' hand '+k,A[k],(.062,.058,.065),glove if name=='Tessa' and k=='rh' else skin)
# Tessa LEFT hand drives blade into Valcair's near RIGHT underarm; shaft absent from both grips.
tip=Vector((-.39,.91,1.36));hand=Vector(T['lh']);axis=(tip-hand).normalized();guard=hand+axis*.08;pommel=hand-axis*.13
rod('sword ordinary closed left hilt',pommel,guard,.028,wood);rod('sword rigid blade enters UNDERARM',guard,tip,.022,silver);per=axis.cross(Vector((0,0,1))).normalized();rod('sword crossguard',guard-per*.105,guard+per*.105,.015,silver)
ell('underarm entry',tip,(.05,.05,.05),red)
# Fallen spear supported on second tread, behind the figures, away from their silhouettes.
rod('dropped single spear shaft',(-.9,1.48,.335),(1.7,1.48,.335),.022,wood);rod('spear leaf tip',(1.7,1.48,.335),(1.94,1.48,.335),.04,silver)
bpy.ops.object.camera_add(location=(-3,-6,2.65));cam=bpy.context.object;target=Vector((.1,1.25,1.13));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.2;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.world.color=(.7,.7,.7);s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(root/'blocking.png');bpy.ops.wm.save_as_mainfile(filepath=str(root/'blocking.blend'));bpy.ops.render.render(write_still=True)
