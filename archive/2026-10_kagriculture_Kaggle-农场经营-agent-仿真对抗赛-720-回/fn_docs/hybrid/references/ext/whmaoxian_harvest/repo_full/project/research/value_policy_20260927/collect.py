"""Counterfactual supervision in local Kaggriculture games; never submit or network."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import contextlib,copy,hashlib,inspect,io,json,sys,time,traceback
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
sys.path.insert(0,str(R/'research/v10_top10_20260926'))
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):import fast_arena as fa
import market_bc_features as ft
from policy import vp_options,vp_action,vp_sync
BASE='submissions/release_v10_r2/main.py'

def continuation(trace,job,at,item=None,quantity=0):
    entries=[fa.load(BASE),fa.load(job['opponent'])]
    seat=job['seat'];ordered=entries if seat==0 else entries[::-1]
    state,env=fa.new_game(job['seed']);config=env.configuration
    assert config.get('seed') is None
    argc=[len(inspect.signature(fn).parameters) for fn in ordered]
    for step in range(at):
        for p,fn in enumerate(ordered):
            obs=copy.deepcopy(trace[step][p].observation);obs['step']=step
            action=fn(*[obs,config][:argc[p]])
            if action!=trace[step+1][p].action:raise AssertionError(('prefix replay mismatch',step,p))
    state=copy.deepcopy(trace[at])
    for step in range(at,719):
        for p,fn in enumerate(ordered):
            state[p].observation.step=step;obs=copy.deepcopy(state[p].observation)
            action=fn(*[obs,config][:argc[p]])
            if step==at and p==seat and quantity:
                action=vp_action(action,item,quantity);vp_sync(obs,action,fn.__globals__)
            state[p].action=copy.deepcopy(action)
        fa.engine.interpreter(state,env)
        for s in state:s.observation.step=step+1
    errors=[fa.diagnostics(fn) for fn in entries]
    return {'money':[state[seat].reward,state[1-seat].reward],'valid':all(s.status=='DONE' for s in state) and not any(errors),'errors':errors}

def gather(job):
    started=time.perf_counter();output=io.StringIO()
    try:
        assert hashlib.sha256((R/BASE).read_bytes()).hexdigest()==job['baseline_sha256']
        assert hashlib.sha256((R/job['opponent']).read_bytes()).hexdigest()==job['opponent_sha256']
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):
            baseline=fa.play(BASE,job['opponent'],job['seed'],job['seat'],capture=True)
            trace=baseline.pop('_trace');assert baseline['valid'],baseline.get('errors')
            control=continuation(trace,job,384)
            assert control['valid'] and control['money']==baseline['money'],('fork control mismatch',control)
            entry=fa.load(BASE);ns=entry.__globals__;history={};opportunities=[]
            for step in range(719):
                obs=copy.deepcopy(trace[step][job['seat']].observation);obs['step']=step
                action=trace[step+1][job['seat']].action
                projected=ns['projected_shed'](action,ns['FarmView'](obs))
                ctx=ft._mbc_context(obs,action,projected,history)
                options=vp_options(obs,action,projected)
                for item,quantities,original,spare in options:
                    opportunities.append(dict(step=step,item=item,quantities=quantities,original=original,spare=spare,features=ft._mbc_features(ctx,item)))
                sold={item:min(max(0,int(projected.get(item,0))),sum(max(0,int(o[2])) for o in action.get('market',[]) if len(o)>=3 and o[:2]==['SELL',item])) for item in ft._MBC_ITEMS}
                ft._mbc_commit(ctx,sold)
            selected=[]
            for low in range(144,672,44):
                group=[o for o in opportunities if low<=o['step']<low+44]
                if group:
                    chosen=min(group,key=lambda o:hashlib.sha256(f"{job['id']}:{o['step']}:{o['item']}".encode()).hexdigest())
                    selected.append(chosen)
            samples=[]
            for opportunity in selected:
                for quantity in opportunity['quantities']:
                    branch=continuation(trace,job,opportunity['step'],opportunity['item'],quantity)
                    gain=(branch['money'][0]-branch['money'][1])-baseline['margin']
                    features=opportunity['features']+[float(quantity),float(opportunity['original']),float(opportunity['spare'])]
                    assert len(features)==48
                    samples.append(dict(step=opportunity['step'],item=opportunity['item'],quantity=quantity,features=features,gain=gain,branch=branch))
            result=dict(job,baseline={k:v for k,v in baseline.items() if k!='checkpoints'},samples=samples,control=control,seconds=time.perf_counter()-started,valid=all(s['branch']['valid'] for s in samples))
        result['captured_output']=output.getvalue()[:1500]
        if output.getvalue().strip():result['valid']=False
        return result
    except Exception:return dict(job,valid=False,exception=traceback.format_exc(),seconds=time.perf_counter()-started)

if __name__=='__main__':
    manifest=D/'training_jobs.json';output=D/'training_results.jsonl'
    jobs=json.loads(manifest.read_text());prior=[json.loads(s) for s in output.read_text().splitlines()] if output.exists() else []
    done={r['id'] for r in prior};assert len(done)==len(prior)
    with ProcessPoolExecutor(max_workers=4) as pool,output.open('a',encoding='utf-8') as handle:
        futures=[pool.submit(gather,j) for j in jobs if j['id'] not in done]
        for future in as_completed(futures):
            row=future.result();handle.write(json.dumps(row)+'\n');handle.flush();prior.append(row)
            print(json.dumps(dict(done=len(prior),total=len(jobs),valid=row['valid'],branches=len(row.get('samples',[])),seconds=round(row.get('seconds',0),2))),flush=True)
    print(json.dumps(dict(complete=True,jobs=len(prior),invalid=sum(not r['valid'] for r in prior),branches=sum(len(r.get('samples',[])) for r in prior))),flush=True)
