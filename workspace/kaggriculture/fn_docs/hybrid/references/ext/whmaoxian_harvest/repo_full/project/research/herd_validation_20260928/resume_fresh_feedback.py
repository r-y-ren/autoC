"""Resume the already selected public feedback sample without resampling it."""
from pathlib import Path
import gzip,hashlib,json,requests,time
D=Path(__file__).resolve().parent;O=D/'fresh_feedback'
selection=json.loads((O/'selection.json').read_text(encoding='utf-8'))
receipts=[]
for view in selection['views']:
    path=O/f"{view['episode']}.json.gz";url=f"https://www.kaggle.com/competitions/episodes/{view['episode']}/replay.json"
    try:
        if path.exists():raw=gzip.decompress(path.read_bytes())
        else:
            error=None
            for attempt in range(2):
                try:
                    response=requests.get(url,timeout=(10,30));response.raise_for_status();raw=response.content;error=None;break
                except requests.RequestException as exc:
                    error=exc
                    if attempt==0:time.sleep(1)
            if error is not None:raise error
        game=json.loads(raw)
        assert len(game['steps'])==720 and game['info']['EpisodeId']==view['episode']
        if not path.exists():path.write_bytes(gzip.compress(raw))
        row=dict(episode=view['episode'],url=url,sha256=hashlib.sha256(raw).hexdigest(),seed=game['info']['seed'],rewards=game['rewards'])
    except Exception as exc:row=dict(episode=view['episode'],url=url,error=str(exc))
    receipts.append(row);(O/'resume_receipts.json').write_text(json.dumps(receipts,indent=2),encoding='utf-8')
    print(json.dumps(dict(episode=view['episode'],ok='error' not in row)),flush=True)
print(json.dumps(dict(selected=len(selection['views']),available=sum('error' not in r for r in receipts))),flush=True)
