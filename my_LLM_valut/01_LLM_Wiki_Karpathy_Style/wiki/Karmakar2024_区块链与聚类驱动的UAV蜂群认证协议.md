---
tags: [论文, 区块链认证, 蜂群安全, PUF, 动态聚类]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/karmakar2024BlockchainBasedDistributedIntelligent.md
venue_tier: CCF-A
literature_type: system
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
  - NS-3.36
  - Ethereum Virtual Machine
frameworks:
  - Scyther
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---


# Karmakar2024 区块链与聚类驱动的UAV蜂群认证协议

## 单行摘要
论文提出 SwarmAuth，把 PUF、区块链、智能聚类和智能合约结合起来，为 UAV 蜂群建立分布式互认证与访问控制机制。

## 题目驱动研究框架
- 研究场景：高动态 UAV 蜂群在不可信环境中的身份认证与可信通信。
- 研究对象：地面控制站、蜂群 UAV、区块链账本、位置聚类与 PUF 认证。
- 核心问题：传统中心化认证易出现单点失效，而蜂群移动性又会破坏认证稳定性。
- 标题承诺的方法：blockchain-based distributed and intelligent clustering-enabled authentication。
- 期望效果：实现可扩展、可追溯、抗攻击的分布式蜂群认证。
- 标题与正文的偏差：正文除了区块链外，动态 K-means 聚类对性能改善也很关键。

## Algorithm Design 快照
论文针对 UAV 蜂群在高移动、不可信环境中缺乏统一身份认证与可信存储的问题，设计了 SwarmAuth 分布式认证框架。系统使用 PUF 完成 GSC 与 UAV 的互认证，并利用区块链不可篡改账本存储认证信息，通过智能合约实现访问控制和状态更新。同时，论文使用基于 K-means 的动态位置聚类形成局部簇，以降低传播时延并适应蜂群移动。最终方案通过安全性分析与 NS-3 仿真验证，在通信与计算开销、吞吐和时延上优于多种基线。

## 图1系统框架草案
- 系统实体：GSC、多个 UAV、区块链节点、智能合约、动态簇头/簇成员。
- 任务/数据流：注册信息写入链上，认证请求在簇内转发，链上合约执行访问控制。
- 控制/优化变量：簇划分、认证消息流程、链上记录更新、簇规模。
- 约束来源：高移动性、无线传播时延、计算/通信开销、安全攻击面。
- 画图提醒：图里需要同时画出“簇内认证流程”和“链上存证流程”两条路径。

## System Model
- UAV 蜂群根据位置使用 K-means 动态形成簇，以维持认证流程的局部性。
- GSC 与 UAV 之间采用基于 PUF 的互认证机制，减轻密钥存储风险。
- 区块链保存注册与认证相关信息，智能合约负责访问控制与记录更新。
- 系统关注的不只是安全正确性，也包括吞吐、时延和簇规模变化下的性能。

## Algorithm Design 详解
- 第一步定义基于 PUF 的注册、互认证和簇内消息传输流程。
- 第二步在链上实现认证信息存储和智能合约控制逻辑。
- 第三步用 K-means 动态生成位置相关簇，控制簇规模和消息传播成本。
- 第四步通过安全证明、Scyther 分析与 NS-3 仿真比较系统性能。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成蜂群拓扑与移动场景
- 平台与软件：`NS-3.36`；`Ethereum Virtual Machine`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：安全分析与性能仿真都较完整，但没有给出公开实现仓库。

## Introduction 写作素材
- 蜂群无人机的安全问题不再只是加密算法选择，而是身份、状态、迁移和访问控制如何共同演化。
- 中心化认证在蜂群场景中会带来单点失效与可扩展性问题。
- 这篇论文适合支撑“自治蜂群需要可信基础设施而不仅是链路安全”的写作判断。

## Related Work 写作素材
- 与中心化认证相比，本文强调区块链分布式存证与访问控制。
- 与静态蜂群安全工作不同，本文加入动态 K-means 聚类应对移动性。
- 与只做协议证明的安全论文不同，本文还给出了吞吐、时延和开销分析。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[区块链认证]]
- [[安全与服务保障]]

## 来源
- [原文](../raw/markdown/karmakar2024BlockchainBasedDistributedIntelligent.md)
