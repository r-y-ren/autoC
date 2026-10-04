"""Cross-check macro variants using the official file-path loader."""
from pathlib import Path
import contextlib,hashlib,io,json,sys,time
D=Path(__file__).resolve().parent;R=D.parents[1]
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make
jobs=json.loads((D/'g2_jobs.json').read_text());paths=list(dict.fromkeys(j['candidate'] for j in jobs))
rows=[json.loads(s) for s in (D/'g2_results.jsonl').read_text().splitlines()];known={r['id']:r for r in rows}
chosen=[]
for candidate in (paths[0],paths[2]):
    possible=[j for j in jobs if j['candidate']==candidate and j['family']=='fieldcraft']
    seed=possible[0]['seed'];chosen.extend(j for j in possible if j['seed']==seed)
assert len(chosen)==4 and all(j['id'] in known for j in chosen)
output=[]
for job in chosen:
    for k in ('candidate','opponent'):assert hashlib.sha256((R/job[k]).read_bytes()).hexdigest()==job[k+'_sha256']
    env=make('kaggriculture',configuration={'seed':job['seed'],'episodeSteps':720},debug=True)
    paths=[str(R/job['candidate']),str(R/job['opponent'])]
    if job['seat']:paths.reverse()
    captured=io.StringIO()
    with contextlib.redirect_stdout(captured),contextlib.redirect_stderr(captured):env.run(paths)
    hashes=[hashlib.sha256(),hashlib.sha256()]
    for step in env.steps[1:]:
        for i in (0,1):hashes[i].update(json.dumps(step[i].action,sort_keys=True).encode())
    final=env.steps[-1];s=job['seat'];coins=[final[s].reward,final[1-s].reward]
    digest=[h.hexdigest() for h in hashes];expected=known[job['id']]
    logs=[v for row in env.logs for v in row if isinstance(v,dict)]
    stderr=[v.get('stderr','') for v in logs if v.get('stderr','').strip()]
    passed=coins==expected['money'] and digest==expected['action_hash'] and len(env.steps)==720 and all(x.status=='DONE' for x in final) and not stderr
    result=dict(candidate=job['candidate'],source_sha256=job['candidate_sha256'],seed=job['seed'],seat=s,coins=coins,all_actions_match=digest==expected['action_hash'],states=len(env.steps),stderr_records=len(stderr),passed=passed,max_official_seconds=max(v.get('duration',0) for v in logs))
    output.append(result);print(json.dumps(result),flush=True)
    (D/'official_macro_crosscheck.json').write_text(json.dumps(dict(games=output,all_passed=all(r['passed'] for r in output),complete=len(output)==4,scope='Execution parity only; not additional independent strength evidence.'),indent=2))
    assert passed,result
