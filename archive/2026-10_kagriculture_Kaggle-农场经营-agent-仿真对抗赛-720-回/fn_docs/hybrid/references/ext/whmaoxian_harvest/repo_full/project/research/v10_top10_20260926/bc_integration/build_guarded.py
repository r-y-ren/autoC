"""Build and test conservative protection of existing sale reservations."""
from pathlib import Path
import hashlib,json,runpy
B=Path(__file__).resolve().parent;R=B.parents[2]
tail=(B/'reservation_guard_tail.txt').read_bytes();manifest=[]
for old in ('hold_p55_q8','balanced35','imitate25'):
    path=B/(old+'_guarded.py');data=(B/(old+'.py')).read_bytes()+tail
    compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    ns=runpy.run_path(str(path))['market_bc_agent'].__globals__
    ns['_mbc_features']=lambda context,item:[0.0]*45
    ns['_mbc_predict']=lambda features:[.01,0.0]
    obs=dict(player=0,step=250,market={'prices':{i:100 for i in ns['_MBC_ITEMS']}})
    action=dict(farmer=['PASS'],hands=[],market=[['SELL','MILK',10]])
    context=dict(projected={'MILK':10},own={'money':20000},total=10,non_sells=[])
    ns['_IMPL'].chassis.players[0]={'sell_state':{'r36_debts':{252:{'MILK':4}}}}
    assert ns['_mbc_advise'](obs,action,context) is action
    assert ns['_MBC_STATS']['held']==0
    ns['_IMPL'].chassis.players[0]={'sell_state':{'due_step':251,'suppress':{'MILK':4}}}
    assert ns['_mbc_advise'](obs,action,context) is action
    ns['_IMPL'].chassis.players[0]={'sell_state':{'r36_debts':{249:{'MILK':4}}}}
    assert ns['_mbc_advise'](obs,action,context)['market'][0][2]<10
    assert [v for v in ns.values() if callable(v)][-1].__name__=='market_bc_agent'
    manifest.append(dict(path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest(),reservation_contract_checks=5))
(B/'guarded_candidates.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(guarded_candidates=3,reservation_checks_passed=15)),flush=True)
