"""gate_equivalence_l3（R13 门③）：四面（形态扩展集/死种≤$900/饿死零容忍/子集）+七件构造用例。

骨架沿 gate_equivalence_v3（R12 门③，**import 复用**其 _seated_terminal/
_starve_verdict/净回收净算/_record_error 部件，零改动不制第二份）：
  (a) 形态面——diff(l3 vs verbatim)：_l1.replay_action_diff(path, l3_fn,
      verbatim_fn)，全部差异形态限于 ALLOWED_DIVERGENCE_KINDS={BUY_SEED 增/
      删（减量单自然分解为 消失+出现 一对，均在允许集）, SELL 变化}、全部差
      异步 ≥ **648**（R13 硬指标；layer_s_block._CXS_FROM 同源值，L3 单窗
      非 v3 双窗参数）；appear 只记账不设阈（减量保单天然成对增删）。
  (b) 结果面——①逐局 l3_final ≥ l1_final（1e-9；l3_final 取 (a) 路 cand 槽、
      l1_final 取 (b) 路 diff(L1 vs verbatim) 的 cand 槽）②死种合计=l3 重演
      终态我方 private.seeds×票价 ≤**$900**（R13 放宽自 v3 的 $500——钳制
      保底买入面下的死种预算重标；票价=_l1.SEED_PRICE）③饿死零容忍（v3 同款
      _starve_verdict：l3 vs L1 终态 plants/shed/inventories 逐品项不减，
      1e-9 容差）④净回收子集重验（v3 同款 _netted_recovery_products：净回收
      =逐品项 ΣBUY_SEED 消失−ΣBUY_SEED 出现，净额>0 才进
      _l1.precision_subset_check 的 dropped 面，判据 净回收 ≤ 原局未种下量）。
  (c) constructed_cases_l3()：七件——R10 三件（import test_layer_s 夹具，
      L3 尾块 layer S 截断语义不变式）+ 新四件（本目录 inject 的
      CLAMP_HELPER_SRC 独立 exec 伪上下文：钳制触发 demand+2 恰好/day28 swap
      不饿死/钳计算异常回退原 q/mode-A 休眠局零足迹）。

裁决 passed=(a)∧(b)①②③④∧(c)（fail-closed：任一局任一路 error/死种值或
终态不可读 → 对应面红；语料空 → 单条全局面 error 防空转绿灯）。evidence 落
evidence/equivalence_evidence.json（**协议 4.0**：per_game 双路+终态产物 +
form/result/subset/cases 四面指标；evidence_path 可覆写供测试 tmp 隔离）。"""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Any, Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)                                   # kaggle_simulations/
L1_DIR = os.path.normpath(os.path.join(KSIM, "orderbook_l1_derivative"))
L2_DIR = os.path.normpath(os.path.join(KSIM, "orderbook_l2_derivative"))
for _path in (L1_DIR, L2_DIR, HERE):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import gate_equivalence_precision as _l1  # noqa: E402  L1 门③（import 复用，零改动）
import gate_equivalence_v3 as _v3         # noqa: E402  v3 骨架部件（import 复用，零改动）
import inject_controller_clamp as _inj    # noqa: E402  CLAMP_HELPER_SRC 消费面（本目录）

# R13 验收硬指标（kaggressure 战役 R13 责任契约）：
DEAD_SEEDS_VALUE_CAP = 900     # l3 重演终局死种合计 ≤$900（票价估值同 _l1.SEED_PRICE）
STARVE_TOL = _v3.STARVE_TOL    # 饿死零容忍：终态产量面逐品项不减的浮点容差（1e-9）
ALLOWED_DIVERGENCE_KINDS = _l1.ALLOWED_DIVERGENCE_KINDS  # {BUY_SEED 增/删, SELL 变化}
FINAL_FACE_TOL = _v3.FINAL_FACE_TOL   # l3_final ≥ l1_final 的浮点容差（1e-9）
STEP_BOUNDARY = 648            # 全部差异步 ≥648（layer_s_block._CXS_FROM 同源；L3 单窗）
EVIDENCE_NAME = "equivalence_evidence.json"
PROTOCOL = "orderbook-l3-equivalence/4.0"

