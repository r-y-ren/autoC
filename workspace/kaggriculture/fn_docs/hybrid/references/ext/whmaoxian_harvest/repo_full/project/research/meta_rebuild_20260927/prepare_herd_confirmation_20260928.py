"""Freeze the single-cohort component before a separate prospective confirmation."""
from pathlib import Path
import hashlib,json,random
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
folder=D/'confirmation_herd_20260928';folder.mkdir(exist_ok=True)
source=D/'candidates/midgame_yarn_nomilk.py';raw=source.read_bytes()
assert sha(raw)=='3c79287b13c061d6e92392462a845fc7bb25eafbc92c204c6405ab9c1dc7c227'
frozen=folder/'agent.py'
if frozen.exists():assert frozen.read_bytes()==raw
else:frozen.write_bytes(raw)
variants=[dict(name='frozen_single_nomilk',path=frozen.relative_to(R).as_posix(),sha256=sha(raw))]
p='submissions/release_v10_r2/main.py';baseline=(R/p).read_bytes()
assert sha(baseline)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
variants.append(dict(name='r2',path=p,sha256=sha(baseline)))
old=json.loads((D/'herd_extension_design.json').read_text())
roster=[op for op in old['roster'] if op['panel'] in ('public_program','new_public_program')]
seeds=random.Random(202609282349).sample(range(1,2147483647),64)
assert not set(seeds)&set(old['seeds']+[1799657451])
jobs=[]
for v in variants:
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel='component_confirmation',seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
design=dict(variants=variants,roster=roster,seeds=seeds,cases=len(jobs),scope='Single-component confirmation only. Four public implementations share lineage; no claim of 2800 rating. No further tuning on this panel.')
for filename,obj in [('herd_confirmation_design.json',design),('herd_confirmation_jobs.json',jobs)]:
    path=D/filename;text=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==text
    else:path.write_text(text)
(folder/'NOT_A_RELEASE.md').write_text('Frozen single-cohort component for confirmation only. Not an approved Kaggle submission.\nSHA256 '+sha(raw)+'\n')
print(json.dumps({'cases':len(jobs),'worlds':len(seeds),'candidate_sha256':sha(raw)}),flush=True)
