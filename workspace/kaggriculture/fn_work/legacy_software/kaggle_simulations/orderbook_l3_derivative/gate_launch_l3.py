"""gate_launch_l3（R13 门④）：发射四门（L1 门④ import 复用重定向）+形态检查扩展。

复用面（零改动 import，gate_h2h_vs_l1 先例同款）：
  - gate_launch_fourgate_l1.run 整链——身份链先行（build_manifest.json 核对）、
    v48_derivative_launch_check 四属性换包重定向（官方 -I 装载语义/双席自打
    720 回合/确定性 sha256/包体身份链）、seed101 obs 全序列（719 步）驱动
    truncation_only_diff；L3 main 末 callable 同名 _cxs_agent（基座中部钳制
    手术不触尾块），L1 门内断言原样成立。
  - 步界 ≥648：L1 门 _truncation_only_diff 内 import layer_s_block 实判
    _CXS_FROM=648（同源，不第二处手拼）——R13 硬指标"差异步 ≥648"即此。

扩展面（R12 留档缺口修复——L2 曾直接复用 L1 门④，其严格口径只认 BUY_SEED
整单消失，把减量对/SELL 变化错记 form_violations）：装载 L1 门模块后把其
形态判定 _seed_drop_form 进程内换为 _l3_truncation_form（try/finally 还原，
只动进程内属性不触盘上 L1 目录）。合法形态集扩为：
  {BUY_SEED 整单消失、BUY_SEED 减量对（同品项 disappear≥appear 且同步——
  逐 diff 步内消失/出现自然同步）、SELL 变化}；
净增单（同品项出现量>消失量）、跨品项顶替、非 BUY_SEED/SELL 订单变化、
非 market 槽位漂移、BUY_SEED 槽位重排（多重集同而序变）= violation。
多重集部件（_market_partition/_multiset_minus/_seed_order_meta）import 复用
gate_equivalence_precision（同包族私有件复用先例：v3 复用 _l1 叶件）。

evidence：L1 门自写 launch_check_evidence.json（协议 1.0 四门面），run 后
增记 l3_form_extension 面并升协议 orderbook-l3-launch-fourgate/1.0（只增键
不删改四门字段；evidence_path 可覆写，测试 tmp 隔离）。返回沿 L1 门契约
{gates, truncation_only_diff:{ok, divergent_steps}, passed, evidence_path}
+ form_extension 摘要键。"""

from __future__ import annotations

import contextlib
import json
import os
import sys
import time
from typing import Any, Dict, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)                                   # kaggle_simulations/
L1_DIR = os.path.normpath(os.path.join(KSIM, "orderbook_l1_derivative"))
if L1_DIR not in sys.path:
    sys.path.insert(0, L1_DIR)

import gate_equivalence_precision as _l1e  # noqa: E402  多重集部件（import 复用）
import gate_launch_fourgate_l1 as _l1g     # noqa: E402  L1 门④（import 复用，零改动）

L3_LAST_CALLABLE = _l1g.L1_LAST_CALLABLE   # "_cxs_agent"（L3 main 末 callable 同名）
BASELINE_LAST_CALLABLE = _l1g.BASELINE_LAST_CALLABLE
STEP_BOUNDARY = 648          # L1 门内 layer_s_block._CXS_FROM 实判（同源，此处仅登记）
EXTENDED_FORM_KINDS = ("buy_seed_whole_disappear",   # BUY_SEED 整单消失
                       "buy_seed_reduce_pair",       # BUY_SEED 减量对（disappear≥appear 同品项同步）
                       "sell_order_change")          # SELL 变化（基座少卖/改卖反应）
PROTOCOL = "orderbook-l3-launch-fourgate/1.0"
EVIDENCE_NAME = "launch_check_evidence.json"


