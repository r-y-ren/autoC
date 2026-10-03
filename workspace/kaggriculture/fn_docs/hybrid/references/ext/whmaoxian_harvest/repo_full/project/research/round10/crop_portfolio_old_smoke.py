"""One official old-diagnostic smoke for physical crop-conversion delivery."""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from league_round9 import digest, run_job

candidate = 'experiments/round10_crop_portfolio_v2.py'
opponent = 'experiments/round8_top2_dsm_strict.py'
job = {
    'candidate': candidate,
    'candidate_sha256': digest(ROOT / candidate),
    'opponent': opponent,
    'opponent_sha256': digest(ROOT / opponent),
    'seed': 1829941733,
    'seat': 0,
    'split': 'old-diagnostic-smoke',
    'id': 'r10cp-v2-physical-smoke',
}
result = run_job(job)
out = ROOT / 'results/round10_crop_portfolio_v2_old_diagnostic.json'
out.write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps({k:result.get(k) for k in ('seed','seat','delta','money','opponent_money','valid','exception')}, indent=2))
print(json.dumps(result.get('telemetry',[{}])[0].get('details',{}).get('_R10CP_REPORT',{}), indent=2))
