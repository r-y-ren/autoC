"""Integrity and accounting receipt, not release authorization."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[1]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
expected={
 'main.py':'6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3',
 'submissions/release_v9/main.py':'6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3',
 'submissions/release_v10/main.py':'3a4601081cc909ae7baf97ec5ddb0e1a8a5a1a27c9cd072cdeaaf7d34c803e0b',
 'submissions/release_v10_r2/main.py':'b35b5b09fbec059ab7cbd2ba67a9fbb6d3e467ef5262f3e2ddba592b3e50c1c4',
 'submissions/release_v10_r2/submission.tar.gz':'25e4b6ed3f9e121e26d0b59c7a7625fb216a6210da0553809a3032913db92e9a'}
for path,digest in expected.items():assert sha(R/path)==digest,path
batches={}
for name in ('g1','g2'):
    jobs=json.loads((D/(name+'_jobs.json')).read_text());rows=[json.loads(s) for s in (D/(name+'_results.jsonl')).read_text().splitlines()]
    target={j['id']:j for j in jobs};assert len(target)==len(jobs)
    assert len(rows)==len(jobs) and len({r['id'] for r in rows})==len(rows)
    for row in rows:
        assert all(row.get(k)==v for k,v in target[row['id']].items())
        assert row.get('cash_identity_checked'),row['id']
    source_hashes={(j[k],j[k+'_sha256']) for j in jobs for k in ('candidate','opponent')}
    for path,digest in source_hashes:assert sha(R/path)==digest,path
    batches[name]=dict(jobs=len(jobs),records=len(rows),valid=sum(bool(r.get('valid')) for r in rows),invalid=sum(not r.get('valid') for r in rows),worlds=len({r['seed'] for r in rows}),ledger_sha256=sha(D/(name+'_results.jsonl')),cash_identity_checks=len(rows)*2)
worlds=json.loads((D/'worlds.json').read_text());assert not set(worlds['confirmation'])&set(worlds['g1']+worlds['g2'])
receipt=dict(captured_utc=datetime.now(timezone.utc).isoformat(),batches=batches,
    fresh_match_total=sum(b['records'] for b in batches.values()),
    valid_match_total=sum(b['valid'] for b in batches.values()),
    invalid_match_total=sum(b['invalid'] for b in batches.values()),
    smoke_included_in_g1=True,original_hashes=expected,original_files_unchanged=True,
    g1_population=24,g2_new_offspring=8,confirmation_worlds_reserved=len(worlds['confirmation']),
    confirmation_run=False,new_release=False,online_submission=False,
    score_target=2800,score_target_verified=False,
    limitations=['Public-program, reconstructed-proxy and evolved-parent panels must remain separate.',
     'Physical cash identities do not make a run with agent diagnostics valid.',
     'Independent ranch and full-route-search branches are incomplete after platform write denials.'])
(D/'integrity_receipt.json').write_text(json.dumps(receipt,indent=2))
print(json.dumps(receipt),flush=True)
