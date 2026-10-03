"""Exercise action safety of the new conditional/holding policies."""
from pathlib import Path
import copy,json,runpy
B=Path(__file__).resolve().parent;R=B.parents[2];reports=[]
for spec in json.loads((B/'second_generation.json').read_text()):
    ns=runpy.run_path(str(R/spec['path']))['market_bc_agent'].__globals__
    assert [v for v in ns.values() if callable(v)][-1].__name__=='market_bc_agent'
    ns['_mbc_features']=lambda context,item:[0.0]*45
    ns['_mbc_predict']=lambda features:[1.0,1.0]
    obs=dict(player=0,step=250,market={'prices':{i:100 for i in ns['_MBC_ITEMS']}})
    action=dict(farmer=['PASS'],hands=[],market=[['HIRE'],['SELL','MILK',2]])
    context=dict(projected={'MILK':10},own={'money':20000},total=10,non_sells=[['HIRE']])
    fn=ns['_mbc_advise'];out=fn(obs,copy.deepcopy(action),context)
    assert out['market']==[['HIRE'],['SELL','MILK',10]] and out['farmer']==['PASS']
    assert fn(obs,action,dict(context,own={'money':1}))==action
    assert fn(dict(obs,step=718),action,context)==action
    full=dict(action,market=[['HIRE']]*10)
    assert fn(obs,full,context)==full
    ns['_mbc_predict']=lambda features:[.01,0.0]
    assert fn(obs,action,context)==action
    holding=dict(action,market=[['SELL','MILK',10]])
    out=fn(obs,holding,dict(context,non_sells=[]))
    expected=2 if spec['settings']['hold'] else 10
    assert out['market']==[['SELL','MILK',expected]],(spec['name'],out)
    reports.append(dict(candidate=spec['name'],passed=True,checks=7))
(B/'second_policy_checks.json').write_text(json.dumps(dict(passed=True,results=reports),indent=2),encoding='utf-8')
print(json.dumps(reports),flush=True)
