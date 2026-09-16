---
tags: [论文, 边缘计算, 移动服务器, 路径规划, 调度]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/cong2024ParallEdgeExploitingComputingMobility.md
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
frameworks: []
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: low
---

# Cong2024 ParallEdge 计算移动并行的 5G/6G 边缘计算

## 单行摘要
论文提出 ParallEdge，用“move-while-processing”替代传统“move-then-process”，通过联合设备分配、路径规划和任务调度降低 5G/6G 边缘服务覆盖的部署成本。

## 题目驱动研究框架
- 研究场景：需要广域服务覆盖的 5G/6G 边缘计算网络。
- 研究对象：静态与移动边缘服务器、分布式 IoT 设备、周期性计算密集任务。
- 核心问题：在大规模稀疏区域中，仅靠静态边缘服务器部署成本太高，如何利用移动服务器以更少设备完成服务覆盖。
- 标题承诺的方法：exploiting computing-mobility parallelism。
- 期望效果：减少所需边缘服务器数量，并提升移动服务器资源利用率。
- 标题与正文的偏差：标题较准确，但正文最关键的范式转换是“move-while-processing”而不是单纯路径优化。

## Algorithm Design 快照
论文针对 5G/6G 边缘服务覆盖成本过高的问题，提出把移动边缘服务器的“移动”和“处理”并行化。与传统先移动到节点、再停留处理的模式不同，ParallEdge 允许服务器在完成当前节点请求收集后立即移动，并在移动过程中并行处理已收集的任务。围绕这一思想，作者将设备-服务器分配、移动路径规划和任务调度联合建模为 NP-hard 问题，再设计两阶段算法：第一阶段用 elitist genetic algorithm 求多服务器场景下的设备分配；第二阶段在单服务器场景中用 Gibbs sampling 交替优化路径和调度，从而逼近低部署成本和低总时延的解。

## 图1系统框架草案
- 系统实体：IoT 设备、静态边缘服务器、移动边缘服务器、任务请求与结果返回链路。
- 任务/数据流：移动服务器巡游访问设备点位，先收集请求，再在移动过程中处理任务，随后回访或返回结果。
- 控制/优化变量：服务器数量、设备分配、访问路径、任务处理顺序。
- 约束来源：服务器存储/算力、任务截止期、设备覆盖、移动速度。
- 画图提醒：图里要把“请求采集-移动处理中-结果返回”三段时序画清楚，否则看不出并行性来源。

## System Model
- 系统同时允许 static server 和 mobile server 共存，但核心创新在于 mobile server 的工作方式从停驻式变为并行式。
- 在 move-while-processing 范式下，一个设备点可能需要访问两次：一次上传任务，一次接收结果。
- 因而，传统 TSP 或 area partition 逻辑不能直接套用，因为边权与点权会受到计算-移动并行程度影响。
- 最终优化目标是最小化服务覆盖所需的服务器数量，并兼顾总处理时延与任务 deadline。

## Algorithm Design 详解
- 第一步是问题拆解：联合优化设备分配、服务器路径和任务调度，证明整体问题 NP-hard。
- 第二步是多服务器阶段：先用 EGA 解决设备到服务器的分配问题，构造适合该问题的染色体结构与适应度函数。
- 第三步是单服务器阶段：给定分配后，把路径与调度视为耦合子问题，通过 Gibbs sampling 交替更新。
- 第四步是任务调度策略：当服务器回访某设备时，优先调度能减少原地等待时间的任务，提高移动-计算并行收益。
- 第五步是部署决策：从理论最少服务器数出发逐步尝试，若无法满足 deadline 再增加服务器，最终确定部署规模。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`low`
- 证据备注：论文给出了结果，但实验资产链条说明有限，当前更适合支撑方法理解而不是直接复现。

## Introduction 写作素材
- 在广域 5G/6G 边缘服务中，真正昂贵的往往不是单台服务器性能，而是大规模覆盖所需的部署数量。
- 当处理时延与移动时延可比时，“先移动后处理”会浪费大量可并行时间。
- 因而，移动边缘服务器的关键不是“会不会移动”，而是“移动能否与处理并行”。
- 这篇论文非常适合作为你后续研究移动边缘基础设施时的背景引文。

## Related Work 写作素材
- 与纯静态边缘部署相比，本文强调移动服务器减少部署数量。
- 与传统移动服务器框架相比，本文的核心差异是 move-while-processing，而不是 move-then-process。
- 与只做路径规划或只做调度的工作相比，本文把设备分配、路径和调度耦合起来统一求解。
- 相关工作写作时，可把它放在“mobile edge server deployment”路线，而不是传统 UAV-MEC 卸载路线。

## 相关系统建模页
- 无

## 相关概念与主题页
- [[计算-移动并行]]
- [[资源分配]]

## 来源
- [原文](../raw/markdown/cong2024ParallEdgeExploitingComputingMobility.md)
