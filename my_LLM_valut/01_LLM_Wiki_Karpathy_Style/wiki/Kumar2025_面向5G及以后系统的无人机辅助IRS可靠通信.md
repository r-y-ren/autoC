---
tags: [论文, IRS, 可靠通信, 能量收集, 理论分析]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/kumar2025DroneassistedIRSSystem.md
venue_tier: CCF-A
literature_type: theory
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - system_model
  - idea_seed
validation_type:
  - theory
  - simulation
data_origin:
  - synthetic
platforms:
  - MATLAB
frameworks: []
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---


# Kumar2025 面向5G及以后系统的无人机辅助IRS可靠通信

## 单行摘要
论文构建了无人机辅助 IRS 的 D2D 通信模型，用高度相关 Nakagami-m 信道和机载能量收集机制联合分析可靠性与网络寿命。

## 题目驱动研究框架
- 研究场景：基础设施缺失条件下的 5G/B5G D2D 可靠通信。
- 研究对象：发射端、接收端、携带 IRS 的无人机、DF/AF 中继与能量收集机制。
- 核心问题：在高度变化导致小尺度和大尺度衰落都变化时，如何同时提升可靠性与网络寿命。
- 标题承诺的方法：drone-assisted IRS system improving reliability and network life span。
- 期望效果：降低中断概率、提升频谱效率，并延长网络可持续工作时长。
- 标题与正文的偏差：正文的亮点更偏向“高度相关信道 + 能量收集 + 可靠性闭式分析”，而非一般意义上的 IRS 部署优化。

## Algorithm Design 快照
论文面向无基础设施场景下的 D2D 通信，提出由无人机携带 IRS 的双路径可靠通信架构。作者使用高度相关的 Nakagami-m 小尺度衰落与高度相关路径损耗指数，统一描述无人机高度变化对链路可靠性的影响；同时设计面向机载 IRS 的动态功率分配与能量收集机制，让无人机既能为 IRS 供能，又能延长网络寿命。在此基础上，论文分别推导 DF 和 AF 中继下的端到端 SNR、频谱效率和中断概率闭式表达，并用 Monte-Carlo 仿真验证理论结果。

## 图1系统框架草案
- 系统实体：地面发射端、地面接收端、无人机中继、机载 IRS、能量收集模块。
- 任务/数据流：发射信号可经 IRS 反射或经无人机中继到达接收端，接收端做选择合并。
- 控制/优化变量：无人机高度、功率分配、DF/AF 中继方式、能量收集比例。
- 约束来源：Nakagami-m 衰落、LoS/NLoS 路损、IRS 供能需求、固定中继功率。
- 画图提醒：图中应明确展示“IRS 路径”和“无人机中继路径”同时存在，并标出能量分流结构。

## System Model
- 直达地面链路处于深衰落，系统依赖无人机和机载 IRS 形成双路径辅助通信。
- 无人机高度同时影响 Nakagami-m 形状参数和大尺度路损指数，因此可靠性随高度非单调变化。
- 能量收集模块从接收信号中提取能量，一部分供 IRS 元件工作，另一部分用于无人机处理。
- 理论分析重点在 DF/AF 两类中继及其对中断概率和寿命的影响。

## Algorithm Design 详解
- 第一步构建高度相关 Nakagami-m 衰落和高度相关路径损耗模型。
- 第二步设计无人机侧的功率分流与 IRS 供能机制。
- 第三步分别推导 DF/AF 中继下的端到端 SNR、频谱效率和中断概率闭式结果。
- 第四步用 Monte-Carlo 仿真验证理论表达式并比较不同高度与发射功率设置。

## 实验证据卡片
- 验证类型：理论推导；数值仿真
- 数据来源：合成通信参数场景
- 平台与软件：`MATLAB`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：理论链条完整，且明确用 Monte-Carlo 仿真验证，但工程实现仍停留在建模层。

## Introduction 写作素材
- 当直达链路深衰落时，单纯依赖 IRS 或单纯依赖中继都不够，双路径辅助机制更稳健。
- 无人机高度不只是几何变量，还会改变小尺度和大尺度衰落结构。
- 这篇论文适合支撑“高度相关信道建模会改变最佳空中部署判断”的写作论点。

## Related Work 写作素材
- 与传统 IRS 工作不同，本文把机载 IRS 的供能问题显式纳入系统设计。
- 与只用 LoS/Rayleigh 极端模型的分析相比，本文使用高度相关 Nakagami-m 模型覆盖更广场景。
- 与只分析可靠性的论文不同，本文还把网络寿命和能量收集耦合进来。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[无人机辅助IRS通信]]
- [[RIS辅助通信]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/kumar2025DroneassistedIRSSystem.md)
