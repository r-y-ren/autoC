"""Supervised targets are historical trades; features use only contemporaneous public data."""
from pathlib import Path
import gzip,hashlib,json
import numpy as np
import flow_features as flow
N=Path(__file__).resolve().parent
split=json.loads((N/'replay_split.json').read_text(encoding='utf-8'))
X=[];Y=[];episodes=[];teams=[];steps=[];receipts=[]
team_index={name:i for i,name in enumerate(sorted({r['team'] for r in split['study']}))}
for episode in sorted({row['episode'] for row in split['study']}):
    raw=gzip.decompress((N/f'study_replays/{episode}.json.gz').read_bytes());game=json.loads(raw)
    assert game['info']['EpisodeId']==episode and len(game['steps'])==720
    for view in [row for row in split['study'] if row['episode']==episode]:
        target=view['seat'];owner=1-target;flow.FLOW_STATE.clear();feature_rows=[];volumes=[]
        for step in range(719):
            obs=dict(game['steps'][step][owner]['observation']);obs['step']=step
            target_obs=dict(game['steps'][step][target]['observation']);target_obs['step']=step
            features=flow.flow_observe(obs)
            flow.flow_commit(obs,game['steps'][step+1][owner]['action'])
            # The target's private view is used only to compute the supervised label.
            sales=flow.flow_sales(target_obs,game['steps'][step+1][target]['action'])
            feature_rows.append([features[item] for item in flow.FLOW_ITEMS])
            volumes.append([sales[item] for item in flow.FLOW_ITEMS])
        quantity=np.asarray(volumes,dtype=np.float32)
        for step in range(144,717):
            soon=quantity[step:step+3].sum(axis=0)
            for item in range(len(flow.FLOW_ITEMS)):
                X.append(feature_rows[step][item]);Y.append([float(quantity[step,item]>0),float(soon[item]>0),min(50,float(soon[item]))/20.0])
                episodes.append(episode);teams.append(team_index[view['team']]);steps.append(step)
    receipts.append(dict(episode=episode,sha256=hashlib.sha256(raw).hexdigest()))
    print(json.dumps(dict(episode=episode,samples=len(X))),flush=True)
arrays=dict(X=np.asarray(X,dtype=np.float32),Y=np.asarray(Y,dtype=np.float32),
    episode=np.asarray(episodes,dtype=np.int64),team=np.asarray(teams,dtype=np.int16),step=np.asarray(steps,dtype=np.int16))
assert arrays['X'].shape[1]==31 and np.isfinite(arrays['X']).all()
np.savez_compressed(N/'flow_dataset.npz',**arrays)
manifest=dict(samples=len(X),features=31,feature_source_sha256=hashlib.sha256((N/'flow_features.py').read_bytes()).hexdigest(),
    dataset_sha256=hashlib.sha256((N/'flow_dataset.npz').read_bytes()).hexdigest(),
    labels=['sell_this_turn','sell_within_three_turns','capped_three_turn_volume_div20'],
    target_rate=arrays['Y'].mean(axis=0).tolist(),source_replays=receipts,team_metadata=team_index,
    no_opponent_private_features=True,heldout_replays_used=False,
    metadata_not_model_inputs=['episode','team'],scope='Supervised study data; not match-strength evidence.')
(N/'flow_dataset_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(dict(samples=len(X),label_means=manifest['target_rate'])),flush=True)
