---
id: shi2024TwoStageStrategyUAVenabled
name: 未知环境下UAV无线供能的搜索-补能两阶段策略
field: [无线供能, 路径规划, 聚类]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 「先搜索目标再补能」的两阶段框架直击农业传感网/农田 IoT 真实部署痛点（节点位置未知、先找到谁需要充电本身就是代价），UMC 搜索+DGC 动态聚类补能可作为智慧农业无人机巡田补能方案的核心技术点
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 按任务流程把探索（未知环境搜索）与优化（动态聚类+补能路线+停留设计）分层的建模思路，适用于未知目标位置下的巡检/充电调度类数模题，避免把全部不确定性压给单一求解器
    reuse_cost: 中
sources:
  - paper_title: "A Two-Stage Strategy for UAV-enabled Wireless Power Transfer in Unknown Environments"
    doi: 10.1109/TMC.2023.3240763
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 未知环境下UAV无线供能的搜索-补能两阶段策略

## 单行摘要

针对传感节点位置未知的 UAV 无线供能（WPT）问题，论文提出"搜索+供能"两阶段策略：第一阶段用 UMC 在未知环境中搜索节点位置，第二阶段用 DGC 依据已发现节点的空间分布动态成簇并设计补能路线与停留方案，同时兼顾搜索效率、总收能量、飞行能耗与能量利用率。

## 方法快照

- 问题设定：多数 WPT 研究假设节点位置已知，本文把"先找到谁需要充电"作为问题主体的一部分，搜索阶段本身计入系统性能。
- 阶段一（UMC）：控制 UAV 在未知区域中搜索尽可能多的传感节点。
- 阶段二（DGC）：按发现节点的空间结构动态聚类成供能簇，再优化补能路线与停留顺序；补能不仅看充电节点（CN）收能，还关注簇内终端节点（EN）的后续能量分配。
- 约束与目标：能量受限 UAV 的飞行能耗与系统能量利用效率联合评估；研究聚焦水平面轨迹与停留，不含复杂三维机动。
- 验证：C++17 仿真（合成场景），i5 2.30GHz/8GB 即可运行，未开源。

## 比赛映射要点

- 数模：两阶段分解是处理"探索+优化"复合题的通用范式——先解决"在哪"，再解决"怎么走"；聚类+路线设计的组合可直接对应数模中的充电车/巡检无人机类赛题。
- 双创申报：农业场景中传感节点散布且无精确坐标是常态；"搜索-成簇-补能"叙事配合低算力实现（i5 级 CPU 可跑），适合写进智慧农业监测项目的可行性论证。

## 关联概念
- 无线供能传输（WPT）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Shi2024_未知环境中UAV无线供能的两阶段策略`（四枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `shi2024TwoStageStrategyUAVenabled` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 C++17 仿真形态承自 vault 页自评（artifact_availability: unknown，未给出完整代码），如需引用请以论文原文复核。
