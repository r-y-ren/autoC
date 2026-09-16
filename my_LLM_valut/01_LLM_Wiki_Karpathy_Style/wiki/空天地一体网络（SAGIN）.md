---
tags: [概念, SAGIN, 空天地一体]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/he2024BalancingTotalEnergy.md
  - ../raw/markdown/chen2025MultiuserTaskOffloading.md
  - ../raw/markdown/tun2025JointUAVDeployment.md
  - ../raw/markdown/zhang2025QuantumassistedOnlineTask.md

---

# 空天地一体网络（SAGIN）

## 定义
[[空天地一体网络（SAGIN）]]是把卫星、空中平台和地面网络统一到同一通信与计算体系中的多域协同网络架构。

## 为什么重要
- 它提供比传统地面网络更广的覆盖范围与更强的弹性。
- 任务可以在不同域之间迁移或卸载，使系统不再局限于地面边缘节点。
- 一旦进入 SAGIN，链路异构性、调度跨度和功耗权衡都会明显增强。

## 在当前语料中的关键问题
- 任务在星间链路、星地链路和空地链路之间如何调度。
- 总能耗、平均工期和长期服务时延如何折中。
- 卫星、空中和地面节点的能力如何统一建模，并在线求解大规模随机优化问题。
- 太赫兹空口与 UAV 部署是否应被视为 SAGIN 卸载问题的一部分，而不是独立通信子问题。

## 当前语料中的代表论文
- [[He2024_空天地一体网络数据卸载中的总能耗与平均工期权衡]]：从调度与功率控制角度平衡总能耗与平均工期。
- [[Chen2025_空天地一体LEO卫星边缘计算多用户卸载]]：把卫星边缘算力显式纳入卸载目的地集合。
- [[Tun2025_THz辅助空天地一体网络中的UAV部署与资源分配]]：把 THz 接入、UAV 协作部署与卫星计算链路统一到同一优化框架。
- [[Zhang2025_量子辅助SATIN在线任务卸载与资源分配]]：在 MEC-enabled SATIN 中用 [[量子辅助优化]] 加速逐时隙在线卸载求解。

## 研究判断
SAGIN 让 UAC 研究从“空地协同”继续推进到真正的跨域资源组织与卸载体系。最新语料进一步显示，THz 接入、UAV 部署和卫星协作已经开始在同一系统问题里被联合处理。

## 相关页面
- [[低轨卫星边缘计算]]
- [[高空平台（HAP）]]
- [[THz辅助空天地一体网络]]
- [[量子辅助优化]]
- [[计算卸载模型]]
- [[He2024_空天地一体网络数据卸载中的总能耗与平均工期权衡]]
- [[Tun2025_THz辅助空天地一体网络中的UAV部署与资源分配]]
- [[Zhang2025_量子辅助SATIN在线任务卸载与资源分配]]

## 来源
- [He2024 原文](../raw/markdown/he2024BalancingTotalEnergy.md)
- [Chen2025 原文](../raw/markdown/chen2025MultiuserTaskOffloading.md)
- [Tun2025 原文](../raw/markdown/tun2025JointUAVDeployment.md)
- [Zhang2025 原文](../raw/markdown/zhang2025QuantumassistedOnlineTask.md)