def _l3_truncation_form(base_action, cand_action, norm_action) -> Tuple[bool, str]:
    """R13 扩展形态判据（L1 门 _seed_drop_form 同签名替身）。

    base=verbatim 动作、cand=L3 动作、norm_action=L1 门 check.norm_action。
    判据（全部满足才绿）：
      ① action 同为 dict 且键集相等；② 非 market 槽位逐项相等；③ market 同为
      list；④ 非 BUY_SEED/SELL 订单（HIRE/BUY_ANIMAL/BUY_PRODUCT…）逐字节相等；
      ⑤ BUY_SEED 消失/出现多重集差逐单可解析（crop 串+qty 整），且**同品项**
      消失量 ≥ 出现量（减量对/整单消失；跨品项顶替与净增单=红）；⑥ 差异非空
      且不可归因零记录（纯 BUY_SEED 槽位重排等）=红。SELL 序列任意变化合法
      （一步至多一类）。返回 (ok, detail)，detail 为台账可读形态摘要。"""
    if not (isinstance(base_action, dict) and isinstance(cand_action, dict)):
        return False, "action 非 dict"
    if set(base_action) != set(cand_action):
        return False, "action 键集不同"
    for key in base_action:
        if key != "market" and norm_action(base_action[key]) != norm_action(cand_action[key]):
            return False, f"非 market 槽位 {key} 漂移"
    base_market, cand_market = base_action.get("market"), cand_action.get("market")
    if not (isinstance(base_market, list) and isinstance(cand_market, list)):
        return False, "market 非 list"
    b_bs, b_sell, b_other = _l1e._market_partition(base_market)
    c_bs, c_sell, c_other = _l1e._market_partition(cand_market)
    if norm_action(b_other) != norm_action(c_other):
        return False, "非 BUY_SEED/SELL 订单差异（HIRE/BUY_ANIMAL 等）"
    sell_changed = norm_action(b_sell) != norm_action(c_sell)
    vanish = _l1e._multiset_minus(b_bs, c_bs)   # verbatim 有 L3 无（消失面）
    added = _l1e._multiset_minus(c_bs, b_bs)    # L3 有 verbatim 无（减量保留面）
    vanish_qty: Dict[str, int] = {}
    added_qty: Dict[str, int] = {}
    for orders, bucket in ((vanish, vanish_qty), (added, added_qty)):
        for order in orders:
            meta = _l1e._seed_order_meta(order)
            if meta is None:
                return False, f"BUY_SEED 订单结构异常: {order!r}"
            crop, qty = meta
            bucket[crop] = bucket.get(crop, 0) + qty
    for crop in sorted(added_qty):
        if added_qty[crop] > vanish_qty.get(crop, 0):
            return False, (f"BUY_SEED {crop} 出现 {added_qty[crop]} > 消失 "
                           f"{vanish_qty.get(crop, 0)}（净增单/跨品项顶替，非减量对）")
    if not vanish and not added and not sell_changed:
        return False, "差异不可归因（BUY_SEED 槽位重排等形态外差异）"
    parts = []
    whole = {c: q for c, q in sorted(vanish_qty.items()) if c not in added_qty}
    pairs = {c: (vanish_qty[c], added_qty[c]) for c in sorted(added_qty)}
    if whole:
        parts.append("BUY_SEED 整单消失 "
                     + ",".join(f"{c}x{q}" for c, q in whole.items()))
    if pairs:
        parts.append("BUY_SEED 减量对 "
                     + ",".join(f"{c} {v}->{a}" for c, (v, a) in pairs.items()))
    if sell_changed:
        parts.append("SELL 变化")
    return True, " + ".join(parts)


@contextlib.contextmanager
def _extended_form():
    """进程内把 L1 门④形态判定换为 L3 扩展集（try/finally 还原）。

    _truncation_only_diff 按模块全局名查 _seed_drop_form，属性替换即生效；
    只动进程内 gate_launch_fourgate_l1 属性，不触盘上 L1 目录（L2 门②
    evidence 落点改指同款纪律）。"""
    original = _l1g._seed_drop_form
    _l1g._seed_drop_form = _l3_truncation_form
    try:
        yield
    finally:
        _l1g._seed_drop_form = original


def run(pkg_path=None, evidence_path=None) -> Dict[str, Any]:
    """门④主入口（L1 门④整链复用+形态扩展）→ {gates, truncation_only_diff,
    passed, evidence_path, form_extension}。

    pkg_path=L3 包目录（默认本目录；build_manifest.json/main.py/
    submission.tar.gz 由 build_l13_candidate 产出）。身份链不匹配/任一门红
    → passed=False（fail-closed，L1 门语义原样）。evidence 落
    <pkg>/evidence/launch_check_evidence.json（可覆写）并增记
    l3_form_extension 面。"""
    t0 = time.perf_counter()
    with _extended_form():
        result = _l1g.run(pkg_path, evidence_path=evidence_path)
    extension = {
        "kinds": list(EXTENDED_FORM_KINDS),
        "step_boundary": {"threshold": STEP_BOUNDARY,
                          "source": "L1 门内 layer_s_block._CXS_FROM 实判（同源）"},
        "candidate_callable": L3_LAST_CALLABLE,
        "baseline_callable": BASELINE_LAST_CALLABLE,
        "note": "R12 留档缺口修复：减量对（同品项 disappear≥appear 同步）与 "
                "SELL 变化入合法形态集；净增单/跨品项顶替/槽位重排仍红",
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    target = result.get("evidence_path")
    if isinstance(target, str) and os.path.isfile(target):
        with open(target, "r", encoding="utf-8") as fh:
            evidence = json.load(fh)
        evidence["protocol"] = PROTOCOL
        evidence["l3_form_extension"] = extension
        with open(target, "w", encoding="utf-8") as fh:
            json.dump(evidence, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
    result["form_extension"] = extension
    return result


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    result = run(argv[0] if argv else None)
    for name, ok in result["gates"].items():
        print(f"[gate] {name}: {'PASS' if ok else 'FAIL'}")
    trunc = result["truncation_only_diff"]
    steps = trunc["divergent_steps"]
    print(f"[extra] truncation_only_diff ok={trunc['ok']} "
          f"n_divergent={len(steps)} "
          f"min_step={min(steps) if steps else None}")
    print(f"passed = {result['passed']}")
    print(f"evidence -> {result['evidence_path']}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
