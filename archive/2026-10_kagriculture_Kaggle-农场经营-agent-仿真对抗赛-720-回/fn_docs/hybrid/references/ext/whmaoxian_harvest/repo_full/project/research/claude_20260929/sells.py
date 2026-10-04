import sys,io,contextlib,json,collections
import resim as R
K=R.K
STEP={'t':0}
_oi=K.interpreter
def interp(state,env):
    STEP['t']=state[0].observation.get('step',0) if hasattr(state[0].observation,'get') else 0
    return _oi(state,env)
LOG2=[]
_oc=R.patched
def patched2(op,item,price,farm,private,market,cap=100):
    inv=market['inventory'][item] if item in market['inventory'] else None
    ok=_oc(op,item,price,farm,private,market,cap)
    if ok and op=='SELL': LOG2.append((STEP['t'],R.who(farm),item,price,inv))
    return ok
K._commit_unit=patched2
import kaggle_environments.envs.kaggriculture.kaggriculture as KK
def run(eid,items):
    LOG2.clear()
    # hook step via _process_market wrapper
    orig=K._process_market
    def pm(state,env):
        STEP['t']=state[0].observation['step']; return orig(state,env)
    K._process_market=pm
    R.resim(eid)
    K._process_market=orig
    g=R.load(eid);names=g['info']['TeamNames']
    for item in items:
        print('#####',item)
        # group consecutive units per (step,player)
        grp=collections.OrderedDict()
        for t,p,it,pr,inv in LOG2:
            if it!=item: continue
            k=(t,p);grp.setdefault(k,[]).append((pr,inv))
        for (t,p),v in grp.items():
            print(f'  d{t//24:2d}h{t%24:2d} P{p}{names[p][:6]:6s} n={len(v):3d} px {v[0][0]}->{v[-1][0]} inv0={v[0][1]}')
if __name__=='__main__':
    run(int(sys.argv[1]),sys.argv[2].split(','))
