"""Build the bounded 19-tomato production repair on the real v7 entry."""
from pathlib import Path
import hashlib
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('--lean',action='store_true',help='Use the feasible planting-day 3-worker routes for the first harvest')
parser.add_argument('--balanced',action='store_true',help='Optimize fertilizer spatial routes while keeping five transporting harvest workers')
parser.add_argument('--delivery',action='store_true',help='Keep full fertilizer crews and optimize first-harvest routes including return')
args=parser.parse_args()

ROOT = Path(__file__).resolve().parents[1]
base = (ROOT / 'experiments/round7_orderbook_v56.py').read_text(encoding='utf-8')
suffix = (ROOT / 'experiments/round7_tomato19_conservative_suffix.txt').read_text(encoding='utf-8')
suffix = suffix.replace('_T19_PARENT = agent', '_T19_PARENT = round7_orderbook_v56_agent')
suffix = suffix.replace('# Local research, 2026-09-22;', '# Local production repair, 2026-09-22;')
# Day 27 cargo is automatically deposited at the daily refresh. Requiring every
# worker to walk home discarded an otherwise feasible entire harvest shift.
suffix = suffix.replace("if day in (27,29) else 0", "if day==29 else 0")
# Establishing a new investment may be declined; committed crops always retain
# their available maintenance shift even when the complete preferred route is late.
suffix = suffix.replace("if schedule[0][0]>available:", "if not state.get('committed') and schedule[0][0]>available:")
suffix = suffix.replace("if farm['money']<budget+3000:", "if farm['money']<budget+(0 if state.get('committed') else 3000):")
if args.lean:
    suffix = suffix.replace('if day==27:return _T19_HARVEST', 'if day==27:return _T19_PLANT')
if args.balanced:
    import json
    routes=json.loads((ROOT/'research/round8/production_spatial_routes_fert3.json').read_text(encoding='utf-8'))['paths']
    assignment=repr([[tuple(p) for p in path] for path in routes])
    suffix=suffix.replace('def _t19_groups(day):', '_T19_FERT_BALANCED='+assignment+'\n\ndef _t19_groups(day):')
    suffix=suffix.replace('if day in (25,26):return _T19_FOUR','if day in (25,26):return _T19_FERT_BALANCED')
if args.delivery:
    import json
    routes=json.loads((ROOT/'research/round8/production_spatial_routes_harvest5.json').read_text(encoding='utf-8'))['paths']
    assignment=repr([[tuple(p) for p in path] for path in routes])
    suffix=suffix.replace('def _t19_groups(day):', '_T19_HARVEST_DELIVERY='+assignment+'\n\ndef _t19_groups(day):')
    suffix=suffix.replace('if day==27:return _T19_HARVEST','if day==27:return _T19_HARVEST_DELIVERY')
    suffix=suffix.replace("if day==29 else 0", "if day in (27,29) else 0")
    # Parent uses TWO watering workers when native hiring ends after hour 2.
    # Infer that from the same known native schedule instead of the stale fixed
    # one-worker approximation. For day26, retain the cheaper feasible parent
    # minimum when it can use the upstream two-worker labor optimization.
    suffix=suffix.replace("n=max(len(a.get('hands',[])) for a in _v219_native_day(_IMPL.chassis.players[int(obs['player'])],day))", "planned=_v219_native_day(_IMPL.chassis.players[int(obs['player'])],day)\n        n=max(len(a.get('hands',[])) for a in planned)\n        last_hire=max((i for i,a in enumerate(planned) if any(o==['HIRE'] for o in a.get('market',[]))),default=-1)\n        if day in (20,22,25):baseline[day]=1 if last_hire<=2 else 2\n        if day==26:baseline[day]=2 if last_hire<=2 else 3")
