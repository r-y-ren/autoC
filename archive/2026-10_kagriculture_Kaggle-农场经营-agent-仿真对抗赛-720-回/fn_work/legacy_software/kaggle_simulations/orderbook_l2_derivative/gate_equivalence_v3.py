"""gate_equivalence_v3（R12 门③）：形态面+结果面（终局≥L1/死种≤$500/饿死零容忍）+净回收子集+九件构造用例。

编排（v2 门③ gate_equivalence_v2 的 v3 增补版，L1 门③ import 复用，逐局两路重演+终态提取）：
  (a) 形态面——diff(v3 vs verbatim)：_l1.replay_action_diff(path, v3_fn,
      verbatim_fn)（cand=v3、control=verbatim 保真对照），全部差异形态限于
      ALLOWED_DIVERGENCE_KINDS={BUY_SEED 增/删（减量单自然分解为 消失+出现
      一对，均在允许集）, SELL 变化}、全部差异步 ≥ **window**（v3 双窗参数：
      w648 主跑/w600 附加跑——不是 L1 的 _CXS_FROM 硬 648）；v3 无 appear
      上限（R12 硬指标无此项，减量保单天然成对增删），appear_total 只记账。
  (b) 结果面——①逐局 v3_final ≥ l1_final（1e-9；v3_final 取 (a) 路 cand 槽、
      l1_final 取 (b) 路 diff(L1 vs verbatim) 的 cand 槽）②死种合计=v3 重演
      终态我方 private.seeds×票价 ≤$500（票价=_l1.SEED_PRICE）③**饿死零容忍**
      （R12 新增）：v3 vs L1 逐局终态对比——我方在田株数（终态 farm tiles 的
      PLANT 地块逐品计数）/收获产物（private.shed 与 inventories 汇总）逐品项
      不减（1e-9 容差；任一品项减产=红，证据记 per_game）——经 _seated_terminal
      等价通道（v2 死种通道扩展：同款驱动循环直读终态，一次重演同时供死种与
      饿死两面）④净回收子集重验：净回收=逐品项 ΣBUY_SEED 消失−ΣBUY_SEED 出现
      （减量单自然分解对；appear 是 v3 实际持有的购买，不入回收），净额>0 才
      进 _l1.precision_subset_check 的 dropped 面——净回收 ≤ 原局该品项未种下
      量（replay_path 定位语料，口径全复用）。
  (c) constructed_cases_v3()：九件——R10 三件+c4/c5（减量语义重校）+新四件
      （8→1 法证/安全边兜超种/空槽忽略/600 窗滴灌），import test_layer_s_v3
      夹具复用（v3 块模块由本门自备，见 _v3_block_modules）。

裁决 passed=(a)∧(b)①②③④∧(c)（fail-closed：任一局任一路 error/死种值或
终态不可读 → 对应面红；语料空 → 单条全局面 error 防空转绿灯）。evidence 落
evidence/equivalence_evidence_w{window}.json（协议 3.0：per_game 双路+终态
产物 + form/result/subset/cases 四面指标；evidence_path 可覆写供测试 tmp 隔离）。
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)                                   # kaggle_simulations/
L1_DIR = os.path.normpath(os.path.join(KSIM, "orderbook_l1_derivative"))
for _path in (L1_DIR, HERE):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import gate_equivalence_precision as _l1  # noqa: E402  L1 门③（import 复用，零改动）

# R12 验收硬指标（kaggressure 战役 R12 责任契约）：
DEAD_SEEDS_VALUE_CAP = 500     # v3 重演终局死种合计 ≤$500（票价估值同 _l1.SEED_PRICE）
STARVE_TOL = 1e-9              # 饿死零容忍：终态产量面逐品项不减的浮点容差
ALLOWED_DIVERGENCE_KINDS = _l1.ALLOWED_DIVERGENCE_KINDS  # {增/删/SELL 变化}
FINAL_FACE_TOL = 1e-9          # v3_final ≥ l1_final 的浮点容差（L1/v2 门同款）
EVIDENCE_NAME_TEMPLATE = "equivalence_evidence_w{window}.json"
PROTOCOL = "orderbook-l2-equivalence/3.0"
V3_BLOCK_NAME_TEMPLATE = "layer_s_block_v3_w{window}.py"  # make 管线产物位（build 注入源）
WINDOWS = (648, 600)           # 主跑窗 + 附加跑窗（宽度：600 更宽）


# ---------------------------------------------------------------------------
# 终态提取（v2 死种等价通道的扩展：一次重演同时供死种面与饿死面）
# ---------------------------------------------------------------------------
def _seated_terminal(replay_path, agent_fn) -> Dict[str, Any]:
    """seated 重演至终局取我方终态：{final_money, seeds, seeds_value, plants, shed, inventories}。

    等价通道（沿 v2 _v2_dead_seeds 同款驱动循环：复用 _l1._load_strip_replay/
    _my_seat/_twin/_obs_dict + twin.step；对手席逐字重放 recorded 动作流，我席
    agent_fn 实驱）跑至终局后直读：
    - final_money[me]（终局资金，冗余留档——裁决面 finals 走 (a)/(b) 路产物）；
    - private.seeds 逐五种子品项（死种面，与 _l1._strip_unplanted_seeds 同口径）；
    - 我方 farm tiles 的 PLANT 地块逐品计数（饿死面·在田株数）；
    - private.shed 与 inventories 逐品汇总（饿死面·收获产物；inventories 为
      逐 farm 清单，同品相加）。
    地块 None/"LOCKED" 占位可忽略（schema 合法）；任何结构/数值畸形抛
    ValueError（→ 该局 error，fail-closed）；agent 调用/引擎步进异常向上抛。
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
        pair[me] = agent_fn(obs)
        twin.step(state, pair)
        taken += 1

    farms = state.seats[0].observation.farms
    if not isinstance(farms, (list, tuple)) or len(farms) <= me \
            or not isinstance(farms[me], dict):
        raise ValueError("终态 farms 缺失/畸形（fail-closed）")
    tiles = farms[me].get("tiles")
    if not isinstance(tiles, (list, tuple)):
        raise ValueError("终态 farm tiles 缺失/畸形（fail-closed）")
    plants: Dict[str, int] = {}
    for row in tiles:
        if not isinstance(row, (list, tuple)):
            raise ValueError("终态 farm tiles 行畸形（fail-closed）")
        for tile in row:
            if tile is None or isinstance(tile, str):
                continue  # 空槽/"LOCKED" 占位（schema 合法，与 _cxs_observed_plant_rate 同归类）
            if not isinstance(tile, dict):
                raise ValueError("终态地块非 dict（fail-closed）")
            if tile.get("kind") != "PLANT":
                continue
            crop = tile.get("crop")
            if not isinstance(crop, str):
                raise ValueError("PLANT 地块 crop 缺失/畸形（fail-closed）")
            plants[crop] = plants.get(crop, 0) + 1

    priv = state.seats[me].observation.private
    if not isinstance(priv, dict):
        raise ValueError("终态 private 缺失/畸形（fail-closed）")
    raw_seeds = priv.get("seeds") or {}
    if not isinstance(raw_seeds, dict):
        raise ValueError("终态 private.seeds 畸形（fail-closed）")
    seeds: Dict[str, int] = {}
    for crop in _l1.SEED_PRICE:
        qty = raw_seeds.get(crop) or 0
        if isinstance(qty, bool) or not isinstance(qty, (int, float)):
            raise ValueError(f"终态 seeds[{crop!r}] 非数（fail-closed）")
        seeds[crop] = int(qty)
    seeds_value = sum(qty * _l1.SEED_PRICE[crop] for crop, qty in seeds.items())

    def _numeric_counts(raw, label) -> Dict[str, Any]:
        if not isinstance(raw, dict):
            raise ValueError(f"终态 {label} 畸形（fail-closed）")
        out: Dict[str, Any] = {}
        for item, n in raw.items():
            if isinstance(n, bool) or not isinstance(n, (int, float)):
                raise ValueError(f"终态 {label}[{item!r}] 非数（fail-closed）")
            key = str(item)
            out[key] = out.get(key, 0) + n
        return out

    shed = _numeric_counts(priv.get("shed") or {}, "shed")
    invs_raw = priv.get("inventories") or []
    if not isinstance(invs_raw, (list, tuple)):
        raise ValueError("终态 inventories 畸形（fail-closed）")
    inventories: Dict[str, Any] = {}
    for inv in invs_raw:
        if not isinstance(inv, dict):
            raise ValueError("终态 inventories 条目畸形（fail-closed）")
        for item, n in _numeric_counts(inv, "inventories").items():
            inventories[item] = inventories.get(item, 0) + n
    return {"final_money": float(twin.final_money(state)[me]),
            "seeds": seeds, "seeds_value": int(seeds_value),
            "plants": plants, "shed": shed, "inventories": inventories}


