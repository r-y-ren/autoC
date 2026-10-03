"""Read-only progress display for the already running frozen confirmation."""
import json, time
from pathlib import Path
root = Path(__file__).resolve().parents[2]
base = root/'results/round11/v10-pressure-ledger-v2-confirmation'
ledger = base.with_suffix('.jsonl')
summary = base.with_suffix('.summary.json')
start = time.monotonic()
while not summary.exists() and time.monotonic()-start < 5400:
    done = bad = 0
    if ledger.exists():
        with ledger.open(encoding='utf-8') as stream:
            for line in stream:
                if not line.endswith('\n'):
                    continue
                row = json.loads(line)
                done += 1
                bad += not row['valid']
    print(json.dumps({'completed':done,'required':768,'invalid':bad}),flush=True)
    time.sleep(30)
if summary.exists():
    result = json.loads(summary.read_text(encoding='utf-8'))
    print(json.dumps({'finished':True,'complete_and_valid':result['complete_and_valid'],
                      'promotion_pool':result['promotion_pool']}),flush=True)
else:
    print('Progress display stopped without a complete summary; no release decision.',flush=True)
