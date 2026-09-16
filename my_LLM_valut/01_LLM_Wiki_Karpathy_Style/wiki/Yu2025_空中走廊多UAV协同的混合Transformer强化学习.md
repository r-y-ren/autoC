---
tags: [论文, 多智能体强化学习, Transformer, 空中走廊, 多无人机协同]
created: 2026-04-10
updated: 2026-04-10
sources:
  - ../raw/markdown/yu2025HybridTransformerBased.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
validation_type:
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks:
  - HTransRL
  - actor-critic
  - Transformer
  - curriculum learning
hardware_stack:
  - NVIDIA RTX 3090
datasets: []
artifact_availability: open
reproducibility_level: high
---

# Yu2025_空中走廊多UAV协同的混合Transformer强化学习

## 单行摘要
论文面向空中走廊中的多 UAV 协同通行问题，提出混合 `Transformer + actor-critic` 的 `HTransRL`，以处理可变规模状态、复杂空中几何约束和多机避碰协同。

## 题目驱动研究框架
- 研究场景：空中走廊约束下的多 UAV 协同飞行。
- 研究对象：多架 UAV、非协同飞行物体、空中走廊拓扑与安全约束。
- 核心问题：多 UAV 在共享空中走廊中同时飞行时，既要高到达率，又要控制碰撞和越界风险，而状态维度还会随系统规模动态变化。
- 标题承诺的方法：hybrid transformer based MARL。
- 期望效果：在复杂空中走廊环境中获得更好的可扩展性、避碰能力和到达效率。
- 标题与正文的偏差：标题突出 hybrid transformer，正文的真正亮点还包括 `MAPOMDP` 建模与 curriculum learning。

## Algorithm Design 快照
作者把空中走廊协同写成 `MAPOMDP`，并针对“状态规模随 UAV 数量变化”这个难点，引入 `Transformer` 处理可变长度观测，再把其与 actor-critic 联合成 `HTransRL`。训练阶段再叠加 curriculum learning，从低复杂度走廊逐步过渡到高复杂度空域，使策略在复杂场景下仍能保持可扩展性。

## 图1系统框架草案
- 环境层：多段空中走廊、静态/移动 NCFO、起止平面。
- 观测层：每架 UAV 局部球形观测区域内的 UAV 与障碍状态。
- 决策层：`Transformer` 编码可变规模观测，actor-critic 生成动作。
- 训练层：curriculum learning 渐进提升任务复杂度。
- 指标层：到达率、碰撞次数、越界次数、旅行时间。

## System Model
- 论文将多 UAV 走廊协同建模为 `MAPOMDP`。
- 每架 UAV 只能感知其局部观测球内的其他 UAV 和非协同飞行物，属于典型部分可观测多智能体场景。
- 空中环境由多个空中走廊段构成，且走廊连接方式和长度在训练中随机变化。
- 安全目标包括避免相互碰撞和走廊边界穿越，同时尽量缩短旅行时间。

## Algorithm Design 详解
- 第一步：定义多 UAV 在空中走廊中的状态、动作、奖励和安全约束。
- 第二步：提出 `HTransRL`，用 `Transformer` 编码可变规模局部观测，再与 actor-critic 联合训练。
- 第三步：通过 hybrid 架构让策略既能保持时空依赖建模能力，又兼顾强化学习控制效率。
- 第四步：使用 curriculum learning，从简单场景逐步提升到复杂空域，提高泛化与可扩展性。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成空中走廊与随机移动障碍场景
- 平台与软件：未说明
- 方法组件：`HTransRL`、`Transformer`、`actor-critic`、`curriculum learning`
- 硬件与算力：`NVIDIA RTX 3090`
- 开源情况：`open`
- 复现判断：`high`
- 缺失信息：未提供真实飞行闭环验证

## Introduction 写作素材
- 当多 UAV 开始在低空走廊内共享空域时，问题不再只是路径规划，而是受部分可观测与动态规模影响的协同控制。
- 传统固定维度策略网络难以优雅处理可变规模邻居与障碍集合。
- 这篇论文适合支撑“空域基础设施化之后，多 UAV 协同将越来越依赖结构化深度模型”的引言逻辑。

## Related Work 写作素材
- 与经典 MARL 路径规划工作相比，本文更突出空中走廊几何约束。
- 与普通注意力或 MLP 策略相比，本文通过 `Transformer` 处理可变维度输入。
- 与一次性训练固定难度环境的工作相比，本文显式使用 curriculum learning。

## 相关系统建模页
- [[区域覆盖与部署模型]]

## 相关概念与主题页
- [[空中走廊协同]]
- [[多智能体强化学习]]
- [[轨迹优化与协同控制]]

## 来源
- [原文](../raw/markdown/yu2025HybridTransformerBased.md)
