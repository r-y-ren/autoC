"""Official path-loaded full game, compared to the old explicit policy every turn.

This known failing development world is a technical fixture, not a fresh rating
sample or an additional independent strategy test.
"""
import contextlib,hashlib,io,json,runpy,time
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
ROOT=Path(__file__).parent
OUT=ROOT/'research/round8/top2'
OLD=ROOT/'experiments/round8_top2_dsm_contract.py'
NEW=ROOT/'experiments/round8_top2_dsm_contract_entry.py'
OPP=ROOT/'external/round8/fieldcraft/main.py'
old_hash=hashlib.sha256(OLD.read_bytes()).hexdigest()
new_hash=hashlib.sha256(NEW.read_bytes()).hexdigest()
assert old_hash=='7735d6f4293495a0942a21fb92f6ff6aaec339dc759375e1ecdbe6226c6f2c53'
assert new_hash=='23768116945ebd7500b2e2298616ff6dd974d27ce2c839643cc7d3e3d4cada57'
official_entry=get_last_callable(NEW.read_text(encoding='utf-8'),path=str(NEW))
assert official_entry.__name__=='round8_dsm_contract_agent'
old_ns=runpy.run_path(str(OLD));old_explicit=old_ns['agent']
assert old_explicit.__name__=='agent'
env=make('kaggriculture',configuration={'seed':733556107,'episodeSteps':720},debug=True)
original_interpreter=env.interpreter
comparisons=[]
def interpreter(state,game):
    if getattr(state[0].observation,'farms',None):
        step=state[0].observation['step']
        expected=old_explicit(state[0].observation,game.configuration)
        actual=state[0].action
        assert expected==actual,('policy mismatch',step,expected,actual)
        comparisons.append({'step':step,'action':json.loads(json.dumps(actual))})
    return original_interpreter(state,game)
env.interpreter=interpreter
started=time.perf_counter()
# This deliberately uses the FILE PATH. Compilation and embedded-data loading
# occur inside the official first-action timer, not in a preloaded function.
env.run([str(NEW),str(OPP)])
duration=time.perf_counter()-started
statuses=[s.status for s in env.steps[-1]]
rewards=[s.reward for s in env.steps[-1]]
logs=[r[0] for r in env.logs if r and isinstance(r[0],dict)]
stderr=[v.get('stderr') for row in env.logs for v in row if v.get('stderr')]
assert statuses==['DONE','DONE'] and len(env.steps)==720 and not stderr
assert len(comparisons)==719 and [r['step'] for r in comparisons]==list(range(719))
assert not any(old_explicit.telemetry.values())
assert rewards==[152686.0,151317.0],rewards
assert logs[0]['duration']<1.0 and max(x.get('duration',0) for x in logs)<1.0
report={
    'old_explicit_source_sha256':old_hash,'new_entry_source_sha256':new_hash,
    'official_loader_entry':'round8_dsm_contract_agent',
    'loading_mode':'official file path passed to env.run; first callback includes compilation/decompression',
    'seed':733556107,'seat':0,'opponent':str(OPP.relative_to(ROOT)),
    'kind':'technical fixture on an already developed world; not independent policy evidence',
    'states':len(env.steps),'all_actions_equal':len(comparisons),
    'action_sha256':hashlib.sha256(json.dumps(comparisons,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
    'statuses':statuses,'stderr':stderr,'rewards':rewards,'matches_previous_explicit_agent_rewards':True,
    'first_action_seconds':logs[0]['duration'],'max_action_seconds':max(x.get('duration',0) for x in logs),
    'old_policy_telemetry':dict(old_explicit.telemetry),
    'cash_repair_telemetry':dict(old_explicit.contract_telemetry),
    'total_seconds':duration,'passed':True}
(OUT/'contract_entry_full_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)
