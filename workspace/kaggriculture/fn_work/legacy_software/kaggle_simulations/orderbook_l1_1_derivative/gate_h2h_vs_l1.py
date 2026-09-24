"""gate_h2h_vs_l1（R11 门①）：v2 vs L1 直量增量 16 局 + vs verbatim 8 局参考面。

主体零改动复用 L1 门① gate_h2h_vs_verbatim.run（import 复用，不制第二份对局
/装载/台账逻辑）：v2 为 cand、L1 为对手，双侧装载身份断言均参数化为
{"_cxs_agent"}（v2 末 callable 与 L1 同名——同为层 S 运行时入口，唯一差异在
_cxs_seed_surplus 净口径）；seeds 缺省沿用 L1 门 DEFAULT_SEEDS（101-104/
201-204 ×双席=16 局，R11 验收"互胜 vs L1 ≥0.55"的直量增量面）；evidence 落
本包 evidence/h2h_evidence.json（evidence_path 可覆写，测试 tmp 隔离防覆写
真台账——L1 门同款口径）。

另附 vs verbatim 8 局参考面（seeds 101-104 ×双席；期望名 {"_cxs_agent"}/
{"_cxd_agent"}，走同一 L1 门装载身份断言）：只记账 ref_face（n/wins/losses/
ties/rate + 自身台账路径），**不设阈值不进门**——参考面回答"v2 对 verbatim
的互胜面是否也没塌"供评审参考，门①裁决只看 v2 vs L1（rate ≥0.55 且全 DONE，
L1 门①同款 fail-closed 口径，任一局非 DONE 即红）。参考面台账独立落
evidence/h2h_ref_evidence.json，摘要增记进主台账件 ref_face 键。

返回 {n, wins, rate, passed, ref_face, evidence_path}（契约键集；per_game
明细留在两份台账件内）。装载失败/装载身份不符（含参考面侧）抛 L1 门的
GateH2HError 上抛（fail-closed，由编排承载为门红）。
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, Optional, Sequence

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(HERE)                                   # kaggle_simulations/
L1_DIR = os.path.normpath(os.path.join(KSIM, "orderbook_l1_derivative"))
if L1_DIR not in sys.path:
    sys.path.insert(0, L1_DIR)

import gate_h2h_vs_verbatim as _base  # noqa: E402  L1 门①（import 复用，零改动）

DEFAULT_SEEDS = _base.DEFAULT_SEEDS                # (101..104, 201..204) → 16 局
DEFAULT_REF_SEEDS = (101, 102, 103, 104)           # 参考面 8 局（双席）
WIN_RATE_THRESHOLD = _base.WIN_RATE_THRESHOLD      # 0.55（R11 验收：互胜 vs L1 ≥0.55）
V2_EXPECTED_CALLABLES = frozenset({"_cxs_agent"})  # cand 侧（v2 末 callable 与 L1 同名）
L1_EXPECTED_CALLABLES = frozenset({"_cxs_agent"})  # 主面对手侧（L1 本尊）
VERBATIM_EXPECTED_CALLABLES = frozenset({"_cxd_agent"})  # 参考面对手侧（verbatim）
EVIDENCE_NAME = "h2h_evidence.json"
REF_EVIDENCE_NAME = "h2h_ref_evidence.json"


def run(v2_main, l1_main, verbatim_main, seeds: Optional[Sequence[int]] = None,
        ref_seeds: Optional[Sequence[int]] = DEFAULT_REF_SEEDS,
        evidence_path: Optional[str] = None) -> Dict[str, Any]:
    """{n, wins, rate, passed, ref_face, evidence_path}。

    主面：_base.run(v2 为 cand、L1 为对手，seeds 缺省 DEFAULT_SEEDS 双侧期望名
    均 {"_cxs_agent"})；参考面：_base.run(v2 vs verbatim，ref_seeds 缺省
    101-104 双席 8 局，期望名 {"_cxs_agent"}/{"_cxd_agent"})——ref_seeds 传空
    序列即跳过参考面（ref_face 记 skipped；单测控真跑局数用）。passed 只取
    主面裁决；ref_face 只记账（gating=False）。
    """
    target = (os.path.abspath(evidence_path) if evidence_path else os.path.join(
        HERE, "evidence", EVIDENCE_NAME))
    main = _base.run(
        v2_main, l1_main,
        seeds=(DEFAULT_SEEDS if seeds is None else seeds),
        evidence_path=target,
        l1_expected_names=V2_EXPECTED_CALLABLES,
        verbatim_expected_names=L1_EXPECTED_CALLABLES)

    ref_target = os.path.join(os.path.dirname(target), REF_EVIDENCE_NAME)
    if ref_seeds:
        ref = _base.run(
            v2_main, verbatim_main, seeds=ref_seeds, evidence_path=ref_target,
            l1_expected_names=V2_EXPECTED_CALLABLES,
            verbatim_expected_names=VERBATIM_EXPECTED_CALLABLES)
        ref_face: Dict[str, Any] = {
            "n": ref["n"], "wins": ref["wins"], "losses": ref["losses"],
            "ties": ref["ties"], "rate": ref["rate"],
            "evidence_path": ref["evidence_path"]}
    else:
        ref_face = {"n": 0, "wins": 0, "losses": 0, "ties": 0, "rate": 0.0,
                    "skipped": True, "evidence_path": None}
    ref_face["gating"] = False  # 参考面不设阈不进门（R11 门①裁决只看 vs L1）

    # 主台账增记参考面摘要（参考面逐局明细在其自身台账件），单文件可读总账。
    with open(target, "r", encoding="utf-8") as fh:
        evidence = json.load(fh)
    evidence["ref_face"] = ref_face
    with open(target, "w", encoding="utf-8") as fh:
        json.dump(evidence, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    return {"n": main["n"], "wins": main["wins"], "rate": main["rate"],
            "passed": main["passed"], "ref_face": ref_face,
            "evidence_path": target}
