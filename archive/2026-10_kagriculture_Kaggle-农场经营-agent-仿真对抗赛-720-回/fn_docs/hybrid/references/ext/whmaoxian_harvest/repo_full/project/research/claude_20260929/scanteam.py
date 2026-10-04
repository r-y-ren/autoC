import requests,time,sys,json
URL='https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes'
def q(sid):
    while True:
        r=requests.post(URL,json={'submissionId':sid},timeout=60)
        if r.status_code==429: time.sleep(20); continue
        return r.json()
lo,hi=int(sys.argv[1]),int(sys.argv[2])
# alternate outward from center
c=(lo+hi)//2; order=[c]
for k in range(1,(hi-lo)//2+1): order+= [c+k,c-k]
for sid in order:
    d=q(sid)
    for s in d.get('submissions',[]):
        if s['id']==sid and s['teamId']==16899200:
            print('FOUND',sid,s,len(d.get('episodes',[])),flush=True)
            json.dump(d,open(f'eplists/{sid}.json','w'))
    time.sleep(1.2)
