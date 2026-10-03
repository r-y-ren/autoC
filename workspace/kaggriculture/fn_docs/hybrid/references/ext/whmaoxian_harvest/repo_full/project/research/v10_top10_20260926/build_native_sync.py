"""Repair task timing in experimental top-ten imitators, never a release."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'native_sync';out.mkdir(exist_ok=True)
prior=json.loads((D/'native_v6_manifest.json').read_text(encoding='utf-8'))
seeds=sorted({j['seed'] for j in json.loads((D/'native_v6_jobs.json').read_text())})
manifest=[];jobs=[]
for spec in prior:
    if not spec['rescue']:continue
    original=(R/spec['path']).read_bytes();assert hashlib.sha256(original).hexdigest()==spec['sha256']
    for label,lead,raw_market in [('sync',0,False),('sync_raw',0,True),('early_raw',1,True)]:
        source=original.decode('utf-8');lines=source.splitlines(True)
        found=[i for i,line in enumerate(lines) if "task=tasks[pointer];target=tuple(task['xy'])" in line]
        assert len(found)==1,found
        insert=f"        if hour < max(0,int(task['hour'])-{lead}):\n            return _walk(pos,target) or ['PASS']\n"
        lines.insert(found[0]+1,insert);source=''.join(lines)
        if raw_market:
            old="scheduled=_TASK_PROXY(obs,configuration)"
            assert source.count(old)==1
            source=source.replace(old,"scheduled=copy.deepcopy(_TASK_ACTIONS[min(718,int(obs['step']))])")
        path=out/(Path(spec['path']).stem+'_'+label+'.py');compile(source,str(path),'exec')
        if path.exists():assert path.read_bytes()==source.encode('utf-8')
        else:path.write_bytes(source.encode('utf-8'))
        candidate=path.relative_to(R).as_posix();digest=hashlib.sha256(path.read_bytes()).hexdigest()
        manifest.append(dict(path=candidate,sha256=digest,parent=spec['path'],parent_sha256=spec['sha256'],variant=label,earliest_task_lead=lead,raw_market=raw_market))
        opponent='submissions/release_v10_r2/main.py'
        for seed in seeds:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent,seed=seed,seat=seat,family='r2',panel='native_development',candidate_sha256=digest,opponent_sha256=hashlib.sha256((R/opponent).read_bytes()).hexdigest())
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
assert len(manifest)==30 and len(jobs)==120
(D/'native_sync_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(D/'native_sync_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest),jobs=len(jobs),changes=['respect_demonstrated_task_time','project_market_only_from_actual_physical_actions_or_use_raw_orders'],release_created=False)),flush=True)
