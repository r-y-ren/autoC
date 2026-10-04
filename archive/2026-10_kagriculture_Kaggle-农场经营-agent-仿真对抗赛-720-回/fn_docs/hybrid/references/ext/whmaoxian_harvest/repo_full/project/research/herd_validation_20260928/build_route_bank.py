"""Build observation-aligned day-three/day-six production branches from public demos."""
from pathlib import Path
import base64,gzip,hashlib,json,zlib
D=Path(__file__).resolve().parent;R=D.parents[1];M=R/'research/meta_rebuild_20260927'
sha=lambda b:hashlib.sha256(b).hexdigest()
records=[];provenance=[];seen=set();root_index=None
for folder in (D,M):
    views=json.loads((folder/'recent_selection.json').read_text(encoding='utf-8'))['views']
    for view in views:
        key=(view['episode'],view['seat'])
        if key in seen:continue
        seen.add(key);seat=view['seat']
        raw=gzip.decompress((folder/'recent_replays'/f"{view['episode']}.json.gz").read_bytes())
        game=json.loads(raw);snapshots={}
        for step in (72,144):
            obs=game['steps'][step][seat]['observation'];farm=obs['farms'][seat]
            fk=json.dumps({k:v for k,v in farm.items() if k!='money'},sort_keys=True,separators=(',',':'))
            snapshots[str(step)]=dict(farm_key=fk,private=obs['private'],shops=obs['town']['unlocked_shops'],prices=obs['market']['prices'])
        if folder==D and view['rank']==4 and root_index is None:root_index=len(records)
        records.append(dict(actions=[s[seat]['action'] for s in game['steps'][1:]],snapshots=snapshots))
        provenance.append(dict(view,record=len(records)-1,replay_sha256=sha(raw)))
assert root_index is not None
blob=zlib.compress(json.dumps(records,separators=(',',':')).encode(),9)
header='\n_RT28_BANK=json.loads(zlib.decompress(base64.b64decode('+repr(base64.b64encode(blob))+')))\n_RT28_ROOT='+str(root_index)+'\n'
base=(D/'salem_checked.py').read_bytes();tail=(D/'route_bank_tail.txt').read_bytes()
variants=[]
for mode in ('fixed','exact_shops','nearest'):
    data=base+(header+'\n_RT28_MODE='+repr(mode)+'\n').encode()+tail
    p=D/('route_'+mode+'.py');compile(data,str(p),'exec')
    if p.exists():assert p.read_bytes()==data
    else:p.write_bytes(data)
    variants.append(dict(name='route_'+mode,path=p.relative_to(R).as_posix(),sha256=sha(data)))
spec=json.loads((D/'diverse_design.json').read_text());jobs=[]
for v in variants:
    for op in spec['roster']:
        for seed in spec['seeds']:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('route_jobs.json',jobs),('route_design.json',dict(variants=variants,roster=spec['roster'],seeds=spec['seeds'],root_index=root_index,records=len(records),scope='Development. New responsive policies derived from public trajectories, not recovered private top-ten source.')),('route_provenance.json',provenance)]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(candidates=len(variants),records=len(records),compressed_bytes=len(blob),jobs=len(jobs))),flush=True)
