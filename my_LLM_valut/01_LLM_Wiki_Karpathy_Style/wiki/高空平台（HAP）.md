---
tags: [概念, HAP, 空中MEC]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/jia2025DistributionallyRobustOptimization.md
  - ../raw/markdown/nabi2025JointOffloadingDecision.md
  - ../raw/markdown/song2024EnergyefficientTrajectoryOptimization.md
  - ../raw/markdown/zhang2025QuantumassistedOnlineTask.md

---

# 高空平台（HAP）

## 定义
[[高空平台（HAP）]]是部署在高空、具备较稳定覆盖与较大容量算力/回传能力的空中节点，常在空中计算或空中 MEC 中承担上层支撑角色。

## 为什么重要
- HAP 能补足 UAV 在续航、算力稳定性和覆盖半径上的天然短板。
- 它让空中系统从“机动补位”走向“分层基础设施组织”。
- 当任务需求大范围分布且时延要求不允许直接回云时，HAP 是自然的上层中枢。

## 在当前语料中的关键问题
- HAP 与 UAV 的职责如何划分：谁负责接入，谁负责稳定计算与回传。
- HAP 是否还承担空中补能节点，而不只是上层算力和回传支撑。
- 分层体系里，卸载粒度和资源分配是否需要分层设计。
- 当信道不确定、用户动态或业务负载波动时，HAP 的引入是否真正提升系统韧性。
- 在 [[空天地一体网络（SAGIN）]] 中，HAP 如何与 BS、卫星和云共同组成在线服务链路。

## 当前语料中的代表论文
- [[Jia2025_UAV与HAP协同空中MEC的分布鲁棒优化]]：强调 HAP 作为稳定算力层，并在不确定 CSI 下做鲁棒优化。
- [[Nabi2025_UAV与HAP协同层次化空中计算联合卸载]]：强调 GU-UAV-HAP 的层次化空中计算与学习驱动控制。
- [[Song2024_基于多目标强化学习的无线充电UAV辅助MEC轨迹优化]]：强调 HAP 还可以作为空中激光补能层，直接改变 UAV 轨迹目标。
- [[Zhang2025_量子辅助SATIN在线任务卸载与资源分配]]：在 BS-HAP-卫星组成的 SATIN 中把 HAP 作为可选 AP 与计算节点。

## 研究判断
HAP 的出现说明空中计算不再只是“多几架 UAV 怎么协同”，而是开始进入分层平台设计阶段。当前语料又进一步表明，HAP 的角色正在从“稳定算力/回传层”扩展到“空中能量支撑层”。

## 相关页面
- [[层次化空中计算]]
- [[空天地一体网络（SAGIN）]]
- [[任务卸载与资源分配研究主线]]
- [[Jia2025_UAV与HAP协同空中MEC的分布鲁棒优化]]
- [[Nabi2025_UAV与HAP协同层次化空中计算联合卸载]]
- [[Zhang2025_量子辅助SATIN在线任务卸载与资源分配]]

## 来源
- [Jia2025 原文](../raw/markdown/jia2025DistributionallyRobustOptimization.md)
- [Nabi2025 原文](../raw/markdown/nabi2025JointOffloadingDecision.md)
- [Song2024 原文](../raw/markdown/song2024EnergyefficientTrajectoryOptimization.md)
- [Zhang2025 原文](../raw/markdown/zhang2025QuantumassistedOnlineTask.md)
