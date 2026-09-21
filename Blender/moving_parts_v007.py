"""MCP visual review correction and clearly marked, non-EFT preview action."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
folder=Path(bpy.data.filepath).parent
out=folder/'K2C3-moving-review-v007.blend'
if out.exists():raise RuntimeError('Output exists')
scene=bpy.context.scene;rig=bpy.data.objects['K2C3_DraftRig']
parts=[o for o in scene.objects if o.name.startswith('K2C3_part_')]
for o in parts:o.hide_set(False)
def coords():
    bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
    return {o.name:[o.evaluated_get(dg).matrix_world@v.co for v in o.evaluated_get(dg).data.vertices] for o in parts}
before=coords()
bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig
bpy.ops.object.mode_set(mode='EDIT')
b=rig.data.edit_bones.new('weapon_bolt')
o=bpy.data.objects['K2C3_part_165']
world=[o.matrix_world@v.co for v in o.data.vertices]
center=sum(world,Vector())/len(world)
b.head=rig.matrix_world.inverted()@center;b.tail=b.head+Vector((.2,0,0))
b.parent=rig.data.edit_bones['weapon']
rig.data.edit_bones['mod_charge'].parent=b
bpy.ops.object.mode_set(mode='OBJECT')
root=bpy.data.collections['01_COMPONENTS_212']
def classify(i,name,binding,status):
    o=bpy.data.objects[f'K2C3_part_{i:03d}']
    for g in list(o.vertex_groups):o.vertex_groups.remove(g)
    g=o.vertex_groups.new(name=binding);g.add(list(range(len(o.data.vertices))),1,'REPLACE')
    col=bpy.data.collections.get(name)
    if not col:col=bpy.data.collections.new(name);root.children.link(col)
    for old in list(o.users_collection):old.objects.unlink(o)
    col.objects.link(o)
    o['draft_binding']=binding;o['classification']=name;o['review_status']=status
classify(165,'16_노리쇠몸체_형상후보','weapon_bolt','MCP 원통형 몸체 확인. 실제 작동/충돌/스트로크 미확정')
classify(159,'09_장전손잡이_후보','mod_charge','MCP 손잡이 연결부 후보. 조립체 이동 검사 대상')
classify(187,'17_배출구테두리_형상후보','weapon','MCP 얇은 테두리 확인. 노리쇠 후보 분류 철회; 정적 유지')
after=coords()
rest=max((a-b).length for n in before for a,b in zip(before[n],after[n]))
assert rest<1e-5,rest
scale=rig.matrix_world.to_scale().x
tests=[]
for name,expected,mode in [('weapon_bolt',{159,160,165},'slide'),('weapon_trigger',{192},'rotate')]:
    p=rig.pose.bones[name];p.rotation_mode='XYZ'
    if mode=='slide':p.location.y=.015/scale
    else:p.rotation_euler.z=math.radians(8)
    posed=coords()
    changed={int(n.rsplit('_',1)[1]) for n in after if max((a-b).length for a,b in zip(after[n],posed[n]))>1e-5}
    assert changed==expected,(name,changed)
    tests.append({'bone':name,'changed_parts':sorted(changed),'mode':mode,'pass':True})
    p.location=(0,0,0);p.rotation_euler=(0,0,0)
    bpy.context.view_layer.update()
# Explicit preview only, never export as production firing or reload animation.
for frame,amount in [(1,0),(10,1),(20,0)]:
    scene.frame_set(frame)
    p=rig.pose.bones['weapon_bolt'];p.location.y=.015/scale*amount;p.keyframe_insert(data_path='location',frame=frame)
    t=rig.pose.bones['weapon_trigger'];t.rotation_euler.z=math.radians(8)*amount;t.keyframe_insert(data_path='rotation_euler',frame=frame)
rig.animation_data.action.name='PREVIEW_ONLY_15mm_8deg_NOT_EFT'
scene.frame_start=1;scene.frame_end=20;scene.frame_set(1)
final=coords()
assert max((a-b).length for n in after for a,b in zip(after[n],final[n]))<1e-5
rig['bolt_status']='165 visual body candidate; 159/160 handle group. 187 static edge. Not confirmed by in-game animation.'
rig['preview_warning']='15 mm slide and 8 degree trigger rotation are arbitrary visual tests, not game/real-world specifications.'
scene['stage']='v007 corrected moving-part candidates + preview animation; full EFT rig still pending'
for a in bpy.context.screen.areas:
    if a.type=='VIEW_3D':
        s=a.spaces.active;s.shading.type='MATERIAL';s.overlay.show_overlays=False
        s.region_3d.view_location=Vector((0,-.13,-.03));s.region_3d.view_distance=1.1
        s.region_3d.view_rotation=Vector((1,0,-.1)).to_track_quat('-Z','Y')
report={'bones':len(rig.data.bones),'rest_error':rest,'tests':tests,'unclassified':len(bpy.data.collections['99_추가검토_소형부품'].objects),'preview_only':True}
(folder/'moving-v007-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(out))
print(json.dumps(report))

