"""Build clearly labelled public-action probes, not private opponent programs."""
from pathlib import Path
import base64, gzip, hashlib, json, zlib
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
PROBES=OUT/'probes'; PROBES.mkdir(exist_ok=True)
views=json.loads((OUT/'current_views.json').read_text(encoding='utf-8'))
losses=json.loads((OUT/'v10_public_summary_rows.json').read_text(encoding='utf-8'))
views += [dict(episode=r['episode'],seat=1-r['seat'],submission=r['opponent_submission'],
    team=str(r['opponent_team']),rating=r['opponent_score'],role='actual_v10_loss')
    for r in losses if r['margin']<0]
roster=[]
for view in views:
    game=json.loads(gzip.decompress((OUT/f"public_replays/{view['episode']}.json.gz").read_bytes()))
    actions=[s[view['seat']]['action'] for s in game['steps'][1:]]
    assert len(actions)==719
    blob=base64.b85encode(zlib.compress(json.dumps(actions,separators=(',',':')).encode(),9)).decode()
    code=f'''# Public action trace {view['episode']}, player {view['seat']}; static diagnostic only.
# This is not the original opponent's private agent and has no reactive planning.
import base64,copy,json,zlib
_ACTIONS=json.loads(zlib.decompress(base64.b85decode({blob!r})))
def agent(observation,configuration=None):
    return copy.deepcopy(_ACTIONS[min(718,max(0,int(observation['step'])))])
'''
    dest=PROBES/f"trace_{view['episode']}_{view['seat']}.py"
    dest.write_text(code,encoding='utf-8')
    roster.append(dict(view,path=dest.relative_to(ROOT).as_posix(),seed=game['info']['seed'],
        rewards=game['rewards'],sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
(OUT/'probe_roster.json').write_text(json.dumps(roster,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared',len(roster),'labelled probes',flush=True)
