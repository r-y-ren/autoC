"""Compose measured modules with explicit parent bindings and immutable sources."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];M=R/'research/meta_rebuild_20260927'
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
def save(path,data):
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
configs=[('finish',False,False,'native'),('herd_finish',True,False,'native'),('herd_noadvance',True,True,'native'),('herd_nopredict',True,False,'off'),('herd_neither',True,True,'off'),('herd_gate6',True,False,'gate6'),('herd_gate6_noadvance',True,True,'gate6')]
variants=[]
for name,herd,noadvance,pred in configs:
    text=base.decode();reports=[]
    if herd:
        text+='\n_K28_NO_MILK=False\n_K28_RATIO=1.1\n_K28_GAIN=600\n'
        text+=(M/'midgame_herd_tail_20260928.txt').read_text()
        text+=(D/'cash_guard_tail.txt').read_text()
        reports+=['_K28_HERD_REPORT','_K28C_REPORT']
    text+='\n_TF_FEED=True\n_TF_CARE=True\n'
    text+=(M/'terminal_feed_tail.txt').read_text().replace('_TF_PARENT=phase_b_agent','_TF_PARENT=agent')
    text+='\n_TS_LIMIT=256\n_TS_PROPOSALS=16\n'
    text+=(M/'terminal_search_tail.txt').read_text().replace('_TS_PARENT=phase_b_agent','_TS_PARENT=agent')
    reports+=['_TF_REPORT','_TS_REPORT']
    if noadvance:text+='\n_ADV_FROM=720\n_B_AGGRESSIVE_K=0\n'
    if pred!='native':
        text+=f'\n_K28F_P_OFF={pred=="off"!r}\n_K28F_P_MATCH=6\n_K28F_P_PRECISION=0.5\n_K28F_P_SCORE=0\n'
        tail=(M/'predictor_gate_tail.txt').read_text().replace('_PG_','_K28F_P_')
        text+=tail.replace('_K28F_P_PARENT=phase_b_agent','_K28F_P_PARENT=agent')
        reports+=['_K28F_P_REPORT']
    text+='\n_K28F_ENTRY=agent\n_MP_REPORT={'+','.join(repr(r)+':'+r for r in reports)+'}\n'
    text+='\ndef fused_agent(observation,configuration=None):\n    if int(observation["step"])==0 and "_K28C_REPORT" in globals():\n        for key in _K28C_REPORT:_K28C_REPORT[key]=0\n    return _K28F_ENTRY(observation,configuration)\nfused_agent.telemetry=_MP_REPORT\nagent=fused_agent\nkaggle_submission_agent=fused_agent\n'
    path=D/'candidates'/('fused_'+name+'.py');compile(text,str(path),'exec');save(path,text.encode())
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(text.encode()).hexdigest(),herd=herd,noadvance=noadvance,pred=pred))
prior=json.loads((D/'herd_stage1_design.json').read_text());seeds=[1799657451]+prior['seeds'][:8]
def job(v,op,seed,seat):
    j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=hashlib.sha256((R/op['path']).read_bytes()).hexdigest())
    j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];return j
jobs=[job(v,op,seed,seat) for v in variants for op in prior['roster'] for seed in seeds for seat in (0,1)]
smoke=[j for j in jobs if j['seed']==1799657451 and j['family']=='r2']
replays=json.loads((D/'replay_opponents.json').read_text())
diagnostic=[job(v,op,op['seed'],op['seat']) for v in variants for op in replays]
for name,data in [('fusion_design.json',dict(variants=variants,seeds=seeds,roster=prior['roster'],scope='Development module interactions; not rating evidence.')),('fusion_jobs.json',jobs),('fusion_preflight_jobs.json',smoke),('fusion_diagnostic_jobs.json',diagnostic)]:
    save(D/name,json.dumps(data,indent=2).encode())
print(json.dumps(dict(variants=len(variants),preflight=len(smoke),development=len(jobs),diagnostic=len(diagnostic))),flush=True)
