"""Extract donor-local transforms and sample original generic animation curves."""
import sys,json,struct,zlib,math,bisect
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'02_Resources/Toolchain/python-libs'))
import UnityPy
OUT=ROOT/'02_Resources/Inspection/K2-Rig'
bundle=ROOT/'02_Resources/SPT/SPT-4.1.5/EscapeFromTarkov_Data/StreamingAssets/Windows/assets/content/weapons/hk416/weapon_hk_416a5_556x45_container.bundle'
env=UnityPy.load(str(bundle));nodes={}
for obj in env.objects:
 if obj.type.name=='Transform':
  d=obj.read();nodes[obj.path_id]={'id':str(obj.path_id),'name':d.m_GameObject.read().m_Name,'parent':str(d.m_Father.path_id),'position':[d.m_LocalPosition.x,d.m_LocalPosition.y,d.m_LocalPosition.z],'rotation':[d.m_LocalRotation.w,d.m_LocalRotation.x,d.m_LocalRotation.y,d.m_LocalRotation.z],'scale':[d.m_LocalScale.x,d.m_LocalScale.y,d.m_LocalScale.z]}
root=next(k for k,n in nodes.items() if n['name']=='weapon_hk_416a5_556x45_model.generated')
def path(k):
 if k==root:return ''
 n=nodes[k];p=int(n['parent'])
 if p not in nodes:return None
 prefix=path(p)
 return None if prefix is None else ((prefix+'/') if prefix else '')+n['name']
mapping={}
for k,n in nodes.items():
 p=path(k)
 if p is not None:n['path']=p;mapping[zlib.crc32(p.encode())]=n
clip=json.loads((OUT/'clip-1661570814695096094.json').read_text())
bindings=clip['m_ClipBindingConstant']['genericBindings']
# M4 source has an additional new-magazine attachment absent from HK416 static prefab.
mag=dict(next(n for n in mapping.values() if n.get('path')=='Weapon_root/Weapon_root_anim/weapon/mod_magazine'))
mag.update(id='m4_mod_magazine_new',name='mod_magazine_new',path='Weapon_root/Weapon_root_anim/weapon/mod_magazine_new',position=[0.0001405334478477016,-0.40374523401260376,-0.011525115929543972],rotation=[1.0,-1.9073486328125e-06,5.362282003239828e-28,-2.811380106914603e-22],scale=[1,1,1])
mapping[zlib.crc32(mag['path'].encode())]=mag
missing=[b for b in bindings if b['path'] not in mapping]
print('BINDINGS',len(bindings),'MISSING',len(missing),'ATTRIBUTES',sorted(set(b['attribute'] for b in bindings)))
assert not missing,missing[:3]
data=clip['m_MuscleClip']['m_Clip']['data'];stream=data['m_StreamedClip'];dense=data['m_DenseClip'];constants=data['m_ConstantClip']['data']
raw=struct.pack('<'+'I'*len(stream['data']),*stream['data']);offset=0;curves=[[] for _ in range(stream['curveCount'])]
while offset<len(raw):
 time,count=struct.unpack_from('<fi',raw,offset);offset+=8
 for _ in range(count):
  index,*coef=struct.unpack_from('<i4f',raw,offset);offset+=20
  assert 0<=index<len(curves)
  curves[index].append((time,coef))
def stream_value(keys,time):
 index=bisect.bisect_right([k[0] for k in keys],time)-1
 t,c=keys[max(index,0)]
 if not math.isfinite(t) or abs(t)>1e10:return c[3]
 dt=time-t
 return ((c[0]*dt+c[1])*dt+c[2])*dt+c[3]
channels=[]
for b in bindings:
 assert b['typeID']==4 and b['attribute'] in [1,2,3,4]
 channels.append({'node':mapping[b['path']]['id'],'attribute':b['attribute'],'width':4 if b['attribute']==2 else 3})
assert sum(c['width'] for c in channels)==stream['curveCount']+dense['m_CurveCount']+len(constants)
frames=[]
for i in range(round(clip['m_MuscleClip']['m_StopTime']*30)+1):
 t=i/30;di=min(round((t-dense['m_BeginTime'])*dense['m_SampleRate']),dense['m_FrameCount']-1)
 values=[stream_value(k,t) for k in curves]+dense['m_SampleArray'][di*dense['m_CurveCount']:(di+1)*dense['m_CurveCount']]+constants
 assert all(math.isfinite(v) for v in values)
 frames.append(values)
result={'source_clip':clip['m_Name'],'fps':30,'nodes':list(mapping.values()),'channels':channels,'frames':frames,'source_bundle':str(bundle),'note':'Sampled original generic curves; no runtime animator events or IK evaluation.'}
(OUT/'reload-charge-decoded.json').write_text(json.dumps(result),encoding='utf-8')
print('DECODED',len(mapping),'nodes',len(frames),'frames',len(frames[0]),'channels')

