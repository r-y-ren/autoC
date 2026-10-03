"""Test public demonstrated production schedules with the existing reactive stack."""
from pathlib import Path
import base64,gzip,hashlib,json,zlib
D=Path(__file__).resolve().parent;R=D.parents[1];out=D/'macro_transplant';out.mkdir(exist_ok=True)
base=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
records=json.loads((D/'demonstrations_index.json').read_text())
allowed={(x['episode'],x['seat']) for x in json.loads((D/'replay_split.json').read_text())['study']}
seeds=sorted({j['seed'] for j in json.loads((D/'native_v6_jobs.json').read_text())});manifest=[];jobs=[]
for index,record in enumerate(records):
    assert (record['episode'],record['seat']) in allowed
    data=(R/record['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==record['sha256']
    tape=json.loads(gzip.decompress(data))['actions'];assert len(tape)==719
    blob=base64.b85encode(zlib.compress(json.dumps(tape,separators=(',',':')).encode(),9)).decode()
    tail='\nimport base64 as _mt_b64, json as _mt_json, zlib as _mt_zlib\n'
    tail+='_MT_TAPE=_mt_json.loads(_mt_zlib.decompress(_mt_b64.b85decode('+repr(blob)+')))\n'
    tail+='''
_IMPL.chassis.routes={i:_MT_TAPE for i in _IMPL.chassis.routes}
_IMPL.chassis.routes.update({i:_MT_TAPE for i in (0,1,2)})
_IMPL.chassis._future_sells.clear()
_MT_PARENT=phase_b_agent
def macro_transplant_agent(observation,configuration=None):
    return _MT_PARENT(observation,configuration)
macro_transplant_agent.telemetry={}
agent=macro_transplant_agent
kaggle_submission_agent=macro_transplant_agent
'''
    path=out/f'macro{index:02d}.py';raw=base+tail.encode();compile(raw,str(path),'exec')
    if path.exists():assert path.read_bytes()==raw
    else:path.write_bytes(raw)
    candidate=path.relative_to(R).as_posix();digest=hashlib.sha256(raw).hexdigest()
    manifest.append(dict(path=candidate,sha256=digest,teacher=record['team'],study_episode=record['episode'],study_seat=record['seat']))
    for seed in seeds:
        for seat in (0,1):
            opponent='submissions/release_v10_r2/main.py'
            job=dict(candidate=candidate,opponent=opponent,seed=seed,seat=seat,family='r2',panel='macro_development',candidate_sha256=digest,opponent_sha256=hashlib.sha256((R/opponent).read_bytes()).hexdigest())
            job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(D/'macro_transplant_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(D/'macro_transplant_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print(json.dumps(dict(variants=len(manifest),full_jobs=len(jobs),heldout_examples_used=False)),flush=True)
