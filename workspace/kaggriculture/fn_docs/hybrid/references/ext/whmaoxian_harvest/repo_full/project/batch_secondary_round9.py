import subprocess,sys,json
from pathlib import Path
selection=json.loads(Path('research/round9/frozen_selection.json').read_text())
commands=[('top2_locked_stress',[sys.executable,'stress_top2_round9.py','--candidate',selection['candidate'],'--expected-sha256',selection['sha256'],'--workers','4']),
 ('direct_v8',[sys.executable,'league_round9.py','--candidate',selection['candidate'],'--opponents','submissions/release_v8/main.py','--split','confirmation','--count','48','--workers','6','--output','results/round9_direct_v8.json'])]
for name,cmd in commands:
 with open(f'results/round9_{name}.log','w',encoding='utf-8') as out:p=subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT)
 print(name,p.returncode,flush=True)
 if p.returncode:raise SystemExit(p.returncode)