# v3 部件 import 复用（本模块全局别名，保测试 monkeypatch 面）：
_seated_terminal = _v3._seated_terminal          # seated 重演终态提取（死种+饿死面）
_starve_verdict = _v3._starve_verdict            # 饿死零容忍纯裁决
_net_recovery_by_crop = _v3._net_recovery_by_crop            # 净回收逐品项净算
_netted_recovery_products = _v3._netted_recovery_products    # (a) 路产物→subset dropped 面
_record_error = _v3._record_error                # record 级 error 归并


# ---------------------------------------------------------------------------
# 汇总裁决（纯函数；合成裁决矩阵单测直喂；v3 同款+死种帽 900+单窗 648）
# ---------------------------------------------------------------------------
def _aggregate_verdict_l3(records, subset_result, cases_result) -> Dict[str, Any]:
    """(a)形态面+(b)结果面（终局/死种/饿死）+subset+cases 汇总（纯函数）。

    form_face.ok = 无任一 error ∧ 逐局（无 violation 形态 ∧ 全部差异步 ≥
    STEP_BOUNDARY=648）∧ 非空记录集；result_face.ok = 无任一 error ∧
    finals_ok（逐局 l3_final ≥ l1_final−1e-9）∧ 死种合计 ≤
    DEAD_SEEDS_VALUE_CAP=$900 ∧ starve_free（l3 vs L1 终态三桶逐品项不减）；
    passed = form ∧ result ∧ subset（净回收子集 all_ok）∧ cases
    （constructed_cases_l3 all_pass）。per_game_summary 逐局一行（error 局
    数值面记 None/0）。"""
    records = list(records or [])
    rows: List[Dict[str, Any]] = []
    n_errors = n_violation_games = n_boundary_breach_games = 0
    n_form_clean = n_final_red = n_starve_red = 0
    appear_total, dead_total = 0, 0
    starve_violations_all: List[Dict[str, Any]] = []
    for record in records:
        error = _record_error(record)
        form = record.get("form") or {}
        result = record.get("result") or {}
        terminal = record.get("terminal")
        divergences = list(form.get("divergences") or []) if error is None else []
        kind_counts: Dict[str, int] = {}
        for entry in divergences:
            kind = entry.get("kind")
            kind_counts[kind] = kind_counts.get(kind, 0) + 1
        n_violations = sum(1 for e in divergences
                           if e.get("kind") not in ALLOWED_DIVERGENCE_KINDS)
        steps = [int(e["step"]) for e in divergences]
        boundary_ok = all(step >= STEP_BOUNDARY for step in steps)
        appear_count = kind_counts.get("buy_seed_appear", 0)
        l3_final = form.get("l1_final") if error is None else None     # (a) 路 cand 槽=l3
        l1_final = result.get("l1_final") if error is None else None   # (b) 路 cand 槽=L1
        verbatim_final = form.get("verbatim_final") if error is None else None
        finals_ok = (error is None
                     and isinstance(l3_final, (int, float))
                     and isinstance(l1_final, (int, float))
                     and (float(l3_final) - float(l1_final)) >= -FINAL_FACE_TOL)
        l3_term = (terminal or {}).get("l3") if error is None else None
        l1_term = (terminal or {}).get("l1") if error is None else None
        if error is None and not (isinstance(terminal, dict)
                                  and isinstance(l3_term, dict)
                                  and isinstance(l1_term, dict)):
            error = "terminal face missing/ill-typed (fail-closed)"
            l3_term = l1_term = None
        dead_value = (l3_term or {}).get("seeds_value") if error is None else None
        if error is None and not (isinstance(dead_value, (int, float))
                                  and not isinstance(dead_value, bool)):
            error = "dead seeds value missing/ill-typed (fail-closed)"  # 结构破损=红
            dead_value = None
        starve = None
        if error is None:
            try:
                starve = _starve_verdict(l3_term, l1_term)
            except Exception as exc:
                error = f"starve metrics unreadable (fail-closed): {type(exc).__name__}: {exc}"
        if starve is not None and not starve["ok"]:
            n_starve_red += 1
            starve_violations_all.extend(
                {"episode": record.get("episode"), **v} for v in starve["violations"])
        form_ok = (error is None and n_violations == 0 and boundary_ok)
        netted = _net_recovery_by_crop(divergences) if error is None else {}
        dropped = list(form.get("dropped") or []) if error is None else []
        try:
            dropped_value = sum(int(e["qty"]) * _l1.SEED_PRICE[e["crop"]]
                                for e in dropped)
        except (KeyError, TypeError, ValueError):
            dropped_value = None  # 产物畸形：不崩编排面，数值面记 None
        net_recovery_value = sum(qty * _l1.SEED_PRICE.get(crop, 0)
                                 for crop, qty in netted.items())
        if error is not None:
            n_errors += 1
        else:
            appear_total += appear_count
            dead_total += int(dead_value or 0)
            if n_violations == 0 and boundary_ok:
                n_form_clean += 1
            else:
                if n_violations:
                    n_violation_games += 1
                if not boundary_ok:
                    n_boundary_breach_games += 1
            if not finals_ok:
                n_final_red += 1
        final_delta = ((l3_final - l1_final)
                       if isinstance(l3_final, (int, float))
                       and isinstance(l1_final, (int, float)) else None)
        rows.append({
            "episode": record.get("episode"), "seat": record.get("seat"),
            "error": error, "form_ok": form_ok,
            "n_violations": n_violations if error is None else 0,
            "steps_boundary_ok": boundary_ok if error is None else None,
            "min_divergence_step": min(steps) if steps else None,
            "kind_counts": kind_counts, "appear_count": appear_count,
            "n_dropped": len(dropped), "dropped_value_est": dropped_value,
            "net_recovery_value_est": net_recovery_value if error is None else None,
            "final_face_ok": finals_ok if error is None else None,
            "l3_final": l3_final, "l1_final": l1_final,
            "verbatim_final": verbatim_final, "final_delta": final_delta,
            "dead_seeds_value": dead_value,
            "dead_seeds": (l3_term or {}).get("seeds") if error is None else None,
            "starve_ok": (starve["ok"] if error is None and starve is not None
                          else None),
            "n_starve_violations": (len(starve["violations"])
                                    if error is None and starve is not None else 0),
            "starve_violations": (starve["violations"]
                                  if error is None and starve is not None else None),
            "l3_plants": (l3_term or {}).get("plants") if error is None else None,
            "l1_plants": (l1_term or {}).get("plants") if error is None else None,
            "l3_shed": (l3_term or {}).get("shed") if error is None else None,
            "l1_shed": (l1_term or {}).get("shed") if error is None else None,
        })
    n_records = len(records)
    form_face = {
        "ok": bool(n_records and n_errors == 0 and n_form_clean == n_records),
        "n_games": n_records, "n_game_clean": n_form_clean,
        "n_violation_games": n_violation_games,
        "n_boundary_breach_games": n_boundary_breach_games,
        "n_error_games": n_errors,
        "appear_total": appear_total,  # 只记账不设阈（减量保单天然成对增删）
        "criteria": {
            "allowed_kinds": list(ALLOWED_DIVERGENCE_KINDS),
            "step_boundary": {"threshold": STEP_BOUNDARY,
                              "source": "R13 硬指标：差异步 ≥648"
                                        "（layer_s_block._CXS_FROM 同源；L3 单窗）"},
        },
    }
    result_face = {
        "ok": bool(n_records and n_errors == 0 and n_final_red == 0
                   and dead_total <= DEAD_SEEDS_VALUE_CAP and n_starve_red == 0),
        "n_games": n_records,
        "finals_ok": bool(n_records and n_errors == 0 and n_final_red == 0),
        "n_final_face_games_red": n_final_red,
        "final_face_criteria": "l3_final >= l1_final - 1e-9 per game",
        "dead_seeds_total_value": dead_total,
        "dead_seeds_cap": DEAD_SEEDS_VALUE_CAP,
        "dead_seeds_source": "l3 seated 重演终态 private.seeds × _l1.SEED_PRICE",
        "starve_free": bool(n_records and n_errors == 0 and n_starve_red == 0),
        "n_starve_games_red": n_starve_red,
        "starve_criteria": "l3 vs L1 终态 plants/shed/inventories 逐品项不减"
                           "（-1e-9 容差；任一减产=红）",
        "starve_violations": starve_violations_all,
    }
    subset = bool(subset_result.get("all_ok"))
    cases = bool(cases_result.get("all_pass"))
    return {"passed": bool(form_face["ok"] and result_face["ok"]
                           and subset and cases),
            "form_face": form_face, "result_face": result_face,
            "subset": subset, "cases": cases,
            "per_game_summary": rows, "n_errors": n_errors}


