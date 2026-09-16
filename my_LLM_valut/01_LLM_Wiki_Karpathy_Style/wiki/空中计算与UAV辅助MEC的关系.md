---
tags: [对比, 空中计算, UAV辅助MEC]
created: 2026-04-06
updated: 2026-04-06
sources:
  - ../raw/markdown/zhang2023JointTaskScheduling.md
  - ../raw/markdown/dai2024UAVAssistedTaskOffloading.md
  - ../raw/markdown/chen2025JointTrajectoryOptimization.md
---

# 空中计算与 UAV 辅助 MEC 的关系

| 维度 | [[空中计算]] | [[UAV辅助MEC]] |
|------|---|---|
| 基础设施假设 | 地面设施可能失效或缺位 | 通常仍有地面边缘系统参与 |
| UAV 角色 | 主要计算与服务节点 | 移动辅助节点、空中服务器或补充算力 |
| 典型目标 | 网络重构、任务完成、生存时间 | 卸载收益、覆盖增强、资源协调 |
| 代表论文 | [[Zhang2023_应急通信空中计算联合调度与多UAV部署]] | [[Dai2024_车联网中的UAV辅助任务卸载]], [[Chen2025_Lyapunov辅助DRL的轨迹与资源联合优化]] |

## 判断
两者不是对立关系。更准确地说，[[空中计算]]是系统范式，[[UAV辅助MEC]]是其中更常见也更工程化的一条研究实现路线。

## 对当前知识库的意义
- 这个区分能帮助后续分类文献时不把“基础设施失效应急系统”和“常规边缘计算增强系统”混在一起。
- 它也解释了为什么第一轮论文里会同时出现应急空中计算和车联网/移动用户 MEC 文献。

## 相关页面
- [[空中计算]]
- [[UAV辅助MEC]]
- [[UAC研究路线图]]

## 来源
- [Zhang2023 原文](../raw/markdown/zhang2023JointTaskScheduling.md)
- [Dai2024 原文](../raw/markdown/dai2024UAVAssistedTaskOffloading.md)
- [Chen2025 原文](../raw/markdown/chen2025JointTrajectoryOptimization.md)
