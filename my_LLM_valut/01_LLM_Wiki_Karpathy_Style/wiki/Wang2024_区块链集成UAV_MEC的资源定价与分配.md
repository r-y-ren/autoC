---
tags: [论文, 区块链, UAV辅助MEC, 资源定价, Stackelberg博弈]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/wang2024ResourceAllocationBlockchain.md
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
platforms:
  - MATLAB R2018b
frameworks:
  - Stackelberg differential game
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Wang2024 区块链集成UAV-MEC的资源定价与分配

## 单行摘要
论文在 UAV-enabled MEC 中引入 DPoS 区块链与信誉验证节点，通过两阶段 Stackelberg 微分博弈联合优化资源定价与分配。

## 题目驱动研究框架
- 研究场景：融合区块链的 UAV 辅助 MEC 网络。
- 研究对象：一架 UAV 主节点、多个边缘验证节点、地面用户、信誉状态与交易状态。
- 核心问题：在开放环境存在安全与隐私风险的前提下，如何通过可信交易机制分配边缘计算资源并维持 QoS。
- 标题承诺的方法：resource allocation in blockchain integration of UAV-enabled MEC networks。
- 期望效果：实现资源交易、定价和信誉激励的动态均衡。
- 标题与正文的偏差：正文更像“区块链驱动的资源交易机制设计”，重点不在传统卸载比例，而在领导者-跟随者定价和信誉动态。

## Algorithm Design 快照
论文研究 UAV-enabled MEC 中引入区块链后的资源交易问题，其中 UAV 作为主节点发布单位资源价格，基于信誉机制选出的边缘验证节点作为跟随者决定计算资源供给。难点在于用户服务需求与验证节点信誉都随时间变化，静态定价无法反映真实供需和激励。为此，作者把需求状态和信誉状态写成微分方程约束，并构建两阶段 Stackelberg 微分博弈：第一阶段 UAV 定价，第二阶段验证节点按收益决定资源分配。最终目标是在保障链上透明可信的同时提升 QoS 与资源利用效率。

## 图1系统框架草案
- 系统实体：UAV 主节点、多个验证节点 BS、地面用户、区块链账本。
- 任务/数据流：用户向 UAV 请求卸载服务；UAV 向验证节点购买/协调计算资源；交易记录写入区块链。
- 控制/优化变量：单位资源价格、验证节点分配的计算资源、UAV 飞行轨迹、验证节点信誉状态。
- 约束来源：用户需求动态、信誉阈值、计算能力、链上共识与交易透明性。
- 画图提醒：图中要同时表现“服务交易流”和“区块链记账流”，这样才能看出机制设计的价值。

## System Model
- UAV 既是移动 MEC 服务提供者，也是 DPoS 机制中的主节点；验证节点由高信誉边缘节点组成。
- 用户需求与验证节点信誉随时间演化，因此系统状态不是静态参数，而是动态变量。
- 区块链用于记录 100% 的资源交易，保证透明与可信，但也引入了额外计算与验证成本。
- 目标函数同时包含时延、能耗和资源交易收益，是典型的机制设计型 UAV-MEC 模型。

## Algorithm Design 详解
- 第一层是状态建模：把用户服务需求和验证节点信誉都建成随时间变化的动态状态。
- 第二层是两阶段 Stackelberg 微分博弈：UAV 作为领导者先定价，验证节点作为跟随者后决定分配资源。
- 第三层分析均衡：求开环解，观察价格、资源分配、需求和信誉如何随时间收敛。
- 这篇论文很适合与[[Chen2025_博弈论驱动的UAV辅助边缘计算卸载与资源定价]]对照，因为它把“定价”从静态博弈推进到了动态信誉与区块链语境。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成区块链集成 UAV-MEC 场景
- 平台与软件：`MATLAB R2018b`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文给出了较完整参数表和状态演化实验，但缺少代码和区块链实现细节。

## Introduction 写作素材
- 在 UAV-MEC 的开放环境中，安全与隐私问题并不会自动被“卸载最优”解决，可信交易机制必须显式进入系统设计。
- 区块链在这里不是附加记录层，而是会改变资源价格、信誉激励和验证节点参与积极性的机制层。
- 这篇论文可以支撑“安全从认证治理进一步延伸到链上资源交易”的写法。

## Related Work 写作素材
- 与只关注安全认证的区块链 UAV 工作相比，本文处理的是资源交易与 QoS 激励。
- 与静态 Stackelberg 定价工作相比，本文引入微分博弈与动态信誉状态。
- 与传统 MEC 定价相比，本文把验证节点诚实参与和链上透明性一并纳入系统效用。

## 相关系统建模页
- [[计算卸载模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[资源定价]]
- [[区块链认证]]
- [[Stackelberg微分博弈]]
- [[安全与服务保障]]
- [[任务卸载与资源分配研究主线]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/wang2024ResourceAllocationBlockchain.md)