suffix = suffix.replace("def agent(observation,configuration=None):", "def round8_production_agent(observation,configuration=None):")
suffix = suffix.replace("agent.telemetry=_T19_REPORT\nagent=globals().pop('agent')\nkaggle_submission_agent=agent", "round8_production_agent.telemetry=_T19_REPORT\nagent=round8_production_agent\nkaggle_submission_agent=round8_production_agent")
suffix = suffix.replace("if day==29 and step>=718-_t19_distance(pos,home) and inv.get('TOMATO',0):", "if day==29 and step>=718-_t19_distance(pos,home) and inv.get('TOMATO',0):")
# At the final harvest, skip a target if harvesting it would prevent a bankable
# return. Earlier days need only reserve the physical operation, since the game
# deposits cargo automatically at midnight. Never cancel the whole day's crew.
suffix = suffix.replace("        if command:\n            walk=_v219_walk(pos,target)", "        if command:\n            work=_t19_distance(pos,target)+1\n            back=(_t19_distance(target,_v219_home(target))+1) if day==29 else 0\n            deadline=718 if day==29 else (day+1)*24-1\n            if work+back>deadline-step+1:\n                _T19_REPORT['partial_route_deferrals']=_T19_REPORT.get('partial_route_deferrals',0)+1\n                continue\n            walk=_v219_walk(pos,target)")
if args.delivery:suffix=suffix.replace("if day==29 else 0", "if day in (27,29) else 0")
if args.delivery:
    # A committed farm degrades to an affordable partial crew instead of
    # dropping a whole maintenance day when fertilizer/order/cash space is tight.
    suffix=suffix.replace("if hour>6 or any(o and o[0]=='HIRE'", "if hour>(18 if state.get('committed') else 6) or any(o and o[0]=='HIRE'")
    old_start=suffix.index('    extra=[]\n',suffix.index('def _v219_request'))
    old_end=suffix.index("    state['requested_day']=day",old_start)
    suffix=suffix[:old_start]+'''    parent_cost=sum(_v219_fib(n) for n in range(farm['hires_today'],farm['hires_today']+parent_hires))
    for order in action['market']:
        if not order:continue
        if order[0]=='BUY_PRODUCT':parent_cost+=int(order[2])*(int(obs['market']['prices'][order[1]])+10)
        elif order[0]=='BUY_ANIMAL':parent_cost+=int(order[2])*{'COW':400,'SHEEP':500,'GOOSE':300}[order[1]]
        elif order[0]=='BUY_SEED':parent_cost+=int(order[2])*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[order[1]]
    desired_fertilizer=day in (25,26)
    # A temporarily full order list is common immediately after native hiring.
    # Wait for the next free slots before shrinking a day's whole crew. Only
    # after the ordinary planning window closes is a partial shift preferable.
    full_slots=count+int(desired_fertilizer)+(0 if state.get('committed') else 2)
    if hour<=6 and len(action['market'])+full_slots>MAX_ORDERS:return action
    proposal=None
    normal_groups=_t19_groups(day)
    for affordable_count in range(count,0,-1):
        for fertilize in ([True,False] if desired_fertilizer and state.get('committed') else [desired_fertilizer]):
            if not state.get('committed') and affordable_count!=count:continue
            extra=[]
            if not state.get('committed'):extra.extend([['BUY_LAND'],['BUY_SEED','TOMATO',19]])
            if fertilize:extra.append(['BUY_PRODUCT','FERTILIZER',19])
            extra.extend([['HIRE'] for _ in range(affordable_count)])
            if len(action['market'])+len(extra)>MAX_ORDERS:continue
            budget=parent_cost+sum(_v219_fib(n) for n in range(farm['hires_today']+parent_hires,farm['hires_today']+parent_hires+affordable_count))
            if not state.get('committed'):budget+=4950
            if fertilize:budget+=19*(int(obs['market']['prices']['FERTILIZER'])+10)
            if farm['money']<budget+(0 if state.get('committed') else 3000):continue
            proposal=(extra,affordable_count,fertilize)
            break
        if proposal is not None:break
    if proposal is None:
        _T19_REPORT['budget_declines']+=1
        return action
    extra,count,fertilize=proposal
    groups=[list(g) for g in normal_groups]
    if count<len(groups):
        packed=[[] for _ in range(count)]
        for g in groups:packed[min(range(count),key=lambda i:len(packed[i]))].extend(g)
        groups=packed
        _T19_REPORT['partial_crews']=_T19_REPORT.get('partial_crews',0)+1
    state['t19_pending']={'step':step,'first':expected+1,'count':count,'groups':groups,
                          'fertilize':fertilize,'maintenance_first':count<len(normal_groups)}
''' + suffix[old_end:]
    suffix=suffix.replace('groups=_t19_groups(day)\n    if len(farm', "groups=pending.get('groups',_t19_groups(day))\n    if len(farm")
    suffix=suffix.replace("'needs_fertilizer':day in (25,26),'loaded':False}","'needs_fertilizer':pending.get('fertilize',day in (25,26)),'loaded':False,\n                              'maintenance_first':pending.get('maintenance_first',False)}")
    suffix=suffix.replace("    for target in role['targets']:\n", "    targets=role['targets']\n    if role.get('maintenance_first') and day<29:\n        def priority(target):\n            x,y=target;t=view.tiles[y][x]\n            urgent=isinstance(t,dict) and t.get('crop')=='TOMATO' and not t.get('watered_today')\n            return (0 if urgent else 1,-int(t.get('consecutive_unwatered',0)) if urgent else 0,_t19_distance(pos,target))\n        targets=sorted(targets,key=priority)\n    for target in targets:\n")
stem='round8_production_delivery' if args.delivery else ('round8_production_balanced' if args.balanced else ('round8_production_lean' if args.lean else 'round8_production'))
(ROOT / ('experiments/'+stem+'_suffix.txt')).write_text(suffix, encoding='utf-8')
output=ROOT / ('experiments/'+stem+'.py')
output.write_text(base+'\n\n'+suffix, encoding='utf-8')
print(output.name, hashlib.sha256(output.read_bytes()).hexdigest())
