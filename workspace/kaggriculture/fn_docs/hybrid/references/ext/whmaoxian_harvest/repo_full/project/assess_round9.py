"""Selection from development only, then one frozen independent confirmation."""
import argparse,json,hashlib,statistics,datetime
from pathlib import Path
from compare_round8 import read,compare
ROOT=Path(__file__).resolve().parent
NAMES=['combined','market_herd','herd_margin','slack','herd_contract']

def total(rows):
 rs=list(rows.values());assert all(r['valid'] for r in rs)
 return {'games':len(rs),'worlds':len({r['seed'] for r in rs}),'wins':sum(r['delta']>0 for r in rs),'losses':sum(r['delta']<0 for r in rs),'ties':sum(r['delta']==0 for r in rs),'points':statistics.mean(r['points'] for r in rs),'mean_margin':statistics.mean(r['delta'] for r in rs)}

def freeze():
 path=ROOT/'research/round9/frozen_selection.json'
 if path.exists():return json.loads(path.read_text(encoding='utf-8'))
 base=read([ROOT/'results/round9_v8_development.json']);assert len(base)==192
 scores={};paths={};hashes={}
 for name in NAMES:
  rows=read([ROOT/f'results/round9_{name}_development.json']);assert rows.keys()==base.keys()
  scores[name]=total(rows);paths[name]=next(iter(rows.values()))['candidate'];hashes[name]=next(iter(rows.values()))['candidate_sha256']
  assert hashlib.sha256((ROOT/paths[name]).read_bytes()).hexdigest()==hashes[name]
 chosen=max(NAMES,key=lambda n:(scores[n]['points'],scores[n]['mean_margin']))
 assert scores[chosen]['points']>total(base)['points']
 decision={'selected':chosen,'candidate':paths[chosen],'sha256':hashes[chosen],'development':scores,'baseline_development':total(base),
 'frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection_metric':'development win points; mean bank margin only breaks ties',
 'confirmation_worlds':48,'confirmation_opponents':json.loads((ROOT/'results/round9_v8_development.manifest.json').read_text())['opponents'],
 'confirmation_candidates':1,'confirmation_gate':'complete matched 384 games each, zero execution failures, world-cluster bootstrap 95 percent lower bound of point gain above zero; then packed-byte technical checks',
 'no_retuning_after_confirmation':True,'online_score_guaranteed':False}
 path.write_text(json.dumps(decision,indent=2),encoding='utf-8');return decision

def confirm():
 d=freeze();base=read([ROOT/'results/round9_v8_confirmation.json']);new=read([ROOT/'results/round9_selected_confirmation.json'])
 assert base.keys()==new.keys() and len(base)==384
 assert all(r['candidate_sha256']==d['sha256'] for r in new.values())
 report={'selection':d,'baseline':total(base),'candidate':total(new),'comparison':compare(base,new)}
 report['paired_final_shop_lists_differ']=sum(base[k]['shops']!=new[k]['shops'] for k in base)
 report['same_seed_does_not_guarantee_same_shops']=True
 report['local_strength_pass']=report['comparison']['metrics']['points_change']['world_bootstrap_95'][0]>0
 (ROOT/'results/round9_final_selection.json').write_text(json.dumps(report,indent=2),encoding='utf-8');return report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--confirmation',action='store_true');a=p.parse_args();print(json.dumps(confirm() if a.confirmation else freeze(),indent=2))
