"""Final byte-level delivery receipt. Does not run games or submit online."""
from pathlib import Path
import hashlib,json,tarfile
C=Path(__file__).resolve().parent;D=C.parent;W=D.parent;R=W.parents[1]
release=R/'submissions/release_v10_r2'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
e=json.loads((release/'evidence.json').read_text(encoding='utf-8'))
summary=json.loads((release/'delivery_summary.json').read_text(encoding='utf-8'))
assert e['strength']['passed'] and e['technical']['technical_acceptance_passed']
assert summary['total_counted_full_games']==15151
assert e['counted_full_games']==15151
assert sha(release/'main.py')==e['source_sha256']==e['selection']['sha256']
assert sha(release/'submission.tar.gz')==e['archive_sha256']
assert (release/'submission.tar.gz').stat().st_size==651310
with tarfile.open(release/'submission.tar.gz','r:gz') as archive:
    members=archive.getnames();assert set(members)=={'main.py','NOTICE.txt','LICENSE.txt'}
    for name in members:
        assert archive.extractfile(name).read()==(release/name).read_bytes()
for name,digest in e['original_files_unchanged'].items():
    assert sha(R/name)==digest,name
for name,count in (('development',1744),('risk',976),('fresh_loss',27)):
    rows=[json.loads(line) for line in (C/f'{name}_results.jsonl').read_text(encoding='utf-8').splitlines()]
    assert len(rows)==count and all(r.get('valid') for r in rows)
assert all((release/name).is_file() for name in ('README.md','known_limitations.json','study_decision.json'))
receipt=dict(archive=str(release/'submission.tar.gz'),archive_bytes=651310,members=members,
 source_sha256=e['source_sha256'],archive_sha256=e['archive_sha256'],original_files_unchanged=True,
 total_counted_full_games=15151,final_validation_full_games=2352,online_submission=False,online_rating=None)
(release/'final_receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(receipt),flush=True)
