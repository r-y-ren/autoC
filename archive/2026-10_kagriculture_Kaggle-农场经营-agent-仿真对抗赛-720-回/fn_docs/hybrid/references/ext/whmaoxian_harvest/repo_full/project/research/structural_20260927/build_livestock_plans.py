"""Test later animal allocation without changing the demonstrated opening."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
parents=['research/structural_20260927/plans/plan02_physical.py','research/structural_20260927/plans/plan02_default.py']
tail=(P/'livestock_plan_policy.txt').read_bytes();out=P/'livestock_plans';out.mkdir(exist_ok=True)
variants=[]
for parent in parents:
    base=(R/parent).read_bytes()
    for start in (72,144):
        for rule,minimum in (('cow',1),('auto',1),('auto',2),('both',1)):
            settings=dict(parent=parent,start=start,rule=rule,minimum=minimum)
            constants=f'\n_LM_START={start}\n_LM_RULE={rule!r}\n_LM_MIN_SHOPS={minimum}\n'
            data=base+constants.encode()+tail
            name=Path(parent).stem+f'_{start}_{rule}{minimum}.py';path=out/name
            compile(data,str(path),'exec')
            if path.exists():assert path.read_bytes()==data
            else:path.write_bytes(data)
            variants.append(dict(path=path.relative_to(R).as_posix(),settings=settings,sha256=hashlib.sha256(data).hexdigest()))
(P/'livestock_manifest.json').write_text(json.dumps(variants,indent=2))
design=json.loads((P/'plan_screen_design.json').read_text());jobs=[]
roster=[r for r in design['roster'] if r['family'] in ('fieldcraft','r2','top_style_03')]
for candidate in [v['path'] for v in variants]+parents+['submissions/release_v10_r2/main.py']:
    for rival in roster:
        for seed in design['seeds']:
            for seat in (0,1):
                row=dict(candidate=candidate,opponent=rival['path'],family=rival['family'],panel=rival['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):row[key+'_sha256']=hashlib.sha256((R/row[key]).read_bytes()).hexdigest()
                row['id']=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()[:24];jobs.append(row)
for name,value in [('livestock_jobs.json',jobs),('livestock_design.json',dict(variants=variants,parents=parents,roster=roster,seeds=design['seeds'],total=len(jobs),scope='Development ablation of later purchases on an unchanged opening.'))]:
    path=P/name
    if path.exists():assert json.loads(path.read_text())==value
    else:path.write_text(json.dumps(value,indent=2))
print(json.dumps(dict(variants=len(variants),games=len(jobs),new_release=False)),flush=True)
