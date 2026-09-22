# -*- coding: utf-8 -*-
# 【中文】gates_v4b.py —— v4b 轻量轮门禁：h2h + patch_safety + P2 保险实弹
# ===========================================================================
# 门 b：h2h vs 纯 v48，8 局 = 4 种子（101/102/202/203）× AB/BA 显式席位；
#   判据=全部平局（行为级≡v48 按构造）+ **构造性证明**：每局完整动作流
#   sha256 == 同种子纯 v48 自打动作流 sha256（同行为确定性 bot 的逐字节
#   身份；非平局或哈希不等=行为不≡，如实 FAIL）。
# 门 c：patch_safety 双面——
#   ① 等价面：v4b vs 纯 v48 同种子（11/22/33/47）真引擎+孪生动作流逐字节
#      一致（P2 未触发局要求一致；触发局如实分列）；
#   ② 保险面：构造双死价局（MILK=88/WOOL=85 持续帧）经 v4b 装载实例注册
#      的 v48h.p2_economic_guard 模块实弹否决（BUY_ANIMAL 消失/
#      BUILD_PASTURE→PASS/其余原样/健康市场零触发）；附 v4b 模块注册面
#      （P1/P3 模块零注册）+ patches 单测全量。
# 归因遥测：纯 v48 轨迹上逐席评估 P2 否决（v4 轮已证 P3 单因，v4b 无 P3）。
# 产物：tmp/probes_v4b/gates_v4b.json。零修改现存文件。
# ===========================================================================
from __future__ import annotations

import json
import os
import subprocess
import sys
import time

sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))               # tmp/
_HYB = os.path.dirname(_HERE)                                     # v48_hybrid/
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
if os.path.join(_HYB, "gates") not in sys.path:
    sys.path.insert(0, os.path.join(_HYB, "gates"))

import gate_common as gc  # noqa: E402
import patch_safety as ps  # noqa: E402

V4B_MAIN = os.path.join(_HYB, "v4b", "main.py")
OUT_DIR = os.path.join(_HERE, "probes_v4b")
gc.AGENT_PATHS["v4b"] = V4B_MAIN

H2H_SEEDS = (101, 102, 202, 203)      # 纯 v48 自打双席同酬种子（h2h 基线域实测）
EQ_SEEDS = (11, 22, 33, 47)           # patch_safety 同种子域


# ---------------------------------------------------------------------------
# 归因遥测：纯 v48 轨迹上 P2 的"若在场会不会动作"评估（v4b 只含 P2）
# ---------------------------------------------------------------------------
def make_v4b_attribution():
    """装载独立 v4b 实例，抓其注册的 p2 模块（P1/P3 模块应不存在），
    在纯 v48 轨迹上逐席评估触发面。"""
    gc.load_agent(V4B_MAIN)                       # 触发 v48h.* 注册（v4b 实例）
    p2 = sys.modules["v48h.p2_economic_guard"]
    p1_present = "v48h.p1_midgame_sell_layer" in sys.modules
    p3_present = "v48h.p3_milestone_monitor" in sys.modules

    state = {"seen": set(), "p2_events": []}

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

    def summary():
        return {"p1_module_registered": p1_present,
                "p3_module_registered": p3_present,
                "modules_expected_v4b": ["v48h.p2_economic_guard"],
                "p2_veto_count": len(state["p2_events"]),
                "p2_veto_events": state["p2_events"][:8]}
    return on_step, summary


def attribution_run(seed: int) -> dict:
    on_step, tel_sum = make_v4b_attribution()
    run = gc.twin_selfplay([lambda: gc.load_agent(gc.BASE_MAIN),
                            lambda: gc.load_agent(gc.BASE_MAIN)], seed,
                           on_step=on_step)
    tel = tel_sum()
    tel["seed"] = seed
    tel["base_finals"] = run["finals"]
    return tel


