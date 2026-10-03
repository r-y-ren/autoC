"""Untouched confirmation worlds, paired against the same reacting rivals."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

r=Path(__file__).parent
p=argparse.ArgumentParser()
p.add_argument('--opponent', required=True)
p.add_argument('--label', required=True)
a=p.parse_args()
for tag,source in [('orderbook','external/orderbook.py'),('fusion','experiments/round7_orderbook_v56.py')]:
    out=f'results/round7_final_{tag}_{a.label}.json'
    subprocess.run([sys.executable,'evaluate.py','--agent',source,'--opponent',a.opponent,
                    '--seeds','56100','56101','56102','56103','56104','56105','--both-seats','--output',out],
                   cwd=r,stdout=subprocess.DEVNULL,check=True)
    data=json.loads((r/out).read_text())
    print(tag,a.label,data['wins'],data['ties'],data['games'],flush=True)
