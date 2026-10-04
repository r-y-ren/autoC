"""Prepare sealed-source confirmation; must follow selection, never tune in here."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent; W=D.parent; R=W.parents[1]
selection=json.loads((D/'selection.json').read_text(encoding='utf-8'))
candidate=selection['candidate']
assert hashlib.sha256((R/candidate).read_bytes()).hexdigest()==selection['sha256']
roster=[p for p in json.loads((W/'public_programs.json').read_text()) if p['name']!='pipe5']
roster += json.loads((W/'additional_programs.json').read_text())
roster += [dict(name='structured',path=(D/'structured_adapter.py').relative_to(R).as_posix())]
assert len(roster)==6
seeds=[int.from_bytes(hashlib.sha256(f'v10r2-blind-final-20260926-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(48)]
known=set()
for folder in (W,D):
 for path in folder.glob('*_jobs.json'):
  if path.name!='confirmation_jobs.json':
   known.update(j['seed'] for j in json.loads(path.read_text(encoding='utf-8')))
assert not set(seeds).intersection(known) and len(set(seeds))==48
candidates=[candidate,'submissions/release_v9/main.py','submissions/release_v10/main.py']
hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in candidates+[p['path'] for p in roster]}
jobs=[]
def add(c,op,panel,family):
 for seed in seeds:
  for seat in (0,1):
   job=dict(candidate=c,opponent=op,panel=panel,family=family,seed=seed,seat=seat,candidate_sha256=hashes[c],opponent_sha256=hashes[op])
   job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]; jobs.append(job)
for c in candidates:
 for p in roster:add(c,p['path'],'public_program',p['name'])
for op in candidates[1:]:add(candidate,op,'direct_reference',Path(op).parent.name)
target=D/'confirmation_jobs.json'
assert not target.exists(),'Confirmation manifest already exists; resume the existing batch instead'
assert len(jobs)==1920
# Interleave versions so machine-load trends do not align with one source version.
jobs.sort(key=lambda x:(x['seed'],x['family'],x['seat'],x['candidate']))
target.write_text(json.dumps(jobs,indent=2),encoding='utf-8')
(D/'confirmation_design.json').write_text(json.dumps(dict(source_selection=selection,
 seeds=seeds,roster=roster,program_games_per_version=576,total_full_games=1920,
 protocol_sha256=hashlib.sha256((D/'CONFIRMATION_PROTOCOL.md').read_bytes()).hexdigest()),indent=2),encoding='utf-8')
print(json.dumps(dict(total=1920,worlds=48,public_programs=6,source_sha256=selection['sha256'])),flush=True)
