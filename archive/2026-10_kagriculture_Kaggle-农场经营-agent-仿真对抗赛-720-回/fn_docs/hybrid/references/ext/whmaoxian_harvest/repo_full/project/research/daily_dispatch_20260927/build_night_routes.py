"""Permit end-of-day collection instead of forcing every route back to the shed."""
from pathlib import Path
import ast,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
parents=['routed2_w12_p1_fert40_fixed12.py','tier_w12_p5_fert40_fixed12.py']
manifest=[]
for name in parents:
    raw=(D/name).read_bytes();text=raw.decode();tree=ast.parse(text)
    def fn(name):return ast.get_source_segment(text,[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name][-1])
    planner=fn('_vr_plan');cost=fn('_vr_cost');insert=fn('_vr_insert_cost')
    planner=planner.replace('def _vr_plan(obs):','def _vr_plan(obs):\n    global _VR_FINAL_DAY\n    _VR_FINAL_DAY=int(obs["step"])//24==29')
    planner=planner.replace('else 23-hour','else 24-hour')
    old="        if route:commands.append((_dp_home(jobs[route[-1]]['xy']),['DROP']))"
    assert planner.count(old)==1;planner=planner.replace(old,"        if route and _VR_FINAL_DAY:commands.append((_dp_home(jobs[route[-1]]['xy']),['DROP']))")
    old="    if route:length+=_dp_dist(where,_dp_home(where))+1"
    assert cost.count(old)==1;cost=cost.replace(old,"    if route and _VR_FINAL_DAY:length+=_dp_dist(where,_dp_home(where))+1")
    old="    else:\n        added+=_dp_dist(position,_dp_home(position))"
    assert insert.count(old)==1;insert=insert.replace(old,"    elif _VR_FINAL_DAY:\n        added+=_dp_dist(position,_dp_home(position))")
    for workers in (11,12,13):
        stem=('night_tier' if name.startswith('tier') else 'night_full')+f'_w{workers}'
        wrapper=f'\n_VR_FINAL_DAY=False\n_VR_WORKERS={workers}\ndef night_route_agent(observation,configuration=None):\n    return routed_dispatch_agent(observation,configuration)\nnight_route_agent.telemetry=_VR_REPORT\nagent=night_route_agent\nkaggle_submission_agent=night_route_agent\n'
        code=raw+b'\n'+cost.encode()+b'\n'+insert.encode()+b'\n'+planner.encode()+wrapper.encode()
        path=D/(stem+'.py');assert not path.exists();compile(code,str(path),'exec');path.write_bytes(code)
        manifest.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(code).hexdigest(),parent=name))
base_path='submissions/release_v10_r2/main.py'
cases=[j for j in json.loads((D/'smoke_jobs.json').read_text()) if j['candidate']==base_path];jobs=[]
for item in manifest:
    for case in cases:
        job=dict(case,candidate=item['path'],candidate_sha256=item['sha256']);job.pop('id')
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(D/'night_manifest.json').write_text(json.dumps(manifest,indent=2))
(D/'night_jobs.json').write_text(json.dumps(jobs,indent=2))
print(json.dumps(dict(variants=len(manifest),games=len(jobs),final_day_return_preserved=True)),flush=True)
