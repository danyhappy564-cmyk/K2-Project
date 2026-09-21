"""Run inside the live Blender session through MCP after visual review."""
import bpy, json, hashlib
from pathlib import Path
from mathutils import Vector
out=Path(bpy.data.filepath).parent/'K2C3-working-v004.blend'
if out.exists(): raise RuntimeError('Refusing to overwrite existing v004')
parts=[o for o in bpy.context.scene.objects if o.name.startswith('K2C3_part_')]
assert len(parts)==212
def fingerprint():
    rows=[]
    for o in sorted(parts,key=lambda o:o.name):
        rows.append((o.name,[list(v.co) for v in o.data.vertices],
                     [list(p.vertices) for p in o.data.polygons],
                     [[list(v.uv) for v in uv.data] for uv in o.data.uv_layers],
                     [list(row) for row in o.matrix_world],
                     [m.name for m in o.data.materials]))
    return hashlib.sha256(json.dumps(rows).encode()).hexdigest()
before=fingerprint()
root=bpy.data.collections['01_COMPONENTS_212']
def move(obj,name,status):
    col=bpy.data.collections.get(name)
    if not col:
        col=bpy.data.collections.new(name);root.children.link(col)
    for old in list(obj.users_collection): old.objects.unlink(obj)
    col.objects.link(obj)
    obj['classification']=name;obj['review_status']=status
changed=[]
for obj in parts:
    i=int(obj.name.rsplit('_',1)[1])
    obj.data.calc_loop_triangles()
    coords=[obj.matrix_world@v.co for v in obj.data.vertices]
    if obj in list(bpy.data.collections['99_추가검토_소형부품'].objects):
        if len(obj.data.loop_triangles)==10 and min(v.z for v in coords)>1.82:
            move(obj,'04_핸드가드_상부레일','MCP: 반복 레일 이빨 형상 및 높이 확인')
        elif i in {201,202,204,207}:
            move(obj,'12_가늠자_후방조준기','MCP: 조준기 형상 확인. 회전축은 미설정')
        elif i==188:
            move(obj,'13_방아쇠울','MCP: 하부 U자 가드 형상 확인')
        elif i==192:
            move(obj,'14_방아쇠','MCP: 방아쇠 형상 확인. 피벗 미설정')
        elif i==40:
            move(obj,'15_가스튜브_후보','MCP: 총열 위 관 형상 확인. 리깅 결합 대상 미확정')
        else:
            obj['review_status']='MCP 확인: 소형 핀/레버/고정부. 개별 기능 및 가동 여부 추가 확인'
            continue
        changed.append(i)
    if i in {159,160,165,187}:
        obj['rig_status']='장전손잡이 주변 겹침 조각. EFT 본 구조와 대조 전 바인딩 금지'
for obj in parts: obj.hide_set(False)
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        s=area.spaces.active;s.overlay.show_overlays=False;s.shading.type='MATERIAL'
        s.region_3d.view_location=Vector((-0.87,0,1.25));s.region_3d.view_distance=8.5
        s.region_3d.view_rotation=Vector((0,-1,-0.12)).to_track_quat('-Z','Y')
assert before==fingerprint(),'Unexpected geometry change'
remaining=len(bpy.data.collections['99_추가검토_소형부품'].objects)
audit={'method':'live Blender MCP visual inspection','changed_part_ids':changed,
       'unclassified':remaining,'part_count':len(parts),'geometry_sha256':before,
       'geometry_unchanged':True,'rigging':'not yet bound; game reference needed'}
(out.parent/'review-v004.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
bpy.context.scene['stage']=f'MCP 부품 검토 v004. 미분류 {remaining}개. 리깅/실척/Unity 적용 전.'
bpy.ops.wm.save_as_mainfile(filepath=str(out))
print(json.dumps(audit,ensure_ascii=False))
