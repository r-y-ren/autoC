"""Three newly captured public losses, retained as fixed-action diagnostics."""
from pathlib import Path
import base64,gzip,hashlib,json,zlib
C=Path(__file__).resolve().parent;D=C.parent;W=D.parent;R=W.parents[1]
meta=json.loads((C/'latest_v10_metadata.json').read_text())['data']
selection=json.loads((D/'phase_b/selection.json').read_text())
candidates=[v['path'] for v in json.loads((C/'candidates.json').read_text())]
candidates += [selection['candidate'],'submissions/release_v9/main.py','submissions/release_v10/main.py']
jobs=[];roster=[]
for eid in (113715719,113689929,113683828):
    episode=next(e for e in meta['episodes'] if e['id']==eid)
    own=next(a for a in episode['agents'] if a['submissionId']==56560965)
    seat=own.get('index',0); rival_seat=1-seat
    game=json.loads(gzip.decompress((C/f'public_replays/{eid}.json.gz').read_bytes()))
    tape=[s[rival_seat]['action'] for s in game['steps'][1:]]
    assert len(tape)==719 and game['info']['EpisodeId']==eid
    blob=base64.b85encode(zlib.compress(json.dumps(tape,separators=(',',':')).encode())).decode()
    text=(f'# Fixed public replay {eid}. Not a reactive private agent.\n'
          'import base64,copy,json,zlib\n'
          f'_A=json.loads(zlib.decompress(base64.b85decode({blob!r})))\n'
          'def agent(observation,configuration=None):\n'
          '    return copy.deepcopy(_A[int(observation["step"])])\n')
    dest=C/f'loss_trace_{eid}.py';dest.write_text(text,encoding='utf-8')
    opponent=dest.relative_to(R).as_posix()
    roster.append(dict(episode=eid,recorded_rewards=game['rewards'],seed=game['info']['seed'],seat=seat))
    for candidate in candidates:
        job=dict(candidate=candidate,opponent=opponent,seed=game['info']['seed'],seat=seat,
                 family=str(eid),panel='fresh_loss_diagnostic',episode=eid,recorded_rewards=game['rewards'])
        for key in ('candidate','opponent'):
            job[key+'_sha256']=hashlib.sha256((R/job[key]).read_bytes()).hexdigest()
        job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24]
        jobs.append(job)
(C/'fresh_loss_roster.json').write_text(json.dumps(roster,indent=2),encoding='utf-8')
(C/'fresh_loss_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print(json.dumps(dict(jobs=len(jobs),new_losses=roster)),flush=True)
