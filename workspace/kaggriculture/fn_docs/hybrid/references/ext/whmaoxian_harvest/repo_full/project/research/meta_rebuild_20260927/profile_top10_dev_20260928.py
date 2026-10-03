"""Exact economic profiles for the newly fetched top-ten development demonstrations."""
from pathlib import Path
import gzip,json,runpy
D=Path(__file__).resolve().parent;F=D/'top10_dev_20260928'
ns=runpy.run_path(str(D/'audit_midgame_income_20260928.py'),run_name='audit_library')
ns['audit'].__globals__['F']=F
views=json.loads((F/'selection.json').read_text())['views'];cache={};profiles=[]
for view in views:
    eid=view['episode'];seat=view['seat']
    if eid not in cache:cache[eid]=ns['audit'](dict(episode=eid))
    audited=cache[eid];daily=[]
    for day in audited['daily']:
        if day['step'] not in (120,240,360,480,600,719):continue
        s=day['cumulative'][seat]
        income={i:s['revenue'].get(i,0)-s['purchases'].get('BUY_PRODUCT:'+i,0) for i in set(s['revenue'])|{'WHEAT','FERTILIZER'}}
        daily.append(dict(step=day['step'],cash=day['cash'][seat],mix=day['mix'][seat],net_trade_income=income,wages=s['wages'],purchases=s['purchases']))
    game=json.loads(gzip.decompress((F/f'{eid}.json.gz').read_bytes()));changes=[]
    for step in range(360):
        action=game['steps'][step+1][seat]['action'] or {}
        orders=[o for o in action.get('market',[]) if o and o[0] in ('BUY_ANIMAL','BUY_LAND')]
        if orders:changes.append(dict(step=step,orders=orders))
    record=dict(view,verified_transitions=audited['all_719_transitions_equal'],reward=audited['rewards'][seat],daily=daily,investment_actions=changes)
    profiles.append(record)
    print(json.dumps(dict(team=view['team'],episode=eid,reward=record['reward'],day10=daily[1]['mix'],net_income=daily[-1]['net_trade_income'])),flush=True)
(F/'economic_profiles.json').write_text(json.dumps(profiles,indent=2))
print(json.dumps(dict(complete=True,verified_unique_replays=len(cache),views=len(profiles))),flush=True)
