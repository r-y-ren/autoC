import sys,io,contextlib,os,time
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
env=make('kaggriculture',configuration={'seed':int(sys.argv[2]),'episodeSteps':720},debug=True)
env.run([os.path.abspath(sys.argv[1]),os.path.abspath('cand/r2.py')])
d=[l[0].get('duration',0) for l in env.logs if l and isinstance(l[0],dict)]
err=[l[0].get('stderr','') for l in env.logs if l and isinstance(l[0],dict) and l[0].get('stderr')]
print('status',[s.status for s in env.steps[-1]],'money',[env.steps[-1][i].observation.farms[i]['money'] for i in (0,1)],'max step s',round(max(d),3),'mean',round(sum(d)/len(d),4),'stderr',len(err))
