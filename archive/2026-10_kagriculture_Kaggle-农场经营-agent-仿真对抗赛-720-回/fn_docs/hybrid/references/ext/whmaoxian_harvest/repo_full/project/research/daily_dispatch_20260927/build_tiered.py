"""Separate essential daily farm maintenance from optional investment tasks."""
from pathlib import Path
import ast,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
parent=D/'routed2_w12_p1_fert20.py';base=parent.read_bytes();text=base.decode()
tree=ast.parse(text)
node=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_vr_plan'][-1]
planner=ast.get_source_segment(text,node)
start=planner.index("    starts=[tuple(farm['farmer'])]")
preparation=planner[:start].replace('def _vr_plan(obs):','def _tier_jobs(obs):')+'    return jobs,crop\n'
packing=planner[planner.index('    plans=[];needs={}'):]
logic=(D/'tier_logic.py.txt').read_text()+ '\n'+packing+'\n'
wrapper="""
_VR_REPORT.update(essential_unassigned=0,optional_upgrades=0)
def tiered_dispatch_agent(observation,configuration=None):
    return routed_dispatch_agent(observation,configuration)
tiered_dispatch_agent.telemetry=_VR_REPORT
agent=tiered_dispatch_agent
kaggle_submission_agent=tiered_dispatch_agent
"""
manifest=[]
for workers in (12,13):
    for weight in (.5,1.0):
        for minimum in (20,40):
            name=f'tier_w{workers}_p{int(weight*10)}_fert{minimum}'
            settings=f'\n_VR_WORKERS={workers}\n_DP_PLANT_WEIGHT={weight}\n_VR_MIN_FERT={minimum}\n'
            code=base+settings.encode()+preparation.encode()+logic.encode()+wrapper.encode()
            path=D/(name+'.py');assert not path.exists();compile(code,str(path),'exec');path.write_bytes(code)
            manifest.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(code).hexdigest()))
base_path='submissions/release_v10_r2/main.py'
cases=[j for j in json.loads((D/'smoke_jobs.json').read_text()) if j['candidate']==base_path];jobs=[]
for item in manifest:
    for case in cases:
        job=dict(case,candidate=item['path'],candidate_sha256=item['sha256']);job.pop('id')
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(D/'tier_manifest.json').write_text(json.dumps(manifest,indent=2))
(D/'tier_jobs.json').write_text(json.dumps(jobs,indent=2))
print(json.dumps(dict(variants=len(manifest),games=len(jobs))),flush=True)