# ---------------------------------------------------------------------------
# 构造用例（(c) 面：七件）
# ---------------------------------------------------------------------------
def _clamp_ns(tape, ca_buffer: int = 8, ca_to: int = 28) -> Dict[str, Any]:
    """伪上下文独立 exec CLAMP_HELPER_SRC（test_build_l4 同款装载面）。

    tape 可为 dict（t→act；缺省步 {}）或 callable(seat, t)→act；注入
    _ca_tape/_CA_BUFFER/_CA_TO 三依赖（注入态三者均定义于插入点之前，
    语义一致）。返回 ns（含 _ca_future_plant_demand/_ca_clamped_target）。"""
    if callable(tape):
        tape_fn = tape
    else:
        mapping = dict(tape or {})
        tape_fn = lambda seat, t: mapping.get(t, {})  # noqa: E731
    ns: Dict[str, Any] = {"_CA_BUFFER": ca_buffer, "_CA_TO": ca_to,
                          "_ca_tape": tape_fn}
    exec(compile(_inj.CLAMP_HELPER_SRC, "<clamp_helper_l3>", "exec"), ns)
    return ns


def _clamp_tape(k_carrot: int = 0, m_wheat: int = 0, carrot_start: int = 650,
                wheat_start: int = 673, anchor: int = 660) -> Dict[int, dict]:
    """route2 后缀伪磁带：k 个 PLANT,CARROT（day≥27 起不限天）+ m 个
    PLANT,WHEAT（默认 t=673 起 day28 swap 窗内）+ 可读性锚（k=m=0 表示
    "磁带可读但零未来种植"而非"读不到"——两语义 helper 侧可分）。"""
    tape: Dict[int, dict] = {anchor: {"farmer": ["PASS"], "hands": []}}
    for i in range(k_carrot):
        tape[carrot_start + i] = {"farmer": ["PLANT", "CARROT"], "hands": []}
    for i in range(m_wheat):
        tape[wheat_start + i] = {"farmer": ["PLANT", "WHEAT"], "hands": []}
    return tape


