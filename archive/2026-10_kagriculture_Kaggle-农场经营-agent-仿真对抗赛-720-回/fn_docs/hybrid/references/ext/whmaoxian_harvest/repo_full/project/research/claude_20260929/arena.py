"""Minimal paired arena. usage: python arena.py cand.py opp.py seeds(N or a-b) [workers] [tag]"""
import sys,os,io,json,time,contextlib,traceback
from concurrent.futures import ProcessPoolExecutor
def run(job):
    cand,opp,seed,seat=job
    t0=time.time()
    try:
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments import make
            from kaggle_environments.agent import get_last_callable
            ents=[get_last_callable(open(p,encoding='utf-8').read(),path=os.path.abspath(p)) for p in (cand,opp)]
            order=ents[::-1] if seat else ents
            env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720},debug=False)
            env.run(order)
        f=env.steps[-1]
        m=[f[i].observation.farms[i]['money'] for i in (seat,1-seat)]
        st=[x.status for x in f]
        return dict(cand=cand,opp=opp,seed=seed,seat=seat,me=m[0],op=m[1],status=st,shops=list(f[0].observation.town['unlocked_shops']),sec=round(time.time()-t0,1))
    except Exception:
        return dict(cand=cand,opp=opp,seed=seed,seat=seat,err=traceback.format_exc()[-800:])
if __name__=='__main__':
    cand,opp,seeds=sys.argv[1],sys.argv[2],sys.argv[3]
    w=int(sys.argv[4]) if len(sys.argv)>4 else 24
    tag=sys.argv[5] if len(sys.argv)>5 else os.path.basename(cand)+'_vs_'+os.path.basename(opp)
    if '-' in seeds: a,b=map(int,seeds.split('-')); S=range(a,b)
    else: S=range(1000,1000+int(seeds))
    jobs=[(cand,opp,s,seat) for s in S for seat in (0,1)]
    os.makedirs('results',exist_ok=True)
    out=open(f'results/{tag}.jsonl','a')
    res=[]
    with ProcessPoolExecutor(w) as p:
        for r in p.map(run,jobs):
            res.append(r);out.write(json.dumps(r)+'\n');out.flush()
    ok=[r for r in res if 'me' in r]
    W=sum(r['me']>r['op'] for r in ok);L=sum(r['me']<r['op'] for r in ok)
    print(tag,'games',len(res),'ok',len(ok),'W',W,'L',L,'T',len(ok)-W-L,'mean me',round(sum(r['me'] for r in ok)/max(1,len(ok))),'mean op',round(sum(r['op'] for r in ok)/max(1,len(ok))),'ratio',round(sum(r['me'] for r in ok)/max(1,sum(r['op'] for r in ok)),3))
    for r in res:
        if 'err' in r: print(r['err']);break
