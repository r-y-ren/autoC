"""Rebuild opponents from already-downloaded public development demonstrations."""
from pathlib import Path
import gzip,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];M=R/'research/meta_rebuild_20260927'
core=(R/'experiments/round7_local_chassis_core.py').read_text(encoding='utf-8')
selection=json.loads((M/'recent_selection.json').read_text())
receipts={r['episode']:r for r in json.loads((M/'recent_receipts.json').read_text())}
folder=D/'archived_opponents';folder.mkdir(exist_ok=True);seen=set();manifest=[]
for view in sorted(selection['views'],key=lambda v:(v['rank'],v['episode'])):
    if view['team'] in seen:continue
    seen.add(view['team']);raw=gzip.decompress((M/'recent_replays'/f"{view['episode']}.json.gz").read_bytes())
    assert hashlib.sha256(raw).hexdigest()==receipts[view['episode']]['sha256']
    game=json.loads(raw);assert len(game['steps'])==720
    actions=[game['steps'][t+1][view['seat']]['action'] for t in range(719)]
    assert all(isinstance(a,dict) for a in actions)
    suffix='\n# Archived public-development proxy; not the author private program.\nimport json\n'
    suffix+='_DEMO=json.loads('+repr(json.dumps(actions,separators=(',',':')))+')\n'
    suffix+='_PROXY=make_agent({0:_DEMO})\ndef archived_proxy_agent(observation,configuration=None):\n    return _PROXY(observation,configuration)\n'
    suffix+='archived_proxy_agent.telemetry=_PROXY.chassis.diagnostics\nagent=archived_proxy_agent\n'
    source=(core+suffix).encode();p=folder/f"archive_{view['rank']:02d}.py";compile(source,str(p),'exec')
    if p.exists():assert p.read_bytes()==source
    else:p.write_bytes(source)
    manifest.append(dict(path=p.relative_to(R).as_posix(),family=f"archived_{view['rank']:02d}",panel='archived_responsive_proxy',sha256=hashlib.sha256(source).hexdigest(),episode=view['episode'],team=view['team'],seed=game['info']['seed'],captured_utc=selection.get('captured_utc'),scope='Previously inspected development replay plus public reactive chassis; NOT private leaderboard code.'))
(D/'archived_opponents.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(proxies=len(manifest),episodes=len({r['episode'] for r in manifest}))),flush=True)
