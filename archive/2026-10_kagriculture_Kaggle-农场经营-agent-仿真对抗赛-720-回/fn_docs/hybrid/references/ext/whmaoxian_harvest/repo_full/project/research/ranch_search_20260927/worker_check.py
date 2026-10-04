"""Synthetic physical-chore checks using the unchanged official game functions."""
from pathlib import Path
import contextlib,copy,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):import fast_arena as fa
records=[]
for animal in ('SHEEP','COW','GOOSE'):
    for count in (2,3,4):
        fn=fa.load('research/ranch_search_20260927/candidates/disabled.py');ns=fn.__globals__
        state,env=fa.new_game(17);obs=state[0].observation;farm=obs['farms'][0];private=obs['private']
        sites=ns['_RN_SITES'][:count];farm['unlocked_quadrants']=['NW','NE','SW','SE']
        for x,y in ns['_RN_SITES']:farm['tiles'][y][x]=None
        context={'animal':animal,'sites':sites};days=[]
        private['shed'][animal]=count
        for day in range(12,29):
            farm['hands']=[[4,4]];private['inventories']=[{},{}];private['shed']['WHEAT']=12
            for hour in range(2,24):
                obs['step']=day*24+hour;command=ns['_rn_worker'](obs,1,context,dict(private['shed']))
                fa.engine._apply_unit_action(farm,private,1,command,10,day,24,100)
            tiles=[farm['tiles'][y][x] for x,y in sites]
            days.append({'day':day,'placed':sum(isinstance(t,dict) and t.get('animal')==animal for t in tiles),'fed':sum(isinstance(t,dict) and t.get('fed_today',False) for t in tiles),'cared':sum(isinstance(t,dict) and t.get('cared_today',False) for t in tiles)})
            fa.engine._daily_refresh_animals(farm,day)
        records.append({'animal':animal,'count':count,'days':days,'all_placed':days[-1]['placed']==count,'all_fed_after_setup':all(d['fed']==count for d in days[1:]),'all_cared_after_setup':all(d['cared']==count for d in days[1:])})
(D/'worker_checks.json').write_text(json.dumps(records,indent=2));print(json.dumps([{k:v for k,v in r.items() if k!='days'} for r in records]),flush=True)
