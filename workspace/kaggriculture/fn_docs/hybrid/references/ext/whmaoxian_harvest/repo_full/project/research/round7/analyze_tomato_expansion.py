"""Read-only action/layout audit of the largest recorded v6 loss."""
from collections import Counter
import gzip
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"research/round7"
g=json.loads(gzip.decompress((OUT/"user-111747876.json.gz").read_bytes()))
physical=[]
for t in range(432):
    a,b=[s["action"] for s in g["steps"][t+1]]
    if (a["farmer"],a["hands"]) != (b["farmer"],b["hands"]):
        physical.append(t)
layouts=[]
for t in (0,432,456):
    farms=g["steps"][t][0]["observation"]["farms"]
    diffs=[]
    for y in range(10):
        for x in range(10):
            def kind(tile):
                return tile.get("animal") or tile.get("crop") or tile.get("kind") if isinstance(tile,dict) else tile
            a,b=[kind(f["tiles"][y][x]) for f in farms]
            if a!=b:diffs.append({"tile":[x,y],"yomogii":a,"v6":b})
    layouts.append({"step":t,"quadrants":[f["unlocked_quadrants"] for f in farms],"different_tile_kinds":diffs})
targets=[{},{}]
for t in range(432,456):
    for seat in (0,1):
        obs=g["steps"][t][seat]["observation"]
        farm=obs["farms"][seat]
        positions=[farm["farmer"],*farm["hands"]]
        a=g["steps"][t+1][seat]["action"]
        for actor,cmd in enumerate([a["farmer"],*a["hands"]]):
            if cmd==["PLANT","TOMATO"]:
                targets[seat].setdefault(actor,[]).append({"step":t,"tile":positions[actor]})
days=[]
for day in range(18,30):
    seats=[]
    for seat in (0,1):
        roles={}
        hires=[]
        for t in range(day*24,min((day+1)*24,719)):
            obs=g["steps"][t][seat]["observation"]
            farm=obs["farms"][seat]
            positions=[farm["farmer"],*farm["hands"]]
            a=g["steps"][t+1][seat]["action"]
            n=sum(o==["HIRE"] for o in a["market"])
            if n:hires.append([t,n])
            for actor,cmd in enumerate([a["farmer"],*a["hands"]]):
                if actor>=12 and actor<len(positions):
                    roles.setdefault(actor,[]).append({"step":t,"position":positions[actor],"command":cmd})
        seats.append({"hires":hires,"crew":roles})
    days.append({"day":day,"seats":seats})
report={"physical_matching_turns_before_432":432-len(physical),"physical_different_steps":physical,
        "layouts":layouts,"planting_targets":targets,"daily_crew":days}
(OUT/"tomato_expansion_trace.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k!="daily_crew"},indent=2))
for d in days:
    print('day',d['day'],[(s['hires'],{a:dict(Counter(v['command'][0] for v in seq)) for a,seq in s['crew'].items()}) for s in d['seats']])
