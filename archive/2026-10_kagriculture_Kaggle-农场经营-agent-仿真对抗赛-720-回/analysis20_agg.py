#!/usr/bin/env python3
"""analysis20 aggregation: builds fn_docs/hybrid/results/2026-09-25-analysis20-pool-audit.json
from /tmp/kagr_root/analysis20_rows.json + submissions + episodes + full leaderboard."""
import csv, json, statistics as st
from collections import Counter, defaultdict

ROOT = "/tmp/kagr_root"
CAMPAIGN = "/mnt/data/Code/autoC/workspace/kaggriculture"
SNAP = f"{CAMPAIGN}/fn_docs/hybrid/results/2026-09-25-analysis20-pool-audit.json"
REFS = {"r30": 56491673, "r31": 56508268, "r32": 56517593, "r33": 56517991, "r34a": 56526029}
A19 = json.load(open(f"{CAMPAIGN}/fn_docs/hybrid/results/2026-09-25-analysis19-r34a-read.json"))
BANDS = ("weak<60k", "mid60-90k", "strong>=90k")

state = json.load(open(f"{ROOT}/analysis20_rows.json"))
rows = state["rows"]

# ---------- 7a reading table ----------
subs = json.load(open(f"{ROOT}/submissions.json"))
by_ref = {s.get("ref") or s.get("id"): s for s in subs}
refs_out = {}
for tag, ref in REFS.items():
    eps = json.load(open(f"{ROOT}/episodes-{tag}-{ref}.json"))
    n_pub = sum(1 for e in eps if "PUBLIC" in e.get("type", ""))
    score = float(by_ref[ref]["publicScore"])
    prev = A19["refs"].get(tag, {})
    refs_out[tag] = {
        "ref": ref, "score": score, "n_pub": n_pub,
        "prev_score": prev.get("score"), "prev_n": prev.get("n"),
        "d_score": round(score - prev["score"], 1) if isinstance(prev.get("score"), (int, float)) else None,
        "d_n": (n_pub - prev["n"]) if isinstance(prev.get("n"), int) else None,
    }

new_eps = {tag: refs_out[tag]["d_n"] for tag in REFS}

# ---------- row groups ----------
r34a = [r for r in rows if r["tag"] == "r34a"]
r33_all = [r for r in rows if r["tag"] == "r33"]
R34A_FIRST = min(r["createTime"] for r in r34a) if r34a else None
r33_win = [r for r in r33_all if r.get("group") == "b_r33_window"]
r33_strict = [r for r in r33_all if r["createTime"] >= R34A_FIRST] if R34A_FIRST else []


def wl(rows_):
    W = sum(1 for r in rows_ if r["res"] == "W")
    L = sum(1 for r in rows_ if r["res"] == "L")
    T = len(rows_) - W - L
    return W, L, T


def band_dist(rows_):
    c = Counter(r["opp_band"] for r in rows_)
    n = len(rows_) or 1
    return {b: {"n": c.get(b, 0), "share": round(c.get(b, 0) / n, 3)} for b in BANDS}


def band_wl(rows_, label=None):
    out = {"n": len(rows_), "WLT": wl(rows_)}
    if rows_:
        out["wr"] = round(wl(rows_)[0] / len(rows_), 3)
        out["mean_margin"] = round(st.mean([r["margin"] for r in rows_]), 1)
    for b in BANDS:
        g = [r for r in rows_ if r["opp_band"] == b]
        e = {"n": len(g)}
        if g:
            W, L, T = wl(g)
            e["WLT"] = [W, L, T]
            e["wr"] = round(W / len(g), 3)
            e["mean_margin"] = round(st.mean([r["margin"] for r in g]), 1)
        out[b] = e
    return out


def loss_dissect(rows_, label=None):
    L = [r for r in rows_ if r["res"] == "L"]
    out = {
        "n_losses": len(L),
        "loss_rate": round(len(L) / len(rows_), 3) if rows_ else None,
        "band_of_losses": dict(Counter(r["opp_band"] for r in L)),
        "margins": sorted(r["margin"] for r in L),
        "median_margin": st.median([r["margin"] for r in L]) if L else None,
        "mirror_twin_losses": sum(1 for r in L if r["mirror_twin"]),
        "small_margin_abs500_losses": sum(1 for r in L if abs(r["margin"]) < 500),
        "losses_vs_strong": [
            {"episode": r["episode"], "opp": r["opp"], "margin": r["margin"],
             "money_ratio": r["money_ratio"], "mirror_twin": r["mirror_twin"]}
            for r in L if r["opp_band"] == "strong>=90k"],
    }
    return out


