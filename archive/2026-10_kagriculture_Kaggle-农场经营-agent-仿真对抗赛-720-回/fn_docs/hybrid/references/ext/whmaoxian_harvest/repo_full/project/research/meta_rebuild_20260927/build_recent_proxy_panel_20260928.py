"""Responsive demonstration proxies; never labelled as private top-ten programs."""
from pathlib import Path
import gzip,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
source=(R/'research/v10_top10_20260926/study_opponents/style_02.py').read_text()
marker='# Public demonstration plus local stock/budget/weed guards; a proxy only.'
assert source.count(marker)==1
chassis=source.split(marker)[0]
views=json.loads((D/'recent_selection.json').read_text())['views']
folder=D/'recent_proxy_panel';folder.mkdir(exist_ok=True)
selected=[];seen=set()
for view in views:
    if view['submission'] in seen:continue
    seen.add(view['submission']);selected.append(view)
proxies=[]
for view in selected:
    raw=gzip.decompress((D/f"recent_replays/{view['episode']}.json.gz").read_bytes())
    game=json.loads(raw);tape=[frame[view['seat']]['action'] for frame in game['steps'][1:]]
    assert len(tape)==719 and all(isinstance(action,dict) for action in tape)
    tail='\n# Archived development demonstration; responsive guards, fixed production.\n_DEMO='+repr(tape)+'\n_PROXY=make_agent({0:_DEMO})\ndef recent_demo_agent(observation,configuration=None):\n    return _PROXY(observation,configuration)\nrecent_demo_agent.telemetry=_PROXY.chassis.diagnostics\nagent=recent_demo_agent\n'
    data=(chassis+tail).encode();path=folder/f"style_rank{view['rank']:02d}.py"
    compile(data,str(path),'exec')
    if path.exists():assert path.read_bytes()==data
    else:path.write_bytes(data)
    proxies.append(dict(view,path=path.relative_to(R).as_posix(),sha256=sha(data),replay_sha256=sha(raw),source_seed=game['info']['seed'],panel='recent_responsive_proxy'))
old=json.loads((D/'midgame_herd_design.json').read_text())['variants']
sequence=json.loads((D/'herd_sequence_v2_design.json').read_text())['variants']
variants=[v for v in old if v['name'] in ('r2','yarn_nomilk')]+[v for v in sequence if v['name']=='early3_nomilk']
seeds=json.loads((D/'herd_extension_design.json').read_text())['seeds'][:8]
jobs=[]
for v in variants:
    assert sha((R/v['path']).read_bytes())==v['sha256']
    for proxy in proxies:
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=proxy['path'],family='recent_rank'+str(proxy['rank']),panel=proxy['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=proxy['sha256'])
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
for filename,obj in [('recent_proxy_design.json',dict(proxies=proxies,variants=variants,seeds=seeds,cases=len(jobs),scope='Development stress test: ten fixed-production responsive proxies, not private programs, not rating evidence.')),('recent_proxy_jobs.json',jobs)]:
    path=D/filename;text=json.dumps(obj,indent=2)
    if path.exists():assert path.read_text()==text
    else:path.write_text(text)
print(json.dumps({'proxies':len(proxies),'cases':len(jobs)}),flush=True)
