"""MCP-reviewed shape groups and HK416 reference markers; no IK claim."""
import bpy,json
from pathlib import Path
from mathutils import Vector
folder=Path(bpy.data.filepath).parent
out=folder/'K2C3-reference-review-v008.blend'
assert not out.exists()
parts=[o for o in bpy.context.scene.objects if o.name.startswith('K2C3_part_')]
assert len(parts)==212
root=bpy.data.collections['01_COMPONENTS_212']
groups={
 '18_전방체결부_정적후보':[7,10,11],
 '19_슬링고리_정적후보':[8,205],
 '21_총몸핀_체결부_정적후보':[151,152,153,154,206,208],
 '22_조작버튼_가동미확정':[177,180,181],
 '23_좌우조작레버_가동미확정':[199,200]}
pending=bpy.data.collections['99_추가검토_소형부품']
assert {int(o.name.rsplit('_',1)[1]) for o in pending.objects}=={i for ids in groups.values() for i in ids}
for name,ids in groups.items():
 col=bpy.data.collections.new(name);root.children.link(col)
 for i in ids:
  o=bpy.data.objects[f'K2C3_part_{i:03d}']
  for previous in list(o.users_collection):previous.objects.unlink(o)
  col.objects.link(o);o['classification']=name
  o['review_status']='MCP 번호별 형상 관찰 완료. 실제 기능/가동 여부 미확정; 정적 바인딩 유지'
pending.name='99_미분류_현재비어있음'
# These are donor-local positions aligned by trigger translation only.
# No model scaling, bone movement or IK assignment is inferred from these points.
rows=json.loads(Path(r'D:/SPT Dev/02_Resources/Inspection/K2-Rig/hk416-transforms.json').read_text())
selected=[r for r in rows if r['parent']==-2624983819621190999]
trigger=Vector(next(r['position'] for r in selected if r['name']=='weapon_trigger'))
rig=bpy.data.objects['K2C3_DraftRig'];anchor=rig.matrix_world@rig.data.bones['weapon_trigger'].head_local
refs=bpy.data.collections.new('90_REFERENCE_ONLY_HK416_손탄창')
bpy.context.scene.collection.children.link(refs)
refs.hide_render=True
names={'weapon_R_hand_marker','weapon_L_hand_marker','mod_magazine','mod_stock','mod_charge','shellport'}
report=[]
for row in selected:
 if row['name'] not in names:continue
 delta=Vector(row['position'])-trigger
 position=anchor+Vector((-delta.x,delta.y,delta.z))
 obj=bpy.data.objects.new('REF_ONLY.'+row['name'],None);refs.objects.link(obj)
 obj.location=position;obj.empty_display_type='SPHERE';obj.empty_display_size=.01;obj.show_name=True
 obj['basis']='HK416 weapon-local positions; X reflected; trigger translation aligned. Orientation NOT transferred.'
 obj['warning']='REFERENCE ONLY. Not a K2 slot or IK target. Exclude from export.'
 report.append({'name':row['name'],'reference_position':list(position),'donor_position':row['position']})
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  s=a.spaces.active;s.shading.type='MATERIAL';s.overlay.show_overlays=True
  s.region_3d.view_location=Vector((0,-.12,-.035));s.region_3d.view_distance=1.1
  s.region_3d.view_rotation=Vector((1,0,-.15)).to_track_quat('-Z','Y')
bpy.context.scene.frame_set(1)
bpy.context.scene['stage']='v008 shape groups + donor reference points; 16 parts remain functionally provisional, no K2 IK setup'
(folder/'reference-v008.json').write_text(json.dumps({'shape_groups':groups,'functionally_unconfirmed_parts':16,'donor_markers':report,'reference_only':True},ensure_ascii=False,indent=2),encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(out))
print(json.dumps({'meshes':len(parts),'shape_groups':groups,'reference_markers':len(report),'functionally_unconfirmed_parts':16},ensure_ascii=False))
