"""Rebuild and technically validate the frozen v8 archive."""
from pathlib import Path
import subprocess
import sys

def main():
    root=Path(__file__).resolve().parent
    args=['--candidate', 'experiments/round8_bounded_production.py', '--stage', 'submissions/release_v8', '--expected-sha256', '9fa83701138e80e3e5f9a6479cc2fa1c7e8a8965c4bd85d4e45d05ec5d4ffd4e', '--entry', 'round8_production_fusion_agent', '--profile', 'bounded-production', '--label', 'candidate_v8']
    subprocess.run([sys.executable,str(root/"build_release_round8.py"),*args],cwd=root,check=True)

if __name__=="__main__":main()
