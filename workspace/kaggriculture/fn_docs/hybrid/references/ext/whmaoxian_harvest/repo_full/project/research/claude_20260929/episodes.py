import json,requests,sys,os
from concurrent.futures import ThreadPoolExecutor
URL='https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes'
os.makedirs('eplists',exist_ok=True)
def get(sid):
    p=f'eplists/{sid}.json'
    r=requests.post(URL,json={'submissionId':sid},timeout=60);r.raise_for_status()
    open(p,'w').write(r.text);return sid,r.json()
def rows(sid,data):
    out=[]
    for e in data.get('episodes',[]):
        a=e.get('agents',[]);mine=[x for x in a if x['submissionId']==sid]
        if e.get('state')!='COMPLETED' or len(a)!=2 or len(mine)!=1:continue
        me=mine[0];o=[x for x in a if x is not me][0]
        out.append(dict(ep=e['id'],end=e.get('endTime',''),type=e.get('type'),seat=me.get('index',0),my=me.get('reward'),opp=o.get('reward'),oppsid=o['submissionId'],oppr=o.get('initialScore'),myr=me.get('updatedScore')))
    return sorted(out,key=lambda x:x['end'])
if __name__=='__main__':
    sids=[int(s) for s in sys.argv[1:]]
    with ThreadPoolExecutor(6) as p: res=list(p.map(get,sids))
    for sid,d in res:
        rs=rows(sid,d)
        mys=[r['my'] for r in rs if r['my'] is not None];ops=[r['opp'] for r in rs if r['opp'] is not None]
        w=sum((r['my'] or 0)>(r['opp'] or 0) for r in rs);l=sum((r['my'] or 0)<(r['opp'] or 0) for r in rs)
        print(sid,'games',len(rs),'W',w,'L',l,'mean my',round(sum(mys)/max(1,len(mys))),'mean opp',round(sum(ops)/max(1,len(ops))),'last rating',rs[-1]['myr'] if rs else None)
