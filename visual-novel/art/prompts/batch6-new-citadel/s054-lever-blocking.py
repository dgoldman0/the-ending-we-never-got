import bpy, math
from mathutils import Vector
from pathlib import Path
root=Path('/home/kir/Documents/Projects/the-ending-we-never-got/visual-novel/art/scene-studies/s054-lever')
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

cube('hall floor',(0,-2,-.1),(8,18,.2),stone)
for y,z,dep in [(1.05,.075,.4),(1.45,.15,.4),(3.55,.225,3.8)]:cube('three low dais steps',(0,y,z),(6,dep,z*2),stone)
cube('throne seat',(0,2.8,.82),(.85,.8,.74),stone);cube('throne high back',(0,3.18,1.50),(.95,.14,2.10),stone)
for x in [-2.6,2.6]:
 for y in [1,-2,-5,-8]:
  bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.32,depth=4.8,location=(x,y,2.4));bpy.context.object.data.materials.append(stone)
cube('far entrance left pier',(-2.45,-10,2.4),(1.8,.5,4.8),stone);cube('far entrance right pier',(2.45,-10,2.4),(1.8,.5,4.8),stone)
cube('entrance lintel',(0,-10,4.3),(3.2,.5,1.0),stone)
black=mat('fading black entrance ward',(.04,.05,.06));cube('black entry plane',(0,-10,1.7),(2.6,.02,3.4),black)
# Mechanical release behind throne, mounted on real masonry with a visible pivot.
cube('lever stone mounting post',(-1.65,3.75,.78),(.28,.32,.68),stone)
ell('IRON LEVER PIVOT',(-1.65,3.75,1.08),(.085,.085,.085),steel)
rod('iron lever pivot to grip',(-1.65,3.75,1.08),(-1.45,3.35,1.22),.035,steel)
rod('lever grip',(-1.55,3.35,1.22),(-1.35,3.35,1.22),.045,wood)
# Tessa front faces camera/back wall +Y. LEFT is -X, on screen RIGHT.
T={'hips':(-1.05,2.96,1.23),'chest':(-1.12,3.22,1.55),'neck':(-1.10,3.34,1.77),'head':(-1.09,3.42,1.89),
'ls':(-1.34,3.22,1.62),'le':(-1.52,3.33,1.40),'lh':(-1.45,3.35,1.22),
'rs':(-.90,3.22,1.62),'re':(-.87,3.15,1.35),'rh':(-1.01,3.37,1.58),
'lk':(-1.23,2.87,.85),'lf':(-1.32,2.70,.51),'rk':(-.87,2.88,.84),'rf':(-.82,2.58,.51)}
ell('Tessa torso',T['chest'],(.22,.16,.3),blue);ell('Tessa hips',T['hips'],(.20,.16,.16),blue);rod('Tessa neck',T['chest'],T['neck'],.085,skin);ell('Tessa head',T['head'],(.115,.105,.145),skin)
for a,b,r in [('rs','re',.07),('re','rh',.055),('ls','le',.07),('le','lh',.055),('hips','lk',.11),('lk','lf',.08),('hips','rk',.11),('rk','rf',.08)]:rod('Tessa'+a+b,T[a],T[b],r,blue)
for k in ['lf','rf']:ell('Tessa boot '+k,T[k],(.11,.18,.07),glove)
ell('Tessa LEFT bare working hand',T['lh'],(.06,.055,.07),skin);ell('Tessa RIGHT torn glove at chest',T['rh'],(.06,.055,.07),glove)
# Valcair collapsed below first riser, reaching uphill toward dropped spear.
ell('Valcair head',(.65,.18,.30),(.125,.13,.16),skin);rod('Val torso',(.8,.04,.26),(1.22,-.48,.24),.23,steel);ell('Val hips',(1.25,-.52,.24),(.22,.22,.16),red)
for a,b in [((1.25,-.52,.24),(1.63,-.96,.15)),((1.63,-.96,.15),(1.93,-1.31,.10)),((1.25,-.52,.24),(.95,-.96,.15)),((.95,-.96,.15),(1.30,-1.50,.10)),((.8,.0,.34),(.38,.42,.24)),((.38,.42,.24),(.38,.88,.18))]:rod('Valcair armor limb',a,b,.09,steel)
ell('Valcair reaching hand',(.38,.89,.18),(.065,.075,.05),skin)
rod('fallen spear on second tread',(-.25,1.47,.335),(2.25,1.47,.335),.022,wood);rod('spear leaf tip',(2.25,1.47,.335),(2.52,1.47,.335),.04,silver)
# Her sword set on dais before she uses left hand for mechanism.
rod('set-down sword blade',(-1.4,2.25,.47),(-1.95,2.50,.47),.018,silver);rod('set-down sword hilt',(-1.4,2.25,.47),(-1.22,2.17,.47),.025,wood)
for obj in bpy.context.scene.objects:
 if obj.name.startswith('Val') or obj.name.startswith('fallen spear') or obj.name.startswith('spear leaf'):obj.location.x-=1.1
bpy.ops.object.camera_add(location=(-3.4,6.5,3.6));cam=bpy.context.object;target=Vector((-.1,1.60,.8));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='PERSP';cam.data.lens=26;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.world.color=(.7,.7,.7);s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(root/'blocking.png');bpy.ops.wm.save_as_mainfile(filepath=str(root/'blocking.blend'));bpy.ops.render.render(write_still=True)
