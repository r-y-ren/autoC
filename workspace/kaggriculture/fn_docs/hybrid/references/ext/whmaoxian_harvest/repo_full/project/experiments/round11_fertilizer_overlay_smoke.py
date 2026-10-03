"""Official 720-step fertilizer overlay smoke and physical production audit."""
import contextlib
import hashlib
import io
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 217881086
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    paths = [ROOT / 'experiments/round11_fertilizer_overlay.py',
             ROOT / 'submissions/release_v9/main.py']
    entries = [get_last_callable(p.read_text(encoding='utf-8'), path=str(p)) for p in paths]
    env = make('kaggriculture', configuration={'seed': seed, 'episodeSteps': 720}, debug=True)
    env.run(entries)
    physical = []
    for step in range(264, 696):
        obs = env.steps[step][0].observation
        farm = obs.farms[0]
        positions = [farm['farmer'], *farm['hands']]
        action = env.steps[step][0].action
        commands = [action.get('farmer') or ['PASS'], *list(action.get('hands') or [])]
        for actor, cmd in enumerate(commands[:len(positions)]):
            if cmd != ['FERTILIZE']:
                continue
            x, y = positions[actor]
            before = farm['tiles'][y][x]
            after = env.steps[step+1][0].observation.farms[0]['tiles'][y][x]
            if not isinstance(before, dict) or before.get('crop') not in ('STRAWBERRY', 'TOMATO'):
                continue
            physical.append({
                'step': step, 'actor': actor, 'site': [x, y], 'crop': before['crop'],
                'watered': before['watered_today'], 'before_until': before['fertilized_until_day'],
                'after_until': after.get('fertilized_until_day') if isinstance(after, dict) else None,
                'before_yield': before['yield_units'],
                'after_yield': after.get('yield_units') if isinstance(after, dict) else None,
            })
    errors = [str(x.get('stderr'))[:400] for row in env.logs for x in row
              if isinstance(x, dict) and x.get('stderr', '').strip()]
    result = {
        'seed': seed, 'source_sha256': hashlib.sha256(paths[0].read_bytes()).hexdigest(),
        'entry': entries[0].__name__, 'states': len(env.steps),
        'statuses': [x.status for x in env.steps[-1]], 'errors': errors[:5],
        'money': [env.steps[-1][i].observation.farms[i]['money'] for i in (0, 1)],
        'telemetry': dict(entries[0].telemetry),
        'physical_fertilize_actions': len(physical),
        'physical_examples': physical[:12],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
