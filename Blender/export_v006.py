"""Live MCP: provisional metric calibration and FBX handoff, not EFT-ready."""
import bpy,json,math
from pathlib import Path
from mathutils import Matrix,Vector
folder=Path(bpy.data.filepath).parent
target=folder/'K2C3-metric-draft-v006.blend'
fbx=folder/'K2C3-metric-draft-v006.fbx'
assert not target.exists() and not fbx.exists(),'Output exists'
parts=[o for o in bpy.context.scene.objects if o.name.startswith('K2C3_part_')]
rig=bpy.data.objects['K2C3_DraftRig']
assert len(parts)==212
barrel=bpy.data.objects['K2C3_part_009']
points=[barrel.matrix_world@v.co for v in barrel.data.vertices]
low=min(v.x for v in points);high=max(v.x for v in points)
scale=0.465/(high-low)
anchor=Vector((0.09,0,(min(v.z for v in points)+max(v.z for v in points))/2))
transform=Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Diagonal((scale,scale,scale,1))@Matrix.Translation(-anchor)
bpy.context.view_layer.update()
dg=bpy.context.evaluated_depsgraph_get()
before={o.name:[o.evaluated_get(dg).matrix_world@v.co for v in o.evaluated_get(dg).data.vertices] for o in parts}
# Transform both rest rig and meshes in world space; modifier evaluates the same rigid relation.
for obj in [rig]+parts:
    obj.matrix_world=transform@obj.matrix_world
bpy.context.view_layer.update()
dg=bpy.context.evaluated_depsgraph_get()
after={o.name:[o.evaluated_get(dg).matrix_world@v.co for v in o.evaluated_get(dg).data.vertices] for o in parts}
error=max((transform@a-b).length for n in before for a,b in zip(before[n],after[n]))
assert error<1e-5,error
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1.0
rig['scale_basis']='PROVISIONAL: part_009 X extent mapped to README 465 mm. Real chamber-to-muzzle measurement unverified.'
rig['axis_basis']='Blender muzzle -Y, up +Z; FBX export -Z forward, Y up'
rig['scale_factor']=scale
for o in parts:
    # Standard FBX skin hierarchy needs mesh objects parented to armature.
    world=o.matrix_world.copy();o.parent=rig;o.matrix_world=world
    o.hide_set(False)
bpy.context.view_layer.update()
# Keep donor/raw reference off, and frame only the metric working model.
for o in scene.objects:
    if o.type in {'CAMERA','LIGHT','EMPTY'}: o.hide_set(True)
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        s=area.spaces.active;s.region_3d.view_location=Vector((0,-0.13,-0.03));s.region_3d.view_distance=1.1
        s.region_3d.view_rotation=Vector((-1,0,-0.12)).to_track_quat('-Z','Y')
        s.shading.type='MATERIAL';s.overlay.show_overlays=True
bpy.ops.object.select_all(action='DESELECT')
for o in [rig]+parts:o.select_set(True)
bpy.context.view_layer.objects.active=rig
bpy.ops.export_scene.fbx(filepath=str(fbx),use_selection=True,object_types={'ARMATURE','MESH'},
    add_leaf_bones=False,bake_anim=False,use_armature_deform_only=True,
    axis_forward='-Z',axis_up='Y',apply_unit_scale=True,path_mode='COPY',embed_textures=True)
coords=[v for vertices in after.values() for v in vertices]
bounds=[[min(v[i] for v in coords) for i in range(3)],[max(v[i] for v in coords) for i in range(3)]]
report={'scale_factor':scale,'basis':'provisional barrel mesh extent 465mm','bounds_m':bounds,
        'max_transform_error':error,'meshes':len(parts),'bones':len(rig.data.bones),
        'expected_vertices':sum(len(o.data.vertices) for o in parts),'expected_polygons':sum(len(o.data.polygons) for o in parts),
        'fbx':str(fbx),'eft_ready':False}
(folder/'metric-v006-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
scene['stage']='v006 provisional metric rig and FBX handoff. No EFT-ready prefab or animation.'
bpy.ops.wm.save_as_mainfile(filepath=str(target))
print(json.dumps(report))
