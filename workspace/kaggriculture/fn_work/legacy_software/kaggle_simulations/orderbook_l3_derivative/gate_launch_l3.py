"""gate_launch_l3（R13 门④）：发射四门（L1 门④ import 复用重定向）+形态检查扩展。

复用面（零改动 import，gate_h2h_vs_l1 先例同款）：
  - gate_launch_fourgate_l1.run 整链——身份链先行（build_manifest.json 核对）、
    v48_derivative_launch_check 四属性换包重定向（官方 -I 装载语义/双席自打
    720 回合/确定性 sha256/包体身份链）、seed101 obs 全序列（719 步）驱动
    truncation_only_diff；L3 main 末 callable 同名 _cxs_agent（基座中部钳制
    手术不触尾块），L1 门内断言原样成立。
  - 步界 ≥576（R13 修订一轮：day24 包络）：L1 门 _truncation_only_diff 内
    import layer_s_block 实判 _CXS_FROM——_extended_form 期间进程内把
    layer_s_block._CXS_FROM 参数化改指本门 STEP_BOUNDARY=576（try/finally
    还原为 L1 原值 648；只动进程内属性不触盘上 L1 目录；layer S 截断窗本体
    仍 648——此处仅门禁包络界）。

扩展面（R12 留档缺口修复——L2 曾直接复用 L1 门④，其严格口径只认 BUY_SEED
整单消失，把减量对/SELL 变化错记 form_violations）：装载 L1 门模块后把其
形态判定 _seed_drop_form 进程内换为 _l3_truncation_form（try/finally 还原，
只动进程内属性不触盘上 L1 目录）。合法形态集扩为：
  {BUY_SEED 整单消失、BUY_SEED 减量对（同品项 disappear≥appear 且同步——
  逐 diff 步内消失/出现自然同步）、SELL 变化}；
净增单（同品项出现量>消失量）、跨品项顶替、非 BUY_SEED/SELL 订单变化、
非 market 槽位漂移、BUY_SEED 槽位重排（多重集同而序变）= violation。
**空槽归一（2026-09-24 修订一轮）**：market 单比较前把 []/None 空槽占位两侧
归一剔除（S6 实证 form 红为空槽数量差伪差异）；归一后两侧恒等=绿（伪差异）；
非空但 len<3 畸形单仍走 violation（fail-closed 语义不变）。
多重集部件（_market_partition/_multiset_minus/_seed_order_meta）import 复用
gate_equivalence_precision（同包族私有件复用先例：v3 复用 _l1 叶件）。

evidence：L1 门自写 launch_check_evidence.json（协议 1.0 四门面），run 后
增记 l3_form_extension 面并升协议 orderbook-l3-launch-fourgate/1.1（只增键
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
STEP_BOUNDARY = 576          # R13 修订一轮：day24 包络（需求相对激活使 day24-26
                             # 即可有合法差异；layer S 截断窗本体仍 648=L1 门
                             # _CXS_FROM 原值，_extended_form 期间进程内参数化
                             # 改指 576 并跑后还原——L1 文件零改动）
EXTENDED_FORM_KINDS = ("buy_seed_whole_disappear",   # BUY_SEED 整单消失
                       "buy_seed_reduce_pair",       # BUY_SEED 减量对（disappear≥appear 同品项同步）
                       "sell_order_change")          # SELL 变化（基座少卖/改卖反应）
PROTOCOL = "orderbook-l3-launch-fourgate/1.1"
EVIDENCE_NAME = "launch_check_evidence.json"


def _is_empty_slot(order) -> bool:
    """空槽占位判定：None / 空 list / 空 tuple（gate_equivalence_l3 同款）。

    非空但 len<3 的畸形单不是空槽——不剔除（差异不对称 → violation 红，
    fail-closed 语义不变）。"""
    return order is None or (isinstance(order, (list, tuple)) and len(order) == 0)


def _l3_truncation_form(base_action, cand_action, norm_action) -> Tuple[bool, str]:
    """R13 扩展形态判据（L1 门 _seed_drop_form 同签名替身；空槽归一修订）。

    base=verbatim 动作、cand=L3 动作、norm_action=L1 门 check.norm_action。
    判据（全部满足才绿）：
      ① action 同为 dict 且键集相等；② 非 market 槽位逐项相等；③ market 同为
      list，且**先剔空槽占位**（[]/None 两侧归一——纯空槽数量差=伪差异直接
      绿）；④ 非 BUY_SEED/SELL 订单（HIRE/BUY_ANIMAL/BUY_PRODUCT…）逐字节相等；
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
    # 空槽归一（R13 修订一轮）：两侧各删 []/None 占位后再比——S6 实证 form 红
    # 为空槽数量差伪差异；归一后恒等=零实质差异=绿（畸形单保留在表内走红路）。
    base_market = [o for o in base_market if not _is_empty_slot(o)]
    cand_market = [o for o in cand_market if not _is_empty_slot(o)]
    if norm_action(base_market) == norm_action(cand_market):
        return True, "空槽占位归一后恒等（[]/None 数量差伪差异，无实质订单差异）"
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
    """进程内把 L1 门④形态判定换为 L3 扩展集+步界参数化改指 576（还原式）。

    _truncation_only_diff 按模块全局名查 _seed_drop_form、调用时实判
    layer_s_block._CXS_FROM——两处进程内属性替换即生效（try/finally 还原）；
    只动进程内 gate_launch_fourgate_l1/layer_s_block 属性，不触盘上 L1 目录
    （门② evidence 落点改指同款纪律）。layer_s_block._CXS_FROM 原值（648=
    layer S 截断窗本体）跑后原样还原；_truncation_only_diff 内 import 与
    本处 import 解析到同一 sys.modules 对象（L1_DIR 唯一 layer_s_block.py）。"""
    import layer_s_block   # 与 _truncation_only_diff 内 import 同一模块对象
    original_form = _l1g._seed_drop_form
    original_from = layer_s_block._CXS_FROM
    _l1g._seed_drop_form = _l3_truncation_form
    layer_s_block._CXS_FROM = STEP_BOUNDARY
    try:
        yield
    finally:
        _l1g._seed_drop_form = original_form
        layer_s_block._CXS_FROM = original_from


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
                          "source": "R13 修订一轮：day24 包络——_extended_form 期间"
                                    "进程内参数化 layer_s_block._CXS_FROM 改指 576"
                                    "（try/finally 还原 L1 原值 648；layer S 截断"
                                    "窗本体仍 648）"},
        "empty_slot_normalization": {
            "applied": True,
            "note": "market 单比较前剔除 []/None 空槽占位（两侧归一）；归一后"
                    "恒等=绿（伪差异）；非空 len<3 畸形单仍 violation",
        },
        "candidate_callable": L3_LAST_CALLABLE,
        "baseline_callable": BASELINE_LAST_CALLABLE,
        "note": "R12 留档缺口修复：减量对（同品项 disappear≥appear 同步）与 "
                "SELL 变化入合法形态集；净增单/跨品项顶替/槽位重排仍红；"
                "R13 修订一轮：空槽归一+步界 576 包络",
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
