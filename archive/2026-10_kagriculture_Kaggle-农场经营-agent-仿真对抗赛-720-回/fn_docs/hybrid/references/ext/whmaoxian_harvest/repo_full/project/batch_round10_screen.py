"""Run the four predeclared V10 hypotheses on the same small development subset."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
opponents = [
    'submissions/release_v9/main.py',
    'external/round9/frontier/main.py',
    'experiments/round8_top2_dsm_strict.py',
    'external/round8/master2965/main.py',
]
variants = [
    ('credit_flush', 'experiments/round10_credit_flush.py'),
    ('ongoing_flush', 'experiments/round10_ongoing_flush.py'),
    ('crop_flush', 'experiments/round10_crop_flush.py'),
    ('no_final_reorder', 'experiments/round10_no_final_reorder.py'),
]
for label, candidate in variants:
    output = f'results/round10_{label}_screen.json'
    log = root / f'results/round10_{label}_screen.log'
    args = [sys.executable, str(root / 'league_round10.py'), '--candidate', candidate,
            '--opponents', *opponents, '--split', 'development', '--count', '8',
            '--workers', '5', '--output', output]
    with log.open('a', encoding='utf-8') as stream:
        result = subprocess.run(args, cwd=root, stdout=stream, stderr=subprocess.STDOUT)
    print(label, result.returncode, flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
