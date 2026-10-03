"""Finite macro league; observe original official functions without altering results."""
from pathlib import Path
from collections import Counter
from concurrent.futures import ProcessPoolExecutor,as_completed
import contextlib,hashlib,io,json,sys,time,traceback
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena as fa

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def run_job(job):
    start=time.perf_counter();engine=fa.engine;loaded=[];ctx={}
    stats=[dict(sales=Counter(),revenue=Counter(),purchases=Counter(),harvest=Counter(),wages=0,land=0,hires=0) for _ in range(2)]
    names=('_process_market','_commit_unit','_do_hire','_do_buy_land','_apply_unit_action')
    originals={name:getattr(engine,name) for name in names};loader=fa.load
    def load(path):
        fn=loader(path);loaded.append(fn);return fn
    def market(state,env):
        ctx['ids']=[id(f) for f in state[0].observation.farms]
        return originals['_process_market'](state,env)
    def commit(op,item,price,farm,private,market,shed_capacity=100):
        before=farm['money'];ok=originals['_commit_unit'](op,item,price,farm,private,market,shed_capacity)
        if ok:
            row=stats[ctx['ids'].index(id(farm))];delta=farm['money']-before
            if op=='SELL':row['sales'][item]+=1;row['revenue'][item]+=delta
            else:row['purchases'][op+':'+item]-=delta
        return ok
    def hire(farm,private,board_size,mult=1):
        before=farm['money'];count=len(farm['hands'])
        result=originals['_do_hire'](farm,private,board_size,mult)
        row=stats[ctx['ids'].index(id(farm))];row['wages']+=before-farm['money']
        row['hires']+=len(farm['hands'])-count;return result
    def land(farm,board_size):
        before=farm['money'];result=originals['_do_buy_land'](farm,board_size)
        stats[ctx['ids'].index(id(farm))]['land']+=before-farm['money'];return result
    def unit(farm,private,idx,action,board_size,day,turns_per_day,shed_capacity=100):
        tracked=bool(action and action[0]=='HARVEST' and idx<len(private['inventories']))
        before=dict(private['inventories'][idx]) if tracked else {}
        result=originals['_apply_unit_action'](farm,private,idx,action,board_size,day,turns_per_day,shed_capacity)
        if tracked:
            row=stats[ctx['ids'].index(id(farm))]
            for item,n in private['inventories'][idx].items():row['harvest'][item]+=max(0,n-before.get(item,0))
        return result
    output=io.StringIO()
    try:
        for k in ('candidate','opponent'):assert digest(R/job[k])==job[k+'_sha256']
        for name,fn in zip(names,(market,commit,hire,land,unit)):setattr(engine,name,fn)
        fa.load=load
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):
            result=fa.play(job['candidate'],job['opponent'],job['seed'],job['seat'])
        ns=loaded[0].__globals__;result.update({k:v for k,v in job.items() if k not in result})
        result['economics']=[stats[job['seat']],stats[1-job['seat']]]
        result['macro']={name:dict(ns.get(name,{})) for name in ('_MP_REPORT','_CA_REPORT','_HD2_REPORT','_CS_REPORT','_T19_REPORT')}
        for row,money in zip(result['economics'],result['money']):
            assert 3000+sum(row['revenue'].values())-sum(row['purchases'].values())-row['wages']-row['land']==money
        result['cash_identity_checked']=True;result['captured_output']=output.getvalue()[:2000]
        if output.getvalue().strip():result['valid']=False
        return result
    except Exception:
        return dict(job,valid=False,exception=traceback.format_exc(),seconds=time.perf_counter()-start)
    finally:
        fa.load=loader
        for name,fn in originals.items():setattr(engine,name,fn)

def batch(pool,command):
    manifest=Path(command['manifest']);output=Path(command['output'])
    jobs=json.loads(manifest.read_text());expected={j['id']:j for j in jobs};assert len(expected)==len(jobs)
    prior=[json.loads(s) for s in output.read_text().splitlines()] if output.exists() else []
    assert len({r['id'] for r in prior})==len(prior)
    for row in prior:assert all(row.get(k)==v for k,v in expected[row['id']].items())
    done={r['id'] for r in prior};pending=[j for j in jobs if j['id'] not in done]
    print(json.dumps(dict(event='start',total=len(jobs),existing=len(prior))),flush=True)
    with output.open('a',encoding='utf-8') as handle:
        futures=[pool.submit(run_job,job) for job in pending]
        for f in as_completed(futures):
            row=f.result();prior.append(row);handle.write(json.dumps(row)+'\n');handle.flush()
            if len(prior)%48==0 or not row.get('valid'):print(json.dumps(dict(event='progress',done=len(prior),total=len(jobs),valid=row.get('valid'))),flush=True)
    print(json.dumps(dict(event='complete',total=len(prior),invalid=sum(not r.get('valid') for r in prior))),flush=True)
if __name__=='__main__':
    with ProcessPoolExecutor(max_workers=6) as pool:
        print('ARENA_READY',flush=True)
        for line in sys.stdin:
            command=json.loads(line)
            if command.get('exit'):break
            batch(pool,command);print('ARENA_READY',flush=True)
