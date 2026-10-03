"""Three already-developed worlds approved for diagnostic task-executor repair."""
from collections import Counter
import contextlib
import gc
import gzip
import io
import json
from pathlib import Path
import runpy
import time
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
ROOT=Path(__file__).parent
OUT=ROOT/'research/round8/top2/task_release_screen.json'
rows=[]
for seed in (82001,82003,82005):
    ns=runpy.run_path(str(ROOT/'experiments/round8_top2_dsm_tasks_release.py'))
    proxy=ns['agent']
    env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720},debug=True)
    start=time.perf_counter()
    env.run([proxy,str(ROOT/'submissions/release_v7/main.py')])
    rewards=[s.reward for s in env.steps[-1]]
    errors=[v.get('stderr') for logs in env.logs for v in logs if v.get('stderr')]
    statuses=[s.status for s in env.steps[-1]]
    telemetry={key:dict(getattr(proxy,key,{})) for key in ('telemetry','routing_telemetry','task_telemetry')}
    st=ns['_R8_TASKS'].state[0]; seqs=ns['_R8_TASKS'].by_day[st['route']].get(29,{})
    unfinished=Counter(task['action'][0] for i,seq in seqs.items() for task in seq[st['indices'].get(i,0):])
    row={'variant':'dsm_tasks_release','seed':seed,'seat':0,'money':rewards[0],'opponent_money':rewards[1],'delta':rewards[0]-rewards[1],'statuses':statuses,'errors':errors,'diagnostics':telemetry,'final_day_unfinished_by_operation':dict(unfinished),'seconds':time.perf_counter()-start,'max_action_seconds':max((v.get('duration',0) for logs in env.logs for v in logs),default=0)}
    rows.append(row); OUT.write_text(json.dumps(rows,indent=2),encoding='utf-8')
    (OUT.parent/f'task_release_{seed}.json.gz').write_bytes(gzip.compress(json.dumps(env.toJSON(),separators=(',',':')).encode()))
    print(json.dumps(row),flush=True)
    assert statuses==['DONE','DONE'] and not errors and not any(telemetry['telemetry'].values())
    del ns,proxy,env
    gc.collect()
