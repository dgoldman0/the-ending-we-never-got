import bpy, math
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);return m
stone=mat('stone',(0.38,.4,.41));floor=mat('flat landing',(0.52,.54,.55));step=mat('regular risers',(.43,.46,.48));blue=mat('human blue',(.12,.22,.34));green=mat('northern green',(.14,.28,.18));brown=mat('Elin ocher',(.48,.30,.13));skin=mat('heads',(.67,.48,.34));linen=mat('covering cloth',(.52,.50,.44));dark=mat('boots',(.12,.10,.08));tessa=mat('Tessa blue gray',(.26,.28,.33));red=mat('Olan auburn',(.43,.22,.10))
def cube(n,loc,size,ma):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(ma);return o
def ell(n,loc,scale,ma):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=1,location=loc);o=bpy.context.object;o.name=n;o.scale=scale;o.data.materials.append(ma);bpy.ops.object.shade_smooth();return o
def seg(n,a,b,r,ma):
 v=Vector(b)-Vector(a);mid=(Vector(a)+Vector(b))/2;bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=v.length,location=mid);o=bpy.context.object;o.name=n;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(ma);return o
Z=1.7
cube('one rectangular landing',(2.5,1.6,Z/2),(5,3.2,Z),floor)
# One narrow incoming flight. Exactly10 equal17cm risers and30cm treads.
for i in range(10):
 h=(i+1)*.17;y=-3+(i+.5)*.3
 cube('incoming step %02d'%i,(3.5,y,h/2),(1.8,.3,h),step)
# One perpendicular upper flight leaves east edge; exactly10 equal risers.
for i in range(10):
 h=Z+(i+1)*.17;x=5+(i+.5)*.3
 cube('upper step %02d'%i,(x,2.25,h/2),(.3,1.8,h),step)
cube('back wall',(2.5,3.35,3.15),(5,.3,2.9),stone)
cube('left parapet',(-.12,1.6,2.025),(.24,3.2,.65),stone)
cube('rear bay return pier',(2.35,3.07,3.10),(.35,.5,2.8),stone)
# Rails outside the stair treads, not additional steps.
for x in [2.5,4.5]:
 for y in [-2.85,-1.65,-.45]:
  level=max(.17,math.ceil((y+3)/.3)*.17);seg('lower rail post',(x,y,level),(x,y,level+.85),.035,dark)
 seg('lower rail',(x,-2.85,1.02),(x,-.15,2.55),.04,dark)
cube('upper side wall',(6.5,3.3,2.7),(3,.3,3),stone)
# Body helpers with exact adult height, natural human proportions.
def standing(n,x,y,z,h,ma,face=(0,1),stop=False):
 scale=h/1.78
 # local coordinates face along vector; x-right vector perpendicular
 f=Vector((face[0],face[1],0)).normalized();r=Vector((f.y,-f.x,0));origin=Vector((x,y,z))
 def P(a,b,c):return tuple(origin+r*a*scale+f*b*scale+Vector((0,0,c*scale)))
 for side in [-1,1]:
  foot=P(side*.12,.06,.065);ob=cube(n+' boot',foot,(.14*scale,.29*scale,.13*scale),dark);ob.rotation_euler.z=math.atan2(-f.x,f.y)
  seg(n+' calf',P(side*.12,0,.14),P(side*.13,0,.48),.085*scale,ma)
  seg(n+' thigh',P(side*.13,0,.48),P(side*.14,0,.9),.10*scale,ma)
 ob=cube(n+' torso',P(0,0,1.18),(.43*scale,.25*scale,.60*scale),ma);ob.rotation_euler.z=math.atan2(-f.x,f.y)
 ell(n+' head',P(0,0,1.63),(.12*scale,.12*scale,.15*scale),red if n=='Olan' else skin)
 for side in [-1,1]:
  sh=P(side*.25,0,1.4);el=P(side*.30,.05,1.1);wr=P(side*.30,.05,.88)
  if stop and side==-1: el=P(side*.32,.24,1.27);wr=P(side*.32,.48,1.48)
  seg(n+' upper arm',sh,el,.075*scale,ma);seg(n+' forearm',el,wr,.065*scale,ma);ell(n+' hand',wr,(.055*scale,.04*scale,.07*scale),skin)
 if n=='Olan':
  ob=ell('RIGHT shield',P(.34,.05,1.08),(.07,.28,.44),dark);ob.rotation_euler.z=math.atan2(-f.x,f.y)
 if n=='Lucan':
  seg('LEFT arm protects ribs',P(-.29,.02,1.09),P(.05,.17,1.08),.065,linen)
 return origin
