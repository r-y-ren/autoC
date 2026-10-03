"""Check new inference source with the actual official file-path loader."""
from pathlib import Path
import contextlib, gc, hashlib, io, json
B=Path(__file__).resolve().parent; R=B.parents[2]
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make
rows=[json.loads(s) for s in (B/'shadow_results.jsonl').read_text().splitlines()]
chosen=[next(r for r in rows if r['candidate'].endswith('/shadow.py') and r['family']==family and r['seat']==seat) for family,seat in [('fieldcraft',0),('top_style_03',1)]]
results=[]
for row in chosen:
    paths=[str(R/row['candidate']),str(R/row['opponent'])]
    env=make('kaggriculture',configuration={'seed':row['seed'],'episodeSteps':720},debug=True)
    env.run(paths if row['seat']==0 else paths[::-1])
    hashes=[hashlib.sha256() for _ in range(2)]
    for step in env.steps[1:]:
        for seat in range(2):hashes[seat].update(json.dumps(step[seat].action,sort_keys=True).encode())
    money=[env.steps[-1][i].reward for i in (row['seat'],1-row['seat'])]
    logs=[s[row['seat']] for s in env.logs if len(s)==2 and isinstance(s[row['seat']],dict)]
    errors=[v.get('stderr','') for v in logs if v.get('stderr','').strip()]
    assert money==row['money'] and [h.hexdigest() for h in hashes]==row['action_hash']
    assert len(env.steps)==720 and not errors and all(s.status=='DONE' for s in env.steps[-1])
    result=dict(seed=row['seed'],seat=row['seat'],family=row['family'],coins=money,all_actions_match=True,states=720,stderr_records=0,max_official_seconds=max(v.get('duration',0) for v in logs))
    results.append(result); print(json.dumps(result),flush=True)
    del env;gc.collect()
(B/'official_shadow.json').write_text(json.dumps(dict(passed=True,games=results),indent=2),encoding='utf-8')
