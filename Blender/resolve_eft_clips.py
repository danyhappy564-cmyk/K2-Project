exec(open(__file__.replace('resolve_eft_clips.py','inspect_eft_animation.py'),encoding='utf-8').read().split('reports=[]')[0])
controller=json.loads(next(out.glob('AnimatorController-*.json')).read_text())
inventory=json.loads((out/'animation-inventory.json').read_text())[0]
refs={ (inventory['externals'][p['m_FileID']-1].split('/')[-1],p['m_PathID']) for p in controller['m_AnimationClips'] if p['m_FileID'] }
matches=[]
manifest=json.loads((base/'Windows.json').read_text())
paths=[base/p for p in manifest['assets/content/weapons/hk416/weapon_hk_416a5_556x45_container.bundle']['Dependencies'] if 'weapons/' in p and '/textures/' not in p]
for path in paths:
 env=UnityPy.load(str(path))
 for asset in env.assets:
  print('CAB',path.name,asset.name)
  for obj in asset.objects.values():
   if obj.type.name!='AnimationClip' or (asset.name,obj.path_id) not in refs:continue
   tree=obj.read_typetree();name=tree['m_Name']
   row={'bundle':str(path.relative_to(base)),'id':obj.path_id,'name':name,'sample_rate':tree['m_SampleRate']}
   matches.append(row)
   if any(s in name.lower() for s in ['reload','mag','patron','charge']):
    (out/f'clip-{obj.path_id}.json').write_text(json.dumps(tree),encoding='utf-8')
(out/'resolved-clips.json').write_text(json.dumps(matches,indent=2),encoding='utf-8')
print('MATCHES',len(matches))
print(json.dumps([r for r in matches if any(s in r['name'].lower() for s in ['reload','mag','patron','charge'])],indent=2))