# Grief group in protected west recess, all on same level floor.
# Mara lies north/south, with natural1.76m body and 42cm shoulders.
mx,my=1.35,2.14
ell('Mara head',(mx,my+.65,Z+.20),(.12,.145,.12),skin)
cube('Mara torso',(mx,my+.22,Z+.17),(.43,.58,.24),blue)
for s in [-1,1]:
 seg('Mara upper leg',(mx+s*.11,my-.08,Z+.16),(mx+s*.11,my-.50,Z+.14),.095,blue)
 seg('Mara lower leg',(mx+s*.11,my-.50,Z+.14),(mx+s*.11,my-.90,Z+.13),.075,dark)
 cube('Mara boot',(mx+s*.11,my-1.0,Z+.13),(.15,.24,.18),dark)
 seg('Mara arm',(mx+s*.25,my+.42,Z+.18),(mx+s*.28,my-.02,Z+.16),.06,blue)
def kneel(n,x,y,z,ma,h=1.78):
 scale=h/1.78
 ell(n+' knees',(x,y-.10,z+.12),(.22*scale,.18*scale,.12*scale),ma)
 seg(n+' thigh',(x,y-.10,z+.15),(x,y+.18,z+.47),.13*scale,ma)
 cube(n+' trunk',(x,y+.13,z+.76),(.40*scale,.25*scale,.62*scale),ma)
 ell(n+' head',(x,y+.17,z+1.15),(.12*scale,.12*scale,.15*scale),skin)
 seg(n+' arm',(x+.21,y+.08,z+.99),(x+.30,y-.11,z+.72),.065,ma)
 seg(n+' arm',(x-.21,y+.08,z+.99),(x-.24,y-.08,z+.69),.065,ma)
kneel('Tessa',.79,2.2,Z,tessa,1.65)
kneel('Elin',.36,2.45,Z,brown,1.60)
kneel('Healer',1.98,1.45,Z,blue)
standing('Olan',3.50,1.15,Z,1.75,blue,(0,-1),True)
standing('Lucan',3.52,-.16,1.70,1.85,green,(0,1))
for n,x,y,h,ma in [('North1',3.05,-.77,1.78,green),('Human1',3.95,-.77,1.76,blue),('North2',3.05,-1.52,1.80,green),('Human2',3.95,-1.52,1.77,blue)]:
 level=math.ceil((y+3)/.3)*.17;standing(n,x,y,level,h,ma,(0,1))
# Open environment beyond citadel sides; neutral studio daylight for geometry assessment.
cube('ground',(3,-1,-.18),(40,40,.3),stone)
world=bpy.context.scene.world;world.color=(.55,.55,.55)
bpy.ops.object.light_add(type='AREA',location=(-3,-4,11));bpy.context.object.data.energy=1700;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=8
bpy.ops.object.camera_add(location=(-8,-9,7.5));cam=bpy.context.object;target=Vector((2.7,.7,2.35));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='PERSP';cam.data.lens=55;bpy.context.scene.camera=cam
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=24;sc.cycles.use_denoising=False;sc.render.resolution_x=1600;sc.render.resolution_y=900;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.filepath='/tmp/s055-geometry-blockout.png'
sc.view_settings.view_transform='Standard';sc.view_settings.look='Medium High Contrast' if 'Medium High Contrast' in [i.name for i in sc.view_settings.bl_rna.properties['look'].enum_items] else sc.view_settings.look
bpy.ops.wm.save_as_mainfile(filepath='/tmp/s055-geometry-blockout.blend');bpy.ops.render.render(write_still=True)
