import bpy, math
from mathutils import Vector
from pathlib import Path
out=Path('/home/kir/Documents/Projects/the-ending-we-never-got/visual-novel/art/scene-studies/s054-duel/batch7/independent')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(name,color,alpha=1):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,alpha);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,alpha);p.inputs['Roughness'].default_value=.7;p.inputs['Alpha'].default_value=alpha
 if alpha<1:m.blend_method='BLEND';m.use_screen_refraction=True;m.show_transparent_back=False
 return m
navy=mat('Tessa blue',(0.04,.12,.25));steel=mat('Valcair grey armor',(.18,.19,.2));skin=mat('bare skin',(.47,.29,.18));glove=mat('RIGHT sword glove',(.16,.08,.035));wood=mat('spear shaft',(.25,.12,.045));blade=mat('sword steel',(.65,.70,.75));black=mat('black ward elbow',(.015,.008,.025));shell=mat('full grounded sanctuary',(.8,.9,1),.025);stone=mat('stone',(.3,.3,.32))
def ball(name,at,r,m,scale=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,radius=r,location=at);o=bpy.context.object;o.name=name;o.data.materials.append(m)
 if scale:o.scale=scale
 return o
def bone(name,a,b,r,m):
 a,b=Vector(a),Vector(b);v=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=r,depth=v.length,location=(a+b)/2);o=bpy.context.object;o.name=name;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(m);ball(name+' joint A',a,r,m);ball(name+' joint B',b,r,m);return o
# Deliberately simple blocking figures; not final anatomy or identity.
T={'hip':(-.61,0,.85),'neck':(-.45,0,1.44),'head':(-.43,0,1.64),'rs':(-.42,-.17,1.4),'re':(-.06,-.12,1.29),'rw':(.22,.12,1.28),'ls':(-.51,.16,1.4),'le':(-.60,.39,1.40),'lw':(-.42,.63,1.58),'rk':(-.83,-.33,.43),'rf':(-.89,-.58,.08),'lk':(-.2,.23,.43),'lf':(.04,.40,.08)}
bone('Tessa torso',T['hip'],T['neck'],.18,navy);ball('Tessa head',T['head'],.115,skin, (.84,.91,1.12))
for side in ['r','l']:
 bone('Tessa '+side+' upperarm',T[side+'s'],T[side+'e'],.055,navy);bone('Tessa '+side+' forearm',T[side+'e'],T[side+'w'],.045,navy);ball('Tessa '+side+' hand',T[side+'w'],.065,glove if side=='r' else skin)
 bone('Tessa '+side+' thigh',T['hip'],T[side+'k'],.09,navy);bone('Tessa '+side+' lowerleg',T[side+'k'],T[side+'f'],.065,glove);ball('Tessa '+side+' boot',T[side+'f'],.09,glove,(1,1.8,.65))
V={'hip':(1.25,1.18,1.0),'neck':(1.0,1.18,1.68),'head':(.98,1.15,1.85),'ls':(.99,.95,1.56),'le':(.74,.77,1.30),'lw':(.50,1.035,1.08),'rs':(1.06,1.37,1.57),'re':(1.37,1.35,1.28),'rw':(1.10,1.035,1.08),'lk':(.81,.65,.53),'lf':(.56,.58,.08),'rk':(1.65,1.16,.55),'rf':(1.97,1.38,.08)}
bone('Valcair torso',V['hip'],V['neck'],.24,steel);ball('Valcair head',V['head'],.13,skin,(.9,1,1.1))
for side in ['l','r']:
 bone('Valcair '+side+' upperarm',V[side+'s'],V[side+'e'],.08,steel);bone('Valcair '+side+' forearm',V[side+'e'],V[side+'w'],.065,steel);ball('Valcair '+side+' gripping hand',V[side+'w'],.07,skin)
 bone('Valcair '+side+' thigh',V['hip'],V[side+'k'],.12,steel);bone('Valcair '+side+' shin',V[side+'k'],V[side+'f'],.085,steel);ball('Valcair '+side+' boot',V[side+'f'],.12,steel,(1,1.7,.65))
