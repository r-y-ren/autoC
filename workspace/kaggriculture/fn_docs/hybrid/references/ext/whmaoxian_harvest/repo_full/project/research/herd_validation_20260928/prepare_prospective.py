"""Freeze nominated candidates, then draw fresh worlds for paired confirmation."""
from pathlib import Path
import hashlib,json,random
D=Path(__file__).resolve().parent;R=D.parents[1];M=R/'research/meta_rebuild_20260927'
sha=lambda b:hashlib.sha256(b).hexdigest()
diverse=json.loads((D/'diverse_design.json').read_text())
base=next(v for v in diverse['variants'] if v['name']=='r2')
variants=[base]
terminal=next(v for v in json.loads((M/'terminal_candidates.json').read_text()) if v['simulations']==256)
variants.append(dict(terminal,name='terminal_only'))
for parent_name,function,name in [('jit_one','just_in_time_herd_agent','jit_one_terminal'),('yarn_nomilk','midgame_herd_agent','nomilk_terminal')]:
    parent=next(v for v in diverse['variants'] if v['name']==parent_name)
    raw=(R/parent['path']).read_bytes();assert sha(raw)==parent['sha256']
    assert b'_TS_PARENT=' not in raw
    tail=(M/'terminal_search_tail.txt').read_bytes().replace(b'_TS_PARENT=phase_b_agent',('_TS_PARENT='+function).encode())
    data=raw+b'\n_TS_LIMIT=256\n_TS_PROPOSALS=16\n'+tail
    report='_JT28_REPORT' if parent_name=='jit_one' else '_K28_HERD_REPORT'
    data+=('\n_MP_REPORT={"terminal":_TS_REPORT,"production":'+report+'}\nterminal_search_agent.telemetry=_MP_REPORT\n').encode()
    p=D/(name+'.py');compile(data,str(p),'exec')
    if p.exists():assert p.read_bytes()==data
    else:p.write_bytes(data)
    variants.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(data)))
for v in variants:assert sha((R/v['path']).read_bytes())==v['sha256']
old=json.loads((D/'herd_extended_design.json').read_text())
seeds=random.Random(202609280915).sample(range(100000,2000000000),32)
assert not set(seeds)&set(old['seeds']+[1799657451])
roster=old['roster'];jobs=[]
for v in variants:
    for op in roster:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('prospective_jobs.json',jobs),('prospective_design.json',dict(variants=variants,roster=roster,seeds=seeds,jobs=len(jobs),scope='Candidates frozen before drawing 32 new random worlds. Independent of this turn development worlds. Local paired evidence only, no online rating conversion.'))]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(candidates=len(variants),worlds=len(seeds),cases=len(jobs))),flush=True)