def _case_clamp_trigger_demand_plus_two() -> Dict[str, Any]:
    """新④-1 钳制触发恰好 demand+2：伪磁带 k 胡萝卜+m 小麦 →
    demand=k+m、target=min(8, k+m+2)（+2 安全边；封顶 8）。"""
    points, evid = [], []
    for k, m in ((0, 0), (1, 0), (0, 1), (3, 2), (6, 3), (10, 0), (2, 7)):
        ns = _clamp_ns(_clamp_tape(k, m))
        demand = ns["_ca_future_plant_demand"](0, 650)
        target = ns["_ca_clamped_target"](27, 0, 650)
        want = min(8, k + m + 2)
        points.append(demand == k + m and target == want)
        evid.append(f"k={k},m={m}: demand={demand} target={target} "
                    f"(expect {k + m}/{want})")
    ok = all(points)
    return {"expected": True, "got": ok,
            "evidence": "; ".join(evid) + (" ; ALL OK"
                                           if ok else " ; FAIL")}


def _case_day28_swap_no_starve() -> Dict[str, Any]:
    """新④-2 day28 swap 不饿死：demand 含小麦槽（day≤28 窗内 PLANT,WHEAT 全
    计入）时 target ≥ 需求（安全边 +2 覆盖 swap 换种消耗；demand≤8 物理上界
    内恒成立）；且小麦确计入 demand（同 k 下 m>0 抬需求）。"""
    points, evid = [], []
    for k, m in ((0, 1), (1, 2), (2, 6), (4, 4), (6, 2), (0, 8), (3, 3)):
        ns = _clamp_ns(_clamp_tape(k, m))
        demand = ns["_ca_future_plant_demand"](0, 650)
        target = ns["_ca_clamped_target"](27, 0, 650)
        points.append(demand == k + m and target >= demand)
        evid.append(f"k={k},m={m}: demand={demand} target={target} "
                    f"(target>=demand: {target >= demand})")
    with_wheat = _clamp_ns(_clamp_tape(2, 2))["_ca_future_plant_demand"](0, 650)
    without_wheat = _clamp_ns(_clamp_tape(2, 0))["_ca_future_plant_demand"](0, 650)
    points.append(with_wheat == 4 and without_wheat == 2)   # 小麦槽确计入
    evid.append(f"wheat counted: with={with_wheat} without={without_wheat}")
    ok = all(points)
    return {"expected": True, "got": ok,
            "evidence": "; ".join(evid) + (" ; ALL OK"
                                           if ok else " ; FAIL")}


