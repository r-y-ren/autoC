---
tags: [论文, RSMA, 安全波束赋形, UAV部署, 物理层安全]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/wang2025SecureBeamformingDeployment.md
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
platforms: []
frameworks:
  - RSMA
  - SCA
  - AO
hardware_stack: []
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Wang2025_RSMA安全波束赋形与部署协同

## 单行摘要
论文针对被动窃听下的两用户 MISO UAV-RSMA 下行系统，联合优化 UAV-BS 三维部署位置与安全波束赋形，并通过 `SCA + AO` 求解和 `L-RSMA` 算法提升总保密速率。

## 题目驱动研究框架
- 研究场景：RSMA-based UAV 下行通信网络。
- 研究对象：UAV-BS、两名合法用户和被动窃听者。
- 核心问题：UAV 广播链路易被窃听，且 RSMA 的叠加信号与安全设计高度耦合。
- 标题承诺的方法：联合 secure beamforming 与 deployment design。
- 期望效果：在 QoS、功率和飞行空间约束下提升 sum secrecy rate。

## Algorithm Design 快照
这篇论文的关键不是单纯把 RSMA 放到 UAV 上，而是把“公共流既是服务消息也是反窃听扰动工具”这层逻辑写进了联合优化。作者将波束赋形与 UAV 三维部署解耦，再通过 `AO` 在两个子问题之间迭代，从而实现 `L-RSMA` 的联合设计。

## 图1系统框架草案
- 接入层：UAV-BS 面向两个地面用户执行下行服务。
- 编码层：每个用户消息被拆为 common / private 两部分。
- 安全层：公共消息被设计成窃听者不可解码的干扰分量。
- 优化层：同时调整 precoding matrix 与 UAV 三维位置。
- 目标层：最大化总保密速率。

## System Model
### 1. 两用户 MISO RSMA 模型
- UAV-BS 面向两个合法用户广播 common stream 与 private streams。
- 窃听者被动监听 common 与 private 流。

### 2. 信道与部署模型
- UAV 与用户/窃听者之间采用 LoS/NLoS 混合信道。
- UAV 三维位置是显式优化变量。

### 3. 约束条件
- 用户 QoS 约束。
- UAV 最大发射功率约束。
- 飞行空间约束。

## Algorithm Design 详解
### 1. 安全波束赋形
- 设计 common precoder 使窃听者难以解码公共流。
- 让 common stream 同时承担“有效服务 + 无效窃听干扰”的双重角色。

### 2. 部署与波束交替优化
- 首先把原问题拆成波束赋形子问题和部署位置子问题。
- 对两个子问题分别使用 `SCA` 近似凸化，再通过 `AO` 交替更新。

### 3. 研究意义
- 论文说明 RSMA 在 UAV 安全通信中不仅是干扰管理工具，也是一种更灵活的保密机制设计入口。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成 RSMA-UAV 通信场景
- 平台与软件：未明确说明
- 方法组件：`RSMA`、`SCA`、`AO`
- 评测指标：sum secrecy rate
- 对比对象：`L-SDMA`、`L-NOMA`
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露统一代码、平台和训练/求解脚本

## Introduction 写作素材
- UAV 开放广播链路使保密设计不能只依赖传统多址接入方式。
- RSMA 兼具资源共享和干扰管理优势，天然适合被重构为安全通信工具。
- 这篇论文适合支撑“RSMA + UAV + 物理层安全”这条新分支的引言动机。

## Related Work 写作素材
- 过去许多 UAV 安全通信工作聚焦 SDMA、NOMA、IRS 或单纯 beamforming。
- 与只优化速率或能效的 RSMA-UAV 工作不同，这篇论文正面讨论了被动窃听下的部署与波束联合设计。
- 它适合放在“新型多址接入如何进入安全 UAV 通信”的 related work 小节。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[区域覆盖与部署模型]]

## 相关概念与主题页
- [[安全波束赋形]]
- [[速率分裂多址（RSMA）]]
- [[物理层安全]]
- [[无人机部署优化]]
- [[安全与服务保障]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/wang2025SecureBeamformingDeployment.md)
