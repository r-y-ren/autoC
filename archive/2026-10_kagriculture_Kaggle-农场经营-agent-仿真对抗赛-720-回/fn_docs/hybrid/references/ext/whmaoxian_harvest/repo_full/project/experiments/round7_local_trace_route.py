"""Diagnose route imitation errors from saved replay observations only."""
import collections
import argparse
import gzip
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--episode', type=int, default=111917373)
parser.add_argument('--seed', type=int, default=44100)
parser.add_argument('--prefix', default='round7_vadim_111917373_v2-audit')
parser.add_argument('--output', default='round7-local-route-trace.json')
args = parser.parse_args()
episode_id = args.episode
index = json.loads((root / 'research/round7/top2/index.json').read_text())
entry = next(r for r in index if r['episode_id'] == episode_id)
reference = json.loads(gzip.decompress((root / f'research/round7/top2/{episode_id}.json.gz').read_bytes()))
report = []
for seat in (0, 1):
    p = root / f'results/{args.prefix}-seed{args.seed}-seat{seat}-replay.json'
    if not p.exists():
        continue
    game = json.loads(p.read_text())
    issues = collections.defaultdict(list)
    daily = []
    for step, states in enumerate(game['steps'][:-1]):
        obs = states[seat]['observation']
        farm = obs['farms'][seat]
        private = obs['private']
        ref_obs = reference['steps'][step][entry['seat']]['observation']
        ref_farm = ref_obs['farms'][entry['seat']]
        action = game['steps'][step+1][seat]['action']
        if len(farm['hands']) != len(ref_farm['hands']):
            issues['hand_count_mismatch'].append({'step': step, 'hands':len(farm['hands']), 'reference':len(ref_farm['hands']), 'money':farm['money']})
        if step % 24 == 0:
            def composition(f):
                return dict(collections.Counter(t.get('animal') or t.get('crop') or t.get('kind') for row in f['tiles'] for t in row if isinstance(t,dict)))
            daily.append({'step':step,'money':farm['money'],'reference_money':ref_farm['money'],'farm':composition(farm),'reference_farm':composition(ref_farm)})
        positions = [farm['farmer'], *farm['hands']]
        commands = [action.get('farmer', ['PASS']), *action.get('hands', [])]
        # Account for sequential shared PICKUP and unit inventories.
        shed = dict(private['shed'])
        plant_requests = collections.Counter(c[1] for c in commands if len(c)>1 and c[0]=='PLANT')
        for kind, n in plant_requests.items():
            if n > private['seeds'].get(kind,0):
                issues['insufficient_seeds'].append({'step':step,'crop':kind,'need':n,'have':private['seeds'].get(kind,0)})
        for actor, (pos, command, inv) in enumerate(zip(positions, commands, private['inventories'])):
            if not command:
                continue
            x,y = pos
            tile = farm['tiles'][y][x]
            op = command[0]
            if op == 'PICKUP' and len(command)>1:
                item = command[1]
                qty = int(command[2]) if len(command)>2 else 1
                near = tuple(pos) in ((4,4),(5,4),(4,5),(5,5))
                if not near:
                    issues['pickup_away'].append({'step':step,'actor':actor,'item':item,'pos':pos})
                else:
                    if shed.get(item,0) < qty:
                        issues['pickup_shortage'].append({'step':step,'actor':actor,'item':item,'need':qty,'have':shed.get(item,0)})
                    shed[item] = max(0,shed.get(item,0)-qty)
            elif op in ('FEED','FERTILIZE') and not inv.get('WHEAT' if op=='FEED' else 'FERTILIZER',0):
                issues['empty_input_use'].append({'step':step,'actor':actor,'op':op,'tile':tile})
            elif op == 'PLACE' and len(command)>1 and command[1] in ('COW','SHEEP','GOOSE') and not inv.get(command[1],0):
                issues['empty_animal_place'].append({'step':step,'actor':actor,'animal':command[1],'pos':pos})
    report.append({'seat':seat,'issue_counts':{k:len(v) for k,v in issues.items()},'first_issues':{k:v[:10] for k,v in issues.items()}, 'daily':daily})
(root / 'results' / args.output).write_text(json.dumps(report, indent=2))
for row in report:
    print('seat',row['seat'],row['issue_counts'])
    print('first', {k:v[:2] for k,v in row['first_issues'].items()})
