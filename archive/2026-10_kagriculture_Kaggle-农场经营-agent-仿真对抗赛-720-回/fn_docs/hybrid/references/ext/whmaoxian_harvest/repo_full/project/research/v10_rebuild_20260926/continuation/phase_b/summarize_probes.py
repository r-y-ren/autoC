"""Report post-freeze replay diagnostics and known residual limitations."""
from pathlib import Path
import hashlib,json,sys
B=Path(__file__).resolve().parent;D=B.parent;W=D.parent;R=W.parents[1]
sys.path.insert(0,str(D));from assess import load,desc
selection=json.loads((B/'selection.json').read_text());candidate=selection['candidate']
rows=load(B/'replay_recheck_results.jsonl');assert len(rows)==78 and all(r.get('valid') for r in rows)
assert all(r['candidate_sha256']==selection['sha256'] for r in rows if r['candidate']==candidate)
summary={name:{panel:desc([r for r in rows if r['candidate']==name and r['panel']==panel])
 for panel in ('known_loss_recheck','current_ladder_fixed_replay')}
 for name in (candidate,'submissions/release_v9/main.py','submissions/release_v10/main.py')}
baseline=[r for r in rows if r['candidate']=='submissions/release_v10/main.py' and r['panel']=='known_loss_recheck']
matched=[r['money']==[r['recorded_rewards'][r['seat']],r['recorded_rewards'][1-r['seat']]] for r in baseline]
assert len(matched)==11 and all(matched)
validation=load(B/'validation_results.jsonl')
residual=[{k:r[k] for k in ('seed','seat','family','panel','margin','final_inventory','final_carried')}
 for r in validation if r['candidate']==candidate and (r.get('final_carried') or any(r.get('final_inventory',{}).values()))]
result=dict(source_sha256=selection['sha256'],summary=summary,
 known_loss_original_v10_reproduced_exactly=11,known_largest_loss_episode=113488570,
 largest_loss_cases=[r for r in rows if r['episode']==113488570],residual_cases=residual,
 limitations=['Fixed replay opponents cannot react to the changed game. These outcomes do not prove wins against their private agents.',
 'The candidate improves six of eleven historical loss traces but not all.',
 'The fifteen recent ladder-trace win count falls from old V10 thirteen to candidate eleven; this regression is retained, not hidden.',
 'Three validation cases in one world and seat retain one unplaced cow; these cases were retained in the final statistics.',
 'Most primary win-point improvement is concentrated in the previously fragile Aurax matchup.',
 'The separate reference-style panel is 144/144 for all three versions and is a robustness check, not improvement evidence.'])
(B/'known_limitations.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'known_loss_baseline_exact':11,'residual_cases':len(residual),'diagnostic_games':78}),flush=True)
