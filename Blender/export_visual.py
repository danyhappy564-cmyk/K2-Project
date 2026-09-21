"""Export rest geometry in native EFT weapon-local axes; no donor game assets."""
import bpy, json
from pathlib import Path
from mathutils import Matrix

root = Path(r'D:/SPT Dev/K2-Project')
out = root/'Assets-Local/UnityInput'
out.mkdir(exist_ok=True)
source = bpy.data.scenes['Scene']
rig = source.objects['K2C3_DraftRig']
fit = bpy.data.objects['K2C3_DonorFitRig']
# The fit object's basis contains the established trigger alignment in donor axes.
transform = Matrix.Diagonal((-1,1,1,1)) @ fit.matrix_basis @ rig.matrix_world.inverted()
groups = {}
for obj in source.objects:
    if not obj.name.startswith('K2C3_part_') or obj.type != 'MESH':
        continue
    mesh = obj.data
    mesh.calc_loop_triangles()
    world = transform @ obj.matrix_world
    normal_matrix = world.to_3x3().inverted().transposed()
    for tri in mesh.loop_triangles:
        material = obj.material_slots[tri.material_index].material.name
        group = groups.setdefault(material,dict(name=material,positions=[],normals=[],uv=[],indices=[]))
        for loop_id in (tri.loops[0],tri.loops[2],tri.loops[1]):
            loop = mesh.loops[loop_id]
            pos = world @ mesh.vertices[loop.vertex_index].co
            normal = (normal_matrix @ mesh.corner_normals[loop_id].vector).normalized()
            uv = mesh.uv_layers.active.data[loop_id].uv
            group['indices'].append(len(group['positions'])//3)
            group['positions'].extend(pos)
            group['normals'].extend(normal)
            group['uv'].extend(uv)
assert sum(len(g['indices'])//3 for g in groups.values()) == 12732
(out/'k2c3-visual.json').write_text(json.dumps(dict(meshes=list(groups.values()))),encoding='utf-8')
print('VISUAL_EXPORT',[(g['name'],len(g['indices'])//3) for g in groups.values()])
