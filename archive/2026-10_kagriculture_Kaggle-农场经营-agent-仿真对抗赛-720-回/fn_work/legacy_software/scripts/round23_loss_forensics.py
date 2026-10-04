# 【中文】round23_loss_forensics.py —— round-23 败局法证（Track-B，只读探针）
# ===========================================================================
# 用途（round-23 败局法证任务包）：
#   1) 19 官方局逐局台账：margin 带、败因模式启发式、对手结构分型；
#   2) 灾难局 ep110634204 逐日时间线（动作/资金/畜群/市价）；
#   3) 惜败带 vs 结构带切分 + "我们怕谁"画像；
#   4) round22（v13.8）同口径败因分布对照。
# 输入：exports/probes/planner_bench/round23_deep_stats.json（现役产物），
#       exports/probes/round22_deep_stats_regen.json（本探针预生成），
#       references/data/online-replays/{round22,round23}/episode-*.json。
# 输出：exports/probes/round23_forensics/*.json（中间数据，gitignored）+
#       stdout 摘要表。只读回放与 src/planner，不写现役文件。
# 纪律：stdlib-only、离线、确定性；所有数字来自回放实测。
# ===========================================================================

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
ROOT = os.path.dirname(SOFTWARE)   # kaggriculture/
REPLAY_DIR = os.path.join(ROOT, "references", "data", "online-replays")
OUT_DIR = os.path.join(SOFTWARE, "exports", "probes", "round23_forensics")
TEAM = "renyxin"
CROPS = ("STRAWBERRY", "WHEAT", "MELON", "CARROT", "TOMATO")
ANIMAL_PRODUCTS = ("MILK", "WOOL", "EGG")
CROP_PRODUCTS = ("STRAWBERRY", "MELON", "WHEAT", "CARROT", "TOMATO")


def load_json(path):
    with open(path, "r", encoding="utf-8") as h:
        return json.load(h)


def official_games(deep_stats):
    """非镜像官方局列表（按 episode_id 升序），附我方席位。"""
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


def curve(p, key="money_end"):
    return [r.get(key) for r in sorted(p["table"], key=lambda r: r["day"])]


def series_total(p, key):
    tot = defaultdict(float)
    for r in p["table"]:
        for k, v in (r.get(key) or {}).items():
            tot[k] += float(v)
    return dict(tot)


def plants_total(p):
    tot = defaultdict(float)
    for r in p["table"]:
        for k, v in (r.get("plants") or {}).items():
            tot[k] += float(v)
    return dict(tot)


def revenue_mix(p):
    rev = series_total(p, "sells_revenue")
    animal = sum(rev.get(k, 0.0) for k in ANIMAL_PRODUCTS)
    crop = sum(rev.get(k, 0.0) for k in CROP_PRODUCTS)
    fert = rev.get("FERTILIZER", 0.0)
    tot = animal + crop + fert
    if tot <= 0:
        return {"animal_share": 0.0, "crop_share": 0.0, "fert_share": 0.0,
                "rev_total": 0.0, "rev": rev}
    return {"animal_share": animal / tot, "crop_share": crop / tot,
            "fert_share": fert / tot, "rev_total": tot, "rev": rev}


def opponent_typing(opp):
    """对手结构分型：主型（单一标签）+ 特征多标签。证据=plants/畜群/卖收。"""
    plants = plants_total(opp)
    ptot = sum(plants.values()) or 1.0
    peak_head = int(opp.get("peak_herd_head") or 0)
    rev = revenue_mix(opp)
    quads = opp.get("quadrant_unlock_day") or {}
    unlocks = [q for q, d in quads.items() if q != "NW"]
    early_sw = quads.get("SW", 99) <= 10
    wheat_share = plants.get("WHEAT", 0.0) / ptot
    berry_share = (plants.get("STRAWBERRY", 0.0)
                   + plants.get("MELON", 0.0)) / ptot
    tags = []
    if peak_head >= 12:
        tags.append("herd_heavy")
    if wheat_share >= 0.40:
        tags.append("wheat_heavy")
    if berry_share >= 0.55:
        tags.append("berry_melon_heavy")
    if len(unlocks) >= 2 and early_sw:
        tags.append("fast_multi_quadrant")
    # 主型：按收入结构判（动物产品收入占比 vs 作物）
    if rev["animal_share"] >= 0.30 and peak_head >= 10:
        primary = "herd_heavy"
    elif wheat_share >= 0.40:
        primary = "wheat_heavy"
    elif berry_share >= 0.55:
        primary = "berry_melon_heavy"
    elif len(unlocks) >= 2 and early_sw:
        primary = "fast_multi_quadrant"
    else:
        primary = "balanced"
    return {"primary": primary, "tags": tags, "plants": plants,
            "plant_total": ptot, "peak_head": peak_head,
            "unlocks": quads, "rev_mix": {k: round(v, 3) for k, v in
                                          rev.items() if k != "rev"},
            "revenue": {k: round(v, 0) for k, v in rev["rev"].items()}}


