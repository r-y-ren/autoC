"""Verify one complete game and its outcome branches before bulk collection."""
from pathlib import Path
import json
from collect import gather
D=Path(__file__).resolve().parent
if __name__=='__main__':
    jobs=json.loads((D/'training_jobs.json').read_text())
    path=D/'pilot_result.json'
    if path.exists():
        result=json.loads(path.read_text());assert result['id']==jobs[0]['id']
    else:
        result=gather(jobs[0]);path.write_text(json.dumps(result,indent=2))
    print(json.dumps({k:result.get(k) for k in ('id','valid','control','seconds','exception','captured_output')}),flush=True)
    print(json.dumps(dict(samples=len(result.get('samples',[])),gains=[s['gain'] for s in result.get('samples',[])])),flush=True)
    if not result['valid']:raise SystemExit(1)
    output=D/'training_results.jsonl'
    if not output.exists():output.write_text(json.dumps(result)+'\n')
