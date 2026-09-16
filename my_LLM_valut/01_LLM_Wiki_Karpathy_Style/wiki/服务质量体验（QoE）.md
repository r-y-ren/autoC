---
tags: [概念, QoE, 用户体验]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/he2024OnlineJointOptimization.md
  - ../raw/markdown/hoang2025Adaptive3DPlacementa.md
---

# 服务质量体验（QoE）

## 定义
[[服务质量体验（QoE）]]强调用户主观感知的服务满意度，常由 MOS 等指标刻画，用来描述数据率、时延和需求满足程度如何共同影响用户体验。

## 为什么重要
- QoE 比单一吞吐或时延更贴近用户真正感受到的服务质量。
- 在 UAV 系统中，移动性和资源稀缺会让“平均最优”与“体验最优”明显不同。
- 它常与队列稳定、长期控制和服务公平性一起出现。

## 在当前语料中的关键问题
- 如何在在线决策中最大化长期 QoE。
- 如何用 MOS 把用户业务需求和实际数据率联系起来。
- QoE 与 SER 这类体验指标之间如何互补。

## 当前语料中的代表论文
- [[He2024_UAV辅助MEC服务质量体验最大化的在线联合优化]]：在 UAV-MEC 中直接最大化长期 QoE。
- [[Hoang2025_6G空中小蜂窝中多UAV基站自适应三维部署]]：在多 UAV-BS 动态部署中用 MOS 衡量用户体验。

## 研究判断
QoE 说明 UAC 正在从系统侧性能指标走向用户侧感知指标。

## 相关页面
- [[服务体验比（SER）]]
- [[安全与服务保障]]
- [[He2024_UAV辅助MEC服务质量体验最大化的在线联合优化]]
- [[Hoang2025_6G空中小蜂窝中多UAV基站自适应三维部署]]

## 来源
- [He2024 原文](../raw/markdown/he2024OnlineJointOptimization.md)
- [Hoang2025 原文](../raw/markdown/hoang2025Adaptive3DPlacementa.md)
