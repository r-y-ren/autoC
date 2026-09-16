---
id: lin2024LyapunovbasedApproachJoint
name: LI2：灾后 PoI 及时监测的 UAV AoI 路径优化
field: [信息年龄 AoI, 路径优化, 深度强化学习]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 带硬约束的路由巡检题中「DRL 出关键插入决策 + 可解释组合优化算子保图可达与能量可行」的混合范式，比端到端 DRL 稳，AoI 新鲜度还能作为差异化评分目标
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 周期巡检 + 信息新鲜度 + 回站补能约束的建模套路可套到应急监测/设施巡检类数模题，Gurobi 初始解与局部算子改进链可直接写进求解章节
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 真实灾后数据（ARIA damage proxy map）与 Crazyflie 室内实飞双重实证背书，支撑应急监测/精准农业持续巡检方案的可行性论证
    reuse_cost: 低
sources:
  - paper_title: "LI2: A New Learning-Based Approach to Timely Monitoring of Points-of-Interest with UAV"
    doi: 10.1109/TMC.2024.3461708
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# LI2：灾后 PoI 及时监测的 UAV AoI 路径优化

## 单行摘要

面向灾后障碍环境下多 PoI 持续监测问题，提出 DRL 引导的 insert-then-improve 框架 LI2：在一般图可达性与回站补能约束下迭代构造周期巡检路径，最小化最大加权 AoI/平均 AoI 等信息新鲜度指标，在真实灾后数据集与室内实飞中超越学习类基线、逼近 AoI 下界。

## 方法快照

- 问题建模：障碍致非完全图（PoI 与地面站 GCS 为节点，边带飞行时间与能耗），UAV 电量有限需周期性回 GCS 充电，路径由多个闭合子回路组成；目标适配多种 AoI 度量（时间平均 AoI、最大加权 AoI）。
- 初始解：Gurobi 求较好的可行初始周期路线，避免随机起点拖慢收敛。
- 插入阶段：DRL 智能体（PPO + GNN-LSTM，Tianshou 实现）只输出「下一个优先插入哪个 PoI」，算法在全部可行插入位置中选 AoI 最优位置。
- 改进阶段：reconnect/exchange/relocate 等局部算子注入问题特定知识；违反能量约束时按回站切分与局部修补重新可行；micro improvement 在可行前提下继续微调。
- 验证：ARIA damage proxy map 真实灾后数据实例 + Crazyflie 2.1 室内实飞（4x RTX 3090 训练）；论文未明确开放完整代码，部分资产（数据与底层工具）可获取。

## 比赛映射要点

- 黑客松/算法赛：持续监测与巡检覆盖类赛题中，硬约束可行性是端到端 DRL 的短板，LI2 的「学习推荐决策 + 算子保证可行」分工可直接移植；AoI 作为时效性指标可成为方案差异化点。
- 数模：应急监测/巡检调度题的建模模板（非完全图 + 补能闭环 + 加权时效目标），insert-then-improve 求解链完整且可解释。
- 双创申报：真实灾后数据 + 实飞验证的实证形态，是应急/农业巡检方案申报里少见的强背书。

## 关联概念
- 近端策略优化（PPO）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Huang2024_LI2灾后PoI及时监测的UAV_AoI路径优化`（4 枚举字段自该页 frontmatter 迁移）。
- **citekey 与 bib 错配（本次实抓核实）**：分片 citekey `lin2024LyapunovbasedApproachJoint` 在 `kb/raw/vault-bib-map.yaml` 中指向 Lin et al. 的太阳能 UAV MEC Lyapunov 论文（IEEE Internet of Things Journal 2024, doi 10.1109/JIOT.2024.3373491），与页内容（LI2/AoI/PoI 监测）不符；经核对该 citekey 名下 raw 原文（`raw/markdown/lin2024LyapunovbasedApproachJoint.md`），其真实论文为 Huang et al. "LI2: A New Learning-Based Approach to Timely Monitoring of Points-of-Interest with UAV"（正文标注 DOI 10.1109/TMC.2024.3461708），对应 bib 正确条目 `huang2025LI2NewLearningbased`（TMC 2025）。本卡 paper_title/doi/published/venue 自该正确条目回填；文件名与 id 仍保留分片 citekey 以维持溯源链与去重键；错配本身建议主会话在 vault 侧修复。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 承自 vault 页自评（artifact_availability: partial，完整代码未明确开放故 runnable 如实标 false）；能耗线性假设等建模细节如需引用请以论文原文复核。
