---
id: li2025FederatedMetalearningBased
name: GFL-PEARL：联邦元学习驱动的UAV辅助VEC能时延权衡卸载
field: [联邦元学习, 计算卸载, UAV 辅助车边缘计算]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 能耗时延统一代价的 MDP 建模加动态任务优先级采样，可直接迁移到任务分配与资源调度类决策题；个性化快速适配思路对异构主体（不同地块/设备/农户）差异化调度有直接借鉴
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 把上下文建模为 DAG 并用 GNN 重构 PEARL 推断网络的元学习骨架，可用于边缘调度或个性化策略类算法题，明确差异化于普通联邦学习全局聚合基线
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 农机与无人机边缘计算的隐私保护协同学习方案技术支撑（TMC 2025，联邦元学习个性化卸载，不上传原始数据）
    reuse_cost: 低
sources:
  - paper_title: "Federated Meta-Learning Based Computation Offloading Approach with Energy-Delay Tradeoffs in UAV-assisted VEC"
    doi: 10.1109/TMC.2025.3573278
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# GFL-PEARL：联邦元学习驱动的UAV辅助VEC能时延权衡卸载

## 单行摘要

面向交通拥堵形成的临时热点 VEC 场景，将 UAV 辅助计算卸载建模为能耗-时延加权代价的 MDP，提出联邦元学习框架 GFL-PEARL：先按热点任务密度优化 UAV 部署，再把上下文表示为 DAG 并用 GNN 重构 PEARL 推断网络，使异构任务车辆在不上传原始数据的前提下快速获得个性化卸载策略，降低平均成本与任务超时率。

## 方法快照

- 问题结构：不同车辆任务与数据分布差异大，统一全局策略泛化差；普通联邦学习只做全局聚合会损失个体适应能力。
- 部署层：先基于热点区域任务密度优化 UAV 位置，保证机动边缘节点覆盖高需求车流。
- 决策层：卸载决策写成 MDP，时延与能耗进统一代价函数，任务支持本地/UAV/RSU/邻近车辆多元卸载。
- 学习层：GFL-PEARL 用 DAG 建模上下文过程，以 GNN 强化 PEARL 的任务相关性提取；训练中动态调整任务优先级提升样本效率。
- 验证：仿真+原型（OMNeT++、SUMO，UAV 搭载 Raspberry Pi，公开数据集 YawDD 与 State Farm）；开源情况未说明。

## 比赛映射要点

- 数模决策题：能耗-时延联合代价 + 任务优先级的调度建模范式，可套用到任务分配、算力调度类题目；元学习个性化适配对应异构决策主体的差异化策略。
- 黑客松算法题：DAG+GNN 的上下文编码与元学习快速适配是可移植组件，对个性化/少样本适应类赛题区别于纯 FL 或纯 RL 基线。
- 双创申报：农业机械/无人机协同作业场景下的隐私保护边缘智能方案支撑。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Li2025_联邦元学习驱动的UAV辅助VEC能时延权衡卸载`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `li2025FederatedMetalearningBased` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按年-01-01 填写；验证类信息（simulation+prototype/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
