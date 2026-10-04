# -*- coding: utf-8 -*-
"""phase_a —— R14 Phase A：全量回放逐日归因（surge 日全景测绘）。

口径（沿 volume_price_decomp.py / audit_r32r33.py，全量沿用其解析方式）：
  - 净收入 = money_delta + seed 支出 + BUY_PRODUCT 支出（R14 在 decomp 的
    money_delta+seed 之上按需求补 BUY_PRODUCT 加回）；
  - 成交量 = 库存背书口径：仅在"该席该步提交过该品项 SELL"的转移上取
    tot_inv（shed+携带 inventories）正差（提交量≠成交量修正；产出/消耗的
    小污染沿 decomp 方法注记）；
  - 转移约定：steps[t] 记录的 action 驱动 t-1→t（twin.replay_transition_actions
    同源）；day d 窗口 = 转移 t∈[max(1,d*24), min(d*24+23, n-1)]，
    day_end_money = steps[d*24+23]（audit day_end_money 口径）；
  - sellable（当日可卖库存估计）= 当日成交量 + 当日末持有
    （= 期初+产出-消耗+买入 的恒等近似，涵盖当日可收）；
  - surge 日定桩：净日差 = 对手日净收入−我方日净收入 ≥ 阈值(1500) 且
    对手当日收入 ≥ 其全程日收入中位数 ×1.5（参数化；附 1000/1500/2000 三档）；
  - 逐 surge 日构成分解（量差/mix 差/价差/结构性库存差 + 覆盖 + 不可处置
    标注[结构性占比≥70% 或覆盖<30%] + 价格可识别性分位）。

席位定向：daily_netflow_decompose 产出双席逐日表；mark_surge_days/
classify_surge_composition 按定向（my_seat）消费——Phase B 双席位各取
"我方=该席位"的定向（'our'=renyxin 原席 / 'other'=对席）。
"""
from __future__ import annotations

import json
import os
import statistics as st

from . import corpus as _corpus

SEED_VALUE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
              "STRAWBERRY": 100, "MELON": 80}

# 报告标注深描集（需求钉死）：r33 六 late-fade + 两 mid-collapse。
DEEP_DIVE_IDS = (112831515, 112835052, 112835161, 112844429, 112851433,
                 112856307, 112843277, 112843266)

DEFAULT_THRESHOLD = 1500.0
DEFAULT_MEDIAN_MULT = 1.5
SENSITIVITY_THRESHOLDS = (1000.0, 1500.0, 2000.0)
STRUCTURAL_SHARE_MAX = 0.70     # 不可处置：结构性库存差占净差比 ≥70%
COVERAGE_MIN = 0.30             # 不可处置：同品类覆盖 <30%


def _jl(x):
    return json.loads(x) if isinstance(x, str) else x


def tot_inv(priv):
    """私有态 → {item: qty}（shed + 携带 inventories 求和，零值剔除）。"""
    priv = _jl(priv) if priv else {}
    s = dict(priv.get("shed") or {})
    for inv in (priv.get("inventories") or []):
        for k, v in (inv or {}).items():
            s[k] = s.get(k, 0) + v
    return {k: v for k, v in s.items() if v}


def _seat_row():
    return {"net": 0.0, "spend_seed": 0.0, "spend_product": 0.0,
            "vol_by_item": {}, "dropval": 0.0, "dropval_by_item": {},
            "inv_start": {}, "inv_end": {}}


