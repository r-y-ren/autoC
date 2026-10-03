"""Retrospective development catalog; exclude heldout/final files and deduplicate cases."""
from pathlib import Path
from collections import defaultdict
import hashlib,json,statistics
D=Path(__file__).resolve().parent;R=D.parents[1]
BASE='b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4'
policies=defaultdict(dict);paths=defaultdict(set);sources=defaultdict(set);invalid=defaultdict(int);conflicts=set();files=0;rows=0
for path in (R/'research').rglob('*results*.jsonl'):
    relative=path.relative_to(R).as_posix()
    if any(w in relative.lower() for w in ('holdout','heldout','confirm','final')):continue
    files+=1
    with path.open(encoding='utf-8') as handle:
        for line in handle:
            try:r=json.loads(line)
            except (json.JSONDecodeError,UnicodeDecodeError):continue
            digest=r.get('candidate_sha256');opponent=r.get('opponent_sha256')
            if not digest or not opponent or 'candidate' not in r:continue
            paths[digest].add(r['candidate']);sources[digest].add(relative)
            if not r.get('valid') or 'margin' not in r:invalid[digest]+=1;continue
            key=(r['seed'],r['seat'],opponent,json.dumps(r.get('config'),sort_keys=True))
            value=(r['margin'],tuple(r['money']),float(r.get('max_seconds',0)),r.get('family','unknown'),r.get('panel','unknown'))
            if key in policies[digest] and policies[digest][key][1]!=value[1]:conflicts.add((digest,key))
            policies[digest][key]=value;rows+=1
refs=policies[BASE]
def points(v):return 1 if v[0]>0 else 0 if v[0]<0 else .5
summary=[]
for digest,records in policies.items():
    if digest==BASE:continue
    paired=[(k,v,refs[k]) for k,v in records.items() if k in refs and (digest,k) not in conflicts and (BASE,k) not in conflicts]
    external=[(k,v,b) for k,v,b in paired if k[2]!=BASE and v[4]!='direct_reference']
    if len(external)<48:continue
    direct=[(k,v,b) for k,v,b in paired if k[2]==BASE]
    row=dict(sha256=digest,paths=sorted(paths[digest]),sources=sorted(sources[digest]),invalid_rows=invalid[digest],paired_external=len(external),worlds=len({k[0] for k,v,b in external}),opponents=len({k[2] for k,v,b in external}),wins=sum(v[0]>0 for k,v,b in external),losses=sum(v[0]<0 for k,v,b in external),ties=sum(v[0]==0 for k,v,b in external),point_gain=sum(points(v)-points(b) for k,v,b in external),margin_gain=round(statistics.mean(v[0]-b[0] for k,v,b in external),2),direct_cases=len(direct),direct_wins=sum(v[0]>0 for k,v,b in direct),direct_losses=sum(v[0]<0 for k,v,b in direct))
    row['gain_rate']=row['point_gain']/len(external)
    summary.append(row)
summary.sort(key=lambda r:(-r['gain_rate'],-r['point_gain'],-r['margin_gain']))
report=dict(files=files,read_valid_rows=rows,baseline_contexts=len(refs),conflicting_contexts=len(conflicts),policies=len(policies),ranked=summary,scope='Retrospective development inventory, not a selection guarantee or rating estimate. Reserved final and heldout filenames excluded. Duplicate contexts counted once by hashes.')
(D/'candidate_catalog_20260929.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='ranked'}),flush=True)
for r in [x for x in summary if x['paired_external']>=96 and x['worlds']>=8 and x['opponents']>=4][:15]:
    print(json.dumps({k:v for k,v in r.items() if k!='sources'}),flush=True)
