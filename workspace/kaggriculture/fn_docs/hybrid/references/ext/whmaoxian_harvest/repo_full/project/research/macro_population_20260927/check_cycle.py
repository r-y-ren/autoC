"""Official market mechanics and bounded-action contract checks."""
from pathlib import Path
import contextlib,copy,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):import fast_arena as fa
checks=[]
def market_case(ours,other):
    state,env=fa.new_game(17)
    for s in state:s.observation.private['shed']['WHEAT']=30
    state[0].action={'market':ours};state[1].action={'market':other}
    fa.engine._process_market(state,env)
    return [f['money'] for f in state[0].observation.farms],[dict(s.observation.private['shed']) for s in state],dict(state[0].observation.market['inventory'])
for side,opponent in [('BUY_PRODUCT','BUY_PRODUCT'),('SELL','SELL')]:
    second='SELL' if side=='BUY_PRODUCT' else 'BUY_PRODUCT'
    cycle=[[side,'WHEAT',8],[second,'WHEAT',8]]
    solo=market_case(cycle,[]);nothing=market_case([],[])
    assert solo==nothing
    for slot in (0,1):
        other=[[]]*slot+[[opponent,'WHEAT',8]]
        before=market_case([],other);after=market_case(cycle,other)
        assert after[1]==before[1] and after[2]==before[2]
        assert after[0][0]>=before[0][0]
        checks.append(dict(direction=side,opponent_slot=slot,own_gain=after[0][0]-before[0][0],opponent_gain=after[0][1]-before[0][1]))
entry=fa.load('research/macro_population_20260927/cycle_agents/p50_q8.py');ns=entry.__globals__
