"""Emission ledger contracts in fresh, isolated agent namespaces."""
from pathlib import Path
import contextlib,copy,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):import fast_arena as fa
results=[]
for v in json.loads((D/'stream_candidates.json').read_text()):
    fn=fa.load(v['path']);ns=fn.__globals__;state,env=fa.new_game(84542791)
    obs=copy.deepcopy(state[0].observation);obs['step']=216;obs['private']['shed']['MILK']=8
    action={'farmer':['PASS'],'hands':[],'market':[['SELL','MILK',5]]}
    previous={'step':216,'own':{'MILK':0},'left':{'MILK':8}}
    ns['_V9_RACE'][0]={'prev':previous}
    ns['_MS_PARENT']=lambda observation,configuration=None:action
    before=copy.deepcopy(obs);result=fn(obs,env.configuration)
    assert result is action and obs==before
    assert previous['own']['MILK']==(5 if v['sync'] else 0)
    assert previous['left']['MILK']==(3 if v['sync'] else 8)
    streams=ns['_v92_q_streams']()
    assert len(streams)==(20 if v['library'] else 0)
    assert all(150<=t<699 and 0<=i<3 and q>=2 for _,ev in streams for (t,i),q in ev.items())
    results.append(dict(candidate=v['name'],passed=True,checks=4))
(D/'stream_unit_checks.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results),flush=True)
