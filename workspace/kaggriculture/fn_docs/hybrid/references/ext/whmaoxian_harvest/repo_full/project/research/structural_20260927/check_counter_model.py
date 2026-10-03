"""Compare the one-turn model against unmodified official game market rules."""
from pathlib import Path
import contextlib,copy,hashlib,io,json,random,sys
P=Path(__file__).resolve().parent;R=P.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
fn=fa.load('submissions/release_v10_r2/main.py');ns=fn.__globals__
source=(P/'counter_market_model.txt').read_text();exec(compile(source,'counter_market_model','exec'),ns)
rng=random.Random(49017);checks=[]
for trial in range(180):
    seat=trial%2;state,env=fa.new_game(910001+trial)
    obs=fa.Attr(dict(state[0].observation));obs['player']=seat;obs['step']=0;obs['private']=state[seat].observation.private
    for p in (0,1):
        state[p].observation.private['shed'].update(WHEAT=rng.randrange(0,35),FERTILIZER=rng.randrange(0,35),MILK=rng.randrange(0,20),STRAWBERRY=rng.randrange(0,10))
        obs.farms[p]['money']=float(rng.choice([50,200,3000,15000]))
    for item in obs.market['inventory']:obs.market['inventory'][item]=10000+rng.randrange(-120,650)
    fa.engine._refresh_prices(obs.market)
    orders=[]
    for p in (0,1):
        out=[]
        for i in range(rng.randrange(0,9)):
            op=rng.choice(('SELL','BUY_PRODUCT','HIRE','BUY_LAND','BUY_ANIMAL','BUY_SEED'))
            item=rng.choice(('WHEAT','FERTILIZER')) if op=='BUY_PRODUCT' else rng.choice(('WHEAT','FERTILIZER','MILK','STRAWBERRY'))
            if op=='BUY_SEED':item=rng.choice(('WHEAT','CARROT','MELON'))
            if op=='BUY_ANIMAL':item=rng.choice(('COW','SHEEP','GOOSE'))
            out.append([op] if op in ('HIRE','BUY_LAND') else [op,item,rng.randrange(1,30)])
        orders.append(out)
    predicted=ns['_mc_run'](obs,dict(obs.private['shed']),orders[seat],orders[1-seat],dict(state[1-seat].observation.private['shed']))
    for p in (0,1):state[p].action={'farmer':['PASS'],'hands':[],'market':orders[p]}
    fa.engine._process_market(state,env)
    expected={'money':[obs.farms[seat]['money'],obs.farms[1-seat]['money']],
              'warehouse':[dict(obs.private['shed']),dict(state[1-seat].observation.private['shed'])],
              'inventory':dict(obs.market['inventory'])}
    assert predicted['money']==expected['money'],(trial,'money',predicted,expected)
    for a,b in zip(predicted['warehouse'],expected['warehouse']):
        assert all(a.get(k,0)==b.get(k,0) for k in set(a)|set(b)),(trial,'warehouse',a,b)
    assert predicted['inventory']==expected['inventory'],(trial,'market',predicted,expected)
    checks.append({'trial':trial,'seat':seat,'passed':True})
(P/'counter_model_checks.json').write_text(json.dumps(dict(passed=True,checks=checks,source_sha256=hashlib.sha256(source.encode()).hexdigest(),scope='One-turn execution parity with explicit inventories; not forecast accuracy.'),indent=2))
print(json.dumps(dict(passed=True,randomized_market_checks=len(checks))),flush=True)
