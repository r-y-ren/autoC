"""Ablate worker guards and state alignment on the same declared development worlds."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
spec=json.loads((D/'route_design.json').read_text())
settings=[('no_feed_fixed','fixed',6,False,False),('no_feed_exact','exact_shops',6,False,False),('raw_fixed6','fixed',6,True,False),('raw_fixed10','fixed',10,True,False),('raw_exact10','exact_shops',10,True,True),('raw_nearest10','nearest',10,True,True)]
variants=[]
for name,mode,root,raw_mode,dominance in settings:
    original=next(v for v in spec['variants'] if v['name']=='route_'+mode)
    source=(R/original['path']).read_bytes();assert sha(source)==original['sha256']
    if dominance:
        a=b"            if snapshot['farm_key']!=key:continue"
        b=b"            if not _rp28_compatible(obs['farms'][seat],snapshot['farm_key']):continue"
        assert source.count(a)==1;source=source.replace(a,b)
    source+=('\n_RT28_ROOT='+str(root)+'\n_V17_FEED_GUARD=False\n').encode()
    source+=(D/'route_execution_tail.txt').read_bytes()
    if raw_mode:source+=b'\n_E279_PUBLIC_AGENT=_rp28_raw\n'
    p=D/('route_'+name+'.py');compile(source,str(p),'exec')
    if p.exists():assert p.read_bytes()==source
    else:p.write_bytes(source)
    variants.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(source),mode=mode,root=root,raw=raw_mode,dominance=dominance))
roster=[r for r in spec['roster'] if r['family'] not in ('pipe16','q45_fixed_public','salem_route_mixture')]
jobs=[]
for v in variants:
    for op in roster:
        for seed in spec['seeds']:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('route_execution_jobs.json',jobs),('route_execution_design.json',dict(variants=variants,roster=roster,seeds=spec['seeds'],scope='Development execution ablation. Dominance alignment preserves type/age/geometry and requires no worse starvation, yield or stored care.'))]:
    (D/name).write_text(json.dumps(data,indent=2))
print(json.dumps(dict(candidates=len(variants),cases=len(jobs))),flush=True)
