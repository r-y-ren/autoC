"""Read-only synopsis of V9's native crop route tapes."""

from collections import Counter, defaultdict
from pathlib import Path
import contextlib
import io
import gzip
import json

ROOT = Path(__file__).resolve().parents[2]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments.agent import get_last_callable

source = ROOT / 'submissions/release_v9/main.py'
agent = get_last_callable(source.read_text(encoding='utf-8'), path=str(source))
namespace = agent.__globals__
chassis = namespace['_IMPL'].chassis
for route, tape in sorted(chassis.routes.items()):
    crops = defaultdict(Counter)
    market = defaultdict(Counter)
    for step, action in enumerate(tape):
        day = step // 24
        for command in [action.get('farmer'), *(action.get('hands') or [])]:
            if command and command[0] in ('PLANT', 'HARVEST', 'WATER', 'FERTILIZE'):
                crops[day][tuple(command)] += 1
        for order in action.get('market', []):
            if order and (order[0] in ('BUY_SEED', 'SELL') and len(order) >= 3 and order[1] in ('STRAWBERRY', 'TOMATO', 'MELON')):
                market[day][tuple(order)] += 1
    seed_count = sum(count*order[2] for order,count in market[11].items()
                     if order[:2]==('BUY_SEED','STRAWBERRY'))
    cumulative = 0
    prefixes = []
    for action in tape[264:288]:
        for order in action.get('market', []):
            if order and order[:2] == ['BUY_SEED','STRAWBERRY']:
                cumulative += int(order[2]); prefixes.append(cumulative)
    print(f'ROUTE {route}: day11 planted strawberry={crops[11][("PLANT", "STRAWBERRY")]} '
          f'seed orders={seed_count} prefixes={prefixes}')

replay = ROOT / 'research/round10/audit_dsm_1829941733.json.gz'
with gzip.open(replay, 'rt', encoding='utf-8') as stream:
    episode = json.load(stream)
print('V9 vs DSM proxy, day11 crop actions:')
for step in range(264, 288):
    z = episode['steps'][step][0]
    obs, action = z['observation'], z.get('action') or {}
    farm = obs['farms'][0]
    pos = [farm['farmer'], *farm['hands']]
    plants = [(j,tuple(pos[j])) for j,command in enumerate(
        [action.get('farmer'), *(action.get('hands') or [])])
        if command and command[:2] == ['PLANT', 'STRAWBERRY'] and j<len(pos)]
    buys = [order for order in action.get('market', [])
            if order and order[:2] == ['BUY_SEED', 'STRAWBERRY']]
    if plants or buys:
        print(step, 'seeds-before', obs['private']['seeds']['STRAWBERRY'],
              'plants', plants, 'buys', buys)

selected = set()
ordered = []
for step in range(264, 288):
    z = episode['steps'][step][0]
    obs, action = z['observation'], z.get('action') or {}
    farm = obs['farms'][0]
    pos = [farm['farmer'], *farm['hands']]
    for j, command in enumerate([action.get('farmer'), *(action.get('hands') or [])]):
        if command and command[:2] == ['PLANT', 'STRAWBERRY'] and j < len(pos):
            selected.add(tuple(pos[j]))
            ordered.append(tuple(pos[j]))
print('Day11 planted tiles', sorted(selected))
harvest21 = set()
for day in range(11, 30):
    counts = Counter()
    for step in range(day*24, min(720, (day+1)*24)):
        z = episode['steps'][step][0]
        obs, action = z['observation'], z.get('action') or {}
        farm = obs['farms'][0]
        pos = [farm['farmer'], *farm['hands']]
        for j, command in enumerate([action.get('farmer'), *(action.get('hands') or [])]):
            if command and command[0] in ('WATER', 'HARVEST', 'FERTILIZE') and j < len(pos) and tuple(pos[j]) in selected:
                counts[command[0]] += 1
                if day==21 and command[0]=='HARVEST':harvest21.add(tuple(pos[j]))
    if counts:
        print('day', day, 'tile work', dict(counts))
print('First patch native day21 harvest',[(k,len(set(ordered[:k])&harvest21)) for k in (5,9,13)])

for name in ('audit_dsm_1829941733','audit_dsm_264393735','audit_dsm_242588832'):
    with gzip.open(ROOT / ('research/round10/' + name + '.json.gz'), 'rt', encoding='utf-8') as stream:
        episode = json.load(stream)
    obs = episode['steps'][264][0]['observation']
    rival = obs['farms'][1]
    items = ('TOMATO','STRAWBERRY')
    print(name, 'shops', obs['town']['unlocked_shops'],
          'prices', {item:obs['market']['prices'][item] for item in items},
          'inventory', {item:obs['market']['inventory'][item] for item in items},
          'rival_plants', {item:sum(isinstance(tile,dict) and tile.get('crop')==item
                                    for row in rival['tiles'] for tile in row) for item in items})