def _case_clamp_fallback_returns_buffer() -> Dict[str, Any]:
    """新④-3 钳计算异常回退原 q：磁带读不到（后缀无可读步条目）→demand None
    →target=_CA_BUFFER(8)；磁带抛异常→8；磁带返回非 dict→8（fail-safe 永不
    抛，回退 q 原公式行为）。"""
    def _boom(seat, t):
        raise RuntimeError("tape down")

    checks = {
        "empty_tape": _clamp_ns({}),
        "raising_tape": _clamp_ns(_boom),
        "nondict_tape": _clamp_ns(lambda seat, t: "not-a-dict"),
    }
    points, evid = [], []
    for label, ns in checks.items():
        demand = ns["_ca_future_plant_demand"](0, 650)
        target = ns["_ca_clamped_target"](27, 0, 650)
        points.append(demand is None and target == 8)
        evid.append(f"{label}: demand={demand} target={target}")
    ok = all(points)
    return {"expected": True, "got": ok,
            "evidence": "; ".join(evid) + (" ; ALL OK"
                                           if ok else " ; FAIL")}


def _case_mode_a_dormant_zero_footprint() -> Dict[str, Any]:
    """新④-4 mode-A 休眠局零足迹：day<27 表达式走原 _CA_BUFFER——helper 防御
    性直回且**磁带零查询**（记录型 tape 断言 day26 求值零调用；day27 同
    tape 查询非空，证门控在 day 而非桩）。"""
    calls: List[Any] = []
    tape = _clamp_tape(2, 1)
    ns = _clamp_ns(lambda seat, t: calls.append((seat, t)) or tape.get(t, {}))
    dormant = ns["_ca_clamped_target"](26, 0, 620)
    dormant_calls = len(calls)
    active = ns["_ca_clamped_target"](27, 0, 650)
    active_calls = len(calls) - dormant_calls
    ok = (dormant == 8 and dormant_calls == 0          # 休眠：原目标+磁带零足迹
          and active == min(8, 3 + 2) and active_calls > 0)  # 激活：确走磁带
    return {"expected": True, "got": ok,
            "evidence": f"day26 target={dormant} tape_calls={dormant_calls} "
                        f"(expect 8/0); day27 target={active} "
                        f"tape_calls={active_calls} (expect 5/>0)"}


