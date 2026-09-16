---
tags: [论文, 协同波束赋形, 多智能体强化学习, 多无人机协同, 空中通信]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/dai2023MultiAgentDeepReinforcement.md
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
  - Python 3.8
frameworks:
  - PyTorch 1.10.0
datasets: []
hardware_stack:
  - AMD EPYC 7642 48-Core CPU
  - NVIDIA GeForce RTX 3090 GPU
  - 128GB RAM
artifact_availability: unknown
reproducibility_level: medium
---

# Dai2023 多智能体深度强化学习的UAV协同波束赋形

## 单行摘要
论文研究多 UAV 形成虚拟天线阵列与远端基站通信的问题，将 UAV 位置和激励电流权重联合建模为多目标优化，并提出 HATRPO-UCB 以在动态环境中同时提升协同波束赋形速率和 UAV 运动能效。

## 题目驱动研究框架
- 研究场景：多 UAV 组成虚拟阵列，与远端基站进行空地协同通信。
- 研究对象：多架旋翼 UAV、远端基站、虚拟阵列波束赋形与 UAV 运动能耗。
- 核心问题：协同波束赋形要求 UAV 同时优化空间位置和激励电流权重，而速率提升与运动能耗又彼此冲突，如何在动态环境下实时求解。
- 标题承诺的方法：multi-agent deep reinforcement learning。
- 期望效果：在保证阵列协同性的同时，提升通信速率并降低整体飞行能耗。
- 标题与正文的偏差：标题强调 collaborative beamforming，正文真正的难点在于多目标优化与多智能体信用分配，而不仅是阵列增益计算。

## Algorithm Design 快照
论文针对多 UAV 组成虚拟天线阵列与远端基站通信的问题，研究如何在动态环境中联合优化 UAV 三维位置和激励电流权重，使阵列传输速率最大而总运动能耗最小。作者先构建多目标优化问题 UCBMOP，把协同波束赋形的阵列增益、空地链路质量、无人机运动约束和碰撞约束统一起来。随后将问题转化为多智能体 Markov game，并在 HATRPO 基础上提出 HATRPO-UCB：通过观测增强、agent-specific global state 和 Beta 分布策略改进训练稳定性与动作边界处理，从而学习多 UAV 协同波束赋形策略。

## 图1系统框架草案
- 系统实体：多架 UAV、远端基站、虚拟阵列原点、空地无线链路。
- 任务/数据流：各 UAV 根据观测移动到目标位置并调整激励电流权重，形成面向指定基站的联合波束。
- 控制/优化变量：UAV 三维坐标、激励电流权重、阵列原点相对位置。
- 约束来源：监控区域边界、高度限制、最小安全间距、运动能耗与服务时长。
- 画图提醒：图里最好把“物理阵列结构”和“MARL 决策层”同时画出来，才能体现通信目标与控制变量的耦合。

## System Model
- 多架 UAV 构成 UAV-enabled virtual antenna array，系统目标是通过位置协同和电流权重调节提升对远端基站的波束增益。
- 优化变量既包括 UAV 的三维悬停位置，也包括每架 UAV 的 excitation current weight，因此系统同时具有几何控制和通信控制两类决策。
- 论文显式建模旋翼 UAV 水平、爬升和下降阶段的运动能耗，并把阵列速率提升和总运动能耗降低视为两个冲突目标。
- 多智能体状态设计不仅包含 UAV 自身和其他 UAV 的相对信息，也包括目标基站的参考点表示，从而适配不同服务目标和动态场景。

## Algorithm Design 详解
- 第一步是构建 UCBMOP：联合最大化阵列传输速率、最小化所有 UAV 的运动能耗。
- 第二步是转化为 Markov game：每架 UAV 作为 agent，动作是下一时隙的位置和激励电流权重，奖励函数综合速率、距离、能耗与阵型紧凑性。
- 第三步是引入 HATRPO-UCB：在 HATRPO 框架中加入 observation enhancement、agent-specific global state 和 Beta policy，以适应有限动作边界和大规模多 UAV 协作。
- 第四步是顺序策略更新：通过 trust-region 型联合策略改进，缓解多智能体非平稳性和信用分配问题。
- 第五步是实验比较：验证所提算法在速率与能耗双目标上均优于若干基线方案。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：`Python 3.8`；`PyTorch 1.10.0`
- 硬件与算力：`AMD EPYC 7642 48-Core CPU`；`NVIDIA GeForce RTX 3090 GPU`；`128GB RAM`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文以数值仿真为主，已经给出部分实验资产信息，但仍缺少更强的真实部署证据。

## Introduction 写作素材
- 多 UAV 协同通信的难点不只在“站得开”，而在“如何一起形成有方向性的有效辐射结构”。
- 一旦 UAV 被视为虚拟阵列元素，位置控制与通信资源控制就不再可分离。
- 传统离线优化难以应对动态基站目标和实时响应要求，多智能体强化学习因此成为可行工具。
- 这篇论文适合支撑“空中通信系统中的控制-通信一体化设计”这一引言切口。

## Related Work 写作素材
- 与只优化轨迹或功率的多 UAV 通信工作相比，本文进一步引入激励电流权重优化。
- 与单智能体 DRL 通信优化工作相比，本文显式处理了多 UAV 协同波束赋形中的联合策略学习。
- 与传统解析式阵列优化相比，本文强调动态环境与实时决策场景下的 MADRL 优势。
- 相关工作写作时，可以把它放在“UAV virtual array + collaborative beamforming + MADRL”的交叉处。

## 相关系统建模页
- [[无人机能耗模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[协同波束赋形]]
- [[多智能体强化学习]]
- [[空中通信与协同传输]]
- [[多无人机协同]]

## 来源
- [原文](../raw/markdown/dai2023MultiAgentDeepReinforcement.md)
