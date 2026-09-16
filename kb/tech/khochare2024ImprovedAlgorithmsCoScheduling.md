---
id: khochare2024ImprovedAlgorithmsCoScheduling
name: UAV机队航线与机载边缘分析共调度（MSP）
field: [任务调度, 边缘计算, 无人机路径规划]
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
    edge: 访问路径与机上 DNN 推理统一进一个带截止期与能量预算的效用最大化模型，MILP 最优基线+五个启发式调度器的组合是巡检/配送/任务指派类赛题的标准解题骨架，且给出 NP-hard 证明与真实能耗约束
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 五个启发式调度器按负载权衡效用与运行时，可直接移植为调度算法赛的原型与对比基线；真实飞行/悬停/机载推理能耗轨迹回放验证（Jetson TX2 实机）是答辩可信度亮点
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 多机巡检边飞边算的作业模式（航线与机载 AI 推理共调度）支撑智慧农业植保巡检降本增效的量化论证
    reuse_cost: 低
sources:
  - paper_title: "Improved Algorithms for Co-Scheduling of Edge Analytics and Routes for UAV Fleet Missions"
    doi: 10.1109/TNET.2023.3277810
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# UAV机队航线与机载边缘分析共调度（MSP）

## 单行摘要

针对无人机编队执行视觉巡检时「飞到哪里」与「何时在机上完成分析」两个决策耦合、分开优化会错过时限或浪费能源的问题，提出 Mission Scheduling Problem：同时建模航线、悬停观测、机载 DNN 推理、活动截止期与能量预算，证明 NP-hard 后以 MILP 给出最优基线，并设计五个启发式调度器做效用与运行时权衡，最后用真实四旋翼的飞行/悬停/推理能耗轨迹回放调度时间线，检验计划在真实电量条件下的可完成率。

## 方法快照

- 问题建模：每个活动既需被访问采集，也可能需在机上完成 DNN 推理；效用由采集价值、按时分析与机上处理价值共同组成。
- 复杂度与基线：MSP 证明为 NP-hard；IBM CPLEX v12 求解 MILP 得最优解基线。
- 五个启发式调度器：CS、RSS、HUFD、EOFO、IPS，在不同负载/活动类型下比较效用与运行时。
- 可行性回放：基于 X-wing 四旋翼（Pixhawk2 + Jetson TX2）真实飞行/悬停/机载推理能耗轨迹回放任务时间线，评估真实电量下行程完成率；路网数据用 OpenStreetMap Bangalore 子集。

## 比赛映射要点

- 数模：路径规划 + 任务调度联合优化是高频题型（巡检、配送、指派），「MILP 最优基线 + 启发式近似」的论证结构与截止期/能量双约束建模可直接迁移。
- 黑客松/算法赛：多调度器对比 + 真实能耗回放的评估方法本身即可作为赛题方案模板；航线层与分析层画在同一时间线上的建模技巧通用。
- 双创申报：智慧农业巡检场景的边飞边算作业模式，用能耗轨迹数据支撑降本增效论证。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Khochare2024_无人机编队任务中边缘分析与航线共调度`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `khochare2024ImprovedAlgorithmsCoScheduling` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 simulation/trace-driven/field_test 混合验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
