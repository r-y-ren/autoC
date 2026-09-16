---
id: dai2024UAVAssistedTaskOffloading
name: Lyapunov在线UAV支援车联网过载卸载
field: [移动边缘计算, Lyapunov 优化, 车联网]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 长期能量约束经 Lyapunov 优化转化为赤字队列、落到逐时隙在线决策的范式，叠加深圳真实轨迹驱动验证，是数模中预算约束下动态调度/排队类赛题的标准解法骨架
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 热点过载 RSU 的动态支援选择（Markov approximation 策略搜索）可迁移为"移动算力节点支援拥塞服务点"类在线调度题，且不依赖未来信息
    reuse_cost: 中
sources:
  - paper_title: "UAV-Assisted Task Offloading in Vehicular Edge Computing Networks"
    doi: 10.1109/TMC.2023.3259394
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# Lyapunov在线UAV支援车联网过载卸载

## 单行摘要

针对城市热点区域 RSU 过载，引入单架 UAV 作为机动边缘缓冲：不直连车辆，只在 RSU 过载时选择一个过载点承接部分计算负载。用 Lyapunov 优化把 UAV 长期能量预算转化为能量赤字队列、落到逐时隙决策，再在过载 RSU 集合上以 Markov approximation 构造离散时间马尔可夫链搜索近似最优支援策略，在线最小化车辆任务时延并给出时延与长期能量的理论分析。

## 方法快照

- 三层结构：车辆层（V2I 卸载）→ RSU 层（常规边缘算力）→ UAV 层（过载机动支援），过载定义为 RSU 负载超出算力。
- 关键转化：Lyapunov 优化把"长期能量约束"变成能量赤字队列，长期控制问题拆为逐时隙可解子问题。
- 策略搜索：基于 Markov approximation 的离散马尔可夫链在过载集合上搜近似最优策略，有理论支撑而非纯启发式。
- 验证：MindSpore 仿真，Shenzhen IoV trajectory dataset 真实轨迹驱动，部分资产公开。

## 比赛映射要点

- 数模：长期预算约束 + 随机任务到达 + 在线决策是典型题型（如应急资源调度、共享运力调度），Lyapunov 队列化方法可直接作为模型骨架，配真实轨迹数据做驱动仿真即成完整答卷结构。
- 黑客松/算法赛：不加未来信息的在线支援/调度策略与"过载检测 → 支援对象选择"决策流可快速原型化。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Dai2024_车联网中的UAV辅助任务卸载`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `dai2024UAVAssistedTaskOffloading` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 simulation/trace-driven 混合验证形态承自 vault 页自评（artifact_availability: partial），如需引用请以论文原文复核。
