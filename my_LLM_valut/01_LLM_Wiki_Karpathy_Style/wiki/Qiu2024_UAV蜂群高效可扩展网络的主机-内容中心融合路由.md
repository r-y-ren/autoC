---
tags: [论文, UAV蜂群, FANET, 路由, 内容中心网络]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/qiu2024IntegratedHostContentCentric.md
venue_tier: CCF-A
literature_type: system
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - system_model
  - engineering_context
validation_type:
  - simulation
data_origin:
  - synthetic
platforms:
  - OMNeT++
  - Ubuntu 20.04 LTS
  - VMware ESXi 6.5.0
frameworks:
  - IHCR
  - AODV
  - LFBL
  - AGGR
hardware_stack:
  - Intel Xeon Gold 6148 2.40GHz
  - 260GB RAM
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Qiu2024_UAV蜂群高效可扩展网络的主机-内容中心融合路由

## 单行摘要
论文针对 UAV 蜂群“拓扑并非一直剧烈变化、但也并不稳定”的网络特性，提出 `IHCR` 融合主机中心和内容中心两种路由范式，在包级仿真中显著提升内容共享与节点通信场景下的可扩展性和交付性能。

## 题目驱动研究框架
- 研究场景：多 UAV 蜂群协同执行复杂任务的 `FANET`。
- 研究对象：UAV 消费者、UAV 内容提供者、路由转发机制。
- 核心问题：纯 host-centric 无法适应高动态拓扑，纯 content-centric 又会浪费稳定路径信息。
- 标题承诺的方法：把 host-centric 与 content-centric 路由统一到同一机制中。
- 期望效果：提升包投递率、降低时延，并把可支持网络规模和流量负载显著放大。

## Algorithm Design 快照
这篇论文的价值在于，它没有把 UAV 蜂群路由简单地做成“重新设计一个新协议”，而是先承认两种经典路由范式各有强项，再围绕“何时复用稳定路径、何时快速重路由”构造融合机制。`IHCR` 的核心因此不是某个复杂优化器，而是一组能同时兼容节点身份和内容名称的命名、失败检测和延迟转发机制。

## 图1系统框架草案
- 业务层：既有节点到节点通信，也有内容共享通信。
- 命名层：把节点标识和内容标识统一进 `NID:N` 结构。
- 路由层：稳定路径复用采用 host-centric 思路。
- 转发层：拓扑波动时切换为 content-centric 重路由。
- 性能层：提升 `PDR`、降低时延并扩大可支持网络规模。

## System Model
### 1. UAV 蜂群网络特征
- 拓扑在编队保持时具有短时稳定性，在编队变化时又会快速波动。
- 网络同时承载控制信息、内容共享信息和节点会话信息。

### 2. 两种通信模式
- 节点到节点：例如控制消息、节点访问认证。
- 内容共享：例如位置信息、图像视频或任务内容分发。

### 3. 性能目标
- 在不同流量模式、不同网络规模和不同 UAV 机动强度下提高路由效率。

## Algorithm Design 详解
### 1. 命名与表结构设计
- 用 `NID:N` 同时维护生产者节点身份和内容标识。
- 避免 host-centric 与 content-centric 在命名空间上的直接冲突。

### 2. 路径复用与重路由协同
- 稳定路径下，复用历史路由减少探测泛洪。
- 路由失效时，用内容中心式失败检测和延迟转发机制快速恢复。

### 3. 研究意义
- 论文说明蜂群网络不适合被硬性归类为“稳定 MANET”或“完全机会网络”。
- 它很适合作为“空中通信系统需要同时理解路径稳定性和内容语义”的代表页。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成蜂群网络流量与移动场景
- 平台与软件：`OMNeT++`、`Ubuntu 20.04 LTS`、`VMware ESXi 6.5.0`
- 硬件与算力：`Intel Xeon Gold 6148 @ 2.40 GHz`、`260 GB RAM`
- 方法组件：`IHCR`、`AODV`、`LFBL`、`AGGR`
- 评测指标：`PDR`、包时延、网络规模容量、流量负载容量
- 对比对象：`AODV`、`LFBL`、`AGGR`
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露仿真脚本与配置文件

## Introduction 写作素材
- UAV 蜂群网络既有高动态性，也存在编队保持期的稳定路径，这和传统 MANET 假设并不一致。
- 纯面向节点的路由和纯面向内容的路由都只抓住了问题的一半。
- 这篇论文很适合支持“空中网络需要面向混合业务和混合稳定性来设计”的写作论述。

## Related Work 写作素材
- `AODV` 等 host-centric 路由擅长利用稳定路径，但对高机动拓扑恢复慢。
- `LFBL` 等 content-centric 路由更灵活，但即使有稳定路径也会重复泛洪。
- 本文把两类范式组合起来，适合作为 `FANET` 中融合式网络层设计的代表工作。

## 相关系统建模页
- 当前更偏网络层路由设计，可先参考[[编码缓存与内容命中模型]]理解内容导向的命中与转发逻辑。

## 相关概念与主题页
- [[主机-内容中心融合路由（IHCR）]]
- [[FANET聚类]]
- [[内容缓存]]
- [[空中通信与协同传输]]
- [[多无人机协同]]

## 来源
- [原文](../raw/markdown/qiu2024IntegratedHostContentCentric.md)