# One straight spear tangent to the FAR waist-height cross-section of the dome.
bone('single continuous wooden spear shaft',(-1.57,1.035,1.08),(2.03,1.035,1.08),.025,wood)
bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=.065,radius2=0,depth=.33,location=(-1.735,1.035,1.08));o=bpy.context.object;o.name='spear point in column';o.rotation_euler=(0,-math.pi/2,0);o.data.materials.append(blade)
# 1.04 m hand-to-tip arming sword; outer blade makes elbow contact with tip remaining beyond.
hand=Vector(T['rw']);contact=Vector((.74,.77,1.37));direction=(contact-hand).normalized();base=hand+direction*.13;tip=hand+direction*1.04
bone('RIGHT gloved hand sword handle',hand-direction*.075,hand+direction*.105,.025,glove)
bone('sword crossguard',hand+direction*.13+Vector((0,0,-.11)),hand+direction*.13+Vector((0,0,.11)),.015,blade)
width=Vector((0,0,.026));thick=Vector((direction.y,-direction.x,0))*.004
verts=[tuple(base+width+thick),tuple(base-width+thick),tuple(tip+thick),tuple(base+width-thick),tuple(base-width-thick),tuple(tip-thick)]
mesh=bpy.data.meshes.new('blade');mesh.from_pydata(verts,[],[(0,1,2),(5,4,3),(0,3,4,1),(0,2,5,3),(1,4,5,2)]);obj=bpy.data.objects.new('sword edge cutting forward ELBOW',mesh);bpy.context.collection.objects.link(obj);obj.data.materials.append(blade)
ball('black ward at actual forward elbow',V['le'],.105,black)
# Closed hemisphere from floor to above her head, no floating disc.
verts=[];faces=[];rings=20;segments=72
for j in range(rings+1):
 a=(math.pi/2)*j/rings
 for i in range(segments):
  t=2*math.pi*i/segments;verts.append((-.6+1.2*math.cos(a)*math.cos(t),1.2*math.cos(a)*math.sin(t),2*math.sin(a)))
for j in range(rings):
 for i in range(segments):
  n=j*segments+i;faces.append((n,j*segments+(i+1)%segments,(j+1)*segments+(i+1)%segments,n+segments))
mesh=bpy.data.meshes.new('grounded shell');mesh.from_pydata(verts,[],faces);obj=bpy.data.objects.new('complete sanctuary dome',mesh);bpy.context.collection.objects.link(obj);obj.data.materials.append(shell)
bpy.ops.mesh.primitive_torus_add(major_radius=1.2,minor_radius=.012,major_segments=72,minor_segments=8,location=(-.6,0,.012));bpy.context.object.data.materials.append(blade)
bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.28,depth=3.6,location=(-2.13,1.035,1.8));bpy.context.object.name='solid impact pillar behind Tessa';bpy.context.object.data.materials.append(stone)
bpy.ops.mesh.primitive_plane_add(size=30);bpy.context.object.data.materials.append(mat('floor',(.47,.47,.47)))
# Front-left depth view, whole fighters and clear foot gap.
bpy.data.objects['Valcair torso'].scale.y=.5
bpy.data.objects['Valcair torso joint A'].scale.y=.5
bpy.data.objects['Valcair torso joint B'].scale=(.4,.4,.4)
bpy.data.objects['Tessa torso joint B'].scale=(.4,.4,.4)
bpy.ops.object.camera_add(location=(-2,-8,2.6));cam=bpy.context.object;cam.rotation_euler=(Vector((-.05,.35,1.04))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.5;bpy.context.scene.camera=cam
bpy.ops.object.light_add(type='AREA',location=(-3,-4,7));bpy.context.object.data.energy=1600;bpy.context.object.data.size=6
scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE';scene.eevee.use_gtao=True;scene.eevee.gtao_distance=3;scene.world.color=(.55,.55,.55);scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast';scene.render.image_settings.file_format='PNG';scene.render.filepath=str(out/'blocking.png');bpy.ops.wm.save_as_mainfile(filepath=str(out/'blocking.blend'));bpy.ops.render.render(write_still=True)
