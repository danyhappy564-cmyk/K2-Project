"""Import K2C3, preserve materials, separate disconnected shells and report bounds."""
import bpy
import json
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'Assets-Local/K2C3/scene.gltf'
OUT = SOURCE.parent / 'Work'
OUT.mkdir(exist_ok=True)
TARGET = OUT / 'K2C3-separated-v001.blend'
if TARGET.exists():
    raise RuntimeError(f'Refusing to overwrite: {TARGET}')
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(SOURCE), merge_vertices=True)
meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
for obj in meshes:
    matrix = obj.matrix_world.copy()
    obj.parent = None
    obj.matrix_world = matrix
bpy.ops.object.select_all(action='DESELECT')
for obj in meshes:
    obj.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')
parts = [o for o in bpy.context.scene.objects if o.type == 'MESH']
records = []
for obj in parts:
    obj.data.calc_loop_triangles()
    coords = [obj.matrix_world @ v.co for v in obj.data.vertices]
    low = [min(v[i] for v in coords) for i in range(3)]
    high = [max(v[i] for v in coords) for i in range(3)]
    records.append((obj, {'triangles': len(obj.data.loop_triangles), 'min': low, 'max': high,
                         'center': [(low[i]+high[i])/2 for i in range(3)]}))
records.sort(key=lambda pair: tuple(pair[1]['center']) + (pair[1]['triangles'],))
for i, (obj, record) in enumerate(records):
    obj.name = f'K2C3_part_{i:03d}'
    obj.data.name = obj.name + '_mesh'
    record['name'] = obj.name
    record['materials'] = [m.name for m in obj.data.materials if m]
    obj['source_part_id'] = i
report = {'blender': bpy.app.version_string, 'parts': len(parts),
          'triangles': sum(r['triangles'] for _, r in records),
          'images': [{'name': im.name, 'size': list(im.size), 'path': im.filepath} for im in bpy.data.images],
          'components': [r for _,r in records]}
(OUT/'components.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(TARGET))
print('K2C3_REPORT', json.dumps({k:v for k,v in report.items() if k != 'components'}))
