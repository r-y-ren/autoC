import sys,io,contextlib,json,gzip,collections
from anal import tilecount
cand,opp,seed=sys.argv[1],sys.argv[2],int(sys.argv[3]);tapef=sys.argv[4] if len(sys.argv)>4 else None
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable
    ents=[get_last_callable(open(p,encoding='utf-8').read(),path=p) for p in (cand,opp)]
env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720});env.run(ents)
ref=json.loads(gzip.decompress(open(tapef,'rb').read())) if tapef else None
for t,s in enumerate(env.steps):
    o=s[0].observation
    if o.hour==0 and o.day%2==0:
        f=o.farms[0]
        line=f"d{o.day:2d} ${f['money']:7.0f} q={len(f['unlocked_quadrants'])} {tilecount(f['tiles'])}"
        if ref: 
            d=o.day; line+=f"\n     ref ${ref['money'][t]:7.0f} {tilecount(ref['tiles_day'][d])}"
        print(line)
print('final',[env.steps[-1][i].observation.farms[i]['money'] for i in (0,1)])
