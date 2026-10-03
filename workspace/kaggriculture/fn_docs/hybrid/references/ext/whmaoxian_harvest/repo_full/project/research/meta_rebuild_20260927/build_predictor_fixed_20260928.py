"""Create distinct, collision-free predictor ablations; preserve all old artifacts."""
from pathlib import Path
import hashlib, json
D=Path(__file__).resolve().parent; R=D.parents[1]
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
design=json.loads((D/'predictor_design.json').read_text()); variants=[]; jobs=[]
for old in design['variants']:
    original=(R/old['path']).read_bytes()
    assert original.startswith(raw)
    tail=original[len(raw):].decode().replace('_PG_', '_K28_PRED_')
    assert '_K28_PRED_' not in raw.decode()
    source=raw+tail.encode(); p=D/'candidates'/('fixed_'+old['name']+'.py')
    compile(source,str(p),'exec')
    if p.exists(): assert p.read_bytes()==source
    else: p.write_bytes(source)
    v=dict(old,name='fixed_'+old['name'],path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(source).hexdigest()); variants.append(v)
    for rival in design['roster']:
        for seat in (0,1):
            j=dict(candidate=v['path'],opponent=rival['path'],family=rival['family'],panel=rival['panel'],seed=design['seeds'][0],seat=seat,candidate_sha256=v['sha256'],opponent_sha256=hashlib.sha256((R/rival['path']).read_bytes()).hexdigest())
            j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24]; jobs.append(j)
out=dict(variants=variants,roster=design['roster'],seeds=design['seeds'][:1],jobs=len(jobs),scope='Development smoke only. Previous invalid records preserved.')
for name,data in [('predictor_fixed_design.json',out),('predictor_fixed_jobs.json',jobs)]:
    p=D/name; text=json.dumps(data,indent=2)
    if p.exists(): assert p.read_text()==text
    else: p.write_text(text)
print(json.dumps({'candidates':len(variants),'smoke_cases':len(jobs)}),flush=True)
