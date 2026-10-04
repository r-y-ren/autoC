"""Mechanism checks only; no claims of match strength."""
from pathlib import Path
import copy,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as fa
variants=json.loads((D/'population_g1.json').read_text())
chosen=next(v for v in variants if v['genome']['initial_care'])
entry=fa.load(chosen['path']);ns=entry.__globals__;ns['_HD2_CARE']=1.0
records=[]
for animal in ('GOOSE','COW','SHEEP'):
    tile=fa.engine._new_animal(animal,0) if hasattr(fa.engine,'_new_animal') else None
    if tile is None:
        tile=dict(kind=fa.engine.ANIMALS[animal]['structure'],animal=animal,placed_day=0,yield_units=0,consecutive_unfed=0,fed_today=False,cared_today=False,fertilizer_available=False,pending_care_bonus=0)
    farm={'tiles':[[tile]]};actual={}
    for day in range(29):
        tile['fed_today']=True;tile['cared_today']=True
        fa.engine._daily_refresh_animals(farm,day)
        if tile['yield_units']:actual[day+1]=tile['yield_units'];tile['yield_units']=0
    predicted=ns['_hd2_schedule'](animal,0,1)
    assert actual==predicted,(animal,actual,predicted)
    old=ns['_MP_ORIGINAL_SCHEDULE'](animal,0,1)
    records.append(dict(animal=animal,first_actual=next(iter(actual.values())),old_first=next(iter(old.values())),new_first=next(iter(predicted.values())),exact_daily_collection_assumption=True))
(D/'lifecycle_checks.json').write_text(json.dumps(dict(passed=True,cases=records,scope='Fed and cared daily, all output harvested each production boundary; not a live revenue forecast.'),indent=2))
print(json.dumps(records))
