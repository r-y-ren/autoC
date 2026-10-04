import json,requests,gzip,os,sys
from concurrent.futures import ThreadPoolExecutor
os.makedirs('replays',exist_ok=True)
def dl(eid):
    p=f'replays/{eid}.json.gz'
    if os.path.exists(p): return eid,'cached'
    r=requests.get(f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json',timeout=90);r.raise_for_status()
    open(p,'wb').write(gzip.compress(r.content));return eid,len(r.content)
if __name__=='__main__':
    with ThreadPoolExecutor(4) as p:
        for x in p.map(dl,[int(a) for a in sys.argv[1:]]): print(x)
