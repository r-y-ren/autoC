---
tags: [论文, UAV蜂群, 空战机动, 多智能体强化学习]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/zheng2024UAVSwarmAir.md
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
  - MARL
  - transfer learning
  - reward assignment
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Zheng2024_迁移增强MARL的UAV蜂群空战机动决策

## 单行摘要
论文针对短距 UAV 蜂群空战中的协同与对抗双重耦合问题，设计可处理不同态势信息的 actor 网络，并通过单机空战向蜂群空战的迁移训练和奖励分配机制缓解训练不稳定与“懒惰智能体”问题。

## 题目驱动研究框架
- 研究场景：短距 UAV 蜂群空战。
- 研究对象：同时与敌方和友方 UAV 交互的蜂群智能体。
- 核心问题：蜂群空战状态复杂、竞争与协作并存，直接训练 MARL 容易出现不稳定和 lazy agent。
- 标题承诺的方法：基于 MARL 和 transfer 的蜂群空战机动决策。
- 期望效果：提升群体协同作战能力和训练效率。

## Algorithm Design 快照
这篇论文很适合代表“高对抗、高耦合”的 UAV 蜂群决策问题。作者没有从零训练复杂蜂群空战策略，而是先利用一对一空战场景得到基础网络，再迁移到多机对抗环境中。与此同时，论文还用奖励分配机制重新分摊贡献，避免局部智能体在合作中“躺平”。

## 图1系统框架草案
- 态势层：敌我双方 UAV 的局部与全局态势。
- 表征层：actor 网络分别处理不同类型情报输入。
- 训练层：从单机空战向蜂群空战迁移。
- 协同层：奖励分配机制鼓励每个成员积极参与。
- 目标层：提升蜂群空战机动与协同决策质量。

## System Model
### 1. 蜂群空战环境
- UAV 同时面对敌方对抗和友方协作。
- 状态快速变化，动作与回报高度耦合。

### 2. 局部-全局状态设计
- actor 侧重局部可执行信息。
- critic 侧利用更完整的全局态势进行评估。

### 3. 学习目标
- 生成更合理的机动决策。
- 降低复杂对抗场景下的训练难度和协作退化。

## Algorithm Design 详解
### 1. 迁移训练
- 先在更稳定的一对一空战场景预训练策略。
- 再把相关表征迁移到更复杂的蜂群空战环境。

### 2. 奖励分配
- 通过 reward assignment 重新分配团队收益。
- 缓解多智能体协作中的 credit assignment 问题。

### 3. 研究意义
- 论文突出展示了 UAV 蜂群对抗任务如何借助迁移学习分阶段求解。
- 对后续写“协同控制向高对抗任务扩展”很有帮助。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成蜂群空战环境
- 平台与软件：未明确说明
- 方法组件：`MARL`、`transfer learning`、`reward assignment`
- 对比对象：无迁移训练、无奖励分配等消融基线
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：缺少训练平台和统一代码披露

## Introduction 写作素材
- 蜂群空战把竞争和协作同时推到极强程度，是检验多智能体策略泛化能力的硬场景。
- 简单从头训练复杂蜂群对抗策略，容易面临训练不稳定和 credit assignment 问题。
- 这篇论文适合用来支撑“复杂 UAV 蜂群任务需要分阶段迁移学习”的引言说法。

## Related Work 写作素材
- 单机空战与蜂群空战的复杂度存在数量级差异。
- 传统 MARL 方法在高度对抗场景中常出现懒惰智能体或协作失灵。
- 这篇论文把迁移训练与奖励重分配结合，专门面向高对抗蜂群机动任务。

## 相关系统建模页
- 当前更偏对抗式机动决策，尚未形成稳定的专用系统建模页。
- 可暂参考[[容错控制与碰撞规避模型]]理解协同约束与安全间隔写法。

## 相关概念与主题页
- [[空战机动决策]]
- [[多智能体强化学习]]
- [[迁移学习]]
- [[多无人机协同]]
- [[轨迹优化与协同控制]]

## 来源
- [原文](../raw/markdown/zheng2024UAVSwarmAir.md)