def daily_netflow_decompose(replay):
    """单局逐日双席分解。

    输入：回放 dict（完整 /tmp/r33audit 形态）。输出：
      {"our_seat", "names", "episode", "days": [{d, px_mean, seats: {"0": row,
      "1": row}, my, opp}]}——my/opp 为 renyxin 定向视图（Phase B 用 seats
      原始面自组对席定向）。row = {net, vol_by_item, vol_total, avgpx,
      sellable, inv_start, inv_end, spend_seed, spend_product, dropval}。
    解析异常向上抛（phase_a_attribution 折成该局 error，不中断全量）。
    """
    info = replay.get("info") or {}
    names = info.get("TeamNames") or replay.get("teams") or []
    if _corpus.TEAM_NAME not in names:
        raise ValueError(f"TeamNames 无 {_corpus.TEAM_NAME!r}: {names!r}")
    our_seat = names.index(_corpus.TEAM_NAME)
    steps = replay.get("steps") or []
    if not steps:
        raise ValueError("回放无 steps")
    n = len(steps)

    def obs(si, who):
        return (steps[si][who] or {}).get("observation") or {}

    # 观测解析缓存（farms/private 均为大 JSON 串，逐日资金/库存读取复用）
    _money_cache = {}
    _inv_cache = {}

    def money(si, who):
        key = (si, who)
        if key not in _money_cache:
            _money_cache[key] = float(
                _jl(obs(si, who).get("farms"))[who]["money"])
        return _money_cache[key]

    def inv(si, who):
        key = (si, who)
        if key not in _inv_cache:
            _inv_cache[key] = tot_inv(obs(si, who).get("private"))
        return _inv_cache[key]

    n_days = (min(n - 1, 29 * 24 + 23) + 24) // 24  # 头起的完整记录日数
    days = []
    for d in range(n_days):
        t_lo, t_hi = max(1, d * 24), min(d * 24 + 23, n - 1)
        si_start = max(0, d * 24 - 1) if d > 0 else 0
        si_end = min(d * 24 + 23, n - 1)
        rows = {0: _seat_row(), 1: _seat_row()}
        px_sum, px_n = {}, 0
        for t in range(t_lo, t_hi + 1):
            prices = (_jl(obs(t - 1, 0).get("market")) or {}).get("prices") or {}
            for item, p in prices.items():
                px_sum[item] = px_sum.get(item, 0.0) + float(p)
            px_n += 1
            for who in (0, 1):
                row = rows[who]
                act = (steps[t][who] or {}).get("action") or {}
                if not isinstance(act, dict):
                    act = {}
                sold_items = set()
                for m in (act.get("market") or []):
                    if not (isinstance(m, list) and len(m) >= 3):
                        continue
                    if m[0] == "SELL":
                        sold_items.add(m[1])
                    elif m[0] == "BUY_SEED":
                        row["spend_seed"] += m[2] * SEED_VALUE.get(m[1], 0)
                    elif m[0] == "BUY_PRODUCT":
                        row["spend_product"] += m[2] * prices.get(m[1], 0)
                if not sold_items:
                    continue
                ib = inv(t - 1, who)
                ia = inv(t, who)
                for item in sold_items:
                    drop = ib.get(item, 0) - ia.get(item, 0)
                    if drop > 0:
                        row["vol_by_item"][item] = (
                            row["vol_by_item"].get(item, 0) + drop)
                        row["dropval"] += drop * prices.get(item, 0)
                        row["dropval_by_item"][item] = (
                            row["dropval_by_item"].get(item, 0.0)
                            + drop * prices.get(item, 0))
        px_mean = {k: round(v / px_n, 2) for k, v in px_sum.items()} if px_n else {}
        day = {"d": d, "px_mean": px_mean, "seats": {}}
        for who in (0, 1):
            row = rows[who]
            net = (money(si_end, who) - money(si_start, who)) \
                + row["spend_seed"] + row["spend_product"]
            inv_start = inv(si_start, who)
            inv_end = inv(si_end, who)
            vol_total = sum(row["vol_by_item"].values())
            row.update({
                "net": round(net, 1),
                "vol_total": vol_total,
                "avgpx": round(row["dropval"] / vol_total, 3) if vol_total else None,
                "inv_start": inv_start, "inv_end": inv_end,
                "sellable": vol_total + sum(inv_end.values()),
            })
            day["seats"][str(who)] = row
        day["my"], day["opp"] = day["seats"][str(our_seat)], day["seats"][str(1 - our_seat)]
        days.append(day)
    return {"episode": info.get("EpisodeId") or replay.get("episode_id"),
            "names": names, "our_seat": our_seat, "days": days}


