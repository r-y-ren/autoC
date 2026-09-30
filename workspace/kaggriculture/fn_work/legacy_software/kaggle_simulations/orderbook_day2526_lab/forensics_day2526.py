# -*- coding: utf-8 -*-
"""forensics_day2526：d25/26 单日凹陷根因定位（traced 对照；判决先行·不发射
不提交）。

责任口径（任务 day2526-T1）：
- 对照=drop_half（u2v2_drop_half，sha 5d2d1246…，在飞最强件）vs mpx 胜者件
  （mpx_w24_p2_3_h14，sha f0101de9…）；8 局 traced 同 seed（26 败局前 8
  fold，席位 j%2 轮转），sim_bridge 对照认证 30/30 先行。
- 解剖窗 d25/26（step 576-624 右开）逐拍：挂单量/成交价/触发门行为（_U2_DEC
  + half_fires）/对手流/排水交互（市场库存 Δ）/库存形态（shed/钱路径）。
- 判定根因候选：门拦错 vs 半量放少 vs 产线节奏（COW interval2 / SHEEP
  interval3 的第 N 周期落点）。
- 读数：终局钱 farms[obs.player]；fill=影子引擎逐拍归因；钱差=逐拍 money Δ。
证据边跑边写 fn_docs/hybrid/results/2026-09-30-day2526.json 的 forensics 节；
账本落 orderbook_day2526_lab/evidence/。不改既有代码；不提交；不发射。
"""
from __future__ import annotations

import importlib.util
import json
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))
import day2526_common as C  # noqa: E402

from orderbook_r40 import sim_bridge as sb  # noqa: E402

RECORD_VERSION = "day2526-forensics/1.0"
NEUTRAL_SEEDS = [2026093001, 2026093002, 2026093003, 2026093004, 2026093005,
                 2026093006, 2026093007, 2026093008, 2026093009, 2026093010,
                 2026093011, 2026093012, 2026093013, 2026093014]
ARMS = {"drop_half": C.DROP_HALF_MAIN, "mpx": C.MPX_MAIN}
FOCUS_STEPS = tuple(range(C.FOCUS[0], C.FOCUS[1]))   # 576..623

ANOMALIES = []


def flush_ev(ev):
    ev["anomaly"] = list(ANOMALIES)
    ev["_generated_at"] = C.now()
    C.EVID_DIR.mkdir(parents=True, exist_ok=True)
    C.EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged = {}
    if C.EVID_PATH.exists():
        try:
            merged = json.loads(C.EVID_PATH.read_text(encoding="utf-8"))
        except Exception:
            merged = {}
    merged.update(ev)
    C.EVID_PATH.write_text(json.dumps(merged, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")


def cert_sim():
    auth_corpus = list(C.LOSS_FOLDS) + [674000 + i * 133 for i in range(8)] \
        + NEUTRAL_SEEDS
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(C.EVID_DIR / "sim_auth_record.json")},
        auth_corpus)
    lite = {k: auth.get(k) for k in
            ("loaded", "consistency", "consistency_ok", "degraded",
             "degraded_reason", "engine", "version")}
    return auth, lite


def run_traced(arm, path, units, run_cfg):
    """逐局 traced 跑（单进程，保 ns 台账可读）。"""
    out = {}
    for u in units:
        sinks, nses = {0: [], 1: []}, {}
        # 我席=track 件（含台账 ns），对面=对手件
        pair = (path, u["opp_path"]) if int(u["seat"]) == 0 else \
            (u["opp_path"], path)
        built = []
        for seat, ap in enumerate(pair):
            inner, ns = C.load_agent_ns(ap)
            nses[seat] = ns
            built.append(C.Tracer(inner, seat, sinks[seat]))
        game = {"seed": int(u["seed"]), "agents": built}
        t0 = time.time()
        res = sb.run_games([game], run_cfg)
        rows = list(res.get("games") or [])
        rr = rows[0] if rows else {}
        key = (int(u["seed"]), int(u["seat"]))
        row = {"seed": int(u["seed"]), "seat": int(u["seat"]),
               "arm": arm, "opponent": u.get("opponent"),
               "banks": rr.get("banks"), "error": rr.get("error"),
               "engine": res.get("engine")}
        if row["banks"] is not None and row["error"] is None:
            row["margin"] = float(rr["banks"][int(u["seat"])]) - float(
                rr["banks"][1 - int(u["seat"])])
            row["reads"] = C.end_reads(sinks[int(u["seat"])])
            row["stream_sha_our"] = C.stream_digest(sinks[int(u["seat"])])
        u2r = (nses[int(u["seat"])].get("_MX_REPORT") or {}).get("u2") \
            if int(u["seat"]) in nses else None
        if u2r is None and isinstance(nses.get(0), dict):
            u2r = (nses[0].get("_MX_REPORT") or {}).get("u2")
        row["u2_report"] = dict(u2r) if isinstance(u2r, dict) else None
        row["u2_dec_focus"] = [d for d in
                               (nses[int(u["seat"])].get("_U2_DEC") or [])
                               if isinstance(d, (list, tuple))
                               and FOCUS_STEPS[0] <= int(d[0]) < FOCUS_STEPS[-1] + 1]
        row["s758"] = {k: v for k, v in
                       (nses[int(u["seat"])].get("_S758_REPORT") or {}).items()
                       if isinstance(v, (int, float))} or None
        out[key] = {"row": row, "sinks": sinks, "elapsed": round(time.time()
                                                                 - t0, 2)}
    return out


