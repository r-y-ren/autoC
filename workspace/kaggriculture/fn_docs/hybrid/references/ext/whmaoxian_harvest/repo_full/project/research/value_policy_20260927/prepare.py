"""Prepare bounded counterfactual learning on declared development worlds."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
source=R/'research/macro_population_20260927'
roster=json.loads((source/'roster.json').read_text())
roster=[o for o in roster if o['family'] in ('r2','fieldcraft','top_style_02','top_style_03')]
worlds=json.loads((source/'route_learning_design.json').read_text())['seeds'][:8]
base=R/'submissions/release_v10_r2/main.py';digest=hashlib.sha256(base.read_bytes()).hexdigest()
jobs=[]
for i,seed in enumerate(worlds):
    for other in roster:
        row=dict(seed=seed,seat=i%2,opponent=other['path'],family=other['family'],baseline_sha256=digest,opponent_sha256=hashlib.sha256((R/other['path']).read_bytes()).hexdigest())
        row['id']=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()[:24];jobs.append(row)
path=D/'training_jobs.json'
if path.exists():assert json.loads(path.read_text())==jobs
else:path.write_text(json.dumps(jobs,indent=2))
manifest=dict(jobs=len(jobs),worlds=worlds,maximum_branches_per_game=24,feature_source_sha256=hashlib.sha256((R/'research/v10_top10_20260926/market_bc_features.py').read_bytes()).hexdigest(),baseline_sha256=digest,scope='Local development only. Private simulated state is used by the simulator and for outcome labels, never as policy input. No final holdout used.')
(D/'training_design.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest),flush=True)
