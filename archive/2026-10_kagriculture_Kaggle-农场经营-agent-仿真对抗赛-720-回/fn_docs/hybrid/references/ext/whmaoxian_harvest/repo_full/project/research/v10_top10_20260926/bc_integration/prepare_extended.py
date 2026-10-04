"""Fresh development worlds for two retained controls and four new policies."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;D=B.parent;R=B.parents[2]
first=json.loads((B/'candidates.json').read_text())
second=json.loads((B/'second_generation.json').read_text())
retained=[x for x in first if x['name'] in ('add_p55_q4','hold_p55_q8')]
variants=retained+second
base='submissions/release_v10_r2/main.py';roster=json.loads((D/'route_expansion_design.json').read_text())['roster']
seeds=[int.from_bytes(hashlib.sha256(f'market-bc-integration-20260927-dev-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(8)]
assert len(set(seeds))==8
assert not set(seeds).intersection(json.loads((D/'route_expansion_design.json').read_text())['seeds'])
jobs=[]
for candidate in [v['path'] for v in variants]+[base]:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):job[key+'_sha256']=hashlib.sha256((R/job[key]).read_bytes()).hexdigest()
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
assert len(jobs)==1232
for name,data in [('extended_jobs.json',jobs),('extended_protocol.json',dict(variants=variants,seeds=seeds,roster=roster,full_jobs=len(jobs),cached_rows=0,selection='p55_q4 and bounded hold retain non-negative initial per-panel margins; new variants are prespecified ablations.',scope='Prospective DEVELOPMENT, not final heldout. No final top-ten heldout replay accessed.'))]:
    path=B/name
    if path.exists():assert json.loads(path.read_text())==data
    else:path.write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps(dict(worlds=len(seeds),variants=len(variants),full_jobs=len(jobs))),flush=True)
