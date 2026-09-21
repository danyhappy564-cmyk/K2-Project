"""Correct imported Euler order, retaining v010 as a comparison checkpoint."""
import bpy, json, math
from pathlib import Path
from mathutils import Euler, Quaternion

folder = Path(bpy.data.filepath).parent
target = folder / 'K2C3-donor-rotation-v011.blend'
assert not target.exists()
d = json.loads(Path(r'D:/SPT Dev/02_Resources/Inspection/K2-Rig/reload-charge-decoded.json').read_text())
scene = bpy.data.scenes['EFT_DONOR_reload_charge']
bpy.context.window.scene = scene
objects = {o.get('source_path'): o for o in scene.objects if o.name.startswith('SRC.')}
nodes = {n['id']: n for n in d['nodes']}
previous = {}
for frame, values in enumerate(d['frames'], 1):
    cursor = 0
    for channel in d['channels']:
        value = values[cursor:cursor + channel['width']]
        cursor += channel['width']
        if channel['attribute'] != 4:
            continue
        obj = objects[nodes[channel['node']]['path']]
        q = Euler(tuple(math.radians(x) for x in value), 'XYZ').to_quaternion()
        q = Quaternion((q.w, q.x, -q.y, -q.z))
        if obj.name in previous and previous[obj.name].dot(q) < 0:
            q.negate()
        previous[obj.name] = q.copy()
        obj.rotation_quaternion = q
        obj.keyframe_insert(data_path='rotation_quaternion', frame=frame)

distances = []
local_positions = []
for frame in range(1, 47):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    palm = scene.objects['SRC.Base HumanRPalm'].matrix_world.translation
    marker = scene.objects['SRC.weapon_R_IK_marker'].matrix_world.translation
    distances.append((palm - marker).length)
    local_positions.append(scene.objects['SRC.weapon'].matrix_world.inverted() @ palm)
drift = max((p - local_positions[0]).length for p in local_positions)
assert drift < .001, drift
assert max(distances) < .001, max(distances)
scene['rotation_order'] = 'XYZ: all 46 frames match donor right-hand IK marker within 1mm; ZXY drift was 219mm'
scene['validation_limit'] = 'XYZ validated against original right-hand marker. Unity runtime comparison and K2 contact fitting still pending.'
scene.frame_set(1)
bpy.context.view_layer.update()
report = {'rotation_order': 'XYZ', 'frames': 46, 'right_palm_weapon_local_max_drift_m': drift,
          'right_palm_to_original_marker_max_m': max(distances), 'previous_ZXY_drift_m': .21923157980665908,
          'scope': scene['validation_limit']}
(folder / 'donor-rotation-v011-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(target))
print(report)
