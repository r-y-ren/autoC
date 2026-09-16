---
id: yang2023RobustTransitionTrajectory
name: 尾座式无人机鲁棒过渡轨迹优化（PCE不确定性传播）
field: [轨迹优化, 鲁棒优化, 不确定性量化]
published: 2023-01-01
maturity: paper
directions: [数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: Science China Information Sciences
  runnable: false
competition_fit:
  - track: 数模-预测与评估
    edge: PCE 不确定性量化 + 期望与标准差加权鲁棒目标 + 1000 次 Monte Carlo 验证的完整流程，可直接套用于含随机参数波动的预测评估类数模题（评估解的稳健性而非只报最优值）
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 相关随机变量 Gram-Schmidt 正交化 → PCE 传播 → 鲁棒问题转高维确定性优化（扩展惩罚函数求解）的建模范式，适用于要求参数扰动下方案仍可行的稳健决策题
    reuse_cost: 中
sources:
  - paper_title: "Robust Transition Trajectory Optimization for Tail-Sitter UAVs Considering Uncertainties"
    doi: 10.1007/s11432-020-3257-x
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 尾座式无人机鲁棒过渡轨迹优化（PCE不确定性传播）

## 单行摘要

针对尾座式 UAV 悬停-巡航转换的过渡飞行阶段，把初始状态、螺旋桨推力系数与机翼气动系数（后两类相关）的不确定性显式写入轨迹优化：先用 Gram-Schmidt 正交化处理相关随机变量，再经 polynomial chaos expansion（PCE）做不确定性传播，把随机鲁棒优化转化为高维确定性优化并用扩展惩罚函数求解，使过渡轨迹在参数偏差与风扰下更集中、更可靠。

## 方法快照

- 问题设定：给定过渡初末状态，优化控制输入轨迹与过渡时间；目标同时考虑终端状态误差与过程高度变化；约束含迎角、俯仰角、最低高度损失、过渡时间窗。
- 不确定性三源：初始状态、推进系数、机翼气动系数（后两类存在相关性，需先正交化转独立变量）。
- 求解链：相关变量正交化 → PCE 得到状态/代价/约束的均值与方差 → 鲁棒目标写成期望与标准差加权 → 高维确定性优化 + 扩展惩罚函数。
- 验证：理论分析 + 数值仿真；用 1000 次 Monte Carlo 对比确定性优化与鲁棒优化的轨迹散布；开源情况未说明。

## 比赛映射要点

- 数模：很多队伍只交一条「最优」轨迹/方案，本文示范的是把不确定性显式建模后报告「期望-方差」双指标并用 Monte Carlo 验证稳健性的完整写作套路，评估类赛题可直接借鉴为加分结构。
- 方法迁移：PCE + 正交化处理「相关不确定性」的技巧不限于飞行器，凡决策题参数间有相关性（价格-需求、气候-产量）都可用同一链路。
- 局限提示：属控制理论短文，无开源实现、无实飞数据，迁移时需自建动力学/场景仿真。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Yang2023_考虑不确定性的尾座式无人机鲁棒过渡轨迹优化`（vault 页 4 枚举字段 venue_tier=CCF-A、evidence_tier=core、paper_role=anchor、reproducibility_level=medium 已迁移至本卡）。
- bib 回填：citekey `yang2023RobustTransitionTrajectory` → 标题/venue/DOI 来自 vault 自带 Zotero bib（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2023），按年-01-01 填写；验证类信息（theory + simulation/synthetic/复现性 medium、开源未说明故 runnable=false）承自 vault 页自评，如需引用请以论文原文复核。
