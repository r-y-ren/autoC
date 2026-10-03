"""Repair None-valued empty-pasture counting; retain failed candidates unchanged."""
from pathlib import Path
import contextlib,hashlib,io,json,sys
P=Path(__file__).resolve().parent;R=P.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import fast_arena as fa
variants=json.loads((P/'ranch_manifest.json').read_text());out=P/'ranches_v2';out.mkdir(exist_ok=True)
old="feed=sum(isinstance(t,dict) and t.get('animal') and not t.get('fed_today') for t in tiles)+missing"
new="feed=sum(1 for t in tiles if isinstance(t,dict) and t.get('animal') and not t.get('fed_today'))+missing"
fixed=[];checks=[]
for v in variants:
    original=(R/v['path']).read_bytes();assert hashlib.sha256(original).hexdigest()==v['sha256']
    text=original.decode();assert text.count(old)==1
    data=text.replace(old,new).encode();path=out/Path(v['path']).name;compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    row=dict(v,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest(),parent_sha256=v['sha256']);fixed.append(row)
    fn=fa.load(row['path']);ns=fn.__globals__;state,env=fa.new_game(71)
    obs=state[0].observation;obs.step=0;obs.farms[0]['farmer']=[5,5]
    for kind in (None,{'kind':'PASTURE'},{'kind':'WEED'}):
        for x,y in ns['_RX_GROUPS'][0]:obs.farms[0]['tiles'][y][x]=kind
        answer=ns['_rx_worker'](obs,0,ns['_RX_GROUPS'][0],{v['animal']:8,'WHEAT':8})
        assert isinstance(answer,list) and answer
        checks.append(dict(candidate=path.name,tile=kind,passed=True))
(P/'ranch_v2_manifest.json').write_text(json.dumps(fixed,indent=2))
(P/'ranch_v2_unit_checks.json').write_text(json.dumps(dict(checks=checks,passed=True),indent=2))
