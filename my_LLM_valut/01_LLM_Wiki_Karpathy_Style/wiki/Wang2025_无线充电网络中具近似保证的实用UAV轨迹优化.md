---
tags: [论文, 轨迹优化, 无线充电, 障碍规避, 近似算法]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/wang2025PracticalOptimizingUAV.md
  - ../raw/markdown/Wang-2025-Practical Optimizing UAV Trajectory.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - system_model
validation_type:
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks:
  - OWGGA
  - ACSA
  - Christofides algorithm
  - submodular optimization
datasets: []
hardware_stack:
  - Intel i7 2.10 GHz CPU
  - 32 GB RAM
artifact_availability: unknown
reproducibility_level: medium
---

# Wang2025 无线充电网络中具近似保证的实用UAV轨迹优化

## 单行摘要
论文在含障碍的无线充电网络中联合处理候选悬停点访问顺序与充电站选择，通过 OWGGA 与 ACSA 构造具近似保证的实用 UAV 闭环轨迹。

## 题目驱动研究框架
- 研究场景：含障碍物、含无线充电站的数据采集与持续飞行网络。
- 研究对象：单架 UAV、服务悬停点、充电站、障碍物集合。
- 核心问题：如何在保证能量可持续的前提下，用一条闭合且可飞行的路径覆盖全部服务点，并尽量缩短总距离与任务完成时间。
- 标题承诺的方法：practical optimizing UAV trajectory in wireless charging networks。
- 期望效果：比启发式路径规划更稳定地降低飞行距离与完成时间，同时保留可解释的性能界。
- 标题与正文的偏差：正文真正亮点不只是“practical”，而是把障碍规避、充电站选取和近似比分析整合到同一条轨迹求解链路中。

## Algorithm Design 快照
论文研究无线充电网络中的 UAV 轨迹优化问题。UAV 需要从基地出发，访问所有服务悬停点、必要时插入若干充电站，并在障碍环境中返回起点。难点在于可飞行路径要同时满足障碍规避、TSP 式访问顺序优化和能量续航约束。为此，作者先用 OWGGA 为任意两点生成带障碍规避的加权边，再把这些边送入 Christofides 近似框架形成候选巡回，随后通过 ACSA 以边际收益最大原则逐步加入充电站，从而在总任务时间、总路径长度和补能需求之间取得平衡。

## 图1系统框架草案
- 系统实体：基地、服务悬停点、无线充电站、圆柱近似障碍物、单架 UAV。
- 任务/数据流：UAV 访问服务点采集数据；当剩余电量不足时转入充电站补能；最终回到基地。
- 控制/优化变量：访问顺序、候选绕障路径、被选中的充电站集合。
- 约束来源：电池容量、飞行高度、障碍规避、必须访问全部服务点、闭环轨迹约束。
- 画图提醒：图中要突出“服务点 + 充电点 + 障碍物”三种节点，以及绕障边与最终闭环路径的区别。

## System Model
- 所有基地、服务点和充电点共同构成 UAV 的候选悬停点集合。
- 障碍物通过外接圆柱近似，使任意两悬停点之间的直连路径可能不可行。
- 目标函数综合考虑任务完成时间和纳入路径的充电站数量，本质上是在“更短路径”和“更少补能”之间做收益最大化。
- UAV 飞行能耗由推进功率、飞行距离、起降加减速与充电过程共同决定。

## Algorithm Design 详解
- OWGGA：针对两点间存在障碍阻挡的情况，利用切线与圆弧构造绕障路径，并给出路径长度界。
- Christofides 融合：将 OWGGA 得到的加权边输入到 TSP 近似求解中，得到覆盖所有服务点的候选闭环路线。
- ACSA：在满足电量约束的前提下，按边际收益逐步选择应插入哪些充电站，避免把充电看成固定静态配置。
- 理论性质：论文同时给出 `1 - 1/e` 的近似比和总路径长度至多 `3π/4` 倍最优解的界。
- 实验结果：平均可将飞行距离降低 `38.01%`、任务完成时间降低 `34.00%`。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成障碍环境与随机网络拓扑
- 平台与软件：未说明
- 硬件与算力：`Intel i7 2.10 GHz CPU`、`32 GB RAM`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文公开了机器配置、默认场景参数以及 50 次随机拓扑平均方式，但未披露代码实现。

## Introduction 写作素材
- 若把无线充电只当静态补能条件，轨迹规划很难真正服务持续作业场景。
- 真实场景中的障碍规避和补能路径选择会改变“最优轨迹”的定义，而不仅是附加约束。
- 这篇论文适合支撑“持续飞行 UAV 系统需要从几何路径规划走向补能感知轨迹规划”的引言判断。

## Related Work 写作素材
- 与传统能量约束轨迹优化相比，本文显式把充电站选择纳入轨迹本体。
- 与纯启发式路径规划相比，本文强调近似界和可解释性能保证。
- 与仅考虑开阔环境的无线供能路径研究相比，本文把障碍规避单独做成可复用的图构建层。

## 相关系统建模页
- [[无人机能耗模型]]
- [[区域覆盖与部署模型]]

## 相关概念与主题页
- [[无线充电网络（WCN）]]
- [[轨迹优化]]
- [[覆盖与部署优化主线]]
- [[轨迹优化与协同控制]]
- [[UAC研究路线图]]

## 来源
- [原文1](../raw/markdown/wang2025PracticalOptimizingUAV.md)
- [原文2](../raw/markdown/Wang-2025-Practical%20Optimizing%20UAV%20Trajectory.md)
