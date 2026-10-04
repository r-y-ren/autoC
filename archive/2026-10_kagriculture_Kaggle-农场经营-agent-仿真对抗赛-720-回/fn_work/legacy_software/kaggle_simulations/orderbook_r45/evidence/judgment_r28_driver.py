# -*- coding: utf-8 -*-
"""R28 判决执行驱动（evidence 构件，只写构建产物与 evidence，不改任何代码）。

链路（全部复用既有件，零码改）：
1. build_r45：r40 字节+三件套齐注（debt_ledger=advance_layer.py 同源、
   valley_gate=quote_context.py 语义件、advance_layer=advance_layer.py）→
   diff 审计+manifest 参数定桩+sha 链；
2. sim_bridge 对照认证先行（30 种子官方 vs 仿真逐局终局资金一致才开快线）；
3. judge_r45 真判决（缺省六局组：镜像压力板/反制臂/26 败局重演/胜局对照/
   baseline_r40 缺省基线臂/h2h_r40；seed_base=670000，局组 670000+gi*1000）；
4. 净量恒等台账采集：runner 沿 judge_r26._chunk 真链路（j23._build_agents+
   sim_bridge.run_games+realized_price_stats）跑局，逐局逐席从装载命名空间
   读 _ADV_LEDGER 快照回填 judge cfg["ledger"]/cfg["traces"]（可变容器，
   judge 跑完后 verify_net_identity 消费）；
5. evidence 落 orderbook_r45/evidence/judgment_r28.json（契约键齐+可复跑命令
   +构建 sha/对照认证/预算/异常附录）。不跑 verify_r45_gates、不发射。
"""
from __future__ import annotations

import gzip
import json
import multiprocessing
import sys
import time
from pathlib import Path

EV_DIR = Path(__file__).resolve().parent
R45_DIR = EV_DIR.parent
SIM_DIR = R45_DIR.parent                      # kaggle_simulations
CAMPAIGN_ROOT = SIM_DIR.parents[2]            # workspace/kaggriculture
if str(SIM_DIR) not in sys.path:
    sys.path.insert(0, str(SIM_DIR))

R45_MAIN = R45_DIR / "build" / "main.py"
R40_MAIN = SIM_DIR / "orderbook_r40" / "build" / "main.py"
CORPUS_DIR = CAMPAIGN_ROOT / "fn_docs" / "hybrid" / "results" / "replays-r30-26"
EVIDENCE_JSON = EV_DIR / "judgment_r28.json"
AUTH_JSON = EV_DIR / "sim_bridge_auth_r28.json"
COUNTER_SCRIPT = EV_DIR / "counter_wool_front_runner.py"
BUILD_DIR = R45_DIR / "build"

N_SEEDS = 60                      # 每 seated 臂独立 seed 数（×双席）
SEED_BASE = 670000                # judge_r45 契约域（局组 670000+gi*1000）
WORKERS = 8
AUTH_N = 30                       # 对照认证局数（min_checked 同值）
BUDGET_CAP = 600                  # 局次预算上限（含对照认证引擎局次）
BUILD_PARAMS = {
    "k": 4,
    "horizon": 48,
    "window": [192, 695],
}
REPRODUCE_COMMANDS = [
    "cd %s/orderbook_r45 && python3 -m pytest -q" % SIM_DIR,
    "cd %s && python3 orderbook_r45/evidence/judgment_r28_driver.py" % SIM_DIR,
]


# --------------------------------------------------------------- 反制件 --
def write_counter_script():
    """Wool Front-Runner 反制对手脚本落 evidence（judge 契约同路径）。

    判决 runner 在场时 judge 不落盘反制件（run_mirror_counter_judgment
    契约分支），由本驱动按同参 make_counter_opponent(None) 生成同一脚本。
    """
    from orderbook_predict import judge_predict as jp  # noqa: WPS433
    art = jp.make_counter_opponent(None)
    COUNTER_SCRIPT.write_text(art["script"], encoding="utf-8")
    return {"kind": art["kind"], "config": art["config"],
            "features": art.get("features"), "path": str(COUNTER_SCRIPT)}


def _fix_counter_agents(agents):
    """反制 spec（type=python/path=None/counter 元数据）→可装载 path。"""
    out = []
    for a in (agents or []):
        if isinstance(a, dict) and a.get("counter") and not a.get("path"):
            a = dict(a)
            a["path"] = str(COUNTER_SCRIPT)
        out.append(a)
    return out


