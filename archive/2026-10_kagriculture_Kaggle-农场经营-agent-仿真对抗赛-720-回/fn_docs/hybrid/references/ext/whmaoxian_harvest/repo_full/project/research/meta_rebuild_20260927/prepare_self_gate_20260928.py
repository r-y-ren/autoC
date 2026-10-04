"""Causal ablations for strategy-identification gates after our own herd changes."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];BASE='submissions/release_v10_r2/main.py'
sha=lambda b:hashlib.sha256(b).hexdigest();variants=[]
for name,parent_name,mode in [('gate_audit_two','h4_two',0),('gate_phase_two','h4_two',1),('gate_all_two','h4_two',2),('gate_phase_one','g3_robust',1)]:
    source=(D/'candidates'/(parent_name+'.py')).read_text(encoding='utf-8')
    assert '_K28G_' not in source
    marker='_K28S_PARENT=phase_b_agent';assert source.count(marker)==1
    helper=f'\n_K28G_MODE={mode}\n'+(D/'self_change_gate_20260928.txt').read_text()
    source=source.replace(marker,helper+'\n_K28S_PARENT=_k28g_phase')
    marker='_MP_REPORT=_K28S_REPORT';assert source.count(marker)==1
    source=source.replace(marker,"_K28S_REPORT.update(gate_opportunities=0,gate_changes=0)\n"+marker)
    path=D/'candidates'/(name+'.py');compile(source,str(path),'exec');data=source.encode()
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=sha(data),mode=mode,parent=parent_name))
p=D/'candidates/h4_two.py';variants.append(dict(name='h4_two',path=p.relative_to(R).as_posix(),sha256=sha(p.read_bytes())))
jobs=[]
for seed in (1799657451,1389476168,347690402):
    for v in variants:
        for seat in (0,1):
            j=dict(candidate=v['path'],opponent=BASE,family='r2',panel='mechanism_diagnostic',seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha((R/BASE).read_bytes()))
            j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,data in [('self_gate_20260928_design.json',dict(variants=variants,scope='Three previously used development worlds. Diagnostic versus intervention; not rating validation.')),('self_gate_20260928_jobs.json',jobs)]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(variants=len(variants),cases=len(jobs))),flush=True)
