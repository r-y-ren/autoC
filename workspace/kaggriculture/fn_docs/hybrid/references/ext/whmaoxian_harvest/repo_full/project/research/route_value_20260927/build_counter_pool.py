"""More responsive public-demonstration opponents, explicitly not private agents."""
from pathlib import Path
import gzip,hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1];T=R/'research/v10_top10_20260926'
core=(R/'experiments/round7_local_chassis_core.py').read_text(encoding='utf-8')
records=json.loads((T/'demonstrations_index.json').read_text())
allowed={(r['episode'],r['seat']) for r in json.loads((T/'replay_split.json').read_text())['study']}
out=D/'counter_pool';out.mkdir(exist_ok=True);roster=[]
for i,record in enumerate(records):
    assert (record['episode'],record['seat']) in allowed
    raw=(R/record['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==record['sha256']
    demo=json.loads(gzip.decompress(raw));path=out/f'demo_{i:02d}.py'
    source=core+'\n_DEMO='+repr(demo['actions'])+'\n_PROXY=make_agent({0:_DEMO})\n'
    source+='def demonstrated_proxy(observation,configuration=None):\n    return _PROXY(observation,configuration)\n'
    source+='demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics\nagent=demonstrated_proxy\n'
    compile(source,str(path),'exec');assert not path.exists();path.write_text(source,encoding='utf-8')
    roster.append(dict(path=path.relative_to(R).as_posix(),family=f'demo_{i:02d}',panel='responsive_proxy',
        teacher=record['team'],episode=record['episode'],seat=record['seat'],sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
(D/'counter_roster.json').write_text(json.dumps(roster,indent=2))
seeds=json.loads((D/'pilot_design.json').read_text())['seeds'][:4];jobs=[]
base='submissions/release_v10_r2/main.py'
for opponent in roster:
    for seed in seeds:
        for seat in (0,1):
            j=dict(candidate=base,opponent=opponent['path'],seed=seed,seat=seat,family=opponent['family'],panel=opponent['panel'])
            for key in ('candidate','opponent'):j[key+'_sha256']=hashlib.sha256((R/j[key]).read_bytes()).hexdigest()
            j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'counter_screen_jobs.json').write_text(json.dumps(jobs,indent=2))
print(json.dumps(dict(proxies=len(roster),games=len(jobs),heldout_views_used=False)),flush=True)
