---
tags: [概念, 强化学习, 多目标优化]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/song2024EnergyefficientTrajectoryOptimization.md
---

# 多目标强化学习（MORL）

## 定义
[[多目标强化学习（MORL）]]是在强化学习中保留多个互相冲突目标的独立奖励分量，并学习能够随偏好变化而切换的策略表示，而不是先把所有目标强行压缩成单一标量奖励。

## 为什么重要
- UAV 系统里常见的时延、能耗、吞吐、AoI、覆盖率往往天然冲突。
- 若过早线性加权，策略只对某组固定偏好有效。
- MORL 更适合“同一系统、不同任务阶段偏好变化”的场景。

## 当前语料中的代表论文
- [[Song2024_基于多目标强化学习的无线充电UAV辅助MEC轨迹优化]]

## 研究判断
MORL 是把“算法输出一个最优解”推进到“算法输出一条偏好可调解族”的关键方法层。

## 相关页面
- [[深度强化学习]]
- [[轨迹优化与协同控制]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [Song2024 原文](../raw/markdown/song2024EnergyefficientTrajectoryOptimization.md)
