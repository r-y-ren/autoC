"""Broader Kaggriculture development: actual programs, proxies and counters remain separate."""
from pathlib import Path
import hashlib,json
N=Path(__file__).resolve().parent;R=N.parents[1];W=R/'research/v10_rebuild_20260926';D=W/'continuation'
DEST=N/'combined_candidates';DEST.mkdir(exist_ok=True)
flow=(N/'flow_candidates_v2/reorder.py').read_bytes();tail=(N/'micro_opportunities_tail.txt').read_bytes()
assert tail.count(b'_U_PARENT=phase_b_agent')==1
tail=tail.replace(b'_U_PARENT=phase_b_agent',b'_U_PARENT=model_flow_agent')
combos=[]
for name,actions in [('care_reorder',('care','water','harvest','fertilizer')),('harvest_reorder',('harvest','care','water','fertilizer'))]:
    source=flow+f'\n_U_START=144\n_U_ACTIONS={actions!r}\n'.encode()+tail
    path=DEST/(name+'.py');path.write_bytes(source);compile(path.read_bytes(),str(path),'exec')
    combos.append(path.relative_to(R).as_posix())
candidates=['submissions/release_v10_r2/main.py',
    (N/'flow_candidates_v2/reorder.py').relative_to(R).as_posix(),
    *[(N/f'micro_candidates/{name}.py').relative_to(R).as_posix() for name in ('harvest','all_care_first','all_harvest_first')],*combos]
public=json.loads((D/'phase_b/validation_design.json').read_text())['public_roster']
roster=[dict(path=r['path'],family=r['name'],panel='public_program') for r in public]
roster += [dict(path=r['path'],family=r['family'],panel='responsive_proxy') for r in json.loads((N/'study_opponents.json').read_text()) if r['family'] in ('top_style_01','top_style_02','top_style_03','top_style_05')]
roster += [dict(path='submissions/release_v10_r2/main.py',family='r2',panel='direct_reference'),
    dict(path=(D/'generation5/advance36.py').relative_to(R).as_posix(),family='counter_advance36',panel='counter_population')]
seeds=[int.from_bytes(hashlib.sha256(f'top10-flow-development-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(8)]
jobs=[]
for candidate in candidates:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],
                    seed=seed,seat=seat,candidate_sha256=hashlib.sha256((R/candidate).read_bytes()).hexdigest(),
                    opponent_sha256=hashlib.sha256((R/opponent['path']).read_bytes()).hexdigest())
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
byid={j['id']:j for j in jobs};reused={}
for file in ('flow_screen_v2_results.jsonl','micro_screen_results.jsonl','proxy_characterization_results.jsonl'):
    for line in (N/file).read_text(encoding='utf-8').splitlines():
        row=json.loads(line);job=byid.get(row['id'])
        if job and row.get('valid') and all(row.get(k)==v for k,v in job.items()):reused[row['id']]=row
results=N/'extended_results.jsonl'
assert not results.exists(),'Refuse to overwrite an active/completed ledger'
results.write_text(''.join(json.dumps(r)+'\n' for r in reused.values()),encoding='utf-8')
(N/'extended_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
design=dict(candidates=candidates,roster=roster,seeds=seeds,jobs=len(jobs),reused=len(reused),fresh_required=len(jobs)-len(reused),
    source_hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in set(candidates+[r['path'] for r in roster])},
    scope='Development only. Cached exact jobs are not counted as freshly executed games. Final confirmation remains separate.')
(N/'extended_design.json').write_text(json.dumps(design,indent=2),encoding='utf-8')
print(json.dumps(dict(jobs=len(jobs),candidates=len(candidates),opponents=len(roster),reused=len(reused),fresh=len(jobs)-len(reused))),flush=True)
