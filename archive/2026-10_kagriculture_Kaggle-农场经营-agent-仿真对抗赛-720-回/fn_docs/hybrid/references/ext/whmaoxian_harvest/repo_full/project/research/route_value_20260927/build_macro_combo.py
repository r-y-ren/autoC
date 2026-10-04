"""Test complementary macro and same-location task improvements as a separate ablation."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
parent=R/'research/macro_population_20260927/population/macro_5a90ca43c24b.py'
source=parent.read_bytes();assert b'macro_population_agent' in source
micro=(R/'research/v10_top10_20260926/micro_opportunities_tail.txt').read_text()
assert micro.count('_U_PARENT=phase_b_agent')==1
micro=micro.replace('_U_PARENT=phase_b_agent','_U_PARENT=macro_population_agent')
code=source+b"\n_U_ACTIONS=('care','water','harvest','fertilizer')\n_U_START=144\n"+micro.encode()
path=D/'macro_micro.py';assert not path.exists();compile(code,str(path),'exec');path.write_bytes(code)
base='submissions/release_v10_r2/main.py';old=json.loads((D/'broad_jobs.json').read_text())
jobs=[]
for case in old:
    if case['candidate']!=base:continue
    job=dict(case,candidate=path.relative_to(R).as_posix(),candidate_sha256=hashlib.sha256(code).hexdigest());job.pop('id')
    job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(D/'macro_combo_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'macro_combo_manifest.json').write_text(json.dumps(dict(candidate=path.relative_to(R).as_posix(),
    sha256=hashlib.sha256(code).hexdigest(),parent_sha256=hashlib.sha256(source).hexdigest(),
    new_games=len(jobs),reference_ledger='broad_results.jsonl',released=False),indent=2))
print(json.dumps(dict(games=len(jobs),candidate=path.name)),flush=True)
