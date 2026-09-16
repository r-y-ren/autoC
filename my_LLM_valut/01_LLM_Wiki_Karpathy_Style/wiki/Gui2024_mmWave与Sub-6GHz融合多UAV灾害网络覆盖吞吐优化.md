---
tags: [论文, 灾害网络, 覆盖优化, 吞吐优化, 空中通信]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/gui2024CoverageProbabilityThroughput.md
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
  - Python 3.9.6
frameworks:
  - PyTorch 1.13.1
datasets: []
hardware_stack:
  - Apple M2
  - Hynix LPDDR5 16GB
artifact_availability: unknown
reproducibility_level: medium
---

# Gui2024 mmWave 与 Sub-6GHz 融合多 UAV 灾害网络覆盖吞吐优化

## 单行摘要
论文在灾害场景下联合处理多 UAV 覆盖概率提升与融合频段吞吐优化，并用 DDPG 做信道和波束功率分配。

## 题目驱动研究框架
- 研究场景：地面基础设施受损后的灾害救援网络。
- 研究对象：采用 mmWave 与 Sub-6GHz 融合链路的多 UAV、地面终端及其聚类分布。
- 核心问题：先提升单 UAV 与整体系统的有效覆盖概率，再在此基础上优化吞吐率并满足频谱-能效约束。
- 标题承诺的方法：coverage probability and throughput optimization。
- 期望效果：以更少部署成本实现更高覆盖质量和更强链路吞吐。
- 标题与正文的偏差：标题看似两个串联目标，但正文实际上先提出新的覆盖质量度量，再把传输资源优化写成 MDP。

## Algorithm Design 快照
论文聚焦灾害救援场景中的多 UAV 通信网络，先定义考虑有效覆盖时间比例与被覆盖终端比例的新型覆盖质量指标，再针对 mmWave 与 Sub-6GHz 融合链路设计总体覆盖改进与吞吐优化方法。在第二阶段，作者把信道与功率波束分配写成满足频谱-能效约束的 MDP，并用 DDPG 进行策略学习，从而把部署、覆盖和传输资源控制串到同一条灾害通信主线上。

## 图1系统框架草案
- 系统实体：多架灾害救援 UAV、地面终端簇、mmWave/Sub-6GHz 双频链路。
- 任务/数据流：UAV 先通过部署与覆盖策略形成有效服务圈，再在链路层做信道和功率波束分配以提升吞吐。
- 控制/优化变量：UAV 部署与覆盖轨迹、终端聚类结果、信道分配、功率波束配置。
- 约束来源：灾害区域终端分布不均、有效覆盖时间、频谱效率与能量效率。
- 画图提醒：图里应把“覆盖概率优化”和“吞吐优化”明确画成两阶段。

## System Model
- 系统采用多 UAV 融合频段通信架构，既利用 sub-6 覆盖稳定性，又利用 mmWave 高吞吐能力。
- 论文提出的覆盖质量不只看几何覆盖，还看有效覆盖持续时间和被覆盖终端比例。
- 在覆盖层之上，又叠加了信道和功率波束分配问题，使系统模型呈现明显的跨层特征。
- 与传统灾害通信部署不同，这里覆盖和吞吐不是分离问题，而是顺序耦合。

## Algorithm Design 详解
- 第一步是定义单 UAV 覆盖质量与系统总体覆盖概率的新指标。
- 第二步是利用终端分布不均特征设计覆盖改进与成本降低策略。
- 第三步是把吞吐优化写成带频谱-能效约束的 MDP。
- 第四步是使用 DDPG 学习信道与功率波束分配策略。
- 第五步是用 Python/PyTorch 仿真验证覆盖与吞吐的联动提升。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：`Python 3.9.6`；`PyTorch 1.13.1`
- 硬件与算力：`Apple M2`；`Hynix LPDDR5 16GB`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文给出较清楚的软件环境和仿真配置，适合作为空中灾害通信覆盖-吞吐联合优化的基线。

## Introduction 写作素材
- 灾害网络中“先有覆盖，再谈吞吐”，但覆盖质量本身并不能只用静态半径描述。
- 多频融合 UAV 网络让部署、覆盖概率和传输资源优化逐步耦合。
- 这篇论文适合支撑“灾害救援网络需要覆盖与吞吐一体化设计”的引言。

## Related Work 写作素材
- 与只优化 UAV 覆盖位置的工作相比，本文把覆盖质量进一步连接到吞吐优化。
- 与单频段设计相比，本文关注 mmWave 与 Sub-6GHz 的融合。
- 与传统解析分配方法相比，本文把资源控制建模为 MDP 并用 DDPG 求解。

## 相关系统建模页
- [[区域覆盖与部署模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[三维区域覆盖]]
- [[空中通信与协同传输]]
- [[覆盖与部署优化主线]]

## 来源
- [原文](../raw/markdown/gui2024CoverageProbabilityThroughput.md)
