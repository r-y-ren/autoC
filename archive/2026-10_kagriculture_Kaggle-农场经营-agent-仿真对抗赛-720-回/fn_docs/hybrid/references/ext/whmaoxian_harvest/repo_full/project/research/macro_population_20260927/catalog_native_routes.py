"""Inspect existing complete production routes, preserving agent sources."""
from pathlib import Path
from collections import Counter
import contextlib,hashlib,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
    entry=fa.load('submissions/release_v10_r2/main.py')
ns=entry.__globals__;routes=ns['_IMPL'].chassis.routes
canonical=lambda obj:json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
first=canonical(routes[0][:144]);records=[]
for rid,tape in routes.items():
    purchases=Counter();land=[];hours=[]
    for t,a in enumerate(tape):
        for order in a.get('market',[]):
            if order and order[0]=='BUY_LAND':land.append(t)
            if len(order)>=3 and order[0] in ('BUY_ANIMAL','BUY_SEED'):purchases[order[0]+':'+order[1]]+=int(order[2])
    record=dict(route=rid,turns=len(tape),prefix144_exact=canonical(tape[:144])==first,
        maximum_workers=max(len(a.get('hands',[])) for a in tape),
        planned_daily_workers=[max(len(a.get('hands',[])) for a in tape[d*24:(d+1)*24]) for d in range(30)],
        purchases=dict(purchases),land_steps=land,sha256=hashlib.sha256(canonical(tape)).hexdigest())
    records.append(record)
result=dict(routes=records,count=len(records),compatible=sum(r['prefix144_exact'] for r in records),
    base_sha256=hashlib.sha256((R/'submissions/release_v10_r2/main.py').read_bytes()).hexdigest(),scope='Compatibility of planned actions only; actual execution and profit require full games.')
(D/'native_route_catalog.json').write_text(json.dumps(result,indent=2))
print(json.dumps(dict(routes=len(records),compatible=result['compatible'],compatible_ids=[r['route'] for r in records if r['prefix144_exact']]),ensure_ascii=False),flush=True)
