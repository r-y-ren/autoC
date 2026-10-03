"""Task-input lookahead ablations in new files, leaving V4 and releases immutable."""
from pathlib import Path
import hashlib,json
N=Path(__file__).resolve().parent;R=N.parents[1]
DEST=N/'native_v5';DEST.mkdir(exist_ok=True)
variants=json.loads((N/'native_v4_manifest.json').read_text());output=[];jobs=[]
seed_values=sorted({j['seed'] for j in json.loads((N/'native_v4_jobs.json').read_text())})
for variant in variants:
    if variant['variant']!='hire0':continue
    original=(R/variant['path']).read_bytes()
    assert hashlib.sha256(original).hexdigest()==variant['source_sha256']
    for look in (1,3,6):
        source=original.decode('utf-8');marker='    orders=_market(observation,commands,needs,'
        assert source.count(marker)==1
        source=source.replace(marker,(N/'supply_prefetch.txt').read_text()+marker)
        source=source.replace("reserve={'WHEAT':max(3,animals),'FERTILIZER':max(3,needs.get('FERTILIZER',0))}","reserve={'WHEAT':max(3,animals,needs.get('keep:WHEAT',0)),'FERTILIZER':max(3,needs.get('FERTILIZER',0),needs.get('keep:FERTILIZER',0))}")
        source+=f'\n_INPUT_LOOK={look}\n'
        path=DEST/f"{variant['teacher_episode']}_{variant['teacher_seat']}_look{look}.py"
        compile(source,str(path),'exec');path.write_text(source,encoding='utf-8')
        candidate=path.relative_to(R).as_posix();digest=hashlib.sha256(path.read_bytes()).hexdigest()
        output.append(dict(path=candidate,sha256=digest,lookahead=look))
        opponent='submissions/release_v10_r2/main.py'
        for seed in seed_values:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent,seed=seed,seat=seat,family='r2',panel='native_development',candidate_sha256=digest,opponent_sha256=hashlib.sha256((R/opponent).read_bytes()).hexdigest())
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(N/'native_v5_manifest.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
(N/'native_v5_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(output),jobs=len(jobs))),flush=True)
