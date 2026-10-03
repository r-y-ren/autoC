"""Compare local settlement formulas to the unmodified official market processor."""
from pathlib import Path
import contextlib,copy,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
entry=fa.load('research/meta_rebuild_20260927/candidates/order_native.py');ns=entry.__globals__
base,env=fa.new_game(417);cases=checks=0;failures=[]
for item in fa.engine.PRODUCTS:
    for offset in (-600,-100,-1,0,1,60,300,600):
        inventory=10000+offset
        for q,r in ((1,1),(5,11),(11,5),(25,25)):
            for op in (('SELL','BUY_PRODUCT') if item in ('WHEAT','FERTILIZER') else ('SELL',)):
                for relation in (-1,0,1):
                    state=copy.deepcopy(base)
                    for seat in (0,1):
                        state[seat].observation.private=fa.engine._new_private()
                        state[0].observation.farms[seat]['money']=1000000.
                    state[0].observation.private['shed'][item]=q
                    if op=='SELL':state[1].observation.private['shed'][item]=r
                    state[0].observation.market['inventory'][item]=inventory
                    left=[['SELL',item,q]];right=[[op,item,r]]
                    if relation<0:right=[[]]+right
                    elif relation>0:left=[[]]+left
                    state[0].action={'market':left};state[1].action={'market':right}
                    fa.engine._process_market(state,env)
                    own=state[0].observation.farms[0]['money']-1000000
                    other=state[0].observation.farms[1]['money']-1000000
                    for alpha in (0.,1.):
                        prices={'fn':lambda index:ns['_r37_market_price'](item,index,fa.engine.MARKET_PARAMS)}
                        predicted=ns['_k29o_pair'](prices,inventory,q,op,r,relation,alpha)
                        actual=own-alpha*other;checks+=1
                        if abs(predicted-actual)>1e-6:failures.append(dict(item=item,offset=offset,q=q,r=r,op=op,relation=relation,alpha=alpha,predicted=predicted,actual=actual))
                    cases+=1
report=dict(cases=cases,checks=checks,mismatches=len(failures),examples=failures[:10],scope='Market-only unit checks with abundant cash and explicit feasible inventories. Opponent-order forecasts themselves are not validated by this test.')
(D/'order_assignment_unit_checks_20260929.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report),flush=True)
assert not failures