def mark_surge_days(decomp, my_seat=None, threshold=DEFAULT_THRESHOLD,
                    median_mult=DEFAULT_MEDIAN_MULT):
    """surge 日标注（参数化，缺数据日跳过）。

    输入：daily_netflow_decompose 产物 + 定向席位（缺省 renyxin 原席）。
    输出：{"surge_days": [d], "sensitivity": {"th1000": [...], ...},
    "threshold", "median_mult", "opp_net_median"}。
    """
    if my_seat is None:
        my_seat = decomp["our_seat"]
    days = decomp["days"]
    opp_nets = [day["seats"][str(1 - my_seat)]["net"] for day in days]
    med = st.median(opp_nets) if opp_nets else 0.0

    def _mark(th):
        out = []
        for day in days:
            my, opp = day["seats"][str(my_seat)], day["seats"][str(1 - my_seat)]
            gap = opp["net"] - my["net"]
            if gap >= th and opp["net"] >= median_mult * med:
                out.append(day["d"])
        return out

    return {"surge_days": _mark(threshold),
            "sensitivity": {f"th{int(th)}": _mark(th)
                            for th in SENSITIVITY_THRESHOLDS},
            "threshold": threshold, "median_mult": median_mult,
            "opp_net_median": med}


def classify_surge_composition(decomp, day_d, my_seat=None,
                               price_series=None):
    """单 surge 日构成分解（分解失败记 None 不中断）。

    输入：decomp 产物 + 日序号 + 定向席位 + price_series（品项→全程逐日
    均价序列，价格可识别性分位用；缺省从 decomp 自取）。
    输出：{quant_gap, mix_gap, px_gap, structural_gap, structural_share,
    coverage, treatable, price_percentile, opp_short_rate, net_gap,
    dropval_gap}。恒等式：dropval_gap = quant_gap + mix_gap + px_gap
    （对手多卖收入按 我方价×量差 / 对手 mix 价值差 / 同品项价差×对手量 三分）。
    """
    if my_seat is None:
        my_seat = decomp["our_seat"]
    days = decomp["days"]
    if price_series is None:
        price_series = {}
        for day in days:
            for item, p in day["px_mean"].items():
                price_series.setdefault(item, []).append(p)
    day = next((x for x in days if x["d"] == day_d), None)
    if day is None:
        return None
    my = day["seats"][str(my_seat)]
    opp = day["seats"][str(1 - my_seat)]
    px_mean = day["px_mean"]

    qm, qo = my["vol_by_item"], opp["vol_by_item"]
    Qm, Qo = my["vol_total"], opp["vol_total"]
    Rm, Ro = my["dropval"], opp["dropval"]
    items = set(qm) | set(qo)
    # 我方整体均价作量差价基（decomp 同口径 avgpx）；品项价基=该席该品项
    # 实现均价（dropval_by_item/vol_by_item，捕捉日内时点差），未卖品项回退
    # 当日均价、再回退 pbar_m（mix/结构性项需要共同价基）。
    pbar_m = (Rm / Qm) if Qm else (Ro / Qo if Qo else 0.0)

    def _px_item(row, item):
        v = row["vol_by_item"].get(item, 0)
        if v > 0:
            return row["dropval_by_item"].get(item, 0.0) / v
        return px_mean.get(item, pbar_m)

    pm_item = {i: _px_item(my, i) for i in items}
    po_item = {i: _px_item(opp, i) for i in items}

    # ① 量差：总量差 × 我方整体均价
    quant_gap = (Qo - Qm) * pbar_m
    # ② mix 差：对手品类结构（按我方价基估值）相对我方整体均价的结构溢价
    if Qo > 0:
        opp_mix_val = sum(qo[i] * pm_item[i] for i in qo) / Qo
    else:
        opp_mix_val = pbar_m
    mix_gap = Qo * (opp_mix_val - pbar_m)
    # ③ 价差：同品项实现均价差 × 对手量（双席共享价格序列 → 该项捕捉的
    # 是日内卖出时点差；我方未卖品项回退当日均价）
    px_gap = sum(qo[i] * (po_item[i] - pm_item[i]) for i in qo)

    # ④ 结构性库存差：对手当日多卖品项（q_o>q_m）中我方当日可卖覆盖不了的部分
    my_avail = {i: my["vol_by_item"].get(i, 0)
                + my["inv_end"].get(i, 0) for i in items}
    outsell = {i for i in items if qo.get(i, 0) > qm.get(i, 0)}
    structural_gap = sum(max(0.0, qo[i] - my_avail.get(i, 0)) * pm_item[i]
                         for i in outsell)
    denom_cov = sum(qo[i] for i in outsell)
    coverage = (sum(min(my_avail.get(i, 0), qo[i]) for i in outsell) / denom_cov
                if denom_cov > 0 else None)

    net_gap = opp["net"] - my["net"]
    dropval_gap = Ro - Rm
    structural_share = (structural_gap / dropval_gap) if dropval_gap > 1e-9 else 0.0
    treatable = not (structural_share >= STRUCTURAL_SHARE_MAX
                     or (coverage is not None and coverage < COVERAGE_MIN))

    # 价格可识别性：surge 日品项价在该品项全程价的分位（在线识别存在性证据）
    pct = {}
    for i in qo:
        series = price_series.get(i) or []
        if len(series) < 2:
            continue
        v = px_mean.get(i)
        below = sum(1 for x in series if x <= v)
        pct[i] = round(100.0 * below / len(series), 1)
    # 对手当日卖空率（A1 处置参数）：成交/(成交+日末持有)
    opp_sellable = opp["sellable"]
    opp_short_rate = (opp["vol_total"] / opp_sellable
                      if opp_sellable > 0 else 0.0)

    return {"quant_gap": round(quant_gap, 1), "mix_gap": round(mix_gap, 1),
            "px_gap": round(px_gap, 1),
            "structural_gap": round(structural_gap, 1),
            "structural_share": round(structural_share, 3),
            "coverage": round(coverage, 3) if coverage is not None else None,
            "treatable": bool(treatable),
            "price_percentile": pct,
            "opp_short_rate": round(min(1.0, max(0.0, opp_short_rate)), 3),
            "net_gap": round(net_gap, 1), "dropval_gap": round(dropval_gap, 1),
            "my_vol": Qm, "opp_vol": Qo}


