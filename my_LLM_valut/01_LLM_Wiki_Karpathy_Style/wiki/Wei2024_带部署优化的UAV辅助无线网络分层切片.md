---
tags: [论文, 网络切片, UAV部署, 6G, 分层优化]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/wei2024HierarchicalNetworkSlicing.md
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
platforms: []
frameworks:
  - decomposition technique
  - stochastic game
  - distributed learning
  - two time-scale slicing
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Wei2024 带部署优化的UAV辅助无线网络分层切片

## 单行摘要
论文针对动态环境与不确定流量需求下的 `UAWN`，提出两时间尺度的分层切片框架，在大时间尺度联合优化跨切片资源切分与 UAV 高度部署，在小时尺度通过随机博弈和分布式学习完成切片内资源调整。

## 题目驱动研究框架
- 研究场景：6G 背景下承载差异化业务的 UAV 辅助无线网络。
- 研究对象：UAV/BS、不同业务切片、切片订阅用户、子信道与 UAV 高度。
- 核心问题：单一 UAWN 难以同时满足 `uRLLC` 与 `eMBB` 等差异化服务，而频繁重切片又会带来计算负担。
- 标题承诺的方法：hierarchical network slicing with deployment optimization。
- 期望效果：在动态环境中以较轻量的方式实现差异化服务保障。
- 标题与正文的偏差：正文真正的亮点是“两时间尺度 + 部署优化 + 分布式学习”三者联动，而非单纯的 slice allocation。

## Algorithm Design 快照
论文把切片问题拆成大时间尺度和小时间尺度两层。大时间尺度上，系统以粗粒度决定各切片资源配额和 UAV 高度部署，并将该问题表述为 `MINLP` 再用分解技术求解。小时间尺度上，各切片用户在动态信道与流量条件下通过随机博弈竞争资源，并用轻量分布式学习逼近纯策略纳什均衡。这样，框架既避免了频繁全局重构，又能实时适应环境变化。

## 图1系统框架草案
- 基础设施层：中心 BS + 一个可调高度 UAV 共同覆盖区域。
- 服务层：多个业务切片并行运行，例如 `uRLLC` 与 `eMBB`。
- 上层控制：大时间尺度执行跨切片资源切分与 UAV 高度部署。
- 下层控制：小时间尺度执行切片内子信道与物理资源调整。
- 画图提醒：要把“时间尺度分层”画清楚，否则会误看成普通切片论文。

## System Model
- 系统由地面 BS 与 UAV 共同服务一个圆形区域，UAV 高度位于给定范围内。
- 每个切片包含不同用户集合和 QoS 偏好，服务类型可对应 `uRLLC` 与 `eMBB`。
- 大时间尺度切片变量决定虚拟资源切分与 UAV 部署；小时间尺度变量决定切片内物理资源分配。
- 无线环境采用动态衰落和随机业务到达建模，因此切片调整必须具备在线适应性。

## Algorithm Design 详解
- 首先定义大时间尺度资源切分问题 `RSP`，联合决定切片资源份额和 UAV 高度，并用分解与动态规划求近优结果。
- 然后定义小时间尺度切片调整问题 `SAP`，把切片内资源竞争建模为随机博弈。
- 在博弈层，论文证明了纯策略纳什均衡存在，并给出轻量分布式学习算法 `FDLA` 进行求解。
- 整体框架的价值不只是“切得更细”，而是明确说明在资源受限 UAV 上，切片控制本身必须轻量化、分层化。
- 这篇论文因此非常适合连接 [[网络切片]]、[[无人机部署优化]] 与 6G 差异化服务主线。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成动态无线环境与随机业务需求
- 平台与软件：未明确说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文提供了算法收敛、系统 utility、throughput 与 delay 对比，强调其轻量分布式特性。

## Introduction 写作素材
- UAV 网络若想同时支持多类业务，切片必须进入主问题，而不是停留在通信系统附属层。
- 资源受限 UAV 不适合直接照搬重型 DRL 切片框架，分层和轻量是很重要的系统约束。
- 当部署优化与切片结合时，UAV 高度本身也成为切片质量的一部分。

## Related Work 写作素材
- 传统 RAN slicing 大多基于地面基础设施，UAWN 切片文献数量明显更少。
- 既有 UAV slicing 工作多聚焦单时间尺度或重学习框架，本文强调两时间尺度和轻量分布式学习。
- 若你后续写 `SAGIN/UAWN slicing`，这篇可作为主干代表。

## 相关系统建模页
- [[区域覆盖与部署模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[层次化网络切片]]
- [[网络切片]]
- [[覆盖与部署优化主线]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/wei2024HierarchicalNetworkSlicing.md)
