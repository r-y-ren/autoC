"""Rebuild and validate the frozen v9 package; no Kaggle upload."""
from pathlib import Path
import subprocess,sys

def main():
    root=Path(__file__).resolve().parent
    args=['--candidate', 'experiments/round9_market_slack.py', '--stage', 'submissions/candidate_v9', '--expected-sha256', '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3', '--entry', 'round9_slack_agent', '--profile', 'generic', '--notice-file', 'research/round9/NOTICE_v9.txt', '--label', 'candidate_v9', '--resume']
    subprocess.run([sys.executable,str(root/"build_release_round8.py"),*args],cwd=root,check=True)
    subprocess.run([sys.executable,str(root/"publish_round9.py")],cwd=root,check=True)

if __name__=="__main__":main()
