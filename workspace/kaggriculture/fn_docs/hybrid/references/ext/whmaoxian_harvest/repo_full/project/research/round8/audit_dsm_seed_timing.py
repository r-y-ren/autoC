"""Bounded replay-only seed liquidity audit; uses existing diagnostic actions."""
import contextlib,copy,gzip,io,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
SOURCE=ROOT/'research/round8/dsm_candidate_diagnostics'
reports=[]
for filename,seed in [('seed733556107-seat0-fieldcraft.json.gz',733556107),
                      ('seed733556107-seat0-master2965.json.gz',733556107),
                      ('seed800459488-seat0-release_v6.json.gz',800459488)]:
    replay=json.loads(gzip.decompress((SOURCE/filename).read_bytes()))
    env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720},debug=True)
    timeline=[]
    for step in range(192):
        obs=env.state[0].observation;farm=obs.farms[0];private=obs.private
        action=replay['steps'][step+1][0]['action']
        before=json.loads(json.dumps(obs))
        env.step([replay['steps'][step+1][p]['action'] for p in (0,1)])
        after=env.state[0].observation
        if 144<=step:
            units=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
            positions=[before['farms'][0]['farmer'],*before['farms'][0]['hands']]
            operations=[]
            for actor,command in enumerate(units):
                if actor>=len(positions) or command[0] in ('PASS','NORTH','SOUTH','EAST','WEST'):continue
                operations.append({'actor':actor,'command':command,'position':positions[actor],
                                   'carried':before['private']['inventories'][actor]})
            timeline.append({'step':step,'money':before['farms'][0]['money'],
                             'money_after':after.farms[0]['money'],
                             'shed':before['private']['shed'],
                             'carried':before['private']['inventories'],
                             'seeds':before['private']['seeds'],
                             'seeds_after':dict(after.private['seeds']),
                             'prices':before['market']['prices'],
                             'market':action['market'],'operations':operations})
    reports.append({'replay':filename,'seed':seed,'kind':'saved action replay only; not a new policy game',
                    'through_step':191,'timeline':timeline})
out=ROOT/'research/round8/top2/seed_timing_audit.json'
out.write_text(json.dumps(reports,indent=2),encoding='utf-8')
for r in reports:
    print(r['replay'])
    for t in r['timeline']:
        if t['step']>=168:
            print(t['step'],t['money'],t['money_after'],
                  {k:v for k,v in t['shed'].items() if v},
                  {k:v for k,v in t['seeds'].items() if v},t['market'])
