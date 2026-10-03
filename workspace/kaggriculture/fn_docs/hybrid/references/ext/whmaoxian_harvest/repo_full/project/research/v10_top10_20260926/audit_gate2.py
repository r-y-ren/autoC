"""Observe qualification and executed production from fresh, in-process games."""
from pathlib import Path
import copy,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as a
candidate='research/v10_top10_20260926/tomato_gate2/r0_g500.py'
seeds=json.loads((D/'route_expansion_design.json').read_text())['seeds']
records=[]
for seed in seeds:
    entries=[a.load(candidate),a.load('submissions/release_v10_r2/main.py')]
    state,env=a.new_game(seed)
    for step in range(433):
        for seat,fn in enumerate(entries):
            obs=copy.deepcopy(state[seat].observation);obs.step=step
            state[seat].action=fn(obs,env.configuration)
        a.engine.interpreter(state,env)
        for s in state:s.observation.step=step+1
    ns=entries[0].__globals__;f=state[0].observation.farms[0]
    row=dict(seed=seed,money=f['money'],quadrants=f['unlocked_quadrants'],shops=state[0].observation.town['unlocked_shops'],forecast=ns['_TG_DECISIONS'].get(0),gate=ns['_TG_REPORT'],production=ns['_T19_REPORT'],original=ns['_CXTB_REPORT'],same_namespace=ns['_v219_request'].__globals__ is ns)
    records.append(row)
    print(json.dumps(row),flush=True)
(D/'gate2_prefix_audit.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
