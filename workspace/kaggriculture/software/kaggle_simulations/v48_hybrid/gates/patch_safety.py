# -*- coding: utf-8 -*-
# 【中文】patch_safety.py —— verify_patch_safety 实局证明（F3）
# ===========================================================================
# 契约：fn_docs/responsibility.md 功能块 verify_patch_safety ← R3,R4。
#   * test_guard_inactive_equivalence（实局化）：
#     ① 注入中性证明：build --p1 off --p2 off --p3 off 旗关变体
#       （tmp/main_p000.py，三补丁零接线）vs 纯基底——同种子 ≥4 局
#       动作流逐字节一致（真引擎 + 孪生双通道），证明装载/接线框架
#       本身零扰动；
#     ② P2/P3 零影响实局：提交构建全开（main.py）vs --p1 on --p2 off
#       --p3 off（tmp/main_p100.py），同种子 ≥4 局动作流逐字节一致；
#       正常局护栏未触发=零动作（逐步 P2 否决/P3 调整遥测计数为 0）。
#       若某局动作流分叉且该局遥测显示护栏触发 → 该局改记**触发证据**
#       （预期行为）而非等价，如实分列；无触发而分叉 = FAIL。
#   * P1 归因诊断（非判据，供 FAIL 修复建议）：p100 vs 纯基底分叉步
#     计数——量化 P1 中期卖单接管的实际足迹。
# 变体构建：python build.py --p1/--p2/--p3 off 仅写 tmp/main_<tag>.py
#   （不产包不覆盖提交件；确定性双跑由 build.py 自证）。
# 产物：gates/out/patch_safety.json。CLI：python gates/patch_safety.py
#   [--quick] [--seeds 11,22,33,47]
# ===========================================================================
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import gate_common as gc  # noqa: E402

SAFETY_SEEDS = (11, 22, 33, 47)


