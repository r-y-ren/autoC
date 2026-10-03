"""Third-generation valuation alternatives on the already declared development panel."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];BASE='submissions/release_v10_r2/main.py'
sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(R/BASE).read_bytes();assert sha(raw)=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
body=(D/'repeat_herd_v2_policy_20260928.txt').read_text()
old="gain=_hd2_ev('SHEEP',k,observation,st)[0]-_hd2_ev('COW',k,observation,st)[0]"
assert body.count(old)==1;body=body.replace(old,'gain=_k28v_gain(k,observation,st)')
variants=[]
settings=[('scenario_future50',[.5],False,False),('scenario_future100',[1.],False,False),('scenario_firstcare',[0.],True,False),('scenario_correct_future',[1.],True,False),('scenario_robust',[0.,1.],True,True)]
for name,futures,correct,robust in settings:
    cfg=dict(FROM=72,TO=264,COW_FLOOR=2,LIMIT=3,RESERVE=150,MIN_GAIN=600,NO_MILK=False,REPAIR=False,FUND_SALES=False)
    constants='\n'+''.join('_K28S_'+k+'='+repr(v)+'\n' for k,v in cfg.items())
    constants+=f'_K28V_FUTURES={futures!r}\n_K28V_CORRECT_FIRST={correct!r}\n_K28V_ROBUST={robust!r}\n'
    data=raw+constants.encode()+(D/'herd_cash_guard_v2_20260928.txt').read_bytes()+(D/'herd_scenario_value_20260928.txt').read_bytes()+body.encode()
    data+=b'\n_TF_FEED=False\n_TF_CARE=True\n'+(D/'terminal_feed_tail.txt').read_bytes().replace(b'_TF_PARENT=phase_b_agent',b'_TF_PARENT=repeat_herd_agent')+b'\n_MP_REPORT=_K28S_REPORT\n'
    path=D/'candidates'/(name+'.py');compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(data),scenarios=futures,correct_first_care=correct,robust=robust))
old_design=json.loads((D/'repeat_screen_20260928_design.json').read_text())
variants.extend(v for v in old_design['variants'] if v['name'] in ('r2','repeat_v2_care_audited','care_only'))
seeds=old_design['seeds'];roster=[o for o in old_design['roster'] if o['family'] in ('fieldcraft','dmitrii','r2','top_style_02','top_style_01')]
jobs=[]
for seed in seeds:
    for op in roster:
        for v in variants:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/op['path']).read_bytes()))
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
record=dict(variants=variants,seeds=seeds,roster=roster,cases=len(jobs),scope='Third generation; reuses declared development worlds. No heldout or online rating claim.')
for name,data in [('scenario_herd_20260928_design.json',record),('scenario_herd_20260928_jobs.json',jobs)]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(variants=len(variants),cases=len(jobs))),flush=True)
