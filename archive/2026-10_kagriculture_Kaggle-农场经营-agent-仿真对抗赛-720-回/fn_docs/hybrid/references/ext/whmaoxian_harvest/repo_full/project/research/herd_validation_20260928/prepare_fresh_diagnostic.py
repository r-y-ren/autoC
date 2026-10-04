"""Post-freeze diagnostic sample with exact replay identities and all outcomes retained."""
from pathlib import Path
import gzip,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];F=D/'fresh_feedback';O=D/'fixed_tapes'
sha=lambda b:hashlib.sha256(b).hexdigest()
selection=json.loads((F/'selection.json').read_text(encoding='utf-8'))
receipts={r['episode']:r for r in json.loads((F/'resume_receipts.json').read_text())}
variants=json.loads((D/'prospective_design.json').read_text())['variants'];jobs=[]
prior={v['episode'] for v in json.loads((D/'current_diagnostic_design.json').read_text())['views']}
for view in selection['views']:
    raw=gzip.decompress((F/f"{view['episode']}.json.gz").read_bytes())
    assert sha(raw)==receipts[view['episode']]['sha256']
    game=json.loads(raw);seat=view['seat'];cfg=game['configuration']
    for field,value in dict(episodeSteps=720,boardSize=10,startingMoney=3000,farmHandCostMult=1,turnsPerDay=24,shedCapacity=100,weedSpawnChance=.005).items():
        assert cfg.get(field,value)==value
    assert not cfg.get('marketParams',{}) and len(game['steps'])==720
    actions=[s[1-seat]['action'] for s in game['steps'][1:]]
    code='PUBLIC_ACTION_TAPE='+repr(actions)+'\n\ndef agent(obs,config=None):\n    return PUBLIC_ACTION_TAPE[int(obs["step"])]\n'
    path=O/f"episode_{view['episode']}_seat_{1-seat}.py";compile(code,str(path),'exec')
    if path.exists():assert path.read_text(encoding='utf-8')==code
    else:path.write_text(code,encoding='utf-8')
    for v in variants:
        assert sha((R/v['path']).read_bytes())==v['sha256']
        j=dict(candidate=v['path'],opponent=path.relative_to(R).as_posix(),family='episode_'+str(view['episode']),panel='fresh_fixed_trace',seed=game['info']['seed'],seat=seat,candidate_sha256=v['sha256'],opponent_sha256=sha(path.read_bytes()),episode=view['episode'],original_money=[game['rewards'][seat],game['rewards'][1-seat]])
        j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
overlap=sorted(prior&{v['episode'] for v in selection['views']})
for name,data in [('fresh_diagnostic_jobs.json',jobs),('fresh_diagnostic_design.json',dict(variants=variants,selection=selection,overlap_previous_episodes=overlap,cases=len(jobs),scope='Later public R2 feedback, sampled before reading. Fixed opponent actions, not online candidate games.'))]:
    p=D/name;text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(cases=len(jobs),views=len(selection['views']),overlap=len(overlap))),flush=True)
