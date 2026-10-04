"""Compile public demonstrated premium sales; no private live state or seed features."""
from pathlib import Path
import contextlib,gzip,hashlib,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):import fast_arena as fa
entry=fa.load('submissions/release_v10_r2/main.py');ns=entry.__globals__
views=json.loads((D/'recent_selection.json').read_text())['views'];items=('MILK','WOOL','STRAWBERRY')
streams=[];sources=[]
for v in views:
    path=D/f"recent_replays/{v['episode']}.json.gz";raw=gzip.decompress(path.read_bytes());game=json.loads(raw)
    events=[]
    for step in range(150,699):
        obs=dict(game['steps'][step][v['seat']]['observation']);obs['step']=step
        action=game['steps'][step+1][v['seat']]['action']
        stock=ns['projected_shed'](action,ns['FarmView'](obs))
        for i,item in enumerate(items):
            orders=action.get('market',[])[:10]
            requested=sum(max(0,int(o[2])) for o in orders if len(o)>=3 and o[:2]==['SELL',item])
            quantity=min(max(0,int(stock.get(item,0))),requested)
            if quantity>=2 and obs['market']['prices'][item]>3:events.append([step,i,quantity])
    streams.append(events)
    sources.append(dict(episode=v['episode'],seat=v['seat'],team=v['team'],sha256=hashlib.sha256(raw).hexdigest(),events=len(events)))
assert len(streams)==20 and all(streams)
result=dict(streams=streams,source_records=sources,items=items,scope='Historical development samples only. Runtime stores ordinal streams, not team names or episode/world identifiers.')
(D/'recent_streams.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(dict(streams=len(streams),events=sum(map(len,streams)))),flush=True)