def tick_view(sinks, our_seat, shadow, steps):
    """逐拍解剖表：价格/库存/挂单/成交/钱路径/对手流/排水。"""
    m = {0: {}, 1: {}}
    for seat in (0, 1):
        for entry in (sinks.get(seat) or []):
            m[seat][int(entry[0])] = (entry[1], entry[2])
    rows = []
    for s in steps:
        obs, act = m[our_seat].get(s, (None, None))
        obs = obs if isinstance(obs, dict) else {}
        market = obs.get("market") or {}
        prices = market.get("prices") or {}
        inv = market.get("inventory") or {}
        shed = ((obs.get("private") or {}) if isinstance(obs.get("private"),
                dict) else {}).get("shed") or {}
        farms = obs.get("farms")
        money = None
        if isinstance(farms, list) and our_seat < len(farms) \
                and isinstance(farms[our_seat], dict):
            money = C.num(farms[our_seat].get("money"))
        our_sub = C.submit_rows(act)
        opp_obs, opp_act = m[1 - our_seat].get(s, (None, None))
        opp_sub = C.submit_rows(opp_act) if isinstance(opp_act, dict) else []
        fills = (shadow.get("ticks") or {}).get(s) or {}
        rows.append({
            "step": s, "day": s // C.DAY, "hour": s % C.DAY,
            "prices": {i: prices.get(i) for i in C.MX_ITEMS},
            "inv": {i: inv.get(i) for i in C.MX_ITEMS},
            "shed": {i: shed.get(i) for i in C.MX_ITEMS},
            "money": money,
            "our_sub": our_sub, "opp_sub": opp_sub,
            "fills": {pl: fills.get(pl) for pl in (0, 1)},
        })
    return rows


def day_rollup(ticks, our_seat):
    """按日汇总（fill 口径影子归因 + submit 口径 + 钱路径 Δ）。"""
    days = defaultdict(lambda: {"fill_val": defaultdict(float),
                                "fill_qty": defaultdict(float),
                                "sub_qty": defaultdict(float),
                                "opp_sub_qty": defaultdict(float),
                                "money_delta": 0.0, "n_ticks": 0})
    money_first = {}
    for r in ticks:
        d = int(r["day"])
        row = days[d]
        row["n_ticks"] += 1
        for o in (r["fills"].get(our_seat) or []):
            if o.get("type") == "SELL":
                row["fill_val"][str(o.get("item"))] += float(o.get("value")
                                                             or 0)
                row["fill_qty"][str(o.get("item"))] += float(o.get("filled")
                                                             or 0)
        for sub in r["our_sub"]:
            if sub["op"] == "SELL":
                row["sub_qty"][sub["item"]] += sub["qty"]
        for sub in r["opp_sub"]:
            if sub["op"] == "SELL":
                row["opp_sub_qty"][sub["item"]] += sub["qty"]
        if r["money"] is not None:
            if d not in money_first:
                money_first[d] = r["money"]
            row["money_last"] = r["money"]
    out = {}
    for d, row in sorted(days.items()):
        out[d] = {
            "fill_total": round(sum(row["fill_val"].values()), 2),
            "fill_by_item": {k: round(v, 2) for k, v in row["fill_val"].items()
                             if v},
            "fill_qty_by_item": {k: round(v, 1) for k, v in
                                 row["fill_qty"].items() if v},
            "sub_qty_by_item": {k: round(v, 1) for k, v in
                                row["sub_qty"].items() if v},
            "opp_sub_qty_by_item": {k: round(v, 1) for k, v in
                                    row["opp_sub_qty"].items() if v},
            "money_open": money_first.get(d),
            "money_close": row.get("money_last"),
        }
    return out


