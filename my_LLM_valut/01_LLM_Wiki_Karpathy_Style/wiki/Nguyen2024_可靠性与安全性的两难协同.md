---
tags: [论文, 可靠性, 安全性, 能量采集, 友好干扰]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/nguyen2024DilemmaReliabilitySecurity.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - system_model
validation_type:
  - theory
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks:
  - exact analysis
  - approximate analysis
  - NSGA-II
hardware_stack: []
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Nguyen2024_可靠性与安全性的两难协同

## 单行摘要
论文研究能量采集中继辅助的 UAV-地面通信系统，在 outage probability 与 intercept probability 之间建立显式双目标权衡，并用 `NSGA-II` 联合优化 UAV 位置与时间切换比。

## 题目驱动研究框架
- 研究场景：UAV-地面网络中，专用 power beacon 为中继供能。
- 研究对象：UAV、能量采集中继、地面终端、窃听者与 power beacon。
- 核心问题：中继和能量采集提升可靠性，但也可能放大窃听暴露面。
- 标题承诺的方法：在 reliability 与 security 的两难关系中做联合优化。
- 期望效果：同时降低中断概率与截获概率，而不是只优化单一指标。

## Algorithm Design 快照
这篇论文的价值不在复杂学习器，而在把“可靠性提升是否反而削弱安全性”变成一个可解析、可求解的双目标问题。作者推导了 OP 与 IP 的精确/近似表达式，然后用 `NSGA-II` 在 UAV 位置与时间切换比之间搜索 Pareto 折中解。

## 图1系统框架草案
- 供能层：power beacon 为中继提供能量采集支持。
- 传输层：UAV 通过中继向地面终端完成双跳传输。
- 干扰层：power beacon 向窃听者持续发射人工噪声。
- 分析层：推导 OP 与 IP 的精确和近似表达。
- 优化层：以 UAV 位置和 TS 比为变量做双目标搜索。

## System Model
### 1. 三阶段链路模型
- 第一阶段用于能量采集。
- 第二阶段 UAV 向中继发送信息，同时窃听者尝试截获。
- 第三阶段中继转发给终端，power beacon 持续发射人工噪声压制窃听。

### 2. 可靠性与安全性指标
- 可靠性由 `outage probability (OP)` 表征。
- 安全性由 `intercept probability (IP)` 表征。

### 3. 优化变量
- UAV 空间位置。
- 时间切换比 `TS ratio`。

## Algorithm Design 详解
### 1. 数学分析
- 推导 OP 与 IP 的精确表达式和闭式近似。
- 显式刻画能量采集、人工噪声和双跳中继对主链路与窃听链路的共同影响。

### 2. 双目标优化
- 以联合最小化 OP 与 IP 为目标构造 `MOOP`。
- 用 `NSGA-II` 搜索次优 Pareto 前沿。

### 3. 研究意义
- 论文提醒我们，UAV 中继、EH 和友好干扰并不自动带来“又可靠又安全”的结果，必须正面处理两类目标之间的结构冲突。

## 实验证据卡片
- 验证类型：`theory`、`simulation`
- 数据来源：合成参数化无线场景
- 平台与软件：未明确说明
- 方法组件：精确/近似概率分析、`NSGA-II`
- 评测指标：`OP`、`IP`、Pareto 折中性能
- 对比对象：单目标或非联合优化方案
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未公开统一仿真脚本和平台栈

## Introduction 写作素材
- UAV 中继和能量采集常被视为提升可靠性的自然手段，但安全性代价往往被低估。
- 当窃听者也能利用双跳结构与 LoS 条件时，系统必须同时对可靠性和安全性负责。
- 这篇论文适合支撑“安全与可靠性不能分开写”的问题动机。

## Related Work 写作素材
- 许多工作只分析 SOP、SR 或 OP 中的某一个指标。
- 与只做 secrecy rate 最大化的研究不同，这篇论文强调可靠性-安全性的双目标 Pareto 结构。
- 它也说明友好干扰和 EH 设计需要放到统一系统模型中讨论。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[可靠性-安全性权衡]]
- [[友好干扰]]
- [[物理层安全]]
- [[可靠性感知卸载]]
- [[安全与服务保障]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/nguyen2024DilemmaReliabilitySecurity.md)
