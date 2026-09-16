---
tags: [概念, 无线充电, 网络]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/wang2025PracticalOptimizingUAV.md
  - ../raw/markdown/song2024EnergyefficientTrajectoryOptimization.md
---

# 无线充电网络（WCN）

## 定义
[[无线充电网络（WCN）]]指系统内存在专门的无线补能设施或链路，使 UAV 或节点在执行任务过程中能够补充能量，从而摆脱一次性电池容量的刚性限制。

## 为什么重要
- 它把“续航约束”从静态预算改写成可规划的网络资源。
- 一旦补能可达，轨迹优化就不再只是最短路径问题，而会变成“访问顺序 + 补能选站 + 任务完成率”的联合问题。
- 对持续作业系统而言，WCN 是从短时任务飞行走向长期任务执行的关键基础设施。

## 当前语料中的代表论文
- [[Wang2025_无线充电网络中具近似保证的实用UAV轨迹优化]]
- [[Song2024_基于多目标强化学习的无线充电UAV辅助MEC轨迹优化]]

## 研究判断
WCN 的引入说明补能不应再被写成背景条件，而应该被视为和路径、任务与服务同层的设计变量。

## 相关页面
- [[无线供能移动边缘计算]]
- [[无人机能耗模型]]
- [[轨迹优化与协同控制]]

## 来源
- [Wang2025 原文](../raw/markdown/wang2025PracticalOptimizingUAV.md)
- [Song2024 原文](../raw/markdown/song2024EnergyefficientTrajectoryOptimization.md)
