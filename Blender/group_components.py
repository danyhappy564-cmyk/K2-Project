"""Draft functional collections. Small uncertain pieces remain explicitly unclassified."""
import bpy,json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Assets-Local/K2C3/Work'
TARGET=OUT/'K2C3-working-v003.blend'
if TARGET.exists(): raise RuntimeError('Output already exists')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'K2C3-components-v002.blend'))
records=json.loads((OUT/'components-v002.json').read_text(encoding='utf-8'))['components']
def signature(objects):
    signatures=Counter()
    for ob in objects:
        me=ob.data
        for p in me.polygons:
            corners=[]
            for li in p.loop_indices:
                co=me.vertices[me.loops[li].vertex_index].co
                uv=me.uv_layers.active.data[li].uv
                corners.append(tuple(round(x,6) for x in (*co,*uv)))
            signatures[(me.materials[p.material_index].name,tuple(corners))]+=1
    return signatures
bpy.data.collections['00_ORIGINAL_reference'].hide_viewport=False
bpy.context.view_layer.update()
original=list(bpy.data.collections['00_ORIGINAL_reference'].objects)
split=list(bpy.data.collections['01_COMPONENTS_212'].objects)
for obj in split:
    src=next(o for o in original if o.data.materials[0]==obj.data.materials[0])
    assert max(abs(obj.matrix_world[i][j]-src.matrix_world[i][j]) for i in range(4) for j in range(4)) < 1e-5
a,b=signature(original),signature(split)
if a!=b:
    print('MISMATCH',list((a-b).items())[:1],list((b-a).items())[:1])
    raise RuntimeError('Geometry, UV or material mismatch')
bpy.data.collections['00_ORIGINAL_reference'].hide_viewport=True
known={9:'02_총열',5:'03_가스블록_가늠쇠',146:'04_핸드가드_상부레일',189:'05_총몸',184:'05_총몸',
       203:'06_권총손잡이',209:'07_버퍼튜브',210:'08_개머리판',211:'08_개머리판',
       160:'09_장전손잡이_후보',168:'10_배출구덮개_후보',187:'11_노리쇠_후보'}
collections={}
for r in records:
    obj=bpy.data.objects[r['name']]
    part_id=int(r['name'].rsplit('_',1)[1])
    group=known.get(part_id)
    confidence='로드맵 및 외형 대조' if group else '미확정'
    if not group:
        if r['max'][0]<-3.0: group='03_가스블록_가늠쇠';confidence='위치 기반 임시 분류'
        elif -2.4<r['center'][0]<-1.0 and r['triangles']<=32:
            group='04_핸드가드_상부레일';confidence='위치 기반 레일 조각 임시 분류'
        else: group='99_추가검토_소형부품'
    if group not in collections:
        col=bpy.data.collections.new(group)
        bpy.data.collections['01_COMPONENTS_212'].children.link(col)
        collections[group]=col
    for col in list(obj.users_collection): col.objects.unlink(obj)
    collections[group].objects.link(obj)
    obj['classification']=group
    obj['review_status']=confidence
    r['group']=group;r['confidence']=confidence
scene=bpy.context.scene
scene['stage']='부품 분리 및 임시 분류. 리깅/크기 보정/Unity 적용 전.'
scene['source_credit']='K2C3 by GAMGO, CC-BY-4.0, https://sketchfab.com/3d-models/k2c3-39bb1eeed4b949c7a620b16667262faf'
scene['geometry_validation']='원본 Blender 임포트 대비 모든 면의 월드좌표·UV·머티리얼 동일'
scene['triangle_note']='glTF 원본 12749 / Blender 임포트 12732. 분리 전후 동일. 원인 추가 확인 필요.'
summary={name:len(col.objects) for name,col in collections.items()}
(OUT/'grouping-v003.json').write_text(json.dumps({'groups':summary,'components':records,'validation':'face/world-coordinate/UV/material equality PASS'},ensure_ascii=False,indent=2),encoding='utf-8')
text=bpy.data.texts.new('작업안내')
text.write('K2C3 부품 분리 작업 파일\n212개 조각, 텍스처 8개 내장.\n00_ORIGINAL_reference: 원본 임포트(숨김)\n01_COMPONENTS_212: 분리된 조각과 기능별 임시 분류\n99_추가검토_소형부품 및 후보 표기 조각은 확정 전입니다.\n리깅·원점·실척·Unity 슬롯 설정은 아직 하지 않았습니다.\nK2C3 by GAMGO / CC-BY-4.0\n')
bpy.ops.wm.save_as_mainfile(filepath=str(TARGET))
print('VALIDATION PASS',summary)



