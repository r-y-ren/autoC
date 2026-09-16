---
tags: [概念, AoI, 信息时效]
created: 2026-04-08
updated: 2026-04-09
sources:
  - ../raw/markdown/hoang2024FiniteBlockLength.md
  - ../raw/markdown/hou2025AgeInformationawareMultiobjective.md
  - ../raw/markdown/lin2024LyapunovbasedApproachJoint.md
  - ../raw/markdown/song2024AoIEnergyTradeoff.md
  - ../raw/markdown/wang2024EnsuringThresholdAoI.md
  - ../raw/markdown/zhan2024TradeoffAgeInformation.md
---

# 信息年龄（AoI）

## 定义
[[信息年龄（AoI）]]衡量接收端当前持有信息距离其最近一次生成时刻已经过去了多久，用于刻画信息新鲜度。

## 为什么重要
- AoI 不只是传输延迟，还考虑等待时间、更新频率和访问周期。
- 在 UAV 场景中，任务传完不等于信息足够新，尤其在持续监测、协同追踪和群智感知任务里更明显。
- 一旦系统强调状态更新、巡检或持续感知，AoI 往往比平均时延更有解释力。

## 在当前语料中的关键问题
- 短包通信里 AoI 与 BLER、块长和 goodput 如何联动。
- 周期性巡检场景中，AoI 如何改变 UAV 路线设计和补能节奏。
- AoI 如何与能耗、任务成功率、运行时间和持续作业一起进入统一目标。
- 什么时候需要进一步从 AoI 升级到 [[阈值AoI]]。

## 当前语料中的代表论文
- [[Hoang2024_有限块长NOMA多用户配对UAV系统性能分析与优化]]：把 AoI 与 BLER、吞吐一起分析。
- [[Hou2025_AoI感知的异构UAV-USV-UUV网络水下目标围捕优化]]：把 AoI 融入异构搜索奖励函数。
- [[Huang2024_LI2灾后PoI及时监测的UAV_AoI路径优化]]：把 AoI 推进到图约束、回站补能和灾后持续巡检问题。
- [[Song2024_空地协同MEC中的AoI与能耗权衡学习]]：把 AoI 与能耗同时写进 HAP-UAV 协同 MEC 的 Pareto 学习框架。
- [[Wang2024_面向UAV群智感知的阈值AoI保障]]：进一步把 AoI 红线保障写成 `threshold AoI` 问题。
- [[Zhan2024_多小区蜂窝网络UAV感知的AoI与运行时间权衡]]：把 AoI 与蜂窝连接 UAV 的 operation time 联动分析。

## 研究判断
AoI 代表 UAC 研究正在从“把数据送到”推进到“把最新数据及时送到，而且长期稳定送到”。Batch_10 的新证据进一步说明，这条线已经开始自然分叉为 `AoI-能耗权衡`、`AoI-运行时间权衡` 和 `阈值AoI保障` 三条更具体的子路线。

## 相关页面
- [[阈值AoI]]
- [[任务队列与时延保障模型]]
- [[无人机辅助群智感知与持续作业]]
- [[轨迹优化与协同控制]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [Hoang2024 原文](../raw/markdown/hoang2024FiniteBlockLength.md)
- [Hou2025 原文](../raw/markdown/hou2025AgeInformationawareMultiobjective.md)
- [Huang2024/lin 原文](../raw/markdown/lin2024LyapunovbasedApproachJoint.md)
- [Song2024 原文](../raw/markdown/song2024AoIEnergyTradeoff.md)
- [Wang2024 原文](../raw/markdown/wang2024EnsuringThresholdAoI.md)
- [Zhan2024 原文](../raw/markdown/zhan2024TradeoffAgeInformation.md)
