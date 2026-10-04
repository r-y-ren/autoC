"""Second dispatcher study: bulk supply, fewer depot trips, crop-cycle batching."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
original=(D/'dispatch.py.txt').read_text()
changes=[
 ("quantity=min(2,max(0,int(private['shed'].get(item,0))))","quantity=min(6 if item=='WHEAT' else 3,max(0,int(private['shed'].get(item,0))))"),
 ("if missing:\n        item=missing[0];requests[item]=requests.get(item,0)+2","if missing:\n        item=missing[0];requests[item]=requests.get(item,0)+(6 if item=='WHEAT' else 3)"),
 ("ripe and (ongoing or age>=last", "ripe and ((ongoing and (held>=3 or expiry>=0)) or (not ongoing and age>=last)"),
 ("grain=sum(b.get('WHEAT',0) for b in obs['private']['inventories'])", "grain=sum(b.get('WHEAT',0) for b in obs['private']['inventories'])\n    consumed=sum(c==['FEED'] for c in [action['farmer']]+action['hands'])\n    grain=max(0,grain-consumed)\n    unfed=max(0,unfed-consumed)"),
 ("reserve=max(0,unfed-grain)+2 if day<29 else 0", "reserve=max(0,unfed-grain)+6 if day<29 else 0"),
 ("orders.extend(sells[:3] if hour<2 else sells[:7])", "orders.extend(sells[:2] if hour<2 else sells[:7])"),
]
text=original
for old,new in changes:
    assert text.count(old)==1,old
    text=text.replace(old,new)
manifest=[]
for delivery in (16,40):
    for weight in (.6,1.5):
        name=f'v2_drop{delivery}_feed{int(weight*10)}'
        constants=f'\n_DP_START=16\n_DP_WORKERS=12\n_DP_DELIVERY={delivery}\n_DP_PLANT_WEIGHT=.3\n_DP_FEED_WEIGHT={weight}\n_DP_DISTANCE_POWER=1.0\n'
        data=base+constants.encode()+text.encode();path=D/(name+'.py');compile(data,str(path),'exec')
        assert not path.exists();path.write_bytes(data)
        manifest.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest()))
old_jobs=json.loads((D/'smoke_jobs.json').read_text());base_path='submissions/release_v10_r2/main.py'
cases=[j for j in old_jobs if j['candidate']==base_path];jobs=[]
for item in manifest:
    for case in cases:
        job=dict(case,candidate=item['path'],candidate_sha256=item['sha256']);job.pop('id')
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(D/'v2_manifest.json').write_text(json.dumps(manifest,indent=2))
(D/'v2_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'v2_changes.json').write_text(json.dumps(dict(changes=changes,source_sha256=hashlib.sha256(original.encode()).hexdigest(),new_games=len(jobs),reference_ledger='smoke_results.jsonl'),indent=2))
print(json.dumps(dict(variants=len(manifest),new_games=len(jobs))),flush=True)
