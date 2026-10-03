"""Finalize public episode statistics and compact audited accounting deltas."""
from collections import Counter
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research/round7"
data = json.loads((OUT / "user_episodes.json").read_text())
teams = {x["id"]:x["teamName"] for x in data["teams"]}
rows = []
for game in data["episodes"]:
    ours = [a for a in game["agents"] if a["submissionId"] == 56416104]
    rival = [a for a in game["agents"] if a["submissionId"] != 56416104]
    if game["state"] != "COMPLETED" or game.get("type") != "EPISODE_TYPE_PUBLIC" or len(ours) != 1 or len(rival) != 1:
        continue
    a,b = ours[0],rival[0]
    delta = a["reward"]-b["reward"]
    rows.append({"episode_id":game["id"],"time":game["endTime"],"seat":a.get("index",0),"delta":delta,
                 "result":"win" if delta>0 else "loss" if delta<0 else "tie",
                 "opponent":teams[b["teamId"]],"rating":a["updatedScore"]})
rows.sort(key=lambda r:r["time"],reverse=True)
losses = sorted(-r["delta"] for r in rows if r["delta"]<0)
def quantile(p):
    index = (len(losses)-1)*p
    lo = int(index)
    return losses[lo] + (losses[min(lo+1,len(losses)-1)]-losses[lo])*(index-lo)
bins = {"0 < loss <= 100":sum(0<x<=100 for x in losses),
        "100 < loss <= 500":sum(100<x<=500 for x in losses),
        "500 < loss <= 5000":sum(500<x<=5000 for x in losses),
        "loss > 5000":sum(x>5000 for x in losses)}
summary = {"as_of":rows[0]["time"],"submission_id":56416104,"public_games":len(rows),
           "record":dict(Counter(r["result"] for r in rows)),
           "last_50":dict(Counter(r["result"] for r in rows[:50])),
           "last_20":dict(Counter(r["result"] for r in rows[:20])),
           "latest_rating":rows[0]["rating"],"peak_visible_rating":max(r["rating"] for r in rows),
           "loss_coin_quantiles":{str(p):quantile(p) for p in (0,.25,.5,.75,.9,1)},
           "loss_coin_bins":bins,"largest_loss":min(rows,key=lambda r:r["delta"])}
comparisons = []
for path in OUT.glob("metrics-*.json"):
    report = json.loads(path.read_text(encoding="utf-8"))
    eid=report["episode_id"]
    replay=json.loads(gzip.decompress((OUT/f"user-{eid}.json.gz").read_bytes()))
    for p,m in enumerate(report["metrics"]):
        m["final_seeds"]=replay["steps"][-1][p]["observation"]["private"]["seeds"]
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    meta=next(r for r in rows if r["episode_id"]==eid)
    me,opp=report["metrics"][meta["seat"]],report["metrics"][1-meta["seat"]]
    comparison={**meta,"revenue_delta":{k:me["sales_revenue"].get(k,0)-opp["sales_revenue"].get(k,0)
                        for k in set(me["sales_revenue"])|set(opp["sales_revenue"])},
                "purchase_cost_delta":{k:me["purchase_cost"].get(k,0)-opp["purchase_cost"].get(k,0)
                        for k in set(me["purchase_cost"])|set(opp["purchase_cost"])},
                "hire_cost_delta":me["hire_cost"]-opp["hire_cost"],"land_cost_delta":me["land_cost"]-opp["land_cost"]}
    check=sum(comparison["revenue_delta"].values())-sum(comparison["purchase_cost_delta"].values())-comparison["hire_cost_delta"]-comparison["land_cost_delta"]
    assert check==meta["delta"]
    comparisons.append(comparison)
summary["accounting_comparisons"]=comparisons
(OUT/"feedback3_ladder_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in summary.items() if k!="accounting_comparisons"},ensure_ascii=False,indent=2))
