---
id: yuan2025TrajectoryOptimizationPower
name: CATEN：多UAV空中基站轨迹与功率的通信型MARL联合优化
field: [UAV 通信, 多智能体强化学习, 资源分配]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: low
signal:
  venue: IEEE Transactions on Computers
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: CTDE 范式下把轨迹与功率作为联合动作输出，跨智能体经验检索共享 + 多头注意力 critic 可直接移植到多机协同调度与覆盖类赛题，区别于只共享状态的朴素 MADRL 基线
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 无人机空中基站为地面用户/农田传感节点提供弹性通信覆盖的完整系统模型与多目标（QoS 满足数与能耗）论证，支撑智慧农业空中通信中继方案申报
    reuse_cost: 低
sources:
  - paper_title: "Trajectory Optimization and Power Allocation for Multi-UAV Wireless Networks: A Communication-Based Multi-Agent Deep Reinforcement Learning Approach"
    doi: 10.1109/TC.2025.3587976
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# CATEN：多UAV空中基站轨迹与功率的通信型MARL联合优化

## 单行摘要

针对多架 UAV 作为空中基站（UAV-ABS）服务地面用户的协同通信问题，提出通信增强的多智能体深度强化学习框架 CATEN——在 CTDE 范式下联合输出轨迹与功率动作，通过 encoder-retrieve-update 的跨 UAV 经验共享机制过滤冗余信息，并用多头注意力 critic 捕捉不同维度协作特征，以最大化满足 QoS 的用户数、最小化系统能耗。

## 方法快照

- 问题建模：Markov game，N 架 UAV-ABS 与 M 个地面用户在连续时隙内协同，轨迹与功率是天然耦合的双重控制变量；目标为「QoS 满足用户数」与「UAV 能耗」的多目标平衡。
- 通信内生化：跨 UAV 经验经编码、检索、更新三步组织共享，显式筛选有效协同信号——通信机制是算法本体而非附加条件。
- 多头注意力 critic：从多个协作特征维度评估联合动作质量，缓解局部观测与强耦合带来的评估偏差。
- 联合决策回路：actor 同时给出「移动到哪里」与「以多大功率服务谁」，验证类型为数值仿真（合成场景），复现性 low。

## 比赛映射要点

- 黑客松/算法赛：多机协同覆盖、任务分配类赛题中，「带通信筛选机制的 MADRL + 多头注意力 critic」是超越朴素 MADRL/MAPPO 基线的差异化组件；经验检索机制可降维成启发式共享策略快速落地。
- 双创申报：空中基站补盲、农业传感数据回传场景的系统模型与能耗-QoS 权衡论证可直接复用为申报书技术路线段落。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Yuan2025_多UAV无线网络轨迹与功率联合优化`（4 枚举字段承自页 frontmatter）。
- bib 回填：citekey `yuan2025TrajectoryOptimizationPower` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性 low 与验证类型（simulation/synthetic）承自 vault 页自评；论文未披露开源代码，如需引用请以原文复核。
