"""Responsive public-route proxies for development; these are not the leaders' private agents."""
from pathlib import Path
import base64,gzip,hashlib,json,zlib
N=Path(__file__).resolve().parent;R=N.parents[1]
core=(R/'experiments/round7_local_chassis_core.py').read_text(encoding='utf-8')
split=json.loads((N/'replay_split.json').read_text(encoding='utf-8'))
index=json.loads((N/'demonstrations_index.json').read_text(encoding='utf-8'))
output=[];seen=set();dest=N/'study_opponents';dest.mkdir(exist_ok=True)
for view in split['study']:
    if view['team'] in seen:continue
    seen.add(view['team'])
    record=next(r for r in index if r['episode']==view['episode'] and r['seat']==view['seat'])
    data_path=R/record['path'];assert hashlib.sha256(data_path.read_bytes()).hexdigest()==record['sha256']
    data=json.loads(gzip.decompress(data_path.read_bytes()))
    blob=base64.b85encode(zlib.compress(json.dumps(data['actions'],separators=(',',':')).encode(),9)).decode()
    suffix='\n# Public demonstration plus local stock/budget/weed guards; a proxy only.\n'
    suffix+='import base64,json,zlib\n'
    suffix+='_DEMO=json.loads(zlib.decompress(base64.b85decode('+repr(blob)+')))\n'
    suffix+='_PROXY=make_agent({0:_DEMO})\n'
    suffix+='def top_style_proxy(observation,configuration=None):\n    return _PROXY(observation,configuration)\n'
    suffix+='top_style_proxy.telemetry=_PROXY.chassis.diagnostics\nagent=top_style_proxy\n'
    target=dest/f"style_{view['rank']:02d}.py";source=core+suffix
    compile(source,str(target),'exec');target.write_text(source,encoding='utf-8')
    output.append(dict(family=f"top_style_{view['rank']:02d}",team=view['team'],
        path=target.relative_to(R).as_posix(),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
        episode=view['episode'],submission_at_capture=view['submission'],
        kind='locally reconstructed responsive proxy, NOT private leaderboard program'))
assert len(output)==10
(N/'study_opponents.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
print(json.dumps(dict(responsive_proxies=len(output))),flush=True)
