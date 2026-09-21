"""Preview-only donor charge motion and two-link left-arm retarget.

Keeps shoulder and right arm fixed; retains donor finger and wrist orientation.
This preserves the donor hand-to-anchor offset, not verified K2 surface contact.
"""
import bpy, json, math
from pathlib import Path
from mathutils import Vector, Matrix

folder = Path(bpy.data.filepath).parent
target = folder / 'K2C3-charge-retarget-v012.blend'
assert not target.exists()
scene = bpy.data.scenes['EFT_DONOR_reload_charge']
bpy.context.window.scene = scene
rig = scene.objects['K2C3_DonorFitRig']
weapon = scene.objects['SRC.weapon']
charge = scene.objects['SRC.mod_charge']
upper = scene.objects['SRC.Base HumanLUpperarm']
fore = scene.objects['SRC.Base HumanLForearm1']
palm = scene.objects['SRC.Base HumanLPalm']
right = scene.objects['SRC.Base HumanRPalm']
samples = []
for frame in range(1, 47):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    inv = weapon.matrix_world.inverted()
    samples.append(dict(weapon=weapon.matrix_world.copy(), charge=inv @ charge.matrix_world.translation,
                        shoulder=upper.matrix_world.translation.copy(), elbow=fore.matrix_world.translation.copy(),
                        wrist=palm.matrix_world.translation.copy(), wrist_q=palm.matrix_world.to_quaternion(),
                        right=right.matrix_world.translation.copy()))
scene.frame_set(1)
bpy.context.view_layer.update()
k2_anchor = weapon.matrix_world.inverted() @ rig.matrix_world @ rig.pose.bones['mod_charge'].head
offset = k2_anchor - samples[0]['charge']
deltas = [s['charge'] - samples[0]['charge'] for s in samples]
active = [i + 1 for i, delta in enumerate(deltas) if delta.length > .0005]
assert active
start, end = min(active), max(active)
# Map weapon-local displacement into the K2 bolt bone's local translation axes.
relative = weapon.matrix_world.inverted() @ rig.matrix_world
to_pose = (relative.to_3x3() @ rig.data.bones['weapon_bolt'].matrix_local.to_3x3()).inverted()
bolt = rig.pose.bones['weapon_bolt']
for frame, delta in enumerate(deltas, 1):
    bolt.location = to_pose @ delta
    bolt.keyframe_insert(data_path='location', frame=frame)
rig.animation_data.action.name = 'PREVIEW_DONOR_CHARGE_NOT_K2_SPEC'

# Copy actions before editing; retain original sampled actions as datablocks.
for obj in (upper, fore, palm):
    obj.animation_data.action = obj.animation_data.action.copy()
    obj.animation_data.action.name = 'K2_FIT_' + obj.name

def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def set_world_rotation(obj, q):
    # Parent scale is approximately unit; assign world rotation, key only local rotation.
    p, _, scale = obj.matrix_world.decompose()
    obj.matrix_world = Matrix.LocRotScale(p, q, scale)
    obj.keyframe_insert(data_path='rotation_quaternion', frame=scene.frame_current)
    bpy.context.view_layer.update()

results = []
for frame, sample in enumerate(samples, 1):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    weight = smooth((frame - (start - 6)) / 6) * smooth(((end + 7) - frame) / 7)
    desired = sample['wrist'] + sample['weapon'].to_3x3() @ (offset * weight)
    a = upper.matrix_world.translation.copy()
    b = fore.matrix_world.translation.copy()
    c = palm.matrix_world.translation.copy()
    l1, l2 = (b - a).length, (c - b).length
    direction = desired - a
    requested = direction.length
    direction.normalize()
    distance = max(abs(l1-l2) + 1e-6, min(requested, l1+l2-1e-6))
    reachable = a + direction * distance
    plane = b-a-direction*(b-a).dot(direction)
    if plane.length < 1e-6:
        raise RuntimeError('Degenerate elbow plane')
    plane.normalize()
    along = (l1*l1-l2*l2+distance*distance)/(2*distance)
    height = math.sqrt(max(0, l1*l1-along*along))
    elbow = a + direction*along + plane*height
    swing = (b-a).rotation_difference(elbow-a)
    set_world_rotation(upper, swing @ upper.matrix_world.to_quaternion())
    b = fore.matrix_world.translation.copy()
    c = palm.matrix_world.translation.copy()
    swing = (c-b).rotation_difference(reachable-b)
    set_world_rotation(fore, swing @ fore.matrix_world.to_quaternion())
    set_world_rotation(palm, sample['wrist_q'])
    error = (palm.matrix_world.translation-desired).length
    shoulder_error = (upper.matrix_world.translation-sample['shoulder']).length
    right_error = (right.matrix_world.translation-sample['right']).length
    charge_actual = weapon.matrix_world.inverted() @ rig.matrix_world @ rig.pose.bones['mod_charge'].head
    charge_error = (charge_actual-(k2_anchor+deltas[frame-1])).length
    assert shoulder_error < 1e-5 and right_error < 1e-5
    assert charge_error < 1e-5
    results.append(dict(frame=frame, weight=weight, wrist_target_error_m=error,
                        reach_clamp_m=abs(requested-distance), shoulder_error_m=shoulder_error,
                        right_hand_error_m=right_error, charge_transfer_error_m=charge_error))

report = dict(source='m4a1_reload_charge_0', active_frames=[start,end],
              donor_travel_m=max(v.length for v in deltas), anchor_offset_weapon_local=list(offset),
              frames=results, max_wrist_target_error_m=max(r['wrist_target_error_m'] for r in results),
              limitation='Preview: donor stroke, candidate bolt group, retained donor finger grip. K2 stroke, hand surface contact and Unity runtime not validated.')
assert report['max_wrist_target_error_m'] < .001, report['max_wrist_target_error_m']
rig['charge_retarget_limit'] = report['limitation']
scene['stage'] = 'v012 donor charge + left-arm target preview; not production animation'
scene.frame_set(18)
bpy.context.view_layer.update()
(folder/'charge-retarget-v012-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(target))
print('SAVED',target,'active',start,end,'travel',report['donor_travel_m'],'wrist error',report['max_wrist_target_error_m'])