def phase_a_attribution(replay_entries, threshold=DEFAULT_THRESHOLD,
                        median_mult=DEFAULT_MEDIAN_MULT,
                        deep_ids=DEEP_DIVE_IDS):
    """全量归因编排：逐局 decompose → mark → classify（双定向）→ 全景汇总。

    输入：corpus_select()['phase_a'] 条目列表（episode/path）。输出报告：
      {per_game, panorama, sensitivity, deep_dive, method_notes, errors}。
    单局解析失败记录不中断（error 面）；treatable=renyxin 定向含可处置
    surge 日；orientations 双定向供 Phase B 双席位取用。
    """
    per_game, errors = [], []
    comp_acc, px_pct_acc = [], []
    surge_day_hist, treatable_games, any_surge_games = {}, 0, 0
    n_treatable_surge_days = 0
    for entry in replay_entries:
        ep = entry.get("episode")
        rec = {"episode": ep, "tag": entry.get("tag"), "path": entry.get("path")}
        try:
            replay = _corpus.load_replay(entry["path"])
            lab = _corpus.game_label(replay)
            if lab.get("error"):
                raise ValueError(lab["error"])
            rec.update({k: lab[k] for k in ("seat", "opp", "res", "margin")})
            decomp = daily_netflow_decompose(replay)
            price_series = {}
            for day in decomp["days"]:
                for item, p in day["px_mean"].items():
                    price_series.setdefault(item, []).append(p)
            orientations = {}
            for oname, seat in (("our", decomp["our_seat"]),
                                ("other", 1 - decomp["our_seat"])):
                marked = mark_surge_days(decomp, seat, threshold, median_mult)
                comps = {}
                for d in marked["surge_days"]:
                    comp = classify_surge_composition(decomp, d, seat,
                                                      price_series)
                    if comp is not None:
                        comps[str(d)] = comp
                orientations[oname] = {
                    "my_seat": seat, "surge_days": marked["surge_days"],
                    "sensitivity": marked["sensitivity"],
                    "opp_net_median": round(marked["opp_net_median"], 1),
                    "composition": comps}
            rec["orientations"] = orientations
            ours = orientations["our"]
            rec["surge_days"] = ours["surge_days"]
            rec["surge_sensitivity"] = ours["sensitivity"]
            treat_days = [d for d, c in ours["composition"].items()
                          if c["treatable"]]
            rec["treatable_surge_days"] = [int(d) for d in treat_days]
            rec["treatable"] = bool(treat_days)
            rec["error"] = None
            # 全景累计（renyxin 定向）
            if ours["surge_days"]:
                any_surge_games += 1
            if rec["treatable"]:
                treatable_games += 1
            n_treatable_surge_days += len(treat_days)
            for d, c in ours["composition"].items():
                surge_day_hist[d] = surge_day_hist.get(d, 0) + 1
                comp_acc.append(c)
                px_pct_acc.extend(c["price_percentile"].values())
        except Exception as exc:  # 单局失败=该局 error，不中断全量
            rec["error"] = f"{type(exc).__name__}: {exc}"
            errors.append({"episode": ep, "error": rec["error"]})
        per_game.append(rec)

    n_ok = [g for g in per_game if not g.get("error")]
    n_surge_days = sum(len(g.get("surge_days") or []) for g in n_ok)
    losses = [g for g in n_ok if g.get("res") == "L"]
    panorama = {
        "n_games": len(per_game), "n_ok": len(n_ok), "n_errors": len(errors),
        "res_counts": {r: sum(1 for g in n_ok if g.get("res") == r)
                       for r in ("W", "L", "T")},
        "n_games_with_surge": any_surge_games,
        "n_games_treatable": treatable_games,
        "n_treatable_losses": sum(1 for g in losses if g.get("treatable")),
        "n_surge_days_total": n_surge_days,
        "n_treatable_surge_days": n_treatable_surge_days,
        "surge_day_histogram": {str(k): v for k, v in sorted(
            surge_day_hist.items(), key=lambda kv: int(kv[0]))},
        "composition_means": _mean_comp(comp_acc),
        "price_identifiability": {
            "n_items_scored": len(px_pct_acc),
            "mean_percentile": round(sum(px_pct_acc) / len(px_pct_acc), 1)
            if px_pct_acc else None,
            "frac_ge_70pct": round(sum(1 for v in px_pct_acc if v >= 70)
                                   / len(px_pct_acc), 3) if px_pct_acc else None,
        },
    }
    deep = [g for g in per_game if g.get("episode") in set(deep_ids)]
    return {"per_game": per_game, "panorama": panorama, "errors": errors,
            "deep_dive": deep, "threshold": threshold,
            "median_mult": median_mult, "deep_ids": list(deep_ids),
            "method_notes": [
                "净收入=money_delta+seed+BUY_PRODUCT 支出（audit/decomp 口径扩展）",
                "成交量=库存背书口径（提交量≠成交量修正；产出/消耗小污染沿 decomp 注记）",
                "day_end=step d*24+23（audit 口径）；转移 t 驱动 t-1→t",
                "sellable=当日成交+日末持有（=期初+产出-消耗+买入 恒等近似，涵盖当日可收）",
                "构成分解价基：品项实现均价（该席该品项 dropval/vol；未卖回退当日均价）；价差项捕捉日内时点差",
                "结构性占比分母=dropval_gap（对手多卖收入差）",
                "对手卖空率=成交/(成交+日末持有)（A1 处置参数同源定义）",
            ]}


def _mean_comp(comps):
    if not comps:
        return None
    keys = ("quant_gap", "mix_gap", "px_gap", "structural_gap",
            "structural_share")
    out = {k: round(sum(c[k] for c in comps) / len(comps), 1) for k in keys}
    covs = [c["coverage"] for c in comps if c["coverage"] is not None]
    out["coverage_mean"] = round(sum(covs) / len(covs), 3) if covs else None
    out["n"] = len(comps)
    return out
