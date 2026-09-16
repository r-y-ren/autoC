---
tags: [论文, 无线供能, 元宇宙, 多UAV, 多任务强化学习]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/wang2024WirelessPoweredMetaverse.md
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
platforms:
  - Python 3.9
frameworks:
  - MURAL
  - PyTorch 1.8.1
  - multi-task DRL
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Wang2024 无线供能元宇宙中的多设备多UAV联合调度

## 单行摘要
论文面向人中心元宇宙应用的无线供能 MEC 场景，联合优化移动设备充电时间、任务调度以及多 UAV 与设备的轨迹设计，并提出多任务深度强化学习算法 MURAL 提升系统计算效率。

## 题目驱动研究框架
- 研究场景：运行元宇宙应用的移动设备计算压力大且能量不足，需要多 UAV 提供无线供能与计算服务。
- 研究对象：多个移动设备、多个 UAV、激光发射器、AP 和元宇宙任务。
- 核心问题：既要给地面设备补能，又要安排 UAV 自身的能量管理和轨迹，单独优化设备端或 UAV 端都不够。
- 标题承诺的方法：joint task scheduling and trajectory design。
- 期望效果：提高系统计算效率，同时在多设备多 UAV 场景下保持可训练的调度复杂度。
- 标题与正文的偏差：正文真正的重点是“无线供能 + 多任务 DRL + 设备与 UAV 双侧调度”，而不是单纯的轨迹规划。

## Algorithm Design 快照
论文研究无线供能移动边缘计算在元宇宙场景下的联合调度问题。移动设备既可本地计算，也可向 UAV 卸载，但设备和 UAV 都受剩余电量约束，且系统还需通过 AP 和激光发射器完成补能。难点在于调度变量跨越设备侧充电、时间分配、UAV 充电调度和双边轨迹设计，组合复杂度极高。为此，作者先用启发式策略完成设备充电时间分配与调度，再用多任务 DRL 学习 UAV 的充电调度和轨迹策略，形成 MURAL。这样系统能够在多设备、多 UAV、动态移动的设置下提升单位时间计算效率。

## 图1系统框架草案
- 系统实体：AP、激光发射器、多架 UAV、多台移动设备。
- 任务/数据流：移动设备先通过 AP/激光补能，再进行本地计算或向 UAV 卸载任务。
- 控制/优化变量：充电时间、设备调度、UAV 调度、UAV 轨迹、设备轨迹。
- 约束来源：设备和 UAV 剩余能量、飞行高度、最大移动速度、计算频率和带宽。
- 画图提醒：图中要把“能量流”和“任务流”分成两类箭头，因为该系统本质上是供能与计算双网络耦合。

## System Model
- 多台移动设备和多架 UAV 都具备计算与能量采集能力，但 UAV 的算力更强。
- AP 和激光发射器为设备与 UAV 提供无线供能，系统允许部分卸载。
- 设备和 UAV 的轨迹共同影响能量获取、通信质量和任务完成率。
- 优化目标是系统计算效率，而不是单纯最小时延或最小能耗。

## Algorithm Design 详解
- 先根据设备剩余能量进行启发式设备调度与充电时间分配。
- 再设计包含共享策略网络与 UAV 专属策略网络的多任务 DRL，学习 UAV 调度和轨迹。
- MURAL 通过交替迭代启发式与 DRL 过程，获得时间分配、UAV 调度和轨迹的联合解。
- 该文说明无线供能场景下，任务调度不能脱离能量补给链路单独设计。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：基于 Manhattan 城市地图和移动模型构建的合成场景
- 平台与软件：`Python 3.9`、`PyTorch 1.8.1`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文清楚给出学习框架与仿真区域设置，但没有披露训练硬件。

## Introduction 写作素材
- 元宇宙场景把“算力不足”和“能量不足”同时放大，因此无线供能与 MEC 需要联合建模。
- 多 UAV 与多设备的联合调度比传统 WPT-MEC 更接近未来沉浸式移动应用。
- 当补能、通信和计算都耦合时，轨迹设计本身就变成资源调度的一部分。

## Related Work 写作素材
- 传统无线供能 MEC 往往只优化设备端或单 UAV 端，缺少多设备多 UAV 联合设计。
- 纯启发式难以适应高维动态场景，而纯 DRL 又难以覆盖所有时隙层决策。
- 该文的价值在于把启发式时间分配与多任务 DRL 进行分层耦合。

## 相关系统建模页
- [[计算卸载模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[无线供能移动边缘计算]]
- [[任务卸载与资源分配研究主线]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/wang2024WirelessPoweredMetaverse.md)