# ---------------------------------------------------------------------------
# 饿死零容忍裁决（纯函数）
# ---------------------------------------------------------------------------
_STARVE_BUCKETS = ("plants", "shed", "inventories")


def _starve_verdict(v3_term, l1_term, tol: float = STARVE_TOL) -> Dict[str, Any]:
    """v3 vs L1 终态产量面对比：{ok, violations, buckets}（纯函数）。

    三桶（在田株数 plants / 收获棚 shed / 产物库 inventories）逐品项并集对比
    v3 ≥ L1−tol；任一品项减产=violations 一条（bucket/item/v3/l1）=ok False。
    桶非 dict / 计数非数 → ValueError（调用方按该局 error 承载，fail-closed——
    终态不可读绝不静默当绿）。"""
    v3_term = v3_term or {}
    l1_term = l1_term or {}
    violations: List[Dict[str, Any]] = []
    buckets: Dict[str, Dict[str, Any]] = {}
    for bucket in _STARVE_BUCKETS:
        v3m, l1m = v3_term.get(bucket) or {}, l1_term.get(bucket) or {}
        if not isinstance(v3m, dict) or not isinstance(l1m, dict):
            raise ValueError(f"terminal {bucket} metrics ill-typed")
        rows: Dict[str, Any] = {}
        for key in sorted(set(v3m) | set(l1m), key=str):
            try:
                delta = float(v3m.get(key, 0)) - float(l1m.get(key, 0))
            except (TypeError, ValueError):
                raise ValueError(f"terminal {bucket}[{key!r}] not numeric") from None
            ok = delta >= -tol
            if not ok:
                violations.append({"bucket": bucket, "item": key,
                                   "v3": v3m.get(key, 0), "l1": l1m.get(key, 0)})
            rows[key] = {"v3": v3m.get(key, 0), "l1": l1m.get(key, 0), "ok": ok}
        buckets[bucket] = rows
    return {"ok": not violations, "violations": violations, "buckets": buckets}


