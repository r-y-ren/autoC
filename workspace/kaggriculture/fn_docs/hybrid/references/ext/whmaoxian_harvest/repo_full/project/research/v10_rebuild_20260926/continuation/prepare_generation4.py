"""Fourth closed-loop generation; no held-out opponent or seed is opened here."""
from pathlib import Path
import hashlib, json
D=Path(__file__).resolve().parent; W=D.parent; R=W.parents[1]
C=D/'generation4'; C.mkdir(exist_ok=True)
base=(W/'combinations/observed4_h24.py').read_bytes()
profiles={'control':{},'supply8':{'_OR2_SN_K':8},'supply12':{'_OR2_SN_K':12},
 'reserve12':{'_OR2_SN_H':12},'reserve48':{'_OR2_SN_H':48},
 'advance16':{'_V10_ADV_HORIZON':16},'advance36':{'_V10_ADV_HORIZON':36},
 'highpressure':{'_OR2_SN_K':8,'_OR2_SN_H':48,'_V10_ADV_THRESHOLD':8}}
candidates=[]
for name, settings in profiles.items():
 raw=base+b'\n# Generation 4: prospective closed-loop ablation.\n'+('\n'.join(f'{k}={v!r}' for k,v in settings.items())+'\n').encode()
 path=C/(name+'.py'); compile(raw,str(path),'exec'); path.write_bytes(raw)
 candidates.append(path.relative_to(R).as_posix())
candidates+=['submissions/release_v9/main.py','submissions/release_v10/main.py']
public=json.loads((W/'public_programs.json').read_text())
extra=json.loads((W/'additional_programs.json').read_text())
roster=[dict(path=p['path'],family=p['name'],panel='public_program') for p in public if p['name']!='pipe5']
roster += [dict(path=p['path'],family=p['name'],panel='public_program') for p in extra if p['role']=='additional_development']
for name in ('observed1_h24','observed8_h24','observed4_h48'):
 roster.append(dict(path=(W/'combinations'/f'{name}.py').relative_to(R).as_posix(),family=name,panel='counter_population'))
roster.append(dict(path='external/round9/frontier/main.py',family='frontier',panel='old_reference'))
seeds=[int.from_bytes(hashlib.sha256(f'v10r2-gen4-expanded-dev-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(8)]
hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in candidates+[p['path'] for p in roster]}
jobs=[]
for candidate in candidates:
 for opp in roster:
  for seed in seeds:
   for seat in (0,1):
    job=dict(candidate=candidate,opponent=opp['path'],family=opp['family'],panel=opp['panel'],seed=seed,seat=seat,
     candidate_sha256=hashes[candidate],opponent_sha256=hashes[opp['path']])
    job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]; jobs.append(job)
(D/'generation4_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
(D/'generation4_design.json').write_text(json.dumps(dict(candidates=candidates,profiles=profiles,roster=roster,seeds=seeds),indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(candidates),opponents=len(roster),worlds=len(seeds),full_games=len(jobs))),flush=True)
