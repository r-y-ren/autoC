---
id: wu2024MultiUAVsNetworkDesign
name: 多UAV计算网络联合设计（VNF+流路由）
field: [多 UAV 网络, 网络功能虚拟化, 混合整数规划]
published: 2024-01-01
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
    edge: UAV 选址+VNF 部署+流路由的 max-min 公平联合优化是设施选址/网络流题型的高配版，S-MILP/NS-MILP 精确建模与 RALS/RAPLS 启发式压求解时间的组合可直接复用为解法骨架
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 可分流/不可分流两种 MILP 模型 + 资源感知位置/路径选择启发式，适用于网络设计类赛题且 max-min 目标自带公平性论证
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 空中算力网络叙事的技术支撑点（UAV 从覆盖平台升级为可编排 VNF 计算基础设施）
    reuse_cost: 低
sources:
  - paper_title: "Multi-UAVs Network Design Algorithms for Computed Rate Maximization"
    doi: 10.1109/TMC.2024.3355391
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 多UAV计算网络联合设计（VNF+流路由）

## 单行摘要

把多 UAV 空中骨干网当作可编排的计算基础设施来设计：地面源宿节点对的业务流须在到达目的地前经所需 VNF（虚拟网络功能）处理，论文联合决定 UAV 位置、VNF 部署与处理前/处理后流的路由，目标是最大化所有源宿对中最小的已计算流率（max-min 公平）。给出可分流（S-MILP）与不可分流（NS-MILP）两个精确模型及理论上界，并提出 RALS/RAPLS 启发式避免穷举全部拓扑组合、以小得多的求解时间拿到高质量近似解。

## 方法快照

- 问题结构：选址（UAV 位置）× 功能放置（VNF 实例指派）× 路由（未处理/已处理流、链路容量共享）三层耦合。
- 流模型：可分流允许业务拆多路径，不可分流要求单路径完成传输与处理，分别对应 S-MILP / NS-MILP。
- 目标：max-min computed flow——不以总吞吐为目标而以最差源宿对流率衡量网络公平性。
- 启发式：RALS / RAPLS 通过资源感知的位置与路径选择在压缩的候选空间内找近似解。
- 验证：仿真（合成源宿对与候选拓扑），对比精确求解与启发式近似（未开源）。

## 比赛映射要点

- 数模优化题：任何"选多少个设施、放在哪、容量怎么切、流量怎么走"的联合题（充电站/仓储/算力节点布局）都可套用此建模套路——max-min 目标天然回应"公平性/最差服务保障"类设问；"精确 MILP 给界 + 启发式给可行解"的双轨写法是标准的论文式论证结构。
- 黑客松/算法赛：带处理顺序约束（先经 VNF 再到宿）的网络流是一般最短路/最大流题目的强化变体。
- 双创申报：空中算力网、低空基础设施类项目书的技术支撑点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wu2024_面向计算流最大化的多UAV网络设计`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `wu2024MultiUAVsNetworkDesign` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、未开源）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
