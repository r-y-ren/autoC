---
tags: [论文, FANET, MAC协议, 协作传输, 能耗优化]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/wu2024MACOptimizationProtocol.md
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
  - MATLAB
frameworks:
  - EC-CMAC
  - cooperative transmission
  - relay selection
hardware_stack: []
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Wu2024_双感知能耗与信道增益的协作UAV-MAC优化协议

## 单行摘要
论文面向恶劣环境和高速机动下的 `FANET` 通信，提出兼顾能耗与信道增益的协作 `MAC` 协议 `EC-CMAC`，通过发射功率估计、候选中继选择和传输模式自适应切换提升网络寿命与包投递率。

## 题目驱动研究框架
- 研究场景：重雾、浓烟和高速机动等恶劣环境下的 `FANET`。
- 研究对象：多 UAV 节点、链路层转发、中继选择与 MAC 竞争机制。
- 核心问题：高动态和恶劣信道下，传统 MAC 难同时兼顾可靠性、时延和能源寿命。
- 标题承诺的方法：基于双感知能耗与信道增益的 MAC 优化协议。
- 期望效果：以较小吞吐和时延代价提升网络寿命与传输成功率。

## Algorithm Design 快照
这篇论文的重心在链路层，而不是常见的网络层路由。作者首先用信道传播模型估计发射功率，再综合节点剩余能量、信道增益、节点方向和位置来选中继，最后在直接传输和协作传输之间自适应切换。它的价值在于提醒我们：蜂群通信性能并不只由路由决定，MAC 级协作同样能显著塑造网络寿命。

## 图1系统框架草案
- 感知层：估计链路信道增益与所需发射功率。
- 节点状态层：感知中继候选节点的残余能量、方向和位置。
- MAC 决策层：判断采用直接传输还是协作传输。
- 协作层：从一跳邻居中选取合适中继执行转发。
- 目标层：降低能耗、延长寿命并提升包传输成功率。

## System Model
### 1. FANET 恶劣环境模型
- UAV 节点在无基础设施环境下自组织成多跳网络。
- 信道衰落、机动性和环境遮挡共同影响链路稳定性。

### 2. 协作 MAC 设计目标
- 面向链路层而不是网络层进行转发模式优化。
- 兼顾节点残余能量与当前信道质量。

### 3. 性能关注点
- 网络寿命、端到端时延、吞吐、包传输率。

## Algorithm Design 详解
### 1. 发送功率与中继选择
- 先依据传播模型估计发送功率需求。
- 再综合残余能量、方向、位置和信道增益选择中继节点。

### 2. 传输模式切换
- 在直接传输与协作转发之间自适应切换。
- 通过一跳邻居转发降低恶劣链路下的数据包失败率。

### 3. 研究意义
- 论文很适合支撑“空中网络不应只停留在路由层，还要向 MAC 层要性能”的论述。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成恶劣传输环境与高速机动场景
- 平台与软件：`MATLAB`
- 方法组件：`EC-CMAC`、`cooperative transmission`、`relay selection`
- 评测指标：端到端时延、吞吐、网络寿命、包传输率
- 对比对象：传统 MAC 或非协作转发协议
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露协议实现代码和参数脚本

## Introduction 写作素材
- 在灾后通信和恶劣环境下，链路层协作比单纯增大发射功率更可持续。
- UAV 蜂群网络的寿命问题往往与链路层竞争和中继策略直接相关。
- 这篇论文适合用来说明“空中通信的性能瓶颈并不只在物理层和网络层”。

## Related Work 写作素材
- 既有 `AODV/OLSR` 等方案偏重网络层路径选择。
- 传统 `TDMA/CSMA` 协议又往往忽略 UAV 特有的机动性与能量约束。
- 本文通过 `EC-CMAC` 把能耗感知和信道增益感知同时拉进 MAC 决策。

## 相关系统建模页
- [[无人机能耗模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[协作MAC协议]]
- [[抗干扰通信]]
- [[空中通信与协同传输]]
- [[多无人机协同]]
- [[无人机能耗模型]]

## 来源
- [原文](../raw/markdown/wu2024MACOptimizationProtocol.md)
