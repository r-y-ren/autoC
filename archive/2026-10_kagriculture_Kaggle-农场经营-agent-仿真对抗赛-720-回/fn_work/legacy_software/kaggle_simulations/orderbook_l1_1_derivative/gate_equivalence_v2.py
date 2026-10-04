"""gate_equivalence_v2（R11 门③）：形态面(appear≤2)+结果面(≥L1/死种≤$900)+子集重验+五件构造用例。

编排（L1 门③ gate_equivalence_precision 的 import 复用版，逐局两路重演）：
  (a) 形态面——diff(v2 vs verbatim)：_l1.replay_action_diff(path, v2_fn,
      verbatim_fn)（cand=v2、control=verbatim 保真对照），全部差异形态限于
      ALLOWED_DIVERGENCE_KINDS={BUY_SEED 增/删, SELL 变化}、全部差异步 ≥
      _CXS_FROM 同源阈值 648，且 26 局 buy_seed_appear **总数 ≤2**（R11 验收
      硬指标：净口径下回买面近零）。
  (b) 结果面——第二路 diff(L1 vs verbatim)（cand=L1、control=verbatim）取逐局
      finals：v2_final ≥ l1_final（1e-9，R11 验收"逐局 v2 终局资金 ≥ L1"）；
      v2 重演终局死种合计 ≤$900（死种=v2 重演终态我方 private.seeds × 票价，
      票价=_l1.SEED_PRICE；经 L1 内部件 _load_strip_replay/_my_seat/_twin/
      _obs_dict + twin.step 同款驱动循环取终态——L1 _seated_replay 只回
      final_money 不回终态，契约明示"或等价通道"）；净截断子集重验：
      dropped(v2 vs verbatim 的 BUY_SEED 消失汇总) ≤ 原局该品项未种下量
      （_l1.precision_subset_check 原样消费 (a) 路产物，replay_path 定位语料）。
  (c) constructed_cases_v2()：R10 三件 import test_layer_s 夹具（在 v2 块上
      重演，夹具全局 layer_s_block 临时改指——test_layer_s_v2
      ._run_fixture_under 复用）+ v2 两件（c4 净覆盖回买单删/c5 真需求保留，
      构造函数 import 复用 test_layer_s_v2）。

裁决 passed=(a)∧(b)∧(c)（fail-closed：任一局任一路 error/死种值不可读 →
对应面红；语料空 → 单条全局面 error 防空转绿灯）。evidence 落本包
evidence/equivalence_evidence.json（协议 2.0：per_game 双路产物 + form/
result/subset/cases 四面指标；evidence_path 可覆写供测试 tmp 隔离）。
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)                                   # kaggle_simulations/
L1_DIR = os.path.normpath(os.path.join(KSIM, "orderbook_l1_derivative"))
for _path in (L1_DIR, HERE):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import gate_equivalence_precision as _l1  # noqa: E402  L1 门③（import 复用，零改动）

# R11 验收硬指标（kaggressure 战役 R11 责任契约）：
APPEAR_CAP = 2                # 26 局 buy_seed_appear 总数 ≤2（回买面近零）
DEAD_SEEDS_VALUE_CAP = 900    # v2 重演终局死种合计 ≤$900（票价估值同 _l1.SEED_PRICE）
ALLOWED_DIVERGENCE_KINDS = _l1.ALLOWED_DIVERGENCE_KINDS  # {增/删/SELL 变化}
FINAL_FACE_TOL = 1e-9         # v2_final ≥ l1_final 的浮点容差（L1 门同款）
EVIDENCE_NAME = "equivalence_evidence.json"
PROTOCOL = "orderbook-l11-equivalence/2.0"
V2_BLOCK_NAME = "layer_s_block_v2.py"


# ---------------------------------------------------------------------------
# 死种提取（等价通道：L1 内部件复用）
# ---------------------------------------------------------------------------
def _v2_dead_seeds(replay_path, v2_fn) -> Dict[str, Any]:
    """v2 seated 重演终态我方死种：{seeds:{crop:qty}, value:Σ qty×票价}。

    等价通道（契约明示）：L1 的 _seated_replay 只回 final_money 不回终态——
    死种需终态 private["seeds"]，故以同款驱动循环（复用 _l1._twin/_obs_dict/
    _load_strip_replay/_my_seat + twin.step；对手席逐字重放 recorded 动作流，
    我席 v2_fn 实驱）跑至终局后直读 private["seeds"]。品项归一化五种子品项
    （_l1.SEED_PRICE 键序，缺项补 0，与 _l1._strip_unplanted_seeds 同口径）。
    agent 调用/引擎步进异常向上抛（→ 该局 error，fail-closed）。
    """
    replay = _l1._load_strip_replay(replay_path)
    me = _l1._my_seat(replay)
    recorded = _l1._twin().replay_transition_actions(replay)
    if not recorded:
        raise ValueError("replay 无转移动作流")
    twin = _l1._twin()
    state = twin.build_state_from_replay(replay, 0, twin.load_engine())
    taken = 0
    while not state.env.done and taken < len(recorded):
        obs = _l1._obs_dict(state, me)
        pair = [recorded[taken][1 - me]] * 2
        pair[me] = v2_fn(obs)
        twin.step(state, pair)
        taken += 1
    priv = state.seats[me].observation.private
    raw = (priv.get("seeds") or {}) if isinstance(priv, dict) else {}
    seeds = {crop: int(raw.get(crop) or 0) for crop in _l1.SEED_PRICE}
    value = sum(qty * _l1.SEED_PRICE[crop] for crop, qty in seeds.items())
    return {"seeds": seeds, "value": int(value)}


# ---------------------------------------------------------------------------
# 汇总裁决（纯函数；合成裁决矩阵单测直喂）
# ---------------------------------------------------------------------------
def _record_error(record) -> Optional[str]:
    """record 级 error 归并：自身 error 或 form/result/dead_seeds 任一 error。"""
    if record.get("error") is not None:
        return str(record["error"])
    for key in ("form", "result", "dead_seeds"):
        part = record.get(key)
        if isinstance(part, dict) and part.get("error") is not None:
            return str(part["error"])
    return None


def _aggregate_verdict(records, subset_result, cases_result) -> Dict[str, Any]:
    """(a)形态面+(b)结果面+subset+cases 汇总（纯函数，合成产物直喂单测）。

    form_face.ok = 无任一 error ∧ 逐局（无 violation 形态 ∧ 全部差异步 ≥
    _CXS_FROM 同源阈值）∧ buy_seed_appear 总数 ≤ APPEAR_CAP ∧ 非空记录集；
    result_face.ok = 无任一 error ∧ 逐局 v2_final ≥ l1_final−1e-9 ∧ 死种合计
    ≤ DEAD_SEEDS_VALUE_CAP ∧ 非空记录集；passed = form ∧ result ∧ subset
    （_l1.precision_subset_check.all_ok）∧ cases（constructed_cases_v2
    .all_pass）。per_game_summary 逐局一行（error 局数值面记 None/0）。"""
    threshold = _l1._cxs_from()
    records = list(records or [])
    rows: List[Dict[str, Any]] = []
    n_errors = n_violation_games = n_boundary_breach_games = 0
    n_form_clean = n_final_red = 0
    appear_total, dead_total = 0, 0
    for record in records:
        error = _record_error(record)
        form = record.get("form") or {}
        result = record.get("result") or {}
        dead = record.get("dead_seeds") or {}
        divergences = list(form.get("divergences") or []) if error is None else []
        kind_counts: Dict[str, int] = {}
        for entry in divergences:
            kind = entry.get("kind")
            kind_counts[kind] = kind_counts.get(kind, 0) + 1
        n_violations = sum(1 for e in divergences
                           if e.get("kind") not in ALLOWED_DIVERGENCE_KINDS)
        steps = [int(e["step"]) for e in divergences]
        boundary_ok = all(step >= threshold for step in steps)
        appear_count = kind_counts.get("buy_seed_appear", 0)
        v2_final = form.get("l1_final") if error is None else None     # (a) 路 cand 槽=v2
        l1_final = result.get("l1_final") if error is None else None   # (b) 路 cand 槽=L1
        verbatim_final = form.get("verbatim_final") if error is None else None
        finals_ok = (error is None
                     and isinstance(v2_final, (int, float))
                     and isinstance(l1_final, (int, float))
                     and (float(v2_final) - float(l1_final)) >= -FINAL_FACE_TOL)
        dead_value = dead.get("value") if error is None else None
        if (error is None and not (isinstance(dead_value, (int, float))
                                   and not isinstance(dead_value, bool))):
            error = "dead seeds value missing/ill-typed (fail-closed)"  # 结构破损=红
            dead_value = None
        form_ok = (error is None and n_violations == 0 and boundary_ok)
        dropped = list(form.get("dropped") or []) if error is None else []
        try:
            dropped_value = sum(int(e["qty"]) * _l1.SEED_PRICE[e["crop"]]
                                for e in dropped)
        except (KeyError, TypeError, ValueError):
            dropped_value = None  # 产物畸形：不崩编排面，数值面记 None
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
        final_delta = ((v2_final - l1_final)
                       if isinstance(v2_final, (int, float))
                       and isinstance(l1_final, (int, float)) else None)
        rows.append({
            "episode": record.get("episode"), "seat": record.get("seat"),
            "error": error, "form_ok": form_ok,
            "n_violations": n_violations if error is None else 0,
            "steps_boundary_ok": boundary_ok if error is None else None,
            "min_divergence_step": min(steps) if steps else None,
            "kind_counts": kind_counts, "appear_count": appear_count,
            "n_dropped": len(dropped), "dropped_value_est": dropped_value,
            "final_face_ok": finals_ok if error is None else None,
            "v2_final": v2_final, "l1_final": l1_final,
            "verbatim_final": verbatim_final, "final_delta": final_delta,
            "dead_seeds_value": dead_value,
            "dead_seeds": dead.get("seeds") if error is None else None,
        })
    n_records = len(records)
    form_face = {
        "ok": bool(n_records and n_errors == 0
                   and n_form_clean == n_records
                   and appear_total <= APPEAR_CAP),
        "n_games": n_records, "n_game_clean": n_form_clean,
        "n_violation_games": n_violation_games,
        "n_boundary_breach_games": n_boundary_breach_games,
        "n_error_games": n_errors,
        "appear_total": appear_total, "appear_cap": APPEAR_CAP,
        "criteria": {
            "allowed_kinds": list(ALLOWED_DIVERGENCE_KINDS),
            "step_boundary": {"threshold": threshold,
                              "source": "layer_s_block._CXS_FROM（经 L1 门③同源）"},
        },
    }
    result_face = {
        "ok": bool(n_records and n_errors == 0 and n_final_red == 0
                   and dead_total <= DEAD_SEEDS_VALUE_CAP),
        "n_games": n_records, "n_final_face_games_red": n_final_red,
        "final_face_criteria": "v2_final >= l1_final - 1e-9 per game",
        "dead_seeds_total_value": dead_total,
        "dead_seeds_cap": DEAD_SEEDS_VALUE_CAP,
        "dead_seeds_source": "v2 seated 重演终态 private.seeds × _l1.SEED_PRICE",
    }
    subset = bool(subset_result.get("all_ok"))
    cases = bool(cases_result.get("all_pass"))
    return {"passed": bool(form_face["ok"] and result_face["ok"]
                           and subset and cases),
            "form_face": form_face, "result_face": result_face,
            "subset": subset, "cases": cases,
            "per_game_summary": rows, "n_errors": n_errors}


# ---------------------------------------------------------------------------
# 构造用例（(c) 面：R10 三件复用 + v2 两件净口径）
# ---------------------------------------------------------------------------
def _load_v2_block_module():
    """本包 layer_s_block_v2.py 独立导入（管线产物位；进程内缓存）。"""
    path = os.path.join(HERE, V2_BLOCK_NAME)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"v2 块源缺失: {path}")
    name = "layer_s_block_v2_gate"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def constructed_cases_v2() -> dict:
    """五构造用例：R10 三件 import test_layer_s 夹具（在 v2 块上重演）+ v2 两件。

    不重写夹具（测试真值仍在 test_layer_s / test_layer_s_v2，防漂移）：c1-c3
    经 test_layer_s_v2._run_fixture_under 把夹具库全局 layer_s_block 临时改指
    v2 模块后调用 L1 夹具（三例磁带均无未来买单，L1/v2 净口径同值）；c4/c5
    直接 import 复用 test_layer_s_v2 的构造函数（传 v2 模块）。夹具异常=该例
    失败（不向上传播，门级红由 all_pass=False 承载）。
    返回 {c1_no_trunc_when_future_plant, c2_trunc_when_no_opportunity,
    c3_s671_boundary, c4_net_covered_buyback_deleted,
    c5_net_short_true_future_plant_kept, all_pass}。
    """
    import test_layer_s as tls       # L1 夹具库（L1_DIR 已在 sys.path）
    import test_layer_s_v2 as tls2   # v2 两件夹具（构造函数复用）
    v2_mod = _load_v2_block_module()

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

    c1 = _adjudicate(lambda: tls2._run_fixture_under(
        tls._invariant_case_c1_no_trunc_when_future_plant, v2_mod))
    c2 = _adjudicate(lambda: tls2._run_fixture_under(
        tls._invariant_case_c2_trunc_when_no_opportunity, v2_mod))
    try:
        sides = tls2._run_fixture_under(tls._invariant_case_c3_s671_boundary,
                                        v2_mod)
        c3_trunc = _verdict(sides["truncate_side"])
        c3_keep = _verdict(sides["keep_side"])
    except Exception as exc:  # 双面夹具共享一次调用：异常=双面俱败
        evidence = f"fixture raised {type(exc).__name__}: {exc}"
        c3_trunc = {"pass": False, "evidence": evidence}
        c3_keep = {"pass": False, "evidence": evidence}
    c4 = _adjudicate(lambda: tls2._invariant_case_c4_net_covered_buyback_deleted(
        v2_mod))
    c5 = _adjudicate(
        lambda: tls2._invariant_case_c5_net_short_true_future_plant_kept(
            v2_mod))
    return {
        "c1_no_trunc_when_future_plant": c1,
        "c2_trunc_when_no_opportunity": c2,
        "c3_s671_boundary": {
            "truncate_side": c3_trunc, "keep_side": c3_keep,
            "pass": c3_trunc["pass"] and c3_keep["pass"],
        },
        "c4_net_covered_buyback_deleted": c4,
        "c5_net_short_true_future_plant_kept": c5,
        "all_pass": bool(c1["pass"] and c2["pass"] and c3_trunc["pass"]
                         and c3_keep["pass"] and c4["pass"] and c5["pass"]),
    }


# ---------------------------------------------------------------------------
# 门③主体
# ---------------------------------------------------------------------------
def run(episodes_dir, v2_main, l1_main, verbatim_main, limit=None,
        evidence_path=None) -> dict:
    """两路重演+三面裁决 → {passed, form_face, result_face, subset, cases,
    per_game_summary, n_errors, evidence_path}。

    编排：① _l1._discover_replays 按局号升序发现语料（limit 截前 N 局）；② 三
    callable 装载一次跨局复用（_l1._as_callable，接受路径/callable）；③ 逐局
    两路 _l1.replay_action_diff——(a) 路 cand=v2/control=verbatim（形态面+
    子集判据消费面），(b) 路 cand=L1/control=verbatim（结果面 finals 来源）；
    (a) 路无 error 再取 v2 终局死种（_v2_dead_seeds）；④ 全 (a) 路产物喂
    _l1.precision_subset_check（净截断子集重验）；⑤ constructed_cases_v2()；
    ⑥ _aggregate_verdict 汇总。evidence 落 <本包>/evidence/
    equivalence_evidence.json（可覆写），协议 2.0：per_game 双路产物 + 四面
    指标。语料目录空/坏 → 单条全局面 error 记录（四面俱红，防空转绿灯）。"""
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
                        "form": None, "result": None, "dead_seeds": None})
    load_error = None
    if replays:
        try:
            v2_fn = _l1._as_callable(v2_main)
            l1_fn = _l1._as_callable(l1_main)
            vb_fn = _l1._as_callable(verbatim_main)
        except Exception as exc:
            load_error = f"装载/语料失败: {type(exc).__name__}: {exc}"
    for path in replays:
        ep = _l1._episode_from_path(path)
        if load_error is not None:  # 装载失败：逐局记 error（fail-closed 留痕）
            records.append({"episode": ep, "seat": None, "error": load_error,
                            "form": None, "result": None, "dead_seeds": None})
            continue
        try:
            form = _l1.replay_action_diff(path, v2_fn, vb_fn)
        except Exception as exc:  # 叶内已自包 error；此处兜底防编排面逃逸
            form = {"error": f"{type(exc).__name__}: {exc}"}
        try:
            result = _l1.replay_action_diff(path, l1_fn, vb_fn)
        except Exception as exc:
            result = {"error": f"{type(exc).__name__}: {exc}"}
        dead_seeds = None
        if form.get("error") is None:  # (a) 路成形才取死种；否则该局已红
            try:
                dead_seeds = _v2_dead_seeds(path, v2_fn)
            except Exception as exc:
                dead_seeds = {"error": f"{type(exc).__name__}: {exc}"}
        seat = form.get("seat")
        if seat is None:
            seat = result.get("seat")
        records.append({"episode": ep, "seat": seat, "error": None,
                        "form": form, "result": result,
                        "dead_seeds": dead_seeds})

    form_products = [r["form"] for r in records if r["form"] is not None]
    subset_result = _l1.precision_subset_check(form_products)
    try:
        cases_result = constructed_cases_v2()
    except Exception as exc:  # import/夹具面逃逸 → cases 红（fail-closed）
        cases_result = {"all_pass": False,
                        "error": f"{type(exc).__name__}: {exc}"}
    aggregate = _aggregate_verdict(records, subset_result, cases_result)

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
            "v2_main": v2_main if isinstance(v2_main, str) else "<callable>",
            "l1_main": l1_main if isinstance(l1_main, str) else "<callable>",
            "verbatim_main": (verbatim_main if isinstance(verbatim_main, str)
                              else "<callable>"),
        },
        "form_face": aggregate["form_face"],
        "result_face": aggregate["result_face"],
        "subset": subset_result,
        "cases": cases_result,
        "verdict": {
            "form_face": aggregate["form_face"]["ok"],
            "result_face": aggregate["result_face"]["ok"],
            "subset": aggregate["subset"],
            "cases": aggregate["cases"],
            "passed": aggregate["passed"],
        },
        "per_game": records,  # 逐局双路产物（(a)/(b) 全量），保留不截断
        "wall_total_s": round(time.perf_counter() - t0, 1),
    }
    with open(target, "w", encoding="utf-8") as fh:
        json.dump(evidence, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    aggregate["evidence_path"] = target
    return aggregate
