"""Fixed public replay opponents: causal diagnostics only, NOT actual private agents."""
from pathlib import Path
import gzip,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
folder=D/'loss_fixtures';folder.mkdir(exist_ok=True)
selection=json.loads((D/'r2_feedback/selection.json').read_text())
variants=json.loads((D/'midgame_herd_design.json').read_text())['variants']+json.loads((D/'herd_sequence_v2_design.json').read_text())['variants']
fixtures=[];jobs=[]
for row in selection:
    raw=gzip.decompress((D/f"r2_feedback/{row['episode']}.json.gz").read_bytes())
    game=json.loads(raw);seat=row['seat'];opponent=1-seat
    tape=[frame[opponent]['action'] for frame in game['steps'][1:]]
    assert len(tape)==719 and all(isinstance(a,dict) for a in tape)
    text='# FIXED REPLAY DIAGNOSTIC ONLY. Public episode '+str(row['episode'])+'\nimport copy\n_TAPE='+repr(tape)+'\ndef fixed_replay_agent(observation,configuration=None):\n    return copy.deepcopy(_TAPE[int(observation["step"])])\nagent=fixed_replay_agent\n'
    p=folder/f"fixed_loss_{row['episode']}.py";compile(text,str(p),'exec')
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
    f=dict(episode=row['episode'],path=p.relative_to(R).as_posix(),sha256=sha(p.read_bytes()),replay_sha256=sha(raw),seed=game['info']['seed'],recorded_seat=seat,recorded_margin=row['margin'],recorded_rewards=game['rewards']);fixtures.append(f)
    for v in variants:
        for s in (0,1):
            j=dict(candidate=v['path'],opponent=f['path'],family=str(row['episode']),panel='fixed_replay_diagnostic',seed=f['seed'],seat=s,candidate_sha256=v['sha256'],opponent_sha256=f['sha256'])
            j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for name,obj in [('loss_fixture_design.json',dict(fixtures=fixtures,variants=variants,scope='Six previously inspected losses. Fixed tapes do not respond like real opponents; development only.')),('loss_fixture_jobs.json',jobs)]:
    p=D/name;text=json.dumps(obj,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps({'fixtures':len(fixtures),'cases':len(jobs)}),flush=True)
