# 【中文】round24_loss_forensics.py —— round-24 败局法证（Track-B DTSP v2，只读探针）
# ===========================================================================
# 用途（round-24 v3 证据链任务包）：
#   1) 26 官方局（13W-13L）逐局台账：三败带（碾压/压制/近失）+ 对手结构画像；
#   2) 9 深挖局（碾压带 4 + 压制带 5）逐日时间线：对手 ≥85k 的结构路径
#      （起量日/依赖产品线/象限数/畜群规模/外购饲料）+ 我方同期对照 +
#      差距拉开第一个分叉日（divergence start，含持续门）；
#   3) 大赢局对称性检查：对手 17-57k 是"弱"还是"被我方挤压"——
#      判别器 = 对手产能相近时其主产品线成交量/实现价在胜局 vs 败局的系统差。
#      口径修正（2026-09-19）：收入/均价/市占一律用 state-diff 实测成交
#      （kgenv.replay_profile.extract_success_metrics 的 per_item filled_qty/value），
#      不用"请求量×日终价"（实测会数倍虚高，如 ep110695554 Felipe 请求 1998
#      成交 79）。
# 输入：exports/probes/planner_bench/round24_deep_stats.json（现役 25 局）+
#       exports/probes/round24_forensics/round24_deep_stats_missing2.json
#       （110790899/110841464 本探针预生成）+
#       references/data/online-replays/round24/episode-*.json（27 份，含 1 镜像）。
# 输出：exports/probes/round24_forensics/*.json（gitignored 中间数据）+ stdout。
# 只读：不改 src/planner/现役 scripts。stdlib-only、离线、确定性。
# ===========================================================================

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
sys.path.insert(0, SOFTWARE)
from kgenv.replay_profile import extract_success_metrics   # noqa: E402

ROOT = os.path.dirname(SOFTWARE)
REPLAY_DIR = os.path.join(ROOT, "references", "data", "online-replays",
                          "round24")
OUT_DIR = os.path.join(SOFTWARE, "exports", "probes", "round24_forensics")
TEAM = "renyxin"
CROPS = ("STRAWBERRY", "WHEAT", "MELON", "CARROT", "TOMATO")
ANIMAL_PRODUCTS = ("MILK", "WOOL", "EGG")
CROP_PRODUCTS = ("STRAWBERRY", "MELON", "WHEAT", "CARROT", "TOMATO")
SELLABLE = CROP_PRODUCTS + ANIMAL_PRODUCTS + ("FERTILIZER",)

# 协调者解构钉死的 9 深挖局与三带归属（round-24 26 局 13W-13L）
CRUSHED = (110687913, 110677576, 110684532, 110694473)      # 对手 ≥86k，差 ≥22k
SUPPRESSED = (110702221, 110699710, 110685617, 110841464,
              110701172)                                     # 对手 85-92k
NEAR_LOSS = (110678765, 110679941, 110741693, 110689244)     # -363 ~ -10.6k
TARGET9 = CRUSHED + SUPPRESSED
FORK_G0 = 2000      # 分叉日主门：gap(opp-me) ≥ 2000
FORK_G1 = 1000      # 持续门：此后任意日 gap 不再跌破 1000


def load_json(path):
    with open(path, "r", encoding="utf-8") as h:
        return json.load(h)


def merged_deep_stats():
    stats = load_json(os.path.join(SOFTWARE, "exports", "probes",
                                   "planner_bench", "round24_deep_stats.json"))
    stats += load_json(os.path.join(OUT_DIR,
                                    "round24_deep_stats_missing2.json"))
    return stats


def official_games(deep_stats):
    out = []
    for e in sorted(deep_stats, key=lambda x: x["episode_id"]):
        teams = e["teams"]
        if teams[0] == teams[1]:
            continue
        me = 0 if teams[0] == TEAM else 1
        out.append({"episode": e["episode_id"], "me": me,
                    "opp": e["players"][1 - me], "mine": e["players"][me]})
    return out


def day_table(p):
    return {r["day"]: r for r in p["table"]}


def curve(p):
    return [r.get("money_end") or 0.0 for r in
            sorted(p["table"], key=lambda r: r["day"])]


def plants_total(p):
    tot = defaultdict(float)
    for r in p["table"]:
        for k, v in (r.get("plants") or {}).items():
            tot[k] += float(v)
    return dict(tot)


