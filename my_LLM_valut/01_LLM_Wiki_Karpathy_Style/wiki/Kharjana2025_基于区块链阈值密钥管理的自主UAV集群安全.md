---
tags: [论文, 阈值密钥管理, 区块链, 多重签名, UAV集群安全]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/kharjana2025SecuringAutonomousUAV.md
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
  - OMNET++
  - Crypto++
frameworks: []
datasets: []
hardware_stack:
  - Ubuntu 20.04.5 LTS virtual machine
  - Windows 11 PC
  - Intel Core i3 CPU 3.60 GHz
  - 8 GB RAM
  - 2 GB RAM virtual machine
artifact_availability: unknown
reproducibility_level: medium
---


# Kharjana2025 基于区块链阈值密钥管理的自主UAV集群安全

## 单行摘要
论文利用区块链上的 crypto-asset 与 multisignature 机制，为自治 UAV 集群建立了可配置阈值的协同密钥管理系统。

## 题目驱动研究框架
- 研究场景：远程部署、自主运行的 UAV 集群安全管理。
- 研究对象：集群 UAV、区块链账本、阈值签名、子集群/重组/迁移等关键场景。
- 核心问题：集中式证书机构和单机密钥持有者都会成为自治集群的单点故障源。
- 标题承诺的方法：threshold key management using crypto-asset and multisignature。
- 期望效果：在重编队、子集群、迁移与重组过程中保持密钥管理安全与可协作性。
- 标题与正文的偏差：正文更像“系统级密钥生命周期设计”，而不仅是单一更新协议。

## Algorithm Design 快照
论文针对自治 UAV 集群在远程环境中缺乏可信密钥管理基础设施的问题，提出基于区块链的阈值密钥管理系统。作者把密钥抽象为 crypto-asset，在链上完成登记、更新、撤销与迁移管理，并使用多重签名实现基于阈值的协同授权。该设计可以覆盖集群重增强、子聚类、重合并和跨簇迁移等复杂场景。论文进一步在 OMNET++ 中结合 AODV 和 DSDV 路由协议分析响应时延、丢包、带宽、链上交易与能耗等指标，验证系统在不同拓扑下的安全性和可行性。

## 图1系统框架草案
- 系统实体：工作 UAV、协作 UAV、区块链服务器、阈值签名模块。
- 任务/数据流：密钥更新请求沿集群路径收集同意签名，再提交链上完成状态变更。
- 控制/优化变量：阈值参数 M、拓扑路径、签名收集流程、路由协议选择。
- 约束来源：通信范围、区块链处理吞吐、簇规模、节点能量与安全阈值。
- 画图提醒：图中应突出“链上资产化密钥”和“多重签名授权”的关系。

## System Model
- 每个关键管理操作都需要达到阈值签名数量后才能被链上接受。
- 系统显式考虑最佳/最差拓扑，以及集群增强、子聚类和跨簇迁移等操作。
- 性能分析不仅看网络指标，还看链上交易/区块/UTXO 负载以及 UAV 能耗。
- 路由协议选择会显著影响请求传播、响应时延和最坏情况下的稳定性。

## Algorithm Design 详解
- 第一步把密钥建模为链上的 crypto-asset，并定义其生命周期操作。
- 第二步通过 multisignature 机制实现可配置阈值授权。
- 第三步把 key update、revocation、migration 等关键场景嵌入自治集群流程。
- 第四步在 OMNET++ 中比较 AODV 和 DSDV 下的网络与链上性能。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成自治集群拓扑与通信场景
- 平台与软件：`OMNET++`；`Crypto++`
- 硬件与算力：`Ubuntu 20.04.5 LTS virtual machine`；`Windows 11 PC`；`Intel Core i3 CPU 3.60 GHz`；`8 GB RAM`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：实验平台和密码学配置相对明确，但链上实现与协议代码未公开。

## Introduction 写作素材
- 自治 UAV 集群真正难的不只是通信安全，而是密钥如何在重组、迁移和局部妥协后仍可自治管理。
- 中心化 CA 在远程自治场景里天然脆弱，因此阈值协作和链上治理开始变得重要。
- 这篇论文适合支撑“安全基础设施也是空中自治系统的一部分”的论证。

## Related Work 写作素材
- 与传统中心化密钥管理不同，本文使用区块链和多重签名进行阈值协作。
- 与只关注单次认证的工作不同，本文覆盖密钥更新、撤销和迁移等生命周期问题。
- 与只给安全证明的论文不同，本文还量化了网络、链上和能耗性能。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[阈值密钥管理]]
- [[区块链认证]]
- [[安全与服务保障]]

## 来源
- [原文](../raw/markdown/kharjana2025SecuringAutonomousUAV.md)