# ---------------------------------------------------------------------------
# 门 c②：P2 保险实弹（v4b 注册模块 + 构造双死价局）
# ---------------------------------------------------------------------------
def p2_live_fire() -> dict:
    gc.load_agent(V4B_MAIN)
    p2 = sys.modules["v48h.p2_economic_guard"]
    p1_absent = "v48h.p1_midgame_sell_layer" not in sys.modules
    p3_absent = "v48h.p3_milestone_monitor" not in sys.modules

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

    # 反面：健康市场零触发（同一 v4b 模块）
    p2.reset_guard_state()
    healthy_out = p2.vetoe_animal_and_shed_steps([tape[0]], healthy_obs(400))
    healthy_noop = healthy_out[0] is tape[0]

    return {
        "channel": "v4b-loaded v48h.p2_economic_guard（提交字节内注册实例）",
        "p1_module_absent": p1_absent,
        "p3_module_absent": p3_absent,
        "dead_persist_steps": frames,
        "detect_series": detect,
        "activated_after_persist": activated,
        "veto_buy_animal_removed": buy_animal_gone,
        "veto_build_pasture_to_pass": pasture_pass,
        "other_orders_kept_verbatim": others_kept,
        "healthy_market_noop_same_object": healthy_noop,
        "passed": bool(activated and buy_animal_gone and pasture_pass
                       and others_kept and healthy_noop
                       and p1_absent and p3_absent),
    }


