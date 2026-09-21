import bpy, json
from pathlib import Path
bpy.ops.wm.read_factory_settings(use_empty=True)
root=Path(__file__).resolve().parents[1]
bpy.ops.import_scene.gltf(filepath=str(root/'Assets-Local/K2C3/scene.gltf'),merge_vertices=False)
for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
    me=ob.data
    me.calc_loop_triangles()
    print('MESH',ob.name,len(me.vertices),len(me.loop_triangles),'bounds',list(ob.dimensions))
    for precision in [7,6,5,4]:
        parent=list(range(len(me.vertices)))
        def find(i):
            while parent[i]!=i:
                parent[i]=parent[parent[i]];i=parent[i]
            return i
        def union(a,b): parent[find(a)]=find(b)
        seen={}
        for v in me.vertices:
            key=tuple(round(x,precision) for x in v.co)
            if key in seen: union(v.index,seen[key])
            else: seen[key]=v.index
        for p in me.polygons:
            for i in p.vertices[1:]: union(p.vertices[0],i)
        print('PRECISION',precision,'PARTS',len({find(p.vertices[0]) for p in me.polygons}))
