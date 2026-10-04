"""Check in-memory strategy clones against frozen R2 on recorded observations."""
from pathlib import Path
import contextlib,copy,gzip,hashlib,io,json,sys,time
D=Path(__file__).resolve().parent;R=D.parents[1];M=R/'research/meta_rebuild_20260927'
sys.path.insert(0,str(D/'runtime_vendor'));sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
import cloudpickle
source='submissions/release_v10_r2/main.py'
assert hashlib.sha256((R/source).read_bytes()).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
reports=[]
for row in json.loads((M/'r2_feedback/selection.json').read_text())[:3]:
    game=json.loads(gzip.decompress((M/'r2_feedback'/f"{row['episode']}.json.gz").read_bytes()));seat=row['seat']
    for boundary in (72,144,432,696):
        parent=fa.load(source);prefix_matches=0
        for step in range(boundary):
            obs=copy.deepcopy(game['steps'][step][seat]['observation']);obs['step']=step
            prefix_matches+=parent(obs,game['configuration'])==game['steps'][step+1][seat]['action']
        started=time.perf_counter();payload=cloudpickle.dumps(parent);clone=cloudpickle.loads(payload)
        serialization_seconds=time.perf_counter()-started;matched=0;differences=[]
        for step in range(boundary,719):
            obs=copy.deepcopy(game['steps'][step][seat]['observation']);obs['step']=step
            trial=clone(copy.deepcopy(obs),game['configuration']);control=parent(copy.deepcopy(obs),game['configuration'])
            if trial==control:matched+=1
            elif len(differences)<3:differences.append(dict(step=step,control=control,clone=trial))
        report=dict(episode=row['episode'],boundary=boundary,prefix_matches=prefix_matches,compared=719-boundary,matched=matched,differences=differences,bytes=len(payload),serialization_seconds=serialization_seconds,distinct_chassis=parent.__globals__['_IMPL'].chassis is not clone.__globals__['_IMPL'].chassis)
        reports.append(report);(D/'cloning_verification.json').write_text(json.dumps(reports,indent=2))
        print(json.dumps({k:v for k,v in report.items() if k!='differences'}),flush=True)
