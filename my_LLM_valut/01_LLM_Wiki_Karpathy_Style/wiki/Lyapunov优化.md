---
tags: [概念, Lyapunov优化, 在线控制]
created: 2026-04-06
updated: 2026-04-06
sources:
  - ../raw/markdown/dai2024UAVAssistedTaskOffloading.md
  - ../raw/markdown/chen2025JointTrajectoryOptimization.md
---

# Lyapunov优化

## 定义
[[Lyapunov优化]]是一类处理长期约束和随机到达过程的在线优化方法，常用来把长期平均约束转化成逐时隙可求解的问题。

## 在当前语料中的作用
- [[Dai2024_车联网中的UAV辅助任务卸载]]：把 UAV 长期能量预算转化为在线可控的能量赤字队列问题。
- [[Chen2025_Lyapunov辅助DRL的轨迹与资源联合优化]]：先用 Lyapunov 解耦长期随机问题，再把部分子问题交给 DRL 或凸优化。

## 为什么重要
- 它非常适合处理任务到达随机、用户移动随机、能量预算长期受限的 UAC 场景。
- 它为“学习方法 + 解析方法”的混合框架提供了稳定骨架。
- 相比完全依赖离线优化，它更接近真实在线系统。

## 相关页面
- [[任务卸载]]
- [[深度强化学习]]
- [[Chen2025_Lyapunov辅助DRL的轨迹与资源联合优化]]
- [[Dai2024_车联网中的UAV辅助任务卸载]]

## 来源
- [Dai2024 原文](../raw/markdown/dai2024UAVAssistedTaskOffloading.md)
- [Chen2025 原文](../raw/markdown/chen2025JointTrajectoryOptimization.md)