# ---------------------------------------------------------------------------
# 净回收子集（(b)④ 面：precision_subset_check 口径复用 + appear 净算）
# ---------------------------------------------------------------------------
def _net_recovery_by_crop(divergences) -> Dict[str, int]:
    """逐品项净回收 = ΣBUY_SEED 消失 − ΣBUY_SEED 出现（净额 ≤0 的品项不入表）。

    减量单在 replay_action_diff 里自然分解为 消失(原量)+出现(减后量) 一对：
    净额恰=减量部分（真少买的量）——appear 是 v3 实际持有的购买，不是回收，
    不净算会把保留量重复计入回收面（假红）。畸形记录（crop 非串/qty 非整）
    不入净算（subset 面对不可解析 dropped 自会 fail-closed）。"""
    net: Dict[str, int] = {}
    for entry in divergences or []:
        kind = entry.get("kind")
        if kind not in ("buy_seed_disappear", "buy_seed_appear"):
            continue
        crop, qty = entry.get("crop"), entry.get("qty")
        if not isinstance(crop, str) or isinstance(qty, bool) \
                or not isinstance(qty, int):
            continue
        net[crop] = net.get(crop, 0) + (qty if kind == "buy_seed_disappear" else -qty)
    return {crop: q for crop, q in net.items() if q > 0}


