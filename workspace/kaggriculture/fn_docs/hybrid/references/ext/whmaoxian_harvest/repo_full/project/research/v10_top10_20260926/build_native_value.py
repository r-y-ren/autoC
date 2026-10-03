"""Finite development of market/task synchronization on public demonstrations."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'native_value';out.mkdir(exist_ok=True)
old_jobs=json.loads((D/'native_v6_jobs.json').read_text())
seeds=sorted({j['seed'] for j in old_jobs});jobs=[];manifest=[]
for teacher in (1,3,4,9):
    parent=D/f'native_v6/teacher{teacher:02d}_rescue1.py'
    for label,feed,cash,lead in [('strict',0,0,False),('buffered',4,12,False),('lead',4,12,True)]:
        path=out/f'teacher{teacher:02d}_{label}.py'
        parameters=f'\n_NV_FEED_RESERVE={feed}\n_NV_FERT_RESERVE=0\n_NV_CASH_RESERVE={cash}\n_NV_LEAD={lead!r}\n'
        raw=parent.read_bytes()+parameters.encode()+(D/'native_value_market.txt').read_bytes()
        compile(raw,str(path),'exec')
        if path.exists():assert path.read_bytes()==raw
        else:path.write_bytes(raw)
        relative=path.relative_to(R).as_posix();digest=hashlib.sha256(raw).hexdigest()
        manifest.append(dict(path=relative,sha256=digest,teacher=teacher,mode=label))
        for seed in seeds:
            for seat in (0,1):
                opponent='submissions/release_v10_r2/main.py'
                job=dict(candidate=relative,opponent=opponent,seed=seed,seat=seat,panel='native_development',family='r2',candidate_sha256=digest,opponent_sha256=hashlib.sha256((R/opponent).read_bytes()).hexdigest())
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(D/'native_value_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(D/'native_value_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest),full_jobs=len(jobs))),flush=True)
