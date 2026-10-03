import sys,io,contextlib,json,gzip,collections
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
    import kaggle_environments.envs.kaggriculture.kaggriculture as K
from anal import load
LOG=[];CUR={}
_opm=K._process_market
def pm(state,env):
    CUR['f']=state[0].observation.farms
    return _opm(state,env)
K._process_market=pm
def who(farm):
    fs=CUR.get('f') or []
    for i,f in enumerate(fs):
        if f is farm: return i
    return None
_orig=K._commit_unit
def patched(op,item,price,farm,private,market,cap=100):
    ok=_orig(op,item,price,farm,private,market,cap)
    if ok: LOG.append((who(farm),op,item,price))
    return ok
K._commit_unit=patched
_oh=K._do_hire
def hire(farm,private,bs,mult=1):
    before=farm['money'];_oh(farm,private,bs,mult)
    if farm['money']<before: LOG.append((who(farm),'HIRE','',before-farm['money']))
K._do_hire=hire
_ol=K._do_buy_land
def land(farm,bs):
    before=farm['money'];_ol(farm,bs)
    if farm['money']<before: LOG.append((who(farm),'LAND','',before-farm['money']))
K._do_buy_land=land
def resim(eid):
    g=load(eid);names=g['info']['TeamNames']
    tapes=[[g['steps'][t+1][p]['action'] for t in range(719)] for p in range(2)]
    def mk(p):
        def a(obs,cfg=None): return tapes[p][obs['step']]
        return a
    env=make('kaggriculture',configuration={'episodeSteps':720});env.info['seed']=g['info']['seed']
    LOG.clear()
    env.run([mk(0),mk(1)])
    farms=env.steps[-1][0].observation.farms
    fid={id(env.state[0].observation.farms[i]):i for i in range(2)}
    final=[env.steps[-1][i].observation.farms[i]['money'] for i in range(2)]
    print('EP',eid,names,'replay',g['rewards'],'resim',final)
    agg=[collections.defaultdict(lambda:[0,0.0]) for _ in range(2)]
    for f,op,item,price in LOG:
        p=f
        if p is None: continue
        k=op+':'+item; agg[p][k][0]+=1; agg[p][k][1]+=price
    keys=sorted(set(agg[0])|set(agg[1]))
    print(f'{"":22s} {names[0][:20]:>28s} {names[1][:20]:>28s}')
    for k in keys:
        a,b=agg[0].get(k,[0,0]),agg[1].get(k,[0,0])
        print(f'{k:22s} {a[0]:6d} {a[1]:9.0f} ({a[1]/max(1,a[0]):5.1f}) {b[0]:6d} {b[1]:9.0f} ({b[1]/max(1,b[0]):5.1f})')
    return agg
if __name__=='__main__':
    for e in sys.argv[1:]: resim(int(e))
