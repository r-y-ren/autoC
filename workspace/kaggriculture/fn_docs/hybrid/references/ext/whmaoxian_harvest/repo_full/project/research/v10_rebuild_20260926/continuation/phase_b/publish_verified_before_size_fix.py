"""Create a new release only after Phase-B strength and archive checks pass."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,tarfile,tempfile
from validate_gate import check
B=Path(__file__).resolve().parent;D=B.parent;W=D.parent;R=W.parents[1]
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
 gate=check();assert gate['passed'],gate['reasons']
 selection=read(B/'selection.json');expected=selection['sha256']
 stage=R/'submissions/candidate_v10_r2b';technical=read(stage/'validation.json')
 official=read(B/'official_crosscheck.json')
 assert technical['technical_acceptance_passed'] and technical['source_sha256']==expected
 assert official['complete'] and official['all_passed'] and official['candidate_sha256']==expected
 assert sha(stage/'main.py')==expected==sha(R/selection['candidate'])
 assert sha(stage/'submission.tar.gz')==technical['archive_sha256']
 with tarfile.open(stage/'submission.tar.gz','r:gz') as archive:
  assert set(archive.getnames())=={'main.py','NOTICE.txt','LICENSE.txt'}
  for name in archive.getnames():assert archive.extractfile(name).read()==(stage/name).read_bytes()
 originals={'main.py':'6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3',
  'submissions/release_v9/main.py':'6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3',
  'submissions/release_v10/main.py':'3a4601081cc909ae7baf97ec5ddb0e1a8a5a1a27c9cd072cdeaaf7d34c803e0b'}
 for name,digest in originals.items():assert sha(R/name)==digest,name
 destination=R/'submissions/release_v10_r2';assert not destination.exists()
 development={}
 for folder,names in [(W,['opening','new_public','generation2','combination','additional_development']),
                      (D,['generation4','extended_dev','generation5','generation6','demand_dev','generation7','generation7_direct'])]:
  for name in names:
   path=folder/(name+'_results.jsonl');rows=[json.loads(s) for s in path.read_text(encoding='utf-8').splitlines()]
   development[name]=dict(games=len(rows),invalid=sum(not r.get('valid') for r in rows),path=path.relative_to(R).as_posix(),sha256=sha(path))
 a_confirm=[json.loads(s) for s in (D/'confirmation_results.jsonl').read_text().splitlines()]
 a_style=[json.loads(s) for s in (D/'style_stress_results.jsonl').read_text().splitlines()]
 assert len(a_confirm)==1920 and len(a_style)==432
 assert all(r.get('valid') for r in a_confirm+a_style)
 assert all(value['invalid']==0 for value in development.values())
 evidence=dict(version='V10-R2',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  source_sha256=expected,archive_sha256=sha(stage/'submission.tar.gz'),
  archive_bytes=(stage/'submission.tar.gz').stat().st_size(),selection=selection,
  strength=gate,technical=technical,official_crosscheck=official,development=development,
  rejected_phase_a_gate=read(D/'confirmation_gate.json'),
  entrypoint_repair_receipt=read(D/'confirmation_entry_repair_receipt.json'),
  original_files_unchanged=originals,online_submission=False,online_rating=None,
  counted_full_games=sum(x['games'] for x in development.values())+1920+432+2352,
  count_scope='Completed development and independent-validation ledgers, including rejected candidates and controls. Technical replays and prefix-only runs are separate. 288 failed loader attempts excluded.',
  environment='kaggle-environments==1.32.7',
  caveats=['Public implementations may share production plans or code ancestry.',
   'New validation worlds were unused in development. Style outcomes were unused for source selection.',
   'Source is frozen before validation. 2800 is a target, not an online measured rating.'])
 staging=Path(tempfile.mkdtemp(prefix='release_v10_r2_staging_',dir=R/'submissions'))
 for name in ('main.py','submission.tar.gz','NOTICE.txt','LICENSE.txt','validation.json'):
  shutil.copy2(stage/name,staging/name)
 (staging/'evidence.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
 for name in ('selection.json','gate_result.json','official_crosscheck.json','VALIDATION_PROTOCOL.md'):
  shutil.copy2(B/name,staging/name)
 assert sha(staging/'main.py')==expected
 assert sha(staging/'submission.tar.gz')==evidence['archive_sha256']
 assert not destination.exists();os.replace(staging,destination)
 print(json.dumps({'release':str(destination),'source_sha256':expected,
  'archive_sha256':evidence['archive_sha256'],'full_games':evidence['counted_full_games'],
  'strength_passed':True,'technical_passed':True,'online_submission':False}),flush=True)
if __name__=='__main__':main()
