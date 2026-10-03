"""Test current top-ten task plans with their demonstrated market commitments."""
from pathlib import Path
import base64,gzip,hashlib,json,zlib
N=Path(__file__).resolve().parent;R=N.parents[1];DEST=N/'native_v6';DEST.mkdir(exist_ok=True)
core=(R/'experiments/round7_local_chassis_core.py').read_text(encoding='utf-8')
runtime=(N/'native_v5/113642005_0_look1.py').read_text(encoding='utf-8')
runtime=runtime[:runtime.index('\n_PLAN=')]
index=json.loads((N/'demonstrations_index.json').read_text());split=json.loads((N/'replay_split.json').read_text())
seen=set();output=[];jobs=[]
seeds=sorted({j['seed'] for j in json.loads((N/'native_v4_jobs.json').read_text())})
for view in split['study']:
    if view['team'] in seen:continue
    seen.add(view['team'])
    record=next(r for r in index if r['episode']==view['episode'] and r['seat']==view['seat'])
    demo=json.loads(gzip.decompress((R/record['path']).read_bytes()))
    for rescue in (False,True):
        source=core+'\n'+runtime+'\n_INPUT_LOOK=1\n'
        for name,value in [('_PLAN',demo['plans']),('_TASK_ACTIONS',demo['actions'])]:
            blob=base64.b85encode(zlib.compress(json.dumps(value,separators=(',',':')).encode(),9)).decode()
            source+='\n'+name+'=json.loads(zlib.decompress(base64.b85decode('+repr(blob)+')))\n'
        source+=f'\n_TASK_RESCUE={rescue!r}\n'+(N/'task_market_tail.txt').read_text(encoding='utf-8')
        path=DEST/f"teacher{view['rank']:02d}_rescue{int(rescue)}.py";compile(source,str(path),'exec');path.write_text(source,encoding='utf-8')
        candidate=path.relative_to(R).as_posix();digest=hashlib.sha256(path.read_bytes()).hexdigest()
        output.append(dict(path=candidate,sha256=digest,teacher=record['team'],rescue=rescue))
        opponent='submissions/release_v10_r2/main.py'
        for seed in seeds:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent,seed=seed,seat=seat,family='r2',panel='native_development',candidate_sha256=digest,opponent_sha256=hashlib.sha256((R/opponent).read_bytes()).hexdigest())
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(N/'native_v6_manifest.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
(N/'native_v6_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(output),jobs=len(jobs))),flush=True)
