"""72-turn functional checks. Never report these as completed games or wins."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import argparse,contextlib,copy,inspect,io,json,time,traceback
import fast_arena as arena

def prefix(job):
    started=time.perf_counter();output=io.StringIO()
    try:
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):
            entries=[arena.load(job['candidate']),arena.load(job['opponent'])]
            ordered=entries if not job['seat'] else entries[::-1]
            argc=[len(inspect.signature(f).parameters) for f in ordered]
            state,env=arena.new_game(job['seed']);checkpoints=[]
            for step in range(72):
                for i,entry in enumerate(ordered):
                    state[i].observation.step=step
                    state[i].action=entry(*[copy.deepcopy(state[i].observation),env.configuration][:argc[i]])
                arena.engine.interpreter(state,env)
                if step in (23,47,71):
                    f=state[job['seat']].observation.farms[job['seat']]
                    mix={}
                    for row in f['tiles']:
                        for tile in row:
                            if isinstance(tile,dict):
                                item=tile.get('animal') or tile.get('crop') or tile.get('kind')
                                mix[item]=mix.get(item,0)+1
                    checkpoints.append(dict(step=step+1,money=f['money'],mix=mix))
            errors=[arena.diagnostics(entry) for entry in entries]
        return dict(job,checkpoints=checkpoints,errors=errors,prefix_only=True,
                    valid=not any(errors) and not output.getvalue().strip(),seconds=time.perf_counter()-started)
    except Exception:
        return dict(job,prefix_only=True,valid=False,exception=traceback.format_exc())

def main():
    p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('output')
    p.add_argument('--workers',type=int,default=2);a=p.parse_args()
    jobs=json.loads(Path(a.manifest).read_text(encoding='utf-8'));out=Path(a.output)
    old=[json.loads(line) for line in out.read_text(encoding='utf-8').splitlines()] if out.exists() else []
    done={r['id'] for r in old};jobs=[j for j in jobs if j['id'] not in done]
    with ProcessPoolExecutor(max_workers=a.workers) as pool,out.open('a',encoding='utf-8') as f:
        futures=[pool.submit(prefix,job) for job in jobs]
        for future in as_completed(futures):
            row=future.result();old.append(row);f.write(json.dumps(row)+'\n');f.flush()
            if len(old)%40==0:print('Prefixes',len(old),flush=True)
    print('Functional checks finished',len(old),'invalid',sum(not r['valid'] for r in old),flush=True)
if __name__=='__main__':main()
