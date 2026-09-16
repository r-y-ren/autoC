---
tags: [概念, PPO, 强化学习]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/lin2024LyapunovbasedApproachJoint.md
  - ../raw/markdown/wang2025JointPositioningComputation.md
  - ../raw/markdown/wang2025JointTaskOffloading.md
---

# 近端策略优化（PPO）

## 定义
[[近端策略优化（PPO）]]是一类通过裁剪策略更新幅度来稳定策略梯度训练的强化学习算法，常用于连续动作或高维控制问题。

## 为什么重要
- UAV 场景中的放置、轨迹和资源控制常包含连续动作。
- PPO 在稳定性和实现复杂度之间取得了较好平衡。
- 它既可以直接求策略，也可以作为专家策略生成器服务于模仿学习。

## 当前语料中的代表论文
- [[Huang2024_LI2灾后PoI及时监测的UAV_AoI路径优化]]
- [[Wang2025_PPO驱动的多UAV_MEC联合定位与计算卸载]]
- [[Wang2025_动态UAV_MEC网络中的任务卸载与迁移优化]]

## 研究判断
PPO 在当前语料里已经从“一个常用 DRL 算法”扩展为多种框架中的稳定策略核心。

## 相关页面
- [[深度强化学习]]
- [[模仿学习]]

## 来源
- [Lin/Huang2024 原文](../raw/markdown/lin2024LyapunovbasedApproachJoint.md)
- [Wang2025 Positioning 原文](../raw/markdown/wang2025JointPositioningComputation.md)
- [Wang2025 Migration 原文](../raw/markdown/wang2025JointTaskOffloading.md)
