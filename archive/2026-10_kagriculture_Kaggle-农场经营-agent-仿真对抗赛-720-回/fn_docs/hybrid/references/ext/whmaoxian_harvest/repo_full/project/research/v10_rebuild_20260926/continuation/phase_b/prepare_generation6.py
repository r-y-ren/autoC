"""Develop mechanism repairs. Phase-A confirmation worlds are now diagnostic development data."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent; D=B.parent; W=D.parent; R=W.parents[1]
base=(D/'generation5/advance36.py').read_bytes()
tail=(B/'repair_tail.py.txt').read_bytes(); C=B/'generation6'; C.mkdir(exist_ok=True)
profiles={'safe_only':{'_B_AGGRESSIVE_K':0,'_B_AGGRESSIVE_HORIZON':12},
 'observed12':{'_B_AGGRESSIVE_HORIZON':12},'observed24':{'_B_AGGRESSIVE_HORIZON':24},
 'advance36':{},'decay36':{'_B_DECAY':True},'floor36':{'_B_FLOOR':True},
 'physics36':{'_B_DECAY':True,'_B_FLOOR':True},
 'similarity95':{'_B_SIM_GATE':.95},'similarity90':{'_B_SIM_GATE':.90},
 'book36':{'_ADV_BOOK':True,'_ADV_SUBTRACT_DEBTS':True}}
candidates=[]
for name,settings in profiles.items():
 raw=base+tail+('\n'+ '\n'.join(f'{k}={v!r}' for k,v in settings.items())+'\n').encode()
 path=C/(name+'.py'); assert not path.exists(); compile(raw,str(path),'exec'); path.write_bytes(raw)
 candidates.append(path.relative_to(R).as_posix())
candidates.append('submissions/release_v10/main.py')
old_design=json.loads((D/'confirmation_design.json').read_text())
roster=[dict(path=p['path'],family=p['name'],panel='public_program') for p in old_design['roster'] if p['name'] in ('fieldcraft','aurax','marketshock')]
roster += [dict(path=(D/'generation5/advance36.py').relative_to(R).as_posix(),family='failed_phase_a',panel='counter_population'),
 dict(path=(D/'generation4/reserve12.py').relative_to(R).as_posix(),family='short_reservations',panel='counter_population')]
seeds=[int.from_bytes(hashlib.sha256(f'v10r2-physics-development-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(4)]
regression=[349766850,489789658,1330271808,1838037457]
hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in candidates+[r['path'] for r in roster]}
jobs=[]
def add(candidate,opponent,seed,panel,family):
 for seat in (0,1):
  job=dict(candidate=candidate,opponent=opponent,seed=seed,seat=seat,panel=panel,family=family,
   candidate_sha256=hashes[candidate],opponent_sha256=hashes[opponent])
  job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
for c in candidates:
 for opp in roster:
  for seed in seeds:add(c,opp['path'],seed,opp['panel'],opp['family'])
 for seed in regression:add(c,roster[0]['path'] if roster[0]['family']=='fieldcraft' else next(p['path'] for p in roster if p['family']=='fieldcraft'),seed,'known_regression','fieldcraft')
jobs.sort(key=lambda j:(j['seed'],j['family'],j['seat'],j['candidate']))
(D/'generation6_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
(B/'generation6_design.json').write_text(json.dumps(dict(profiles=profiles,candidates=candidates,roster=roster,new_development_seeds=seeds,known_regression_seeds=regression,previous_confirmation_reclassified_as_development=True),indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(candidates),games=len(jobs),new_worlds=len(seeds),known_diagnostic_worlds=len(regression))),flush=True)