def margin_band(m):
    if m < 0:
        m = -m
    if m < 1000:
        return "<1k 惜败"
    if m < 2000:
        return "1-2k 运气带"
    if m < 5000:
        return "2-5k 结构带边缘"
    if m < 20000:
        return "5-20k 结构带"
    return ">=20k 崩局带"


def classify_loss(mine, opp, margin):
    """败因模式启发式（证据字段全部随行输出，供人工复核）。"""
    tm, to = day_table(mine), day_table(opp)
    money_m = curve(mine)
    money_o = curve(opp)

    def at(tbl, d, k="money_end"):
        v = tbl.get(d, {}).get(k)
        return v if isinstance(v, (int, float)) else 0.0

    lead_d12 = at(tm, 12) - at(to, 12)
    lead_d18 = at(tm, 18) - at(to, 18)
    lead_d24 = at(tm, 24) - at(to, 24)
    ramp_m = at(tm, 24) - at(tm, 12)
    ramp_o = at(to, 24) - at(to, 12)
    late_m = money_m[29] - at(tm, 24)
    late_o = money_o[29] - at(to, 24)
    head_d18 = at(tm, 18, "herd_head")
    empty_d18 = at(tm, 18, "herd").get("EMPTY_STRUCTURE", 0) \
        if isinstance(at(tm, 18, "herd"), dict) else 0
    peak_head = int(mine.get("peak_herd_head") or 0)
    ev = {"lead_d12": round(lead_d12), "lead_d18": round(lead_d18),
          "lead_d24": round(lead_d24), "ramp_me_d12_d24": round(ramp_m),
          "ramp_opp_d12_d24": round(ramp_o),
          "late_me_d24_d29": round(late_m), "late_opp_d24_d29": round(late_o),
          "head_d18": head_d18, "empty_structures_d18": empty_d18,
          "peak_head": peak_head, "final_opp": round(money_o[29])}
    # 优先级：早期压制 > 畜群扩建失败 > 终局反超 > 中期断档
    if lead_d12 <= -5000:
        pat = "early_press(开局即被压制)"
    elif empty_d18 >= 8 or head_d18 <= 8:
        pat = "herd_build_failure(扩建失败)"
    elif lead_d24 > -2000 and margin <= -5000:
        pat = "late_overtake(终局被反超)"
    elif ramp_m < 0.75 * ramp_o:
        pat = "mid_ramp_gap(中期爬坡差)"
    else:
        pat = "steady_gap(全程稳定差)"
    return pat, ev


def game_ledger(deep_stats):
    rows = []
    for g in official_games(deep_stats):
        mine, opp = g["mine"], g["opp"]
        margin = mine["reward"] - opp["reward"]
        pat, ev = classify_loss(mine, opp, margin)
        rows.append({
            "episode": g["episode"], "opponent": opp["team"],
            "me_seat": g["me"], "margin": round(margin),
            "result": "W" if margin > 0 else "L",
            "band": margin_band(margin),
            "loss_pattern": pat if margin < 0 else "",
            "evidence": ev,
            "final_me": round(mine["reward"]),
            "final_opp": round(opp["reward"]),
            "d12_me": round(curve(mine)[12]), "d12_opp": round(curve(opp)[12]),
            "d24_me": round(curve(mine)[24]), "d24_opp": round(curve(opp)[24]),
            "opp_type": opponent_typing(opp),
            "my_care": mine["totals"]["care"],
            "my_feed_ops": mine["totals"]["feed_ops"],
            "my_feed_buy": mine["totals"]["feed_buy_qty"],
            "my_hires": mine["totals"]["hires"],
            "my_peak_head": int(mine.get("peak_herd_head") or 0),
            "my_unlocks": mine.get("quadrant_unlock_day"),
        })
    return rows


