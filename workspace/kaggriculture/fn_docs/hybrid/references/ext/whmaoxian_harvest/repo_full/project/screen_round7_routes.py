"""Small reacting-opponent screen; exploration seeds are not release holdouts."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
p = argparse.ArgumentParser()
p.add_argument('--team', required=True)
a = p.parse_args()
for source in sorted((ROOT / 'experiments/round7_routes').glob(a.team + '_*.py')):
    output = ROOT / ('results/round7_' + source.stem + '.json')
    subprocess.run([sys.executable, str(ROOT/'evaluate.py'), '--agent', str(source),
                    '--opponent', str(ROOT/'submissions/release_v6/main.py'), '--seeds', '44100', '44101',
                    '--both-seats', '--output', str(output)], check=True, stdout=subprocess.DEVNULL)
    d=json.loads(output.read_text())
    print(source.stem,d['wins'],d['games'],sum(r['delta'] for r in d['results'])/d['games'],flush=True)
