"""Rebuild the frozen V10 archive and publish only if all recorded gates pass.
No Kaggle upload; the frozen V9 and root main.py are never overwritten.
"""
from pathlib import Path
import hashlib
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SHA = '3a4601081cc909ae7baf97ec5ddb0e1a8a5a1a27c9cd072cdeaaf7d34c803e0b'

def main():
    source = ROOT/'experiments/v10_pressure_ledger.py'
    if hashlib.sha256(source.read_bytes()).hexdigest() != SHA:
        raise RuntimeError('The frozen V10 source changed; use a new experiment instead.')
    command = [sys.executable, str(ROOT/'build_release_round8.py'),
        '--candidate','experiments/v10_pressure_ledger.py',
        '--stage','submissions/candidate_v10_ledger','--expected-sha256',SHA,
        '--entry','v10_ledger_agent','--profile','generic',
        '--notice-file','research/v10_20260926/NOTICE_v10.txt',
        '--license-file','submissions/release_v9/LICENSE.txt',
        '--label','candidate_v10_ledger','--resume']
    subprocess.run(command, cwd=ROOT, check=True)
    subprocess.run([sys.executable,str(ROOT/'publish_v10_verified.py')],cwd=ROOT,check=True)

if __name__ == '__main__':
    main()
