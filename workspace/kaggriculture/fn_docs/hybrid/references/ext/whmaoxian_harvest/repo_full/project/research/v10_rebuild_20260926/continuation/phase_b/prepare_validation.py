"""Freeze fresh Phase-B validation jobs after one source has been selected."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent; D=B.parent; W=D.parent; R=W.parents[1]
selection=json.loads((B/'selection.json').read_text(encoding='utf-8'))
candidate=selection['candidate']
assert hashlib.sha256((R/candidate).read_bytes()).hexdigest()==selection['sha256']
public=json.loads((D/'confirmation_design.json').read_text())['roster']
styles=('broker_bea','ledger_lena','slotter_silas','closer_cleo','rancher_rita','melon_mateo')
style=[dict(name=name,path=(D/'reference_agents'/f'{name}.py').relative_to(R).as_posix()) for name in styles]
seeds={kind:[int.from_bytes(hashlib.sha256(f'v10r2-phaseB-final-{kind}-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(count)] for kind,count in [('primary',48),('style',12)]}
known=set()
for folder in (W,D,B):
 for path in folder.glob('*_jobs.json'):
  known.update(job['seed'] for job in json.loads(path.read_text(encoding='utf-8')))
for path in (R/'research').glob('round*/league_seeds.json'):
 old=json.loads(path.read_text(encoding='utf-8'))
 for group in old.values():
  if isinstance(group,list):known.update(x for x in group if isinstance(x,int))
new=[s for group in seeds.values() for s in group]
assert len(new)==len(set(new))==60 and not known.intersection(new)
candidates=[candidate,'submissions/release_v9/main.py','submissions/release_v10/main.py']
hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in candidates+[o['path'] for o in public+style]}
jobs=[]
def add(c,opp,panel,worlds):
 for seed in worlds:
  for seat in (0,1):
   job=dict(candidate=c,opponent=opp['path'],family=opp['name'],panel=panel,seed=seed,seat=seat,candidate_sha256=hashes[c],opponent_sha256=hashes[opp['path']])
   job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
for c in candidates:
 for opp in public:add(c,opp,'public_program',seeds['primary'])
 for opp in style:add(c,opp,'style_stress',seeds['style'])
for old in candidates[1:]:add(candidate,{'path':old,'name':Path(old).parent.name},'direct_reference',seeds['primary'])
assert len(jobs)==2352 and len({j['id'] for j in jobs})==2352
jobs.sort(key=lambda j:(j['seed'],j['panel'],j['family'],j['seat'],j['candidate']))
target=B/'validation_jobs.json';assert not target.exists()
target.write_text(json.dumps(jobs,indent=2),encoding='utf-8')
design=dict(selection=selection,seeds=seeds,public_roster=public,style_roster=style,
 total_games=2352,primary_games_per_version=576,style_games_per_version=144,
 direct_games_per_old_version=96,protocol_sha256=hashlib.sha256((B/'VALIDATION_PROTOCOL.md').read_bytes()).hexdigest(),
 source_hashes=hashes,previous_seen_seed_count=len(known),overlap=0)
(B/'validation_design.json').write_text(json.dumps(design,indent=2),encoding='utf-8')
print(json.dumps({'games':2352,'new_worlds':60,'candidate_sha256':selection['sha256']}),flush=True)
