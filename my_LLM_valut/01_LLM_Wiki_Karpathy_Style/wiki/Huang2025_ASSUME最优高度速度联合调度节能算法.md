---
tags: [论文, 能耗优化, 高度调度, 速度调度, 数据采集]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/huang2025ASSUMEOptimalAlgorithm.md
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
  - field_test
data_origin:
  - mixed
platforms: []
frameworks: []
datasets:
  - Catalonia water sensor dataset
hardware_stack:
  - 2 kg hexacopter drone
  - Pixhawk 3.6.5
  - Raspberry Pi 3b
  - ACS712 current module
artifact_availability: unknown
reproducibility_level: medium
---

# Huang2025 ASSUME 最优高度速度联合调度节能算法

## 单行摘要
论文基于真实飞行测试建立速度相关能耗模型，并提出 ASSUME 算法联合调度 UAV 高度和速度以最小化数据采集能耗。

## 题目驱动研究框架
- 研究场景：UAV 沿直线监测路径从地面节点收集数据，例如电力线、道路、管线或河岸场景。
- 研究对象：单架 UAV、线性部署的异构地面节点、飞行高度与速度调度。
- 核心问题：在更真实的速度相关能耗模型下，如何联合决定高度、速度与节点切换。
- 标题承诺的方法：an optimal algorithm to minimize UAV energy by altitude and speed scheduling。
- 期望效果：在保证数据采集完成的同时显著降低飞行能耗。
- 标题与正文的偏差：正文真正的亮点是“真实飞行测试 + 动态规划最优算法 + 线上启发式”三位一体。

## Algorithm Design 快照
论文针对 UAV 辅助数据采集场景，指出固定高度和简化能耗模型会错过大量节能空间。作者先通过真实飞行测试拟合出更实际的速度相关能耗函数，再结合一般化地空通信模型，构造 UAV 高度-速度调度与节点传输切换问题。求解上，论文先提出 looking before crossing 算法处理基础速度调度，再通过动态规划扩展为 ASSUME，实现高度与速度联合优化，并补充在线启发式处理未知节点信息场景。

## 图1系统框架草案
- 系统实体：单 UAV、沿直线分布的地面节点、飞行高度层与速度控制。
- 任务/数据流：UAV 沿路径飞行，在不同高度和速度下采集节点数据。
- 控制/优化变量：飞行高度、飞行速度、节点传输切换时机。
- 约束来源：速度相关推进功率、地空通信覆盖、节点异构数据量和线性路径。
- 画图提醒：图里最好把“实测功率曲线”和“时间-距离虚拟房间”同时画出来。

## System Model
- 论文关注线性 GN 部署场景，UAV 只能沿前进方向运动，不能回飞。
- 节点传输效率依赖 UAV 高度，而 UAV 推进能耗依赖飞行速度，因此二者紧耦合。
- 论文忽略无线发送能耗，强调飞行能耗在总能量里占主导。
- 系统模型兼顾真实飞行测试得到的功率曲线与公开真实传感器数据。

## Algorithm Design 详解
- 第一步通过真实飞行测试拟合速度相关能耗模型。
- 第二步在基础情形下提出 looking before crossing 算法处理速度调度。
- 第三步用动态规划扩展为 ASSUME，联合优化高度、速度与节点切换。
- 第四步补充在线启发式算法，处理节点信息不完全已知的场景。

## 实验证据卡片
- 验证类型：数值仿真；真实飞行/现场测试
- 数据来源：真实飞行测试与公开真实传感器数据
- 平台与软件：未说明
- 硬件与算力：`2 kg hexacopter drone`；`Pixhawk 3.6.5`；`Raspberry Pi 3b`；`ACS712 current module`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：这篇论文对“能耗模型必须回到真实飞行测量”这一点特别有价值。

## Introduction 写作素材
- 许多 UAV 优化论文默认能耗与距离或飞行时间线性相关，但真实平台并非如此。
- 高度调度和速度调度一旦耦合，就会把经典轨迹问题推进到更接近工程现实的层面。
- 这篇论文适合用来支撑“真实能耗模型会改变最优调度结构”的论点。

## Related Work 写作素材
- 与固定高度或简化能耗模型的工作不同，本文引入真实飞行测试支持的速度相关模型。
- 与只做路径规划的工作不同，本文强调高度、速度与节点切换三者的联合调度。
- 与纯离线最优不同，本文同时讨论了 agnostic 在线场景。

## 相关系统建模页
- [[无人机能耗模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[高度-速度联合调度]]
- [[轨迹优化与协同控制]]
- [[无人机能耗模型]]

## 来源
- [原文](../raw/markdown/huang2025ASSUMEOptimalAlgorithm.md)
