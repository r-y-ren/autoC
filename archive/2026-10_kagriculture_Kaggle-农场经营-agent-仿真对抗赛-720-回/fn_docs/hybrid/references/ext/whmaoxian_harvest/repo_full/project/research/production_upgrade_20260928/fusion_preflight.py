"""Run complete-game preflight before admitting composed candidates to the league."""
from pathlib import Path
import json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/macro_population_20260927'))
import arena
jobs=json.loads((D/'fusion_preflight_jobs.json').read_text())
path=D/'fusion_preflight.jsonl'
prior=[json.loads(s) for s in path.read_text().splitlines() if s.strip()] if path.exists() else []
done={r['id'] for r in prior}
with path.open('a',encoding='utf-8') as handle:
    for job in jobs:
        if job['id'] in done:continue
        row=arena.run_job(job);prior.append(row)
        handle.write(json.dumps(row)+'\n');handle.flush()
        print(json.dumps(dict(candidate=Path(job['candidate']).stem,seat=job['seat'],valid=row.get('valid'),margin=row.get('margin'),max_action_seconds=row.get('max_seconds'),error=str(row.get('exception') or row.get('errors'))[-400:])),flush=True)
        if not row.get('valid'):raise RuntimeError('Preflight failed; do not expand this build.')
assert len(prior)==len(jobs) and all(r.get('valid') for r in prior)
output=D/'fusion_results.jsonl'
if not output.exists():output.write_bytes(path.read_bytes())
print(json.dumps(dict(event='preflight_passed',cases=len(prior),cache_seeded=True)),flush=True)