def build_variant(p1: str, p2: str, p3: str) -> dict:
    """build.py 旗关变体构建（产物仅落 tmp/main_<tag>.py）。"""
    tag = "".join("1" if f == "on" else "0" for f in (p1, p2, p3))
    proc = subprocess.run(
        [sys.executable, os.path.join(gc.HYB, "build.py"),
         "--p1", p1, "--p2", p2, "--p3", p3],
        capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise SystemExit(f"build.py --p1 {p1} --p2 {p2} --p3 {p3} 失败:\n"
                         f"{proc.stdout[-800:]} {proc.stderr[-800:]}")
    info = json.loads(proc.stdout)
    path = info["diagnostic_build"]
    expect = os.path.join(gc.TMP_DIR, f"main_p{tag}.py")
    if path != expect:
        raise SystemExit(f"旗关变体落点异常: {path} != {expect}")
    info["sha256_verified"] = gc.sha256_file(path) == info["sha256"]
    return info


def make_p23_telemetry():
    """P2/P3 触发遥测器：装载一个独立混合实例，抓取其 v48h.* 补丁模块
    引用（与被测 agent 实例互不共享状态；P2 streak 状态逐席重置）。

    遥测在 **p100（无护栏）轨迹**上评估"若护栏在场会不会动作"：
      * P2：vetoe_animal_and_shed_steps 改写动作 = 有效触发（接线中
        P2 不受 defer 探针门控）；
      * P3：assess 判偏离且 adjust_sell_timing 实际削减卖单 = 有效触发，
        **且须与接线同仲裁**——defer 探针（终局/终盘倾销/近克隆/d0）
        为真时 P3 立正（接线语义），只记 armed 不计有效触发。"""
    gc.load_agent(gc.HYB_MAIN)              # 触发 v48h.* 注册
    p1 = sys.modules["v48h.p1_midgame_sell_layer"]
    p2 = sys.modules["v48h.p2_economic_guard"]
    p3 = sys.modules["v48h.p3_milestone_monitor"]

    state = {"seen": set(), "p2_events": [], "p3_events": [],
             "p3_armed_deferred": []}

    def _defer_frame(so):
        try:
            return bool(p1.should_defer_to_tape(so))
        except Exception:                         # noqa: BLE001
            return True                           # 探针异常→让位（接线同语义）

    def on_step(seat, obs, action):
        if seat not in state["seen"]:
            state["seen"].add(seat)
            p2.reset_guard_state()          # 该席开始：guard 状态清零
        so = gc.structify_obs(obs)
        try:
            vetoed = p2.vetoe_animal_and_shed_steps([action], so)[0]
            if gc.norm_action(vetoed) != gc.norm_action(action):
                state["p2_events"].append(
                    {"seat": seat, "step": so.get("step")})
        except Exception as e:                        # noqa: BLE001
            state["p2_events"].append(
                {"seat": seat, "step": so.get("step"), "telemetry_error":
                 repr(e)[:120]})
        try:
            step = int(so.get("step") or 0)
            deviation = p3.assess_milestone_deviation(so, step // 24)
            if isinstance(deviation, dict) and deviation.get("deviated"):
                market = action.get("market") if isinstance(action, dict) \
                    else None
                sells = [o for o in (market or [])
                         if isinstance(o, (list, tuple)) and o
                         and o[0] == "SELL"]
                if sells:
                    kept = p3.adjust_sell_timing(sells, deviation)
                    if len(kept) != len(sells):
                        if _defer_frame(so):
                            state["p3_armed_deferred"].append(
                                {"seat": seat, "step": step,
                                 "n_sells": len(sells)})
                        else:
                            state["p3_events"].append(
                                {"seat": seat, "step": step,
                                 "n_sells": len(sells), "kept": len(kept)})
        except Exception as e:                        # noqa: BLE001
            state["p3_events"].append(
                {"seat": seat, "step": None, "telemetry_error":
                 repr(e)[:120]})

    def summary():
        return {"p2_veto_events": state["p2_events"],
                "p2_veto_count": len(state["p2_events"]),
                "p3_adjust_events": state["p3_events"],
                "p3_adjust_count": len(state["p3_events"]),
                "p3_armed_but_deferred": state["p3_armed_deferred"],
                "p3_armed_deferred_count": len(state["p3_armed_deferred"])}
    return on_step, summary


def real_engine_pair(path_a: str, path_b: str, seed: int) -> dict:
    """同种子双自打局对比（真引擎）：返回流哈希/终局资金/逐字节一致性。"""
    ra = gc.run_engine_game(gc.load_agent(path_a), gc.load_agent(path_a),
                            seed)
    rb = gc.run_engine_game(gc.load_agent(path_b), gc.load_agent(path_b),
                            seed)
    diffs = gc.first_stream_diff(ra["seat_actions"], rb["seat_actions"])
    n_diff = len(gc.first_stream_diff(ra["seat_actions"], rb["seat_actions"],
                                      limit=10**9))
    return {
        "seed": seed,
        "a": {"sha": ra["action_stream_sha256"], "rewards": ra["rewards"],
              "statuses": ra["statuses"], "anoms": ra["anomaly_kinds"]},
        "b": {"sha": rb["action_stream_sha256"], "rewards": rb["rewards"],
              "statuses": rb["statuses"], "anoms": rb["anomaly_kinds"]},
        "streams_byte_equal": ra["action_stream_sha256"]
        == rb["action_stream_sha256"],
        "rewards_equal": ra["rewards"] == rb["rewards"],
        "both_done": (ra["statuses"] == ["DONE", "DONE"]
                      and rb["statuses"] == ["DONE", "DONE"]),
        "differing_action_steps": n_diff,
        "first_diffs": diffs,
        "wall_s": round(ra["wall_s"] + rb["wall_s"], 1),
    }


def twin_pair(path_a: str, path_b: str, seed: int, on_step_a=None) -> dict:
    """同种子双自打局对比（孪生通道）：流哈希/终局/逐字节一致性。"""
    ra = gc.twin_selfplay([lambda: gc.load_agent(path_a),
                           lambda: gc.load_agent(path_a)], seed,
                          on_step=on_step_a)
    rb = gc.twin_selfplay([lambda: gc.load_agent(path_b),
                           lambda: gc.load_agent(path_b)], seed)
    n_diff = len(gc.first_stream_diff(ra["streams"], rb["streams"],
                                      limit=10**9))
    return {
        "seed": seed,
        "a": {"sha": ra["action_stream_sha256"], "finals": ra["finals"]},
        "b": {"sha": rb["action_stream_sha256"], "finals": rb["finals"]},
        "streams_byte_equal": ra["action_stream_sha256"]
        == rb["action_stream_sha256"],
        "finals_equal": ra["finals"] == rb["finals"],
        "differing_action_steps": n_diff,
        "first_diffs": gc.first_stream_diff(ra["streams"], rb["streams"]),
    }


def _squash(rec, keys_stream=True):
    out = dict(rec)
    if not keys_stream:
        out.pop("first_diffs", None)
    return out


def run_patch_safety(quick: bool = False,
                     seeds=SAFETY_SEEDS) -> dict:
    print("== verify_patch_safety（实局证明）==", flush=True)
    t0 = time.perf_counter()
    seeds = list(seeds)[:2] if quick else list(seeds)

    print("-- 构建旗关变体（build.py，仅落 tmp/）--", flush=True)
    v_off = build_variant("off", "off", "off")     # main_p000.py
    v_p1 = build_variant("on", "off", "off")       # main_p100.py
    p_off_path = v_off["diagnostic_build"]
    p_p1_path = v_p1["diagnostic_build"]
    print(f"  p000: {v_off['sha256'][:12]}… {v_off['bytes']}B "
          f"(sha_verified={v_off['sha256_verified']})",
          flush=True)
    print(f"  p100: {v_p1['sha256'][:12]}… {v_p1['bytes']}B "
          f"(sha_verified={v_p1['sha256_verified']})", flush=True)

    # ---- ① 注入中性证明：p000 vs 纯基底 -------------------------------
    print(f"-- ① 中性注入：p000（三补丁零接线）vs 纯基底，seeds={seeds} --",
          flush=True)
    neutral = {"real_engine": [], "twin": []}
    for seed in seeds:
        rec = real_engine_pair(p_off_path, gc.BASE_MAIN, seed)
        neutral["real_engine"].append(_squash(rec))
        tw = twin_pair(p_off_path, gc.BASE_MAIN, seed)
        neutral["twin"].append(_squash(tw))
        print(f"  [real seed={seed}] streams_equal="
              f"{rec['streams_byte_equal']} rewards_equal="
              f"{rec['rewards_equal']} rewards={rec['a']['rewards']} "
              f"done={rec['both_done']} [{rec['wall_s']}s]", flush=True)
        print(f"  [twin seed={seed}] streams_equal="
              f"{tw['streams_byte_equal']} finals_equal="
              f"{tw['finals_equal']} finals={tw['a']['finals']}",
              flush=True)
    eq_ok = all(
        r["streams_byte_equal"] and r["rewards_equal"] and r["both_done"]
        for r in neutral["real_engine"]) and all(
        t["streams_byte_equal"] and t["finals_equal"]
        for t in neutral["twin"])
    neutral_ok = eq_ok and len(seeds) >= 4
    neutral["summary"] = {
        "n_seeds": len(seeds), "floor": 4,
        "all_streams_byte_equal": eq_ok,
        "n_seeds_floor_ok": len(seeds) >= 4,
        "interpretation": "装载/接线框架本身零扰动（旗关变体≡纯基底）",
        "passed": neutral_ok,
    }

    # ---- ② P2/P3 零影响实局：全开 vs p100 -----------------------------
    print(f"-- ② P2/P3 零影响：全开 vs p100，seeds={seeds} --", flush=True)
    p23 = {"real_engine": [], "twin": [], "telemetry": {},
           "per_seed_classification": {}}
    for seed in seeds:
        rec = real_engine_pair(gc.HYB_MAIN, p_p1_path, seed)
        p23["real_engine"].append(_squash(rec))
        print(f"  [real seed={seed}] streams_equal="
              f"{rec['streams_byte_equal']} rewards="
              f"{rec['a']['rewards']} vs {rec['b']['rewards']} "
              f"done={rec['both_done']} [{rec['wall_s']}s]", flush=True)
        # 遥测落在 p100（a=无护栏）轨迹上：正常局里护栏若在场会不会动作
        on_step, tel_sum = make_p23_telemetry()
        tw = twin_pair(p_p1_path, gc.HYB_MAIN, seed, on_step_a=on_step)
        tel = tel_sum()
        p23["twin"].append(_squash(tw))
        p23["telemetry"][str(seed)] = tel
        print(f"  [twin seed={seed}] streams_equal="
              f"{tw['streams_byte_equal']} finals="
              f"{tw['a']['finals']} vs {tw['b']['finals']}", flush=True)
        print(f"  [telemetry seed={seed}] p2_vetoes={tel['p2_veto_count']} "
              f"p3_adjusts={tel['p3_adjust_count']} "
              f"p3_armed_deferred={tel['p3_armed_deferred_count']}",
              flush=True)
        triggered = tel["p2_veto_count"] > 0 or tel["p3_adjust_count"] > 0
        equiv = (tw["streams_byte_equal"] and tw["finals_equal"]
                 and rec["streams_byte_equal"] and rec["rewards_equal"])
        if equiv and not triggered:
            cls = "equivalent_zero_trigger"   # P3 armed-deferred 允许（仲裁让位）
        elif triggered and not equiv:
            cls = "trigger_evidence"           # 护栏触发→分叉=预期行为
        else:
            cls = "UNEXPECTED_DIVERGENCE"      # 无有效触发而分叉 → FAIL
        p23["per_seed_classification"][str(seed)] = cls
        print(f"  [classify seed={seed}] {cls}", flush=True)
    n_equiv = sum(1 for c in p23["per_seed_classification"].values()
                  if c == "equivalent_zero_trigger")
    n_trig = sum(1 for c in p23["per_seed_classification"].values()
                 if c.startswith("trigger"))
    n_bad = sum(1 for c in p23["per_seed_classification"].values()
                if c == "UNEXPECTED_DIVERGENCE")
    p23["summary"] = {
        "n_seeds": len(seeds), "floor": 4,
        "n_equivalent_zero_trigger": n_equiv,
        "n_trigger_evidence": n_trig,
        "n_unexpected_divergence": n_bad,
        "effective_trigger_events": {
            s: {"p2_vetoes": p23["telemetry"][s]["p2_veto_count"],
                "p3_adjusts": p23["telemetry"][s]["p3_adjust_count"],
                "p3_armed_deferred":
                    p23["telemetry"][s]["p3_armed_deferred_count"]}
            for s in p23["telemetry"]},
        "passed": n_bad == 0 and len(seeds) >= 4,
    }

    # ---- P1 归因诊断（非判据）----------------------------------------
    print(f"-- P1 归因诊断：p100 vs 纯基底，seeds={seeds} --", flush=True)
    p1diag = {"twin": [], "real_engine": []}
    for seed in seeds:
        tw = twin_pair(p_p1_path, gc.BASE_MAIN, seed)
        p1diag["twin"].append(_squash(tw))
        rec = real_engine_pair(p_p1_path, gc.BASE_MAIN, seed)
        p1diag["real_engine"].append(_squash(rec))
        print(f"  [twin seed={seed}] streams_equal="
              f"{tw['streams_byte_equal']} differing_steps="
              f"{tw['differing_action_steps']} first_diff="
              f"{(tw['first_diffs'] or [{}])[0].get('step')}",
              flush=True)
        print(f"  [real seed={seed}] streams_equal="
              f"{rec['streams_byte_equal']} differing_steps="
              f"{rec['differing_action_steps']} rewards="
              f"{rec['a']['rewards']} vs {rec['b']['rewards']}",
              flush=True)
    p1diag["summary"] = {
        "note": "P1=中期卖单接管（常开层）；与基底分叉属预期，非安全判据；"
                "数字用于 h2h/panel FAIL 的归因与修复建议",
        "twin_differing_steps": {str(t["seed"]): t["differing_action_steps"]
                                 for t in p1diag["twin"]},
        "real_differing_steps": {str(r["seed"]): r["differing_action_steps"]
                                 for r in p1diag["real_engine"]},
        "real_rewards": {str(r["seed"]):
                         {"p100": r["a"]["rewards"],
                          "base": r["b"]["rewards"]}
                         for r in p1diag["real_engine"]},
    }

    report = {
        "protocol": "v48h-patch-safety/1.0",
        "variants": {
            "p000_neutral": {"path": p_off_path, "sha256": v_off["sha256"],
                             "bytes": v_off["bytes"]},
            "p100_p1_only": {"path": p_p1_path, "sha256": v_p1["sha256"],
                             "bytes": v_p1["bytes"]},
            "submission_all_on": {"path": gc.HYB_MAIN,
                                  "sha256": gc.sha256_file(gc.HYB_MAIN)},
            "pure_base": {"path": gc.BASE_MAIN,
                          "sha256": gc.sha256_file(gc.BASE_MAIN)},
        },
        "seeds": seeds,
        "neutral_injection_proof": neutral,
        "p23_zero_impact_proof": p23,
        "p1_attribution_diagnostic": p1diag,
        "gate": {
            "criterion": "① p000≡纯基底（≥4 种子动作流逐字节一致，真引擎"
                         "+孪生）；② 全开≡p100（≥4 种子，零触发局动作流"
                         "逐字节一致；触发局如实分列为触发证据；无触发而"
                         "分叉=FAIL）",
            "neutral_injection_passed": neutral_ok,
            "p23_zero_impact_passed": p23["summary"]["passed"],
            "passed": neutral_ok and p23["summary"]["passed"],
        },
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    out = gc.write_json(os.path.join(gc.OUT_DIR, "patch_safety.json"),
                        report)
    print(f"patch_safety passed = {report['gate']['passed']} "
          f"(neutral={neutral_ok}, p23_zero_impact="
          f"{p23['summary']['passed']}) -> {out}", flush=True)
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="v48_hybrid patch safety (F3)")
    ap.add_argument("--quick", action="store_true",
                    help="2 种子冒烟（不构成门判据）")
    ap.add_argument("--seeds", default=None,
                    help="逗号分隔种子域（默认 11,22,33,47）")
    args = ap.parse_args()
    seeds = ([int(s) for s in args.seeds.split(",")]
             if args.seeds else SAFETY_SEEDS)
    rep = run_patch_safety(quick=args.quick, seeds=seeds)
    print(json.dumps({"neutral": rep["neutral_injection_proof"]["summary"],
                      "p23": rep["p23_zero_impact_proof"]["summary"],
                      "p1_diag": rep["p1_attribution_diagnostic"]["summary"],
                      "gate": rep["gate"]},
                     ensure_ascii=False, indent=1))
    sys.exit(0 if rep["gate"]["passed"] else 1)
