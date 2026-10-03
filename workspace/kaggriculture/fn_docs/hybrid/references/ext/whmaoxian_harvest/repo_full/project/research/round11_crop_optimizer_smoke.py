"""Two bounded official-engine smokes; these old diagnostics are not validation."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from league_round9 import digest, run_job

candidate = 'experiments/round11_crop_optimizer.py'
opponent = 'experiments/round8_top2_dsm_strict.py'
for seed in (1829941733, 242588832):
    job = {
        'candidate': candidate,
        'candidate_sha256': digest(ROOT / candidate),
        'opponent': opponent,
        'opponent_sha256': digest(ROOT / opponent),
        'seed': seed,
        'seat': 0,
        'split': 'old-diagnostic-smoke',
        'id': 'r11co-smoke-%d' % seed,
    }
    result = run_job(job)
    path = ROOT / ('results/round11_crop_optimizer_smoke_%d.json' % seed)
    path.write_text(json.dumps(result, indent=2), encoding='utf-8')
    telemetry = result.get('telemetry',[{}])[0].get('details',{}).get('_R11CO_REPORT',{})
    print(json.dumps({'seed':seed, 'valid':result.get('valid'), 'delta':result.get('delta'),
                      'exception':result.get('exception'), 'telemetry':telemetry}, ensure_ascii=False))
