"""Check new policy isolation, shadow equivalence, and declared production assumptions."""
from pathlib import Path
import contextlib,copy,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1];BASE='submissions/release_v10_r2/main.py'
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
names=['repeat_v2_one.py','g3_correct_future.py','g3_robust.py','g3_native_sales.py']
checks=[]
for name in names:
    entry=fa.load('research/meta_rebuild_20260927/candidates/'+name);native=fa.load(BASE)
    ns=entry.__globals__;ns['_K28S_LIMIT']=0
    state,env=fa.new_game(19283017);same=0
    old_schedule=ns['_hd2_schedule'];old_future=ns['_HD2_FUTURE']
    for step in range(719):
        obs=copy.deepcopy(state[0].observation);obs.step=step
        action=entry(copy.deepcopy(obs),env.configuration);reference=native(copy.deepcopy(obs),env.configuration)
        assert action==reference,(name,step)
        assert ns['_hd2_schedule'] is old_schedule and ns['_HD2_FUTURE']==old_future
        same+=1
        for i in (0,1):state[i].observation.step=step;state[i].action=copy.deepcopy(reference)
        fa.engine.interpreter(state,env)
    checks.append(dict(candidate=name,shadow_actions_equal=same,valuation_globals_restored=True))
    print(json.dumps(checks[-1]),flush=True)
    if '_k28v_gain' in ns:
        ns['_k28v_gain'](1,obs,{})
        assert ns['_hd2_schedule'] is old_schedule and ns['_HD2_FUTURE']==old_future
        saved=ns['_HD2_CARE'];ns['_HD2_CARE']=1.0
        for animal in ('COW','SHEEP','GOOSE'):
            farm=fa.engine._new_farm(10,3000);farm['tiles'][4][4]=fa.engine._new_animal(animal,0)
            observed={}
            for day in range(29):
                tile=farm['tiles'][4][4];tile['fed_today']=True;tile['cared_today']=True
                fa.engine._daily_refresh_animals(farm,day)
                q=tile.get('yield_units',0)
                if q:observed[day+1]=q;tile['yield_units']=0
            expected=ns['_k28v_schedule'](animal,0,1)
            assert observed==expected,(animal,observed,expected)
        ns['_HD2_CARE']=saved
        checks[-1]['all_three_fully_cared_schedules_match_engine']=True
(D/'herd_g3_contract_checks_20260928.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(dict(complete=True,shadow_comparisons=sum(c['shadow_actions_equal'] for c in checks),schedules_checked=9)),flush=True)