def main() -> int:
    t0 = time.perf_counter()
    os.makedirs(OUT_DIR, exist_ok=True)
    report = {"protocol": "v4b-gates-light/1.0",
              "variant_main": V4B_MAIN,
              "sha256": gc.sha256_file(V4B_MAIN), "bytes":
                  os.path.getsize(V4B_MAIN)}

    # ---- 门 b：h2h vs 纯 v48（4 种子 × AB/BA + 构造性流身份）-----------
    print(f"== h2h v4b vs pure_v48（seeds={H2H_SEEDS}，AB/BA）==", flush=True)
    base_stream = {}
    for seed in H2H_SEEDS:                       # 同种子纯 v48 自打（流身份基准）
        rb = gc.run_engine_game(gc.load_agent(gc.BASE_MAIN),
                                gc.load_agent(gc.BASE_MAIN), seed)
        base_stream[seed] = rb["action_stream_sha256"]
        print(f"  [base seed={seed}] stream={rb['action_stream_sha256'][:16]} "
              f"rewards={rb['rewards']} [{rb['wall_s']}s]", flush=True)
    games = []
    for seed in H2H_SEEDS:
        for seat in (0, 1):
            tg = time.perf_counter()
            rec = gc.run_seated_h2h("v4b", "pure_v48", seed, seat)
            stream_identity = (rec["action_stream_sha256"]
                               == base_stream[seed])
            slim = {"seed": seed, "me_seat": seat,
                    "me_money": rec["me_money"], "opp_money": rec["opp_money"],
                    "margin": round(rec["me_money"] - rec["opp_money"], 1),
                    "result": ("WIN" if rec["me_win"] else
                               "TIE" if rec["me_tie"] else "LOSS"),
                    "statuses": rec["statuses"], "turns": rec["turns_played"],
                    "anomaly_kinds": rec["anomaly_kinds"],
                    "action_stream_sha256":
                        rec["action_stream_sha256"][:16],
                    "stream_identical_to_pure_v48_selfplay": stream_identity,
                    "wall_s": round(time.perf_counter() - tg, 1)}
            games.append(slim)
            print(f"  seed={seed} seat={seat} me={slim['me_money']:9.1f} "
                  f"opp={slim['opp_money']:9.1f} margin={slim['margin']:+9.1f}"
                  f" {slim['result']:4s} statuses={slim['statuses']} "
                  f"stream_id={stream_identity} [{slim['wall_s']}s]",
                  flush=True)
    ties = sum(1 for g in games if g["result"] == "TIE")
    h2h = {"games": games, "n": len(games), "ties": ties,
           "all_done": all(g["statuses"] == ["DONE", "DONE"] for g in games),
           "criterion": "8 局全部平局 + 每局完整动作流 sha256 == 同种子纯 "
                        "v48 自打动作流（同行为确定性 bot 按构造）；"
                        "非平局/流不等=行为不≡纯 v48",
           "anomaly_kinds_seen": sorted({k for g in games
                                         for k in g["anomaly_kinds"]})}
    h2h["all_stream_identical"] = all(
        g["stream_identical_to_pure_v48_selfplay"] for g in games)
    h2h["passed"] = bool(ties == len(games) and h2h["all_done"]
                         and h2h["all_stream_identical"])
    print(f"h2h: {ties}/{len(games)} TIE all_done={h2h['all_done']} "
          f"all_stream_identical={h2h['all_stream_identical']} "
          f"passed={h2h['passed']}", flush=True)
    report["h2h_vs_pure_v48"] = h2h

    # ---- 门 c①：等价面（真引擎+孪生，同种子双自打对比）----------------
    print(f"== patch_safety 等价面 v4b vs 纯 v48（seeds={EQ_SEEDS}）==",
          flush=True)
    eq = {"real_engine": [], "twin": [], "attribution": [],
          "per_seed_classification": {}}
    for seed in EQ_SEEDS:
        rec = ps.real_engine_pair(V4B_MAIN, gc.BASE_MAIN, seed)
        eq["real_engine"].append(rec)
        print(f"  [real seed={seed}] streams_equal="
              f"{rec['streams_byte_equal']} differing_steps="
              f"{rec['differing_action_steps']} first_diff_step="
              f"{(rec['first_diffs'] or [{}])[0].get('step')} "
              f"rewards={rec['a']['rewards']} vs {rec['b']['rewards']} "
              f"done={rec['both_done']} [{rec['wall_s']}s]", flush=True)
        tw = ps.twin_pair(V4B_MAIN, gc.BASE_MAIN, seed)
        eq["twin"].append(tw)
        print(f"  [twin seed={seed}] streams_equal={tw['streams_byte_equal']}"
              f" differing_steps={tw['differing_action_steps']}", flush=True)
        tel = attribution_run(seed)
        eq["attribution"].append(tel)
        print(f"  [attr seed={seed}] p2={tel['p2_veto_count']} "
              f"p1_reg={tel['p1_module_registered']} "
              f"p3_reg={tel['p3_module_registered']}", flush=True)
        triggered = tel["p2_veto_count"] > 0
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

    # ---- 门 c②：P2 保险实弹 + patches 单测 ------------------------------
    print("== patch_safety 保险面：双死价构造 + v4b 注册模块实弹 ==", flush=True)
    live = p2_live_fire()
    print(f"  live_fire passed={live['passed']} "
          f"(activated={live['activated_after_persist']}, "
          f"buy_animal_removed={live['veto_buy_animal_removed']}, "
          f"pasture_pass={live['veto_build_pasture_to_pass']}, "
          f"healthy_noop={live['healthy_market_noop_same_object']}, "
          f"p1_absent={live['p1_module_absent']}, "
          f"p3_absent={live['p3_module_absent']})", flush=True)
    pytest = subprocess.run(
        [sys.executable, "-m", "pytest",
         os.path.join(_HYB, "patches", "test_economic_guard.py"), "-q",
         "--no-header", "-p", "no:cacheprovider"],
        capture_output=True, text=True, timeout=300)
    pytest_tail = pytest.stdout.strip().splitlines()[-1] if pytest.stdout else ""
    print(f"  patches pytest: rc={pytest.returncode} {pytest_tail}", flush=True)
    insurance = {"live_fire": live,
                 "patches_pytest": {"returncode": pytest.returncode,
                                    "tail": pytest_tail},
                 "passed": bool(live["passed"] and pytest.returncode == 0)}
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
    out = gc.write_json(os.path.join(OUT_DIR, "gates_v4b.json"), report)
    print(f"v4b gates overall passed = {report['gate']['passed']} -> {out}",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
