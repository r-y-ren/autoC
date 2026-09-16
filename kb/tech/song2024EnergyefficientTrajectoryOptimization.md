---
id: song2024EnergyefficientTrajectoryOptimization
name: 无线充电UAV辅助MEC的多目标RL轨迹优化（MORL-TER）
field: [多目标强化学习, 轨迹优化, 无线供能]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 能效与任务采集量双目标写成向量奖励 MOMDP，一套参数化策略（MORL-TER 改善 trace-based 经验回放）适配全部偏好权重、免每权重重训，是多目标权衡类数模题的高效求解范式，替代线性标量化
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 高空平台激光补能与任务采集/机载计算一体化的"边充边作业"航迹方案，可支撑植保/巡检无人机续航痛点的智慧农业申报技术点（供能作为轨迹设计的一等变量是差异化叙事）
    reuse_cost: 中
sources:
  - paper_title: "Energy-Efficient Trajectory Optimization with Wireless Charging in UAV-assisted MEC Based on Multi-Objective Reinforcement Learning"
    doi: 10.1109/TMC.2024.3384405
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 无线充电UAV辅助MEC的多目标RL轨迹优化（MORL-TER）

## 单行摘要

在 HAP 激光补能的 UAV 辅助 MEC 系统中，论文把"能效最大化"与"任务采集数量最大化"写成带向量奖励的 MOMDP，并在 EMOQL 基础上设计 trace-based experience replay 得到 MORL-TER——训练后的参数化策略在给定偏好权重时直接输出对应轨迹，无需为每种偏好单独重训，从而覆盖整个偏好空间并适配动态偏好。

## 方法快照

- 系统构成：高空平台（HAP）经激光束为 UAV 持续供能；UAV 一边飞行一边采集地面智能设备（GSD）的计算任务并在机载队列中处理。
- 双目标冲突：任务采得越多，机载处理与飞行能耗越高；能效与任务量天然冲突，不宜线性标量化强行合并。
- 建模：状态、偏好与向量奖励统一写入 MOMDP，两个目标保持独立语义。
- 算法：在 EMOQL 框架引入 TER（trace-based experience replay），缓解经验回放偏差、提高样本效率；决策时按给定偏好权重直接输出轨迹策略。
- 行为解释：偏好偏能效时倾向稀疏区域与更少任务，偏任务量时积极进入高密集区域。
- 验证：Python 仿真器 + PyTorch 1.7，6 组测试实例、完整参数表与网络结构，未公开代码。

## 比赛映射要点

- 数模：多目标题普遍用加权和压成单目标；本卡给出"向量奖励 + 偏好条件化策略"的学习法替代——一次训练即可按评委/用户偏好切换解，Pareto 分析章节可直接借其实验设计（多组偏好权重扫描）。
- 双创申报：把"补能"写成轨迹决策的一等变量（而非背景假设），配合 HAP/激光补能的前沿概念，可为无人机续航类痛点提供有记忆点的方案叙事。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Song2024_基于多目标强化学习的无线充电UAV辅助MEC轨迹优化`（四枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `song2024EnergyefficientTrajectoryOptimization` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 Python/PyTorch 数值仿真形态承自 vault 页自评（artifact_availability: unknown，未公开实现代码），如需引用请以论文原文复核。
