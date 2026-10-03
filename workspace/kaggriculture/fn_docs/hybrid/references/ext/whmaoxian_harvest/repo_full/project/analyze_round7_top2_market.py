"""Measure executed trades on exactly reconstructed public study games."""
from collections import Counter
import contextlib
import gzip
import importlib
import io
import json
from pathlib import Path
import time
from benchmark_replays import tape_policy
from research_round7_top2 import counts
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
ROOT = Path(__file__).parent
OUT = ROOT/'research/round7/top2'
old_market, old_commit = engine._process_market, engine._commit_unit
ctx = {}

def observe_market(state, env):
    ctx['turn'] += 1
    ctx['farms'] = [id(f) for f in state[0].observation.farms]
    return old_market(state, env)

def observe_commit(op, item, price, farm, private, market, shed_capacity=100):
    ok = old_commit(op, item, price, farm, private, market, shed_capacity)
    if ok:
        seat = ctx['farms'].index(id(farm))
        ctx['trades'][seat][(ctx['turn'], op, item, price)] += 1
    return ok

def run(game, players):
    ctx.update(turn=-1, trades=[Counter(), Counter()])
    env = make('kaggriculture', configuration=dict(game['configuration'], seed=game['info']['seed']), debug=True)
    env.run(players)
    assert [s.status for s in env.steps[-1]] == ['DONE', 'DONE']
    assert not [v.get('stderr') for logs in env.logs for v in logs if v.get('stderr')]
    trades = [[list(key)+[qty] for key,qty in sorted(c.items())] for c in ctx['trades']]
    return env, trades

def summarize(trades, seat):
    products = {}
    for t, op, item, price, qty in trades[seat]:
        if op != 'SELL':
            continue
        v = products.setdefault(item, {'qty':0, 'revenue':0, 'floor_qty':0, 'sales_by_day': [0]*30, 'revenue_by_day': [0]*30})
        v['qty'] += qty
        v['revenue'] += price*qty
        v['floor_qty'] += qty if price==1 else 0
        v['sales_by_day'][t//24] += qty
        v['revenue_by_day'][t//24] += qty*price
    for v in products.values():
        v['avg_price'] = v['revenue']/max(1,v['qty'])
    return products

engine._process_market, engine._commit_unit = observe_market, observe_commit
result = []
rows = [r for r in json.loads((OUT/'index.json').read_text()) if r['split']=='study']
try:
    for row in rows:
        game = json.loads(gzip.decompress((OUT/f"{row['episode_id']}.json.gz").read_bytes()))
        env, trades = run(game, [tape_policy([s[p]['action'] for s in game['steps'][1:]]) for p in range(2)])
        assert [s.reward for s in env.steps[-1]] == game['rewards']
        (OUT/f"{row['episode_id']}_trades.json.gz").write_bytes(gzip.compress(json.dumps(trades).encode()))
        summary = {**row, 'reproduced_exactly': True, 'products': summarize(trades,row['seat'])}
        result.append(summary)
        (OUT/'study_sales.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print('reproduced', row['team'], row['episode_id'], {k:round(v['avg_price'],1) for k,v in summary['products'].items()}, flush=True)
    row = rows[0]
    game = json.loads(gzip.decompress((OUT/f"{row['episode_id']}.json.gz").read_bytes()))
    players = [tape_policy([s[p]['action'] for s in game['steps'][1:]]) for p in range(2)]
    players[row['seat']] = str(ROOT/'submissions/release_v6/main.py')
    env, trades = run(game, players)
    out = env.toJSON()
    (OUT/'v6_same_seed_counterfactual.json.gz').write_bytes(gzip.compress(json.dumps(out).encode()))
    snapshots = []
    for t in [23,47,71,143,239,359,479,599,719]:
        farm = out['steps'][t][row['seat']]['observation']['farms'][row['seat']]
        snapshots.append({'step':t,'money':farm['money'],'hands':len(farm['hands']),'counts':counts(farm)})
    result = {'kind':'v6_replaces_Vadim_against_frozen_historical_rival_not_live_agent', 'episode_id':row['episode_id'], 'seat':row['seat'], 'original_rewards':game['rewards'], 'rewards':out['rewards'], 'snapshots':snapshots, 'products':summarize(trades,row['seat'])}
    (OUT/'v6_comparison.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('v6 counterfactual', result['rewards'], 'vs historical', result['original_rewards'],flush=True)
finally:
    engine._process_market, engine._commit_unit = old_market, old_commit
