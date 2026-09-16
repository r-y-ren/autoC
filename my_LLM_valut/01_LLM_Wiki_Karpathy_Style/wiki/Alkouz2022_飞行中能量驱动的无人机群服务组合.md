---
tags: [论文, DaaS, 服务组合, 多无人机协同, 能量共享]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/alkouz2022InflightEnergydrivenComposition.md
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
  - trace_driven
data_origin:
  - mixed
platforms: []
frameworks: []
datasets:
  - London urban road network dataset
hardware_stack:
  - DJI Phantom 3
  - CrazyFlie 2.1
artifact_availability: partial
reproducibility_level: medium
---

# Alkouz2022 飞行中能量驱动的无人机群服务组合

## 单行摘要
论文把多包裹群体配送建模为 swarm-based drone service，并引入 support drone 的飞行中能量共享，把群体交付与 Energy-as-a-Service 组成双层服务组合问题，以缩短配送时间。

## 题目驱动研究框架
- 研究场景：城市 skyway 网络中的多包裹无人机群配送。
- 研究对象：配送无人机、支持充电无人机、屋顶节点、充电垫、风场与编队。
- 核心问题：在电池受限、风场扰动、充电垫有限和同步到达要求下，如何通过飞行中充电提升群体配送效率。
- 标题承诺的方法：energy-driven composition of drone swarm services。
- 期望效果：减少中途停靠和地面充电等待时间，提高群体配送成功率与时效性。
- 标题与正文的偏差：标题强调 energy-driven composition，但正文真正新意是把 swarm delivery service 和 Energy-as-a-Service 做成嵌套两层组合。

## Algorithm Design 快照
论文针对城市空中走廊中的多无人机群体配送，研究在电池容量、风条件、编队位置差异和有限充电垫约束下，如何通过飞行中的能量共享减少中途停靠。作者将配送服务抽象为 swarm-based drone service，将支援无人机的能量共享抽象为 Energy-as-a-Service，并建立双层服务组合框架。具体流程是先选择编队形态与 support drone 数量，再决定 support drone 在编队中的位置，随后通过 priority-based 或 fairness-based 能量共享策略以及 re-ordering 机制，在每段航程内决定充电对象与充电时长，最后用增强 A* 搜索全局最短配送时间路径。

## 图1系统框架草案
- 系统实体：配送无人机群、support drone、skyway 节点、屋顶充电站、服务注册与调度系统。
- 任务/数据流：用户提交多包裹同步配送请求后，系统先选择编队和 support drone，再在路径搜索过程中嵌套能量共享服务组合。
- 控制/优化变量：编队类型、support drone 数量与位置、能量共享对象、共享时长、群体重排顺序、路径选择。
- 约束来源：载重、电池容量、风速风向、充电垫数量、必须同时到达的时间窗。
- 画图提醒：图里最好把“外层配送服务组合”和“内层能量共享组合”分开画，否则很难体现双层服务结构。

## System Model
- 论文采用 skyway network，节点表示可停靠屋顶，边表示群体可飞行的航段，每个节点可能同时具有目的地和充电站属性。
- 群体被视为静态 swarm，默认成员数固定并保持空间一致性，但为了完成能量共享可以进行局部 re-ordering。
- 配送服务的功能属性是多包裹群体送达，QoS 则体现为总配送时间、充电时间和等待时间；Energy-as-a-Service 的 QoS 则体现为可共享能量、位置及时窗。
- 作者显式区分 intrinsic constraints（载重、电池）和 extrinsic constraints（风、充电垫、时间窗），这非常适合写系统模型时的约束分类。

## Algorithm Design 详解
- 第一步是服务抽象：把 swarm delivery 抽象为 SDS，把 support drone 的供能行为抽象为 EaaS，从而把能量问题纳入服务组合语义。
- 第二步是预组合：先选编队，再根据冗余理论与失败概率估计最优 support drone 数量，并讨论其在编队中的位置。
- 第三步是能量共享策略：作者设计 priority-based 与 fairness-based 两种能量分配方法，处理谁先被充、充多久的问题。
- 第四步是群体重排：由于 support drone 只能近距离给相邻无人机充电，论文进一步研究了 re-ordering 对编队能耗和共享可行性的影响。
- 第五步是全局路径组合：在每段航程的局部能量共享决策之上，用 enhanced A* 搜索全局最优配送路径，目标是最小化总配送时间。

## 实验证据卡片
- 验证类型：数值仿真；真实数据驱动仿真
- 数据来源：混合来源；涉及数据集：`London urban road network dataset`
- 平台与软件：未说明
- 硬件与算力：`DJI Phantom 3`；`CrazyFlie 2.1`
- 开源情况：部分资产公开
- 复现判断：`medium`
- 证据备注：论文使用真实数据或真实轨迹驱动仿真，但这仍不等同于实际部署或实飞验证。

## Introduction 写作素材
- 多无人机群配送的瓶颈不只在“路怎么走”，还在“什么时候不得不停下来充电”。
- 如果只依赖固定充电站，群体同步约束会放大等待时间，从而显著拉长总配送时延。
- 因而，把能量共享上升为服务能力，而不是把它当成背景假设，是一种很有启发性的系统设计思路。
- 这篇论文很适合支撑“服务组合视角可以重写无人机群配送问题”的引言论证。

## Related Work 写作素材
- 与单无人机路径规划不同，本文处理的是群体服务与同步到达问题。
- 与只考虑路径或充电站布局的工作相比，本文把 support drone 与 EaaS 显式纳入服务组合。
- 与传统 swarm formation 工作相比，本文不只研究节能编队，还研究为了共享能量而进行的编队重排。
- 在 DaaS 相关综述写作里，这篇论文非常适合作为“selection and composition + energy sharing”的代表作。

## 相关系统建模页
- [[无人机能耗模型]]
- [[服务化无人机三层架构模型]]

## 相关概念与主题页
- [[无人机即服务（DaaS）]]
- [[多无人机协同]]
- [[DaaS研究挑战与应用版图]]

## 来源
- [原文](../raw/markdown/alkouz2022InflightEnergydrivenComposition.md)
