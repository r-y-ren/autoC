"""Paired fresh-seed comparison of the frozen economy candidate and v6."""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
parser = argparse.ArgumentParser()
parser.add_argument('--opponent', required=True)
parser.add_argument('--label', required=True)
args = parser.parse_args()
for tag, source in [('v6', 'submissions/release_v6/main.py'), ('candidate', 'experiments/round7_economy.py')]:
    output = f'results/round7_holdout_{tag}_{args.label}.json'
    subprocess.run([sys.executable,'evaluate.py','--agent',source,'--opponent',args.opponent,
                    '--seeds','55300','55301','55302','55303','--both-seats','--output',output],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    print(output, flush=True)
