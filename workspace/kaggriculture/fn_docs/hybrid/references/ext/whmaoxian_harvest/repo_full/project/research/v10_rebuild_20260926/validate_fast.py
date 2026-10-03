"""Validate the screening transition wrapper against complete official games."""
from pathlib import Path
import copy, json, sys, time
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fast_arena as arena
OUT = Path(__file__).resolve().parent
A = 'submissions/release_v10/main.py'
B = 'submissions/release_v9/main.py'
def canonical(obs):
    result = copy.deepcopy(dict(obs))
    result.pop('remainingOverageTime', None)
    return json.dumps(result, sort_keys=True)
results = []
for seed in (0, 907121):
    official = arena.make('kaggriculture', configuration={'seed':seed,'episodeSteps':720}, debug=True)
    began = time.perf_counter()
    official.run([str(arena.ROOT/A), str(arena.ROOT/B)])
    elapsed = time.perf_counter()-began
    state, env = arena.new_game(seed)
    differences = []
    for step in range(719):
        for seat in (0,1):
            state[seat].observation.step = step
            state[seat].action = copy.deepcopy(official.steps[step+1][seat].action)
        arena.engine.interpreter(state, env)
        for seat in (0,1):
            state[seat].observation.step = step+1
            if canonical(state[seat].observation) != canonical(dict(official.steps[step+1][seat].observation, step=step+1)):
                differences.append([step+1,seat])
    check = dict(seed=seed, official_seconds=elapsed, matching_observations=1438-len(differences),
                 differences=differences[:10], official_money=[s.reward for s in official.steps[-1]],
                 replayed_money=[s.reward for s in state])
    results.append(check)
    print(json.dumps(check), flush=True)
    (OUT/'fast_transition_validation.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    assert not differences
    screened = arena.play(A,B,seed)
    print('Independent screen', json.dumps(screened), flush=True)
print('Screening transition validation PASSED', flush=True)
