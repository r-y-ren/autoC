---
tags: [论文, 空地通信, NOMA, 索引调制, 多无人机协同]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/li2025CooperativeNonorthogonalMultiple.md
venue_tier: Unknown
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - theory
validation_type:
  - theory
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks: []
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: low
---

# Li2025_空地多UAV网络中基于索引调制的协作NOMA

## 单行摘要
论文提出 `MCU-NOMA-IM` 与 `MCCU-NOMA-IM`，通过把比特映射到调制符号、子载波索引和能量分配模式，减少多 UAV 空地网络中的 SIC 依赖和用户间干扰，并给出 BER 上界分析。

## 题目驱动研究框架
- 研究场景：地面站与多个 UAV 构成的空地通信网络，要求在有限时频资源下支持多 UAV 接入。
- 研究对象：地面站、多个协作 UAV、NOMA 链路、索引调制、合作转发阶段。
- 核心问题：传统 NOMA 在多 UAV 场景下容易受 inter-user interference 和 SIC 误差地板影响，远端 UAV 可靠性尤其差。
- 具体方法：把 NOMA 与索引调制结合，设计 `MCU-NOMA-IM` 和分簇增强版 `MCCU-NOMA-IM`。
- 期望效果：在 BER、频谱效率和时延之间取得更优折中，尤其提升远端 UAV 的接收可靠性。

## Algorithm Design 快照
本文不是做轨迹或资源优化，而是设计新的物理层协作传输机制。作者把多 UAV 的信息分散编码到多个独立维度，包括调制符号、子载波激活模式以及能量分配模式，使不同 UAV 的信息可以在无需传统 SIC 的情况下被区分和恢复。对于基础版 `MCU-NOMA-IM`，整个合作过程按 `广播 + 多时隙合作` 进行；对于增强版 `MCCU-NOMA-IM`，再把距离相近的 UAV 聚成簇，允许一时隙内支持更多并行协作，从而减少端到端时延。论文同时推导了三 UAV 与四 UAV 场景下的 BER 上界，并用数值仿真验证理论分析。

## 图1系统框架草案
- 系统实体：一个地面站、多个单天线 UAV、广播阶段链路、UAV 间合作链路。
- 任务/数据流：地面站先广播携带多维索引信息的 OFDM-IM 向量；近端 UAV 先解码，再在合作阶段为远端 UAV 转发辅助信息。
- 控制/优化变量：活跃子载波集合、调制符号、能量分配模式、UAV 分簇方式、合作时隙数。
- 约束来源：时隙数量、Nakagami-m 信道条件、准静态 UAV 假设、BER 指标与 SE 目标。
- 画图提醒：要把“广播阶段”和“合作阶段”分层画出，并显式标出近端 UAV 对远端 UAV 的帮助关系。

## System Model
### A. MCU-NOMA-IM 基础系统
- 系统包含一个地面站和 `K` 个 UAV，所有节点单天线，UAV 在一个通信周期内近似准静态。
- 整体传输由一个广播阶段和多个合作阶段组成；文中主要分析 `K=3` 和 `K=4`。

### B. 多维索引调制
- 信息并不只映射到 PSK/QAM 符号，还映射到子载波激活模式 `SAP` 和能量分配模式 `EAP`。
- 通过不同信息维度承载不同 UAV 的数据，可在一定程度上避免传统 NOMA 的强干扰与 SIC 依赖。

### C. 合作阶段
- 近端 UAV 在接收到广播信号后，重构辅助向量并转发给更远端 UAV。
- 因而远端 UAV 的 BER 由“直达链路 + 合作链路”共同决定。

### D. MCCU-NOMA-IM 分簇增强
- 当 UAV 数量变大时，普通 MCU-NOMA-IM 需要过多合作时隙。
- MCCU-NOMA-IM 通过把距离相近 UAV 进行分簇，在减少合作时隙的同时保持索引调制带来的 BER 优势。

## Algorithm Design 详解
- 第一步是信号构造：把不同 UAV 的比特映射到调制符号、SAP 和 EAP 等不同维度。
- 第二步是广播阶段检测：近端 UAV 基于 ML 检测恢复相关索引与符号。
- 第三步是合作阶段重构：近端 UAV 根据已恢复信息生成合作向量，帮助远端 UAV 进一步检测。
- 第四步是理论分析：分别对三 UAV 和四 UAV 场景推导 BER 上界。
- 第五步是时延改造：提出分簇版 `MCCU-NOMA-IM`，用 `J+1` 个时隙替代基础方案随 UAV 数线性增长的合作时隙需求。

## 实验证据卡片
- 验证类型：理论分析 + 数值仿真
- 数据来源：合成场景
- 平台与软件：未说明
- 硬件与算力：未说明
- 评测指标：BER、SNR 增益、理论-仿真匹配程度、时隙数量/端到端时延
- 对比基线：`MCU-NOMA`、`NC-MU-NOMA-IM`
- 开源情况：未说明
- 复现判断：`low`
- 证据备注：理论推导完整，但实验更偏数值验证，缺少实现栈和代码资产。

## Introduction 写作素材
- 在多 UAV 空地通信中，频谱紧张与干扰问题并不天然意味着必须依赖传统 SIC-NOMA。
- 如果能把信息映射到多个独立维度，空地协作系统就有机会同时改善干扰管理和远端链路可靠性。
- 这篇论文适合支撑“物理层调制设计本身也能重塑多 UAV 协作方式”的论述。

## Related Work 写作素材
- 与传统 cooperative NOMA 相比，本文利用索引调制减少了对 SIC 的依赖。
- 与只分析单 UAV 或双用户 NOMA 的工作相比，本文显式面向多 UAV 协作场景。
- 与只关注 BER 而不考虑时隙扩展的机制相比，本文进一步提出分簇版 `MCCU-NOMA-IM` 来回应时延问题。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[多无人机协同]]
- [[索引调制]]
- [[空中通信与协同传输]]
- [[Hoang2024_有限块长NOMA多用户配对UAV系统性能分析与优化]]

## 来源
- [原文](../raw/markdown/li2025CooperativeNonorthogonalMultiple.md)
