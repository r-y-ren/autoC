"""Repair task prerequisites in a new prototype; retain failed v1 unmodified."""
from pathlib import Path
import ast,hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
DEST=OUT/'intent_agents_v2';DEST.mkdir(exist_ok=True)
records=json.loads((OUT/'intent_agents.json').read_text(encoding='utf-8'))
new=[]
for row in records:
    text=(ROOT/row['path']).read_text(encoding='utf-8')
    marker="        skip=False;replacement=None\n"
    replacement=marker+"        if hour<task['hour']:\n            return _walk(pos,target) or ['PASS']\n"
    assert text.count(marker)==1;text=text.replace(marker,replacement)
    marker="    orders=_market(observation,commands,needs,daily['hands'])"
    prefix="""    # Prefund imminent seed tasks rather than waiting at an empty field.
    seed_need={}
    for queue in tasks:
        for task in queue:
            c=task['op']
            if c[0]=='PLANT' and step%24<=task['hour']<=step%24+3:
                seed_need[c[1]]=seed_need.get(c[1],0)+1
    for crop,q in seed_need.items():
        needs['seed:'+crop]=max(needs.get('seed:'+crop,0),q-seeds.get(crop,0))
"""
    assert text.count(marker)==1;text=text.replace(marker,prefix+marker)
    path=DEST/Path(row['path']).name;path.write_text(text,encoding='utf-8');compile(text,str(path),'exec')
    new.append(dict(row,path=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
(OUT/'intent_agents_v2.json').write_text(json.dumps(new,indent=2),encoding='utf-8')
print('New prerequisite-aware prototypes',len(new),flush=True)
