---
tags: [论文, 空中MEC, HAP, 分布鲁棒优化, CVaR]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/jia2025DistributionallyRobustOptimization.md
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
platforms: []
frameworks: []
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---


# Jia2025 UAV与HAP协同空中MEC的分布鲁棒优化

## 单行摘要
论文构建了 HAP 与多 UAV 组成的分层空中 MEC 体系，并用 CVaR 驱动的分布鲁棒优化处理 CSI 不确定性下的能量最小化问题。

## 题目驱动研究框架
- 研究场景：UAV 与 HAP 协同提供空中多接入边缘计算服务。
- 研究对象：地面用户、多 UAV、一个 HAP、无线链路不确定性与分层计算资源。
- 核心问题：在 CSI 存在误差和机会约束存在不确定性的情况下，如何稳定地完成卸载与资源配置。
- 标题承诺的方法：distributionally robust optimization for aerial MEC。
- 期望效果：在不确定环境里降低总能耗并提升可服务用户数。
- 标题与正文的偏差：正文的另一个亮点是把 UAV 部署、分层算力分配和二元卸载决策放进同一层级模型。

## Algorithm Design 快照
论文提出由一个高空平台 HAP 和多架 UAV 组成的层次化空中 MEC 系统，其中 HAP 提供稳定的大容量算力，UAV 提供灵活接入。考虑实际环境中 CSI 估计误差引起的约束不确定性，作者把总能耗最小化问题写成带机会约束的混合整数非线性规划。为此，论文先用加权 K-means 优化 UAV 部署，再借助 CVaR 机制把机会约束转化为分布鲁棒约束，并进一步重写为 MISOCP；随后通过原始分解与二元鲸鱼优化算法求解资源分配和离散决策，最终获得近最优且更稳健的空中 MEC 方案。

## 图1系统框架草案
- 系统实体：地面用户、多架 UAV、一个 HAP、分层回传与计算链路。
- 任务/数据流：任务先通过 G2U 链路进入 UAV，再根据资源状况在 UAV 或 HAP 侧执行。
- 控制/优化变量：UAV 部署、用户关联、任务卸载、通信资源和计算频率。
- 约束来源：电池容量、时延限制、传输功率、CSI 误差、机会约束。
- 画图提醒：图中要突出“UAV 灵活接入 + HAP 稳定算力”的分层结构。

## System Model
- HAP 位于高空固定位置，为多 UAV 提供上层稳定算力支撑。
- UAV 作为近端空中 MEC 节点，负责接入地面用户并处理中近程任务。
- 卸载决策、资源配置和 UAV 部署彼此耦合，且受到不确定信道误差影响。
- 目标是在满足任务 QoS 的前提下最小化总能耗，并尽可能多服务用户。

## Algorithm Design 详解
- 第一步使用加权 K-means 预优化 UAV 的部署位置。
- 第二步把含机会约束的 MINLP 通过 CVaR 转化为分布鲁棒约束形式。
- 第三步把鲁棒问题转为 MISOCP，并用 primal decomposition 分解为连续和离散子问题。
- 第四步用二元鲸鱼优化算法求解离散卸载与关联决策。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成空中 MEC 场景
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：鲁棒性评估设计较完整，但实现平台与代码形态未公开。

## Introduction 写作素材
- 单纯把 UAV 看成移动边缘节点已经难以覆盖大范围场景，高空平台可以提供更稳定的上层算力补充。
- 现实中的 CSI 误差会破坏许多“最优”卸载方案，因此不确定性必须进入主问题而不是事后讨论。
- 这篇论文适合支撑“空中 MEC 正从 UAV 单层协同走向 UAV-HAP 分层体系”的写作判断。

## Related Work 写作素材
- 与传统 UAV-MEC 相比，本文将 HAP 引入分层空中 MEC 架构。
- 与确定性优化相比，本文使用 DRO + CVaR 处理机会约束与 CSI 误差。
- 与单阶段启发式相比，本文把部署、卸载和资源配置做了协同求解。

## 相关系统建模页
- [[计算卸载模型]]
- [[信道与通信速率模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[高空平台（HAP）]]
- [[分布鲁棒优化（DRO）]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [原文](../raw/markdown/jia2025DistributionallyRobustOptimization.md)
