---
tags: [论文, 联邦学习, 多无人机协同, 群体智能, 数据价值]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/cui2024DataValueBased.md
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
  - public_dataset
platforms: []
frameworks: []
datasets:
  - MNIST
  - FLAME
hardware_stack: []
artifact_availability: partial
reproducibility_level: medium
---

# Cui2024 不稳定通信下基于数据价值的UAV群异步联邦学习

## 单行摘要
论文面向空中链路不稳定、数据异构的 UAV 群联邦学习场景，提出两阶段异步联邦学习框架，用 Shapley Value 衡量数据价值、用 Network AoU 表征公平性，并以 Whittle Index 实现顺序 UAV 选择。

## 题目驱动研究框架
- 研究场景：空中通信不稳定、各 UAV 本地数据分布异构的群体协同训练场景。
- 研究对象：作为联邦学习客户端的多架 UAV、中心 UAV、局部数据集与空空链路。
- 核心问题：同步聚合在不稳定通信下难以持续，而只偏向高价值数据又会损害公平性与泛化能力，如何在异步更新中同时兼顾收敛、数据价值和公平性。
- 标题承诺的方法：data value based asynchronous federated learning。
- 期望效果：提升 UAV 群训练鲁棒性，在链路波动条件下仍维持较好的模型精度与选择公平性。
- 标题与正文的偏差：标题强调“data value based”，正文真正的完整结构是“Shapley 预训练评估 + AoU 公平建模 + Whittle Index 顺序选择”。

## Algorithm Design 快照
论文针对 UAV 群在不稳定空空通信条件下的协同模型训练问题，研究在本地数据异构和链路掉线并存时如何进行鲁棒联邦学习。作者提出两阶段异步联邦学习框架：预训练阶段把 UAV 参与训练过程建模为合作博弈，用 Shapley Value 衡量不同 UAV 数据集的边际贡献，并给出采样估计误差上界；训练阶段进一步引入 Network AoU，把数据价值、公平性和连接概率统一到顺序 UAV 选择问题中，再用 Whittle Index 最小化 AoU。最终系统在不依赖同步聚合的前提下实现更稳健的群体训练。

## 图1系统框架草案
- 系统实体：中心 UAV、多个普通 UAV、本地数据集、空空无线链路、测试集。
- 任务/数据流：中心 UAV 顺序选择可连接 UAV 参与参数更新；被选 UAV 用本地数据训练后回传参数；预训练阶段评估数据价值，训练阶段按 AoU 与价值联合调度。
- 控制/优化变量：客户端选择顺序、Shapley 估计样本、AoU 状态、Whittle 指数。
- 约束来源：链路断连概率、数据异构、有限采样预算、公平性需求。
- 画图提醒：最好把“预训练阶段”和“训练阶段”画成上下两层，否则数据价值评估与在线调度的关系不够清楚。

## System Model
- 系统由一个中心 UAV 和多个采集数据的从属 UAV 组成，每个 UAV 持有局部数据集，且由于部署区域不同，本地数据通常是 Non-IID 的。
- 通信链路是随机可用的，论文用每个 UAV 与中心保持连接的概率建模不稳定通信，因此中心并不等待所有客户端完成后再做聚合。
- 参数更新采用顺序异步方式：中心每轮只选择一架 UAV 更新参数，从而避免同步聚合中的 straggler 问题。
- 作者同时显式建模数据价值与公平性：前者通过合作博弈中的 Shapley Value 估计，后者通过 AoU 与 Network AoU 描述“多久没被选中过”及其对泛化的影响。

## Algorithm Design 详解
- 第一步是提出异步联邦学习框架：中心主动选择 UAV 更新，而不是被动等待全部反馈。
- 第二步是收敛分析：作者分别讨论凸和非凸情形，给出训练性能上界，并指出数据量与梯度异质性共同决定单个 UAV 的训练贡献。
- 第三步是数据价值评估：把 UAV 参与训练建模为合作博弈，用 Shapley Value 衡量边际贡献，并设计分布式采样估计方法以降低精确求解复杂度。
- 第四步是公平性建模：提出 AoU 与 Network AoU，使“高价值客户端多参与”和“所有客户端都应适度参与”之间可被统一权衡。
- 第五步是在线调度：将顺序 UAV 选择转化为 Whittle Index 驱动的 AoU 最小化问题，在链路随机可用的条件下得到近似最优策略。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：公开数据集；涉及数据集：`MNIST`、`FLAME`
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：部分资产公开
- 复现判断：`medium`
- 证据备注：论文以数值仿真为主，已经给出部分实验资产信息，但仍缺少更强的真实部署证据。

## Introduction 写作素材
- 在 UAV 群协同训练里，同步联邦学习最脆弱的不是模型本身，而是空中链路不稳定带来的参数等待与失配。
- 数据异构并不只会带来训练退化，它也意味着不同 UAV 的数据价值本身存在差异，因此“让谁更新”是一个核心问题。
- 仅按照数据价值贪心选择客户端会损害全局泛化，因此公平性必须显式进入系统设计。
- 这篇论文很适合支撑“空中边缘智能训练需要从同步聚合转向异步价值感知调度”的引言逻辑。

## Related Work 写作素材
- 与传统同步联邦学习相比，本文把空中链路不稳定性作为一等约束，转向顺序异步更新。
- 与只按数据量或梯度大小衡量客户端贡献的工作相比，本文用 Shapley Value 建模数据价值。
- 与只关注收敛速度的客户端选择工作相比，本文进一步把公平性抽象为 AoU 并引入 Whittle Index 调度。
- 相关工作写作时，可以把它放在“UAV swarm + asynchronous FL + data value + fairness-aware scheduling”的交叉点。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[联邦学习]]
- [[多无人机协同]]
- [[空中边缘大模型前沿]]

## 来源
- [原文](../raw/markdown/cui2024DataValueBased.md)