def fills_by_seat(replay):
    """state-diff 实测成交：{seat: {item: {filled_qty, value, avg_price,
    requested_qty}}}（SELL 方向；取自 extract_success_metrics）。"""
    s = extract_success_metrics(replay, strict=False)
    out = {}
    for p in s["players"]:
        per = (p["market"]["SELL"].get("per_item") or {})
        out[p["seat"]] = {
            item: {"filled_qty": v.get("filled_qty", 0),
                   "value": round(v.get("value", 0.0), 1),
                   "avg_price": v.get("avg_price"),
                   "requested_qty": v.get("requested_qty", 0)}
            for item, v in per.items()}
    return out


def revenue_by_line(fills_seat):
    rev = {k: v["value"] for k, v in fills_seat.items() if v["value"] > 0}
    animal = sum(rev.get(k, 0.0) for k in ANIMAL_PRODUCTS)
    crop = sum(rev.get(k, 0.0) for k in CROP_PRODUCTS)
    fert = rev.get("FERTILIZER", 0.0)
    tot = animal + crop + fert
    return {"rev": rev, "rev_total": tot,
            "animal_share": animal / tot if tot else 0.0,
            "crop_share": crop / tot if tot else 0.0,
            "fert_share": fert / tot if tot else 0.0}


def first_revenue_day(p, product, threshold=100.0):
    for r in sorted(p["table"], key=lambda r: r["day"]):
        if float((r.get("sells_revenue") or {}).get(product, 0.0)) >= threshold:
            return r["day"]
    return None


def ramp_days(p, levels=(5000, 20000, 50000)):
    """起量节奏：资金首次到达各档位的日数。"""
    out = {}
    for lv in levels:
        hit = None
        for r in sorted(p["table"], key=lambda r: r["day"]):
            if (r.get("money_end") or 0.0) >= lv:
                hit = r["day"]
                break
        out[f"m{lv//1000}k_day"] = hit
    return out


def struct_profile(p, fills=None):
    """结构画像：产能（种植格/畜群/象限）、收入线（实测成交）、外购饲料。"""
    plants = plants_total(p)
    fills = fills or {}
    rev = revenue_by_line(fills)
    quads = p.get("quadrant_unlock_day") or {}
    top_lines = sorted(rev["rev"].items(), key=lambda x: -x[1])[:4]
    return {
        "final": round(p["reward"]),
        "d12": round(p["money"]["day12"] or 0),
        "d24": round(p["money"]["day24"] or 0),
        "ramp_d12_d24": round(p["money"]["ramp_d12_d24"] or 0),
        "plants": {k: int(v) for k, v in sorted(plants.items(),
                                                key=lambda x: -x[1])},
        "plant_total": int(sum(plants.values())),
        "peak_herd": p.get("peak_herd"),
        "peak_head": int(p.get("peak_herd_head") or 0),
        "quads": quads,
        "n_quad_beyond_nw": len([q for q in quads if q != "NW"]),
        "feed_buy_qty": p["totals"]["feed_buy_qty"],
        "feed_buy_spend": round(p["totals"]["feed_buy_spend"]),
        "rev_total": round(rev["rev_total"]),
        "rev_animal_share": round(rev["animal_share"], 3),
        "top_lines": [(k, round(v)) for k, v in top_lines],
    }


def divergence_start(gap, g0=FORK_G0, g1=FORK_G1):
    """差距拉开第一个分叉日：最小 d 使 gap(d)≥g0 且此后每日 gap≥g1。

    返回 None 表示全程无持续拉开（近失带常见）。"""
    n = len(gap)
    for d in range(n):
        if gap[d] < g0:
            continue
        tail = gap[d:]
        if tail and min(tail) >= g1:
            return d
    return None


