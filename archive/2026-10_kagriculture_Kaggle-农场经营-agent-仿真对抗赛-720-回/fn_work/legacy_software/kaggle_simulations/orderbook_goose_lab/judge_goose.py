# -*- coding: utf-8 -*-
"""judge_goose（goose lab）：鹅线变体 vs H1 原版 配对因果 A/B 判决（不发射）。

责任口径（任务 B4b 判决）：**变体 vs H1 配对**（26 败局+新中性块 672000+i*67，
n=16 双席/变体）：
- 配对口径（ab_r41/K2 净翻胜定义，track1 ab_t1b 同式）：control=H1 原版 vs
  对手 O，arm=变体 vs 同一 O，同 seed+seat 配对；对手 j23.DEFAULT_OPPONENTS
  轮转；margin=run_games banks（=终局 farms[obs.player].money 干净口径）。
- 判据：净翻胜>0（net_flip_wins=win_variant−win_control）∧ 胜局对照不翻负
  （flips_neg==0）=正臂。
- 附经济面对照：逐日现金 / 终局钱 / 蛋肥收入占比（trace 口径=挂单量×挂价）。
预算：≤450 局次（game 口径；fold=games/2 同报）：认证 30 + control 32 +
32×变体数。sim_bridge 先认证 30/30（不过即停）；workers=2。
复用（不改写）：ab_r41._specs_for / judge_r23._build_agents / sim_bridge.run_games
/sim_bridge.sim_bridge。只写 orderbook_goose_lab/ 与
fn_docs/hybrid/results/2026-09-29-goose-line.json（任务指定证据路径）。
"""
from __future__ import annotations

import json
import multiprocessing
import os
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))

import goose_line as gl  # noqa: E402
import gates_goose as gg  # noqa: E402

RECORD_VERSION = "judge-goose/1.0"
EVID_DIR = HERE / "evidence"
RESULT_PATH = (KSIM_DIR.parents[2] / "fn_docs" / "hybrid" / "results"
               / "2026-09-29-goose-line.json")
H1_MAIN = gl.H1_MAIN
WORKERS = 2
BUDGET_CAP_GAMES = 450

# 语料：26 败局回放（前 8 fold，canonical 序）+ 新中性块 672000+i*67（i=0..7）
LOSS_SEEDS_26 = [
    1825501814, 2013941152, 786146079, 1883261866,
    963182245, 240876256, 1705553586, 2009279466,
    161402123, 435866961, 841473039, 1388158282,
    1647385154, 671940665, 219073637, 1439493993,
    1360429471, 671494671, 1900972921, 973657130,
    1911990026, 1918725083, 176568822, 427304807,
    720683523, 906608145,
]
NEUTRAL_SEEDS = [672000 + i * 67 for i in range(8)]
FOLDS = ([(int(s), "loss_replay") for s in LOSS_SEEDS_26[:8]]
         + [(int(s), "neutral_672k67") for s in NEUTRAL_SEEDS])