def constructed_cases_l3() -> dict:
    """七构造用例：R10 三件（import test_layer_s 夹具——L3 尾块 layer S 截断
    语义不变式，真值仍在 test_layer_s 防漂移）+新四件（CLAMP_HELPER_SRC 独立
    exec 伪上下文：钳制触发/day28 swap 不饿死/异常回退/mode-A 零足迹）。

    夹具异常=该例失败（不向上传播，门级红由 all_pass=False 承载）。返回
    {c1…c7 各例 {pass, evidence}, c3 双面, all_pass}。"""
    import test_layer_s as tls   # 夹具库（L1_DIR 已在 sys.path）

    def _verdict(case):
        ok = case["got"] == case["expected"]
        detail = case["evidence"] if ok else (
            f'{case["evidence"]}; FAIL got={case["got"]!r} '
            f'expected={case["expected"]!r}')
        return {"pass": ok, "evidence": detail}

    def _adjudicate(thunk):
        try:
            return _verdict(thunk())
        except Exception as exc:
            return {"pass": False,
                    "evidence": f"fixture raised {type(exc).__name__}: {exc}"}

    c1 = _adjudicate(tls._invariant_case_c1_no_trunc_when_future_plant)
    c2 = _adjudicate(tls._invariant_case_c2_trunc_when_no_opportunity)
    try:
        sides = tls._invariant_case_c3_s671_boundary()
        c3_trunc = _verdict(sides["truncate_side"])
        c3_keep = _verdict(sides["keep_side"])
    except Exception as exc:  # 双面夹具共享一次调用：异常=双面俱败
        evidence = f"fixture raised {type(exc).__name__}: {exc}"
        c3_trunc = {"pass": False, "evidence": evidence}
        c3_keep = {"pass": False, "evidence": evidence}
    c4 = _adjudicate(_case_clamp_trigger_demand_plus_two)
    c5 = _adjudicate(_case_day28_swap_no_starve)
    c6 = _adjudicate(_case_clamp_fallback_returns_buffer)
    c7 = _adjudicate(_case_mode_a_dormant_zero_footprint)
    return {
        "c1_no_trunc_when_future_plant": c1,
        "c2_trunc_when_no_opportunity": c2,
        "c3_s671_boundary": {
            "truncate_side": c3_trunc, "keep_side": c3_keep,
            "pass": c3_trunc["pass"] and c3_keep["pass"],
        },
        "c4_clamp_trigger_demand_plus_two": c4,
        "c5_day28_swap_no_starve": c5,
        "c6_clamp_fallback_returns_buffer": c6,
        "c7_mode_a_dormant_zero_footprint": c7,
        "all_pass": bool(c1["pass"] and c2["pass"] and c3_trunc["pass"]
                         and c3_keep["pass"] and c4["pass"] and c5["pass"]
                         and c6["pass"] and c7["pass"]),
    }


