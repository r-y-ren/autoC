---
tags: [论文, 任务卸载, 资源定价, 博弈论, UAV辅助MEC]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/chen2025TaskOffloadingResource.md
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
reproducibility_level: low
---

# Chen2025 博弈论驱动的 UAV 辅助边缘计算卸载与资源定价

## 单行摘要
论文在 BS-ES 与 UAV-ES 共存的 MEC 系统中，把用户分配、任务卸载和服务器资源定价联合起来，先用非合作博弈做用户分配，再用 Stackelberg 博弈求服务器定价与用户卸载均衡。

## 题目驱动研究框架
- 研究场景：含一个地面 BS 边缘服务器和一个 UAV 边缘服务器的 UAV-assisted MEC 系统。
- 研究对象：多个边缘用户、BS-ES、UAV-ES 以及用户的计算任务。
- 核心问题：在服务器有收益诉求、用户有成本与满意度诉求时，如何同时决定用户去哪个服务器以及服务器如何定价。
- 标题承诺的方法：task offloading and resource pricing based on game theory。
- 期望效果：提升服务器与用户双方效用，避免单一服务器过载并控制 UAV 侧能耗。
- 标题与正文的偏差：标题较准确，但正文其实是“先做用户分配，再做定价-卸载博弈”的两阶段框架。

## Algorithm Design 快照
论文针对 BS-ES 与 UAV-ES 共存的 UAV 辅助 MEC 系统，研究用户卸载目的地选择和服务器资源定价问题。作者认为在真正的服务交互里，用户是否卸载、卸载多少与服务器如何报价是相互影响的，因此不能只优化卸载比例而忽略价格机制。为此，论文分两步求解：先把用户分配问题建模为多用户非合作博弈，以服务器总能耗最小为目标，通过 GBUA 算法为每个用户选择 BS 或 UAV；随后再将服务器与用户的交互建模为 Stackelberg 博弈，由服务器先定价、用户再决定卸载量，并通过 RPATO 算法求解 Stackelberg 均衡。

## 图1系统框架草案
- 系统实体：多个边缘用户、一台地面 BS-ES、一台 UAV-ES。
- 任务/数据流：用户先完成目标服务器分配，再依据服务器价格决定卸载量，服务器执行任务并返回结果。
- 控制/优化变量：用户分配策略、用户卸载量、服务器定价、UAV 计算能耗。
- 约束来源：用户时延容忍上界、价格上下界、UAV 电池容量、服务器计算能力。
- 画图提醒：图中要把“分配阶段”和“定价/卸载阶段”分开，否则会看不出两阶段博弈结构。

## System Model
- 系统包含一个 BS 边缘服务器和一个 UAV 边缘服务器，两者都可向用户出售闲置计算资源。
- 用户效用不只包含时延和能耗，还包含对卸载量的满意度以及超过时延容忍阈值时的 reward-penalty 项。
- 服务器效用则由售卖计算资源的收入减去计算能耗与 reward-penalty 项构成，因此服务器既希望多卖资源，也要避免低效执行。
- UAV 侧还存在自身悬停与计算带来的额外能耗预算约束，这使 UAV 定价行为不能脱离能量模型独立考虑。

## Algorithm Design 详解
- 第一步是用户分配：作者先假定用户完全卸载，构造以最小化服务器总能耗为目标的用户分配问题。
- 第二步是 NE 证明：把用户服务器选择建模为非合作博弈，证明存在 Nash 均衡，并设计 GBUA 算法迭代更新分配结果。
- 第三步是定价-卸载博弈：在给定分配结果后，将 BS-ES 与 UAV-ES 视为 leaders，用户视为 followers，建立 Stackelberg 模型。
- 第四步是 backward induction：通过逆向归纳证明存在唯一 Stackelberg 均衡，并用 RPATO 迭代搜索近似解。
- 第五步是系统目标：并非单纯最小化时延，而是提升服务器和用户双方效用，因此更接近现实服务市场建模。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`low`
- 证据备注：论文给出了结果，但实验资产链条说明有限，当前更适合支撑方法理解而不是直接复现。

## Introduction 写作素材
- 在现实边缘系统里，计算资源不是免费供给，服务器定价会直接改变用户卸载行为。
- 因此，仅研究“任务往哪里卸”是不够的，还要研究“资源卖多少钱”。
- UAV-assisted MEC 场景下，UAV 服务器的能量限制会进一步改变其最优报价策略，这使资源定价成为系统建模不可忽略的一部分。
- 这篇论文很适合支撑“从纯技术调度走向机制设计与服务交互”的引言拓展。

## Related Work 写作素材
- 与只做任务卸载优化的工作相比，本文显式考虑资源定价和双边效用。
- 与只做单阶段 Stackelberg 定价的工作相比，本文先处理用户分配，再处理定价与卸载耦合。
- 与普通地面 MEC 定价文献相比，本文把 UAV 侧能耗约束引入服务器效用。
- 相关工作中可将其归入“pricing-aware offloading”路线，与传统 UAV-MEC 卸载研究形成机制层互补。

## 相关系统建模页
- [[计算卸载模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[任务卸载]]
- [[资源分配]]
- [[资源定价]]
- [[UAV辅助MEC]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [原文](../raw/markdown/chen2025TaskOffloadingResource.md)
