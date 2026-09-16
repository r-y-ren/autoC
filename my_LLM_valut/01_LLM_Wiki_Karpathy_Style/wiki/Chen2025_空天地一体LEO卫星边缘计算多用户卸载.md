---
tags: [论文, 任务卸载, 低轨卫星, 博弈论, UAV]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/chen2025MultiuserTaskOffloading.md
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

# Chen2025 空天地一体 LEO 卫星边缘计算多用户卸载

## 单行摘要
论文把 UAV 与 LEO 卫星联合组成 ULSE 网络，在多用户竞争有限资源和卫星覆盖时间受限的条件下，将任务卸载建模为潜在博弈，并用 JULTO 算法寻找 Nash 均衡。

## 题目驱动研究框架
- 研究场景：地形复杂、地面通信基础设施薄弱区域的 UAV-assisted LEO satellite edge computing。
- 研究对象：多个移动用户设备、UAV 边缘服务器、LEO 卫星边缘服务器。
- 核心问题：在 UAV 与 LEO 卫星资源都有限且卫星可见时间受限时，多用户如何形成平衡的卸载策略。
- 标题承诺的方法：multi-user task offloading + game-theoretic approach。
- 期望效果：降低用户综合开销，并在分布式决策中兼顾资源竞争与覆盖时间约束。
- 标题与正文的偏差：标题强调 game-theoretic approach，但正文更关键的建模点其实是“LEO 覆盖时间约束 + UAV 无线供能 + 多用户潜在博弈”。

## Algorithm Design 快照
论文针对 UAV 与 LEO 卫星联合构成的空天地边缘网络，研究多用户在本地、UAV 和 LEO 卫星之间的任务卸载选择。问题同时受到 UAV/卫星计算资源限制、LEO 可见覆盖时间限制以及用户个体自利性的影响，因此难以直接集中式求解。作者先证明原问题 NP-hard，再把每个用户的卸载选择建模为 LUTO-Game，其中用户的目标是最小化由时延和能耗加权得到的个人成本。随后，作者证明该博弈是 potential game，并设计分布式 JULTO 算法迭代更新 UAV/LEO 卸载策略，以收敛到 Nash 均衡。

## 图1系统框架草案
- 系统实体：移动用户、若干 UAV 边缘节点、若干 LEO 卫星边缘节点。
- 任务/数据流：用户任务可本地执行、卸载到 UAV，或在满足可见时间的前提下卸载到 LEO 卫星。
- 控制/优化变量：每个用户的卸载目的地、对应获得的计算资源、是否满足卫星覆盖时间约束。
- 约束来源：UAV/LEO 计算能力上界、LEO 可见时间、用户传输功率与传播时延。
- 画图提醒：建议在图中单独画出“coverage window”时间约束，否则很难体现 LEO 与普通边缘服务器的差异。

## System Model
- 用户的成本函数由时延与能耗加权构成，允许根据偏好设置不同权重。
- UAV 侧不仅提供计算资源，还允许通过无线能量传输补充用户能量，这使 UAV 卸载成本与 LEO 卸载成本结构不同。
- LEO 卸载除了普通传输与计算资源约束，还存在由轨道运动导致的 coverage time 约束，这是该系统最关键的额外约束。
- 最终的卸载决策空间包含三类动作：本地、UAV、LEO，但不同动作对应不同的成本模型与可行域。

## Algorithm Design 详解
- 第一步是成本建模：分别定义本地计算、UAV 卸载、LEO 卸载的时延与能耗成本。
- 第二步是全局问题构造：目标是最小化所有用户总成本，同时满足卫星覆盖时间与两类边缘节点的资源约束。
- 第三步是复杂性分析：作者证明该问题 NP-hard，因此难以直接求全局最优。
- 第四步是博弈重构：将每个用户看作理性参与者，构造 LUTO-Game，并通过 potential function 证明至少存在一个可行 Nash 均衡。
- 第五步是分布式求解：JULTO 允许多个用户并行更新卸载选择，并给出 price of anarchy 分析来刻画分布式均衡与集中式最优之间的性能差距。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`low`
- 证据备注：论文给出了结果，但实验资产链条说明有限，当前更适合支撑方法理解而不是直接复现。

## Introduction 写作素材
- 仅依赖 UAV 边缘无法保证全局覆盖，而仅依赖 LEO 卫星又会受到可见时间和资源窗口的限制。
- 因此，真正值得研究的是空天地异构边缘节点共存时的多用户竞争性卸载。
- 在这类场景里，卫星 coverage window 不是细节约束，而是决定系统可行性的核心要素。
- 这篇论文很适合支撑“从地空协同扩展到空天地一体化边缘卸载”的引言论证。

## Related Work 写作素材
- 与传统 UAV-assisted MEC 文献相比，本文引入了 LEO 卫星计算资源与可见时间约束。
- 与只做集中式优化的 SAGIN 工作相比，本文强调多用户自利行为和分布式均衡。
- 与纯卫星 MEC 文献相比，本文用 UAV 补足卫星资源的局部灵活性与供能能力。
- 相关工作写作时，它适合放在“space-air integrated offloading”方向，和经典 UAV-MEC 工作形成层级扩展。

## 相关系统建模页
- [[计算卸载模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[任务卸载]]
- [[低轨卫星边缘计算]]
- [[资源分配]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [原文](../raw/markdown/chen2025MultiuserTaskOffloading.md)