def market_price_paths(replay):
    """逐日日终市价（共享市场，任一席观测一致）。"""
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


def disaster_timeline(deep_stats, replay_path, episode_id):
    e = [x for x in deep_stats if x["episode_id"] == episode_id][0]
    me = 0 if e["teams"][0] == TEAM else 1
    replay = load_json(replay_path)
    prices = market_price_paths(replay)
    mine, opp = e["players"][me], e["players"][1 - me]
    tm, to = day_table(mine), day_table(opp)
    # 逐日动作（我方席位）：market 单类型计数 + BUY_ANIMAL 明细
    acts_by_day = defaultdict(lambda: {"orders": 0, "buy_animal": [],
                                       "sell_kinds": set()})
    steps = replay["steps"]
    for t in range(0, len(steps) - 1):
        entry = steps[t + 1][me] if isinstance(steps[t + 1], list) \
            else steps[t + 1].get(str(me))
        action = (entry or {}).get("action") or {}
        day = t // 24
        rec = acts_by_day[day]
        for order in action.get("market") or []:
            if not isinstance(order, list) or not order:
                continue
            rec["orders"] += 1
            op = order[0]
            if op == "BUY_ANIMAL" and len(order) >= 3:
                rec["buy_animal"].append((order[1], int(order[2])))
            elif op == "SELL" and len(order) >= 2:
                rec["sell_kinds"].add(order[1])
    timeline = []
    for d in range(30):
        rm, ro = tm.get(d, {}), to.get(d, {})
        a = acts_by_day.get(d, {"orders": 0, "buy_animal": [], "sell_kinds": set()})
        timeline.append({
            "day": d,
            "me_money": rm.get("money_end"), "opp_money": ro.get("money_end"),
            "me_herd": rm.get("herd"), "opp_herd": ro.get("herd"),
            "me_animal_buys": rm.get("animal_buys"),
            "opp_animal_buys": ro.get("animal_buys"),
            "me_action_orders": a["orders"],
            "me_buy_animal_actions": a["buy_animal"],
            "prices": prices.get(d),
            "me_sells": rm.get("sells_qty"), "opp_sells": ro.get("sells_qty"),
        })
    return {"episode": episode_id,
            "teams": e["teams"], "rewards": e["rewards"],
            "totals_me": mine["totals"], "totals_opp": opp["totals"],
            "unlocks_me": mine["quadrant_unlock_day"],
            "unlocks_opp": opp["quadrant_unlock_day"],
            "timeline": timeline}