def market_price_paths(replay):
    steps = replay["steps"]
    prices_by_day = {}
    for t, step in enumerate(steps):
        entry = step[0] if isinstance(step, list) else step.get("0")
        obs = (entry or {}).get("observation") or {}
        day = obs.get("day", t // 24)
        mkt = obs.get("market") or {}
        if mkt.get("prices"):
            prices_by_day[day] = dict(mkt["prices"])
    return prices_by_day


def actions_by_day(replay, seat):
    """逐日动作摘要：BUY_ANIMAL 明细 / 卖出品类 / HIRE 次数。"""
    steps = replay["steps"]
    acts = defaultdict(lambda: {"buy_animal": [], "sell_kinds": defaultdict(int),
                                "hire": 0})
    for t in range(0, len(steps) - 1):
        entry = steps[t + 1][seat] if isinstance(steps[t + 1], list) \
            else steps[t + 1].get(str(seat))
        action = (entry or {}).get("action") or {}
        day = t // 24
        rec = acts[day]
        for order in action.get("market") or []:
            if not isinstance(order, list) or not order:
                continue
            op = order[0]
            if op == "BUY_ANIMAL" and len(order) >= 3:
                rec["buy_animal"].append((order[1], int(order[2])))
            elif op == "SELL" and len(order) >= 3:
                rec["sell_kinds"][order[1]] += int(order[2])
            elif op == "HIRE":
                rec["hire"] += 1
    return acts


def realized_price(fills_seat, product):
    f = fills_seat.get(product)
    if not f or (f.get("filled_qty") or 0) < 10:
        return None
    return f.get("avg_price")


def shared_lines(fills_m, fills_o, min_qty=40):
    """双方都实质成交过的产品（各 ≥min_qty 件，实测口径）。"""
    shared = []
    for k in SELLABLE:
        qm = (fills_m.get(k) or {}).get("filled_qty", 0)
        qo = (fills_o.get(k) or {}).get("filled_qty", 0)
        if qm >= min_qty and qo >= min_qty:
            shared.append(k)
    return shared


def game_row(g, fills_m, fills_o):
    mine, opp = g["mine"], g["opp"]
    margin = mine["reward"] - opp["reward"]
    if margin > 0:
        band = "W"
    elif g["episode"] in CRUSHED:
        band = "L-crushed"
    elif g["episode"] in SUPPRESSED:
        band = "L-suppressed"
    elif g["episode"] in NEAR_LOSS:
        band = "L-near"
    else:
        band = "L-other"
    return {
        "episode": g["episode"], "opponent": opp["team"], "me_seat": g["me"],
        "margin": round(margin), "result": "W" if margin > 0 else "L",
        "band": band,
        "me": struct_profile(mine, fills_m), "opp": struct_profile(opp, fills_o),
    }


def fork_timeline(g, replay, prices, fills_m, fills_o):
    """深挖局逐日对照 + 分叉日 + 双方结构路径。"""
    mine, opp = g["mine"], g["opp"]
    tm, to = day_table(mine), day_table(opp)
    cm, co = curve(mine), curve(opp)
    gap = [round(co[d] - cm[d]) for d in range(30)]
    fork = divergence_start(gap)
    acts_m = actions_by_day(replay, g["me"])
    acts_o = actions_by_day(replay, 1 - g["me"])
    timeline = []
    for d in range(30):
        rm, ro = tm.get(d, {}), to.get(d, {})
        timeline.append({
            "day": d,
            "me_money": rm.get("money_end"), "opp_money": ro.get("money_end"),
            "gap": gap[d],
            "me_herd": rm.get("herd"), "opp_herd": ro.get("herd"),
            "me_crops": rm.get("crops"), "opp_crops": ro.get("crops"),
            "me_plants": rm.get("plants"), "opp_plants": ro.get("plants"),
            "me_animal_buys": rm.get("animal_buys"),
            "opp_animal_buys": ro.get("animal_buys"),
            "me_sells": rm.get("sells_qty"), "opp_sells": ro.get("sells_qty"),
            "me_rev": rm.get("sells_revenue"),
            "opp_rev": ro.get("sells_revenue"),
            "me_hire": acts_m[d]["hire"], "opp_hire": acts_o[d]["hire"],
            "prices": prices.get(d),
        })
    return {
        "episode": g["episode"], "opponent": opp["team"],
        "me_seat": g["me"], "margin": round(mine["reward"] - opp["reward"]),
        "band": ("crushed" if g["episode"] in CRUSHED else "suppressed"),
        "fork_day": fork,
        "gap_by_day": gap,
        "me_profile": struct_profile(mine, fills_m),
        "opp_profile": struct_profile(opp, fills_o),
        "opp_line_starts": {k: first_revenue_day(opp, k)
                            for k in ANIMAL_PRODUCTS + CROPS},
        "me_line_starts": {k: first_revenue_day(mine, k)
                           for k in ANIMAL_PRODUCTS + CROPS},
        "opp_ramp": ramp_days(opp), "me_ramp": ramp_days(mine),
        "timeline": timeline,
    }


def win_symmetry(rows, game_map, fills_map, prices_cache):
    """大赢局对称性：对手产能相近却收入塌 → 挤压证据；产能塌 → 对手弱。

    判别指标（实测成交口径）：
      - opp 主产品线成交量/实现价 vs 9 败局同产品线基准；
      - 我方在同产品线成交占比（market share）；
      - opp 产能（plant_total + peak_head）与收入效率（rev/产能格）。"""
    wins = [r for r in rows if r["result"] == "W"]
    big_wins = [r for r in wins if r["opp"]["final"] < 57000]
    # 9 败局对手主产品线实现价基准（MILK/WOOL/STRAWBERRY…）
    base_price = defaultdict(list)
    for r in rows:
        if r["result"] != "L":
            continue
        for line, val in r["opp"]["top_lines"]:
            fp = realized_price(fills_map[(r["episode"], 1 - r["me_seat"])],
                                line) if False else None
        # 逐产品（不只 top1）基准
    for g in game_map.values():
        pass
    out = []
    for r in big_wins:
        ep = r["episode"]
        g = game_map[ep]
        fm = fills_map[(ep, g["me"])]
        fo = fills_map[(ep, 1 - g["me"])]
        prices = prices_cache[ep]
        opp_top = r["opp"]["top_lines"][0][0] if r["opp"]["top_lines"] else None
        rec = {
            "episode": ep, "opponent": r["opponent"],
            "margin": r["margin"],
            "opp_final": r["opp"]["final"], "opp_d12": r["opp"]["d12"],
            "opp_d24": r["opp"]["d24"],
            "opp_plant_total": r["opp"]["plant_total"],
            "opp_peak_head": r["opp"]["peak_head"],
            "opp_rev_total": r["opp"]["rev_total"],
            "opp_top_line": opp_top,
            "opp_top_rev": r["opp"]["top_lines"][0][1],
            "opp_top_filled": (fo.get(opp_top) or {}).get("filled_qty"),
            "opp_top_realized_price": realized_price(fo, opp_top)
            if opp_top else None,
            "me_realized_price_same": realized_price(fm, opp_top)
            if opp_top else None,
            "shared_lines": shared_lines(fm, fo),
        }
        if opp_top:
            qm = (fm.get(opp_top) or {}).get("filled_qty", 0)
            qo = (fo.get(opp_top) or {}).get("filled_qty", 0)
            if qm + qo > 0:
                rec["me_market_share_top"] = round(qm / (qm + qo), 3)
            pp = prices
            early = [pp[d].get(opp_top) for d in range(8, 16)
                     if pp.get(d, {}).get(opp_top) is not None]
            late = [pp[d].get(opp_top) for d in range(16, 26)
                    if pp.get(d, {}).get(opp_top) is not None]
            rec["prices_top_early_late"] = (
                round(sum(early) / len(early), 1) if early else None,
                round(sum(late) / len(late), 1) if late else None)
        cap = r["opp"]["plant_total"] + r["opp"]["peak_head"]
        rec["opp_rev_per_cap"] = round(r["opp"]["rev_total"] / cap, 1) if cap else None
        cap_m = r["me"]["plant_total"] + r["me"]["peak_head"]
        rec["me_rev_per_cap"] = round(r["me"]["rev_total"] / cap_m, 1) if cap_m else None
        out.append(rec)
    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    stats = merged_deep_stats()
    games = official_games(stats)
    game_map = {g["episode"]: g for g in games}

    # 实测成交层（逐局缓存到 probes 目录，二次运行免重算）
    fills_cache_path = os.path.join(OUT_DIR, "round24_fills_cache.json")
    if os.path.isfile(fills_cache_path):
        raw = load_json(fills_cache_path)
        fills_map = {tuple(map(int, k.split("|"))): v
                     for k, v in raw.items()}
    else:
        fills_map = {}
    replays, prices_cache = {}, {}
    for g in games:
        ep = g["episode"]
        path = os.path.join(REPLAY_DIR, f"episode-{ep}-replay.json")
        replay = load_json(path)
        replays[ep] = replay
        prices_cache[ep] = market_price_paths(replay)
        for seat in (0, 1):
            if (ep, seat) not in fills_map:
                fills_map[(ep, seat)] = fills_by_seat(replay).get(seat, {})
    with open(fills_cache_path, "w", encoding="utf-8") as h:
        json.dump({f"{k[0]}|{k[1]}": v for k, v in fills_map.items()}, h,
                  ensure_ascii=False, indent=1)

    rows = []
    for g in games:
        ep = g["episode"]
        rows.append(game_row(g, fills_map[(ep, g["me"])],
                             fills_map[(ep, 1 - g["me"])]))
    with open(os.path.join(OUT_DIR, "round24_ledger_forensics.json"), "w",
              encoding="utf-8") as h:
        json.dump(rows, h, ensure_ascii=False, indent=1, default=str)

    wins = [r for r in rows if r["result"] == "W"]
    losses = [r for r in rows if r["result"] == "L"]
    print(f"===== round24 台账：{len(rows)} 官方局 "
          f"{len(wins)}W-{len(losses)}L margin 总和 "
          f"{sum(r['margin'] for r in rows):+d} 局均 "
          f"{sum(r['margin'] for r in rows)/len(rows):+.0f} =====")
    for r in rows:
        print(f"  ep{r['episode']} {r['band']:13s} margin {r['margin']:+8d} "
              f"me {r['me']['final']:6d} opp {r['opp']['final']:6d} "
              f"opp_rev {r['opp']['rev_total']:7.0f} "
              f"opp_plants {r['opp']['plant_total']:3d} "
              f"opp_head {r['opp']['peak_head']:2d} "
              f"opp_top {r['opp']['top_lines'][0] if r['opp']['top_lines'] else '-'}")

    # ---- 9 深挖局时间线 ----
    forks = []
    for ep in TARGET9:
        ft = fork_timeline(game_map[ep], replays[ep], prices_cache[ep],
                           fills_map[(ep, game_map[ep]["me"])],
                           fills_map[(ep, 1 - game_map[ep]["me"])])
        forks.append(ft)
        op = ft["opp_profile"]
        print(f"\n== ep{ep} [{ft['band']}] vs {ft['opponent']} "
              f"margin {ft['margin']:+d} fork_day={ft['fork_day']} "
              f"gap_by_day d6/d9/d12/d18/d24 = "
              f"{ft['gap_by_day'][6]}/{ft['gap_by_day'][9]}/"
              f"{ft['gap_by_day'][12]}/{ft['gap_by_day'][18]}/"
              f"{ft['gap_by_day'][24]}")
        print(f"   opp: final {op['final']} d12 {op['d12']} d24 {op['d24']} "
              f"rev {op['rev_total']} plants {op['plants']} "
              f"head {op['peak_head']} quads {op['quads']} "
              f"feed {op['feed_buy_qty']}u animal_share "
              f"{op['rev_animal_share']}")
        print(f"   opp top_lines {op['top_lines']} "
              f"line_starts {ft['opp_line_starts']} ramp {ft['opp_ramp']}")
        print(f"   me : final {ft['me_profile']['final']} "
              f"d12 {ft['me_profile']['d12']} d24 {ft['me_profile']['d24']} "
              f"rev {ft['me_profile']['rev_total']} "
              f"plants {ft['me_profile']['plants']} "
              f"head {ft['me_profile']['peak_head']} "
              f"quads {ft['me_profile']['quads']} "
              f"line_starts {ft['me_line_starts']}")
    with open(os.path.join(OUT_DIR, "round24_fork_timelines.json"), "w",
              encoding="utf-8") as h:
        json.dump(forks, h, ensure_ascii=False, indent=1, default=str)

    # ---- 大赢对称性 ----
    sym = win_symmetry(rows, game_map, fills_map, prices_cache)
    with open(os.path.join(OUT_DIR, "round24_win_symmetry.json"), "w",
              encoding="utf-8") as h:
        json.dump(sym, h, ensure_ascii=False, indent=1, default=str)
    print(f"\n===== 大赢对称性（{len(sym)} 局 opp<57k，实测成交口径）=====")
    for s in sym:
        print(f"  ep{s['episode']} vs {s['opponent'][:20]:20s} "
              f"opp_final {s['opp_final']:6d} rev {s['opp_rev_total']:7.0f} "
              f"plants {s['opp_plant_total']:3d} head {s['opp_peak_head']:2d} "
              f"top {s['opp_top_line']}({s['opp_top_rev']:.0f},"
              f"fill {s['opp_top_filled']}) "
              f"rev/cap opp {s['opp_rev_per_cap']} me {s['me_rev_per_cap']} "
              f"share_me {s['me_market_share_top']} "
              f"price(E,L) {s['prices_top_early_late']}")

    # ---- 败局对手主产品线实现价基准（对称性对照组）----
    print("\n===== 9 败局对手主产品线实现价（对照基准）=====")
    for ep in TARGET9:
        g = game_map[ep]
        fo = fills_map[(ep, 1 - g["me"])]
        r = [x for x in rows if x["episode"] == ep][0]
        lines = r["opp"]["top_lines"][:2]
        pr = [(k, realized_price(fo, k)) for k, _ in lines]
        print(f"  ep{ep} {r['opponent'][:20]:20s} {pr}")
    print(f"\nwrote {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
