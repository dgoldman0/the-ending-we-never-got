import bpy, math
from mathutils import Vector
from pathlib import Path
out=Path('/home/kir/Documents/Projects/the-ending-we-never-got/visual-novel/art/scene-studies/s053-bend')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);return m
stone=mat('ordinary gray stone',(.36,.38,.39));blue=mat('human blue',(.10,.22,.42));green=mat('north green',(.12,.24,.13));skin=mat('skin',(.52,.32,.23));wood=mat('shield brown',(.3,.15,.06));steel=mat('steel',(.65,.7,.75))
def cube(n,p,s,ma):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.scale=s;o.data.materials.append(ma);return o
def ell(n,p,s,ma):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=12,location=p);o=bpy.context.object;o.name=n;o.scale=s;o.data.materials.append(ma);return o
def rod(n,a,b,r,ma):
 v=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=v.length,location=(Vector(a)+Vector(b))/2);o=bpy.context.object;o.name=n;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(ma);return o
# Actual ninety-degree stair turn. Lower rises north, upper rises east.
for i in range(8):
 y=-1.45+i*.34;h=(i+1)*.175;cube('lower stair tread', (0,y,h/2),(1.8,.34,h),stone)
cube('single level square turning landing',(0,2.0,.7),(1.8,1.8,1.4),stone)
for i in range(9):
 x=1.07+i*.34;h=1.4+(i+1)*.175;cube('upper stair tread',(x,2.0,h/2),(.34,1.8,h),stone)
cube('upper north wall',(1.3,3.12,2.75),(4.6,.35,5.5),stone)
# Low parapet follows outside lower flight only.
for i in range(8):
 y=-1.45+i*.34;h=(i+1)*.175;cube('left parapet',(-1.02,y,h+.40),(.22,.34,.8),stone)
# standing mannequin and specified limbs
def person(n,pos,ma,heading,arms=None):
 x,y,z=pos;f=Vector((math.cos(heading),math.sin(heading),0));L=Vector((-math.sin(heading),math.cos(heading),0));P=Vector(pos)
 hip=P+Vector((0,0,.88));ch=P+Vector((0,0,1.30));head=P+Vector((0,0,1.64));ell(n+' torso',ch,(.22,.18,.30),ma);ell(n+' hips',hip,(.20,.16,.15),ma);ell(n+' head',head,(.115,.11,.145),skin)
 for side in [-1,1]:
  foot=P+L*.17*side+f*.13*side+Vector((0,0,.08));knee=(foot+hip)/2;rod(n+' leg',hip,knee,.10,ma);rod(n+' shin',knee,foot,.075,ma);ell(n+' boot',foot,(.12,.18,.075),wood)
  shoulder=ch+L*.21*side+Vector((0,0,.10));elbow=shoulder+Vector((0,0,-.30));hand=elbow+f*.25+Vector((0,0,-.1))
  if arms and side in arms:elbow,hand=map(Vector,arms[side])
  rod(n+' upper arm',shoulder,elbow,.075,ma);rod(n+' forearm',elbow,hand,.06,ma);ell(n+' hand',hand,(.06,.06,.075),skin)
 return P
# Facing downhill (-Y): LEFT is +X; RIGHT is -X.
person('Mara',(0,1.6,1.4),blue,-math.pi/2,{1:[(.35,1.5,2.53),(.37,1.19,2.57)],-1:[(-.34,1.65,2.50),(-.45,1.34,2.46)]})
bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.40,depth=.07,location=(.37,1.07,2.62),rotation=(math.pi/2,0,0));bpy.context.object.name='Mara LEFT shield';bpy.context.object.data.materials.append(wood)
rod('Mara RIGHT sword',(-.45,1.34,2.43),(-.75,.45,2.75),.018,steel);rod('Mara guard',(-.56,1.29,2.45),(-.34,1.39,2.43),.018,steel)
person('Attacker1',(-.20,.35,1.05),green,math.pi/2,{ -1:[(.05,.53,2.15),(.26,.85,2.43)]})
rod('attacker sword',(.26,.85,2.43),(.38,1.07,2.78),.018,steel)
person('Attacker2',(-.25,-.65,.53),green,math.pi/2)
# Pair walking away, upper flight at X2.0, on adjacent depth positions.
person('helper',(2.08,1.57,2.1),blue,0,{1:[(2.15,1.87,3.50),(2.2,2.27,3.50)]})
person('wounded',(2.08,2.28,2.1),blue,0)
bpy.ops.object.camera_add(location=(-6.5,-7.2,6.1));cam=bpy.context.object;target=Vector((.70,1.30,2.25));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=7.8;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.world.color=(.65,.65,.65);s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(out/'blocking.png');bpy.ops.wm.save_as_mainfile(filepath=str(out/'blocking.blend'));bpy.ops.render.render(write_still=True)