# ---------------------------------------------------------------------------
# 门③主体
# ---------------------------------------------------------------------------
def run(episodes_dir, l3_main, l1_main, verbatim_main, limit=None,
        evidence_path=None) -> dict:
    """两路重演+终态提取+四面裁决 → {passed, form_face, result_face, subset,
    cases, per_game_summary, n_errors, evidence_path}。

    编排（v3 同款）：① _l1._discover_replays 按局号升序发现语料（limit 截前
    N 局）；② 三 callable 装载一次跨局复用（_l1._as_callable，接受路径/
    callable）；③ 逐局两路 _l1.replay_action_diff——(a) 路 cand=l3/control=
    verbatim（形态面+净回收消费面），(b) 路 cand=L1/control=verbatim（结果面
    finals 来源）；(a) 路无 error 再做终态提取（_seated_terminal 两遍：l3
    死种+饿死面、L1 饿死对照面）；④ (a) 路产物经净回收净算
    （_netted_recovery_products）喂 _l1.precision_subset_check；⑤
    constructed_cases_l3()；⑥ _aggregate_verdict_l3 汇总（步界 648/死种帽
    900）。evidence 落 <本包>/evidence/equivalence_evidence.json（可覆写），
    协议 4.0：per_game 双路+终态产物 + 四面指标。语料目录空/坏 → 单条全局面
    error 记录（四面俱红，防空转绿灯）。"""
    t0 = time.perf_counter()
    replays: List[str] = []
    discovery_note = None
    try:
        replays = _l1._discover_replays(episodes_dir, limit)
    except OSError as exc:
        discovery_note = f"{type(exc).__name__}: {exc}"
    records: List[Dict[str, Any]] = []
    if not replays:
        reason = discovery_note or (
            f"episodes_dir 无 episode-*-strip.json.gz 语料: "
            f"{os.path.abspath(episodes_dir)}")
        records.append({"episode": None, "seat": None,
                        "error": f"语料发现失败: {reason}",
                        "form": None, "result": None, "terminal": None})
    load_error = None
    if replays:
        try:
            l3_fn = _l1._as_callable(l3_main)
            l1_fn = _l1._as_callable(l1_main)
            vb_fn = _l1._as_callable(verbatim_main)
        except Exception as exc:
            load_error = f"装载/语料失败: {type(exc).__name__}: {exc}"
    for path in replays:
        ep = _l1._episode_from_path(path)
        if load_error is not None:  # 装载失败：逐局记 error（fail-closed 留痕）
            records.append({"episode": ep, "seat": None, "error": load_error,
                            "form": None, "result": None, "terminal": None})
            continue
        try:
            form = _l1.replay_action_diff(path, l3_fn, vb_fn)
        except Exception as exc:  # 叶内已自包 error；此处兜底防编排面逃逸
            form = {"error": f"{type(exc).__name__}: {exc}"}
        try:
            result = _l1.replay_action_diff(path, l1_fn, vb_fn)
        except Exception as exc:
            result = {"error": f"{type(exc).__name__}: {exc}"}
        terminal = None
        if form.get("error") is None:  # (a) 路成形才取终态；否则该局已红
            try:
                terminal = {"l3": _seated_terminal(path, l3_fn),
                            "l1": _seated_terminal(path, l1_fn)}
            except Exception as exc:
                terminal = {"error": f"{type(exc).__name__}: {exc}"}
        seat = form.get("seat")
        if seat is None:
            seat = result.get("seat")
        records.append({"episode": ep, "seat": seat, "error": None,
                        "form": form, "result": result, "terminal": terminal})

    form_products = [r["form"] for r in records if r["form"] is not None]
    subset_result = _l1.precision_subset_check(
        _netted_recovery_products(form_products))
    try:
        cases_result = constructed_cases_l3()
    except Exception as exc:  # import/夹具面逃逸 → cases 红（fail-closed）
        cases_result = {"all_pass": False,
                        "error": f"{type(exc).__name__}: {exc}"}
    aggregate = _aggregate_verdict_l3(records, subset_result, cases_result)

    target = os.path.abspath(evidence_path or os.path.join(
        HERE, "evidence", EVIDENCE_NAME))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    evidence = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "protocol": PROTOCOL,
        "inputs": {
            "episodes_dir": os.path.abspath(episodes_dir),
            "n_replays": len(replays),
            "replays": [os.path.basename(p) for p in replays],
            "limit": limit,
            "step_boundary": STEP_BOUNDARY,
            "l3_main": l3_main if isinstance(l3_main, str) else "<callable>",
            "l1_main": l1_main if isinstance(l1_main, str) else "<callable>",
            "verbatim_main": (verbatim_main if isinstance(verbatim_main, str)
                              else "<callable>"),
        },
        "form_face": aggregate["form_face"],
        "result_face": aggregate["result_face"],
        "subset": subset_result,
        "subset_netting": {
            "note": "净回收=逐品项 ΣBUY_SEED 消失−ΣBUY_SEED 出现（减量单自然分解"
                    "对；appear 是 l3 实际持有的购买不入回收）；净额>0 才进 "
                    "precision_subset_check 的 dropped 面，判据 净回收 ≤ 原局未种下量",
        },
        "cases": cases_result,
        "verdict": {
            "form_face": aggregate["form_face"]["ok"],
            "result_face": aggregate["result_face"]["ok"],
            "subset": aggregate["subset"],
            "cases": aggregate["cases"],
            "passed": aggregate["passed"],
        },
        "per_game": records,  # 逐局双路+终态产物全量，保留不截断
        "wall_total_s": round(time.perf_counter() - t0, 1),
    }
    with open(target, "w", encoding="utf-8") as fh:
        json.dump(evidence, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    aggregate["evidence_path"] = target
    return aggregate
