---
id: wang2025OptimizingJointSpeed
name: 低空巡检数据采集的联合速度与高度调度（SSF-ACO）
field: [UAV数据采集, 轨迹优化, 蚁群算法]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 「先证明固定高度下最优速度调度结构性质（SSF），再把一般联合问题改写成 shortest-path 型图交给 ACO」的解法套路是数模优化题的标杆范式；在线版 SSF-ACO-Online 仅比离线高 1.24% 能耗，可直接覆盖信息逐步揭示的在线决策题型
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 覆盖区间随高度变化 + 非线性速度-功率曲线的联合建模把「沿线路飞行」变成结构化图搜索，SSF-ACO 对比 PSO/GA/SA 平均降 13.11% 能耗，是基础设施巡检调度赛题的差异化算法组件
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空经济巡检服务（道路 / 桥梁 / 管线传感器数据采集）的算法内核支撑，直接对应当前低空经济申报热点
    reuse_cost: 低
sources:
  - paper_title: "Optimizing Joint Speed and Altitude Schedule for UAV Data Collection in Low-Altitude Airspace"
    doi: 10.1109/TMC.2025.3591698
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 低空巡检数据采集的联合速度与高度调度（SSF-ACO）

## 单行摘要

低空基础设施（道路、桥梁、管线）沿线传感器巡检中，传感器传输范围随 UAV 飞行高度变化、推进功率又是速度的非线性函数——采集调度不能再简化为「固定高度 + 固定速度」。论文先证明固定高度下最优速度调度的结构性质，提出 Slowest Segment First（SSF）策略；再构建飞行调度图把联合速度-高度-采集顺序问题（JUSAS）改写为 shortest-path 型图问题，交给 SSF-ACO 求解；最后扩展 SSF-ACO-Online，在飞行中逐步发现新传感器时以局部信息多次调用离线求解器完成在线重规划。

## 方法快照

- 场景模型：传感器沿线部署，其数据传输范围与飞行高度相关，高度变化改变覆盖区间及重叠关系；水平功率为速度非线性函数（存在能效最优速度 v*），垂直运动有额外能耗。
- 理论基础：固定高度场景最优速度调度结构（SSF），为一般问题提供分解依据。
- 求解链：SSF → 调度图改造 → SSF-ACO；在线版通过控制通信范围提前探测新传感器并局部重规划。
- 实验结论：SSF-ACO 较 SSF-Only / SSF-PSO / SSF-GA / SSF-SA 平均降 13.11% 能耗（100 次随机实例平均）；在线版仅高 1.24%，并给出在线计算耗时表与参数扫描。平台与代码未披露，无开源。

## 比赛映射要点

- 数模决策类：「结构性质证明 → 图改造 → 元启发求解」三段式是优化类数模题的高分写法模板；在线重规划版本对应动态 / 在线题型。
- 黑客松算法类：沿线巡检、依赖覆盖窗口的采集调度赛题可直接套用高度-覆盖-顺序耦合建模与图搜索解法。
- 双创申报：低空经济基础设施巡检（道路 / 桥梁 / 管线 / 农业设施）服务的核心算法叙事。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wang2025_低空空域数据采集的联合速度与高度调度`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `wang2025OptimizingJointSpeed` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 与 simulation/synthetic 验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
