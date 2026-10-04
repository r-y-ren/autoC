"""Expected-margin alternatives, evaluated separately from forecast-only gates."""
from pathlib import Path
import hashlib,json
N=Path(__file__).resolve().parent;R=N.parents[1];DEST=N/'flow_ev';DEST.mkdir(exist_ok=True)
base=(N/'flow_candidates_v2/replace20.py').read_bytes().decode('utf-8')
configurations=[('margin2p60',2,.6,True),('margin10p60',10,.6,True),
    ('margin2p85',2,.85,True),('margin10p85',10,.85,True),
    ('all_margin2p60',2,.6,False),('all_margin10p85',10,.85,False)]
design=json.loads((N/'flow_screen_v2_design.json').read_text());manifest=[];jobs=[]
for name,gain,probability,keep in configurations:
    source=base+f'\n_EV_MIN_GAIN={gain}\n_EV_PROB_SCALE={probability}\n_EV_KEEP_BASE={keep!r}\n_EV_LOOK=12\n'
    source+=(N/'flow_ev_tail.txt').read_text(encoding='utf-8')
    path=DEST/(name+'.py');path.write_bytes(source.encode('utf-8'));compile(path.read_bytes(),str(path),'exec')
    candidate=path.relative_to(R).as_posix();digest=hashlib.sha256(path.read_bytes()).hexdigest()
    manifest.append(dict(name=name,path=candidate,sha256=digest,gain=gain,probability_scale=probability,keep_native=keep))
    for opponent in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                job=dict(candidate=candidate,opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],
                    seed=seed,seat=seat,candidate_sha256=digest,opponent_sha256=hashlib.sha256((R/opponent['path']).read_bytes()).hexdigest())
                job['id']=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()[:24];jobs.append(job)
(N/'flow_ev_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(N/'flow_ev_jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print(json.dumps(dict(candidates=len(manifest),jobs=len(jobs))),flush=True)
