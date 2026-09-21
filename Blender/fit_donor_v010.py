"""MCP-only preview: attach a copy of K2 to the sampled donor weapon."""
import bpy, json
from pathlib import Path
from mathutils import Matrix, Vector

folder = Path(bpy.data.filepath).parent
target = folder / 'K2C3-donor-fit-v010.blend'
assert not target.exists(), 'Keep existing checkpoints intact'
source = bpy.data.scenes['Scene']
scene = bpy.data.scenes['EFT_DONOR_reload_charge']
bpy.context.window.scene = scene
scene.frame_set(1)
bpy.context.view_layer.update()
original = source.objects['K2C3_DraftRig']
weapon = scene.objects['SRC.weapon']
trigger = scene.objects['SRC.weapon_trigger']
k2_trigger = original.matrix_world @ original.data.bones['weapon_trigger'].head_local
donor_trigger = weapon.matrix_world.inverted() @ trigger.matrix_world.translation
offset = donor_trigger - k2_trigger
collection = bpy.data.collections.new('K2_DONOR_FIT_PREVIEW')
scene.collection.children.link(collection)
rig = original.copy()
rig.data = original.data.copy()
rig.name = 'K2C3_DonorFitRig'
rig.animation_data_clear()
collection.objects.link(rig)
for bone in rig.pose.bones:
    bone.matrix_basis = Matrix.Identity(4)
rig.parent = weapon
rig.matrix_parent_inverse = Matrix.Identity(4)
rig.matrix_basis = Matrix.Translation(offset) @ original.matrix_world
rig['alignment'] = 'Provisional: trigger point only; no hand IK or production retarget'
copies = []
for obj in source.objects:
    if obj.type != 'MESH' or not obj.name.startswith('K2C3_part_'):
        continue
    clone = obj.copy()
    clone.data = obj.data.copy()
    clone.name = 'FIT.' + obj.name
    collection.objects.link(clone)
    clone.parent = rig
    clone.matrix_parent_inverse = obj.matrix_parent_inverse.copy()
    clone.matrix_basis = obj.matrix_basis.copy()
    for modifier in clone.modifiers:
        if modifier.type == 'ARMATURE' and modifier.object == original:
            modifier.object = rig
    copies.append(clone)
assert len(copies) == 212
assert sum(len(o.data.polygons) for o in copies) == 12732
samples = {}
for frame in (1, 23, 46):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    actual = rig.matrix_world @ rig.data.bones['weapon_trigger'].head_local
    expected = weapon.matrix_world @ donor_trigger
    assert (actual - expected).length < 1e-5
    samples[frame] = {'trigger_anchor': list(actual), 'weapon_position': list(weapon.matrix_world.translation)}
    for name in ('Base HumanLPalm', 'Base HumanRPalm'):
        samples[frame][name] = list(scene.objects['SRC.' + name].matrix_world.translation)
scene.frame_set(1)
bpy.context.view_layer.update()
for obj in scene.objects:
    obj.select_set(False)
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
center = weapon.matrix_world @ (offset + Vector((0, -.1, 0)))
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        space = area.spaces.active
        space.shading.type = 'MATERIAL'
        space.region_3d.view_location = center
        space.region_3d.view_distance = 1.35
        # View along donor weapon local X, keeping local Z upright.
        basis = weapon.matrix_world.to_quaternion()
        space.region_3d.view_rotation = basis @ Vector((1, -.25, .25)).to_track_quat('Z', 'Y')
scene['k2_fit_limit'] = 'Trigger-anchor translation only. K2 moving parts neutral. No runtime IK, skin or full reload cycle.'
report = {'mesh_count': len(copies), 'triangles': 12732, 'offset_weapon_local': list(offset), 'samples': samples,
          'limits': scene['k2_fit_limit'], 'source_file': str(folder / 'K2C3-with-donor-reload-v009.blend')}
(folder / 'donor-fit-v010-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(target))
print('SAVED', target, '212 meshes; anchor checks passed at frames 1,23,46')