def opp_freq(rows_, other_rows):
    c = Counter(r["opp"] for r in rows_)
    oc = Counter(r["opp"] for r in other_rows)
    tab = [{"opp": o, "n": n, "WLT": wl([r for r in rows_ if r["opp"] == o])}
           for o, n in c.most_common()]
    only_here = [{"opp": o, "n": n,
                  "record": wl([r for r in rows_ if r["opp"] == o]),
                  "mean_margin": round(st.mean([r["margin"] for r in rows_ if r["opp"] == o]), 1)}
                 for o, n in c.items() if n >= 3 and oc.get(o, 0) == 0]
    named = {o: {"n": c.get(o, 0), "record": wl([r for r in rows_ if r["opp"] == o]),
                 "n_in_r33_window": oc.get(o, 0)}
             for o in ("haideptry", "haodou092") if c.get(o)}
    return {"top": tab[:15], "n_unique_opps": len(c),
            "only_in_this_pool_ge3": only_here, "named_lineage": named}


pool_audit = {
    "mirror_twin_rule": "fallback |margin|<500 AND |ourF-oppF|/mean(ourF,oppF)<0.01 (原 classification.json Fratio 公式未入库，此为近似口径)",
    "windows": {
        "r34a_first_game": R34A_FIRST,
        "r33_window_b_from": min((r["createTime"] for r in r33_win), default=None),
        "note": "b_r33_window=r33 PUBLIC 局中昨日 replay 轮(09-24T11:51Z pull)之后新增; strict=r33 中 createTime>=r34a 首局",
    },
    "band_dist": {
        "r34a_full": band_dist(r34a),
        "r33_window_b": band_dist(r33_win),
        "r33_strict_r34a_window": band_dist(r33_strict),
        "r33_all_rows": band_dist(r33_all),
    },
    "opp_analysis": {
        "r34a_vs_r33window": opp_freq(r34a, r33_win),
        "r33window_vs_r34a": opp_freq(r33_win, r34a),
        "shared_opps_overlap": len({r["opp"] for r in r34a} & {r["opp"] for r in r33_win}),
    },
    "band_wl": {
        "r34a_full": band_wl(r34a),
        "r33_window_b": band_wl(r33_win),
        "r33_strict": band_wl(r33_strict),
        "r33_all_rows": band_wl(r33_all),
    },
    "loss_dissect": {
        "r34a_full": loss_dissect(r34a),
        "r33_window_b": loss_dissect(r33_win),
        "r33_strict": loss_dissect(r33_strict),
    },
    "kinship_proxy": {
        "note": "同源克隆战签名: 强带+微差(|m|<500)/mirror_twin",
        "r34a": {
            "strong_small_margin": sum(1 for r in r34a if r["opp_band"] == "strong>=90k" and abs(r["margin"]) < 500),
            "strong_n": sum(1 for r in r34a if r["opp_band"] == "strong>=90k"),
            "mirror_twin_all": sum(1 for r in r34a if r["mirror_twin"]),
            "small_margin_all": sum(1 for r in r34a if abs(r["margin"]) < 500),
        },
        "r33_window_b": {
            "strong_small_margin": sum(1 for r in r33_win if r["opp_band"] == "strong>=90k" and abs(r["margin"]) < 500),
            "strong_n": sum(1 for r in r33_win if r["opp_band"] == "strong>=90k"),
            "mirror_twin_all": sum(1 for r in r33_win if r["mirror_twin"]),
            "small_margin_all": sum(1 for r in r33_win if abs(r["margin"]) < 500),
        },
    },
}

