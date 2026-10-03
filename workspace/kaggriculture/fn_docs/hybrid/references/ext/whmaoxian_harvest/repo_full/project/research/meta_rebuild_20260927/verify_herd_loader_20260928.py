"""Cross-check new candidate files with the official local file loader."""
from pathlib import Path
import contextlib,gc,hashlib,io,json,sys,time
D=Path(__file__).resolve().parent;R=D.parents[1];BASE='submissions/release_v10_r2/main.py'
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
cases=[('repeat_v2_two.py',1799657451,0),('repeat_v2_two.py',1799657451,1),('repeat_v2_care_audited.py',1401688540,0),('repeat_v2_care_audited.py',1401688540,1)]
results=[]
for name,seed,seat in cases:
    candidate='research/meta_rebuild_20260927/candidates/'+name
    before=hashlib.sha256((R/candidate).read_bytes()).hexdigest()
    fast=fa.play(candidate,BASE,seed,seat)
    ordered=[str(R/candidate),str(R/BASE)] if seat==0 else [str(R/BASE),str(R/candidate)]
    env=fa.make('kaggriculture',configuration={'seed':seed,'episodeSteps':720},debug=False)
    capture=io.StringIO();start=time.perf_counter()
    with contextlib.redirect_stdout(capture),contextlib.redirect_stderr(capture):env.run(ordered)
    hashes=[hashlib.sha256(),hashlib.sha256()]
    for step in env.steps[1:]:
        for i in (0,1):hashes[i].update(json.dumps(step[i].action,sort_keys=True).encode())
    final=env.steps[-1];money=[final[seat].reward,final[1-seat].reward]
    status=[s.status for s in final];action_hash=[h.hexdigest() for h in hashes]
    valid=fast['valid'] and len(env.steps)==720 and money==fast['money'] and status==['DONE','DONE'] and action_hash==fast['action_hash'] and not capture.getvalue().strip()
    result=dict(candidate=candidate,seed=seed,seat=seat,valid=valid,money=money,statuses=status,steps=len(env.steps),action_hash=action_hash,source_sha256=before,seconds=time.perf_counter()-start,output=capture.getvalue()[:500])
    results.append(result);print(json.dumps(result),flush=True)
    (D/'herd_loader_checks_20260928.json').write_text(json.dumps(results,indent=2))
    assert valid,result
    assert hashlib.sha256((R/candidate).read_bytes()).hexdigest()==before
    del env;gc.collect()
