---
tags: [论文, THz, SAGIN, UAV部署, 资源分配]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/tun2025JointUAVDeployment.md
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
platforms:
  - Python
  - CVXPY
frameworks:
  - BCD
  - matching game
  - CCP
  - SCA
  - BSUM
datasets: []
hardware_stack:
  - Intel Core i5-8500 3.00 GHz
  - 32.0 GB RAM
  - NVIDIA GeForce GTX 1660 Ti
artifact_availability: unknown
reproducibility_level: medium
---

# Tun2025 THz辅助空天地一体网络中的UAV部署与资源分配

## 单行摘要
论文在 THz-assisted MEC-enabled integrated SAG 网络中联合优化设备卸载、THz 子带分配、功率控制、UAV 部署和 UAV 二次卸载，以最小化终端与 UAV 总能耗。

## 题目驱动研究框架
- 研究场景：缺乏地面基础设施区域中的 THz 辅助空天地一体 MEC 网络。
- 研究对象：地面设备、多个 UAV、LEO 卫星、THz 子带与机载 MEC 服务链。
- 核心问题：在多 UAV 协作与星空地回传并存时，如何同时决定设备卸载、空口资源和 UAV 部署位置。
- 标题承诺的方法：joint UAV deployment and resource allocation。
- 期望效果：在满足时延约束的前提下同时降低终端和 UAV 的总能耗。
- 标题与正文的偏差：正文真正重点不是单一 deployment，而是把 deployment、sub-band、power control 和 UAV-to-UAV/UAV-to-satellite 卸载统一到同一 BCD 框架。

## Algorithm Design 快照
论文研究 THz-assisted MEC-enabled integrated SAG 网络中的能量最小化问题。地面设备可将任务卸载给 UAV，UAV 之间还可继续协作转发任务，或进一步卸载到 LEO 卫星。难点在于离散的任务卸载、THz 子带匹配、连续功率控制、连续 UAV 部署和二次卸载决策强耦合。为此，作者用 BCD 将原问题拆成四个子问题，再分别用 convex optimization、matching game、CCP、SCA 和 BSUM 求解，从而得到可迭代收敛的联合部署与资源分配算法。

## 图1系统框架草案
- 系统实体：无线设备、多个 UAV、LEO 卫星、THz 子带资源。
- 任务/数据流：设备任务先卸载到关联 UAV；UAV 再选择本地算、转发给其他 UAV，或上送卫星。
- 控制/优化变量：设备卸载比例、THz 子带分配、发射功率、UAV 位置、UAV 二次卸载目的地。
- 约束来源：任务时延、THz 资源限制、发射功率上限、空口干扰与部署可行性。
- 画图提醒：要突出“device -> UAV -> UAV/LEO”这条二跳服务链，而不是只画星空地拓扑。

## System Model
- 网络由地面设备、多个 UAV 和 LEO 卫星组成，设备在 K-means 关联结果基础上接入 UAV。
- UAV 利用 THz 频段向地面设备提供短距高比特率接入，并通过空中协作或卫星回传实现远端计算。
- 优化目标是最小化设备与 UAV 的总能耗，而非只最小化终端侧卸载能量。
- 任务必须满足最大容忍时延，因此部署与子带选择会直接影响是否可卸载。

## Algorithm Design 详解
- 子问题1：设备任务卸载比例，通过标准凸优化处理。
- 子问题2：THz 子带分配与功率控制，通过 one-to-one matching game + CCP 协同求解。
- 子问题3：UAV 部署，通过 SCA 逐步凸化非凸位置优化问题。
- 子问题4：UAV 任务二次卸载，通过 BSUM 处理离散协作决策。
- 实验结论：对给定覆盖面积和设备规模，`4` 架 UAV 已接近能效最优，再继续增加 UAV 可能只提升硬件成本。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成 THz 辅助空天地一体场景
- 平台与软件：`Python`、`CVXPY`
- 硬件与算力：`Intel Core i5-8500 3.00 GHz`、`32 GB RAM`、`NVIDIA GeForce GTX 1660 Ti`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文明确披露了求解平台配置，并给出 95% 置信区间与多种对比变体。

## Introduction 写作素材
- 仅把 UAV 看作“临时接入点”会低估其在跨域计算链中的中继与协作价值。
- THz 的高带宽潜力只有和 UAV 部署、功率控制、子带分配联合考虑时才真正可用。
- 这篇论文适合支撑“空天地一体卸载正在从静态链路拼接走向跨域协同部署”的判断。

## Related Work 写作素材
- 与传统 SAG 卸载工作相比，本文显式纳入 UAV 间协作和 THz 子带分配。
- 与单 UAV 轨迹/部署研究相比，本文更强调跨域基础设施和多 UAV 协作链。
- 与只做 power control 或 only offloading 的 THz MEC 研究相比，本文把 deployment 放入主问题核心。

## 相关系统建模页
- [[计算卸载模型]]
- [[信道与通信速率模型]]
- [[区域覆盖与部署模型]]

## 相关概念与主题页
- [[THz辅助空天地一体网络]]
- [[空天地一体网络（SAGIN）]]
- [[无人机部署优化]]
- [[任务卸载与资源分配研究主线]]
- [[覆盖与部署优化主线]]

## 来源
- [原文](../raw/markdown/tun2025JointUAVDeployment.md)
