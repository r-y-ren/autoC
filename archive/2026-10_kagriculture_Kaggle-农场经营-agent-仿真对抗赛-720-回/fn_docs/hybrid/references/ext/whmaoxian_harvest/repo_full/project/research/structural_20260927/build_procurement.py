"""Standalone production plus observed-inventory procurement experiments."""
from pathlib import Path
import base64,gzip,hashlib,json,zlib
P=Path(__file__).resolve().parent;R=P.parents[1];T=R/'research/v10_top10_20260926'
plans=json.loads((P/'plan_manifest.json').read_text())
records=json.loads((T/'demonstrations_index.json').read_text())
lookup={(r['episode'],r['seat']):r for r in records}
tail=(P/'procurement_tail.txt').read_bytes();out=P/'procurement';out.mkdir(exist_ok=True)
variants=[]
for plan in [p for p in plans if p['mode']=='physical']:
    record=lookup[(plan['source_episode'],plan['source_seat'])]
    demo=json.loads(gzip.decompress((R/record['path']).read_bytes()))
    game=json.loads(gzip.decompress((T/f"study_replays/{record['episode']}.json.gz").read_bytes()))
    needs=[{} for _ in range(719)]
    for day,daily in enumerate(demo['plans']):
        for tasks in daily['tasks']:
            for task in tasks:
                cmd=task['op'];t=day*24+int(task['hour'])
                if t<719 and len(cmd)>=3 and cmd[0]=='PICKUP' and cmd[1] in ('WHEAT','FERTILIZER'):
                    needs[t][cmd[1]]=needs[t].get(cmd[1],0)+max(0,int(cmd[2]))
    hints={'capital':[a.get('market',[]) for a in demo['actions']], 'needs':needs,
           'workers':[len(s[record['seat']]['observation']['farms'][record['seat']]['hands']) for s in game['steps'][1:]]}
    encoded=base64.b85encode(zlib.compress(json.dumps(hints,separators=(',',':')).encode(),9)).decode()
    base=(R/plan['path']).read_bytes();assert hashlib.sha256(base).hexdigest()==plan['sha256']
    for start,look in ((0,4),(144,12)):
        payload='\n_PB_HINTS=json.loads(zlib.decompress(base64.b85decode('+repr(encoded)+')))\n'
        payload+='_PB_CAPITAL=_PB_HINTS["capital"]\n_PB_NEEDS=_PB_HINTS["needs"]\n_PB_WORKERS=_PB_HINTS["workers"]\n'
        payload+=f'_PB_FROM={start}\n_PB_LOOK={look}\n'
        data=base+payload.encode()+tail;path=out/f'plan{plan["plan"]:02d}_from{start}.py'
        compile(data,str(path),'exec')
