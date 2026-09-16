---
tags: [论文, 分布式导航, 联邦强化学习, 异构UAV, MEC]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/wang2024DecentralizedNavigationHeterogeneous.md
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
data_origin:
  - synthetic
platforms: []
frameworks:
  - SHDRLN
  - DFRL
  - federated reinforcement learning
  - maximum entropy learning
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Wang2024 异构联邦强化学习的UAV-MEC分布式导航

## 单行摘要
论文面向异构 UAV-enabled MEC 的分布式导航问题，提出 SHDRLN 与 DFRL，在不依赖集中式全局观测的前提下提升整体能效与知识共享稳定性。

## 题目驱动研究框架
- 研究场景：具有移动用户和异构 UAV 的 UAV-enabled MEC 网络。
- 研究对象：多架性能不同的 UAV、移动用户、云端聚合服务器。
- 核心问题：在各 UAV 飞行能力、覆盖半径和计算资源不同的条件下，如何学习可共享但又可个性化的导航策略。
- 标题承诺的方法：decentralized navigation with heterogeneous federated reinforcement learning.
- 期望效果：在提升任务卸载能效的同时，让异构 UAV 能共享知识而不过度同质化。
- 标题与正文的偏差：正文重点不只是 federated RL，而是“如何在异构体之间抽象通用 skill 并在本地做过滤聚合”。

## Algorithm Design 快照
论文研究多 UAV 在 MEC 场景中的分布式导航问题。由于 UAV 在覆盖半径、最大速度和算力上存在异构性，集中式训练既不现实也难以迁移，而直接做参数共享又容易破坏个体差异。为此，作者提出 SHDRLN，用上层技能策略和下层技能网络抽象通用导航技能；再提出 DFRL，在云端聚合相似策略、在 UAV 端自适应过滤不适合自身参数的更新。这样，系统既保留分布式执行能力，也维持跨异构 UAV 的知识共享效率。

## 图1系统框架草案
- 系统实体：多架异构 UAV、移动用户、云服务器。
- 任务/数据流：UAV 依据局部观测决定移动与服务；云端周期性聚合上层策略参数后回传。
- 控制/优化变量：飞行方向、速度、技能选择、联邦聚合权重。
- 约束来源：局部可观测性、异构性能参数、任务卸载等待时间、能量消耗。
- 画图提醒：图中要把“本地技能网络 + 云端聚合 + UAV 端过滤”三层联邦结构画清楚。

## System Model
- 各 UAV 的覆盖半径、数量规模、最大飞行速度和计算资源可以不同。
- 每架 UAV 根据局部观测独立决策，系统不依赖集中式全局状态。
- 优化目标是整体任务卸载能效，同时兼顾用户覆盖与等待时间。
- 知识共享通过云端聚合实现，但聚合结果需要适配不同 UAV 的性能参数。

## Algorithm Design 详解
- SHDRLN：采用分层强化学习，将原子动作抽象为高层通用 skill，以减小异构策略差异。
- DFRL：在服务器端聚合相似 SPN 参数，在 UAV 端做自适应梯度过滤，避免负迁移。
- 训练观察：SHDRLN (DFRL) 比 SHDRLN 和 SAC 有更好的能效稳定性，且在较大异构差异下下降更平缓。
- 方法意义：这篇论文把[[异构联邦强化学习]]接入[[轨迹优化与协同控制]]主线，说明导航学习不只是在做 MARL，也在吸收 federated personalization 的思想。
- 实验结论：DFRL 可用约三分之一的训练轮数达到 `2.7 KB/J` 左右的平均能效，同时对异构度变化更稳健。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成多 UAV-MEC 场景
- 平台与软件：未说明
- 硬件与算力：未明确披露
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文给出了多组异构性敏感性实验和训练/测试时间对比，但未公开代码与平台栈。

## Introduction 写作素材
- 当 UAV 明显异构时，共享一个统一导航策略并不总是合理，策略共享需要结构化抽象。
- 分布式导航不只是控制问题，还包含跨 UAV 知识组织与迁移问题。
- 这篇论文可支撑“异构空中平台上的学习控制正在从 MARL 走向分层 + 联邦共享”的判断。

## Related Work 写作素材
- 与 CTDE 式多智能体方法相比，本文强调真实场景下的局部观测与异构共享。
- 与普通联邦学习相比，本文的共享对象不是静态分类器，而是分层导航策略。
- 与单 UAV DRL 导航相比，本文更强调跨 UAV 的可迁移知识组织。

## 相关系统建模页
- [[计算卸载模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[异构联邦强化学习]]
- [[联邦学习]]
- [[轨迹优化与协同控制]]
- [[任务卸载与资源分配研究主线]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/wang2024DecentralizedNavigationHeterogeneous.md)
