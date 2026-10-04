"""按 R11 裁决清单把法证脚本分三档（保留/工具箱/归档）并产出迁移映射注册表条目，未分类件即失败（fail-closed 逐件列出）。

上游: R11（详见 fn_docs/responsibility.md）

实现要点：
- 裁决清单为模块级唯一事实源 ADJUDICATED_TIERS（R11 三档具名清单）：保留档
  5 件 permanent-gate、工具箱档 3 件、归档档 18 件单次法证——每件
  {tier, reason, precondition}；唯 v143 带 precondition="run_official_bench
  已吸收 seated（B3 完成）"（W3 依赖 W1 的波间契约）。
- 输入 script_list 逐件归一为 basename（容忍路径形态），凡不在裁决清单者即
  "未分类件"→ ValueError 逐件列出（fail-closed，不静默丢弃）；重复件亦拒。
- R11 的裁决范围=法证脚本子集（26 件）；scripts/ 中评估链/库件等其余脚本
  属其他需求管辖（R15 market_ledger 归位、R1-R9 评估链吸收等），不进本
  注册表——范围裁剪由调用方 archive_forensic_assets 负责（实际清单∩裁决
  清单，并向注册表登记范围外清单，不静默）。
- 输出为 {保留, 工具箱, 归档} 映射 + counts + 扁平 entries（注册表直写形态，
  每件 {file, tier, reason, precondition}，precondition 无则为 None）。
"""

from __future__ import annotations

from pathlib import Path

__all__ = ["partition_script_tiers", "ADJUDICATED_TIERS",
           "TIER_RETAIN", "TIER_TOOLBOX", "TIER_ARCHIVE", "TIER_ORDER"]

TIER_RETAIN = "保留"
TIER_TOOLBOX = "工具箱"
TIER_ARCHIVE = "归档"
TIER_ORDER = (TIER_RETAIN, TIER_TOOLBOX, TIER_ARCHIVE)

_V143_PRECONDITION = "run_official_bench 已吸收 seated（B3 完成）"

# R11 裁决清单（fn_docs/requirements.md R11 + 块引言）：文件名 → 三档裁决。
# 保留/工具箱件留主线原位；归档件战后按注册表 dest 搬移（本批零物理移动）。
ADJUDICATED_TIERS: dict[str, dict] = {
    # ---- 保留档（permanent-gate，5 件）----
    "twin_fidelity.py": {
        "tier": TIER_RETAIN,
        "reason": "permanent-gate：孪生保真常驻门禁，R11 裁决留主线", "precondition": None},
    "planner_flagoff_golden.py": {
        "tier": TIER_RETAIN,
        "reason": "permanent-gate：旗关黄金复验门，R11 裁决留主线", "precondition": None},
    "v48_derivative_launch_check.py": {
        "tier": TIER_RETAIN,
        "reason": "permanent-gate：v48 衍生发射前检查门，R11 裁决留主线", "precondition": None},
    "v48plus_launch_check.py": {
        "tier": TIER_RETAIN,
        "reason": "permanent-gate：v48+ 发射前检查门，R11 裁决留主线", "precondition": None},
    "p41_official_load_probe.py": {
        "tier": TIER_RETAIN,
        "reason": "permanent-gate：P41 官方装载探针，R11 裁决留主线", "precondition": None},
    # ---- 工具箱档（3 件）----
    "m4_switchover_regression.py": {
        "tier": TIER_TOOLBOX,
        "reason": "工具箱：M4 切换回归工具，R11 裁决限定 --golden-only 通道留用",
        "precondition": None},
    "solver_shadow_stats.py": {
        "tier": TIER_TOOLBOX,
        "reason": "工具箱：求解器影子统计工具，R11 裁决留用", "precondition": None},
    "sprintA_structure_probe.py": {
        "tier": TIER_TOOLBOX,
        "reason": "工具箱：SprintA 结构探针，R11 裁决留用", "precondition": None},
    # ---- 归档档（单次法证，18 件）----
    "round23_disaster_dtsp_probe.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：round-23 灾难局 DTSP 探针，裁决已留痕 JOURNAL/digests（G13→R11）",
        "precondition": None},
    "round23_dtsp_engagement_probe.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：round-23 DTSP 接合探针，裁决已留痕（G13→R11）",
        "precondition": None},
    "round23_dtsp_stepdiff_probe.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：round-23 DTSP 步差探针，裁决已留痕（G13→R11）",
        "precondition": None},
    "round23_loss_forensics.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：round-23 损失法证，裁决已留痕（G13→R11）",
        "precondition": None},
    "round24_counterfactual_probe.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：round-24 反事实探针，裁决已留痕（G13→R11）",
        "precondition": None},
    "round24_d0_counterfactual.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：round-24 d0 反事实，裁决已留痕（G13→R11）",
        "precondition": None},
    "round24_loss_forensics.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：round-24 损失法证，裁决已留痕（G13→R11）",
        "precondition": None},
    "v15_h2h_v48.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：v15 对 v48 h2h 对照，裁决已留痕（G13→R11）",
        "precondition": None},
    "v15_d0_counterfactual_giants.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：v15 d0 巨人反事实，裁决已留痕（G13→R11）",
        "precondition": None},
    "v15_regression_gate.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：v15 回归门，裁决已留痕（G13→R11）",
        "precondition": None},
    "v143_sellrace_gates.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：v14.3 sellrace 三门裁决已留痕；seated 通道已被 fn_work "
                  "run_official_bench 吸收（B3），归档不损失可复算性（G13→R11）",
        "precondition": _V143_PRECONDITION},
    "v3_readmission_suite.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：v3 复裁套件（席位错位通道历史记录，修正版在 fn_work），"
                  "裁决已留痕（G13→R11）",
        "precondition": None},
    "v31_pressure_calibration.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：v31 压力定标，裁决已留痕（G13→R11）",
        "precondition": None},
    "planner_calibration_suite.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次定标：planner 定标套件，结论已留痕（G13→R11）",
        "precondition": None},
    "v48plus_ab_gate.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：v48+ A/B 门消融，裁决已留痕（G13→R11）",
        "precondition": None},
    "v48plus_layer_ablation.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：v48+ 层消融，裁决已留痕（G13→R11）",
        "precondition": None},
    "v48plus_metrics.py": {
        "tier": TIER_ARCHIVE,
        "reason": "单次法证：v48+ 指标提取，结论已留痕（G13→R11）",
        "precondition": None},
    "profile_v48_gap.py": {
        "tier": TIER_ARCHIVE,
        "reason": "一次性剖析：v48 缺口画像（C 审查登记路径损坏件），结论已留痕（G13→R11）",
        "precondition": None},
}


