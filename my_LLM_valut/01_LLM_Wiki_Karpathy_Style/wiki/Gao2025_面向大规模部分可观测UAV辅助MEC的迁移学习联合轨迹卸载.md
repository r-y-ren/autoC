---
tags: [论文, UAV辅助MEC, 任务卸载, 迁移学习, 多智能体强化学习]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/gao2025TransferLearningJoint.md
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
artifact_availability: open
reproducibility_level: medium
---

# Gao2025 面向大规模部分可观测 UAV 辅助 MEC 的迁移学习联合轨迹卸载

## 单行摘要
论文提出 PTMF-MAAC，通过策略迁移与部分可观测平均场多智能体学习提升大规模 UAV-MEC 联合轨迹卸载效率。

## 题目驱动研究框架
- 研究场景：大规模、部分可观测的 UAV 辅助 MEC 服务环境。
- 研究对象：多架 UAV、智能终端、动态到达任务以及局部可见的协同决策信息。
- 核心问题：现有联合轨迹控制与任务卸载算法训练样本需求大、难扩展到大规模 UAV 系统。
- 标题承诺的方法：transfer learning for joint trajectory control and task offloading。
- 期望效果：提高学习效率，并让策略在更多 UAV 参与的场景中保持可扩展性。
- 标题与正文的偏差：标题强调 transfer learning，但正文真正的完整解法是“策略迁移 + mean-field MAAC + 部分可观测建模”。

## Algorithm Design 快照
论文面向大规模部分可观测 UAV-MEC 系统，研究多 UAV 如何联合决定飞行轨迹和任务卸载策略，同时避免传统 MARL 在规模扩大时训练成本爆炸。作者提出 PTMF-MAAC 框架：先用策略迁移机制判断哪些 UAV 历史策略可被复用以及何时终止迁移，再用部分可观测平均场方法把其他 UAV 的影响压缩成均值表示，显著降低联合状态/动作空间规模。整体目标是在保持低时延服务能力的同时提升训练效率和可扩展性。

## 图1系统框架草案
- 系统实体：多架 UAV、多个智能终端、局部观测器、共享经验或迁移源策略库。
- 任务/数据流：终端任务到达后，邻近 UAV 依据局部状态决定轨迹机动与卸载服务；策略迁移模块为每个 UAV 选择可借鉴的已有策略。
- 控制/优化变量：UAV 轨迹动作、任务卸载动作、策略迁移开关与终止时机、平均场表征。
- 约束来源：局部可观测、终端时延需求、UAV 数量扩张带来的联合空间爆炸。
- 画图提醒：图里应把“源策略迁移”和“平均场近似”画成并列的两层加速机制。

## System Model
- 系统被建模为部分可观测多智能体环境，每个 UAV 只能获得局部观测，而无法直接访问全局状态。
- 每个 UAV 需要联合决定服务终端的轨迹控制与任务卸载，因此控制变量同时包含运动和计算决策。
- 随着 UAV 数量增加，直接建模所有智能体的交互会导致状态与动作维度指数级增长。
- 论文通过 mean-field 思路把“其他 UAV 的影响”压缩成平均值，从而得到更可扩展的近似系统模型。

## Algorithm Design 详解
- 第一步是策略迁移：为每个 UAV 判断哪些历史策略可复用，以及何时结束迁移以避免负迁移。
- 第二步是平均场建模：用平均场近似替代显式枚举全部其他 UAV 的交互影响。
- 第三步是 MAAC 学习：在部分可观测条件下做多智能体 actor-critic 学习。
- 第四步是联合动作设计：把轨迹控制和任务卸载纳入同一策略输出空间。
- 第五步是大规模验证：通过与基线比较展示学习效率和规模扩展能力的提升。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：代码或资产已公开
- 复现判断：`medium`
- 证据备注：论文提供了代码入口，但实验仍以仿真环境为主，因此它更适合作为大规模 UAV-MEC 学习范式的算法锚点。

## Introduction 写作素材
- 大规模 UAV-MEC 的瓶颈不只是决策最优性，还有训练是否学得动、能不能扩展。
- 当 UAV 数量增长时，传统联合轨迹卸载算法面临严重的样本复杂度和状态维数问题。
- 这篇论文适合支撑“从可解小规模到可扩展大规模”的引言逻辑。

## Related Work 写作素材
- 与小规模联合轨迹卸载方法相比，本文面向 large-scale partially observable 场景。
- 与纯 mean-field 方法相比，本文进一步引入策略迁移以缩短冷启动训练时间。
- 与集中式全局状态方法相比，本文强调部分可观测和分布式决策。

## 相关系统建模页
- [[计算卸载模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[迁移学习]]
- [[多智能体强化学习]]
- [[任务卸载与资源分配研究主线]]
- [[轨迹优化与协同控制]]

## 来源
- [原文](../raw/markdown/gao2025TransferLearningJoint.md)
