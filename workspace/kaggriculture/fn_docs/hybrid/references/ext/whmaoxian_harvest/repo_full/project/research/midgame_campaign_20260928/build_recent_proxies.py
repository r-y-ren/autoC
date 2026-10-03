"""Latest public action demonstrations wrapped in the existing guarded chassis.
These are responsive replay proxies, never the leaders' private programs.
Only action dictionaries are extracted; no downloaded Python is executed.
"""
from pathlib import Path
import ast,base64,gzip,hashlib,json,zlib
S=Path(__file__).resolve().parent;R=S.parents[1]
old=R/'research/v10_top10_20260926/study_opponents/style_02.py'
library=old.read_text(encoding='utf-8').split('# Public demonstration plus local stock/budget/weed guards; a proxy only.')[0]
assert 'class Chassis' in library and 'def make_agent' in library
folder=S/'recent_proxies';folder.mkdir(exist_ok=True)
selection=json.loads((S/'recent_selection.json').read_text())['views']
receipts={r['episode']:r for r in json.loads((S/'recent_receipts.json').read_text())}
sha=lambda b:hashlib.sha256(b).hexdigest();out=[]
for index,view in enumerate(selection):
    raw=gzip.decompress((S/'recent_replays'/f"{view['episode']}.json.gz").read_bytes())
    assert sha(raw)==receipts[view['episode']]['sha256']
    game=json.loads(raw);assert len(game['steps'])==720
    actions=[step[view['seat']]['action'] for step in game['steps'][1:]]
    assert all(isinstance(a,dict) and set(a)<=set(('farmer','hands','market')) for a in actions)
    packed=base64.b85encode(zlib.compress(json.dumps(actions,separators=(',',':')).encode(),9)).decode()
    suffix="\n# Public actions only; no hidden-state or rival-identity input.\nimport base64,json,zlib\n"
    suffix+=f"_DEMO=json.loads(zlib.decompress(base64.b85decode({packed!r})))\n"
    suffix+="_PROXY=make_agent({0:_DEMO})\ndef recent_style_proxy(observation,configuration=None):\n    return _PROXY(observation,configuration)\nrecent_style_proxy.telemetry=_PROXY.chassis.diagnostics\nagent=recent_style_proxy\n"
    data=(library+suffix).encode();path=folder/f'style_{index:02d}.py';ast.parse(data)
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    out.append(dict(name=f'recent_{index:02d}',path=path.relative_to(R).as_posix(),sha256=sha(data),
                    family=f"recent_rank_{view['rank']:02d}",panel='recent_responsive_proxy',
                    view=view,seed=game['info']['seed'],source_sha256=sha(raw),
                    action_sha256=sha(json.dumps(actions,sort_keys=True).encode())))
report=dict(variants=out,library_sha256=sha(library.encode()),views=len(out),
            unique_episodes=len({v['view']['episode'] for v in out}),
            scope='Development demonstrations selected before inspection. Chassis may diverge from original action stream due to live stock and budget guards. Not private executable strategies or rating calibration.')
p=S/'recent_proxy_manifest.json';text=json.dumps(report,indent=2,ensure_ascii=True)
if p.exists():assert p.read_text()==text
else:p.write_text(text)
print(json.dumps(dict(proxies=len(out),unique_episodes=report['unique_episodes'],library_sha256=report['library_sha256'])),flush=True)
