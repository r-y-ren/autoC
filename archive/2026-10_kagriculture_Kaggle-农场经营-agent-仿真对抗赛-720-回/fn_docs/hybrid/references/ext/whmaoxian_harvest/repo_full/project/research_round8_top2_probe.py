"""Small predeclared proxy feasibility screen, not release model selection."""
import contextlib
import gc
import io
import json
from pathlib import Path
import runpy
import time
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make

ROOT=Path(__file__).parent
OUT=ROOT/'research/round8/top2/proxy_screen.json'
PANEL=[('vadim_strict',82000),('dsm_strict',82001),('vadim_tasks',82002),('dsm_tasks',82003),('vadim_strict',82004),('dsm_strict',82005)]
rows=[]
for variant,seed in PANEL:
    for seat in (0,1):
        ns=runpy.run_path(str(ROOT/f'experiments/round8_top2_{variant}.py'))
        proxy=ns['agent']
        env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720},debug=True)
        players=[proxy,str(ROOT/'submissions/release_v7/main.py')]
        if seat:
            players.reverse()
        start=time.perf_counter(); env.run(players)
        rewards=[s.reward for s in env.steps[-1]]
        errors=[v.get('stderr') for logs in env.logs for v in logs if v.get('stderr')]
        statuses=[s.status for s in env.steps[-1]]
        telemetry={key:dict(getattr(proxy,key,{})) for key in ('telemetry','routing_telemetry','task_telemetry')}
        row={'variant':variant,'seed':seed,'seat':seat,'money':rewards[seat],'opponent_money':rewards[1-seat],'delta':rewards[seat]-rewards[1-seat],'statuses':statuses,'errors':errors,'diagnostics':telemetry,'seconds':time.perf_counter()-start}
        rows.append(row); OUT.write_text(json.dumps(rows,indent=2),encoding='utf-8')
        print(json.dumps(row),flush=True)
        assert statuses==['DONE','DONE'] and not errors
        assert not any(telemetry['telemetry'].values())
        del ns,proxy,env,players
        gc.collect()
