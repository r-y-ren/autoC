---
tags: [论文, UaaS, 服务接力, 资源定价, 平台机制]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/roy2025ServHUServiceHandoff.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - introduction
validation_type:
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks:
  - optimal SSP selection
  - Lagrangian multiplier
  - KKT
  - optimal pricing
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Roy2025 Serv-HU面向UaaS的服务接力机制

## 单行摘要
论文为 `UaaS` 平台提出 `Serv-HU` 服务接力机制，在主服务提供者无法独立覆盖全部任务区域时，分两阶段完成 `SSP` 最优选择与终端定价，从而在不要求用户分别签约多个服务商的前提下完成连续服务交付。

## 题目驱动研究框架
- 研究场景：多个服务提供者共享的 `UaaS` 平台。
- 研究对象：终端用户、主服务提供者 `PSP`、次级服务提供者 `SSP`、UAV 资源与计费关系。
- 核心问题：单个服务提供者往往无法覆盖用户请求的完整区域，而让用户自行与多个提供者交互会破坏服务体验和平台一致性。
- 标题承诺的方法：service hand-off。
- 期望效果：在维持单一入口的情况下，由平台完成未覆盖区域的服务接力与价格协调。
- 标题与正文的偏差：正文的核心贡献除了 hand-off 机制，还包括一整套 PSP/SSP 协同计价框架。

## Algorithm Design 快照
论文把 `UaaS` 中的连续服务交付问题拆成两个阶段。第一阶段，`PSP` 从多个候选 `SSP` 中挑选最合适的补位提供者，以覆盖自己无法服务的子区域。第二阶段，在已确定接力关系的前提下，利用 `Lagrangian + KKT` 求解终端最优收费价格，使 `PSP` 在承担转包支出的同时仍保持利润，而终端用户的总支付又低于随机接力方案。

## 图1系统框架草案
- 用户层：终端用户只向一个 `PSP` 提交完整任务区域请求。
- 平台层：`PSP` 识别未覆盖子区域，并向候选 `SSP` 发起服务接力选择。
- 执行层：`PSP` 与被选中的 `SSP` 共同部署 UAV 完成整片区域服务。
- 经济层：平台计算 `cash outflow / inflow / service payoff`，再给出统一收费价格。
- 画图提醒：图里应把“单一用户入口”和“平台内部多提供者协作”明确分层，这是这篇论文最关键的服务计算价值。

## System Model
- `UaaS` 平台包含终端用户、服务提供者和 UAV 所有者三类主体。
- 用户只与 `PSP` 交互，若 `PSP` 覆盖不足，则由其协调 `SSP` 承担未服务区域。
- 系统把服务区域划分为多个子区域，并围绕覆盖能力、单位面积定价、服务评价与资源可用性构造 `SSP` 选择准则。
- 在定价层面，平台同时考虑 PSP 的支出、与 SSP 的结算关系以及面向终端的最优收费上界/下界。

## Algorithm Design 详解
- 阶段一为 `SSP` 选择问题：根据服务评价、可服务区域、单位面积收费和资源能力，递归地选出能够补足未覆盖区域的次级提供者集合。
- 阶段二为最优定价问题：在既定 hand-off 方案下，通过 `Lagrangian` 与 `KKT` 求出 `PSP` 的最优收费区间与最优价格。
- 论文还讨论了多 `SSP` 协同场景下的多跳通信成本，说明 hand-off 不只是业务逻辑切换，也会影响底层通信组织。
- 其研究意义在于把“服务连续性”正式写成平台机制问题，而不是假设服务能力天然充足。
- 对当前知识库而言，这篇论文把 DaaS/UaaS 主线从服务选择、组合推进到了“服务接力与收益分配”。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成平台区域划分与价格参数
- 平台与软件：未明确说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：仿真显示最优 `SSP` 选择相较随机选择可使最终收费降低约 `10.3%-12.7%`。

## Introduction 写作素材
- 无人机服务平台真正困难的不是“单个 provider 怎么最优”，而是“当 provider 覆盖不足时，平台如何保持服务连续性”。
- 如果让用户自己与多个 provider 协商，会显著拉高服务摩擦和使用成本。
- 因而，服务 hand-off 与平台定价机制是 DaaS/UaaS 成熟化的重要一步。

## Related Work 写作素材
- 既有 UaaS/DaaS 文献常聚焦服务组合和覆盖，但较少研究 provider 之间的接力与收益结算。
- 本文适合作为“平台协作机制”类工作代表，与纯任务卸载或纯轨迹优化文献形成明显对照。
- 如果要写“服务连续性、平台机制、收益分配”，这篇很适合放在 related work 的中后段。

## 相关系统建模页
- [[服务化无人机三层架构模型]]

## 相关概念与主题页
- [[服务接力（Service Hand-off）]]
- [[无人机即服务（DaaS）]]
- [[资源定价]]
- [[DaaS研究挑战与应用版图]]

## 来源
- [原文](../raw/markdown/roy2025ServHUServiceHandoff.md)
