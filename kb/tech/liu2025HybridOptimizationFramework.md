---
id: liu2025HybridOptimizationFramework
name: UaMCS 混合优化框架：信任约束下的全局 AoI 最小化
field: [UAV 群智感知, AoI 优化, 深度强化学习]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 把数据质量（工人信任）内生进 AoI 时效优化的建模思路，适配数据采集/传感网调度类开放题，区别于把数据真实性当外部假设的常规路径规划解法
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: D3QN 的状态-动作设计与"信任值更新 → 下一跳补采决策"闭环可直接迁移到动态环境下的采样/巡检调度题，给出可演示的在线决策组件
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业多源监测（人工网点 + 无人机补采）人机协同采集方案的技术支撑，信任评估机制正面回应评审对数据质量与系统可靠性的质疑
    reuse_cost: 低
sources:
  - paper_title: "A Hybrid Optimization Framework for Age of Information Minimization in UAV-assisted MCS"
    doi: 10.1109/TSC.2025.3528339
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# UaMCS 混合优化框架：信任约束下的全局 AoI 最小化

## 单行摘要

面向 UAV 与工人协同的城市级移动群智感知，提出"基于信任的任务分配（GMTA）+ 基于 D3QN 的 UAV 路径规划（DRL-GAM）"混合优化框架，把工人可信度显式并入 AoI 优化，在信任与能量双重约束下最小化全局信息年龄。

## 方法快照

- 系统结构：平台 + 大量工人（便宜但可能提交虚假数据）+ 单架 UAV（可信灵活但能量受限）+ 感知节点；工人覆盖城市可达热点，UAV 补采工人无法抵达或失约的区域。
- GMTA：在负载约束下按任务紧急性与工人信任分数分配任务——更紧急的任务优先给高可信工人；信任值由直接信任与推荐信任按上报质量持续更新，抑制恶意工人对 AoI 估计的干扰。
- DRL-GAM：UAV 路径规划建模为 MDP，用 D3QN 从当前全局 AoI 状态学习最优下一动作；UAV 路径被工人执行结果持续驱动，形成"信任评估 → 动态补采"闭环。
- 关键立场：AoI 最小化不能把"数据一定真实"当作默认前提——只优化路径而不考虑工人信任，AoI 估计本身就可能是错的；把数据质量与时效目标统一进同一决策框架是本文真正亮点。
- 验证：真实数据驱动的数值仿真（MATLAB R2022a、CVX、SeDuMi；3.20 GHz 双核 CPU、32 GB 内存）；论文未披露具体数据集名称，开源情况未说明。

## 比赛映射要点

- 数模（数据分析与决策）：数据采集/传感网调度类赛题中，"信任 × 新鲜度"双目标建模是现成的差异化框架；平台-工人-UAV 三层实体结构可直接对应当赛题的多主体协同设定。
- 黑客松（数据与算法）：GMTA 优先级分配 + D3QN 在线路径决策是两块可独立演示的组件；"UAV 路径被工人执行结果驱动"的闭环叙事在答辩中容易讲清。
- 双创（文书与申报）：智慧农业多源监测的人机协同采集方案（人工巡田 + 无人机补采盲区）技术支撑点，信任评估模块回应数据可靠性问题。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Liu2025_面向UaMCS全局AoI最小化的混合优化框架`（frontmatter venue_tier/evidence_tier/paper_role/reproducibility_level 已映射到本卡 4 枚举字段）。
- bib 回填：citekey `liu2025HybridOptimizationFramework` → 标题/venue/DOI 来自 vault 自带 Zotero bib（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation + trace_driven、真实数据集名称缺失、复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
