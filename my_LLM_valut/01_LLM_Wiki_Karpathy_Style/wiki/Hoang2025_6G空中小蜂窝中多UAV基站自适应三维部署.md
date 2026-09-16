---
tags: [论文, UAV-BS, 三维部署, QoE, Lyapunov优化]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/hoang2025Adaptive3DPlacementa.md
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
reproducibility_level: medium
---

# Hoang2025 6G 空中小蜂窝中多 UAV 基站自适应三维部署

## 单行摘要
论文在动态 6G 空中小蜂窝中联合动态聚类与 actor-critic 部署控制，在队列稳定约束下最大化用户长期 MOS。

## 题目驱动研究框架
- 研究场景：多个 UAV-BS 为移动用户和异构流量需求提供 6G 空中小蜂窝服务。
- 研究对象：移动用户、下载队列、多个 UAV-BS、用户流量热力图。
- 核心问题：在用户位置与需求持续变化时，如何动态调整多 UAV-BS 的三维位置。
- 标题承诺的方法：adaptive 3D placement with DRL。
- 期望效果：在保持队列稳定的前提下提升长期 MOS。
- 标题与正文的偏差：正文的关键贡献不只是 DRL，而是“动态聚类 + Lyapunov 引导 critic + 热力图状态编码”。

## Algorithm Design 快照
论文考虑动态网络中的多 UAV-BS 部署问题，用户位置与业务流量随时间变化，未完成下载会在 UAV-BS 队列中形成 backlog。为此，作者先用 K-means 动态聚类将用户分配到不同 UAV-BS，再利用 actor-critic DRL 调整 UAV-BS 的三维位置。与普通 DRL 不同，critic 模块并不完全依赖另一个神经网络，而是使用 Lyapunov drift-minus-reward 作为标签引导，从而在队列稳定约束下最大化长期 MOS。

## 图1系统框架草案
- 系统实体：多个 UAV-BS、移动用户、下载队列与业务热力图。
- 任务/数据流：用户持续产生流量，未完成下载在 UAV-BS 队列中积累。
- 控制/优化变量：用户聚类、UAV-BS 的 3D 位置、移动速度方向。
- 约束来源：队列稳定、UAV 最大速度、长期平均推进功率、用户时变流量。
- 画图提醒：图里应突出“动态聚类 -> 热力图编码 -> Lyapunov 引导部署决策”。

## System Model
- 系统核心是 traffic-aware 的动态 3D placement，而不是静态覆盖。
- 用户侧 backlog 队列直接反映瞬时业务压力，因此服务质量与队列稳定强耦合。
- MOS 被用作长期体验指标，说明部署问题已经从几何覆盖推进到用户感知满意度。
- UAV-BS 移动决策既受当前流量热区影响，也受长期能耗与稳定性约束影响。

## Algorithm Design 详解
- 第一步通过 K-means 对移动用户进行动态聚类。
- 第二步生成用户流量热力图并与 UAV 状态拼接形成 actor 输入。
- 第三步由 DNN actor 产生候选移动决策，再由 Lyapunov-guided critic 选择最优动作。
- 第四步周期性重训练策略网络，使部署策略持续适应时变网络。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文适合作为“QoE 驱动的多 UAV-BS 三维部署”方向的代表页。

## Introduction 写作素材
- 在动态空中小蜂窝里，静态最优部署很快会被移动用户和异构流量打破。
- 如果只优化覆盖率或平均速率，很难刻画真实用户体验与排队压力。
- 这篇论文适合支撑“部署问题正在从几何设计走向体验驱动在线控制”的论断。

## Related Work 写作素材
- 与静态 UAV-BS 部署工作不同，本文面向动态用户与异构流量。
- 与只做 rate maximization 的部署方法不同，本文显式最大化 MOS。
- 与纯 actor-critic 方法不同，本文用 Lyapunov 指导 critic 评价。

## 相关系统建模页
- [[区域覆盖与部署模型]]
- [[任务队列与时延保障模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[服务质量体验（QoE）]]
- [[三维区域覆盖]]
- [[无人机部署优化]]
- [[覆盖与部署优化主线]]

## 来源
- [原文](../raw/markdown/hoang2025Adaptive3DPlacementa.md)
