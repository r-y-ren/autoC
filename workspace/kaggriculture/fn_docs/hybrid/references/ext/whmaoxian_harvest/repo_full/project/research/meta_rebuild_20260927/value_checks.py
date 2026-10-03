"""Small mechanism checks before complete games; not strength evidence."""
from pathlib import Path
import contextlib,copy,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):import fast_arena as fa
checks=[]
for row in json.loads((D/'value_candidates.json').read_text()):
    fn=fa.load(row['path']);ns=fn.__globals__;state,env=fa.new_game(765412321)
    obs=copy.deepcopy(state[0].observation);obs['step']=216;obs['farms'][0]['money']=20000;obs['private']['shed']['MILK']=8
    action={'farmer':['PASS'],'hands':[],'market':[]};before=copy.deepcopy(action)
    context=ns['_mbc_context'](obs,action,dict(obs['private']['shed']),{});internal={'last_changed':-1000}
    prediction=ns['_vp_predict'];ns['_vp_predict']=lambda x:(100,1)
    result=ns['_vp_propose'](obs,action,context,internal)
    assert action==before and result['farmer']==action['farmer'] and result['hands']==action['hands'] and len(result['market'])<=10
    if row['settings']['shadow']:assert result is action
    else:assert 0<sum(o[2] for o in result['market'])<=8
    for kind in ('low_cash','late','purchase','pickup'):
        o=copy.deepcopy(obs);a=copy.deepcopy(action)
        if kind=='low_cash':o['farms'][0]['money']=100
        if kind=='late':o['step']=718
        if kind=='purchase':a['market']=[['BUY_PRODUCT','WHEAT',1]]
        if kind=='pickup':a['farmer']=['PICKUP','MILK',1]
        c=ns['_mbc_context'](o,a,dict(o['private']['shed']),{})
        assert ns['_vp_propose'](o,a,c,{'last_changed':-1000}) is a
    ns['_vp_predict']=prediction;checks.append(dict(name=row['name'],passed=True,checks=5))
(D/'value_unit_checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks),flush=True)
