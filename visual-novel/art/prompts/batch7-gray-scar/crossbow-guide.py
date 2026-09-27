import bpy, math
from mathutils import Vector
from pathlib import Path
out=Path('/home/kir/Documents/Projects/the-ending-we-never-got/visual-novel/art/scene-studies/batch7-gray-scar')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(name,c):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);return m
wood=mat('stock brown',(.25,.11,.045));steel=mat('bow limbs dark steel',(.10,.13,.16));string=mat('taut string ivory',(.82,.75,.58));bolt=mat('bolt shaft',(.5,.28,.09));silver=mat('stirrup',(.4,.43,.45))
def rod(name,a,b,r,m):
 v=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=v.length,location=(Vector(a)+Vector(b))/2);o=bpy.context.object;o.name=name;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(m)
def line(name,pts,r,m):
 for a,b in zip(pts,pts[1:]):rod(name,a,b,r,m)
def box(name,p,sc,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=name;o.scale=sc;o.data.materials.append(m)
box('ONE straight wooden stock',(0,0,0),(1.65,.11,.10),wood)
# Bow tips displaced back towards the stock butt, both arms lie in horizontal plane.
pts=[(.35,-.65,.04),(.5,-.56,.04),(.65,-.34,.04),(.69,0,.04),(.65,.34,.04),(.5,.56,.04),(.35,.65,.04)]
line('ONE transverse bow with two limbs',pts,.022,steel)
line('SINGLE connected drawn string',[(.35,-.65,.05),(-.27,0,.05),(.35,.65,.05)],.005,string)
rod('bolt along stock',(-.22,0,.085),(.91,0,.085),.009,bolt)
line('front foot stirrup',[(.75,-.075,-.02),(.98,-.12,-.02),(1.03,0,-.02),(.98,.12,-.02),(.75,.075,-.02)],.012,silver)
# Trigger below rear third.
line('trigger lever',[(-.3,0,-.03),(-.4,0,-.18),(-.52,0,-.15)],.008,steel)
bpy.ops.object.camera_add(location=(2.7,-4.2,4.0));cam=bpy.context.object;cam.rotation_euler=(Vector((.1,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=2.3;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.world.color=(.55,.55,.55);s.render.resolution_x=1000;s.render.resolution_y=700;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(out/'crossbow-structure.png');bpy.ops.wm.save_as_mainfile(filepath=str(out/'crossbow-structure.blend'));bpy.ops.render.render(write_still=True)
