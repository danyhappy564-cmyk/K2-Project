import bpy, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Assets-Local/K2C3/Work'
TARGET=OUT/'K2C3-components-v002.blend'
if TARGET.exists(): raise RuntimeError('Output already exists')
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'Assets-Local/K2C3/scene.gltf'),merge_vertices=False)
source=[o for o in bpy.context.scene.objects if o.type=='MESH']
original=bpy.data.collections.new('00_ORIGINAL_reference')
bpy.context.scene.collection.children.link(original)
parts=bpy.data.collections.new('01_COMPONENTS_212')
bpy.context.scene.collection.children.link(parts)
report=[]
for ob in source:
    me=ob.data
    parent=list(range(len(me.vertices)))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]]; i=parent[i]
        return i
    def union(a,b): parent[find(a)]=find(b)
    seen={}
    for v in me.vertices:
        key=tuple(round(x,7) for x in v.co)
        if key in seen: union(v.index,seen[key])
        else: seen[key]=v.index
    for p in me.polygons:
        for vi in p.vertices[1:]: union(p.vertices[0],vi)
    groups={}
    for p in me.polygons: groups.setdefault(find(p.vertices[0]),[]).append(p)
    normals=[tuple(n.vector) for n in me.corner_normals]
    for polys in groups.values():
        old_ids=sorted({vi for p in polys for vi in p.vertices})
        remap={vi:i for i,vi in enumerate(old_ids)}
        mesh=bpy.data.meshes.new('component_mesh')
        mesh.from_pydata([me.vertices[i].co for i in old_ids],[],[[remap[v] for v in p.vertices] for p in polys])
        for mat in me.materials: mesh.materials.append(mat)
        for dst,src in zip(mesh.polygons,polys):
            dst.material_index=src.material_index
            dst.use_smooth=src.use_smooth
        src_loops=[li for p in polys for li in p.loop_indices]
        for layer in me.uv_layers:
            uv=mesh.uv_layers.new(name=layer.name)
            for li,orig_li in enumerate(src_loops): uv.data[li].uv=layer.data[orig_li].uv
        mesh.normals_split_custom_set([normals[i] for i in src_loops])
        obj=bpy.data.objects.new('component',mesh)
        parts.objects.link(obj)
        obj.matrix_world=ob.matrix_world.copy()
        coords=[obj.matrix_world @ v.co for v in mesh.vertices]
        low=[min(v[i] for v in coords) for i in range(3)]
        high=[max(v[i] for v in coords) for i in range(3)]
        mesh.calc_loop_triangles()
        report.append((obj,dict(triangles=len(mesh.loop_triangles),min=low,max=high,center=[(a+b)/2 for a,b in zip(low,high)])))
    for col in list(ob.users_collection): col.objects.unlink(ob)
    original.objects.link(ob)
original.hide_viewport=True
original.hide_render=True
report.sort(key=lambda item: tuple(item[1]['center'])+(item[1]['triangles'],))
for i,(obj,r) in enumerate(report):
    obj.name=f'K2C3_part_{i:03d}'
    r['name']=obj.name
    obj['source_part_id']=i
    obj['classification']='Unreviewed'
lo=Vector([min(r['min'][i] for _,r in report) for i in range(3)])
hi=Vector([max(r['max'][i] for _,r in report) for i in range(3)])
center=(lo+hi)/2
extent=hi-lo
assert len(report)==212,len(report)
audit={'components':[r for _,r in report],'bounds':[list(lo),list(hi)],'triangles':sum(r['triangles'] for _,r in report),'parts':len(report)}
(OUT/'components-v002.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.samples=24
scene.render.resolution_x=1500
scene.render.resolution_y=700
scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Studio')
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0.20,0.20,0.20,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=0.7
camera_data=bpy.data.cameras.new('ReviewCamera')
camera=bpy.data.objects.new('ReviewCamera',camera_data)
scene.collection.objects.link(camera)
camera.location=center+Vector((0,-extent.x*1.7,extent.z*0.15))
camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
camera_data.type='ORTHO'
camera_data.ortho_scale=extent.x*1.15
scene.camera=camera
for name,offset,power,size in [('Key',(0,-4,5),1500,5),('Fill',(1,3,3),1100,4)]:
    data=bpy.data.lights.new(name,'AREA'); data.energy=power; data.shape='DISK';data.size=size
    light=bpy.data.objects.new(name,data);scene.collection.objects.link(light)
    light.location=center+Vector(offset)
    light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.select_all(action='DESELECT')
for obj,_ in report: obj.select_set(True)
bpy.context.view_layer.objects.active=report[0][0]
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            space=area.spaces.active
            space.region_3d.view_location=center
            space.region_3d.view_distance=extent.x*1.1
            space.region_3d.view_rotation=camera.rotation_euler.to_quaternion()
            space.shading.type='MATERIAL'
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(TARGET))
scene.render.filepath=str(OUT/'K2C3-side.png')
bpy.ops.render.render(write_still=True)
print('COMPONENTS_READY',len(report),audit['triangles'],list(extent))
