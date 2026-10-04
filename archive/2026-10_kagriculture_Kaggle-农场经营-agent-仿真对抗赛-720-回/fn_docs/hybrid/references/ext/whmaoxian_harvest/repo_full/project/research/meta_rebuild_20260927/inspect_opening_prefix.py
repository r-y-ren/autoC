"""Inspect a short original-policy prefix under standard full-game configuration."""
from pathlib import Path
import contextlib,copy,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):import fast_arena as fa
state,env=fa.new_game(1991468825)
entries=[fa.load('submissions/release_v10_r2/main.py'),fa.load('research/v10_rebuild_20260926/notebooks/extracted/fieldcraft/single_file.py')]
snap=[]
for step in range(120):
    for seat,fn in enumerate(entries):
        state[seat].observation.step=step
        state[seat].action=fn(copy.deepcopy(state[seat].observation),env.configuration)
    if step in (0,1,48,49,50,51,52,53,54,55,87,91,96,97,98,99,100,101,102,103,104,105):
        o=state[0].observation;f=o.farms[0];a=state[0].action
        snap.append(copy.deepcopy(dict(step=step,cash=f['money'],prices=o.market['prices'],
            crop_site=f['tiles'][4][2],cow_site=f['tiles'][4][4],
            actors=list(zip([f['farmer']]+f['hands'],[a['farmer']]+a['hands'])),market=a['market'],bags=o.private['inventories'])))
    fa.engine.interpreter(state,env)
    for s in state:s.observation.step=step+1
(D/'opening_prefix_audit.json').write_text(json.dumps(dict(steps=120,scope='Prefix inspection only, not a completed game.',snapshots=snap),indent=2))
dm=fa.load('research/meta_rebuild_20260927/public_agents/dmitrii.py');s,e=fa.new_game(104851)
print(json.dumps(dict(dmitrii_entry=dm.__name__,dmitrii_opening=dm(s[0].observation,e.configuration),snapshots=[x for x in snap if x['step'] in (49,50,51,96,98,100,102)])),flush=True)