def _netted_recovery_products(products) -> List[Dict[str, Any]]:
    """(a) 路产物 → 净回收 dropped 面（喂 _l1.precision_subset_check）。

    逐局把 product["dropped"] 重写为净回收逐品项一条（step 取该品项最小消失步，
    供台账定位）；error 局原样透传（checker 自记 error，fail-closed）。其余键
    （episode/seat/replay_path…）原样保留——checker 消费面兼容。"""
    out: List[Dict[str, Any]] = []
    for product in products:
        if not isinstance(product, dict) or product.get("error") is not None:
            out.append(product)
            continue
        divergences = product.get("divergences") or []
        netted = _net_recovery_by_crop(divergences)
        steps_by_crop: Dict[str, Any] = {}
        for entry in divergences:
            if entry.get("kind") != "buy_seed_disappear":
                continue
            crop, step = entry.get("crop"), entry.get("step")
            if crop in netted:
                prev = steps_by_crop.get(crop)
                steps_by_crop[crop] = step if prev is None else min(prev, step)
        copy = dict(product)
        copy["dropped"] = [{"step": steps_by_crop.get(crop, 0), "crop": crop,
                            "qty": qty} for crop, qty in netted.items()]
        out.append(copy)
    return out


# ---------------------------------------------------------------------------
# 汇总裁决（纯函数；合成裁决矩阵单测直喂）
# ---------------------------------------------------------------------------
def _record_error(record) -> Optional[str]:
    """record 级 error 归并：自身 error 或 form/result/terminal 任一 error。"""
    if record.get("error") is not None:
        return str(record["error"])
    for key in ("form", "result", "terminal"):
        part = record.get(key)
        if isinstance(part, dict) and part.get("error") is not None:
            return str(part["error"])
    return None


