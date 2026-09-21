import sys,json
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'02_Resources/Toolchain/python-libs'))
import UnityPy
root=Path(__file__).resolve().parents[2]
base=root/'02_Resources/SPT/SPT-4.1.5/EscapeFromTarkov_Data/StreamingAssets/Windows'
out=root/'02_Resources/Inspection/K2-Rig';out.mkdir(exist_ok=True)
reports=[]
for name in ['assets/content/weapons/hk416/weapon_hk_416a5_556x45_container.bundle','assets/content/weapons/hk416/weapon_hk_416a5_556x45_assets.bundle']:
 env=UnityPy.load(str(base/name));report={'bundle':name,'types':dict(Counter(o.type.name for o in env.objects)),'externals':[],'assets':[]}
 for a in env.assets:
  report['externals'] += [str(x.path) for x in a.externals]
 for o in env.objects:
  if o.type.name in ['Animator','AnimatorController','AnimationClip','MonoBehaviour']:
   tree=o.read_typetree()
   report['assets'].append({'id':o.path_id,'type':o.type.name,'name':tree.get('m_Name'),'keys':list(tree)})
   (out/f'{o.type.name}-{o.path_id}.json').write_text(json.dumps(tree,ensure_ascii=False,indent=2),encoding='utf-8')
 reports.append(report)
(out/'animation-inventory.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
print(json.dumps(reports,indent=2))
