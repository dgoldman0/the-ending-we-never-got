import bpy, math
from mathutils import Vector
from pathlib import Path
out=Path('/home/kir/Documents/Projects/the-ending-we-never-got/visual-novel/art/scene-studies/s054-duel/batch7')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def material(name,c):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);return m
stone=material('stone',(.5,.5,.48));blue=material('Tessa blue',(.10,.24,.38));steel=material('Valcair armor',(.20,.23,.24));skin=material('warm skin',(.5,.30,.19));glove=material('short right glove',(.20,.10,.06));wood=material('single wood spear',(.33,.12,.035));white=material('white shelter',(.8,.94,1));metal=material('silver blade',(.7,.74,.78));black=material('black elbow ward',(.012,.008,.018));red=material('burgundy',(.25,.035,.055))
def ell(n,p,scale,ma):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=p);o=bpy.context.object;o.name=n;o.scale=scale;o.data.materials.append(ma);return o

def rod(n,a,b,r,ma):
 a=Vector(a);b=Vector(b);v=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=r,depth=v.length,location=(a+b)/2);o=bpy.context.object;o.name=n;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(ma);return o

def cube(n,p,sc,ma):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.scale=sc;o.data.materials.append(ma);return o

def arc(n,pts):
 for j in range(len(pts)-1):rod(n+str(j),pts[j],pts[j+1],.007,white)
cube('floor',(0,1,-.08),(14,15,.16),stone)
T={'hip':(-.4,.45,.87),'chest':(-.32,.53,1.27),'head':(-.3,.60,1.61),
'rs':(-.17,.39,1.38),'re':(.12,.50,1.56),'rh':(.40,.70,1.60),
'ls':(-.48,.67,1.38),'le':(-.6,.94,1.20),'lh':(-.28,1.17,1.19),
'rk':(-.65,.10,.46),'rf':(-.9,-.1,.055),'lk':(-.02,.76,.43),'lf':(.12,1.06,.055)}
V={'hip':(1.80,1.80,1.0),'chest':(1.67,1.77,1.46),'head':(1.54,1.70,1.84),
'ls':(1.55,1.60,1.61),'le':(1.20,1.43,1.60),'lh':(.95,1.50,1.30),
'rs':(1.80,1.95,1.61),'re':(2.0,1.85,1.25),'rh':(1.80,1.50,1.30),
'lk':(1.35,1.14,.52),'lf':(1.30,.8,.06),'rk':(2.05,2.12,.55),'rf':(2.30,2.35,.06)}
for name,actor,body,leg,r in [('Tessa',T,blue,blue,.085),('Valcair',V,steel,red,.11)]:
 ell(name+' torso',actor['chest'],(.20 if name=='Tessa' else .27,.17,.3),body);ell(name+' pelvis',actor['hip'],(.20 if name=='Tessa' else .26,.17,.17),leg);ell(name+' head',actor['head'],(.115 if name=='Tessa' else .135,.12,.15),skin)
 rod(name+' neck',actor['chest'],actor['head'],.07,skin)
 for a,b,rad in [('rs','re',r),('re','rh',r*.78),('ls','le',r),('le','lh',r*.78),('hip','lk',r*1.18),('lk','lf',r*.9),('hip','rk',r*1.18),('rk','rf',r*.9)]:rod(name+' '+a+b,actor[a],actor[b],rad,body)
 for k in ['lf','rf']:ell(name+' boot'+k,actor[k],(.10,.17,.06),glove)
ell('Tessa RIGHT sword glove',T['rh'],(.052,.052,.072),glove);ell('Tessa LEFT bare palm',T['lh'],(.07,.025,.085),skin)
# Pole is a single immutable geometric line through both hands, with its point in solid stone.
D=(Vector(V['rh'])-Vector(V['lh'])).normalized();tip=Vector(V['lh'])-D*.95;butt=Vector(V['rh'])+D*.7
rod('ONE RIGID SPEAR SHAFT',tip+D*.21,butt,.021,wood);rod('spear steel point',tip,tip+D*.24,.04,metal)
for k in ['lh','rh']:ell('Valcair grip '+k,V[k],(.065,.065,.06),skin)
# Columns: point reaches rightmost tangent on foreground central pillar.
pillar=Vector(tip)+Vector((0,.29,0));pillar.z=2.7
bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=.29,depth=5.4,location=pillar);bpy.context.object.name='SPEAR IMPACT COLUMN';bpy.context.object.data.materials.append(stone)
for xy in [(-2.3,3.0),(2.8,4.4),(-2.3,6)]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=.29,depth=5.4,location=(*xy,2.7));bpy.context.object.data.materials.append(stone)
# One sword from RIGHT grip to forward LEFT elbow.
h=Vector(T['rh']);target=Vector(V['le']);sd=(target-h).normalized();guard=h+sd*.08;pom=h-sd*.12
rod('sword hilt',pom,guard,.025,glove);rod('sword blade to elbow',guard,target,.017,metal)
per=sd.cross(Vector((0,0,1))).normalized();rod('crossguard',guard-per*.095,guard+per*.095,.012,metal);ell('BLACK ward at elbow',target,(.115,.11,.12),black)
# Front hemisphere, grounded opening at rear for the outward sword cut.
C=Vector((-.40,.45,.30));R=1.50;low=math.asin(-C.z/R)
for az in [math.radians(-35),math.radians(0),math.radians(35),math.radians(70),math.radians(105)]:
 pts=[]
 for i in range(45):
  elev=low+(math.pi/2-low)*i/44;pts.append(C+Vector((R*math.cos(elev)*math.cos(az),R*math.cos(elev)*math.sin(az),R*math.sin(elev))))
 arc('DOME meridian',pts)
pts=[]
for i in range(55):
 az=math.radians(-35+140*i/54);pts.append(C+Vector((R*math.cos(low)*math.cos(az),R*math.cos(low)*math.sin(az),-C.z)))
arc('DOME FLOOR footprint',pts)
for i in range(3):cube('dais riser '+str(i),(0,5.7+i*.35,.08*(i+1)),(4.2,2.4-i*.7,.16*(i+1)),stone)
cube('plain throne back',(0,6.0,1.25),(.8,.25,1.5),steel)
bpy.ops.object.camera_add(location=(3,-7,2.8));cam=bpy.context.object;look=Vector((.55,1.1,1.05));cam.rotation_euler=(look-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.9;bpy.context.scene.camera=cam
bpy.ops.object.light_add(type='AREA',location=(-3,-3,7));bpy.context.object.data.energy=1500;bpy.context.object.data.size=5
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(out/'blocking.png');bpy.ops.wm.save_as_mainfile(filepath=str(out/'blocking.blend'));bpy.ops.render.render(write_still=True)
