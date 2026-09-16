---
tags: [论文, 多UAV网络, 虚拟网络功能, 网络设计]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/wu2024MultiUAVsNetworkDesign.md
venue_tier: CCF-A
literature_type: system
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - system_model
  - methodology
validation_type:
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks:
  - S-MILP
  - NS-MILP
  - RALS
  - RAPLS
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Wu2024_面向计算流最大化的多UAV网络设计

## 单行摘要
论文研究多 UAV 网络中“放置 UAV、部署 VNF、路由未处理/已处理流”的联合设计问题，并通过 MILP 与启发式算法最大化源宿对之间的最小计算流率。

## 题目驱动研究框架
- 研究场景：多架 UAV 作为空中骨干网络，为地面源宿节点对提供通信与计算服务。
- 研究对象：UAV 位置、VNF 部署、未处理流与已处理流路由路径。
- 核心问题：在通信与计算资源同时受限时，如何构建一个公平且高效的多 UAV 计算网络。
- 标题承诺的方法：multi-UAV network design algorithms for computed rate maximization。
- 期望效果：最大化所有源宿对中的最小已计算流率，并降低求解时间。

## Algorithm Design 快照
论文把问题表述得很“网络系统化”：不是单独优化路由，也不是单独做 UAV 部署，而是把[[虚拟网络功能（VNF）]]部署、UAV 选址和处理前/处理后流量路由统一起来。S-MILP 和 NS-MILP 分别对应可分流与不可分流模型；RALS 与 RAPLS 则在不穷举全部拓扑的情况下近似寻找高质量解。这使论文非常适合支撑“UAV 集群可以被当作可计算网络基础设施来设计”的系统范式判断。

## 图1系统框架草案
- 地面层：多个固定源宿节点对产生业务流。
- 空中层：多架 UAV 组成骨干拓扑。
- 功能层：UAV 上承载多个 VNF 实例。
- 路由层：业务流分为未处理流和已处理流。
- 优化层：联合决定 UAV 位置、VNF 指派与路由路径。
- 目标层：最大化最小计算流率。

## System Model
### 1. 多 UAV 计算骨干
- UAV 不仅提供转发，还提供 VNF 处理能力。
- 每个源宿对的流量必须在到达目的地前经过所需 VNF 处理。

### 2. 流模型
- 可分流模型允许一个业务拆分到多路径。
- 不可分流模型要求单一路径完成传输与处理。

### 3. 优化目标
- 最大化 max-min computed flow。
- 在此过程中同时满足链路容量与计算资源约束。

## Algorithm Design 详解
### 1. S-MILP / NS-MILP
- 精确建模 UAV 选址、VNF 分配、流路由与链路共享。
- 给出不同流模型下的理论上界。

### 2. RALS / RAPLS
- 避免穷举所有拓扑组合。
- 通过资源感知的位置选择和路径选择寻找高质量近似解。

### 3. 研究意义
- 这篇论文不以传统 QoS 指标为唯一目标，而以“最小已计算流率”衡量网络公平性。
- 它把 UAV 网络从覆盖平台推进成了可编排的[[虚拟网络功能（VNF）]]基础设施。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成源宿对与候选拓扑场景
- 平台与软件：未明确说明
- 方法组件：`S-MILP`、`NS-MILP`、`RALS`、`RAPLS`
- 对比对象：精确求解与启发式近似解
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露统一求解器平台与代码环境

## Introduction 写作素材
- 多 UAV 网络不只是在空中“连起来”，更可以在空中“算起来”。
- 当 UAV 承载 VNF 后，网络拓扑、计算资源与流量路径需要被统一设计。
- 这篇论文适合支撑“空中网络基础设施化与服务链化”的引言论述。

## Related Work 写作素材
- 传统 VNF 放置与路由大多假设网络拓扑固定。
- 传统 UAV 网络设计又往往忽略处理前/处理后流量和 VNF 结构。
- 这篇论文把两者真正联到了一起，是网络设计视角下的一篇代表论文。

## 相关系统建模页
- [[服务放置模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[虚拟网络功能（VNF）]]
- [[多无人机协同]]
- [[空中通信与协同传输]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [原文](../raw/markdown/wu2024MultiUAVsNetworkDesign.md)
