"""Causal decision and unchanged-prefix checks for complete-plan livestock variants."""
from pathlib import Path
import contextlib,copy,hashlib,io,json,sys
P=Path(__file__).resolve().parent;R=P.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
variants=json.loads((P/'livestock_manifest.json').read_text());checks=[]
for v in variants:
    entry=fa.load(v['path']);ns=entry.__globals__;start=v['settings']['start']
    for seat in (0,1):
        states,env=fa.new_game(41);obs=fa.Attr(dict(states[0].observation))
        obs['player']=seat;obs['private']=states[seat].observation.private;state={}
        rid=ns['_lm_router'](obs,0,state)
        pristine=copy.deepcopy(ns['_LM_ORIGINAL'])
        obs['step']=start;obs['town']['unlocked_shops']=['SMOOTHIE_SHOP','PIZZA_SHOP']
        chosen=ns['_lm_router'](obs,start,state)
        assert chosen==rid and ns['_PLAN_IMPL'].chassis.routes[rid][:start]==pristine[:start]
        assert state['mapping']=={'SHEEP':'COW'}
        for a in ns['_PLAN_IMPL'].chassis.routes[rid][start:]:
            assert not any(len(o)>=3 and o[:2]==['BUY_ANIMAL','SHEEP'] for o in a.get('market',[]))
        ns['_lm_router'](obs,0,{})
        assert ns['_PLAN_IMPL'].chassis.routes[rid]==pristine
        checks.append(dict(candidate=v['path'],seat=seat,prefix_steps=start,reset=True))
(P/'livestock_unit_checks.json').write_text(json.dumps(dict(passed=True,checks=checks,scope='Synthetic decision and prefix contracts; full matches remain separate.'),indent=2))
print(json.dumps(dict(passed=True,checks=len(checks))),flush=True)
