"""Test slot objective against unchanged official market matching."""
from pathlib import Path
from collections import Counter
import copy,hashlib,itertools,json,random,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as arena
candidate='research/v10_top10_20260926/slot_candidates/s1_margin.py'
entry=arena.load(candidate);ns=entry.__globals__;rng=random.Random(9272026)
checks=0
for trial in range(60):
    state,env=arena.new_game(100+trial)
    item=ns['FLOW_ITEMS'][trial%7];q=rng.randrange(1,21);slot=rng.randrange(10)
    opponent=[rng.randrange(5) for _ in range(10)]
    state[0].observation.private['shed'][item]=q
    state[1].observation.private['shed'][item]=sum(opponent)
    stock=state[0].observation.market['inventory'][item]+rng.choice([-20,0,10,50,200])
    state[0].observation.market['inventory'][item]=stock
    orders=[[] for _ in range(10)];orders[slot]=['SELL',item,q]
    state[0].action=dict(market=orders)
    state[1].action=dict(market=[['SELL',item,v] if v else [] for v in opponent])
    params=ns['_v44y_params'](state[0].observation)
    predicted=ns['_sp_value'](item,q,slot,opponent,stock,params)
    money=[state[0].observation.farms[i]['money'] for i in (0,1)]
    arena.engine._process_market(state,env)
    actual=(state[0].observation.farms[0]['money']-money[0])-(state[0].observation.farms[1]['money']-money[1])
    assert abs(actual-predicted)<1e-7,(trial,item,actual,predicted)
    checks+=1
assignment_checks=0
for size in range(2,7):
    for trial in range(6):
        scores=[[rng.random()*100 for _ in range(size)] for _ in range(size)]
        score,order=ns['_sp_assignment'](scores)
        best=max(sum(scores[i][p[i]] for i in range(size)) for p in itertools.permutations(range(size)))
        assert abs(score-best)<1e-7 and sorted(order)==list(range(size))
        assignment_checks+=1
state,env=arena.new_game(918);obs=state[0].observation;obs['step']=400
obs['private']['shed'].update(STRAWBERRY=10,MILK=10,WOOL=10)
action=dict(farmer=['PASS'],hands=[],market=[['SELL','MILK',5],['SELL','STRAWBERRY',5],['BUY_SEED','WHEAT',1],['SELL','WOOL',2]])
predictions={i:[0]*10 for i in ns['FLOW_ITEMS']};predictions['STRAWBERRY'][1]=10
changed=ns['_sp_reorder'](obs,action,predictions)
assert Counter(map(tuple,action['market']))==Counter(map(tuple,changed['market']))
assert action['market'][2]==changed['market'][2] and action['market'][3]==changed['market'][3]
assert action['farmer']==changed['farmer'] and action['hands']==changed['hands']
report=dict(passed=True,official_market_comparisons=checks,assignment_bruteforce_comparisons=assignment_checks,order_quantities_and_fixed_slots_preserved=True,source_sha256=hashlib.sha256((R/candidate).read_bytes()).hexdigest(),scope='Synthetic objective and invariance checks; not strength evidence.')
(D/'slot_unit_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)
