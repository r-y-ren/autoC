"""Use only successfully executed public intents and remove unpayable cash reserves."""
from pathlib import Path
import base64,hashlib,json,zlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
DEST=OUT/'intent_agents_v3';DEST.mkdir(exist_ok=True)
v2=json.loads((OUT/'intent_agents_v2.json').read_text(encoding='utf-8'))
records=json.loads((OUT/'effective_intents.json').read_text(encoding='utf-8'))
new=[]
for row in records:
    prototype=next(r for r in v2 if r['episode']==row['episode'] and r['seat']==row['seat'])
    text=(ROOT/prototype['path']).read_text(encoding='utf-8')
    assert text.count('\n_PLAN=')==1
    text=text[:text.index('\n_PLAN=')]
    text=text.replace('if cash<cost+50:break','if cash<cost:break')
    text=text.replace('if cash>=cost+100:orders.append','if cash>=cost+20:orders.append')
    blob=base64.b85encode(zlib.compress(json.dumps(row['plans'],separators=(',',':')).encode(),9)).decode()
    text+='\n_PLAN=json.loads(zlib.decompress(base64.b85decode('+repr(blob)+')))\n'
    path=DEST/Path(prototype['path']).name;path.write_text(text,encoding='utf-8');compile(text,str(path),'exec')
    new.append(dict(prototype,path=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
(OUT/'intent_agents_v3.json').write_text(json.dumps(new,indent=2),encoding='utf-8')
print('Executed-intent prototypes',len(new),flush=True)
