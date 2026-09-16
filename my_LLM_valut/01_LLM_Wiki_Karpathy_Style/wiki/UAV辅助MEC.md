---
tags: [概念, MEC, UAV]
created: 2026-04-06
updated: 2026-04-08
sources:
  - ../raw/markdown/dai2024UAVAssistedTaskOffloading.md
  - ../raw/markdown/chen2025JointTrajectoryOptimization.md
  - ../raw/markdown/wu2025SecurityawareDesignsMultiUAV.md
  - ../raw/markdown/bai2024DelayAwareCooperativeTask.md
  - ../raw/markdown/chen2024AdaptiveBitrateVideo.md
  - ../raw/markdown/chen2025TaskOffloadingResource.md
---

# UAV辅助MEC

## 定义
[[UAV辅助MEC]]指 UAV 作为移动边缘节点、空中服务器、缓存节点或弹性补充算力，与地面边缘设施共同支撑任务执行和资源调度。

## 典型特征
- 地面设施通常仍然存在，或至少是系统设计的一部分。
- UAV 的角色可以是补充算力、改善覆盖、缓解过载、承载缓存服务或提供可售卖的边缘资源。
- 优化问题常表现为[[任务卸载]]、[[资源分配]]、[[轨迹优化]]、缓存/转码和服务定价的联合设计。

## 在当前 wiki 中的代表论文
- [[Dai2024_车联网中的UAV辅助任务卸载]]：UAV 支援过载 RSU。
- [[Chen2025_Lyapunov辅助DRL的轨迹与资源联合优化]]：单UAV 场景下的轨迹与资源联合优化。
- [[Bai2024_多UAV边云协同时延感知任务卸载]]：多UAV 边缘集群与远端云协同卸载。
- [[Chen2024_面向自适应码率视频的UAV辅助MEC鲁棒缓存]]：UAV 上的缓存、转码与回源联合优化。
- [[Chen2025_博弈论驱动的UAV辅助边缘计算卸载与资源定价]]：把卸载与资源定价一起建模。
- [[Wu2025_安全感知的多UAV部署卸载与服务放置]]：带安全和服务放置约束的多UAV MEC。

## 研究重点
- 卸载目的地与比例决策
- 计算/通信/缓存资源协调
- UAV 飞行路径与能量约束
- 安全、服务可得性与价格机制

## 相关页面
- [[空中计算]]
- [[空中计算与UAV辅助MEC的关系]]
- [[任务卸载]]
- [[资源分配]]

## 来源
- [Dai2024 原文](../raw/markdown/dai2024UAVAssistedTaskOffloading.md)
- [Chen2025 原文](../raw/markdown/chen2025JointTrajectoryOptimization.md)
- [Wu2025 原文](../raw/markdown/wu2025SecurityawareDesignsMultiUAV.md)
- [Bai2024 原文](../raw/markdown/bai2024DelayAwareCooperativeTask.md)
- [Chen2024 原文](../raw/markdown/chen2024AdaptiveBitrateVideo.md)
- [Chen2025 定价原文](../raw/markdown/chen2025TaskOffloadingResource.md)
