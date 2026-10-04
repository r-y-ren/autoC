"""Build standalone production-plan experiments from declared public study data.
These are local reconstructions, never the original private leaderboard agents.
All historical evaluation identifiers remain in provenance, not runtime inputs.
"""
from pathlib import Path
import base64,gzip,hashlib,json,zlib
P=Path(__file__).resolve().parent;R=P.parents[1]
T=R/'research/v10_top10_20260926'
core=(R/'experiments/round7_local_chassis_core.py').read_text(encoding='utf-8')
views=json.loads((T/'replay_split.json').read_text(encoding='utf-8'))['study']
out=P/'plans';out.mkdir(exist_ok=True)
roster=[]
for i,view in enumerate(views):
    episode=view['episode'];seat=view['seat']
    source=T/f'study_replays/{episode}.json.gz'
    raw=source.read_bytes();game=json.loads(gzip.decompress(raw))
    actions=[s[seat]['action'] for s in game['steps'][1:]]
    assert len(actions)==719 and all(isinstance(a,dict) for a in actions)
    encoded=base64.b85encode(zlib.compress(json.dumps(actions,separators=(',',':')).encode(),9)).decode()
    for mode in ('physical','default'):
        settings={} if mode=='default' else dict(hand_align=True,weed_repair=True,sell_lead=False,budget_guard=False,room_guard=False,clamp_sells=False,dead_stock=False,terminal_liquidation=True,front_run=False)
        tail='\n# Standalone observation-guarded reconstruction of a public production plan.\n'
        tail+='import base64,json,zlib\n'
        tail+='_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('+repr(encoded)+')))\n'
        tail+='_PLAN_IMPL=make_agent({0:_SCHEDULE},**'+repr(settings)+')\n'
        tail+='def standalone_plan_agent(observation,configuration=None):\n    return _PLAN_IMPL(observation,configuration)\n'
        tail+='standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics\nagent=standalone_plan_agent\nkaggle_submission_agent=standalone_plan_agent\n'
        data=(core+tail).encode();path=out/f'plan{i:02d}_{mode}.py'
        compile(data,str(path),'exec')
        if path.exists():assert path.read_bytes()==data
        else:path.write_bytes(data)
        roster.append(dict(path=path.relative_to(R).as_posix(),mode=mode,plan=i,source_episode=episode,source_seat=seat,source_team=view['team'],source_sha256=hashlib.sha256(raw).hexdigest(),sha256=hashlib.sha256(data).hexdigest()))
manifest=P/'plan_manifest.json'
if manifest.exists():assert json.loads(manifest.read_text())==roster
else:manifest.write_text(json.dumps(roster,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(roster),study_views=len(views),heldout_used=False,released=False)),flush=True)
