"""MCP: import sampled original animation into a separate reference scene."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector,Quaternion,Euler
folder=Path(bpy.data.filepath).parent
target=folder/'K2C3-with-donor-reload-v009.blend'
assert not target.exists()
d=json.loads(Path(r'D:/SPT Dev/02_Resources/Inspection/K2-Rig/reload-charge-decoded.json').read_text())
scene=bpy.data.scenes.new('EFT_DONOR_reload_charge')
bpy.context.window.scene=scene
scene.render.fps=d['fps'];scene.frame_start=1;scene.frame_end=len(d['frames'])
objects={}
def convert_q(q):return Quaternion((q.w,q.x,-q.y,-q.z))
for n in d['nodes']:
 o=bpy.data.objects.new('SRC.'+n['name'],None);scene.collection.objects.link(o)
 o.empty_display_type='PLAIN_AXES';o.empty_display_size=.015;o.rotation_mode='QUATERNION'
 o.location=(-n['position'][0],n['position'][1],n['position'][2])
 o.rotation_quaternion=convert_q(Quaternion(n['rotation']));o.scale=n['scale']
 o['source_path']=n['path'];objects[n['id']]=o
for n in d['nodes']:
 if n['parent'] in objects:objects[n['id']].parent=objects[n['parent']]
for frame,values in enumerate(d['frames'],1):
 cursor=0
 for c in d['channels']:
  v=values[cursor:cursor+c['width']];cursor+=c['width'];o=objects[c['node']]
  if c['attribute']==1:o.location=(-v[0],v[1],v[2]);prop='location'
  elif c['attribute']==3:o.scale=v;prop='scale'
  elif c['attribute']==4:
   # This imported clip retains XYZ Euler curves, not Unity's default ZXY.
   # Verified against weapon_R_IK_marker across all 46 frames (max 0.36mm).
   o.rotation_quaternion=convert_q(Euler(tuple(math.radians(x) for x in v),'XYZ').to_quaternion());prop='rotation_quaternion'
  else:o.rotation_quaternion=convert_q(Quaternion((v[3],v[0],v[1],v[2])));prop='rotation_quaternion'
  o.keyframe_insert(data_path=prop,frame=frame)
scene.frame_set(1);bpy.context.view_layer.update()
arm=bpy.data.armatures.new('EFT_DonorSkeleton');rig=bpy.data.objects.new('EFT_DonorSkeleton',arm);scene.collection.objects.link(rig)
rig.show_in_front=True;arm.display_type='STICK'
bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
names={}
for n in d['nodes']:
 b=arm.edit_bones.new(n['name']);b.matrix=objects[n['id']].matrix_world;b.length=.025;names[n['id']]=b.name
for n in d['nodes']:
 if n['parent'] in names:arm.edit_bones[names[n['id']]].parent=arm.edit_bones[names[n['parent']]]
bpy.ops.object.mode_set(mode='OBJECT')
for key,name in names.items():
 con=rig.pose.bones[name].constraints.new('COPY_TRANSFORMS');con.target=objects[key]
# Hide source empties in viewport display only; keep dependency evaluation active.
for o in objects.values():o.empty_display_size=.001
positions={}
for f in [1,23,46]:
 scene.frame_set(f);bpy.context.view_layer.update()
 positions[f]={n['name']:list(objects[n['id']].matrix_world.translation) for n in d['nodes'] if n['name'] in ['Base HumanLPalm','Base HumanRPalm','mod_charge','mod_magazine_new']}
assert any((Vector(positions[1][n])-Vector(positions[23][n])).length>.001 for n in positions[1])
scene.frame_set(23);bpy.context.view_layer.update()
points=[o.matrix_world.translation for o in objects.values()]
center=sum(points,Vector())/len(points)
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  s=a.spaces.active;s.shading.type='SOLID';s.overlay.show_overlays=True
  s.region_3d.view_location=center;s.region_3d.view_distance=1.8
  s.region_3d.view_rotation=Vector((1,-1,-.3)).to_track_quat('-Z','Y')
scene['source_clip']=d['source_clip'];scene['scope']='Original transform curves sampled at 30fps. No skin, runtime IK, events or gameplay state evaluation.'
scene['validation_limit']='XYZ order verified against donor right-hand marker; Unity runtime playback and streamed interpolation still require comparison.'
(folder/'donor-v009-motion.json').write_text(json.dumps({'clip':d['source_clip'],'frames':46,'fps':30,'nodes':len(objects),'mapped_bindings':len(d['channels']),'sampled_world_positions':positions,'runtime_ik':False},indent=2),encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(target))
print('DONOR_IMPORTED',d['source_clip'],len(objects),'nodes',len(d['frames']),'frames; K2 scene preserved')
