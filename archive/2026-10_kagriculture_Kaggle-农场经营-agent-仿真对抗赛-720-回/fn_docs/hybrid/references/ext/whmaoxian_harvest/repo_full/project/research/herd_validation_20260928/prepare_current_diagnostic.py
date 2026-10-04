"""Paired development counterfactuals, preserving episode and seat provenance."""
from pathlib import Path
import gzip,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];M=R/'research/meta_rebuild_20260927'
sha=lambda b:hashlib.sha256(b).hexdigest()
first=json.loads((D/'herd_extended_design.json').read_text())['variants']
v2=json.loads((D/'repeat_v2_candidates.json').read_text())
variants=[first[0],next(v for v in first if v['name']=='yarn_nomilk')]
variants += [v for v in v2 if v['name'] in ('repeat_two_v2','early_two_v2')]
variants += json.loads((D/'jit_candidates.json').read_text())
views=[]
for r in json.loads((M/'r2_feedback/selection.json').read_text()):
    views.append(dict(episode=r['episode'],opponent_seat=1-r['seat'],kind='known_r2_loss',source=str(M/'r2_feedback')))
for folder,label in ((M,'archived_top10_development'),(D,'current_top10_development')):
    for r in json.loads((folder/'recent_selection.json').read_text())['views']:
        views.append(dict(episode=r['episode'],opponent_seat=r['seat'],kind=label,source=str(folder/'recent_replays')))
O=D/'fixed_tapes';O.mkdir(exist_ok=True);jobs=[];receipts=[]
seen=set()
for view in views:
    key=(view['episode'],view['opponent_seat'])
    if key in seen:continue
    seen.add(key)
    raw=gzip.decompress((Path(view['source'])/f"{view['episode']}.json.gz").read_bytes())
    game=json.loads(raw);seat=view['opponent_seat'];cfg=game['configuration']
    for field,value in dict(episodeSteps=720,boardSize=10,startingMoney=3000,farmHandCostMult=1,turnsPerDay=24,shedCapacity=100,weedSpawnChance=.005).items():
        assert cfg.get(field,value)==value,(view['episode'],field,cfg.get(field))
    assert not cfg.get('marketParams',{}) and len(game['steps'])==720
    actions=[s[seat]['action'] for s in game['steps'][1:]]
    code='PUBLIC_ACTION_TAPE='+repr(actions)+'\n\ndef agent(obs,config=None):\n    return PUBLIC_ACTION_TAPE[int(obs["step"])]\n'
    p=O/f"episode_{view['episode']}_seat_{seat}.py";compile(code,str(p),'exec')
    if p.exists():assert p.read_text()==code
    else:p.write_text(code,encoding='utf-8')
    receipts.append(dict(view,seed=game['info']['seed'],rewards=game['rewards'],replay_sha256=sha(raw),tape_sha256=sha(p.read_bytes())))
    for v in variants:
        assert sha((R/v['path']).read_bytes())==v['sha256']
        j=dict(candidate=v['path'],opponent=p.relative_to(R).as_posix(),family='episode_'+str(view['episode']),panel='fixed_trace_diagnostic',seed=game['info']['seed'],seat=1-seat,candidate_sha256=v['sha256'],opponent_sha256=sha(p.read_bytes()),episode=view['episode'],trace_kind=view['kind'],original_money=[game['rewards'][1-seat],game['rewards'][seat]])
        j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
assert len({j['id'] for j in jobs})==len(jobs)
for name,data in [('current_diagnostic_jobs.json',jobs),('current_diagnostic_design.json',dict(variants=variants,views=receipts,scope='Fixed public actions only. Current and archived development views are not live top-ten opponents.'))]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(cases=len(jobs),views=len(receipts),episodes=len({v['episode'] for v in receipts}))),flush=True)
