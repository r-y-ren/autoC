"""A matched complete-game development screen, with proxy and actual programs separate."""
from pathlib import Path
import hashlib,json
N=Path(__file__).resolve().parent;R=N.parents[1];W=R/'research/v10_rebuild_20260926';D=W/'continuation'
candidates=json.loads((N/'flow_candidates_manifest.json').read_text())
candidates.append(dict(name='r2',path='submissions/release_v10_r2/main.py'))
public=json.loads((D/'phase_b/validation_design.json').read_text())['public_roster']
proxies=json.loads((N/'study_opponents.json').read_text())
roster=[dict(path=r['path'],family=r['name'],panel='public_program') for r in public if r['name'] in ('fieldcraft','marketshock','aurax','structured')]
roster += [dict(path=r['path'],family=r['family'],panel='responsive_proxy') for r in proxies if r['family'] in ('top_style_02','top_style_03')]
roster += [dict(path='submissions/release_v10_r2/main.py',family='r2',panel='direct_reference'),
    dict(path=(D/'generation5/advance36.py').relative_to(R).as_posix(),family='counter_advance36',panel='counter_population')]
seeds=[int.from_bytes(hashlib.sha256(f'top10-flow-development-{i}'.encode()).digest()[:4],'big')%2000000000 for i in range(2)]
jobs=[]
for candidate in candidates:
    for opponent in roster:
        for seed in seeds:
            for seat in (0,1):
                job=dict(candidate=candidate['path'],opponent=opponent['path'],family=opponent['family'],
                    panel=opponent['panel'],seed=seed,seat=seat,
                    candidate_sha256=hashlib.sha256((R/candidate['path']).read_bytes()).hexdigest(),
                    opponent_sha256=hashlib.sha256((R/opponent['path']).read_bytes()).hexdigest())
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(N/'flow_screen_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
(N/'flow_screen_design.json').write_text(json.dumps(dict(candidates=candidates,roster=roster,seeds=seeds,total_jobs=len(jobs)),indent=2),encoding='utf-8')
print(json.dumps(dict(jobs=len(jobs),candidates=len(candidates),opponents=len(roster))),flush=True)
