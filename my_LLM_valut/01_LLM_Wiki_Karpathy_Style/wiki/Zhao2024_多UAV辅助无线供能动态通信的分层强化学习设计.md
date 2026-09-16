---
tags: [论文, 无线供能动态通信, 分层强化学习, 无线供能, WPCN]
created: 2026-04-10
updated: 2026-04-10
sources:
  - ../raw/markdown/zhao2024DesigningMultiUAVAided.md
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
platforms:
  - Python 3.9.12
frameworks:
  - PyTorch 1.12.1
  - MAHDRL
  - SAC
  - DQN
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Zhao2024_多UAV辅助无线供能动态通信的分层强化学习设计

## 单行摘要
论文研究多 UAV 辅助 WPCN 中节点在能量采集与数据传输之间的动态切换，提出双阈值节点类型更新规则，并用双层 `MAHDRL` 分别学习 UAV 轨迹/WET 与子时隙 WDC 决策，以最大化总传输数据量。

## 题目驱动研究框架
- 研究场景：动态环境下的多 UAV 无线供能通信网络。
- 研究对象：多个 UAV、无线节点 WN、能量采集 E-node、信息传输 I-node。
- 核心问题：节点类型会随电量动态切换，UAV 的轨迹、供能和收数动作又彼此紧耦合，传统分离式设计难以奏效。
- 标题承诺的方法：hierarchical deep reinforcement learning。
- 期望效果：在 UAV 有限机载能量约束下提升全网数据传输总量。

## Algorithm Design 快照
论文的关键创新在于：不再默认节点按照固定 harvest-then-transmit 周期工作，而是允许每个节点在时间槽内根据双阈值规则动态切换成 E-node 或 I-node。对应地，作者用双层 `MAHDRL` 分别处理不同时间尺度决策：上层 `SAC` 决定 UAV 连续轨迹和二元 WET 动作，下层 `DQN` 决定子时隙级别的 WDC 调度。

## 图1系统框架草案
- 实体：多个 UAV、多个无线节点 WN。
- 节点状态：E-node / I-node 双阈值切换。
- 决策层：上层轨迹 + WET，下层子时隙 WDC。
- 指标：总传输数据量、UAV 机载能量约束。

## System Model
- 每个节点会依据电量水平动态切换角色，而不是固定 Harvest-then-Transmit。
- 多个 UAV 既要决定连续飞行轨迹，又要选择何时对节点发起 WET 或 WDC。
- 系统显式建模 UAV 电量与节点电量演化，因此是一个长期动态资源管理问题。
- WDC 在更细粒度的子时隙内进行，以缓解多节点上传干扰。

## Algorithm Design 详解
- 第一步：提出 double-threshold WN type updating rule，定义 E-node / I-node 切换逻辑。
- 第二步：把总数据量最大化问题写成多智能体层次化决策问题。
- 第三步：上层 `SAC` 学习连续轨迹与 WET 决策。
- 第四步：下层 `DQN` 在给定轨迹下学习 WDC 子时隙调度。
- 第五步：通过训练/测试阶段仿真比较验证多 UAV 数量与网络规模下的可扩展性。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成场景参数
- 平台与软件：`Python 3.9.12`
- 方法组件：`PyTorch 1.12.1`、`MAHDRL`、`SAC`、`DQN`
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未提供真实硬件验证与代码发布信息

## Introduction 写作素材
- 无线供能通信不应再被看成固定两阶段协议，节点状态更新本身就是系统动态的一部分。
- 当多 UAV 同时参与 WET 和 WDC 时，连续轨迹与离散子时隙调度天然需要层次化求解。

## Related Work 写作素材
- 与固定节点类型或固定两阶段协议的工作相比，本文强调节点角色动态更新。
- 与单时间尺度 DRL 不同，本文显式把 WET 与 WDC 分到两层处理。

## 相关系统建模页
- [[无人机能耗模型]]

## 相关概念与主题页
- [[无线供能动态通信]]
- [[无线供能传输（WPT）]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [原文](../raw/markdown/zhao2024DesigningMultiUAVAided.md)
