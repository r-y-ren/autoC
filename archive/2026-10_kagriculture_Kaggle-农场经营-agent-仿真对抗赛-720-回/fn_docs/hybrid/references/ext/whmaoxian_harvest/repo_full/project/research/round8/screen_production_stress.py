"""Frozen default-rule trigger screen; prefixes are NOT completed games.

The official private runner is invoked identically to Environment.run so a
triggered prefix can continue with the same persistent agents and environment.
Configuration.episodeSteps is always 720. No saved hidden fields reach agents.
"""
import contextlib
import gc
import gzip
import hashlib
import io
import json
import os
import sys
import time
import traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.chdir(ROOT);sys.path.insert(0,str(ROOT))
from league_round8 import telemetry
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    import kaggle_environments
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
candidate='experiments/round8_production_delivery.py'
opponent='external/round8/master2965/main.py'
paths=[candidate,opponent]
hashes=[hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths]
assert hashes[0]=='05d9d50dd489f78a0561c717e483adef022d0fef1c52af604aed43e85508c02b'
assert 'V92_SELL_LIB' not in os.environ
seeds=[int.from_bytes(hashlib.sha256(f'r8-production-stress-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(80)]
league=json.loads((ROOT/'research/round8/league_seeds.json').read_text())
assert not(set(seeds)&{s for values in league.values() for s in values})
out=ROOT/'research/round8/production_stress';out.mkdir(parents=True,exist_ok=True)
manifest={'seed_generation':"int.from_bytes(sha256('r8-production-stress-'+str(i))[:4], 'big') % 2000000000",
          'seeds':seeds,'candidate':candidate,'opponent':opponent,'source_hashes':hashes,'seat':0,
          'configuration':{'episodeSteps':720},'prefix_state_count':434,'stop_after_actual_19plant_worlds':6,
          'exclusion':'all development, confirmation and reserve league seeds'}
mp=out/'manifest.json'
if mp.exists():assert json.loads(mp.read_text())==manifest
else:mp.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
ledger=out/'screen.jsonl'
rows=[json.loads(line) for line in ledger.read_text().splitlines()] if ledger.exists() else []
done={r['seed'] for r in rows}
complete=sum(r.get('actual_19plant_world',False) for r in rows)
for index,seed in enumerate(seeds):
    if seed in done:continue
    if complete>=6:break
    started=time.perf_counter()
    row={'index':index,'seed':seed,'seat':0,'kind':'prefix-only','configuration_episodeSteps':720}
    env=None;entries=None
    try:
        assert [hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths]==hashes
        sys.modules.pop('mirror_plan',None)
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            entries=[get_last_callable(Path(p).read_text(encoding='utf-8'),path=str(ROOT/p)) for p in paths]
        env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720},debug=True)
        env.reset(2)
        runner=env._Environment__agent_runner(entries)
        while not env.done and len(env.steps)<434:
            if time.perf_counter()-started>=env.configuration.runTimeout:raise TimeoutError('official runTimeout')
            actions,logs=runner.act();env.step(actions,logs)
        namespace=entries[0].__globals__
        state=namespace['_V219_STATES'].get(0,{})
        row['prefix_state']={k:v for k,v in state.items() if k in ('eligible','t19_enabled','committed','t19_forecast_value','t19_forecast_extra_labor')}
        row['prefix_shops']=list(env.steps[-1][0].observation.town['unlocked_shops'])
        triggered=bool(state.get('t19_enabled'))
        row['investment_triggered']=triggered
        if triggered:
            while not env.done:
                if time.perf_counter()-started>=env.configuration.runTimeout:raise TimeoutError('official runTimeout')
                actions,logs=runner.act();env.step(actions,logs)
            row['kind']='completed-triggered-game'
            final=env.steps[-1]
            row['money']=final[0].reward;row['opponent_money']=final[1].reward
            row['delta']=row['money']-row['opponent_money']
            row['actual_19plant_world']=namespace['_T19_REPORT']['plants']==19
            complete+=int(row['actual_19plant_world'])
            replay=out/f'seed{seed}-seat0-replay.json.gz'
            replay.write_bytes(gzip.compress(json.dumps(env.toJSON()).encode()))
            row['replay']=str(replay.relative_to(ROOT)).replace('\\','/')
        logs=[(i,l) for step in env.logs for i,l in enumerate(step) if isinstance(l,dict)]
        row['states']=len(env.steps);row['statuses']=[s.status for s in env.steps[-1]]
        row['stderr']=[{'seat':i,'text':l['stderr'][:1200]} for i,l in logs if l.get('stderr','').strip()]
        row['entry_names']=[e.__name__ for e in entries]
        row['telemetry']=[telemetry(e) for e in entries]
        row['production']=dict(namespace['_T19_REPORT'])
        row['max_action_seconds']=max((l.get('duration',0) for i,l in logs if i==0),default=0)
        row['valid']=not row['stderr'] and not row['telemetry'][0]['nonzero']
        if triggered:row['valid']=row['valid'] and row['states']==720 and row['statuses']==['DONE','DONE']
        else:row['valid']=row['valid'] and row['states']==434 and row['statuses']==['ACTIVE','ACTIVE']
    except Exception:
        row['valid']=False;row['exception']=traceback.format_exc()
    row['seconds']=round(time.perf_counter()-started,3)
    rows.append(row)
    with ledger.open('a',encoding='utf-8') as f:f.write(json.dumps(row)+'\n')
    summary={'screened_prefixes':len(rows),'completed_triggered':sum(r['kind']=='completed-triggered-game' for r in rows),
             'actual_19plant_worlds':sum(r.get('actual_19plant_world',False) for r in rows),
             'prefix_only':sum(r['kind']=='prefix-only' for r in rows),'invalid':sum(not r['valid'] for r in rows),
             'completed_results':[{k:r.get(k) for k in ('seed','money','opponent_money','delta','valid','actual_19plant_world')} for r in rows if r['kind']=='completed-triggered-game']}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps({k:row.get(k) for k in ('index','seed','kind','investment_triggered','actual_19plant_world','delta','valid','seconds')}),flush=True)
    del env,entries
    gc.collect()
print(json.dumps(summary),flush=True)
