# -*- coding: utf-8 -*-
# 【中文】gates_v4.py —— v4 轻量轮门禁：h2h + patch_safety + P2 保险实弹
# ===========================================================================
# 门 b：h2h vs 纯 v48，8 局 = 4 种子（101/102/202/203，纯 v48 自打席位
#   对称种子域）× AB/BA 显式席位；判据=全部平局（行为级≡v48 按构造）；
#   非平局=行为不≡，如实 FAIL。
# 门 c：patch_safety 双面——
#   ① 等价面：v4 vs 纯 v48 同种子（11/22/33/47）真引擎+孪生动作流逐字节
#      一致（P2/P3 未触发局才要求一致；触发局如实分列）；
#   ② 保险面：构造双死价局（MILK=88/WOOL=85 持续帧）经 v4 装载实例注册
#      的 v48h.p2_economic_guard 模块实弹否决（BUY_ANIMAL 消失/
#      BUILD_PASTURE→PASS/其余原样）；附 patches 单测全量（触发面覆盖）。
# 归因遥测：纯 v48 轨迹上逐席评估 P2 否决/P3 偏离（v4 首分叉定位用）。
# 产物：tmp/probes_v4/gates_v4.json。零修改现存文件。
# ===========================================================================
from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import sys
import time
import zlib

sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))               # tmp/
_HYB = os.path.dirname(_HERE)                                     # v48_hybrid/
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
if os.path.join(_HYB, "gates") not in sys.path:
    sys.path.insert(0, os.path.join(_HYB, "gates"))

import gate_common as gc  # noqa: E402
import patch_safety as ps  # noqa: E402

V4_MAIN = os.path.join(_HYB, "v4", "main.py")
OUT_DIR = os.path.join(_HERE, "probes_v4")
gc.AGENT_PATHS["v4"] = V4_MAIN

H2H_SEEDS = (101, 102, 202, 203)      # 纯 v48 自打双席同酬种子（h2h 基线域实测）
EQ_SEEDS = (11, 22, 33, 47)           # patch_safety 同种子域


