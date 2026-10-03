"""Build bounded multi-batch allocation variants, preserving frozen releases."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert sha(base)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
assert b'_H29_' not in base
panel=json.loads((D/'herd_extension_design.json').read_text())
seeds=[1799657451]+panel['seeds'][:7]
def cfg(start,cap,reserve=150,nomilk=False,ratio=0,gain=-1000000):
    return dict(start=start,end=264,cap=cap,reserve=reserve,nomilk=nomilk,ratio=ratio,gain=gain)
settings=[('early1',cfg(72,1,50)),('early3',cfg(72,3)),('mid3',cfg(144,3)),('early3_nomilk',cfg(72,3,nomilk=True)),('early3_ev',cfg(72,3,ratio=1.1,gain=600)),('early6_nomilk',cfg(72,6,nomilk=True))]
variants=[];jobs=[]
for name,genome in settings:
    data=base+('\n_H29_CFG='+repr(genome)+'\n').encode()+(D/'herd_sequence_v2_20260928.txt').read_bytes()
    path=D/'candidates'/('sequence_v2_'+name+'.py');compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    v=dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(data),genome=genome);variants.append(v)
    for rival in panel['roster']:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=rival['path'],family=rival['family'],panel=rival['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/rival['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for filename,obj in [('herd_sequence_v2_design.json',dict(variants=variants,roster=panel['roster'],seeds=seeds,cases=len(jobs),scope='Development screening; reuse existing identical R2 controls without counting them as new games.')),('herd_sequence_v2_jobs.json',jobs)]:
    path=D/filename;text=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==text
    else:path.write_text(text)
print(json.dumps(dict(candidates=len(variants),cases=len(jobs))),flush=True)
