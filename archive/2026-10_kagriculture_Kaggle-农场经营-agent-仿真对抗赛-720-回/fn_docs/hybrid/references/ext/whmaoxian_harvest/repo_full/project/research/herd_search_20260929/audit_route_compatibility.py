"""Compare archived expert farm structures before considering any policy handoff."""
from pathlib import Path
import gzip,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];M=R/'research/meta_rebuild_20260927'
reference=json.loads(gzip.decompress((M/'r2_feedback/114242169.json.gz').read_bytes()))
selection=json.loads((M/'recent_selection.json').read_text())['views']
receipts={r['episode']:r for r in json.loads((M/'recent_receipts.json').read_text())}
def shape(farm):
    values=[]
    for row in farm['tiles']:
        for tile in row:
            if tile is None or isinstance(tile,dict) and tile.get('kind')=='WEED':values.append(None)
            elif isinstance(tile,dict):values.append(tuple(tile.get(k) for k in ('kind','crop','animal','planted_day','placed_day')))
            else:values.append(tile)
    return values
reports=[]
for view in selection:
    raw=gzip.decompress((M/'recent_replays'/f"{view['episode']}.json.gz").read_bytes());assert hashlib.sha256(raw).hexdigest()==receipts[view['episode']]['sha256']
    game=json.loads(raw);seat=view['seat'];matches={}
    for step in (0,24,48,72,144,192,240):
        a=shape(reference['steps'][step][0]['observation']['farms'][0]);b=shape(game['steps'][step][seat]['observation']['farms'][seat])
        matches[step]=sum(x!=y for x,y in zip(a,b))
    reports.append(dict(team=view['team'],rank=view['rank'],episode=view['episode'],seat=seat,different_tiles=matches,shops144=game['steps'][144][seat]['observation']['town']['unlocked_shops']))
(D/'route_compatibility_audit.json').write_text(json.dumps(reports,indent=2))
print(json.dumps(reports),flush=True)
