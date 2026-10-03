import subprocess,sys
pairs=[('submissions/release_v8/main.py','v8'),('experiments/round9_market_combined.py','combined'),('experiments/round9_market_herd.py','market_herd')]
for source,name in pairs:
 p=subprocess.run([sys.executable,'league_round9.py','--candidate',source,'--opponents','external/round9/frontier/main.py','external/round8/master2965/main.py','experiments/round8_top2_dsm_strict.py','external/orderbook.py','--split','development','--count','24','--workers','6','--output',f'results/round9_{name}_development.json'],stdout=open(f'results/round9_{name}_development.log','w',encoding='utf-8'),stderr=subprocess.STDOUT)
 print(name,p.returncode,flush=True)
 if p.returncode:raise SystemExit(p.returncode)
