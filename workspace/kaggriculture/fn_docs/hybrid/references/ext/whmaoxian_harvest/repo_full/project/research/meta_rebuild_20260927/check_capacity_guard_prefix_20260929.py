"""Exact single-turn checks against public replay observations and official transitions."""
from pathlib import Path
import contextlib,copy,gzip,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
variants=json.loads((D/'capacity_design_20260929.json').read_text())['variants'];reports=[]
checks=[(114242169,0,575),(114197750,0,671),(114277466,1,623),(114289716,1,575)]
def transition(game,step,own,changed=None):
    state,env=fa.new_game(game['info']['seed'],config=game['configuration'])
    for turn in range(step+1):
        for seat in (0,1):
            state[seat].observation.step=turn
            action=changed if turn==step and seat==own and changed is not None else game['steps'][turn+1][seat]['action']
            state[seat].action=copy.deepcopy(action)
        fa.engine.interpreter(state,env)
    return state
for episode,seat,step in checks:
    game=json.loads(gzip.decompress((D/'r2_feedback'/f'{episode}.json.gz').read_bytes()))
    original=game['steps'][step+1][seat]['action'];obs=copy.deepcopy(game['steps'][step][seat]['observation']);obs['step']=step
    base=transition(game,step,seat)
    expected=game['steps'][step+1][seat]['observation']
    assert base[seat].observation.farms==expected['farms']
    assert base[seat].observation.private==expected['private']
    for v in variants:
        fn=fa.load(v['path']);ns=fn.__globals__
        action=ns['_k29c_capacity_action'](copy.deepcopy(obs),copy.deepcopy(original))
        result=transition(game,step,seat,action)
        own=result[seat].observation.farms[seat];base_own=base[seat].observation.farms[seat]
        assert {k:x for k,x in own.items() if k!='money'}=={k:x for k,x in base_own.items() if k!='money'}
        assert own['money']>=base_own['money']
        assert sum(result[seat].observation.private['shed'].values())<=100
        reports.append(dict(episode=episode,step=step,candidate=v['name'],changed=action!=original,cash_gain=own['money']-base_own['money'],report=ns['_K29C_REPORT'],baseline_reproduced=True,physical_state_unchanged=True))
(D/'capacity_unit_checks_20260929.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
print(json.dumps(dict(checks=len(reports),changed=sum(r['changed'] for r in reports),results=reports)),flush=True)