def partition_script_tiers(script_list) -> dict:
    """按 R11 裁决清单把脚本清单分三档，产出迁移映射（注册表条目形态）。

    Args:
        script_list: 脚本文件可迭代（basename 或含路径形态，逐件归一为
            Path(...).name）；调用方（archive_forensic_assets）负责先按
            裁决范围裁剪实际清单——本函数对范围外件零容忍。

    Returns:
        dict：
        {"保留": [条目…], "工具箱": [条目…], "归档": [条目…],
         "counts": {"保留": n, "工具箱": n, "归档": n},
         "entries": [全部条目按文件名排序]}
        条目 = {"file": 文件名, "tier": 保留|工具箱|归档, "reason": str,
                "precondition": str|None}。

    Raises:
        ValueError: 未分类件（不在 R11 三档裁决清单）或重复件——fail-closed
            逐件列出，不静默丢弃。
    """
    raw_names = [Path(str(item)).name for item in script_list]
    duplicates = sorted({n for n in raw_names if raw_names.count(n) > 1})
    if duplicates:
        raise ValueError(f"脚本清单含重复件，拒绝划分: {duplicates}")
    names = sorted(set(raw_names))

    unclassified = [n for n in sorted(names) if n not in ADJUDICATED_TIERS]
    if unclassified:
        raise ValueError(
            f"未分类件 {len(unclassified)} 件（不在 R11 三档裁决清单），fail-closed 拒绝划分:\n"
            f"  {unclassified}\n"
            f"排查: ①新法证脚本须先经裁决入清单（fn_docs/requirements.md R11）"
            f"再进划分；②评估链/库件等非 R11 管辖脚本应由调用方裁剪出范围"
            f"（并向注册表登记范围外清单），不得混入本划分。"
        )

    tiers: dict[str, list[dict]] = {tier: [] for tier in TIER_ORDER}
    for name in sorted(names):
        ruling = ADJUDICATED_TIERS[name]
        tiers[ruling["tier"]].append({
            "file": name,
            "tier": ruling["tier"],
            "reason": ruling["reason"],
            "precondition": ruling["precondition"],
        })

    return {
        **{tier: tiers[tier] for tier in TIER_ORDER},
        "counts": {tier: len(tiers[tier]) for tier in TIER_ORDER},
        "entries": [entry for tier in TIER_ORDER for entry in tiers[tier]],
    }
