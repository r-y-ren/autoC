---
id: zhang2024UAVSwarmenabledCollaborative
name: 时间域合谋窃听下的UAV集群协同安全中继（UVAA+IMOGOA）
field: [协同安全中继, 协作波束形成, 多目标优化]
published: 2024-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: "UAV 集群虚拟天线阵列（UVAA）+ 阵列权重/节点选择/位置/服务顺序混合变量的三目标 Pareto 优化（改进蚱蜢算法 IMOGOA），多目标元启发式求解器与'速率-安全-能耗'折中结构可迁移到无人机/传感网赛题的协同传输设计"
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: "连续变量（阵列激励、位置）与组合变量（节点选择、关联顺序）混排的多目标优化问题建模与 Pareto 前沿求解流程，可作为数模多目标决策题的求解器备选，与 NSGA-II 类基线对比形成差异化"
    reuse_cost: 中
sources:
  - paper_title: "UAV Swarm-Enabled Collaborative Secure Relay Communications with Time-Domain Colluding Eavesdropper"
    doi: 10.1109/TMC.2024.3350885
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 时间域合谋窃听下的UAV集群协同安全中继（UVAA+IMOGOA）

## 单行摘要

用 UAV swarm 作为协同安全中继，在配备平面阵列（PAA）的地面微基站与 IoT 终端之间建立协作波束形成中继链路；针对可跨时隙合并信息的时间域合谋窃听者，把基站/UAV 阵列激励权重、UAV 接收节点选择、机群空间位置与用户服务顺序统一为三目标问题 US2RMOP（合法总速率最大、窃听总速率最小、机群能耗最小），用改进多目标蚱蜢算法 IMOGOA 搜索 Pareto 折中。

## 方法快照

- 结构创新：UAV 集群组织成 UVAA 虚拟阵列与基站阵列协同波束赋形——空间位置与阵列控制耦合为同一问题，超出"UAW 当中继拉链路"的传统视野。
- 威胁模型：时间域合谋窃听者可跨时隙汇聚截获信息，因此瞬时链路优化不足，必须做全局多目标安全折中。
- 问题性质：US2RMOP 非凸、NP-hard、连续与离散变量混排。
- 求解：IMOGOA（改进多目标 grasshopper 算法）做近 Pareto 搜索，充分利用机群可重构性。
- 实验结论：在 2/4/8/16 架 UAV 等设置下对比传统多跳中继、LAA relay、MRS/LRS 策略，三目标折中更优。
- 验证：仿真（合成 IoT 中继与窃听拓扑，平台与代码未披露）。

## 比赛映射要点

- 黑客松/算法赛：多无人机/多节点协同传输类赛题中，"把集群当可重构虚拟阵列 + 三目标 Pareto 折中"的问题定义方式是差异化论证；IMOGOA 可直接替换常用的 NSGA-II/PSO 求解位。
- 数模多目标决策题：混合变量多目标优化的完整建模范式（目标冲突刻画 → Pareto 求解 → 折中方案选取），适合作为决策类论文的求解框架参考。

## 关联概念
- 协同安全中继通信

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhang2024_时间域合谋窃听下的UAV集群协同安全中继`（4 枚举字段自 vault 页 frontmatter 迁移，reproducibility_level=medium）。
- bib 回填：citekey `zhang2024UAVSwarmenabledCollaborative` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真设置有披露但无平台与代码）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
