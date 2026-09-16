---
id: zema20243DTrajectoryOptimization
name: TRA/EDD：智慧城市多任务UAV补能设施与三维轨迹优化
field: [UAV 轨迹优化, MILP, 智慧城市]
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
    edge: 补能停靠、数据下载与访问顺序耦合的离线 MILP 建模 + 在线反应式规划的对照结构，正是数模优化题「全局 benchmark 对比在线近似策略」的现成模板，且平台链（NS3+CPLEX）披露完整
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: TRA/EDD 基础设施设定把无人机持续作业从「电池换电」升级为「补能+数据同步一体化节点」，可直接支撑智慧农业机库/换电站网络规划申报
    reuse_cost: 低
sources:
  - paper_title: 3D Trajectory Optimization for Multimission UAVs in Smart City Scenarios
    doi: 10.1109/TMC.2022.3215705
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# TRA/EDD：智慧城市多任务UAV补能设施与三维轨迹优化

## 单行摘要

面向智慧城市多任务 UAV 的持续作业问题，引入训练与补能区域（TRA）及能量与数据分发节点（EDD）两类基础设施，让 UAV 在任务执行中机会性停靠完成补能与高速数据下载；分别建立离线 MILP 全局模型（M1/M2 双目标，CPLEX 求解）与在线事件驱动反应式规划（NS3 实现），并给出两者的工程对照结论。

## 方法快照

- 系统设定：TRA 是区域级设施，EDD 是区内具体补能/数据节点；多 UAV 共享 EDD 带宽，连接分配直接影响停留时间。
- 预仿真回填：先用 NS3 测定不同并发连接数下的带宽与下载耗时（如 10 MB 下载时间），再把实测通信参数回填给离线优化模型。
- 离线模型：完整先验下写成 MILP（M1 与 M2 两类目标），小规模实例可作 benchmark，但计算开销随规模指数增长。
- 在线模型：NS3 中以 mobility model + application 形式实现 UAV 与 EDD 交互的事件驱动近似决策，更适合实际运行。
- 验证为数值仿真（合成智慧城市场景），平台与内存配置披露较完整（NS3 3.30、Java、CPLEX 12.x）。

## 比赛映射要点

- 数模优化题：多任务调度 + 资源（带宽/充电桩）共享 + 时限约束的问题结构与「离线最优做上界、在线策略做落地」的写法可整体移植到车辆/无人机/机器人调度题。
- 双创申报：农业无人机机库、换电与数据回传一体化站点的选址与调度论证可复用其 TRA/EDD 抽象；在线方案说明「无先验也要能跑」的工程可行性。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zema2024_智慧城市多任务UAV的三维轨迹优化`（4 枚举字段承自页 frontmatter）。
- bib 回填：citekey `zema20243DTrajectoryOptimization` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性 medium 与验证类型（simulation/synthetic）承自 vault 页自评；论文未说明开源情况，如需引用请以原文复核。
