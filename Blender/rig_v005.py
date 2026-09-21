"""MCP-run rigid draft rig. NOT an EFT-ready rig or calibrated animation."""
import bpy, json, math
from pathlib import Path
from mathutils import Vector
out=Path(bpy.data.filepath).parent/'K2C3-rig-draft-v005.blend'
if out.exists(): raise RuntimeError('Output exists')
parts=[o for o in bpy.context.scene.objects if o.name.startswith('K2C3_part_')]
assert len(parts)==212 and not any(o.type=='ARMATURE' for o in bpy.context.scene.objects)
for o in parts: o.hide_set(False)
bpy.context.view_layer.update()
def evaluated():
    dg=bpy.context.evaluated_depsgraph_get()
    return {o.name:[o.evaluated_get(dg).matrix_world@v.co for v in o.evaluated_get(dg).data.vertices] for o in parts}
baseline=evaluated()
collection=bpy.data.collections.new('20_RIG_DRAFT_試作')
bpy.context.scene.collection.children.link(collection)
data=bpy.data.armatures.new('K2C3_DraftRig')
rig=bpy.data.objects.new('K2C3_DraftRig',data);collection.objects.link(rig)
rig.show_in_front=True;data.display_type='STICK'
bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig
bpy.ops.object.mode_set(mode='EDIT')
def bone(name,head,tail,parent=None):
    b=data.edit_bones.new(name);b.head=head;b.tail=tail
    if parent: b.parent=data.edit_bones[parent]
bone('weapon',(-0.1,0,1.5),(-0.1,0,1.75))
bone('weapon_trigger',(0.09,0,1.17),(0.09,0,1.02),'weapon')
bone('mod_charge',(-0.69,0.14,1.59),(-0.49,0.14,1.59),'weapon')
bone('mod_stock',(1.76,0,1.5),(2.25,0,1.5),'weapon')
bpy.ops.object.mode_set(mode='OBJECT')
mapping={192:'weapon_trigger',160:'mod_charge',210:'mod_stock',211:'mod_stock'}
for o in parts:
    i=int(o.name.rsplit('_',1)[1]);name=mapping.get(i,'weapon')
    group=o.vertex_groups.new(name=name);group.add(list(range(len(o.data.vertices))),1.0,'REPLACE')
    mod=o.modifiers.new('K2C3_DraftRigidBinding','ARMATURE');mod.object=rig
    o['draft_binding']=name
    if i in {159,165,168,187}: o['rig_review']='Unconfirmed moving geometry: bound to static root pending review'
bpy.context.view_layer.update()
after=evaluated()
rest_error=max((a-b).length for n in baseline for a,b in zip(baseline[n],after[n]))
assert rest_error<1e-5,rest_error
tests=[]
for name,expected in [('weapon_trigger',{192}),('mod_charge',{160}),('mod_stock',{210,211})]:
    pose=rig.pose.bones[name];pose.location.y=0.03
    bpy.context.view_layer.update();posed=evaluated()
    changed={int(o.name.rsplit('_',1)[1]) for o in parts if max((a-b).length for a,b in zip(after[o.name],posed[o.name]))>1e-5}
    pose.location=(0,0,0);bpy.context.view_layer.update()
    assert changed==expected,(name,changed)
    tests.append({'bone':name,'moved_parts':sorted(changed),'pass':True})
# Preserve unconfirmed pieces in a visibly provisional collection rather than claiming identification.
pending=bpy.data.collections['99_추가검토_소형부품']
for o in pending.objects:
    i=int(o.name.rsplit('_',1)[1])
    o['review_region']='전방 고정부' if i in {7,8,10,11} else '총몸 핀/레버/연결부'
    o['review_status']='MCP 양측 형상 확인. 개별 기능/가동 여부 미확정; 시험 리그에서는 정적 루트 유지'
rig['warning']='시험용 리그. 피벗은 형상 기반 근사값, 미터 단위/손 IK/Unity 애니메이션 호환 미검증.'
rig['reference']='HK416 local bundle: weapon, weapon_trigger, mod_charge, mod_stock. Names only; transforms not copied.'
rig['bolt_status']='weapon_bolt binding deferred: K2 internal bolt geometry not confirmed'
bpy.context.scene['stage']='v005: rigid draft binding and isolated-motion tests passed; EFT integration pending'
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        s=area.spaces.active;s.shading.type='MATERIAL';s.overlay.show_overlays=True
        s.region_3d.view_location=Vector((-0.87,0,1.25));s.region_3d.view_distance=7.5
        s.region_3d.view_rotation=Vector((0,-1,-0.12)).to_track_quat('-Z','Y')
report={'parts':212,'bones':4,'rest_max_error':rest_error,'motion_tests':tests,'unconfirmed_small_parts':len(pending.objects),'production_ready':False}
(out.parent/'rig-v005-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(out))
print(json.dumps(report,ensure_ascii=False))
