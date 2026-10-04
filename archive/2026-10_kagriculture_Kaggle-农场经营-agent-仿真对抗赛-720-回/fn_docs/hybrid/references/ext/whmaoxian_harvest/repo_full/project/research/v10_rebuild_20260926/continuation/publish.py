"""Publish a new immutable V10-R2 directory only after all frozen checks pass."""
from pathlib import Path
import datetime,hashlib,json,shutil,tarfile
import gate
D=Path(__file__).resolve().parent; R=D.parents[2]
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
 selection=read(D/'selection.json'); expected=selection['sha256']
 strength=gate.check(); assert strength['passed'],strength['reasons']
 stage=R/'submissions/candidate_v10_r2'
 technical=read(stage/'validation.json')
 assert technical['technical_acceptance_passed'] and technical['source_sha256']==expected
 official=read(D/'official_crosscheck.json')
 assert official['complete'] and official['all_passed']
 assert sha(stage/'main.py')==expected==sha(R/selection['candidate'])
 assert sha(stage/'submission.tar.gz')==technical['archive_sha256']
 with tarfile.open(stage/'submission.tar.gz','r:gz') as archive:
  assert set(archive.getnames())=={'main.py','NOTICE.txt','LICENSE.txt'}
  for name in archive.getnames():assert archive.extractfile(name).read()==(stage/name).read_bytes()
 originals={'main.py':'6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3',
  'submissions/release_v9/main.py':'6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3',
  'submissions/release_v10/main.py':'3a4601081cc909ae7baf97ec5ddb0e1a8a5a1a27c9cd072cdeaaf7d34c803e0b'}
 for name,digest in originals.items():assert sha(R/name)==digest,name
 dest=R/'submissions/release_v10_r2'
 assert not dest.exists(),'Refusing to overwrite any prior release'
 dest.mkdir()
 for name in ('main.py','submission.tar.gz','NOTICE.txt','LICENSE.txt','validation.json'):
  shutil.copy2(stage/name,dest/name)
 development={}
 for folder,names in [(D.parent,['opening','new_public','generation2','combination','additional_development']),
                      (D,['generation4','extended_dev','generation5'])]:
  for name in names:
   ledger=folder/(name+'_results.jsonl'); rows=[json.loads(x) for x in ledger.read_text(encoding='utf-8').splitlines()]
   development[name]=dict(games=len(rows),invalid=sum(not r.get('valid') for r in rows),
    path=ledger.relative_to(R).as_posix(),sha256=sha(ledger))
 design=read(D/'confirmation_design.json')
 assert design['protocol_sha256']==sha(D/'CONFIRMATION_PROTOCOL.md')
 manifest=dict(version='V10-R2',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  candidate=selection['candidate'],source_sha256=expected,archive_sha256=sha(dest/'submission.tar.gz'),
  archive_bytes=(dest/'submission.tar.gz').stat().st_size(),online_submission=False,online_rating=None,
  original_sources_preserved=originals,development=development,
  confirmation= strength,confirmation_design=design,official_crosscheck=official,
  technical_report='validation.json',
  confirmation_ledger=dict(path=(D/'confirmation_results.jsonl').relative_to(R).as_posix(),sha256=sha(D/'confirmation_results.jsonl')),
  full_development_executions=sum(x['games'] for x in development.values()),
  confirmation_full_executions=1920,prefix_checks_not_counted_as_full_games=799,
  caveats=['Fixed public implementations can share ancestry.','No static replay wins are rating evidence.',
           'The fast screening runner calls official transitions; actual file-path loading was cross-checked separately.',
           '2800 is a target, not a measured rating or calibrated probability.'])
 (dest/'evidence.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
 (D/'confirmation_gate.json').write_text(json.dumps(strength,indent=2),encoding='utf-8')
 shutil.copy2(D/'selection.json',dest/'selection.json')
 shutil.copy2(D/'CONFIRMATION_PROTOCOL.md',dest/'CONFIRMATION_PROTOCOL.md')
 print(json.dumps(dict(release=str(dest),source_sha256=expected,archive_sha256=manifest['archive_sha256'],
  strength_passed=True,technical_passed=True,online_submission=False)),flush=True)
if __name__=='__main__':main()
