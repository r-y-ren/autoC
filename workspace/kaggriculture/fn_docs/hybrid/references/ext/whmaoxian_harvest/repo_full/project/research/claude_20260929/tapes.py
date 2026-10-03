"""Download replay, extract one seat's tape + context compactly, discard raw replay."""
import json,requests,gzip,os,sys,hashlib
from concurrent.futures import ThreadPoolExecutor
os.makedirs('tapes',exist_ok=True)
def extract(eid,sid):
    p=f'tapes/{eid}_{sid}.json.gz'
    if os.path.exists(p): return p
    raw=None
    rp=f'replays/{eid}.json.gz'
    if os.path.exists(rp): raw=gzip.decompress(open(rp,'rb').read())
    else:
        r=requests.get(f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json',timeout=120);r.raise_for_status();raw=r.content
    g=json.loads(raw)
    # find seat via ListEpisodes info is not in replay; match by team name later -> caller passes seat via sid lookup
    return g
def compact(g,seat):
    steps=g['steps']
    tape=[steps[t+1][seat]['action'] for t in range(len(steps)-1)]
    shops=[];money=[];omoney=[];prices=[];inv=[];tiles_day=[]
    last=None
    for t,s in enumerate(steps):
        o=s[seat]['observation']
        sh=o['town']['unlocked_shops']
        if sh!=last: shops.append([t,list(sh)]);last=list(sh)
        money.append(o['farms'][seat]['money']);omoney.append(o['farms'][1-seat]['money'])
        if o['hour']==0: tiles_day.append(o['farms'][seat]['tiles'])
    return dict(id=g['info']['EpisodeId'],seat=seat,names=g['info']['TeamNames'],rewards=g['rewards'],tape=tape,shops=shops,money=money,omoney=omoney,tiles_day=tiles_day,
                prices=[steps[t][seat]['observation']['market']['prices'] for t in range(0,720,24)])
def job(args):
    eid,sid,seat=args
    p=f'tapes/{eid}_{sid}.json.gz'
    if os.path.exists(p): return eid,'cached'
    try:
        g=extract(eid,sid)
        c=compact(g,seat);c['sid']=sid
        open(p,'wb').write(gzip.compress(json.dumps(c).encode()))
        return eid,'ok'
    except Exception as e: return eid,repr(e)[:100]
if __name__=='__main__':
    from episodes import rows
    sid=int(sys.argv[1]);n=int(sys.argv[2])
    rs=rows(sid,json.load(open(f'eplists/{sid}.json')))[-n:]
    with ThreadPoolExecutor(6) as p:
        for x in p.map(job,[(r['ep'],sid,r['seat']) for r in rs]): print(x,flush=True)