def summarize(rows, label):
    print(f"\n===== {label}：{len(rows)} 官方局 =====")
    wins = [r for r in rows if r["result"] == "W"]
    losses = [r for r in rows if r["result"] == "L"]
    mean_me = sum(r["final_me"] for r in rows) / len(rows)
    mean_opp = sum(r["final_opp"] for r in rows) / len(rows)
    print(f"{len(wins)}W-{len(losses)}L  margin 总和 "
          f"{sum(r['margin'] for r in rows):+d}  局均 "
          f"{sum(r['margin'] for r in rows) / len(rows):+.0f}  "
          f"(我方均值 {mean_me:.0f} vs 对手均值 {mean_opp:.0f})")
    print("-- 败局分类 --")
    for r in losses:
        print(f"  ep{r['episode']} vs {r['opponent'][:24]:24s} "
              f"margin {r['margin']:+7d}  {r['band']:12s}  "
              f"{r['loss_pattern']:28s} 对手={r['opp_type']['primary']}"
              f"({','.join(r['opp_type']['tags'])})")
    print("-- 败因分布 --")
    cnt = defaultdict(int)
    for r in losses:
        cnt[r["loss_pattern"]] += 1
    for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
        print(f"  {v}x {k}")
    print("-- 对手主型分布（败局 vs 胜局）--")
    for grp, name in ((losses, "L"), (wins, "W")):
        c = defaultdict(int)
        for r in grp:
            c[r["opp_type"]["primary"]] += 1
        print(f"  {name}: " + ", ".join(f"{k}={v}" for k, v in
                                        sorted(c.items(), key=lambda x: -x[1])))
    return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    r23 = load_json(os.path.join(SOFTWARE, "exports", "probes",
                                 "planner_bench", "round23_deep_stats.json"))
    r22 = load_json(os.path.join(SOFTWARE, "exports", "probes",
                                 "round22_deep_stats_regen.json"))
    rows23 = game_ledger(r23)
    rows22 = game_ledger(r22)
    summarize(rows23, "round23 DTSP v1")
    summarize(rows22, "round22 v13.8")

    # 运气带/结构带切分（round23）
    luck = [r for r in rows23 if r["result"] == "L" and r["margin"] > -2000]
    struct = [r for r in rows23 if r["result"] == "L" and r["margin"] <= -2000]
    print(f"\n-- 惜败/运气带（margin>-2k）：{len(luck)} 局 "
          f"{[r['episode'] for r in luck]}")
    print(f"-- 结构带（margin<=-2k）：{len(struct)} 局 "
          f"{[r['episode'] for r in struct]}")
    if struct:
        # 结构带共性：对手共同特征
        opp_types = defaultdict(int)
        opp_final = [r["final_opp"] for r in struct]
        opp_d24 = [r["d24_opp"] for r in struct]
        for r in struct:
            opp_types[r["opp_type"]["primary"]] += 1
        print(f"   结构带对手终局 min/med/max = {min(opp_final)}/"
              f"{sorted(opp_final)[len(opp_final)//2]}/{max(opp_final)}, "
              f"d24 min/med/max = {min(opp_d24)}/"
              f"{sorted(opp_d24)[len(opp_d24)//2]}/{max(opp_d24)}")
        print(f"   结构带对手主型: {dict(opp_types)}")
    # 胜局对照：对手 d24/final
    wins = [r for r in rows23 if r["result"] == "W"]
    if wins:
        wd24 = sorted(r["d24_opp"] for r in wins)
        wf = sorted(r["final_opp"] for r in wins)
        print(f"-- 胜局对手 d24 max={wd24[-1]} final max={wf[-1]} "
              f"(败局带对照)")

    # 灾难局时间线
    tl = disaster_timeline(r23, os.path.join(
        REPLAY_DIR, "round23", "episode-110634204-replay.json"), 110634204)
    with open(os.path.join(OUT_DIR, "disaster_110634204_timeline.json"),
              "w", encoding="utf-8") as h:
        json.dump(tl, h, ensure_ascii=False, indent=1, default=str)
    print("\n===== 灾难局 ep110634204 时间线（要点）=====")
    for t in tl["timeline"]:
        if t["day"] in (0, 5, 6, 7, 9, 10, 11, 12, 13, 14, 17, 19, 24, 29):
            p = t["prices"] or {}
            print(f" d{t['day']:2d} me {t['me_money']:8.0f} "
                  f"opp {t['opp_money']:8.0f} | me_herd {t['me_herd']} "
                  f"buys {t['me_animal_buys']} acts {t['me_action_orders']:2d}"
                  f" {t['me_buy_animal_actions']} | opp_herd {t['opp_herd']} "
                  f"opp_buys {t['opp_animal_buys']}"
                  f" | WOOL {p.get('WOOL')} MILK {p.get('MILK')} "
                  f"EGG {p.get('EGG')} MELON {p.get('MELON')} "
                  f"STRAW {p.get('STRAWBERRY')}")

    with open(os.path.join(OUT_DIR, "round23_ledger_forensics.json"),
              "w", encoding="utf-8") as h:
        json.dump(rows23, h, ensure_ascii=False, indent=1, default=str)
    with open(os.path.join(OUT_DIR, "round22_ledger_forensics.json"),
              "w", encoding="utf-8") as h:
        json.dump(rows22, h, ensure_ascii=False, indent=1, default=str)
    print(f"\nwrote {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
