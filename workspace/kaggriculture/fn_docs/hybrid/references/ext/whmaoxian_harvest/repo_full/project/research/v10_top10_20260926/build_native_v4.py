"""New local task-executor candidates; immutable previous sources are inputs only."""
from pathlib import Path
import base64,copy,gzip,hashlib,json,zlib
N=Path(__file__).resolve().parent;R=N.parents[1];W=R/'research/v10_rebuild_20260926'
DEST=N/'native_v4';DEST.mkdir(exist_ok=True)
records=json.loads((W/'effective_intents.json').read_text(encoding='utf-8'))
old=json.loads((W/'intent_agents_v3.json').read_text(encoding='utf-8'));outputs=[]
for row in records:
    prototype=next(p for p in old if p['episode']==row['episode'] and p['seat']==row['seat'])
    raw=(R/prototype['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==prototype['sha256']
    text=raw.decode('utf-8');text=text[:text.index('\n_PLAN=')]
    a=text.index("        if op=='PICKUP':");b=text.index("        elif op=='PLANT':",a)
    fixed=text[:a]+(N/'pickup_fix.txt').read_text(encoding='utf-8')+text[b:]
    game=json.loads(gzip.decompress((W/f"public_replays/{row['episode']}.json.gz").read_bytes()))
    plans=copy.deepcopy(row['plans']);seat=row['seat']
    for day in plans:day['hire_hours']=[]
    for t in range(1,len(game['steps'])):
        if t%24==0:continue
        count=len(game['steps'][t][seat]['observation']['farms'][seat]['hands'])
        hours=plans[(t-1)//24]['hire_hours']
        hours.extend([(t-1)%24]*max(0,count-len(hours)))
    for label,look in [('pickup',None),('hire0',0),('hire1',1)]:
        source=fixed
        if look is not None:
            source=source.replace("_market(observation,commands,needs,daily['hands'])",f"_market(observation,commands,needs,sum(h <= step%24+{look} for h in daily['hire_hours']))")
        blob=base64.b85encode(zlib.compress(json.dumps(plans,separators=(',',':')).encode(),9)).decode()
        source+='\n_PLAN=json.loads(zlib.decompress(base64.b85decode('+repr(blob)+')))\n'
        destination=DEST/f"{row['episode']}_{seat}_{label}.py"
        compile(source,str(destination),'exec')
        destination.write_text(source,encoding='utf-8')
        outputs.append(dict(name=destination.stem,path=destination.relative_to(R).as_posix(),
            source_sha256=hashlib.sha256(destination.read_bytes()).hexdigest(),
            teacher_episode=row['episode'],teacher_seat=seat,variant=label))
(N/'native_v4_manifest.json').write_text(json.dumps(outputs,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(outputs))),flush=True)
