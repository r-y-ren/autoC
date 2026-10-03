"""Add a separately reported contemporary-style stress panel, not a rating test."""
from pathlib import Path
import hashlib,json
S=Path(__file__).resolve().parent;R=S.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
prior=json.loads((S/'extended_design.json').read_text());proxies=json.loads((S/'recent_proxy_manifest.json').read_text())['variants']
variants=[v for v in prior['variants'] if v['name'] in ('r2','yarn_nomilk')]
jobs=[]
for v in variants:
    for op in proxies:
        seeds=[op['seed']]+prior['seeds'][:2]
        assert len(set(seeds))==len(seeds)
        for seed in seeds:
            for seat in (0,1):
                j=dict(candidate=v['path'],opponent=op['path'],family=op['family'],panel=op['panel'],seed=seed,seat=seat,candidate_sha256=v['sha256'],opponent_sha256=op['sha256'])
                j['id']=sha(json.dumps(j,sort_keys=True).encode())[:24];jobs.append(j)
report=dict(variants=variants,roster=proxies,uniform_worlds=prior['seeds'][:2],cases=len(jobs),
            scope='One original demonstration seed plus two predeclared development seeds per proxy, both seats. Results against responsive reconstructions do not identify actual leaderboard strength.')
for suffix,data in [('jobs',jobs),('design',report)]:
    p=S/f'recent_panel_{suffix}.json';text=json.dumps(data,indent=2)
    if p.exists():assert p.read_text()==text
    else:p.write_text(text)
print(json.dumps(dict(cases=len(jobs),proxies=len(proxies))),flush=True)
