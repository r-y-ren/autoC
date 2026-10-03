"""One diagnostic paired game with a fixed public-replay rival action tape.

The rival is not adaptive after our actions change; this is a mechanics smoke,
not evidence of competitive gain or a Round 10 development/confirmation game.
"""

from __future__ import annotations

import contextlib
import gzip
import hashlib
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPLAY = ROOT / 'research/round10/v9_public_replays/112476879.json.gz'
V9 = ROOT / 'experiments/round9_market_slack.py'
CANDIDATE = ROOT / 'experiments/round10_opening_cash.py'
OUT = ROOT / 'research/round10/opening_cash_public_replay_smoke.json'
V9_SHA = '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3'
CANDIDATE_SHA = 'dbbd2cee2d99385082eb39132e054c3ea0728cc5206824dceb500f3d52f1347c'
REPLAY_SHA = 'b1cdbb5ae2dac67d'  # provenance SHA prefix, verified below


def livestock(farm):
    counts = {}
    for row in farm['tiles']:
        for tile in row:
            if isinstance(tile, dict) and tile.get('animal'):
                animal = tile['animal']
                counts[animal] = counts.get(animal, 0) + 1
    return counts


def main():
    assert hashlib.sha256(V9.read_bytes()).hexdigest() == V9_SHA
    assert hashlib.sha256(CANDIDATE.read_bytes()).hexdigest() == CANDIDATE_SHA
    provenance = json.loads((ROOT / 'research/round10/v9_public_replay_provenance.json').read_text(encoding='utf-8'))
    record = next(x for x in provenance['replays'] if x['episode_id'] == 112476879)
    game_bytes = gzip.decompress(REPLAY.read_bytes())
    assert hashlib.sha256(game_bytes).hexdigest() == record['sha256']
    game = json.loads(game_bytes)
    assert game['info']['seed'] == 1392039591
    assert game['rewards'] == [90848.0, 107685.0]
    rival_actions = [game['steps'][t + 1][1]['action'] for t in range(719)]

    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable

    result = {}
    for label, source in (('v9', V9), ('candidate', CANDIDATE)):
        agent = get_last_callable(source.read_text(encoding='utf-8'), path=str(source))

        def recorded_rival(observation, configuration=None):
            return rival_actions[int(observation['step'])]

        conf = dict(game['configuration'], seed=game['info']['seed'])
        env = make('kaggriculture', configuration=conf, debug=True)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            env.run([agent, recorded_rival])
        checkpoints = {}
        for day, hour in ((0, 23), (1, 1), (1, 23), (2, 0), (5, 23), (10, 23), (29, 23)):
            step = day * 24 + hour
            obs = env.steps[step][0].observation
            farm = obs.farms[0]
            checkpoints[f'{day}:{hour}'] = {
                'cash': farm['money'],
                'hands': len(farm['hands']),
                'animals': livestock(farm),
                'wheat_shed': obs.private['shed'].get('WHEAT', 0),
            }
        result[label] = {
            'status': [s.status for s in env.steps[-1]],
            'rewards': [s.reward for s in env.steps[-1]],
            'checkpoints': checkpoints,
            'opening_action': env.steps[1][0].action,
        }
    result['warning'] = 'Replay action tape is fixed and nonadaptive; diagnostic only.'
    result['public_episode_id'] = 112476879
    result['public_seed'] = 1392039591
    result['v9_reproduces_public_rewards'] = result['v9']['rewards'] == game['rewards']
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: {'rewards': v['rewards'], 'checkpoints': v['checkpoints']}
                      for k, v in result.items() if k in ('v9', 'candidate')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
