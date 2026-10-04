"""Read frozen tapes and donor states; no full games or candidate source edits."""
import contextlib
import copy
import gzip
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent
SOURCE = ROOT / 'experiments/round8_top2_dsm_contract_entry.py'
raw = SOURCE.read_text(encoding='utf-8')
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == '23768116945ebd7500b2e2298616ff6dd974d27ce2c839643cc7d3e3d4cada57'
ns = {}
exec(compile(raw, str(SOURCE), 'exec'), ns)
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    from kaggle_environments.utils import structify
    from kaggle_environments.agent import get_last_callable

index = {str(x['episode_id']): x for x in json.loads((OUT / 'compiled_index.json').read_text())}
counts = Counter()
animal_examples = []
cash_examples = []
mixed_examples = []
route_stats = []
original_hire = engine._do_hire
original_commit = engine._commit_unit

def market_probe(replay, step, seat, own_action):
    """Only this donor snapshot's physical actions and one official market turn."""
    state = structify(copy.deepcopy(replay['steps'][step]))
    for p in range(2):
        state[p].action = copy.deepcopy(own_action if p == seat else replay['steps'][step + 1][p]['action'])
        farm = state[0].observation.farms[p]
        private = state[p].observation.private
        action = state[p].action or {}
        for i, cmd in enumerate([action.get('farmer', ['PASS'])] + action.get('hands', [])):
            # PLANT changes no market money or shed; skip its seed consumption here.
            if cmd and cmd[0] == 'PLANT':
                continue
            engine._apply_unit_action(farm, private, i, cmd, 10, step // 24, 24, 100)
    report = Counter()
    target_farm = state[0].observation.farms[seat]

    def hire(farm, *args):
        n = farm['hires_today']
        result = original_hire(farm, *args)
        if farm is target_farm:
            report['hire_success' if farm['hires_today'] > n else 'hire_failed'] += 1
        return result

    def commit(op, item, price, farm, *args):
        result = original_commit(op, item, price, farm, *args)
        if farm is target_farm and op == 'BUY_SEED':
            report['seed_units_success' if result else 'seed_order_failed'] += 1
        return result

    engine._do_hire = hire
    engine._commit_unit = commit
    try:
        engine._process_market(state, SimpleNamespace(configuration=replay['configuration']))
    finally:
        engine._do_hire = original_hire
        engine._commit_unit = original_commit
    report['ending_money'] = target_farm['money']
    return dict(report)

for rid, demo in ns['_R8_DEMOS'].items():
    row = index[rid]
    seat = row['seat']
    replay = json.loads(gzip.decompress((OUT / (rid + '.json.gz')).read_bytes()))
    rc = Counter()
    for step, action in enumerate(demo['actions'][:len(replay['steps']) - 1]):
        counts['tape_turns'] += 1
        obs = copy.deepcopy(replay['steps'][step][seat]['observation'])
        obs['step'] = step
        if not obs.get('farms'):
            obs['farms'] = replay['steps'][step][0]['observation']['farms']
        view = ns['_View'](obs, seat, ns['_R8_IMPL'].cfg)
        units = [action.get('farmer', ['PASS'])] + action.get('hands', [])
        for i, cmd in enumerate(units[:len(view.positions)]):
            if not cmd or cmd[0] != 'PLACE' or len(cmd) < 2 or cmd[1] not in engine.ANIMALS:
                continue
            counts['animal_place'] += 1
            rc['animal_place'] += 1
            if not ns['_shed_adjacent'](view.positions[i], 10):
                continue
            counts['animal_place_shed_adjacent'] += 1
            rc['animal_place_shed_adjacent'] += 1
            x, y = view.positions[i]
            tile = view.tiles[y][x]
            matching = isinstance(tile, dict) and tile.get('kind') == engine.ANIMALS[cmd[1]]['structure'] and 'animal' not in tile
            later_drop = [j for j in range(i+1, min(len(units), len(view.positions))) if units[j] and units[j][0] == 'DROP' and ns['_shed_adjacent'](view.positions[j], 10)]
            if later_drop:
                counts['adjacent_animal_place_before_drop'] += 1
            if not matching:
                counts['animal_place_shed_fallthrough'] += 1
                if view.inv(i).get(cmd[1], 0) > 0:
                    counts['animal_place_shed_fallthrough_with_carried_animal'] += 1
                animal_examples.append({'route': rid, 'step': step, 'actor': i, 'command': cmd, 'position': view.positions[i], 'tile': tile, 'inventory': view.inv(i), 'shed_total': sum(view.shed.values()), 'later_drop': later_drop})
        market = action.get('market', [])
        fixed = [j for j, o in enumerate(market) if o and o[0] in ('HIRE', 'BUY_SEED')]
        other = [j for j, o in enumerate(market) if o and o[0] in ('BUY_PRODUCT', 'BUY_ANIMAL', 'BUY_LAND')]
        if not fixed or not other:
            continue
        counts['mixed_purchase_turns'] += 1
        rc['mixed_purchase_turns'] += 1
        for op in {market[j][0] for j in other}:
            counts['mixed_with_' + op] += 1
        before = any(j < k for j in other for k in fixed)
        if before:
            counts['other_purchase_before_fixed'] += 1
        hired = view.hires_today
        required = 0
        for o in market:
            if o and o[0] == 'HIRE':
                required += ns['_fib'](hired)
                hired += 1
            elif o and o[0] == 'BUY_SEED' and len(o) > 2:
                required += ns['SEED_PRICE'].get(o[1], 0) * int(o[2])
        if len(mixed_examples) < 12:
            mixed_examples.append({'route': rid, 'step': step, 'money': view.money, 'required': required, 'market': market, 'before': before})
        if not before or required > view.money:
            continue
        counts['cash_guard_nontrigger_with_prior_purchase'] += 1
        # Evaluate only these local mixed-order snapshots, never advance a full game.
        unchanged = ns['_r8_contract'](obs, replay['configuration'], copy.deepcopy(action))
        assert unchanged['market'] == market
        result = market_probe(replay, step, seat, action)
        if not result.get('hire_failed') and not result.get('seed_order_failed'):
            continue
        counts['local_fixed_failure_on_nontrigger_turn'] += 1
        proj = ns['_R8_IMPL']._projected_shed(action, view)
        reserve = dict(proj)
        eligible, others = [], []
        for o in market:
            if len(o) > 2 and o[0] == 'SELL' and int(o[2]) > 0 and reserve.get(o[1], 0) >= int(o[2]):
                eligible.append(o)
                reserve[o[1]] -= int(o[2])
            else:
                others.append(o)
        moved = copy.deepcopy(action)
        moved['market'] = eligible + others
        reordered = market_probe(replay, step, seat, moved)
        rescued = reordered.get('hire_success', 0) > result.get('hire_success', 0) or reordered.get('seed_units_success', 0) > result.get('seed_units_success', 0)
        if rescued:
            counts['nontrigger_failure_rescued_by_same_stock_sell_frontload'] += 1
        cash_examples.append({'route': rid, 'step': step, 'seat': seat, 'recorded_money': view.money, 'fixed_required': required, 'market': market, 'matches_public_market': market == replay['steps'][step+1][seat]['action'].get('market'), 'official_local_result': result, 'frontload_result': reordered, 'frontload_rescued': rescued, 'eligible_sells': eligible})
    route_stats.append({'route': rid, 'seat': seat, **rc})
    print(rid, dict(rc), flush=True)

# One bounded official-function construction demonstrates the inventory mismatch.
farm = engine._new_farm(10, 0)
farm['hands'] = [[4, 4]]
private = engine._new_private()
private['shed']['FERTILIZER'] = 99
private['inventories'] = [{'SHEEP': 1}, {'TOMATO': 1}]
obs = {'step': 1, 'player': 0, 'farms': [copy.deepcopy(farm), engine._new_farm(10, 0)], 'private': copy.deepcopy(private), 'market': {}}
action = {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['DROP']], 'market': []}
projected = ns['_R8_IMPL']._projected_shed(action, ns['_View'](obs, 0, ns['_R8_IMPL'].cfg))
engine._apply_unit_action(farm, private, 0, action['farmer'], 10, 0, 24, 100)
engine._apply_unit_action(farm, private, 1, action['hands'][0], 10, 0, 24, 100)
micro = {'projected_shed': projected, 'official_shed': private['shed'], 'official_remaining_cargo': private['inventories']}
assert projected.get('TOMATO') == 1 and private['shed']['TOMATO'] == 0
entry = get_last_callable(raw)
summary = {'candidate_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(), 'official_selected_entry': entry.__name__, 'scope': '24 frozen tapes against their public donor observations; local official function probes only, not new games, not ranking evaluation', 'counts': counts, 'route_stats': route_stats, 'animal_examples': animal_examples, 'mixed_examples': mixed_examples, 'cash_examples': cash_examples, 'synthetic_inventory_case': micro}
(OUT / 'contract_review_tape_audit.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'counts': counts, 'official_selected_entry': entry.__name__, 'cash_examples': len(cash_examples), 'synthetic_inventory_case': micro}, ensure_ascii=False, indent=2))

# A separate synthetic cash-order case, with a coherent eight-worker state.
farm = engine._new_farm(10, 50)
farm['hires_today'] = 8
farm['hands'] = [[4, 4] for _ in range(8)]
private = engine._new_private()
private['shed']['TOMATO'] = 1
private['inventories'] = [{} for _ in range(9)]
market = engine._new_market()
engine._refresh_prices(market)
obs = {'step': 1, 'player': 0, 'farms': [farm, engine._new_farm(10, 0)], 'private': private, 'market': market}
action = {'farmer': ['PASS'], 'hands': [], 'market': [['BUY_PRODUCT', 'WHEAT', 1], ['HIRE'], ['SELL', 'TOMATO', 1]]}
contract = ns['_r8_contract'](copy.deepcopy(obs), None, copy.deepcopy(action))
cash_micro = {'scope': 'Synthetic official single-market-turn construction only; not a game', 'initial_money': 50, 'initial_hires_today': 8, 'next_hire_cost': engine._hire_cost(8), 'market': action['market'], 'contract_action_unchanged': contract == action, 'outcomes': {}}
for label, orders in [('original', action['market']), ('contract', contract['market']), ('frontload', [action['market'][2]] + action['market'][:2])]:
    state = structify([{'observation': copy.deepcopy(obs), 'action': {'market': orders}}, {'observation': {'private': engine._new_private()}, 'action': {'market': []}}])
    engine._process_market(state, SimpleNamespace(configuration={}))
    result = state[0].observation.farms[0]
    cash_micro['outcomes'][label] = {'money': result['money'], 'hires_today': result['hires_today'], 'hands': len(result['hands']), 'shed': dict(state[0].observation.private.shed)}
assert cash_micro['outcomes']['original']['hires_today'] == 8
assert cash_micro['outcomes']['contract']['hires_today'] == 8
assert cash_micro['outcomes']['frontload']['hires_today'] == 9
(OUT / 'contract_review_cash_micro.json').write_text(json.dumps(cash_micro, indent=2), encoding='utf-8')