def _aggregate_verdict(records, subset_result, cases_result, window=648) -> Dict[str, Any]:
    """(a)形态面+(b)结果面（终局/死种/饿死）+subset+cases 汇总（纯函数）。

    form_face.ok = 无任一 error ∧ 逐局（无 violation 形态 ∧ 全部差异步 ≥ window
    ——v3 双窗参数，非 L1 硬 648）∧ 非空记录集；result_face.ok = 无任一 error
    ∧ finals_ok（逐局 v3_final ≥ l1_final−1e-9）∧ 死种合计 ≤ DEAD_SEEDS_VALUE_CAP
    ∧ starve_free（v3 vs L1 终态三桶逐品项不减）；passed = form ∧ result ∧
    subset（净回收子集 all_ok）∧ cases（constructed_cases_v3 all_pass）。
    per_game_summary 逐局一行（error 局数值面记 None/0）。"""
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
        boundary_ok = all(step >= window for step in steps)
        appear_count = kind_counts.get("buy_seed_appear", 0)
        v3_final = form.get("l1_final") if error is None else None    # (a) 路 cand 槽=v3
        l1_final = result.get("l1_final") if error is None else None  # (b) 路 cand 槽=L1
        verbatim_final = form.get("verbatim_final") if error is None else None
        finals_ok = (error is None
                     and isinstance(v3_final, (int, float))
                     and isinstance(l1_final, (int, float))
                     and (float(v3_final) - float(l1_final)) >= -FINAL_FACE_TOL)
        v3_term = (terminal or {}).get("v3") if error is None else None
        l1_term = (terminal or {}).get("l1") if error is None else None
        if error is None and not (isinstance(terminal, dict)
                                  and isinstance(v3_term, dict)
                                  and isinstance(l1_term, dict)):
            error = "terminal face missing/ill-typed (fail-closed)"
            v3_term = l1_term = None
        dead_value = (v3_term or {}).get("seeds_value") if error is None else None
        if error is None and not (isinstance(dead_value, (int, float))
                                  and not isinstance(dead_value, bool)):
            error = "dead seeds value missing/ill-typed (fail-closed)"  # 结构破损=红
            dead_value = None
        starve = None
        if error is None:
            try:
                starve = _starve_verdict(v3_term, l1_term)
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
        final_delta = ((v3_final - l1_final)
                       if isinstance(v3_final, (int, float))
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
            "v3_final": v3_final, "l1_final": l1_final,
            "verbatim_final": verbatim_final, "final_delta": final_delta,
            "dead_seeds_value": dead_value,
            "dead_seeds": (v3_term or {}).get("seeds") if error is None else None,
            "starve_ok": (starve["ok"] if error is None and starve is not None
                          else None),
            "n_starve_violations": (len(starve["violations"])
                                    if error is None and starve is not None else 0),
            "starve_violations": (starve["violations"]
                                  if error is None and starve is not None else None),
            "v3_plants": (v3_term or {}).get("plants") if error is None else None,
            "l1_plants": (l1_term or {}).get("plants") if error is None else None,
            "v3_shed": (v3_term or {}).get("shed") if error is None else None,
            "l1_shed": (l1_term or {}).get("shed") if error is None else None,
        })
    n_records = len(records)
    form_face = {
        "ok": bool(n_records and n_errors == 0 and n_form_clean == n_records),
        "n_games": n_records, "n_game_clean": n_form_clean,
        "n_violation_games": n_violation_games,
        "n_boundary_breach_games": n_boundary_breach_games,
        "n_error_games": n_errors,
        "appear_total": appear_total,  # 只记账不设阈（R12 无 appear 上限；减量保单天然成对增删）
        "criteria": {
            "allowed_kinds": list(ALLOWED_DIVERGENCE_KINDS),
            "step_boundary": {"threshold": window,
                              "source": "run(window)（v3 双窗参数：w648 主跑/w600 附加跑）"},
        },
    }
    result_face = {
        "ok": bool(n_records and n_errors == 0 and n_final_red == 0
                   and dead_total <= DEAD_SEEDS_VALUE_CAP and n_starve_red == 0),
        "n_games": n_records,
        "finals_ok": bool(n_records and n_errors == 0 and n_final_red == 0),
        "n_final_face_games_red": n_final_red,
        "final_face_criteria": "v3_final >= l1_final - 1e-9 per game",
        "dead_seeds_total_value": dead_total,
        "dead_seeds_cap": DEAD_SEEDS_VALUE_CAP,
        "dead_seeds_source": "v3 seated 重演终态 private.seeds × _l1.SEED_PRICE",
        "starve_free": bool(n_records and n_errors == 0 and n_starve_red == 0),
        "n_starve_games_red": n_starve_red,
        "starve_criteria": "v3 vs L1 终态 plants/shed/inventories 逐品项不减（-1e-9 容差；任一减产=红）",
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
# 构造用例（(c) 面：九件，import test_layer_s_v3 夹具复用）
# ---------------------------------------------------------------------------
_V3_MODULE_CACHE: Dict[int, Any] = {}


def _v3_block_modules() -> Dict[int, Any]:
    """双窗 v3 块模块 {648: mod, 600: mod}（进程内缓存）。

    块源优先 make 管线产物位 HERE/layer_s_block_v3_w{window}.py（build 的 make
    产物，注入源同字节）；缺失则 make_layer_s_v3_block.make 从 L1 块确定性再生
    （tmp 落盘，make 内建受控变更集审计全跑）——两条路径产物逐字节同源（make
    幂等），(c) 面与 build 注入件语义一致。装载失败向上抛（→ cases 红，
    fail-closed）。"""
    modules: Dict[int, Any] = {}
    for window in WINDOWS:
        if window in _V3_MODULE_CACHE:
            modules[window] = _V3_MODULE_CACHE[window]
            continue
        cand = os.path.join(HERE, V3_BLOCK_NAME_TEMPLATE.format(window=window))
        if not os.path.isfile(cand):
            import make_layer_s_v3_block as maker
            l1_block = os.path.join(L1_DIR, "layer_s_block.py")
            tmp_dir = tempfile.mkdtemp(prefix=f"gate_equiv_v3_w{window}_")
            cand = os.path.join(tmp_dir, V3_BLOCK_NAME_TEMPLATE.format(window=window))
            maker.make(l1_block, cand, window=window)
        name = f"layer_s_block_v3_w{window}_gate_equiv"
        spec = importlib.util.spec_from_file_location(name, cand)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        _V3_MODULE_CACHE[window] = module
        modules[window] = module
    return modules


def constructed_cases_v3() -> dict:
    """九构造用例：R10 三件+c4/c5（减量语义重校）+新四件（8→1/安全边/空槽/600 窗）。

    不重写夹具（测试真值仍在 test_layer_s_v3，防漂移）：九件全部 import 复用
    test_layer_s_v3 的构造函数（c1-c8 传 w648 块模块、c9 传 w600 块模块——
    600 窗件用 window=600 的构造局夹具）。夹具异常=该例失败（不向上传播，
    门级红由 all_pass=False 承载）。返回 {c1…c9 各例 {pass, evidence},
    c3 双面, all_pass}。"""
    import test_layer_s_v3 as tls3   # 夹具库（HERE 已在 sys.path）
    mods = _v3_block_modules()
    v3_mod, v3_w600 = mods[648], mods[600]

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

    c1 = _adjudicate(lambda: tls3._invariant_case_c1_no_trunc_when_future_plant(v3_mod))
    c2 = _adjudicate(lambda: tls3._invariant_case_c2_trunc_when_no_opportunity(v3_mod))
    try:
        sides = tls3._invariant_case_c3_s671_boundary(v3_mod)
        c3_trunc = _verdict(sides["truncate_side"])
        c3_keep = _verdict(sides["keep_side"])
    except Exception as exc:  # 双面夹具共享一次调用：异常=双面俱败
        evidence = f"fixture raised {type(exc).__name__}: {exc}"
        c3_trunc = {"pass": False, "evidence": evidence}
        c3_keep = {"pass": False, "evidence": evidence}
    c4 = _adjudicate(lambda: tls3._invariant_case_c4_covered_buyback_reduced_to_zero(v3_mod))
    c5 = _adjudicate(lambda: tls3._invariant_case_c5_short_true_future_plant_kept(v3_mod))
    c6 = _adjudicate(lambda: tls3._invariant_case_c6_8to1_forensic(v3_mod))
    c7 = _adjudicate(lambda: tls3._invariant_case_c7_margin_backstop_reactive_overshoot(v3_mod))
    c8 = _adjudicate(lambda: tls3._invariant_case_c8_empty_slot_ignored(v3_mod))
    c9 = _adjudicate(lambda: tls3._invariant_case_c9_window600_drip(v3_w600))
    return {
        "c1_no_trunc_when_future_plant": c1,
        "c2_trunc_when_no_opportunity": c2,
        "c3_s671_boundary": {
            "truncate_side": c3_trunc, "keep_side": c3_keep,
            "pass": c3_trunc["pass"] and c3_keep["pass"],
        },
        "c4_covered_buyback_reduced_to_zero": c4,
        "c5_short_true_future_plant_kept": c5,
        "c6_8to1_forensic": c6,
        "c7_margin_backstop_reactive_overshoot": c7,
        "c8_empty_slot_ignored": c8,
        "c9_window600_drip": c9,
        "all_pass": bool(c1["pass"] and c2["pass"] and c3_trunc["pass"]
                         and c3_keep["pass"] and c4["pass"] and c5["pass"]
                         and c6["pass"] and c7["pass"] and c8["pass"]
                         and c9["pass"]),
    }


# ---------------------------------------------------------------------------
# 门③主体
# ---------------------------------------------------------------------------
def run(episodes_dir, v3_main, l1_main, verbatim_main, window=648, limit=None,
        evidence_path=None) -> dict:
    """两路重演+终态提取+四面裁决 → {passed, form_face, result_face, subset,
    cases, per_game_summary, n_errors, evidence_path}。

    编排：① _l1._discover_replays 按局号升序发现语料（limit 截前 N 局）；② 三
    callable 装载一次跨局复用（_l1._as_callable，接受路径/callable）；③ 逐局
    两路 _l1.replay_action_diff——(a) 路 cand=v3/control=verbatim（形态面+净回收
    消费面），(b) 路 cand=L1/control=verbatim（结果面 finals 来源）；(a) 路无
    error 再做终态提取（_seated_terminal 两遍：v3 死种+饿死面、L1 饿死对照面）；
    ④ (a) 路产物经净回收净算（_netted_recovery_products）喂
    _l1.precision_subset_check；⑤ constructed_cases_v3()；⑥ _aggregate_verdict
    汇总（步界阈值=window）。evidence 落 <本包>/evidence/
    equivalence_evidence_w{window}.json（可覆写），协议 3.0：per_game 双路+终态
    产物 + 四面指标。语料目录空/坏 → 单条全局面 error 记录（四面俱红，防空转
    绿灯）。"""
    t0 = time.perf_counter()
    if isinstance(window, bool) or not isinstance(window, int) or window <= 0:
        raise ValueError(f"window 必须为正 int，got {window!r}")
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
            v3_fn = _l1._as_callable(v3_main)
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
            form = _l1.replay_action_diff(path, v3_fn, vb_fn)
        except Exception as exc:  # 叶内已自包 error；此处兜底防编排面逃逸
            form = {"error": f"{type(exc).__name__}: {exc}"}
        try:
            result = _l1.replay_action_diff(path, l1_fn, vb_fn)
        except Exception as exc:
            result = {"error": f"{type(exc).__name__}: {exc}"}
        terminal = None
        if form.get("error") is None:  # (a) 路成形才取终态；否则该局已红
            try:
                terminal = {"v3": _seated_terminal(path, v3_fn),
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
        cases_result = constructed_cases_v3()
    except Exception as exc:  # import/夹具面逃逸 → cases 红（fail-closed）
        cases_result = {"all_pass": False,
                        "error": f"{type(exc).__name__}: {exc}"}
    aggregate = _aggregate_verdict(records, subset_result, cases_result,
                                   window=window)

    target = os.path.abspath(evidence_path or os.path.join(
        HERE, "evidence", EVIDENCE_NAME_TEMPLATE.format(window=window)))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    evidence = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "protocol": PROTOCOL,
        "inputs": {
            "episodes_dir": os.path.abspath(episodes_dir),
            "n_replays": len(replays),
            "replays": [os.path.basename(p) for p in replays],
            "limit": limit,
            "window": window,
            "v3_main": v3_main if isinstance(v3_main, str) else "<callable>",
            "l1_main": l1_main if isinstance(l1_main, str) else "<callable>",
            "verbatim_main": (verbatim_main if isinstance(verbatim_main, str)
                              else "<callable>"),
        },
        "form_face": aggregate["form_face"],
        "result_face": aggregate["result_face"],
        "subset": subset_result,
        "subset_netting": {
            "note": "净回收=逐品项 ΣBUY_SEED 消失−ΣBUY_SEED 出现（减量单自然分解"
                    "对；appear 是 v3 实际持有的购买不入回收）；净额>0 才进 "
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
