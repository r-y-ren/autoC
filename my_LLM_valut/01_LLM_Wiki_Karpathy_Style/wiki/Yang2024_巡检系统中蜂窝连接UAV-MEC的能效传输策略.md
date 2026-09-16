---
tags: [论文, 巡检系统, 蜂窝连接UAV, MEC, 能效传输]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/yang2024EnergyEfficientTransmission.md
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
  - SCA
  - BCD
  - weighted graph ordering
hardware_stack: []
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Yang2024_巡检系统中蜂窝连接UAV-MEC的能效传输策略

## 单行摘要
论文面向蜂窝连接 UAV 巡检系统，在多预设巡检点之间联合优化访问顺序、任务完成时间、通信调度、计算资源分配和 UAV 轨迹，以最小化总体能耗。

## 题目驱动研究框架
- 研究场景：UAV 沿既定巡检点执行数据采集并向地面基站卸载计算任务。
- 研究对象：蜂窝连接 UAV、多个巡检点、地面基站 `GBSs` 与 MEC 资源。
- 核心问题：巡检路径、通信时机和计算卸载共同决定能耗与任务完成时长。
- 标题承诺的方法：设计 energy efficient transmission strategy。
- 期望效果：在巡检约束下同时降低 UAV 飞行与传输能耗。

## Algorithm Design 快照
这篇论文的关键不在单一轨迹优化，而在“先排顺序，再做段间传输策略”。作者先根据巡检点和基站的通信拓扑构造加权边，再决定巡检顺序；随后在相邻巡检点之间联合优化 UAV 轨迹、通信调度和计算资源分配。这样做让巡检业务中的“离散访问顺序”和“连续传输控制”被拆成两个可协同的问题。

## 图1系统框架草案
- 任务层：UAV 依次访问多个巡检点执行数据采集。
- 连接层：UAV 与地面基站保持蜂窝连接并进行任务卸载。
- 规划层：先优化巡检点访问顺序，再优化段间传输策略。
- 资源层：联合调度通信时机、计算资源与 UAV 轨迹。
- 目标层：最小化总能耗。

## System Model
### 1. 巡检与卸载模型
- UAV 需要遍历多个预设巡检点完成数据采集。
- 采集后任务可卸载给邻近 `GBS` 的 MEC 资源处理。

### 2. 双子问题结构
- 子问题一：巡检点遍历顺序设计。
- 子问题二：相邻巡检点之间的通信传输与轨迹联合设计。

### 3. 目标函数
- 最小化飞行、通信和计算相关总能耗。
- 同时满足任务完成时间与连接约束。

## Algorithm Design 详解
### 1. 巡检顺序设计
- 结合通信速率表现和巡检点-基站拓扑构造加权边。
- 使巡检顺序兼容轻任务与重任务卸载场景。

### 2. 段间传输优化
- 用 `SCA` 和 `BCD` 联合更新 UAV 轨迹与无线资源分配。
- 兼顾数据上传、任务处理与下一段飞行准备。

### 3. 研究意义
- 论文把“蜂窝连接 UAV”从单纯链路保持问题推进到“巡检顺序 + 传输策略 + MEC”一体化问题。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成巡检点与地面基站部署场景
- 平台与软件：未明确说明
- 方法组件：`SCA`、`BCD`、`weighted graph ordering`
- 评测指标：总能耗、任务完成时间、传输效率
- 对比对象：round tour、穷举最优或传统巡检传输方案
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露代码、求解器和统一仿真平台

## Introduction 写作素材
- 巡检 UAV 的瓶颈不仅来自飞行距离，还来自持续的数据上传和 MEC 卸载过程。
- 蜂窝连接 UAV 与传统空中基站问题不同，更强调任务执行路径上的持续连接质量。
- 这篇论文适合支撑“业务驱动的 UAV-MEC 需要离散调度与连续控制共同设计”的引言表述。

## Related Work 写作素材
- 既有蜂窝连接 UAV 研究常聚焦覆盖或中断时间。
- 既有 MEC 研究则更多关注静态任务卸载和资源分配。
- 本文的代表性在于把巡检次序、传输和卸载一并写进能耗主目标中。

## 相关系统建模页
- [[计算卸载模型]]
- [[无人机能耗模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[蜂窝连接无人机通信]]
- [[任务卸载]]
- [[任务卸载与资源分配研究主线]]
- [[轨迹优化]]
- [[无人机能耗模型]]

## 来源
- [原文](../raw/markdown/yang2024EnergyEfficientTransmission.md)
