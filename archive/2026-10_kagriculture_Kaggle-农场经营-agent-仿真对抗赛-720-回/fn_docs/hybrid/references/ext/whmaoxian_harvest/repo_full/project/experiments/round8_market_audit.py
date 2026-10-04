"""Audit biologically periodic supply using only previous successful study trades."""
import gzip,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
periods={'MILK':48,'WOOL':72,'STRAWBERRY':48,'EGG':24}
rows=[r for r in json.loads((root/'research/round7/top2/index.json').read_text()) if r['split']=='study']
output=[]
for row in rows:
 trades=json.loads(gzip.decompress((root/f"research/round7/top2/{row['episode_id']}_trades.json.gz").read_bytes()))[row['seat']]
 history={}
 for t,op,item,price,q in trades:
  if op=='SELL' and price>1: history[t,item]=history.get((t,item),0)+q
 metrics={}
 for item,period in periods.items():
  guessed=hits=qty_guess=qty_actual=0
  for t in range(240,696):
   previous=[sum(history.get((t-lag+dt,item),0) for dt in (-1,0,1)) for lag in (period,2*period)]
   if min(previous)>=4:
    guessed+=1;qty_guess+=min(previous)
    actual=sum(history.get((t+dt,item),0) for dt in (-1,0,1))
    hits+=actual>=2;qty_actual+=actual
  metrics[item]={'predictions':guessed,'matched_within_one_turn':hits,'precision':round(hits/max(guessed,1),3),'predicted_qty':qty_guess,'actual_qty_in_windows':qty_actual}
 output.append({'team':row['team'],'episode_id':row['episode_id'],'metrics':metrics})
print(json.dumps(output,indent=2))
(root/'results/round8_market_recurrence_audit.json').write_text(json.dumps(output,indent=2))
