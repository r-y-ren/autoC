"""Read-only gate probe on existing diagnostic replays, not a score estimate."""

from pathlib import Path
import contextlib
import gzip
import io
import json

ROOT = Path(__file__).resolve().parents[2]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments.agent import get_last_callable

candidate = ROOT / 'experiments/round10_crop_portfolio_v2.py'
entry = get_last_callable(candidate.read_text(encoding='utf-8'), path=str(candidate))
namespace = entry.__globals__
for name in ('audit_dsm_1829941733','audit_dsm_264393735','audit_dsm_242588832',
             'audit_frontier_867611781'):
    with gzip.open(ROOT / ('research/round10/' + name + '.json.gz'), 'rt', encoding='utf-8') as stream:
        replay = json.load(stream)
    for step in range(264):
        entry(replay['steps'][step][0]['observation'])
    obs = replay['steps'][264][0]['observation']
    native = namespace['_IMPL'].chassis.players.get(0, {})
    print(name, 'native_route', native.get('route'),
          'structural', namespace['_r10cp_native_structure'](obs),
          'choice', namespace['_r10cp_choice'](obs))
    for k in (0,5,9,13):
        berry = namespace['_r10cp_mean_and_tail'](namespace['_r10cp_scenario_values'](obs,'STRAWBERRY',13-k))
        tomato = namespace['_r10cp_mean_and_tail'](namespace['_r10cp_scenario_values'](obs,'TOMATO',k))
        score = 0.7*(berry[0]+tomato[0])+0.3*(berry[1]+tomato[1])+50*k
        print(' ',k,'berry',tuple(round(x) for x in berry),'tomato',tuple(round(x) for x in tomato),'score',round(score))
