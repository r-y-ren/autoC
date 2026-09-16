---
tags: [论文, 服务缓存, 用户偏好, 任务卸载, UAV-MEC]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/zhou2025UserPreferenceOriented.md
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
platforms:
  - CVX
frameworks:
  - OOA
  - greedy submodular caching
  - iterative alternating optimization
  - dependent rounding
datasets:
  - EUA dataset
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Zhou2025 用户偏好导向的UAV辅助MEC服务缓存与任务卸载

## 单行摘要
论文提出在线算法 `OOA`，在 UAV-assisted MEC 中根据用户服务偏好和历史轨迹动态更新服务缓存，并联合优化任务卸载与 UAV 位置，以最小化整体服务时延。

## 题目驱动研究框架
- 研究场景：多 UAV 辅助的移动边缘计算网络。
- 研究对象：用户服务偏好、UAV 服务缓存、任务卸载、UAV 轨迹与能量预算。
- 核心问题：静态缓存策略难以适应用户偏好随时间变化的服务需求，而忽略能量预算又会让前期低时延决策损害后续服务能力。
- 标题承诺的方法：user preference oriented service caching and task offloading。
- 期望效果：在有限能量和有限存储下持续降低总服务时延。
- 标题与正文的偏差：正文的亮点不只是用户偏好，而是把“缓存更新阈值 + 在线卸载 + 轨迹迭代”组织成完整闭环。

## Algorithm Design 快照
作者把 UAV-MEC 网络中的服务缓存与任务卸载统一成一个在线服务组织问题。首先，系统根据用户显式偏好和历史任务统计估计服务命中收益，若当前命中率低于期望阈值，则触发缓存重构。然后，在给定缓存方案下，`OOA` 通过能量加权把长期能量约束转化为单时隙优化，再交替优化 UAV 轨迹与任务卸载。这样，缓存更新不会过于频繁，而卸载决策也能随剩余能量自适应变化。

## 图1系统框架草案
- 请求层：用户按服务类型生成任务，请求分布随时间变化。
- 缓存层：UAV 存储有限，需要决定缓存哪些服务程序。
- 控制层：若命中率显著低于期望，则触发缓存更新；随后进行一轮任务卸载与轨迹迭代。
- 求解层：`GCA` 做缓存，`IAU` 做轨迹与卸载，`DR` 做整数化。
- 画图提醒：很适合画成“缓存更新门控 + 单时隙卸载优化”的在线闭环图。

## System Model
- 系统由多架 UAV 与多名用户构成，任务按服务类型生成，且不同服务有不同存储大小与计算负载。
- UAV 存储同时决定可提供的服务集合，因此服务缓存直接约束任务卸载可行域。
- UAV 总能量被通信、计算、飞行和缓存更新共同消耗，长期能量预算成为系统硬约束。
- 用户偏好由显式上传偏好和历史任务统计共同决定，因此缓存策略具有明显个性化和时变性。

## Algorithm Design 详解
- 缓存层面，论文先构造期望命中率目标，并证明其具有次模性，从而用带理论保证的贪心缓存算法 `GCA` 求解。
- 在线控制层面，作者引入能量权重因子，把长期能量约束转为每个时隙的延迟-能量加权目标。
- 对单时隙卸载问题，`IAU` 交替优化 UAV 轨迹与任务卸载，其中轨迹子问题用 `CVX` 处理，卸载子问题则先松弛再用 `dependent rounding` 恢复整数解。
- 整体算法 `OOA` 的关键不是单个子模块，而是“缓存更新触发机制 + 在线轨迹/卸载闭环”的组合。
- 对当前知识库来说，这篇论文非常适合连接 [[服务放置模型]]、[[内容缓存]] 与在线 UAV-MEC 主线。

## 实验证据卡片
- 验证类型：`simulation` + `trace_driven`
- 数据来源：`EUA dataset` 用户位置数据 + 合成服务请求与能量参数
- 平台与软件：`CVX`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文使用真实用户位置数据驱动仿真，相比纯随机布点更接近实际移动性。

## Introduction 写作素材
- 如果服务缓存不随用户偏好变化，命中率会快速下降，进而放大远端回退时延。
- UAV 早期过度追求时延最优会消耗大量飞行能量，从而损害后续服务能力。
- 因而，服务缓存更新和卸载控制需要在同一在线框架中被协调。

## Related Work 写作素材
- 既有 UAV 缓存文献多聚焦内容缓存，而本文强调服务程序缓存。
- 既有在线卸载工作往往默认服务集合固定，而本文把缓存更新也拉进在线控制环路。
- 若你后续要写“用户偏好驱动服务组织”，这篇很适合作为代表文献。

## 相关系统建模页
- [[服务放置模型]]
- [[计算卸载模型]]

## 相关概念与主题页
- [[用户偏好服务缓存]]
- [[内容缓存]]
- [[任务卸载与资源分配研究主线]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/zhou2025UserPreferenceOriented.md)
