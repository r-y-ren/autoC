---
id: li2024MultiObjectiveOptimizationUAV
name: 双侧虚拟天线阵列UAV辅助IoT多目标优化（EMSSA）
field: [UAV 辅助 IoT, 协作波束形成, 多目标优化]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: low
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 混合变量大规模多目标优化器 EMSSA（二进制/整数/连续/排序变量分别设计初始化与更新算子 + 混沌映射调参），可替换 NSGA-II/MOPSO 基线形成差异化求解组件
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 时间-安全-能耗三目标 Pareto 建模加按偏好从解集选折中解的决策流程，是数模多目标决策题的标准论证骨架
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业传感网数据采集场景（地面 IoT 集群 + 无人机回传基站）的技术支撑点，含面向窃听方向旁瓣整形的物理层安全亮点
    reuse_cost: 低
sources:
  - paper_title: "Multi-Objective Optimization for UAV Swarm-Assisted IoT With Virtual Antenna Arrays"
    doi: 10.1109/TMC.2023.3298888
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 双侧虚拟天线阵列UAV辅助IoT多目标优化（EMSSA）

## 单行摘要

面向多 IoT 集群到远程基站的数据采集与分发，在地面传感器侧与空中 UAV 侧同时构造协作波束形成的 GVAA/AVAA 虚拟天线阵列，把任务完成时间、窃听方向总旁瓣电平、UAV 总能耗建成三目标 MOP，并提出混合变量群智能优化器 EMSSA 求 Pareto 解集——用「协作波束形成增强链路」替代「UAV 频繁飞行弥补链路」，从范式上降低移动成本。

## 方法快照

- 系统三层：地面 IoT 集群选传感器组 GVAA 定向发给选中 UAV；UAV 群内部广播同步；再按 BS 访问顺序组 AVAA 依次分发。
- 安全建模：不直接最大化 secrecy rate，而是把窃听方向的总旁瓣电平作为独立优化目标压低（阵列方向图安全整形）。
- 能耗模型：旋翼 UAV 推进功率拆成悬停/传输能耗与阵列构形机动能耗两部分。
- 问题性质：传感器选择（二进制）、空中接收 UAV 选择（整数）、位置与激励权重（连续）、BS 访问顺序（排序）混合变量，NP-hard 大规模问题。
- EMSSA 三类增强：分变量类型可行初始化（连续部分用 Weierstrass 函数）、关键参数混沌映射、分变量 mutation/扰动/PMX 交叉更新。
- 验证：合成场景仿真（16/32 UAV、8 BS 规模），对比 RandomLAA/MSSA/MOSPO/MOMVO/MODA/MOPSO，未开源。

## 比赛映射要点

- 黑客松/算法赛：混合变量多目标优化题可直接套用 EMSSA 的「按变量类型设计算子」思路；相比直接套 NSGA-II 有明确差异化，且对含排序变量（访问顺序/路由）的赛题尤其对症。
- 数模：三目标冲突关系（时间-安全-能耗）+ Pareto 前沿 + 决策者偏好选解的完整论证链，是多目标决策类论文的标准结构模板。
- 双创申报：农田传感网 + 无人机数据回传的智慧农业方案技术亮点（少飞行、物理层安全）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Li2024_无人机群辅助IoT多目标优化虚拟天线阵列`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `li2024MultiObjectiveOptimizationUAV` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（low，仿真级、未开源、软件栈未说明）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