# ------------------------------------------------- 真链路跑局+台账采集 --
def _chunk_run(payload):
    """一批局：j23._build_agents+sim_bridge.run_games（judge_r26._chunk 同链路）
    +逐席 _ADV_LEDGER 快照（净量恒等对账域）。单局红计入不短路。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    from orderbook_r43 import judge_r26 as j26  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    games, metas = [], []
    for spec in specs:
        spec = dict(spec)
        spec["agents"] = _fix_counter_agents(spec.get("agents"))
        try:
            agents, sinks = j23._build_agents(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
            metas.append((spec, sinks, agents, None))
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, None, None,
                          "build_error: %s" % repr(exc)[:120]))
    res = sb.run_games(games, cfg) if games else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks, agents, berr) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        seat = int(spec.get("our_seat", 0) or 0)
        row = {"game_id": spec.get("game_id"), "seed": int(spec["seed"]),
               "our_seat": seat, "arm": spec.get("arm"),
               "banks": rr.get("banks"), "error": rr.get("error")}
        if berr is not None:
            row["error"] = berr
        if row["banks"] is not None and row["error"] is None:
            banks = row["banks"]
            row["margin"] = float(banks[seat]) - float(banks[1 - seat])
            sink = sinks.get(seat) if isinstance(sinks, dict) else None
            row["reads"] = j26.realized_price_stats(sink or []) \
                if sink is not None else {}
        else:
            row["margin"] = None
            row["reads"] = {}
        # 净量恒等对账域：逐席读装载命名空间 _ADV_LEDGER（r45 实例才有）
        if row["error"] is None and agents:
            ledgers = {}
            for s_i, ag in enumerate(agents):
                inner = getattr(ag, "inner", ag)
                ns = getattr(inner, "__globals__", None)
                led = ns.get("_ADV_LEDGER") if isinstance(ns, dict) else None
                if not (isinstance(led, dict)
                        and isinstance(led.get("debts"), list)
                        and isinstance(led.get("settled"), list)):
                    continue
                key = str(row["game_id"]) if s_i == seat else \
                    "%s#opp%d" % (row["game_id"], s_i)
                ledgers[key] = {
                    "debts": [dict(r) for r in led["debts"]
                              if isinstance(r, dict)],
                    "settled": [dict(r) for r in led["settled"]
                                if isinstance(r, dict)],
                }
            if ledgers:
                row["_ledgers"] = ledgers
        out.append(row)
    return out


def make_runner(trace_harvest, ledger_harvest, counter, run_cfg_default):
    """判决 runner（judge_r45 cfg["runner"] 注入口）：真链路跑局+回填台账。"""

    def runner(specs, cfg):
        specs = [dict(s) for s in specs]
        runcfg = dict(run_cfg_default)
        if isinstance(cfg, dict):
            runcfg.update(cfg)
        workers = int(runcfg.get("workers", WORKERS) or WORKERS)
        n_chunks = max(1, min(workers * 2, max(1, len(specs))))
        tasks = [{"specs": specs[i::n_chunks], "cfg": dict(runcfg)}
                 for i in range(n_chunks)]
        tasks = [t for t in tasks if t["specs"]]
        if workers <= 1 or len(tasks) <= 1:
            parts = [_chunk_run(t) for t in tasks]
        else:
            ctx = multiprocessing.get_context("fork")
            with ctx.Pool(processes=min(workers, len(tasks))) as pool:
                parts = pool.map(_chunk_run, tasks)
        rows = []
        for part in parts:
            rows.extend(part)
        n_games = counter.setdefault("judgment_games", 0)
        counter["judgment_games"] = n_games + len(rows)
        for r in rows:
            for key, snap in (r.pop("_ledgers", None) or {}).items():
                ledger_harvest[key] = snap
                trace_harvest.append({"game_id": key})
        return rows

    return runner


# ------------------------------------------------------------ 语料解析 --
def _parse_replay(path):
    """strip 重演件→(seed, our_seat, opp_actions, episode_id, margin)。"""
    data = json.loads(gzip.open(path, "rb").read().decode("utf-8"))
    seed = data.get("seed")
    if seed is None:
        seed = (data.get("configuration") or {}).get("seed")
    if seed is None:
        seed = (data.get("info") or {}).get("seed")
    teams = list(data.get("teams")
                 or (data.get("info") or {}).get("TeamNames") or [])
    our_seat = teams.index("renyxin") if "renyxin" in teams else 0
    opp_seat = 1 - our_seat
    opp_actions = []
    for s in (data.get("steps") or []):
        act = None
        if isinstance(s, (list, tuple)) and len(s) > opp_seat:
            node = s[opp_seat]
            if isinstance(node, dict):
                act = node.get("action")
        opp_actions.append(act if isinstance(act, dict)
                           else {"farmer": ["PASS"], "hands": [], "market": []})
    margin = None
    rewards = data.get("rewards")
    if isinstance(rewards, (list, tuple)) and len(rewards) == 2 \
            and all(isinstance(x, (int, float)) for x in rewards):
        margin = float(rewards[our_seat]) - float(rewards[1 - our_seat])
    return {"seed": int(seed), "our_seat": int(our_seat),
            "actions": opp_actions,
            "episode_id": data.get("episode_id"),
            "margin": margin}


def build_control_games():
    """胜局对照组（control_win）=同库胜局（replays-r30-26 中 margin>0 局）
    tape 重演（固定席位，seated=False）。"""
    games = []
    n_win = n_loss = 0
    for p in sorted(CORPUS_DIR.glob("episode-*.json*.gz")):
        rec = _parse_replay(p)
        if rec["margin"] is None or rec["margin"] <= 0:
            n_loss += 1
            continue
        n_win += 1
        ep = rec["episode_id"] if rec["episode_id"] is not None else p.stem
        games.append({
            "game_id": "control-win-%s" % ep,
            "seed": rec["seed"], "our_seat": rec["our_seat"],
            "opponent": {"type": "tape", "actions": rec["actions"]},
        })
    return games, {"n_win": n_win, "n_loss": n_loss}


def auth_seeds():
    """对照认证种子=26 重演真种子+4 中性种子（确定性）。"""
    seeds = []
    for p in sorted(CORPUS_DIR.glob("episode-*.json*.gz")):
        rec = _parse_replay(p)
        seeds.append(rec["seed"])
    seeds += [2026092801, 2026092802, 2026092803, 2026092804]
    return seeds


# ------------------------------------------------------------------ 主线 --
def main():
    t0 = time.perf_counter()
    from orderbook_r45 import build_r45 as b45       # noqa: WPS433
    from orderbook_r45 import judge_r45 as j45       # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb       # noqa: WPS433

    print("[R28] ①build_r45（r40 底+三件套齐注）", flush=True)
    adv_src = str((R45_DIR / "advance_layer.py").resolve())
    gate_src = str((SIM_DIR / "orderbook_r44" / "quote_context.py").resolve())
    params = dict(BUILD_PARAMS)
    params["modules"] = {"debt_ledger": adv_src, "valley_gate": gate_src,
                         "advance_layer": adv_src}
    build = b45.build_r45(str(R40_MAIN), params, str(BUILD_DIR))
    print("    main_sha256:", build["main_sha256"], flush=True)
    print("    tar_sha256 :", build["tar_sha256"], flush=True)

    counter_meta = write_counter_script()
    print("[R28] ②sim_bridge 对照认证（%d 种子官方 vs 仿真）" % AUTH_N,
          flush=True)
    auth = sb.sim_bridge(
        {"n_games": AUTH_N, "min_checked": AUTH_N,
         "record_path": str(AUTH_JSON)}, corpus=auth_seeds())
    AUTH_JSON.write_text(json.dumps(auth, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")
    print("    consistency:", auth.get("consistency"),
          "ok:", auth.get("consistency_ok"),
          "speedup:", auth.get("wall_speedup"), flush=True)

    control_games, control_meta = build_control_games()
    print("[R28] ③judge_r45 真判决（n_seeds=%d，胜局对照 %d 局）"
          % (N_SEEDS, len(control_games)), flush=True)
    trace_harvest, ledger_harvest = [], {}
    counter = {}
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    runner = make_runner(trace_harvest, ledger_harvest, counter, run_cfg)
    cfg = {
        "seed_base": SEED_BASE,
        "n_seeds": N_SEEDS,
        "runner": runner,
        "traces": trace_harvest,
        "ledger": ledger_harvest,
        "control": {"games": control_games, "seated": False},
        "run_cfg": run_cfg,
        "r40_main": str(R40_MAIN),
        "evidence_path": str(EVIDENCE_JSON),
        "source": {"commands": list(REPRODUCE_COMMANDS),
                   "note": "R28 真判决：build_r45+sim_bridge 对照认证+"
                           "judge_r45 缺省六局组；台账=装载命名空间 "
                           "_ADV_LEDGER 快照（不改码采集）"},
    }
    ev = j45.judge_r45(dict(build), str(CORPUS_DIR), cfg)

    # ---- evidence 附录（契约键之外的执行面留痕） ---------------------------
    try:
        blob = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
    except Exception as exc:
        blob = dict(ev)
        blob["evidence_readback_error"] = repr(exc)[:160]
    arms = ev.get("arms") or []
    anomalies = []
    for a in arms:
        if a.get("error"):
            anomalies.append({"arm": a.get("arm"), "error": str(a["error"])[:200]})
        for key in (a.get("red_seeds") or []):
            anomalies.append({"arm": a.get("arm"), "red_seed": key})
    corpus_err = (ev.get("corpus") or {}).get("error")
    if corpus_err:
        anomalies.append({"corpus_error": str(corpus_err)[:200]})
    if not auth.get("consistency_ok"):
        anomalies.append({"bridge_auth": "对照未过（快线不成立，回退官方引擎）",
                          "reason": auth.get("degraded_reason")})
    total_games = int(counter.get("judgment_games", 0)) + 2 * AUTH_N
    blob["r28_run"] = {
        "driver": str(Path(__file__).resolve()),
        "build": {
            "base_main": str(R40_MAIN),
            "base_main_sha256": build["manifest"]["base_main_sha256"],
            "main_sha256": build["main_sha256"],
            "tar_sha256": build["tar_sha256"],
            "main_bytes": build["manifest"]["main_bytes"],
            "params_pinned": build["params_pinned"],
            "three_pieces": build["manifest"]["three_pieces"],
            "audit": build["audit"],
            "manifest_path": build["man_path"],
        },
        "bridge_auth": {
            "n_seeds": AUTH_N,
            "consistency": auth.get("consistency"),
            "consistency_ok": auth.get("consistency_ok"),
            "engine": auth.get("engine"),
            "wall_speedup": auth.get("wall_speedup"),
            "timing": auth.get("timing"),
            "kagg_version": (auth.get("install") or {}).get("version"),
            "record": str(AUTH_JSON),
        },
        "counter_opponent": counter_meta,
        "control_group": {
            "source": "fn_docs/hybrid/results/replays-r30-26 同库胜局"
                      "（margin>0）tape 重演",
            "n_games": len(control_games),
            "win_loss_split_of_library": control_meta,
        },
        "harvest": {
            "scope": "逐局逐席 r45 装载命名空间 _ADV_LEDGER 快照"
                     "（镜像臂双席均入账；r40 席无台账不入账）",
            "n_trace_records": len(trace_harvest),
            "n_ledger_records": len(ledger_harvest),
        },
        "budget": {
            "cap": BUDGET_CAP,
            "auth_engine_games": 2 * AUTH_N,
            "judgment_games": int(counter.get("judgment_games", 0)),
            "total_engine_games": total_games,
            "within_cap": total_games <= BUDGET_CAP,
        },
        "wall_clock": {
            "total_elapsed_s": round(time.perf_counter() - t0, 2),
            "judge_elapsed_s": ev.get("elapsed_s"),
        },
        "anomalies": anomalies,
        "reproduce_commands": list(REPRODUCE_COMMANDS),
        "not_run": ["verify_r45_gates（任务圈禁：不跑五门）",
                    "发射（任务圈禁：不发射；读数门由主会话定）"],
    }
    EVIDENCE_JSON.write_text(json.dumps(blob, ensure_ascii=False, indent=1,
                                        default=str) + "\n", encoding="utf-8")
    print("[R28] verdict:", ev.get("verdict"), flush=True)
    for key, row in (ev.get("criteria") or {}).items():
        print("    %-22s %-4s %s" % (key, row.get("verdict"),
                                     json.dumps(row.get("value"),
                                                ensure_ascii=False,
                                                default=str)[:160]),
              flush=True)
    print("[R28] budget:", blob["r28_run"]["budget"], flush=True)
    print("[R28] anomalies:", len(anomalies), flush=True)
    print("[R28] evidence:", EVIDENCE_JSON, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
