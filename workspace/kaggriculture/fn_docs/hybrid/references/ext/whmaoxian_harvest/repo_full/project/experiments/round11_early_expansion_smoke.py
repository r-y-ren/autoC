"""Official-engine physical smoke for the Round 11 sheep route."""
import contextlib
import hashlib
import io
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITES = ((5, 5), (5, 6), (6, 5))


def describe(state):
    obs = state.observation
    farm = obs.farms[0]
    cells = [farm['tiles'][y][x] for x, y in SITES]
    return {
        'money': farm['money'], 'land': list(farm['unlocked_quadrants']),
        'sheep': sum(isinstance(x, dict) and x.get('animal') == 'SHEEP' for x in cells),
        'unfed': sum(isinstance(x, dict) and x.get('animal') == 'SHEEP' and x.get('consecutive_unfed', 0) > 0 for x in cells),
        'wool_on_tiles': sum(int(x.get('yield_units', 0)) for x in cells if isinstance(x, dict)),
        'shed_wool': int(obs.private['shed'].get('WOOL', 0)),
        'shed_fertilizer': int(obs.private['shed'].get('FERTILIZER', 0)),
        'market_wool': int(obs.market['inventory']['WOOL']),
        'market_fertilizer': int(obs.market['inventory']['FERTILIZER']),
    }


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 217881086
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    paths = [ROOT / 'experiments/round11_early_expansion.py', ROOT / 'submissions/release_v9/main.py']
    entries = [get_last_callable(p.read_text(encoding='utf-8'), path=str(p)) for p in paths]
    env = make('kaggriculture', configuration={'seed': seed, 'episodeSteps': 720}, debug=True)
    env.run(entries)
    sys.path.insert(0, str(ROOT / 'research/round10'))
    from quantify_top_gap import digest_game
    game = env.toJSON()
    game.setdefault('info', {})['EpisodeId'] = -seed  # local replay has no Kaggle id
    exact = digest_game(game, 0, 'Round11 sheep candidate')
    errors = [str(x.get('stderr'))[:400] for row in env.logs for x in row if isinstance(x, dict) and x.get('stderr', '').strip()]
    active = {str(step): describe(env.steps[step][0]) for step in (266, 267, 272, 288, 312, 360, 432, 504, 624, 719)}
    purchases = env.steps[266][0].action.get('market', [])
    sales = {'WOOL': 0, 'FERTILIZER': 0}
    for step in range(267, 719):
        for order in env.steps[step][0].action.get('market', []):
            if len(order) >= 3 and order[:2] in (['SELL', 'WOOL'], ['SELL', 'FERTILIZER']):
                sales[order[1]] += int(order[2])
    result = {
        'seed': seed, 'candidate_sha256': hashlib.sha256(paths[0].read_bytes()).hexdigest(),
        'parent_sha256': hashlib.sha256(paths[1].read_bytes()).hexdigest(),
        'entry': entries[0].__name__, 'statuses': [x.status for x in env.steps[-1]],
        'errors': errors[:5], 'step_count': len(env.steps),
        'candidate_money': env.steps[-1][0].observation.farms[0]['money'],
        'opponent_money': env.steps[-1][1].observation.farms[1]['money'],
        'purchase_orders_step266': purchases,
        'requested_sale_units_all': sales,
        'candidate_telemetry': dict(entries[0].telemetry), 'checkpoints': active,
        'exact_stage_11_15': exact['stages']['11-15'],
        'exact_stage_16_20': exact['stages']['16-20'],
        'exact_stage_21_25': exact['stages']['21-25'],
        'exact_stage_26_29': exact['stages']['26-29'],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
