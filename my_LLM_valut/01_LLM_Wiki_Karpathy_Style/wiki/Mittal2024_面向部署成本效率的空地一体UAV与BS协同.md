---
tags: [论文, 部署优化, 空地一体网络, CF-MIMO, coalition game]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/mittal2024DeploymentCostawareUAV.md
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
frameworks:
  - genetic algorithm
  - coalition formation game
  - pilot-aware clustering
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Mittal2024 面向部署成本效率的空地一体UAV与BS协同

## 单行摘要
论文在 clustered cell-free M-MIMO 支撑的空地一体网络中，以部署成本效率 DCE 为核心目标，联合优化 UAV 数量、位置和 BS/UAV 聚类协作关系。

## 题目驱动研究框架
- 研究场景：需要大范围覆盖与大规模连接的 integrated aerial-terrestrial network。
- 研究对象：地面 BS、空中 UAV、用户簇、cell-free M-MIMO 协作结构。
- 核心问题：在提升总速率的同时，如何控制 UAV 部署成本和能耗，避免“性能更好但太贵”的空中网络设计。
- 标题承诺的方法：deployment cost-aware UAV and BS collaboration。
- 期望效果：在 UAV-only、BS-only 与混合协同三者之间找到更具成本效率的平衡点。
- 标题与正文的偏差：正文真正重点不只是 UAV placement，而是把部署、聚类、pilot contamination 和 coalition formation 放进一套统一效益指标。

## Algorithm Design 快照
论文研究 clustered CF-M-MIMO enabled IATN 中的部署成本效率最大化问题。网络效益不是单看 sum-rate，而是用 DCE 同时度量“速率收益”和“部署+能耗成本”。难点在于 UAV 数量、位置、用户聚类和 BS/UAV 协作彼此耦合。为此，作者采用三段式求解：先用网格化遗传算法决定 UAV 密度与位置，再做 pilot-contamination aware 的用户聚类，最后用 coalition formation game 形成 BS/UAV 协作簇。这样，系统可以在成本与吞吐之间显式找平衡，而不是盲目增加 UAV 数量。

## 图1系统框架草案
- 系统实体：地面 BS、空中 UAV、用户、clustered CF-M-MIMO 协作簇。
- 任务/数据流：用户被划入若干簇，由 BS/UAV 形成的 coalition 联合服务。
- 控制/优化变量：UAV 个数、UAV 网格位置、用户聚类、BS/UAV 所属联盟。
- 约束来源：功率预算、pilot contamination、位置可部署性、联盟稳定性。
- 画图提醒：建议突出“空地混合基础设施 + 用户簇 + coalition”三层，而不是只画 UAV 点位。

## System Model
- 地面 BS 与 UAV 共同组成 integrated aerial-terrestrial network，用户通过 clustered CF-M-MIMO 方式被联合服务。
- 目标函数 DCE 定义为网络总速率与部署加能耗成本之比，而不是传统单一速率目标。
- UAV 部署通过网格化候选位置离散化，便于数量和位置同时优化。
- 用户簇与 BS/UAV 联盟结构共同决定 pilot contamination 与最终系统收益。

## Algorithm Design 详解
- 部署阶段：把区域划分为网格，用遗传算法搜索 UAV 数量与位置组合。
- 聚类阶段：根据用户簇与 pilot contamination 风险做污染感知聚类。
- 协作阶段：通过 coalition game 让 BS 与 UAV 形成稳定服务联盟，目标是提高整体 DCE。
- 研究结论：IATN 不必追求越多 UAV 越好，存在明显的最优 UAV 数量；部署面积增大时，最优 UAV 数量也会变化。
- 这篇论文很适合作为[[覆盖与部署优化主线]]里“成本效率导向部署”分支的锚点。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成用户、BS 与 UAV 空地一体场景
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文披露了 10 km x 10 km 区域、100 个拓扑平均和 50 次 coalition 重复实验，但未披露软件栈。

## Introduction 写作素材
- 仅追求 UAV 带来的速率收益会忽略空中基础设施的部署与运行代价。
- 对于空地协同网络，合理问题不是“多几架 UAV 是否更强”，而是“每一架 UAV 的边际收益是否仍然划算”。
- 这篇论文适合支撑“UAV 部署设计需要从覆盖驱动走向成本效率驱动”的引言判断。

## Related Work 写作素材
- 与最少 UAV 部署研究不同，本文强调的是速率收益与部署成本的比值，而非仅最少数量。
- 与只优化 UAV 位置的研究不同，本文进一步引入用户聚类与 coalition 结构。
- 与纯 UAV-only 或 BS-only 网络相比，本文说明混合 IATN 往往能提供更好的成本效率平衡。

## 相关系统建模页
- [[区域覆盖与部署模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[部署成本效率（DCE）]]
- [[空地一体网络（IATN）]]
- [[无人机部署优化]]
- [[覆盖与部署优化主线]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/mittal2024DeploymentCostawareUAV.md)
