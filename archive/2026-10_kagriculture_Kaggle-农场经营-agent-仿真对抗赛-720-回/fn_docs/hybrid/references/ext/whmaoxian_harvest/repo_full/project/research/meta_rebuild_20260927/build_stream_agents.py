"""Separate ledger correction from current-meta stream forecasting."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
raw=(R/'submissions/release_v10_r2/main.py').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
streams=json.loads((D/'recent_streams.json').read_text())['streams'];variants=[]
settings=[('sync_only',True,False,6,.5),('stream6',True,True,6,.5),('stream12',True,True,12,.65),('stream6_native_book',False,True,6,.5)]
for name,sync,library,minimum,precision in settings:
    constants=f'\n_MS_SYNC={sync}\n_MS_MIN_MATCH={minimum}\n_MS_PRECISION={precision}\n_MS_STREAMS={streams if library else []!r}\n'
    source=raw+constants.encode()+(D/'stream_tail.txt').read_bytes()
    path=D/f'candidates/{name}.py';compile(source,str(path),'exec')
    assert not path.exists();path.write_bytes(source)
    variants.append(dict(name=name,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(source).hexdigest(),sync=sync,library=library,minimum=minimum,precision=precision))
(D/'stream_candidates.json').write_text(json.dumps(variants,indent=2))
design=json.loads((D/'value_extended_design.json').read_text());jobs=[]
for v in variants:
    for opponent in design['roster']:
        for seed in design['seeds']:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=opponent['path'],family=opponent['family'],panel=opponent['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=hashlib.sha256((R/opponent['path']).read_bytes()).hexdigest())
                j['id']=hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()[:24];jobs.append(j)
(D/'stream_jobs.json').write_text(json.dumps(jobs,indent=2))
(D/'stream_design.json').write_text(json.dumps(dict(variants=variants,seeds=design['seeds'],roster=design['roster'],jobs=len(jobs),control_ledger='value_extended_results.jsonl',scope='Development and mechanism ablations; not independent rating evidence.'),indent=2))
print(json.dumps(dict(variants=len(variants),new_games=len(jobs),streams=len(streams))),flush=True)
