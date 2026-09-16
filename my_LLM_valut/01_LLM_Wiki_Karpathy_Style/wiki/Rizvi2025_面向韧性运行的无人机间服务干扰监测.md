---
tags: [论文, DaaS, 韧性, 服务干扰, 无人机配送]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/rizvi2025MonitoringInterdroneService.md
venue_tier: CCF-A
literature_type: system
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - related_work
  - system_model
validation_type:
  - trace_driven
data_origin:
  - public_dataset
platforms: []
frameworks:
  - spatio-temporal proximity analysis
  - heuristic detection
  - Percentage Impact Score
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Rizvi2025 面向韧性运行的无人机间服务干扰监测

## 单行摘要
论文从服务韧性视角研究 skyway 网络中的无人机间干扰，提出节点级/航段级干扰 taxonomy、基于时空邻近性的启发式检测算法和 `PIS` 严重度评估，用于主动发现会破坏配送效率的近距飞行干扰事件。

## 题目驱动研究框架
- 研究场景：多服务提供方共享 skyway 网络执行无人机配送。
- 研究对象：服务提供者、服务消费者、super-provider、skyway nodes/segments、配送 UAV。
- 核心问题：现有 DaaS 组合和 UTM 冲突检测多关注“是否会撞”，但忽略了大量不会碰撞、却会显著恶化能耗和交付时间的干扰事件。
- 标题承诺的方法：monitoring inter-drone service interference。
- 期望效果：提前发现干扰并评估其严重度，为后续改航、限流和充电调度提供依据。
- 标题与正文的偏差：正文真正贡献不只在“监测”，而在于把干扰正式写进服务系统的 QoS 语义里。

## Algorithm Design 快照
作者首先把服务型无人机配送中的干扰分为节点级和航段级两类：前者体现在充电桩拥塞、后者体现在共享航段中的时空近距飞行。本文聚焦航段级负干扰，使用无人机轨迹与运行时序构造时空重叠判据，再用启发式方法快速识别潜在干扰事件。进一步地，论文用 `Percentage Impact Score (PIS)` 定量评估干扰对能耗和交付时长的影响，避免把所有近距事件一视同仁。

## 图1系统框架草案
- 参与方：服务提供者、消费者、super-provider。
- 运行载体：由 rooftop nodes 与 skyway segments 构成的 skyway network。
- 监测层：收集各 provider 申报的飞行计划、航段、时序和充电需求。
- 分析层：`segment overlap detection -> interference taxonomy -> PIS severity assessment`。
- 处置层：为改航、延迟放行、重分配充电资源等韧性控制提供依据。

## System Model
- 将无人机配送明确建模为服务系统，功能属性对应包裹在 skyway 节点间的交付，非功能属性包括能耗、成本和交付时间。
- skyway network 由节点与 LoS 航段构成，节点既可能是配送点，也可能是中继充电点。
- 干扰 taxonomy 分为节点级干扰与航段级干扰，其中后者由同一航段中的时空重叠引起，会通过气动作用改变实际能耗。
- 系统中的 super-provider 拥有全局航迹视图，因此能在服务执行前进行干扰监测与严重度分析。

## Algorithm Design 详解
- 论文先给出服务型配送环境下的干扰 taxonomy，明确哪些事件属于“影响安全的冲突”，哪些属于“影响效率的干扰”。
- 然后聚焦负航段级干扰，基于无人机在三维空间中的时间重叠、垂直间距和相对位置关系构造启发式检测规则。
- 在识别出疑似干扰后，再通过 `PIS` 衡量其对电池消耗、额外充电时间和到达时刻的影响。
- 文章的重要启发是：韧性运行不只是在故障发生后恢复，而是要先把会传播成节点拥塞和服务延误的微弱干扰提前识别出来。
- 这使得 DaaS 主线从“服务选择与组合”自然延伸到“服务运行监测与韧性保障”。

## 实验证据卡片
- 验证类型：`trace_driven`
- 数据来源：真实配送/skyway 数据集
- 平台与软件：未明确说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文使用真实世界数据做干扰检测评估，检测准确率约 `95%`，并显著快于穷举和 `K-means` 基线。

## Introduction 写作素材
- 未来高密度无人机配送的关键问题不再只是能否飞通，而是能否在共享航路中持续保持服务韧性。
- 近距飞行带来的气动干扰可能不会直接导致碰撞，却会通过额外能耗与充电排队破坏时效性。
- 因此，DaaS 不仅需要服务选择与组合，还需要运行中的干扰监测与严重度评估。

## Related Work 写作素材
- UTM 文献更关注 collision/conflict detection，而本文强调效率损害型 interference。
- DaaS 组合文献多假设飞行平稳无干扰，本文指出这在高密度 skyway 网络里不现实。
- 若你后续要写“服务韧性”或“无人机配送运行监测”，这篇很适合作为开口文献。

## 相关系统建模页
- [[服务化无人机三层架构模型]]

## 相关概念与主题页
- [[服务干扰监测]]
- [[无人机即服务（DaaS）]]
- [[DaaS研究挑战与应用版图]]
- [[安全与服务保障]]

## 来源
- [原文](../raw/markdown/rizvi2025MonitoringInterdroneService.md)
