import subprocess,sys,json
from pathlib import Path
from assess_round9 import freeze
selection=freeze()
pairs=[('submissions/release_v8/main.py','v8'),(selection['candidate'],'selected')]
for source,name in pairs:
 with open(f'results/round9_{name}_confirmation.log','w',encoding='utf-8') as out:
  p=subprocess.run([sys.executable,'league_round9.py','--candidate',source,'--opponents',*selection['confirmation_opponents'],'--split','confirmation','--count','48','--workers','6','--output',f'results/round9_{name}_confirmation.json'],stdout=out,stderr=subprocess.STDOUT)
 print(name,p.returncode,flush=True)
 if p.returncode:raise SystemExit(p.returncode)
subprocess.run([sys.executable,'assess_round9.py','--confirmation'],check=True)
