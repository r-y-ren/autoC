---
tags: [论文, 数字孪生, 毫米波, V2X, 路由]
created: 2026-04-10
updated: 2026-04-10
sources:
  - ../raw/markdown/zhou2025DigitalTwinEmpowered.md
venue_tier: CCF-A
literature_type: system
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - system_model
  - methodology
validation_type:
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks:
  - digital twin network
  - reinforcement learning
  - mmWave routing
hardware_stack: []
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Zhou2025_数字孪生赋能的UAV辅助毫米波多跳V2X路由

## 单行摘要
论文面向城市高密度 VANET 场景提出数字孪生赋能的毫米波多跳 V2X 路由方案，以街道/路口/Core 三层 DT 网络协同 UAV 交叉口转发和强化学习街道选择，提高分组投递率并降低时延。

## 题目驱动研究框架
- 研究场景：城市道路中的 mmWave 多跳 V2X 通信。
- 研究对象：车辆、街道/路口数字孪生、交叉口 UAV 中继和核心 DT。
- 核心问题：毫米波链路在城市环境中易受遮挡和动态拓扑影响，传统车联网路由难稳定兼顾投递率与时延。
- 标题承诺的方法：digital twin empowered routing with UAV assistance。
- 期望效果：通过 DT 全局信息和 UAV 路口中继提升城市 mmWave 多跳转发性能。
- 标题与正文的偏差：标题突出 DT 赋能，正文的真正系统亮点在于“三层 DTN + UAV 路口转发 + RL 街道选择”的联合设计。

## Algorithm Design 快照
论文把城市路网中的每条街道和交叉口映射成数字孪生子体，并由核心 DT 组织跨层同步。街道内部的 relay 选择与波束宽度配置由 street sub-DT 协助完成，而跨街道转发则由部署在路口的 UAV 中继负责，交由 intersection sub-DT 中的 RL 代理进行街道选择决策。这样，DT 的全局交通流信息和 UAV 的机动中继能力被统一到了同一个多跳路由框架里。

## 图1系统框架草案
- 物理层：车辆、城市街道、路口 UAV。
- 虚拟层：street sub-DT、intersection sub-DT、Core DT。
- 决策层：街道内 relay 选择 + 交叉口 RL 街道选择。
- 链路层：mmWave 数据传输与波束宽度配置。
- 指标层：packet delivery rate、delay、average hops。

## System Model
- 城市道路被分解成街道与路口两个层级的子数字孪生，并由核心 DT 统一管理。
- 街道内节点通过毫米波链路做多跳中继，路口则由 UAV 辅助完成跨街道转发。
- 路由决策同时考虑车辆密度、网络负载、链路质量和传输距离。
- RL 代理部署在 intersection sub-DT，而非 UAV 本体，以减轻机载资源消耗。

## Algorithm Design 详解
- 第一步：构建分层数字孪生网络 `DTN`，组织街道、路口与核心层的数据同步。
- 第二步：在街道内部按候选转发节点负载、链路质量和距离做下一跳选择，并调节波束宽度。
- 第三步：在交叉口部署 UAV 中继，并利用 RL 决定应把数据转发到哪条街道。
- 第四步：结合车辆密度和网络负载设计更稳健的街道选择策略，减少拥塞与时延。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成城市 VANET 场景
- 平台与软件：未明确说明
- 方法组件：`digital twin network`、`reinforcement learning`、`mmWave routing`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未明确披露统一仿真平台与代码开放情况

## Introduction 写作素材
- 城市 mmWave 车联网的挑战并不只在波束对齐，而在动态拓扑下如何获得足够全局的街道级路由视图。
- 数字孪生为车联网提供了一种把全局交通信息和局部链路决策统一起来的可能。
- 这篇论文适合支撑“UAV 与数字孪生正在共同重塑路由控制层”的写作逻辑。

## Related Work 写作素材
- 与传统车联网路由工作相比，本文更强调街道级数字孪生建模与 UAV 路口辅助。
- 与只使用 RSU 的中心控制方案相比，本文更突出 UAV 的快速部署与 LoS 优势。
- 与一般 DT 驱动 VEC 工作相比，本文聚焦于 mmWave 多跳 V2X 路由。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[数字孪生元宇宙]]
- [[空中通信与协同传输]]
- [[空天地一体网络（SAGIN）]]

## 来源
- [原文](../raw/markdown/zhou2025DigitalTwinEmpowered.md)
