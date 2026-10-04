"""Retain failed attempts and replace every affected entrypoint case, not losses."""
from pathlib import Path
import datetime,hashlib,json,shutil
D=Path(__file__).resolve().parent; R=D.parents[2]
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def rows(path):return [json.loads(x) for x in Path(path).read_text(encoding='utf-8').splitlines()]
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
 initial=rows(D/'confirmation_results.jsonl'); repaired=rows(D/'confirmation_entry_repair_results.jsonl')
 jobs=read(D/'confirmation_jobs.json'); repair_jobs=read(D/'confirmation_entry_repair_jobs.json')
 assert len(initial)==len(jobs)==1920 and len(repaired)==len(repair_jobs)==288
 assert {r['id'] for r in initial}=={j['id'] for j in jobs}
 assert {r['id'] for r in repaired}=={j['id'] for j in repair_jobs}
 affected=[r for r in initial if r['family']=='marketshock']
 unaffected=[r for r in initial if r['family']!='marketshock']
 assert len(affected)==288 and len(unaffected)==1632
 assert all(not r.get('valid') and 'Object of type function is not JSON serializable' in r.get('exception','') for r in affected)
 assert all(r.get('valid') for r in unaffected+repaired),'Do not remove unrelated failures'
 identity=lambda r:(r['candidate_sha256'],r['seed'],r['seat'],r['family'])
 assert {identity(r) for r in affected}=={identity(r) for r in repaired}
 selection=read(D/'selection.json'); assert sha(R/selection['candidate'])==selection['sha256']
 archive=D/'confirmation_initial_attempt'; assert not archive.exists(); archive.mkdir()
 for name in ('confirmation_jobs.json','confirmation_results.jsonl','confirmation_results.summary.json','confirmation.log','confirmation_design.json'):
  shutil.copy2(D/name,archive/name)
 corrected_jobs=[j for j in jobs if j['family']!='marketshock']+repair_jobs
 corrected_rows=[dict(r,evidence_origin='initial_unaffected') for r in unaffected]+[dict(r,evidence_origin='declared_entry_repair') for r in repaired]
 corrected_jobs.sort(key=lambda r:(r['seed'],r['family'],r['seat'],r['candidate']))
 corrected_rows.sort(key=lambda r:(r['seed'],r['family'],r['seat'],r['candidate']))
 (D/'confirmation_jobs.json').write_text(json.dumps(corrected_jobs,indent=2),encoding='utf-8')
 (D/'confirmation_results.jsonl').write_text('\n'.join(json.dumps(r) for r in corrected_rows)+'\n',encoding='utf-8')
 design=read(D/'confirmation_design.json')
 for opponent in design['roster']:
  if opponent['name']=='marketshock':
   opponent['original_path']=opponent['path']; opponent['original_sha256']=opponent['sha256']
   opponent['path']=repair_jobs[0]['opponent']; opponent['sha256']=repair_jobs[0]['opponent_sha256']
   opponent['entrypoint_adapter']=True
 (D/'confirmation_design.json').write_text(json.dumps(design,indent=2),encoding='utf-8')
 receipt=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate_sha256=selection['sha256'],
  initial_jobs_sha256=sha(archive/'confirmation_jobs.json'),initial_ledger_sha256=sha(archive/'confirmation_results.jsonl'),
  correction_jobs_sha256=sha(D/'confirmation_entry_repair_jobs.json'),correction_ledger_sha256=sha(D/'confirmation_entry_repair_results.jsonl'),
  corrected_jobs_sha256=sha(D/'confirmation_jobs.json'),corrected_ledger_sha256=sha(D/'confirmation_results.jsonl'),
  initial_failed_non_game_attempts=288,unaffected_full_games_retained=1632,repaired_full_games=288,
  final_valid_full_games=1920,selection_changed=False,policy_changed=False)
 (D/'confirmation_entry_repair_receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
 print(json.dumps(receipt),flush=True)
if __name__=='__main__':main()
