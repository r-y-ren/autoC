---
tags: [论文, 激光供能, 可再生能源, UAV通信, 绿色网络]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/panahi2024ReliableEnergyEfficientUAV.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: supporting
use_for:
  - methodology
  - system_model
  - related_work
validation_type:
  - simulation
data_origin:
  - synthetic
platforms:
  - MATLAB
  - YALMIP
frameworks:
  - cost-aware energy procurement
  - UAV placement
  - wireless power transfer
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Panahi2024 激光与可再生能源协同供能的UAV通信成本优化

## 单行摘要
论文面向通信型 UAV 的长航时问题，联合优化激光波束、机载电池和本地可再生能源的能量采购量，并进一步给出兼顾链路质量与能量成本的 UAV 放置策略。

## 题目驱动研究框架
- 研究场景：激光供能与本地可再生能源共同支撑的 UAV 通信系统。
- 研究对象：通信 UAV、激光发射器 `LBD`、地面用户、低功耗地面设备和可再生能源来源。
- 核心问题：既有 UAV 通信研究多关注能耗最小化，却较少关心“能源从哪里买、买多少、成本如何计”。
- 标题承诺的方法：reliable and energy-efficient UAV communications from a cost-aware perspective。
- 期望效果：在保障通信链路质量的同时，降低 UAV 整个运行周期的能源采购成本。
- 标题与正文的偏差：正文的关键亮点不是传统 EE，而是显式引入能源采购成本和多源供能结构。

## Algorithm Design 快照
论文把 UAV 的供能系统拆成三部分：机载电池、地面激光束和本地可再生能源。作者先在给定时间周期内优化每个时段从电池和激光链路获取多少能量，以最小化总体采购成本；随后再根据供能结果设计 UAV 的成本感知放置位置，使 UAV 同时获得更好的通信链路和能量接收条件。若可再生能源有剩余，还允许通过 `WPT` 向低功耗地面设备售能，形成一定的成本抵消机制。

## 图1系统框架草案
- 空中实体：具通信服务能力的 UAV。
- 地面实体：`LBD`、GBS、用户设备、低功耗 IoT 设备。
- 能量流：激光供能、机载电池释放、可再生能源注入、向 GD 的反向 WPT。
- 决策变量：分时能量采购量、UAV 放置位置。
- 画图提醒：把通信链路和能量链路并行画出，会更突出“通信质量-能量成本”双目标结构。

## System Model
- UAV 在运行周期内可从激光发射器和机载电池获得能量，而电池又由本地可再生能源补充。
- 系统允许在可再生能源富余时，把一部分能量通过 WPT 转给地面低功耗设备。
- 通信链路质量依赖 UAV 放置位置，能量获取又依赖与 LBD 的空间关系。
- 目标函数是总能源采购成本，而不是单纯的推进或通信功耗。

## Algorithm Design 详解
- 首先建立时间分段的能量采购优化问题，决定各时段从不同能源源头获取的量。
- 再通过成本感知的 UAV 放置策略，同时兼顾通信覆盖与激光供能成功率。
- 额外把多余可再生能源卖给地面设备，形成“供能-通信-收益”联动。
- 这篇论文很适合支撑你后续写“硬件供能现实如何回过头塑造空中系统设计”的段落。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成参数场景
- 平台与软件：`MATLAB`、`YALMIP`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：系统模型和优化流程清晰，但仍停留在仿真验证层。

## Introduction 写作素材
- 仅讨论 UAV 的平均能耗还不够，真实系统还要回答“能源采购成本由谁承担、如何分时优化”。
- 激光供能和可再生能源让 UAV 通信从单一能耗问题变成多源能量管理问题。
- 因此，未来的 UAV 通信研究应更多关注“能量流 + 业务流”的共同设计。

## Related Work 写作素材
- 既有能效文献通常优化能量使用，而很少优化能量采购与售能。
- 既有激光供能工作多关注延长飞行时长，较少与通信放置协同建模。
- 该文是“供能成本进入 UAV 通信主问题”的代表例子。

## 相关系统建模页
- [[无人机能耗模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[激光供能]]
- [[无线供能移动边缘计算]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/panahi2024ReliableEnergyEfficientUAV.md)
