# -*- coding: utf-8 -*-
"""calibrate_oppcond：对手画像器标定批（指纹采集 + 阈值冻结；判决先行·不发射）。

责任口径（任务 opp-conditional A1）：开局窗（step≤144）公开信号指纹采集——
money 轨迹/现金差（EXP288 镜像口径 step1 现金差<0.5）、CT_TABLE 形 step2
(rival money, market WHEAT) 指纹、_r37_similarity 农场指纹、rival_sold 卖流
签名（v9 库存差分口径）。标定批=H1_base vs 5 对手件 × 3 seeds × 双席（30 局），
与判决语料隔离（throwaway 域 673000+i*37）。

产物 evidence/calib_fingerprints.json：逐 (opponent, seed, seat) 特征行 +
逐对手特征范围 + 指纹表候选 + 画像器阈值建议。
只写 orderbook_oppcond_lab/。不改既有代码。不发射。
"""
from __future__ import annotations

import json
import multiprocessing
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))

H1_MAIN = str(KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py")
OPPONENTS = {
    "r37": str(KSIM_DIR / "orderbook_r37" / "build" / "main.py"),
    "2965a": str(KSIM_DIR / "orderbook_2965_adopt" / "a" / "main.py"),
    "2965b": str(KSIM_DIR / "orderbook_2965_adopt" / "b" / "main.py"),
    "r40": str(KSIM_DIR / "orderbook_r40" / "build" / "main.py"),
    "h1": H1_MAIN,
    "wfr": str(KSIM_DIR / "orderbook_iterk_lab" / "opponents"
               / "counter_wool_front_runner.py"),
}
CALIB_SEEDS = [673000 + i * 37 for i in range(3)]   # 与判决语料隔离
WORKERS = 2
RECORD_VERSION = "oppcond-calib/1.0"
SIM_STEPS = (24, 48, 72, 96, 120, 143)


# ---------------------------------------------------------- 特征（公开信号） --
def _similarity(obs):
    """_r37_similarity 同式（公开农格指纹匹配率；≥8 占用格才有效）。"""
    farms = obs.get("farms") or []
    player = int(obs.get("player", 0))
    if len(farms) < 2:
        return 0.0
    own, rival = farms[player], farms[1 - player]
    if own.get("unlocked_quadrants") != rival.get("unlocked_quadrants"):
        return 0.0
    matches = total = 0
    for a, b in zip([t for row in own.get("tiles") or [] for t in row],
                    [t for row in rival.get("tiles") or [] for t in row]):
        sa = (a.get("crop"), a.get("animal")) if isinstance(a, dict) else (None, None)
        sb = (b.get("crop"), b.get("animal")) if isinstance(b, dict) else (None, None)
        if sa != (None, None) or sb != (None, None):
            total += 1
            matches += sa == sb
    return matches / total if total >= 8 else 0.0


_RACE_ITEMS = ("CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL")
_SHOP_ITEMS = {
    "BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"), "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}


def _town_draw(shops, step):
    draw = dict.fromkeys(_RACE_ITEMS, 0)
    if step % 4 == 0:
        for shop in shops:
            items = _SHOP_ITEMS.get(shop, ())
            for item in items:
                if item in draw:
                    draw[item] += 2 if len(items) == 1 else 1
    if step % 24 == 0:
        for item in draw:
            draw[item] += 1
    return draw


def _own_sells(act):
    out = {}
    if isinstance(act, dict):
        for o in act.get("market") or []:
            if isinstance(o, (list, tuple)) and len(o) >= 3 and o[0] == "SELL":
                try:
                    out[str(o[1])] = out.get(str(o[1]), 0) + int(o[2])
                except Exception:
                    pass
    return out


def _farm_sig(obs, player):
    farms = obs.get("farms") or []
    if len(farms) < 2:
        return {}
    farm = farms[1 - player]
    animals = {}
    crops = {}
    occupied = 0
    yld = 0
    for row in farm.get("tiles") or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if tile.get("animal"):
                animals[tile["animal"]] = animals.get(tile["animal"], 0) + 1
                occupied += 1
            elif tile.get("crop"):
                crops[tile["crop"]] = crops.get(tile["crop"], 0) + 1
                occupied += 1
            yld += int(tile.get("yield_units", 0) or 0)
    return {"animals": animals, "crops": crops, "occupied": occupied,
            "yield_units": yld, "hands": len(farm.get("hands") or []),
            "quadrants": list(farm.get("unlocked_quadrants") or [])}


def extract_features(sink):
    """追踪槽 [(step, obs, act)]（我席）→ 开局窗特征（step≤143）。"""
    feats = {
        "money_own": {}, "money_rival": {}, "step1_cashdiff": None,
        "rkey2": None, "sim": {}, "rival_sold_cum": {}, "own_sold_cum": {},
        "farm_sig_143": None, "start_money_rival": None,
    }
    prev_inv = None
    prev_step = None
    for entry in (sink or []):
        step, obs, act = int(entry[0]), entry[1], entry[2]
        if step > 143:
            break
        if not isinstance(obs, dict):
            continue
        player = int(obs.get("player", 0))
        farms = obs.get("farms") or []
        if len(farms) < 2:
            continue
        own_m = float(farms[player].get("money", 0.0))
        riv_m = float(farms[1 - player].get("money", 0.0))
        feats["money_own"][step] = own_m
        feats["money_rival"][step] = riv_m
        if step == 0:
            feats["start_money_rival"] = riv_m
        if step == 1:
            feats["step1_cashdiff"] = round(abs(riv_m - own_m), 4)
        inv = ((obs.get("market") or {}) if isinstance(obs.get("market"), dict)
               else {}).get("inventory") or {}
        if step == 2:
            feats["rkey2"] = [round(riv_m, 3), int(inv.get("WHEAT", 0))]
        if step in SIM_STEPS:
            feats["sim"][step] = round(_similarity(obs), 4)
        if prev_inv is not None and prev_step == step - 1:
            shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
            draw = _town_draw(shops, step - 1)
            osold = _own_sells(act)
            for item in _RACE_ITEMS:
                try:
                    sold = (int(inv.get(item, 0)) - int(prev_inv.get(item, 0))
                            + draw.get(item, 0) - osold.get(item, 0))
                except Exception:
                    continue
                if sold > 0:
                    feats["rival_sold_cum"][item] = \
                        feats["rival_sold_cum"].get(item, 0) + int(sold)
            for item, n in osold.items():
                feats["own_sold_cum"][item] = \
                    feats["own_sold_cum"].get(item, 0) + n
        prev_inv = {k: int(v) for k, v in inv.items()}
        prev_step = step
        if step == 143:
            feats["farm_sig_143"] = _farm_sig(obs, player)
    sims = list(feats["sim"].values())
    feats["sim_max"] = max(sims) if sims else None
    feats["sim_final"] = sims[-1] if sims else None
    return feats


# --------------------------------------------------------------- 跑局 --
def _run_chunk(payload):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    games, meta = [], []
    for g in payload["games"]:
        ag, sinks = j23._build_agents(g["spec"])
        games.append({"seed": int(g["spec"]["seed"]), "agents": ag})
        meta.append((g, sinks))
    res = sb.run_games(games, {"engine": "auto", "workers": 1}) \
        if games else {"games": [], "engine": None}
    rows = list(res.get("games") or [])
    out = []
    for i, (g, sinks) in enumerate(meta):
        rr = rows[i] if i < len(rows) else {}
        seat = int(g["spec"]["our_seat"])
        sink = (sinks or {}).get(seat) or []
        row = {
            "opponent": g["opponent"], "seed": int(g["spec"]["seed"]),
            "our_seat": seat, "banks": rr.get("banks"), "error": rr.get("error"),
            "features": extract_features(sink),
        }
        if rr.get("banks") is not None and rr.get("error") is None:
            banks = rr["banks"]
            row["margin"] = round(float(banks[seat]) - float(banks[1 - seat]), 2)
        out.append(row)
    return {"rows": out, "engine": res.get("engine"),
            "fallback_reason": res.get("fallback_reason")}


def main():
    t0 = time.perf_counter()
    specs = []
    for opp, path in OPPONENTS.items():
        for seed in CALIB_SEEDS:
            for seat in (0, 1):
                # 我臂（H1_base）落 our_seat，对手落对席（画像器视角=我席）
                agents = ([{"type": "python", "path": H1_MAIN},
                           {"type": "python", "path": path}] if seat == 0
                          else [{"type": "python", "path": path},
                                {"type": "python", "path": H1_MAIN}])
                specs.append({"opponent": opp, "spec": {
                    "game_id": "calib-%s-%d-%d" % (opp, seed, seat),
                    "seed": seed, "kind": "calib", "trace": True,
                    "our_seat": seat, "agents": agents}})
    chunks = [specs[i::WORKERS] for i in range(WORKERS)]
    tasks = [{"games": c} for c in chunks if c]
    if WORKERS <= 1 or len(tasks) <= 1:
        parts = [_run_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(WORKERS, len(tasks))) as pool:
            parts = pool.map(_run_chunk, tasks)
    rows = []
    for p in parts:
        rows.extend(p["rows"])
    rows.sort(key=lambda r: (r["opponent"], r["seed"], r["our_seat"]))

    # 逐对手特征汇总（指纹表候选：rkey2 唯一性检验）
    by_opp = {}
    for r in rows:
        by_opp.setdefault(r["opponent"], []).append(r)
    summary = {}
    for opp, rs in by_opp.items():
        rkeys = sorted({tuple(r["features"].get("rkey2") or ()) for r in rs})
        diffs = [r["features"].get("step1_cashdiff") for r in rs
                 if r["features"].get("step1_cashdiff") is not None]
        simmax = [r["features"].get("sim_max") for r in rs
                  if r["features"].get("sim_max") is not None]
        summary[opp] = {
            "n_games": len(rs),
            "rkey2_unique": [list(k) for k in rkeys],
            "step1_cashdiff": diffs,
            "sim_max": simmax,
            "start_money_rival": sorted({r["features"].get("start_money_rival")
                                         for r in rs}),
            "rival_sold_cum_sum": {
                item: sorted({r["features"]["rival_sold_cum"].get(item, 0)
                              for r in rs}) for item in _RACE_ITEMS},
        }
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {
            "commands": ["python3 orderbook_oppcond_lab/calibrate_oppcond.py"],
            "our_arm": H1_MAIN,
            "opponents": OPPONENTS,
            "calib_seeds": CALIB_SEEDS,
            "seed_isolation": "throwaway 域 673000+i*37（与判决语料 26 败局/"
                              "672000+i*59 零交集）",
            "workers": WORKERS,
            "caliber": "开局窗 step≤143 公开信号（money 轨迹/step1 现金差/"
                       "step2 (money,WHEAT) 指纹/_r37_similarity 农场指纹/"
                       "rival_sold 卖流签名 v9 库存差分口径）",
        },
        "summary_by_opponent": summary,
        "rows": rows,
        "elapsed_s": round(time.perf_counter() - t0, 1),
        "n_error_games": sum(1 for r in rows if r.get("error")),
        "engines": [p.get("engine") for p in parts],
    }
    evid = MODULE_DIR / "evidence"
    evid.mkdir(parents=True, exist_ok=True)
    (evid / "calib_fingerprints.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1, default=str))
    print("elapsed", out["elapsed_s"], "s errors", out["n_error_games"])
    return out


if __name__ == "__main__":
    main()
