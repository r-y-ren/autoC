"""Check the feeding predicate against unchanged official animal transitions."""
from pathlib import Path
import contextlib,copy,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):import fast_arena as fa
entry=fa.load('research/meta_rebuild_20260927/candidates/late_feed.py');ns=entry.__globals__
checked=0;eligible=0
for animal in ('GOOSE','COW','SHEEP'):
    for placed in range(29):
        for unfed in (0,1):
            for held in (0,2,4):
                tile={'kind':'COOP' if animal=='GOOSE' else 'PASTURE','animal':animal,'placed_day':placed,'yield_units':held,'consecutive_unfed':unfed,'fed_today':False,'cared_today':True,'fertilizer_available':False,'pending_care_bonus':3}
                checked+=1
                if not ns['_tf_no_feed_benefit'](tile,28):continue
                eligible+=1;a={'tiles':[[copy.deepcopy(tile)]]};b=copy.deepcopy(a)
                a['tiles'][0][0]['fed_today']=True
                fa.engine._daily_refresh_animals(a,28);fa.engine._daily_refresh_animals(b,28)
                assert a['tiles'][0][0].get('animal')==b['tiles'][0][0].get('animal')==animal
                assert a['tiles'][0][0]['yield_units']==b['tiles'][0][0]['yield_units']
                assert a['tiles'][0][0]['fertilizer_available']==b['tiles'][0][0]['fertilizer_available']
report=dict(passed=True,states_checked=checked,eligible_transitions=eligible,scope='Day28-to29 physical preservation under the predicate; no future midnight occurs before the standard episode ends. Not match-strength evidence.')
(D/'husbandry_unit_checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
