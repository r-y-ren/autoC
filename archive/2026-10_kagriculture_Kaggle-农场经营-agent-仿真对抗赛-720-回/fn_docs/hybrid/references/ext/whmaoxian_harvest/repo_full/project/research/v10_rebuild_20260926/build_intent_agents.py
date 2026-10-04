"""Compile task intentions from public study traces, with reactive execution."""
from pathlib import Path
import base64,gzip,hashlib,json,zlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
DEST=OUT/'intent_agents';DEST.mkdir(exist_ok=True)
runtime=(OUT/'intent_runtime.py.txt').read_text(encoding='utf-8')
runtime=runtime.replace("elif not isinstance(tile,dict):skip=True", "elif tile is None:replacement=['BUILD_COOP' if cmd[1]=='GOOSE' else 'BUILD_PASTURE']\n            elif isinstance(tile,dict) and tile.get('kind')=='WEED':replacement=['DIG']")
compile(runtime,'intent_runtime.py','exec')
views=json.loads((OUT/'current_views.json').read_text(encoding='utf-8'))
views=[r for r in views if r['role']=='study' and r['submission'] not in {56555482,56551631,56531474,56494372}][:6]
records=[]
for view in views:
    game=json.loads(gzip.decompress((OUT/f"public_replays/{view['episode']}.json.gz").read_bytes()))
    seat=view['seat'];plan=[]
    for day in range(30):
        maximum=max(len(game['steps'][t][seat]['observation']['farms'][seat]['hands'])
                    for t in range(day*24,min(720,(day+1)*24)))
        tasks=[[] for _ in range(maximum+1)]
        for step in range(day*24,min(719,(day+1)*24)):
            obs=game['steps'][step][seat]['observation'];farm=obs['farms'][seat]
            positions=[farm['farmer']]+farm['hands'];action=game['steps'][step+1][seat]['action']
            commands=[action.get('farmer') or ['PASS']]+(action.get('hands') or [])
            for actor,cmd in enumerate(commands[:len(positions)]):
                if not cmd or cmd[0] in ('PASS','NORTH','SOUTH','EAST','WEST'):continue
                x,y=positions[actor];quadrant=1+(x>=5)+2*(y>=5)
                tasks[actor].append(dict(xy=[x,y],op=cmd,hour=step%24,quadrant=quadrant))
        for queue in tasks:
            for index,task in enumerate(queue):
                cmd=task['op']
                if cmd[0]!='PICKUP':continue
                item=cmd[1];needed=0
                for later in queue[index+1:]:
                    op=later['op']
                    if op[:2]==['PICKUP',item]:break
                    if item=='WHEAT' and op[0]=='FEED':needed+=1
                    elif item=='FERTILIZER' and op[0]=='FERTILIZE':needed+=1
                    elif op[:2]==['PLACE',item]:needed+=1
                task['op']=['PICKUP',item,needed or min(1,int(cmd[2]) if len(cmd)>2 else 1)]
        plan.append(dict(hands=maximum,tasks=tasks))
    blob=base64.b85encode(zlib.compress(json.dumps(plan,separators=(',',':')).encode(),9)).decode()
    code=runtime+'\nimport base64,json,zlib\n_PLAN=json.loads(zlib.decompress(base64.b85decode('+repr(blob)+')))\n'
    dest=DEST/f"teacher_{view['submission']}_{view['episode']}.py"
    dest.write_text(code,encoding='utf-8')
    records.append(dict(view,path=dest.relative_to(ROOT).as_posix(),seed=game['info']['seed'],
        sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),kind='local_intent_reconstruction_not_original_agent'))
(OUT/'intent_agents.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print('Reactive public-intent reconstructions',len(records),flush=True)