def mean_path(ticks_list, keys=("prices", "inv", "shed", "money")):
    """多局逐拍均值路径（focus 窗）。"""
    acc = defaultdict(lambda: defaultdict(list))
    for ticks in ticks_list:
        for r in ticks:
            s = r["step"]
            for item in C.MX_ITEMS:
                v = (r["prices"] or {}).get(item)
                if isinstance(v, (int, float)):
                    acc[s]["px_" + item].append(float(v))
                v = (r["inv"] or {}).get(item)
                if isinstance(v, (int, float)):
                    acc[s]["inv_" + item].append(float(v))
                v = (r["shed"] or {}).get(item)
                if isinstance(v, (int, float)):
                    acc[s]["shed_" + item].append(float(v))
            if isinstance(r["money"], (int, float)):
                acc[s]["money"].append(float(r["money"]))
    out = {}
    for s in sorted(acc):
        out[s] = {k: round(statistics.mean(v), 2) for k, v in
                  acc[s].items() if v}
    return out


def main():
    t_start = time.time()
    auth, auth_lite = cert_sim()
    ev = {
        "version": RECORD_VERSION,
        "experiment": "d25/26 单日凹陷根因定位：drop_half vs mpx 8 局 traced "
                      "同 seed 逐拍解剖 step 576-624（挂单量/成交价/触发门/"
                      "对手流/排水/库存形态）；判定门拦错 vs 半量放少 vs 产线"
                      "节奏（判决先行·不发射不提交）",
        "source": {
            "commands": ["python3 forensics_day2526.py"],
            "arms": {k: {"main": v, "sha256": __import__("hashlib").sha256(
                Path(v).read_bytes()).hexdigest()} for k, v in ARMS.items()},
            "corpus": {"traced_folds": C.LOSS_FOLDS,
                       "traced_spec": "26 败局前 8 fold，席位 j%2 轮转（8 局/"
                                      "臂，同 seed 配对）",
                       "auth_extra": NEUTRAL_SEEDS},
            "workers": 1,
            "caliber": {
                "money": "终局钱 farms[obs.player].money；逐拍钱差=obs.money Δ",
                "fill": "影子引擎逐拍归因（kgenv.replay_profile）",
                "submit": "挂单 qty×卖时市价口径另计",
                "window": "d25/26=step 576-624 右开；对照日 d24/d27"},
            "sim_auth": auth_lite,
        },
        "forensics": {},
    }
    flush_ev(ev)
    if not auth_lite.get("consistency_ok"):
        ev["forensics"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_ev(ev)
        print("ABORT", ev["forensics"], flush=True)
        return ev
    run_cfg = {"engine": "auto", "bridge": auth, "workers": 1}

    from orderbook_r40 import judge_r23 as j23
    opp_paths = [str(KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    units = []
    for j, seed in enumerate(C.LOSS_FOLDS):
        units.append({"seed": int(seed), "seat": j % 2,
                      "opp_path": opp_paths[j % len(opp_paths)],
                      "opponent": Path(opp_paths[j % len(opp_paths)]
                                       ).parent.name})

    runs = {}
    for arm, path in ARMS.items():
        print("run", arm, flush=True)
        runs[arm] = run_traced(arm, path, units, run_cfg)

    # ---- 逐拍解剖 + 逐日汇总 ----
    per_unit = []
    ticks_by_arm = {"drop_half": [], "mpx": []}
    days_by_arm = {"drop_half": [], "mpx": []}
    half_events = []
    for u in units:
        key = (int(u["seed"]), int(u["seat"]))
        rec = {"seed": key[0], "seat": key[1], "opponent": u["opponent"]}
        for arm in ARMS:
            g = runs[arm].get(key) or {}
            row = g.get("row") or {}
            shadow = C.shadow_ticks(g.get("sinks") or {}, key[0]) or {}
            ticks = tick_view(g.get("sinks") or {}, key[1], shadow,
                              FOCUS_STEPS)
            full_ticks = tick_view(g.get("sinks") or {}, key[1], shadow,
                                   range(480, 648))
            days = day_rollup(full_ticks, key[1])
            ticks_by_arm[arm].append(ticks)
            days_by_arm[arm].append(days)
            rec[arm] = {
                "margin": row.get("margin"),
                "terminal_money": (row.get("reads") or {}).get(
                    "terminal_money"),
                "u2_report": row.get("u2_report"),
                "u2_dec_focus": row.get("u2_dec_focus"),
                "s758": row.get("s758"),
                "day25": days.get(25), "day26": days.get(26),
                "day24": days.get(24), "day27": days.get(27),
                "stream_sha_our": row.get("stream_sha_our"),
            }
            if arm == "drop_half" and row.get("u2_dec_focus"):
                half_events.append({"seed": key[0], "seat": key[1],
                                    "dec": row["u2_dec_focus"],
                                    "half_fires": (row.get("u2_report") or {})
                                    .get("half_fires")})
        per_unit.append(rec)

    # ---- 跨臂 d25/26 钱差拆解 ----
    def _day_total(rec, arm, day, field):
        d = (rec.get(arm) or {}).get("day%d" % day) or {}
        return float(d.get(field) or 0.0)

    cross = {"d25_fill_delta": [], "d26_fill_delta": [],
             "d25_money_delta": [], "d26_money_delta": [],
             "d25_sub_delta": [], "d26_sub_delta": []}
    for rec in per_unit:
        for day in (25, 26):
            a = rec["drop_half"].get("day%d" % day) or {}
            b = rec["mpx"].get("day%d" % day) or {}
            cross["d%d_fill_delta" % day].append(
                float(a.get("fill_total") or 0) - float(b.get("fill_total")
                                                        or 0))
            ma, mb = a.get("money_close"), b.get("money_close")
            oa, ob = a.get("money_open"), b.get("money_open")
            if None not in (ma, mb, oa, ob):
                cross["d%d_money_delta" % day].append((ma - oa) - (mb - ob))
            sa = sum((a.get("sub_qty_by_item") or {}).values())
            sbq = sum((b.get("sub_qty_by_item") or {}).values())
            cross["d%d_sub_delta" % day].append(sa - sbq)

    cross_mean = {k: round(statistics.mean(v), 2) if v else None
                  for k, v in cross.items()}
    cross_detail = {k: [round(x, 2) for x in v] for k, v in cross.items()}

    # ---- 逐拍均值路径（focus）----
    paths = {arm: mean_path(ticks_by_arm[arm]) for arm in ARMS}

    # ---- 触发门行为聚合 ----
    fire_counts = {"drop_half": defaultdict(int), "mpx": {}}
    for rec in per_unit:
        u2r = rec["drop_half"].get("u2_report") or {}
        for k in ("gate_calls", "base_fires", "fires", "half_fires",
                  "gate_blocked", "post648_pass"):
            fire_counts["drop_half"][k] += int(u2r.get(k) or 0)
    focus_fires = defaultdict(lambda: defaultdict(int))
    for he in half_events:
        for d in he["dec"]:
            focus_fires[int(d[0])][str(d[1])] += 1

    # ---- 产线节奏核对（COW interval2 / SHEEP interval3）----
    prod = {
        "COW_MILK": "first_yield_day 8 + 2k → 8/10/…/24/26/28（购入相位 "
                    "+1d 则 25/27）",
        "SHEEP_WOOL": "first_yield_day 6 + 3k → 6/9/…/24/27（购入相位 +1d "
                      "→ 25，+2d → 26）",
        "note": "d25/26 恰为 MILK/WOOL 第 N 周期落点（按购入相位）；解剖表核 "
                "shed/inv 逐拍是否有产出跳变",
    }

    ev["forensics"] = {
        "method": "8 局 traced 同 seed 双臂（drop_half vs mpx）；影子引擎逐拍"
                  "归因；解剖窗 step 576-624；对照日 24/27",
        "per_unit": per_unit,
        "cross_arm": {"mean": cross_mean, "detail": cross_detail},
        "day_stats_traced": {
            arm: {"d25_fill_mean": round(statistics.mean(
                [ (d.get(25) or {}).get("fill_total") or 0 for d in days ]),
                1), "d26_fill_mean": round(statistics.mean(
                [ (d.get(26) or {}).get("fill_total") or 0 for d in days ]),
                1), "d24_fill_mean": round(statistics.mean(
                [ (d.get(24) or {}).get("fill_total") or 0 for d in days ]),
                1), "d27_fill_mean": round(statistics.mean(
                [ (d.get(27) or {}).get("fill_total") or 0 for d in days ]),
                1)}
            for arm, days in days_by_arm.items()},
        "focus_mean_paths": {arm: {str(s): v for s, v in
                                   sorted(p.items()) if 570 <= s < 630}
                             for arm, p in paths.items()},
        "gate_behavior": {"drop_half_totals": dict(fire_counts["drop_half"]),
                          "focus_fires_by_step": {str(s): dict(v) for s, v in
                                                  sorted(focus_fires.items())}},
        "production_rhythm": prod,
        "elapsed_s": round(time.time() - t_start, 1),
    }
    flush_ev(ev)
    # 账本
    (C.EVID_DIR / "forensics_day2526_ledger.json").write_text(
        json.dumps({"per_unit": per_unit, "cross": cross_detail,
                    "generated": C.now()}, ensure_ascii=False, indent=1,
                   default=str) + "\n", encoding="utf-8")
    print("cross mean:", json.dumps(cross_mean, ensure_ascii=False),
          flush=True)
    print("done", ev["forensics"]["elapsed_s"], flush=True)
    return ev


if __name__ == "__main__":
    main()
