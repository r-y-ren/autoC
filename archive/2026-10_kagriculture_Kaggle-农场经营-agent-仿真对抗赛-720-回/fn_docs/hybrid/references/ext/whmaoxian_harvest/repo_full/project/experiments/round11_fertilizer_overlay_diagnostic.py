"""Diagnose why the bounded fertilizer overlay is inactive in an official game."""
import collections
import contextlib
import io
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1193292362
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    source = ROOT / 'experiments/round11_fertilizer_overlay.py'
    parent = ROOT / 'submissions/release_v9/main.py'
    entries = [get_last_callable(p.read_text(encoding='utf-8'), path=str(p)) for p in (source, parent)]
    env = make('kaggriculture', configuration={'seed': seed, 'episodeSteps': 720}, debug=True)
    env.run(entries)
    ns = entries[0].__globals__
    report = collections.Counter()
    examples = []
    for step in range(11*24, 29*24):
        day, hour = divmod(step, 24)
        if hour > 20:
            continue
        obs = env.steps[step][0].observation
        farm = obs.farms[0]
        native = ns['_IMPL'].chassis.players[0]
        all_ready = []
        for y, row in enumerate(farm['tiles']):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict) or tile.get('crop') not in ns['_R11F_CROPS']:
                    continue
                crop = tile['crop']
                first, interval, cap = ns['_R11F_CROPS'][crop]
                age = day+1-int(tile['planted_day'])
                if (age >= first and (age-first)%interval == 0 and
                    (age-first)//interval < cap and tile.get('watered_today') and
                    int(tile.get('fertilized_until_day', -1)) < day and
                    int(tile.get('yield_units', 0)) <= cap-2):
                    all_ready.append((x,y,crop))
        if not all_ready:
            continue
        report['raw_ready_turns'] += 1
        report['raw_ready_targets'] += len(all_ready)
        ready = ns['_r11f_ready'](obs)
        if not ready:
            report['price_blocked_turns'] += 1
            if len(examples) < 8:
                examples.append([step, 'price', all_ready[:3], obs.market['prices']['FERTILIZER']])
            continue
        report['priced_ready_turns'] += 1
        commands = [env.steps[step][0].action.get('farmer') or ['PASS'],
                    *list(env.steps[step][0].action.get('hands') or [])]
        _, busy = ns['_r9s_reservations'](obs, native)
        role = set()
        for m in (ns['_V219_STATES'],ns['_V233_STATES']):
            role.update(m.get(0, {}).get('workers', {}))
        available = [i for i in range(1,len(farm['hands'])+1)
                     if i < len(commands) and commands[i] == ['PASS']]
        if not available:
            report['no_pass_turns'] += 1
            continue
        report['pass_turns'] += 1
        idle = [i for i in available if i not in busy and i not in role]
        if not idle:
            report['all_busy_turns'] += 1
            if len(examples) < 8:
                examples.append([step, 'busy', ready[:1], available[:5]])
            continue
        report['idle_turns'] += 1
        if not any(obs.private['inventories'][i].get('FERTILIZER',0) for i in idle):
            report['no_carried_turns'] += 1
        if int(obs.private['shed'].get('FERTILIZER',0)) < 2:
            report['low_shed_turns'] += 1
        if ns['_r11f_future_input_reserved'](obs,native):
            report['future_input_turns'] += 1
        if any(o and o[:2] == ['SELL','FERTILIZER'] for o in env.steps[step][0].action.get('market',[])):
            report['current_sell_turns'] += 1
        if len(examples) < 8:
            examples.append([step, 'idle', ready[:1], idle[:5],
                             obs.private['shed'].get('FERTILIZER',0)])
    print(json.dumps({'seed':seed,'counts':report,'examples':examples},indent=2))


if __name__ == '__main__':
    main()
