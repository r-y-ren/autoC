---
id: jia2024EnergyTimeTradeoff
name: 多 UAV IoT 数据采集时间-能量权衡（MSMOACO）
field: [多目标优化, UAV 数据采集, 蚁群优化]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE/ACM Transactions on Networking
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: worst-case 双目标（最大任务完成时间 + 最大能量消耗）的 Pareto 折中建模加多策略多目标蚁群 MSMOACO 求解链，是数模「兼顾效率与公平」调度题的完整可复用模板，20 次重复实验的报告方式也贴合数模论文规范
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: 任务分配/访问序列/悬停位置/飞行速度联合编码与几何避碰修正，可直接嵌入多机器人调度赛题的元启发式求解器，自适应悬停优化是少见的采集效率组件
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 植保/巡田多机作业的时间-能耗-避碰联合调度与按任务偏好从 Pareto 解集选解的决策叙事，是智慧农业无人机集群方案的直接支撑点
    reuse_cost: 低
sources:
  - paper_title: "Energy and Time Trade-off Optimization for Multi-UAV Enabled Data Collection of IoT Devices"
    doi: 10.1109/TNET.2024.3450489
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 多 UAV IoT 数据采集时间-能量权衡（MSMOACO）

## 单行摘要

把多 UAV 物联网数据采集中的任务完成时间与能量消耗作为并列的 worst-case 目标（最大完成时间、最大能耗），联合优化每架 UAV 的轨迹、悬停位置、飞行速度与避碰策略，用嵌入适应度引导变异、自适应悬停优化和几何避碰的多策略多目标蚁群算法 MSMOACO 搜索 Pareto 前沿，输出一组可按任务偏好选取的折中解。

## 方法快照

- 问题建模：多 UAV 从给定起点出发访问负责的 IoT 设备集合后回到终点；悬停位置可调以平衡访问精度与飞行代价；显式加入最小安全间距的几何避碰。
- 双目标：不优化总和而是同时压低两个 worst-case 指标——最慢 UAV 的完成时间与最累 UAV 的能耗，避免单目标最优把负担压在少数机上。
- MSMOACO：编码设备分配 + 访问序列 + 悬停位置 + 速度控制；改进 ACO 生成可行轨迹，多策略变异与 Pareto 支配维护解集，冲突场景由几何避碰策略实时修正局部飞行段。
- 验证：合成 IoT 分布数值仿真，多场景参数与 20 次重复实验；平台/硬件/开源情况论文未说明。

## 比赛映射要点

- 数模：多目标调度是常考题型，「max-max 双目标 + Pareto 前沿 + 按偏好选解」的完整叙事与元启发式求解链可直接迁移，且报告口径规范。
- 黑客松/算法赛：多机路径 + 避碰 + 悬停优化的组件化程度高，能拼装进无人机/机器人赛题的求解器。
- 双创申报：精准农业多机作业的能耗与时效权衡是评审关心点，Pareto 决策叙事显专业。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Jia2024_多UAV物联网数据采集的时间能量权衡优化`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `jia2024EnergyTimeTradeoff` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16），页内容与 bib 条目相符。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 承自 vault 页自评（artifact_availability: unknown，故 runnable 如实标 false）；Pareto 前沿形状等结果如需引用请以论文原文复核。