# ---------------------------------------------------------------------------
# 归因遥测：纯 v48 轨迹上 P2/P3 的"若在场会不会动作"评估
# ---------------------------------------------------------------------------
def make_v4_attribution():
    """装载独立 v4 实例，抓其注册的 p2/p3 模块（P1 模块应不存在），
    在纯 v48 轨迹上逐席评估触发面。"""
    gc.load_agent(V4_MAIN)                       # 触发 v48h.* 注册（v4 实例）
    p2 = sys.modules["v48h.p2_economic_guard"]
    p3 = sys.modules["v48h.p3_milestone_monitor"]
    p1_present = "v48h.p1_midgame_sell_layer" in sys.modules
    # 注意：随后 gc.load_agent(BASE_MAIN) 不注册 v48h.*；轨迹 agent 装载会
    # 再注册新实例并替换 sys.modules 项，此处先抓局部引用即与本遥测私有。

    state = {"seen": set(), "p2_events": [], "p3_dev_steps": [],
             "p3_adjust_events": [], "first_dev": None}

    def on_step(seat, obs, action):
        if seat not in state["seen"]:
            state["seen"].add(seat)
            p2.reset_guard_state()
        so = gc.structify_obs(obs)
        try:
            vetoed = p2.vetoe_animal_and_shed_steps([action], so)[0]
            if gc.norm_action(vetoed) != gc.norm_action(action):
                state["p2_events"].append({"seat": seat, "step": so.get("step")})
        except Exception as e:                              # noqa: BLE001
            state["p2_events"].append({"seat": seat, "step": so.get("step"),
                                       "telemetry_error": repr(e)[:120]})
        try:
            step = int(so.get("step") or 0)
            dev = p3.assess_milestone_deviation(so, step // 24)
            if isinstance(dev, dict) and dev.get("deviated"):
                failed = dev.get("detail", {}).get("failed")
                rec = {"seat": seat, "step": step, "day": step // 24,
                       "failed_checks": failed}
                state["p3_dev_steps"].append(rec)
                if state["first_dev"] is None:
                    state["first_dev"] = rec
                market = action.get("market") if isinstance(action, dict) \
                    else None
                sells = [o for o in (market or [])
                         if isinstance(o, (list, tuple)) and o
                         and o[0] == "SELL"]
                if sells:
                    kept = p3.adjust_sell_timing(sells, dev)
                    if len(kept) != len(sells):
                        state["p3_adjust_events"].append(
                            {"seat": seat, "step": step, "n_sells": len(sells),
                             "kept": len(kept)})
        except Exception as e:                              # noqa: BLE001
            state["p3_dev_steps"].append({"seat": seat, "step": None,
                                          "telemetry_error": repr(e)[:120]})

    def summary():
        return {"p1_module_registered": p1_present,
                "p2_veto_count": len(state["p2_events"]),
                "p2_veto_events": state["p2_events"][:8],
                "p3_deviated_step_count": len(state["p3_dev_steps"]),
                "p3_effective_adjust_count": len(state["p3_adjust_events"]),
                "p3_adjust_events": state["p3_adjust_events"][:8],
                "first_deviation": state["first_dev"]}
    return on_step, summary


def attribution_run(seed: int) -> dict:
    on_step, tel_sum = make_v4_attribution()
    run = gc.twin_selfplay([lambda: gc.load_agent(gc.BASE_MAIN),
                            lambda: gc.load_agent(gc.BASE_MAIN)], seed,
                           on_step=on_step)
    tel = tel_sum()
    tel["seed"] = seed
    tel["base_finals"] = run["finals"]
    return tel


# ---------------------------------------------------------------------------
# 门 c②：P2 保险实弹（v4 注册模块 + 构造双死价局）
# ---------------------------------------------------------------------------
def p2_live_fire() -> dict:
    gc.load_agent(V4_MAIN)
    p2 = sys.modules["v48h.p2_economic_guard"]

    def dead_obs(step, day=13, player=0):
        return {"step": step, "day": day, "hour": 0, "player": player,
                "market": {"prices": {"MILK": 88, "WOOL": 85, "EGG": 50}}}

    def healthy_obs(step, day=13):
        return {"step": step, "day": day, "hour": 0, "player": 0,
                "market": {"prices": {"MILK": 160, "WOOL": 200, "EGG": 50}}}

    buy_animal_step = {
        "farmer": ["PASS"], "hands": [],
        "market": [["BUY_PRODUCT", "WHEAT", 4], ["HIRE"], ["HIRE"],
                   ["BUY_SEED", "MELON", 7], ["BUY_SEED", "WHEAT", 5],
                   ["BUY_ANIMAL", "SHEEP", 4]]}
    pasture_step = {
        "farmer": ["FEED"],
        "hands": [["EAST"], ["COLLECT_FERTILIZER"], ["BUILD_PASTURE"],
                  ["PLANT", "STRAWBERRY"], ["WATER"]],
        "market": [["BUY_ANIMAL", "COW", 2], ["SELL", "WOOL", 2]]}
    tape = [buy_animal_step, pasture_step]

    # 双死价持续帧推进到激活态
    p2.reset_guard_state()
    frames = p2.DEAD_PERSIST_STEPS
    detect = [p2.detect_dead_price_market(dead_obs(300 + i))
              for i in range(frames + 2)]
    activated = detect[-1]

    out = p2.vetoe_animal_and_shed_steps(tape, dead_obs(400))
    flat = [c for s in out for c in s["market"]]
    buy_animal_gone = not any(c[0] == "BUY_ANIMAL" for c in flat)
    pasture_pass = (out[1]["hands"][2] == ["PASS"]
                    and len(out[1]["hands"]) == 5)
    others_kept = out[0]["market"][:5] == buy_animal_step["market"][:5]

    # 反面：健康市场零触发（同一 v4 模块）
    p2.reset_guard_state()
    healthy_out = p2.vetoe_animal_and_shed_steps([tape[0]], healthy_obs(400))
    healthy_noop = healthy_out[0] is tape[0]

    return {
        "channel": "v4-loaded v48h.p2_economic_guard（提交字节内注册实例）",
        "dead_persist_steps": frames,
        "detect_series": detect,
        "activated_after_persist": activated,
        "veto_buy_animal_removed": buy_animal_gone,
        "veto_build_pasture_to_pass": pasture_pass,
        "other_orders_kept_verbatim": others_kept,
        "healthy_market_noop_same_object": healthy_noop,
        "passed": bool(activated and buy_animal_gone and pasture_pass
                       and others_kept and healthy_noop),
    }


def blob_identity() -> dict:
    """v4 内嵌 blob 只含 P2/P3 源（P1 模块零内嵌），源字节与 patches/ 一致。"""
    text = open(V4_MAIN, "r", encoding="utf-8").read()
    lines = text.split("\n")
    start = next(i for i, ln in enumerate(lines)
                 if ln.startswith("_V48H_MODULES = "))
    chunk = []
    for ln in lines[start + 1:]:
        if ln.startswith("    '") and ln.rstrip().endswith("'"):
            chunk.append(ln.strip()[1:-1])
        elif ln == ")" and chunk:
            break
    if not chunk:
        return {"ok": False, "error": "blob block not found"}
    blob_text = "".join(chunk)
    modules = json.loads(zlib.decompress(
        base64.b85decode(blob_text)).decode("utf-8"))
    import hashlib
    detail = {}
    for name, src in modules.items():
        fname = ("economic_guard.py" if "p2_" in name
                 else "milestone_monitor.py" if "p3_" in name
                 else "midgame_sell_layer.py")
        disk = open(os.path.join(_HYB, "patches", fname), "rb").read()
        detail[name] = {
            "embedded_sha256": hashlib.sha256(src.encode()).hexdigest(),
            "disk_sha256": hashlib.sha256(disk).hexdigest(),
            "identical": src == disk.decode("utf-8"),
        }
    return {"ok": all(v["identical"] for v in detail.values()),
            "embedded_modules": sorted(modules),
            "p1_module_absent": not any("p1_" in k for k in modules),
            "detail": detail}


def main() -> int:
    t0 = time.perf_counter()
    os.makedirs(OUT_DIR, exist_ok=True)
    report = {"protocol": "v4-gates-light/1.0",
              "variant_main": V4_MAIN,
              "sha256": gc.sha256_file(V4_MAIN), "bytes":
                  os.path.getsize(V4_MAIN)}

    # ---- 门 b：h2h vs 纯 v48（4 种子 × AB/BA）--------------------------
    print(f"== h2h v4 vs pure_v48（seeds={H2H_SEEDS}，AB/BA）==", flush=True)
    games = []
    for seed in H2H_SEEDS:
        for seat in (0, 1):
            tg = time.perf_counter()
            rec = gc.run_seated_h2h("v4", "pure_v48", seed, seat)
            slim = {"seed": seed, "me_seat": seat,
                    "me_money": rec["me_money"], "opp_money": rec["opp_money"],
                    "margin": round(rec["me_money"] - rec["opp_money"], 1),
                    "result": ("WIN" if rec["me_win"] else
                               "TIE" if rec["me_tie"] else "LOSS"),
                    "statuses": rec["statuses"], "turns": rec["turns_played"],
                    "anomaly_kinds": rec["anomaly_kinds"],
                    "action_stream_sha256":
                        rec["action_stream_sha256"][:16],
                    "wall_s": round(time.perf_counter() - tg, 1)}
            games.append(slim)
            print(f"  seed={seed} seat={seat} me={slim['me_money']:9.1f} "
                  f"opp={slim['opp_money']:9.1f} margin={slim['margin']:+9.1f}"
                  f" {slim['result']:4s} statuses={slim['statuses']} "
                  f"[{slim['wall_s']}s]", flush=True)
    ties = sum(1 for g in games if g["result"] == "TIE")
    h2h = {"games": games, "n": len(games), "ties": ties,
           "all_done": all(g["statuses"] == ["DONE", "DONE"] for g in games),
           "criterion": "8 局全部平局（两确定性同行为 bot 按构造）；"
                        "非平局=行为不≡纯 v48",
           "anomaly_kinds_seen": sorted({k for g in games
                                         for k in g["anomaly_kinds"]})}
    h2h["passed"] = bool(ties == len(games) and h2h["all_done"])
    print(f"h2h: {ties}/{len(games)} TIE all_done={h2h['all_done']} "
          f"passed={h2h['passed']}", flush=True)
    report["h2h_vs_pure_v48"] = h2h

    # ---- 门 c①：等价面（真引擎+孪生，同种子双自打对比）----------------
    print(f"== patch_safety 等价面 v4 vs 纯 v48（seeds={EQ_SEEDS}）==",
          flush=True)
    eq = {"real_engine": [], "twin": [], "attribution": [],
          "per_seed_classification": {}}
    for seed in EQ_SEEDS:
        rec = ps.real_engine_pair(V4_MAIN, gc.BASE_MAIN, seed)
        eq["real_engine"].append(rec)
        print(f"  [real seed={seed}] streams_equal="
              f"{rec['streams_byte_equal']} differing_steps="
              f"{rec['differing_action_steps']} first_diff_step="
              f"{(rec['first_diffs'] or [{}])[0].get('step')} "
              f"rewards={rec['a']['rewards']} vs {rec['b']['rewards']} "
              f"done={rec['both_done']} [{rec['wall_s']}s]", flush=True)
        tw = ps.twin_pair(V4_MAIN, gc.BASE_MAIN, seed)
        eq["twin"].append(tw)
        print(f"  [twin seed={seed}] streams_equal={tw['streams_byte_equal']}"
              f" differing_steps={tw['differing_action_steps']}", flush=True)
        tel = attribution_run(seed)
        eq["attribution"].append(tel)
        print(f"  [attr seed={seed}] p2={tel['p2_veto_count']} "
              f"p3_dev={tel['p3_deviated_step_count']} "
              f"p3_adjust={tel['p3_effective_adjust_count']} "
              f"first={tel['first_deviation']}", flush=True)
        triggered = (tel["p2_veto_count"] > 0
                     or tel["p3_effective_adjust_count"] > 0)
        equiv = tw["streams_byte_equal"] and rec["streams_byte_equal"]
        cls = ("equivalent_zero_trigger" if equiv and not triggered
               else "trigger_evidence" if triggered and not equiv
               else "UNEXPECTED_DIVERGENCE" if not equiv
               else "EQUIVALENT_WITH_TELEMETRY_MISMATCH")
        eq["per_seed_classification"][str(seed)] = cls
        print(f"  [classify seed={seed}] {cls}", flush=True)
    n_eq = sum(1 for c in eq["per_seed_classification"].values()
               if c == "equivalent_zero_trigger")
    eq["summary"] = {"n_seeds": len(EQ_SEEDS), "floor": 4,
                     "n_equivalent_zero_trigger": n_eq,
                     "n_trigger_evidence":
                         sum(1 for c in eq["per_seed_classification"].values()
                             if c == "trigger_evidence"),
                     "n_unexpected_divergence":
                         sum(1 for c in eq["per_seed_classification"].values()
                             if c == "UNEXPECTED_DIVERGENCE")}
    print(f"equivalence: {eq['summary']}", flush=True)
    report["patch_safety_equivalence"] = eq

    # ---- 门 c②：P2 保险实弹 + blob 身份 + patches 单测 -----------------
    print("== patch_safety 保险面：双死价构造 + v4 注册模块实弹 ==", flush=True)
    live = p2_live_fire()
    print(f"  live_fire passed={live['passed']} "
          f"(activated={live['activated_after_persist']}, "
          f"buy_animal_removed={live['veto_buy_animal_removed']}, "
          f"pasture_pass={live['veto_build_pasture_to_pass']}, "
          f"healthy_noop={live['healthy_market_noop_same_object']})",
          flush=True)
    ident = blob_identity()
    print(f"  blob_identity ok={ident['ok']} p1_absent={ident.get('p1_module_absent')}",
          flush=True)
    pytest = subprocess.run(
        [sys.executable, "-m", "pytest",
         os.path.join(_HYB, "patches", "test_economic_guard.py"), "-q",
         "--no-header", "-p", "no:cacheprovider"],
        capture_output=True, text=True, timeout=300)
    pytest_tail = pytest.stdout.strip().splitlines()[-1] if pytest.stdout else ""
    print(f"  patches pytest: rc={pytest.returncode} {pytest_tail}", flush=True)
    insurance = {"live_fire": live, "blob_identity": ident,
                 "patches_pytest": {"returncode": pytest.returncode,
                                    "tail": pytest_tail},
                 "passed": bool(live["passed"] and ident["ok"]
                                and pytest.returncode == 0)}
    print(f"insurance passed={insurance['passed']}", flush=True)
    report["patch_safety_insurance"] = insurance

    report["gate"] = {
        "h2h_all_ties_passed": h2h["passed"],
        "equivalence_passed": (eq["summary"]["n_equivalent_zero_trigger"]
                               >= 4
                               and eq["summary"]["n_unexpected_divergence"]
                               == 0),
        "insurance_passed": insurance["passed"],
    }
    report["gate"]["passed"] = all(report["gate"].values())
    report["wall_s"] = round(time.perf_counter() - t0, 1)
    out = gc.write_json(os.path.join(OUT_DIR, "gates_v4.json"), report)
    print(f"v4 gates overall passed = {report['gate']['passed']} -> {out}",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
