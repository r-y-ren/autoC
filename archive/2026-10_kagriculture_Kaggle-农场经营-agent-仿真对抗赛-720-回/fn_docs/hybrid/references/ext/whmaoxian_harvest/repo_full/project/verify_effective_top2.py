"""Verify effective-order compilation preserves original outcomes (study only)."""
import contextlib
import gzip
import io
import json
from pathlib import Path
from benchmark_replays import tape_policy
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
OUT=Path(__file__).parent/'research/round7/top2'
routes=json.loads((OUT/'effective_routes.json').read_text())['routes']
results=[]
for row in [routes[0],routes[3]]:
    game=json.loads(gzip.decompress((OUT/f"{row['episode_id']}.json.gz").read_bytes()))
    players=[tape_policy([s[p]['action'] for s in game['steps'][1:]]) for p in range(2)]
    players[row['seat']]=tape_policy(row['actions'])
    env=make('kaggriculture',configuration=dict(game['configuration'],seed=game['info']['seed']),debug=True)
    env.run(players)
    rewards=[s.reward for s in env.steps[-1]]
    assert rewards==game['rewards'],(row['episode_id'],rewards,game['rewards'])
    assert [s.status for s in env.steps[-1]]==['DONE','DONE']
    assert not [v.get('stderr') for logs in env.logs for v in logs if v.get('stderr')]
    results.append({'episode_id':row['episode_id'],'team':row['team'],'rewards':rewards,'compiled_non_sell_preserves_original_rewards':True})
    (OUT/'effective_route_checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(row['team'],row['episode_id'],rewards,'compiled matches exactly',flush=True)
