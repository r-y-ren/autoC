"""Prepare explicit, paired local simulated-game tests with immutable source hashes."""
from pathlib import Path
import hashlib,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
mode=sys.argv[1] if len(sys.argv)>1 else 'smoke'
variants=json.loads((D/'manifest.json').read_text())
roster=json.loads((R/'research/macro_population_20260927/roster.json').read_text())
seeds=[667500670,942022459] if mode=='smoke' else [667500670,942022459,223350887,1726596017]
if mode=='smoke':roster=[o for o in roster if o['family'] in ('fieldcraft','top_style_03')]
if mode!='smoke':variants=[v for v in variants if v['name'] not in ('mechanism_only','disabled')]
paths=[v['path'] for v in variants]+['submissions/release_v10_r2/main.py']
jobs=[]
for path in paths:
    for other in roster:
        for seed in seeds:
            for seat in ((0,) if mode=='smoke' else (0,1)):
                row=dict(candidate=path,opponent=other['path'],family=other['family'],panel=other['panel'],seed=seed,seat=seat)
                for key in ('candidate','opponent'):row[key+'_sha256']=hashlib.sha256((R/row[key]).read_bytes()).hexdigest()
                row['id']=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()[:24];jobs.append(row)
manifest=D/(mode+'_jobs.json')
if manifest.exists():assert json.loads(manifest.read_text())==jobs
else:manifest.write_text(json.dumps(jobs,indent=2))
(D/(mode+'_design.json')).write_text(json.dumps(dict(jobs=len(jobs),seeds=seeds,roster=roster,variants=variants,scope='Previously seen development worlds; mechanism-only forced entry is not release-eligible.'),indent=2))
print(json.dumps(dict(jobs=len(jobs),mode=mode)),flush=True)