# ---------- deep cuts: trajectory / same-stage / scheduling / mirror farmers ----------
def blocks(rs, k=5):
    n = len(rs)
    per = max(1, n // k)
    out = []
    for i in range(k):
        b = rs[i * per:(i + 1) * per] if i < k - 1 else rs[i * per:]
        W, L, T = wl(b)
        out.append({"games": f"{b[0]['createTime'][11:16]}-{b[-1]['createTime'][11:16]}Z",
                    "WLT": [W, L, T], "mean_margin": round(st.mean([r["margin"] for r in b]), 0),
                    "mean_ourF": round(st.mean([r["ourF"] for r in b]), 0)})
    return out


r34a_sorted = sorted(r34a, key=lambda r: r["createTime"])
r33w_sorted = sorted(r33_win, key=lambda r: r["createTime"])
r33_all_sorted = sorted(r33_all, key=lambda r: r["createTime"])
r33_first65 = r33_all_sorted[:65]
W65, L65, _ = wl(r33_first65)
sm_r33w = [r for r in r33_win if abs(r["margin"]) < 500]
Wsm, Lsm, Tsm = wl(sm_r33w)
sched = {}
for tag, ref in REFS.items():
    eps = json.load(open(f"{ROOT}/episodes-{tag}-{ref}.json"))
    pub = sorted(e["createTime"] for e in eps if "PUBLIC" in e.get("type", ""))
    sched[tag] = {"n_pub": len(pub), "first": pub[0], "last_game": pub[-1],
                  "still_sched": pub[-1] >= "2026-09-25T01:30"}
farmer = Counter(r["opp"] for r in sm_r33w)

deep_cuts = {
    "trajectory_5blk": {"r34a": blocks(r34a_sorted), "r33_window": blocks(r33w_sorted)},
    "same_stage": {
        "note": "r33 首局09:44Z(昨晨), r34a 首局16:17Z(昨午后) —— 池时代不同",
        "r33_first65": {"WLT": [W65, L65, 0], "wr": round(W65 / 65, 3),
                        "mean_ourF": round(st.mean([r["ourF"] for r in r33_first65]), 0),
                        "mean_margin": round(st.mean([r["margin"] for r in r33_first65]), 0),
                        "score_then": 2017.4},
        "r34a_full95": {"WLT": wl(r34a), "wr": round(wl(r34a)[0] / len(r34a), 3),
                        "mean_ourF": round(st.mean([r["ourF"] for r in r34a]), 0),
                        "mean_margin": round(st.mean([r["margin"] for r in r34a]), 0),
                        "score_now": 1868.5},
    },
    "scheduling": {
        "rule_observed": "活跃件=最近2次提交：r30止于r32上线(09:08≈09:19)、r31止于r33上线(09:36≈09:39)、r32止于r34a上线(15:57≈16:13)",
        "refs": sched,
        "now_utc": "2026-09-25T02:41Z",
    },
    "pool_segregation": {
        "r34a_unique_opps": len({r["opp"] for r in r34a}),
        "r33_window_unique_opps": len({r["opp"] for r in r33_win}),
        "shared_opps": sorted({r["opp"] for r in r34a} & {r["opp"] for r in r33_win}),
    },
    "r33_mirror_farmers": {
        "small_margin_games": len(sm_r33w), "record_within": [Wsm, Lsm, Tsm],
        "top_smallm_opps": farmer.most_common(8),
        "prior42_smallm": sum(1 for r in r33_all_sorted if r.get("group") == "c_r33_prior" and abs(r["margin"]) < 500),
        "note": "r33 昨日白天(前42局)小差局21% -> 窗口期(12:09Z后)53%：同源镜像潮淹没老件池",
    },
    "r34a_mirror_games": [{"episode": r["episode"], "opp": r["opp"], "res": r["res"], "margin": r["margin"]}
                          for r in r34a if abs(r["margin"]) < 500],
}

# ---------- 7f leaderboard ----------
lb = list(csv.reader(open("/tmp/lb_a20/kaggriculture-publicleaderboard-2026-09-25T02:38:14.csv")))
hdr = [h.replace("\ufeff", "") for h in lb[0]]
idx = {h: i for i, h in enumerate(hdr)}
lbout = {"csv": "kaggriculture-publicleaderboard-2026-09-25T02:38:14.csv (download, 9988 teams)",
         "cols": hdr, "top5": [{"rank": r[idx["Rank"]], "team": r[idx["TeamName"]],
                                "score": r[idx["Score"]]} for r in lb[1:6]],
         "us_and_lineage": []}
for r in lb[1:]:
    n = r[idx["TeamName"]]
    ln = n.lower()
    if n == "renyxin" or "haideptry" in ln or "haodou" in ln:
        lbout["us_and_lineage"].append({"rank": int(r[idx["Rank"]]), "team": n,
                                        "score": float(r[idx["Score"]]),
                                        "submissionCount": r[idx["SubmissionCount"]]})
n_2500 = sum(1 for r in lb[1:] if float(r[idx["Score"]]) > 2500)
n_2000 = sum(1 for r in lb[1:] if float(r[idx["Score"]]) > 2000)
lbout["structure"] = {"teams": len(lb) - 1, "gt2500": n_2500, "gt2000": n_2000}
lbout["note_renyxin_board_score"] = ("板面分 2002.4=r33 而非我方最高 r30 2071.4 —— 板面口径未取历史最高件；"
                                     "haideptry 名件不在榜（未参赛或未提交），2965 血统在榜可见名为 haodou092")

snapshot = {
    "source": {
        "pulled_at": state.get("finished_utc") or state["started_utc"],
        "commands": [
            "KAGGLE_API_TOKEN=$(kaggle auth print-access-token) python3 pull_meta.py <ROOT>",
            "kaggle competitions episodes 56526029 --format json  # raw_decode_list 解析",
            "kaggle competitions leaderboard kaggriculture --show --csv",
            "kaggle competitions leaderboard kaggriculture --download  # 全量 9988 队",
            "kaggle competitions replay <id>  # a=95(r34a全量) b=81(r33窗口) 流式拉取后即删(tmpfs容量), c=42 原地解析",
            "python3 /tmp/kagr_root/analysis20_rows.py  # pull+parse+rows",
            "python3 /tmp/kagr_root/analysis20_agg.py  # 本快照",
        ],
    },
    "refs": refs_out,
    "new_episodes_since_a19": new_eps,
    "pool_audit": pool_audit,
    "deep_cuts": deep_cuts,
    "leaderboard": lbout,
    "fails": state["fails"],
    "selfplay": state["selfplay"],
    "rows_r34a": [{k: r[k] for k in ("episode", "createTime", "opp", "seat", "res", "margin",
                                     "ourF", "oppF", "opp_band", "opp_actions", "opp_animals_end",
                                     "margin_d10", "margin_d20", "money_ratio", "mirror_twin")}
                  for r in sorted(r34a, key=lambda x: x["episode"])],
    "rows_r33_window": [{k: r[k] for k in ("episode", "createTime", "opp", "seat", "res", "margin",
                                           "ourF", "oppF", "opp_band", "opp_actions", "opp_animals_end",
                                           "margin_d10", "margin_d20", "money_ratio", "mirror_twin")}
                        for r in sorted(r33_win, key=lambda x: x["episode"])],
    "rows_r33_prior": [{"episode": r["episode"], "createTime": r["createTime"], "opp": r["opp"],
                        "res": r["res"], "margin": r["margin"], "opp_band": r["opp_band"],
                        "mirror_twin": r["mirror_twin"]}
                       for r in sorted([x for x in r33_all if x.get("group") == "c_r33_prior"],
                                       key=lambda x: x["episode"])],
}
json.dump(snapshot, open(SNAP, "w"), ensure_ascii=False, indent=1)

# ---------- console summary ----------
print("=== refs ===")
for t, v in refs_out.items():
    print(f"{t}: {v['score']}@{v['n_pub']} (prev {v['prev_score']}@{v['prev_n']}, d={v['d_score']}/{v['d_n']})")
print("=== band dist ===")
for k, v in pool_audit["band_dist"].items():
    print(k, {b: f"{d['n']}({d['share']:.0%})" for b, d in v.items()})
print("=== band WL ===")
for k in ("r34a_full", "r33_window_b", "r33_strict", "r33_all_rows"):
    v = pool_audit["band_wl"][k]
    print(k, "n=", v["n"], "WLT=", v["WLT"], "wr=", v.get("wr"),
          "| weak:", v["weak<60k"], "| mid:", v["mid60-90k"], "| strong:", v["strong>=90k"])
print("=== r34a losses ===")
ld = pool_audit["loss_dissect"]["r34a_full"]
print("nL=", ld["n_losses"], "rate=", ld["loss_rate"], "bands=", ld["band_of_losses"],
      "med=", ld["median_margin"], "mirror=", ld["mirror_twin_losses"], "smallm=", ld["small_margin_abs500_losses"])
print("=== r33 window losses ===")
ld = pool_audit["loss_dissect"]["r33_window_b"]
print("nL=", ld["n_losses"], "rate=", ld["loss_rate"], "bands=", ld["band_of_losses"],
      "med=", ld["median_margin"], "mirror=", ld["mirror_twin_losses"], "smallm=", ld["small_margin_abs500_losses"])
print("=== opp top r34a ===")
for t in pool_audit["opp_analysis"]["r34a_vs_r33window"]["top"][:10]:
    print(t["opp"], t["n"], t["WLT"])
print("=== only in r34a pool >=3 ===")
for t in pool_audit["opp_analysis"]["r34a_vs_r33window"]["only_in_this_pool_ge3"]:
    print(t["opp"], t["n"], t["record"], "mm=", t["mean_margin"])
print("=== named ===", pool_audit["opp_analysis"]["r34a_vs_r33window"]["named_lineage"])
print("=== kinship ===", json.dumps(pool_audit["kinship_proxy"]))
print("=== leaderboard ===", lbout["us_and_lineage"], lbout["structure"])
print("fails:", state["fails"], "selfplay:", len(state["selfplay"]))
print("SNAP ->", SNAP)
