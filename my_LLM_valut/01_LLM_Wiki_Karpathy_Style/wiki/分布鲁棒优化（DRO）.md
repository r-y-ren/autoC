---
tags: [概念, DRO, 鲁棒优化]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/jia2025DistributionallyRobustOptimization.md
  - ../raw/markdown/chen2024AdaptiveBitrateVideo.md
---


# 分布鲁棒优化（DRO）

## 定义
[[分布鲁棒优化（DRO）]]在只掌握不确定参数分布部分信息或模糊集合时，对最坏分布情形下的目标和约束进行优化。

## 为什么重要
- 真实无线和任务环境常带有估计误差，确定性最优解很容易失效。
- DRO 能把“误差存在”正式写进模型，而不是只做灵敏度分析。
- 它特别适合 CSI 不确定、需求波动和统计信息不足的空中网络场景。

## 在当前语料中的关键问题
- 如何把机会约束转写成 tractable 的鲁棒形式。
- CVaR 等风险度量如何进入 UAV/MEC 优化问题。
- 鲁棒收益是否会带来可接受的复杂度代价。

## 当前语料中的代表论文
- [[Chen2024_面向自适应码率视频的UAV辅助MEC鲁棒缓存]]：从分布不确定性角度处理缓存和内容交付。
- [[Jia2025_UAV与HAP协同空中MEC的分布鲁棒优化]]：用 CVaR 机制重写机会约束并求解 UAV-HAP 空中 MEC。

## 研究判断
DRO 表明空中网络优化正在从“理想参数最优”走向“误差条件下仍可用”的稳健设计。

## 相关页面
- [[高空平台（HAP）]]
- [[任务卸载与资源分配研究主线]]
- [[Jia2025_UAV与HAP协同空中MEC的分布鲁棒优化]]
- [[Chen2024_面向自适应码率视频的UAV辅助MEC鲁棒缓存]]

## 来源
- [Jia2025 原文](../raw/markdown/jia2025DistributionallyRobustOptimization.md)
- [Chen2024 原文](../raw/markdown/chen2024AdaptiveBitrateVideo.md)
