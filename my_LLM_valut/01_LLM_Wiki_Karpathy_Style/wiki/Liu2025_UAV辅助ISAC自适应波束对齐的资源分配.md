---
tags: [论文, ISAC, 波束对齐, 资源分配, 无人机通信]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/liu2025ResourceAllocationAdaptive.md
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

# Liu2025 UAV辅助ISAC自适应波束对齐的资源分配

## 单行摘要
论文研究 UAV 辅助 ISAC 网络中感知辅助波束对齐的问题，联合优化通信功率、感知功率和感知驻留时间以最大化通信速率下界。

## 题目驱动研究框架
- 研究场景：UAV 挂载空中基站的 ISAC 网络。
- 研究对象：地面用户 GUs、空中基站 ABS、宏基站 MBS、共享频谱下的感知与通信链路。
- 核心问题：UAV 高动态导致波束易失配，如何利用感知结果辅助波束对齐并提升通信速率。
- 标题承诺的方法：resource allocation for adaptive beam alignment。
- 期望效果：在感知与通信共享频率的情况下，提高 GU-ABS 与 ABS-MBS 两段链路的总体通信能力。
- 标题与正文的偏差：正文的核心创新不仅是波束对齐，还包括从 CRB 推导 ISAC 速率下界，并用 DRL 替代高复杂度 SCA 求解。

## Algorithm Design 快照
论文面向 UAV 辅助的一体化感知与通信网络，研究如何用机载雷达对地面用户与宏基站进行位置感知，从而改善空中基站的波束对齐精度并提升通信速率。难点在于感知功率、感知时间和通信发射功率共用频谱并彼此耦合，且误对齐误差会同时影响接入链路和回传链路。为此，作者先利用 Cramer-Rao Bound 推导通信速率下界，进而建立联合优化问题，再将其拆分为 GU-ABS 和 ABS-MBS 两个资源分配子问题。为降低计算复杂度，论文进一步用 DRL 近似替代逐次凸近似求解，实现更快的资源配置。

## 图1系统框架草案
- 系统实体：GUs、UAV 挂载 ABS、MBS、机载感知模块。
- 任务/数据流：ABS 先通过感知估计 GUs 与 MBS 的相对位置，再做波束对齐，完成 GU-ABS 接入与 ABS-MBS 回传。
- 控制/优化变量：通信发射功率、感知功率、感知驻留时间、关联链路资源。
- 约束来源：共享频谱、误对齐误差、CRB 感知精度、功率预算与时频资源预算。
- 画图提醒：图中要清晰表现“感知帮助通信”和“接入/回传双子问题”这两层关系。

## System Model
- 网络由 GUs、ABS 和 MBS 构成，ABS 同时承担通信中继与机载感知功能。
- 波束失配误差由感知精度决定，感知精度又受到感知功率与驻留时间影响，因此速率与感知精度强耦合。
- 论文分别建模了 GU-ABS 与 ABS-MBS 两段通信，并把两段链路放入统一资源分配框架。
- 目标是最大化通信速率下界而非直接最大化瞬时经验速率，这使模型具有明确的估计精度支撑。

## Algorithm Design 详解
- 第一步从 Cramer-Rao Bound 出发，推导感知误差如何影响波束对齐和通信速率下界。
- 第二步建立联合优化问题，把通信功率、感知功率和感知驻留时间同时作为决策变量。
- 第三步将原问题按 GU-ABS 与 ABS-MBS 两段链路拆分，降低直接求解难度。
- 第四步先给出基于 SCA 的近似求解思路，再设计 DRL 方法替代高复杂度的迭代凸化。
- 方法意义在于把[[一体化感知与通信（ISAC）]]从“共享硬件”推进到“感知精度直接进入速率优化”的层面。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成 UAV-ISAC 场景
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文提供了完整的参数化仿真和复杂度分析，但未披露实现平台与代码资产。

## Introduction 写作素材
- UAV 的高机动性带来部署灵活性，也让波束保持和回传对准变得更困难。
- 在空中网络中，感知与通信不是独立模块，感知误差会直接决定通信收益。
- 如果要写 ISAC 引言，这篇论文很适合支撑“感知辅助对齐”而非“单纯共享频谱”的研究转向。

## Related Work 写作素材
- 与只优化通信资源的 UAV 网络工作相比，本文显式建模感知功率与感知驻留时间。
- 与常规波束训练/对齐方案相比，本文通过 CRB 把感知精度与速率下界建立了理论连接。
- 与纯 SCA 解法相比，本文强调 DRL 在复杂耦合资源分配上的近似替代价值。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[一体化感知与通信（ISAC）]]
- [[自适应波束对齐]]
- [[空中通信与协同传输]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/liu2025ResourceAllocationAdaptive.md)