# ------------------------------------------------------------ 经济面 --
def econ_face(sink):
    """逐日现金 + 终局钱 + 蛋肥收入占比（trace 口径：挂单量×挂时价）。"""
    daily = {}
    sells = []          # (item, qty, px)
    last_obs = None
    for step, obs, act in (sink or []):
        if not isinstance(obs, dict):
            continue
        step = int(step)
        try:
            player = int(obs.get("player", 0))
        except Exception:
            player = 0
        farms = obs.get("farms")
        money = None
        if isinstance(farms, list) and player < len(farms) \
                and isinstance(farms[player], dict):
            try:
                money = float(farms[player].get("money", 0.0))
            except (TypeError, ValueError):
                money = None
        if money is not None and step % 24 == 0:
            daily[step // 24] = round(money, 2)
        prices = ((obs.get("market") or {}) if isinstance(obs.get("market"),
                  dict) else {}).get("prices") or {}
        if isinstance(act, dict):
            for cmd in (act.get("market") or []):
                if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                        and str(cmd[0]) == "SELL":
                    px = prices.get(str(cmd[1]))
                    if isinstance(px, (int, float)):
                        sells.append((str(cmd[1]), float(cmd[2]), float(px)))
        last_obs = obs
    terminal = daily.get(29)
    if terminal is None and last_obs is not None:
        try:
            player = int(last_obs.get("player", 0))
            terminal = float(last_obs["farms"][player].get("money", 0.0))
        except Exception:
            terminal = None
    income = {}
    total = 0.0
    for item, qty, px in sells:
        v = qty * px
        income[item] = income.get(item, 0.0) + v
        total += v
    egg_fert = income.get("EGG", 0.0) + income.get("FERTILIZER", 0.0)
    share = round(egg_fert / total, 4) if total > 0 else None
    return {"daily_money": daily, "terminal_money": terminal,
            "sell_income": {k: round(v, 1) for k, v in sorted(income.items())},
            "egg_fert_income": round(egg_fert, 1),
            "egg_fert_share": share}


def _agg_econ(rows):
    tms = [r["econ"]["terminal_money"] for r in rows
           if isinstance(r.get("econ"), dict)
           and isinstance(r["econ"].get("terminal_money"), (int, float))]
    shs = [r["econ"]["egg_fert_share"] for r in rows
           if isinstance(r.get("econ"), dict)
           and isinstance(r["econ"].get("egg_fert_share"), (int, float))]
    egg = [r["econ"]["sell_income"].get("EGG", 0.0) for r in rows
           if isinstance(r.get("econ"), dict)]
    fert = [r["econ"]["sell_income"].get("FERTILIZER", 0.0) for r in rows
            if isinstance(r.get("econ"), dict)]
    # 逐日现金均值（对齐日序）
    day_series = {}
    for r in rows:
        e = r.get("econ") or {}
        for d, v in (e.get("daily_money") or {}).items():
            day_series.setdefault(int(d), []).append(float(v))
    daily_mean = {str(d): round(statistics.mean(vs), 1)
                  for d, vs in sorted(day_series.items())}
    return {"n": len(tms),
            "terminal_money_mean": round(statistics.mean(tms), 1) if tms else None,
            "terminal_money_median": round(statistics.median(tms), 1) if tms else None,
            "egg_fert_share_mean": round(statistics.mean(shs), 4) if shs else None,
            "egg_income_mean": round(statistics.mean(egg), 1) if egg else None,
            "fert_income_mean": round(statistics.mean(fert), 1) if fert else None,
            "daily_money_mean": daily_mean}


# ------------------------------------------------------------ 局跑口 --
def _chunk(payload):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    games, metas = [], []
    for spec in specs:
        try:
            agents, sinks = j23._build_agents(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, {"build_error": repr(exc)[:120]}))
            continue
        metas.append((spec, sinks))
    res = sb.run_games(games, cfg) if games else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"game_id": spec.get("game_id"), "seed": int(spec["seed"]),
               "seat": int(spec.get("our_seat", 0)), "arm": spec.get("arm"),
               "opponent": spec.get("opponent"), "stratum": spec.get("stratum"),
               "banks": rr.get("banks"), "error": rr.get("error"),
               "margin": None, "econ": {}}
        if isinstance(sinks, dict) and "build_error" in sinks:
            row["error"] = sinks["build_error"]
            sinks = None
        if row["banks"] is not None and row["error"] is None:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - float(banks[1 - row["seat"]])
            if isinstance(sinks, dict):
                sink = sinks.get(row["seat"])
                if sink is not None:
                    try:
                        row["econ"] = econ_face(sink)
                    except Exception as exc:
                        row["econ_error"] = repr(exc)[:100]
        out.append(row)
    return out


