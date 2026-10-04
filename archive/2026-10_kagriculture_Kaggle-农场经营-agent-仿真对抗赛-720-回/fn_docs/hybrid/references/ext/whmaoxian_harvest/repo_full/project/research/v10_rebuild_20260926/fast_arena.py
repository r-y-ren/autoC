"""Memory-bounded screening with unchanged official transition functions.
This is a local screening harness, not the official submission runner.
Validate against full official runs before using its results for selection.
"""
from pathlib import Path
from types import SimpleNamespace
from functools import lru_cache
import contextlib, copy, gc, hashlib, importlib, io, json, time, traceback
ROOT = Path(__file__).resolve().parents[2]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
class Attr(dict):
    def __getattr__(self, key):
        try: return self[key]
        except KeyError: raise AttributeError(key)
    def __setattr__(self, key, value): self[key] = value
@lru_cache(maxsize=128)
def source_code(path):
    return (ROOT/path).read_text(encoding='utf-8')
def load(path):
    return get_last_callable(source_code(path), path=str(ROOT/path))
def new_game(seed, config=None):
    cfg = Attr(actTimeout=1, boardSize=10, episodeSteps=720, farmHandCostMult=1,
        marketParams={}, maxMarketOrdersPerTurn=10, runTimeout=1200, seed=None,
        shedCapacity=100, startingMoney=3000, townCenterSellInterval=24,
        townShopSellInterval=4, townShopUnlockInterval=3, turnsPerDay=24, weedSpawnChance=.005)
    cfg.update(config or {})
    # Official initialization preserves configuration and observation defaults.
    initialized = make('kaggriculture', configuration=dict(cfg, seed=seed), debug=False)
    state = copy.deepcopy(initialized.state)
    env = SimpleNamespace(configuration=copy.deepcopy(initialized.configuration),
                          info=dict(initialized.info), done=False)
    for other in state[1:]:
        for key in ('farms', 'market', 'town'):
            other.observation[key] = state[0].observation[key]
    return state, env

def diagnostics(entry):
    values = {}
    def visit(value, prefix, depth=0):
        if depth > 4: return
        if isinstance(value, dict):
            for key, child in value.items(): visit(child, prefix+'.'+str(key), depth+1)
        elif isinstance(value, (int, float)) and value and any(s in prefix.lower() for s in ('error','fallback')):
            values[prefix] = value
    for name, value in entry.__globals__.items():
        if any(x in name.upper() for x in ('REPORT','STATS','DIAGNOSTIC')): visit(value, name)
        chassis = getattr(value, 'chassis', None)
        if chassis is not None: visit(getattr(chassis,'diagnostics',{}),name+'.chassis')
    visit(getattr(entry,'telemetry',{}),'entry')
    return values

def play(candidate, opponent, seed, seat=0, capture=False, config=None):
    start = time.perf_counter()
    entries = [load(candidate), load(opponent)]
    ordered = entries if seat == 0 else entries[::-1]
    state, env = new_game(seed, config)
    import inspect
    argument_counts = [len(inspect.signature(fn).parameters) for fn in ordered]
    durations = [[], []]
    trace = [copy.deepcopy(state)] if capture else None
    action_hashes = [hashlib.sha256(), hashlib.sha256()]
    invalid_actions = 0
    checkpoints = []
    for step in range(int(env.configuration.episodeSteps)-1):
        for i, fn in enumerate(ordered):
            state[i].observation.step = step
            obs = copy.deepcopy(state[i].observation)
            before = time.perf_counter()
            action = fn(*[obs, env.configuration][:argument_counts[i]])
            elapsed = time.perf_counter()-before
            durations[i].append(elapsed)
            if not isinstance(action, dict) or len(action.get('market', [])) > 10:
                invalid_actions += 1
            state[i].action = copy.deepcopy(action)
            action_hashes[i].update(json.dumps(action, sort_keys=True).encode())
        engine.interpreter(state, env)
        for s in state: s.observation.step = step+1
        if capture: trace.append(copy.deepcopy(state))
        if step in (23,47,71,143,239,479,695,718):
            farm = state[seat].observation.farms[seat]
            mix = {}
            for row in farm['tiles']:
                for tile in row:
                    if isinstance(tile,dict):
                        item = tile.get('animal') or tile.get('crop') or tile.get('kind')
                        mix[item] = mix.get(item,0)+1
            checkpoints.append(dict(step=step+1,money=farm['money'],mix=mix,hands=len(farm['hands'])))
    money = [state[seat].reward, state[1-seat].reward]
    errors = [diagnostics(entry) for entry in entries]
    result = dict(candidate=candidate, opponent=opponent, seed=seed, seat=seat,
        money=money, margin=money[0]-money[1], statuses=[s.status for s in state],
        max_seconds=max(durations[seat]), total_seconds=sum(durations[seat]),
        seconds=time.perf_counter()-start, errors=errors, invalid_actions=invalid_actions,
        action_hash=[h.hexdigest() for h in action_hashes],
        shops=list(state[0].observation.town['unlocked_shops']))
    result['valid'] = result['statuses']==['DONE','DONE'] and not any(errors) and not invalid_actions
    result['checkpoints'] = checkpoints
    result['final_inventory'] = dict(state[seat].observation.private['shed'])
    result['final_carried'] = sum(sum(inv.values()) for inv in state[seat].observation.private['inventories'])
    if capture: result['_trace'] = trace
    del state, env, entries, ordered
    gc.collect()
    return result

def run_job(job):
    started = time.perf_counter()
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = play(job['candidate'], job['opponent'], job['seed'], job.get('seat',0))
        result.update({k:v for k,v in job.items() if k not in result})
        result['stderr_stdout'] = output.getvalue()[:2000]
        if output.getvalue().strip(): result['valid'] = False
        return result
    except Exception:
        return dict(job, valid=False, exception=traceback.format_exc(), seconds=time.perf_counter()-started)
