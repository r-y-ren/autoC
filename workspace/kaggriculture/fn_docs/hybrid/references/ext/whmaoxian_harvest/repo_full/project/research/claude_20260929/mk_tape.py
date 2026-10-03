"""Build a candidate that replays given tapes with R2's chassis. usage: mk_tape.py out.py mode tapefiles..."""
import sys,json,gzip,base64,zlib
out,mode=sys.argv[1],sys.argv[2];files=sys.argv[3:]
tapes=[];meta=[]
for f in files:
    c=json.loads(gzip.decompress(open(f,'rb').read()))
    tapes.append(c['tape']);meta.append(dict(id=c['id'],shops=[s for t,s in c['shops']][-1]))
blob=base64.b85encode(zlib.compress(json.dumps(dict(tapes=tapes,meta=meta)).encode(),9)).decode()
src=open('chassis.py',encoding='utf-8').read()
src+=f'''
import base64 as _b64,zlib as _zl,json as _js
_D=_js.loads(_zl.decompress(_b64.b85decode({blob!r})))
_T={{i:t for i,t in enumerate(_D['tapes'])}}
_M=_D['meta']
MODE={mode!r}
def _router(obs,step,st):
    if MODE=='fixed': return 0
    shops=list((obs.get('town') or {{}}).get('unlocked_shops') or [])
    if 'route' not in st: st['route']=0
    if MODE=='shop2' and step>=144 and not st.get('done'):
        best=0;bs=-1
        for i,m in enumerate(_M):
            s=sum(1 for a,b in zip(m['shops'],shops) if a==b)
            if s>bs: bs=s;best=i
        st['route']=best;st['done']=True
    return st['route']
_S={{'hand_align': True, 'weed_repair': True, 'sell_lead': True, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False}}
_IMPL=make_agent(_T,router=_router,**_S)
def agent(observation,configuration=None):
    return _IMPL(observation,configuration)
'''
open(out,'w',encoding='utf-8').write(src)
print(out,len(src))