def _play(specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_chunk, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


def make_units():
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    opp_paths = [str(rel) if Path(rel).is_file() else str(KSIM_DIR / rel)
                 for rel in j23.DEFAULT_OPPONENTS]
    for p in opp_paths:
        if not Path(p).is_file():
            raise FileNotFoundError("对局件缺失: %s" % p)
    units = []
    for j, (seed, stratum) in enumerate(FOLDS):
        opp_path = opp_paths[j % len(opp_paths)]
        for seat in (0, 1):
            units.append({"seed": seed, "seat": seat, "opp_path": opp_path,
                          "opponent": Path(opp_path).parent.name + "/" +
                          Path(opp_path).name,
                          "stratum": stratum})
    return units, opp_paths


def specs_for(rows_src, arm, cand_path):
    from orderbook_r40 import ab_r41 as ab  # noqa: WPS433
    specs = ab._specs_for(rows_src, arm, cand_path, True)
    for spec, src in zip(specs, rows_src):
        spec["stratum"] = src["stratum"]
        spec["game_id"] = "goose-%s-%d-s%d" % (arm, int(src["seed"]),
                                               int(src["seat"]))
    return specs


def ab_stats(ledger_units, vid):
    agg = {"n": 0, "delta_sum": 0.0, "margin_control_sum": 0.0,
           "margin_variant_sum": 0.0, "win_control": 0, "win_variant": 0,
           "flips_pos": 0, "flips_neg": 0, "loss_recovery": 0,
           "loss_recovery_n": 0}
    for lu in ledger_units:
        v = (lu.get("variants") or {}).get(vid)
        if v is None:
            continue
        agg["n"] += 1
        agg["delta_sum"] += v["delta"]
        agg["margin_control_sum"] += lu["margin_control"]
        agg["margin_variant_sum"] += v["margin_variant"]
        wc = 1 if lu["margin_control"] > 0 else 0
        wv = 1 if v["margin_variant"] > 0 else 0
        agg["win_control"] += wc
        agg["win_variant"] += wv
        if wv and not wc:
            agg["flips_pos"] += 1
        if wc and not wv:
            agg["flips_neg"] += 1
        if lu["stratum"] == "loss_replay":
            agg["loss_recovery_n"] += 1
            if v["delta"] > 0:
                agg["loss_recovery"] += 1
    n = max(1, agg["n"])
    out = {"n": agg["n"],
           "mean_delta": round(agg["delta_sum"] / n, 2),
           "mean_margin_control": round(agg["margin_control_sum"] / n, 2),
           "mean_margin_arm": round(agg["margin_variant_sum"] / n, 2),
           "win_rate_control": round(agg["win_control"] / n, 4),
           "win_rate_arm": round(agg["win_variant"] / n, 4),
           "net_flip_wins": int(agg["win_variant"]) - int(agg["win_control"]),
           "flips_pos": agg["flips_pos"], "flips_neg": agg["flips_neg"],
           "control_win_guard_ok": bool(agg["flips_neg"] == 0),
           "loss_recovery": "%d/%d 败局 delta>0" % (agg["loss_recovery"],
                                                    agg["loss_recovery_n"])}
    out["positive_arm"] = bool(out["net_flip_wins"] > 0
                               and out["control_win_guard_ok"])
    return out


def ensure_auth(auth_corpus=None):
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth_path = EVID_DIR / "sim_auth.json"
    corpus = list(auth_corpus or (LOSS_SEEDS_26 + [2026092901, 2026092902]))
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(EVID_DIR / "sim_auth_record.json")}, corpus)
    lite = {k: auth.get(k) for k in
            ("loaded", "consistency", "wall_speedup", "consistency_ok",
             "degraded", "degraded_reason", "engine", "timing", "version")}
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    auth_path.write_text(json.dumps(lite, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")
    return auth


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"cap_局次": BUDGET_CAP_GAMES, "caliber": "局次=game（fold=games/2 同报）",
              "auth_games": 0, "control_games": 0, "variant_games": 0}
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {
            "commands": ["python3 orderbook_goose_lab/econ_model.py",
                         "python3 orderbook_goose_lab/goose_line.py --build-all",
                         "python3 orderbook_goose_lab/gates_goose.py",
                         "python3 orderbook_goose_lab/judge_goose.py"],
            "base_main": str(H1_MAIN),
            "base_sha256": gl.hashlib.sha256(H1_MAIN.read_bytes()).hexdigest(),
            "corpus": {"loss_folds": LOSS_SEEDS_26[:8],
                       "neutral_folds": NEUTRAL_SEEDS,
                       "strata": "26 败局回放（前 8 fold）+ 新中性块 672000+i*67"
                                 "（i=0..7）；fold 口径 n=16 双席/变体"},
            "pairs_caliber": "变体 vs H1 原版配对（ab_r41/K2 净翻胜定义）："
                             "control=H1 vs 对手 O，arm=变体 vs 同 O，同 seed+seat；"
                             "margin=run_games banks（farms[obs.player] 干净口径）",
            "workers": WORKERS,
        },
        "budget": budget,
    }

    # ---- sim_bridge 对照认证 30/30（不过即停）----
    auth = ensure_auth()
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "consistency_ok", "engine",
                  "wall_speedup", "version")}
    budget["auth_games"] = 30
    print("sim auth:", auth_lite.get("consistency_ok"), auth_lite.get("consistency"),
          flush=True)
    if not auth_lite.get("consistency_ok"):
        out["aborted"] = "sim_bridge 对照认证未过 30/30"
        out["source"]["sim_auth"] = auth_lite
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1,
                                          default=str) + "\n", encoding="utf-8")
        print("ABORT", out["aborted"], flush=True)
        return out
    out["source"]["sim_auth"] = auth_lite
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    # ---- 构建件/门禁/孪生 读入（goose_line/gates_goose 产）----
    build = json.loads((EVID_DIR / "goose_build.json").read_text(
        encoding="utf-8")) if (EVID_DIR / "goose_build.json").is_file() else {}
    gates = json.loads((EVID_DIR / "goose_gates.json").read_text(
        encoding="utf-8")) if (EVID_DIR / "goose_gates.json").is_file() \
        else {"gates": {}}
    kept = [vid for vid, v in (build.get("variants") or {}).items()
            if v.get("kept")]
    gate_ok = [vid for vid in kept
               if (gates.get("gates") or {}).get(vid, {}).get("overall")]
    judged = [vid for vid in kept if vid in gate_ok]
    k_max = (BUDGET_CAP_GAMES - 32 - budget["auth_games"]) // 32
    judged = judged[:max(0, k_max)]
    out["variants"] = {}
    for vid, v in (build.get("variants") or {}).items():
        out["variants"][vid] = {
            "spec": v.get("spec"),
            "desc": gl.VARIANT_SPECS.get(vid, {}).get("desc"),
            "n_table_rows": v.get("n_table_rows"),
            "kept_twin": v.get("kept"),
            "n_bad_routes": v.get("n_bad_routes"),
            "gates": {k: gv.get("passed") for k, gv in
                      (gates.get("gates") or {}).get(vid, {}).items()
                      if k.startswith("gate")},
            "gates_overall": (gates.get("gates") or {}).get(vid, {}).get("overall"),
            "judged": vid in judged,
            "audit_summary": {
                "conservation_match": sum(
                    1 for c in (v.get("audit") or {}).get("conservation", [])
                    if c.get("match")),
                "conservation_n": len((v.get("audit") or {}).get(
                    "conservation", [])),
                "slot_ok": (v.get("audit") or {}).get("slot_ok"),
                "shared_seg": (v.get("audit") or {}).get("shared_seg"),
            },
            "feasibility": {
                "verdict": (v.get("feasibility") or {}).get("verdict"),
                "n_bad_routes": v.get("n_bad_routes"),
                "anchor_seed2": (v.get("feasibility") or {}).get("anchor_seed2"),
            },
            "table_full_path": v.get("table_full_path"),
            "pkg_dir": v.get("pkg_dir"),
        }
    out["feasibility"] = {vid: out["variants"][vid]["feasibility"]
                          for vid in out["variants"]}
    print("judged:", judged, "kept:", kept, "gate_ok:", gate_ok, flush=True)

    # ---- 配对跑局：control 共享 + 各变体 ----
    units, opp_paths = make_units()
    out["source"]["opponents"] = opp_paths
    t1 = time.perf_counter()
    p1 = _play(specs_for(units, "control", str(H1_MAIN)), run_cfg)
    budget["control_games"] = len(units)
    by_key = {(int(r["seed"]), int(r["seat"])): r for r in p1}
    var_rows = {}
    for vid in judged:
        rows = _play(specs_for(units, vid, str(Path(
            build["variants"][vid]["pkg_dir"]) / "main.py")), run_cfg)
        budget["variant_games"] += len(units)
        var_rows[vid] = {(int(r["seed"]), int(r["seat"])): r for r in rows}
        print(vid, "played", len(rows), "games", flush=True)
    budget["total_games"] = (budget["auth_games"] + budget["control_games"]
                             + budget["variant_games"])
    budget["total_局次_folds"] = budget["total_games"] // 2

    # ---- 账本 + ab 统计 + 经济面 ----
    ledger_units = []
    for u in units:
        r1 = by_key.get((u["seed"], u["seat"]))
        if r1 is None or r1.get("error") is not None or r1.get("margin") is None:
            continue
        rec = {"seed": u["seed"], "seat": u["seat"], "opponent": u["opponent"],
               "stratum": u["stratum"], "margin_control": r1["margin"],
               "econ_control": r1.get("econ"), "variants": {}}
        for vid in judged:
            r2 = var_rows[vid].get((u["seed"], u["seat"]))
            if r2 is None or r2.get("error") is not None \
                    or r2.get("margin") is None:
                continue
            rec["variants"][vid] = {
                "margin_variant": r2["margin"],
                "delta": r2["margin"] - r1["margin"],
                "econ_variant": r2.get("econ")}
        if rec["variants"]:
            ledger_units.append(rec)

    pairs, econ_stats = {}, {}
    for vid in judged:
        st = ab_stats(ledger_units, vid)
        st["spec"] = out["variants"][vid]["spec"]
        # 逐局 margin（lite）
        st["units_lite"] = [
            {"seed": lu["seed"], "seat": lu["seat"],
             "stratum": lu["stratum"], "margin_control": lu["margin_control"],
             "margin_variant": lu["variants"][vid]["margin_variant"],
             "delta": lu["variants"][vid]["delta"]}
            for lu in ledger_units if vid in lu["variants"]]
        pairs[vid] = st
        var_econ = _agg_econ([{"econ": lu["variants"][vid]["econ_variant"]}
                              for lu in ledger_units if vid in lu["variants"]])
        ctl_econ = _agg_econ([{"econ": lu["econ_control"]}
                              for lu in ledger_units if vid in lu["variants"]])
        econ_stats[vid] = {
            "control": ctl_econ, "variant": var_econ,
            "terminal_money_delta_mean": (
                round(var_econ["terminal_money_mean"]
                      - ctl_econ["terminal_money_mean"], 1)
                if var_econ["terminal_money_mean"] is not None
                and ctl_econ["terminal_money_mean"] is not None else None),
            "egg_fert_share_control": ctl_econ["egg_fert_share_mean"],
            "egg_fert_share_variant": var_econ["egg_fert_share_mean"],
        }

    out["pairs"] = pairs
    out["econ_stats"] = econ_stats
    out["criteria"] = {
        "positive_arm": "净翻胜>0（net_flip_wins=win_variant−win_control）的变体"
                        "为正臂；胜局对照不翻负（flips_neg==0）",
        "corpus_n": "16 fold 双席/变体（8 败局回放 + 8 新中性 672000+i*67）",
        "econ_face": "逐日现金（d0..d29 farms[obs.player].money）/终局钱/"
                     "蛋肥收入占比（EGG+FERTILIZER 挂单量×挂价 占比）",
    }
    positive = [vid for vid, s in pairs.items() if s.get("positive_arm")]
    out["verdict"] = {
        "positive_variants": positive,
        "verdict": ("PROD_ARM_CANDIDATE: %s" % positive) if positive
        else "NO_POSITIVE_GOOSE_ARM（鹅线无优势：无正翻胜变体）",
        "budget_compliance": "局次 %d/%d（cap 合规）" % (
            budget["total_games"], BUDGET_CAP_GAMES),
    }
    out["anomaly"] = []
    if (build.get("variants") or {}).get("goose9econ") is not None:
        out["anomaly"].append(
            "任务提要 EGG T=45 与引擎源码/抽取档 T=332 不符（源码直读"
            " kaggriculture.py MARKET_PARAMS EGG T=332）——econ_model 以 332 为准")
    for vid, v in (build.get("variants") or {}).items():
        for row in v.get("stats_rows", []):
            if row.get("stats", {}).get("convert_blocked"):
                out["anomaly"].append(
                    "%s/route %s: %d 次换链被 10 单帽阻断（同拍拆单不可用，"
                    "改用邻链补偿；trunk 波次谱与计划差 1 已登记）"
                    % (vid, row["route"], row["stats"]["convert_blocked"]))
                break
        seg = (v.get("audit") or {}).get("shared_seg") or {}
        if seg.get("tail", {}).get("divergent"):
            out["anomaly"].append(
                "%s: tail 共享段 %d 组跨路由有差异（仅 route 2 尾被复用；"
                "HARVEST 物种无关=零风险，信息登记）"
                % (vid, seg["tail"]["divergent"]))
        if v.get("n_bad_routes"):
            out["anomaly"].append(
                "%s: feasibility 孪生 %d 路由未过三闸（已弃判）"
                % (vid, v["n_bad_routes"]))
    out["anomaly"].append(
        "基线 route 101 落位 16/17（一格引擎 no-op：(3,2) GOOSE 库存缺链属"
        "基线自身行为；三闸按基线相对口径）")
    out["anomaly"].append("harness 噪声不修不管（任务边界）；终局钱 farms[obs.player] 口径")
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)

    (EVID_DIR / "judge_ledger.json").write_text(
        json.dumps({"units": ledger_units, "pairs": pairs},
                   ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")
    print("verdict:", out["verdict"], flush=True)
    print("budget:", budget, flush=True)
    for vid, s in pairs.items():
        print("  %s: n=%d delta=%.1f netflip=%+d flips_neg=%d %s"
              % (vid, s["n"], s["mean_delta"], s["net_flip_wins"],
                 s["flips_neg"], s["loss_recovery"]), flush=True)
    return out


if __name__ == "__main__":
    main()
