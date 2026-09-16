---
tags: [论文, MEC, 服务选择, 无人机配送, 智慧物流]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/xu2024HolisticHybridService.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - related_work
validation_type:
  - simulation
  - trace_driven
data_origin:
  - mixed
platforms:
  - Antwork ADNET
frameworks:
  - H2S2
  - static service selection
  - dynamic re-selection
datasets:
  - Antwork ADNET scenario
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Xu2024 MEC无人机末端配送的整体混合服务选择

## 单行摘要
论文面向真实 UAV 末端配送场景提出 `H2S2` 整体混合服务选择策略，将配送服务选择与计算服务选择统一起来，并同时覆盖静态选择与动态重选，以降低 UAV 能耗和服务响应时间。

## 题目驱动研究框架
- 研究场景：`MEC-based UAV last-mile delivery` 智慧物流系统。
- 研究对象：配送服务、计算服务、UAV 末端配送路径、边缘计算节点、动态网络环境。
- 核心问题：现有工作往往分开优化 delivery service 与 computational service，也很少同时考虑静态选择与运行时重选。
- 标题承诺的方法：holistic and hybrid service selection。
- 期望效果：在真实物流场景中同时提升交付效率与边缘服务响应能力。
- 标题与正文的偏差：正文真正的贡献点是把“多类服务 + 多阶段决策”合在一个完整物流流程里。

## Algorithm Design 快照
作者将末端配送系统中的服务划分为两类：一类是负责包裹移动的 delivery services，另一类是由 MEC 环境提供的 computational services。`H2S2` 的核心不是单次挑一个最优服务，而是构造一套贯穿整个配送流程的选择机制：静态阶段先给出整体最优服务计划，动态阶段在服务可用性、网络条件或设备移动性变化时触发重选。这样，配送与计算不再各自独立，而是共同决定 UAV 能耗与系统响应时延。

## 图1系统框架草案
- 物流层：订单、配送站点、UAV 路径与配送服务实例。
- 计算层：边缘节点提供计算服务实例，用于任务处理和系统协同。
- 决策层：静态服务选择 + 动态服务重选。
- 优化目标：同时压低 UAV 送货能耗与计算服务响应时间。
- 画图提醒：把 delivery 与 computation 两条服务链并行画出来，再用 `H2S2` 在上层把两者联结，会非常贴近论文主旨。

## System Model
- 系统显式区分 delivery service model 与 computational service model，两者共同决定用户体验。
- UAV 飞行路径依赖真实配送站点网络，服务实例受位置、时间和可用性约束。
- 运行环境考虑服务多样性、服务可得性与设备移动性，因此重选机制不是附加模块，而是系统主干。
- 论文从服务消费者视角建模，把 UAV 配送企业视为真正做选择的主体。

## Algorithm Design 详解
- 先建立服务选择框架，统一组织配送服务与计算服务两类对象。
- 然后设计 `H2S2`，将静态阶段的全局最优服务选择与动态阶段的重选联动起来。
- 与只做 delivery 或只做 computation 的方法不同，`H2S2` 明确把多阶段物流过程看作一个连续服务系统。
- 论文基于 `Antwork ADNET` 的真实 UAV 航路数据抽象出仿真数据集，因此系统模型与一般纯合成场景相比更接近真实物流部署。
- 对知识库而言，这篇论文非常适合支撑“从服务放置/缓存走向 service selection”这条主线。

## 实验证据卡片
- 验证类型：`simulation` + `trace_driven`
- 数据来源：真实 `ADNET` 航路数据抽象出的仿真场景
- 平台与软件：`Antwork ADNET`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文在真实末端配送场景基础上评估，报告了交付效率提升与 UAV 能耗下降。

## Introduction 写作素材
- 在智能物流里，配送服务与计算服务是耦合存在的，分开优化会损失整体最优。
- 服务选择不应只看静态最优，还要看运行过程中能否根据可用性变化及时重选。
- 因此，MEC-based UAV delivery 更像服务系统问题，而不只是路径或调度问题。

## Related Work 写作素材
- 既有工作要么做云/MEC 服务选择，要么做无人机配送服务选择，很少把两者统一。
- 既有动态服务重选文献也常不覆盖完整配送流程。
- 这篇论文是“整体视角服务选择”分支的代表页。

## 相关系统建模页
- [[服务放置模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[整体混合服务选择]]
- [[无人机即服务（DaaS）]]
- [[DaaS研究挑战与应用版图]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [原文](../raw/markdown/xu2024HolisticHybridService.md)
