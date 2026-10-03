"""Counterfactual diagnostic tapes: public actions only, never a live-rival claim."""
from pathlib import Path
import gzip,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];M=R/'research/meta_rebuild_20260927'
sha=lambda b:hashlib.sha256(b).hexdigest()
base=json.loads((D/'herd_extended_design.json').read_text())['variants']
repeat=json.loads((D/'repeat_design.json').read_text())['variants']
variants=[base[0],base[2],repeat[2],repeat[4]]
views=[]
for r in json.loads((M/'r2_feedback/selection.json').read_text()):
    views.append(dict(episode=r['episode'],opponent_seat=1-r['seat'],kind='known_r2_loss',folder='r2_feedback'))
for r in json.loads((M/'recent_selection.json').read_text())['views']:
    views.append(dict(episode=r['episode'],opponent_seat=r['seat'],kind='archived_top10_development',folder='recent_replays'))
folder=D/'fixed_tapes';folder.mkdir(exist_ok=True);jobs=[];receipts=[]
for view in views:
    raw=gzip.decompress((M/view['folder']/f"{view['episode']}.json.gz").read_bytes())
    game=json.loads(raw);seat=view['opponent_seat'];cfg=game['configuration']
    assert len(game['steps'])==720 and cfg.get('episodeSteps',720)==720
    assert cfg.get('boardSize',10)==10 and cfg.get('startingMoney',3000)==3000
    assert cfg.get('farmHandCostMult',1)==1 and not cfg.get('marketParams',{})
    actions=[s[seat]['action'] for s in game['steps'][1:]]
    code='PUBLIC_ACTION_TAPE='+repr(actions)+'\n\ndef agent(obs,config=None):\n    return PUBLIC_ACTION_TAPE[int(obs["step"])]\n'
    p=folder/f"episode_{view['episode']}_seat_{seat}.py";compile(code,str(p),'exec')
    if p.exists():assert p.read_text()==code
    else:p.write_text(code,encoding='utf-8')
    receipts.append(dict(view,seed=game['info']['seed'],rewards=game['rewards'],replay_sha256=sha(raw),tape_sha256=sha(p.read_bytes())))
    for v in variants:
        assert sha((R/v['path']).read_bytes())==v['sha256']
        j=dict(candidate=v['path'],opponent=p.relative_to(R).as_posix(),family='episode_'+str(view['episode']),panel='fixed_trace_diagnostic',seed=game['info']['seed'],seat=1-seat,candidate_sha256=v['sha256'],opponent_sha256=sha(p.read_bytes()),episode=view['episode'],trace_kind=view['kind'],original_money=[game['rewards'][1-seat],game['rewards'][seat]])
        j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
assert len({j['id'] for j in jobs})==len(jobs)
for name,data in [('fixed_diagnostic_jobs.json',jobs),('fixed_diagnostic_design.json',dict(variants=variants,views=receipts,scope='Frozen public action counterfactuals only. Not reactive opponents or online skill calibration.'))]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(cases=len(jobs),views=len(views),episodes=len({v['episode'] for v in views}))),flush=True)
