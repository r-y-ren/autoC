"""Controlled third generation: quantity, future demand and native sales ablations."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];BASE='submissions/release_v10_r2/main.py'
sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(R/BASE).read_bytes();assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
base_body=(D/'repeat_herd_v2_policy_20260928.txt').read_text()
old="gain=_hd2_ev('SHEEP',k,observation,st)[0]-_hd2_ev('COW',k,observation,st)[0]"
assert base_body.count(old)==1;base_body=base_body.replace(old,'gain=_k28v_gain(k,observation,st)')
settings=[('g3_future50',[.5],False,False,1,True),('g3_future100',[1.],False,False,1,True),('g3_firstcare',[0.],True,False,1,True),('g3_correct_future',[1.],True,False,1,True),('g3_robust',[0.,1.],True,True,1,True),('g3_robust_two',[0.,1.],True,True,2,True),('g3_native_sales',[0.],False,False,1,False),('g3_native_robust',[0.,1.],True,True,1,False)]
variants=[]
for name,futures,correct,robust,limit,sales in settings:
    cfg=dict(FROM=72,TO=264,COW_FLOOR=2,LIMIT=limit,RESERVE=150,MIN_GAIN=600,NO_MILK=False,REPAIR=False,FUND_SALES=False)
    constants='\n'+''.join('_K28S_'+k+'='+repr(v)+'\n' for k,v in cfg.items())
    constants+=f'_K28V_FUTURES={futures!r}\n_K28V_CORRECT_FIRST={correct!r}\n_K28V_ROBUST={robust!r}\n'
    body=base_body
    if not sales:
        old="extra=min(st['credit'],max(0,int(stock.get('WOOL',0))-planned))"
        assert body.count(old)==1;body=body.replace(old,'extra=0  # Native market layers retain full control.')
    data=raw+constants.encode()+(D/'herd_cash_guard_v2_20260928.txt').read_bytes()+(D/'herd_scenario_value_20260928.txt').read_bytes()+body.encode()
    path=D/'candidates'/(name+'.py');compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(data),scenarios=futures,correct_first_care=correct,robust=robust,limit=limit,extra_sales=sales))
old_design=json.loads((D/'repeat_screen_20260928_design.json').read_text())
variants.extend(v for v in old_design['variants'] if v['name'] in ('r2','repeat_v2_one'))
seeds=old_design['seeds'];roster=[o for o in old_design['roster'] if o['family']!='top_style_04']
jobs=[]
for seed in seeds:
    for op in roster:
        for v in variants:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
record=dict(variants=variants,seeds=seeds,roster=roster,cases=len(jobs),scope='Generation three uses declared development worlds, not heldout. Terminal-care modification excluded after observed regressions.')
for name,data in [('herd_g3_20260928_design.json',record),('herd_g3_20260928_jobs.json',jobs)]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(variants=len(variants),cases=len(jobs))),flush=True)
