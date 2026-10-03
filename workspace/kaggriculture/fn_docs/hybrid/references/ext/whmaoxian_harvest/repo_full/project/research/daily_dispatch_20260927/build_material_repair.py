"""Repair prematurely skipped seed tasks and speculative morning purchases."""
from pathlib import Path
import hashlib,json,ast
D=Path(__file__).resolve().parent;R=D.parents[1]
parents=['routed2_w12_p1_fert40.py','routed2_w13_p1_fert40.py',
         'tier_w12_p5_fert40.py','tier_w13_p5_fert40.py']
manifest=[]
for parent_name in parents:
    parent=D/parent_name;raw=parent.read_bytes();text=raw.decode();tree=ast.parse(text)
    def function(name):return ast.get_source_segment(text,[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name][-1])
    command=function('_vr_command')
    old="        elif op=='PLANT':skip=tile is not None or private['seeds'].get(command[1],0)<=0"
    new="""        elif op=='PLANT':
            skip=tile is not None
            if not skip and private['seeds'].get(command[1],0)<=0:
                return _dp_walk(pos,target) if pos!=target else ['PASS']"""
    assert command.count(old)==1;command=command.replace(old,new)
    market=function('_vr_market')
    old="""        needs['FERTILIZER']=12
        crop=_dp_crop(day,prices,stock.get('WHEAT',0),needs.get('WHEAT',0))
        if crop:seeds[crop]=8"""
    assert market.count(old)==1
    market=market.replace(old,"        needs['FERTILIZER']=min(12,int(stock.get('FERTILIZER',0)))")
    market=market.replace("orders.extend(sales[:3] if hour<2 else sales[:7])","orders.extend(sales[:1] if hour<2 else sales[:7])")
    for workers in (12,13):
        name=parent.stem+'_fixed'+str(workers)
        wrapper=f'\n_VR_WORKERS={workers}\ndef material_repaired_agent(observation,configuration=None):\n    return routed_dispatch_agent(observation,configuration)\nmaterial_repaired_agent.telemetry=_VR_REPORT\nagent=material_repaired_agent\nkaggle_submission_agent=material_repaired_agent\n'
        code=raw+b'\n'+command.encode()+b'\n'+market.encode()+wrapper.encode()
        path=D/(name+'.py');assert not path.exists();compile(code,str(path),'exec');path.write_bytes(code)
        manifest.append(dict(path=path.relative_to(R).as_posix(),parent=parent_name,workers=workers,
            sha256=hashlib.sha256(code).hexdigest(),parent_sha256=hashlib.sha256(raw).hexdigest()))
base_path='submissions/release_v10_r2/main.py'
cases=[j for j in json.loads((D/'smoke_jobs.json').read_text()) if j['candidate']==base_path];jobs=[]
for item in manifest:
    for case in cases:
        job=dict(case,candidate=item['path'],candidate_sha256=item['sha256']);job.pop('id')
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(D/'material_manifest.json').write_text(json.dumps(manifest,indent=2))
(D/'material_jobs.json').write_text(json.dumps(jobs,indent=2))
print(json.dumps(dict(variants=len(manifest),games=len(jobs),repairs=['Retain unfunded seed tasks until supplied','No speculative daily fertilizer repurchase','More first-hour hiring slots'])),flush=True)
