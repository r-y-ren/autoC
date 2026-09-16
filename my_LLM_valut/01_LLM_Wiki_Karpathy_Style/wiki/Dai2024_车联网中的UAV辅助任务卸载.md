---
tags: [论文, UAV辅助MEC, 任务卸载, Lyapunov, 车联网]
created: 2026-04-06
updated: 2026-04-08
sources:
  - ../raw/markdown/dai2024UAVAssistedTaskOffloading.md
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
  - trace_driven
data_origin:
  - mixed
platforms:
  - MindSpore
frameworks:
  - MindSpore
datasets:
  - Shenzhen IoV trajectory dataset
hardware_stack: []
artifact_availability: partial
reproducibility_level: medium
---

# Dai2024 车联网中的 UAV 辅助任务卸载

## 单行摘要
论文针对城市热点区域 RSU 过载问题，引入 UAV 作为机动边缘服务器，在长期能量约束下在线最小化车联网任务时延。

## 题目驱动研究框架
- 研究场景：车联网 VEC 网络中，热点区域 RSU 因车辆密度和任务到达激增而过载。
- 研究对象：车辆、RSU、单个 UAV、长期运行中的边缘卸载系统。
- 核心问题：UAV 应在每个时隙支援哪个过载 RSU，才能降低车辆任务时延且不透支自身长期能量预算。
- 标题承诺的方法：UAV-assisted task offloading。
- 期望效果：在不依赖未来信息的前提下，在线得到近似最优的 UAV 辅助卸载决策。
- 标题与正文的偏差：标题看起来像“车辆直接向 UAV 卸载”，但正文更准确的对象是“UAV 支援过载 RSU”，即 UAV 作为第二层边缘缓冲器，而不是车辆直连空中服务器。

## Algorithm Design 快照
论文面向车联网热点区域中 RSU 计算过载的问题，研究单 UAV 如何动态支援不同过载 RSU，以在线降低车辆任务时延。难点在于过载位置随车辆密度和任务到达不断变化，同时 UAV 的能量消耗具有长期预算约束，不能只做瞬时最优。为此，论文把长期能量约束通过 Lyapunov 优化转化为逐时隙决策，再用基于 Markov approximation 的方法在过载 RSU 集合上搜索近似最优的 UAV 辅助卸载策略。整体目标是在保证 UAV 长期可持续运行的同时，稳定地缓解热点区域的任务拥塞。

## 图1系统框架草案
- 系统实体：车辆层、RSU 层、UAV 层。
- 任务/数据流：车辆先把计算密集型任务卸载到 RSU；当 RSU 过载时，UAV 选择一个过载 RSU，承接其部分计算工作负载。
- 控制/优化变量：每时隙 UAV 支援对象、从 RSU 到 UAV 的卸载量、UAV 飞行状态与能量赤字队列。
- 约束来源：车辆到 RSU 传输时延、RSU/UAV 计算能力、UAV 长期能量预算、任务到达随机性。
- 画图提醒：论文原始 Fig. 1 是深圳负载热力图，真正可直接服务写作的系统框架应以论文 Fig. 2 为蓝本来画三层结构图。

## System Model
- 系统由车辆层、RSU 层和 UAV 层构成；车辆任务先通过 V2I 链路送至 RSU，UAV 只在 RSU 过载时介入。
- 过载是通过 RSU 计算工作负载超出其计算能力来定义的，因此问题的本质不是“有没有链路”，而是“如何缓解空间上和时间上都在变化的计算热点”。
- UAV 以固定高度飞行并可调整位置，其任务是为某个过载 RSU 提供额外边缘计算能力，而非直接跟踪每一辆车的位置。
- 论文同时建模了车辆到 RSU 的卸载时延、RSU 到 UAV 的辅助卸载时延，以及 UAV 的长期能量约束与能量赤字队列。

## Algorithm Design 详解
- 第一步是在线问题转化：论文使用 Lyapunov 优化把长期 UAV 能量约束转化为能量赤字队列，从而把长期控制问题变成逐时隙可求解的问题。
- 第二步是策略搜索：在给定时隙的过载 RSU 集合上，构造基于 Markov approximation 的离散时间 Markov 链，以搜索近似最优的 UAV 辅助卸载策略。
- 第三步是性能证明：论文给出了在线算法的任务时延与长期能量行为分析，使方法不仅是启发式策略，而是具有理论支撑的随机优化框架。
- 方法论上，这篇论文非常适合作为[[Lyapunov优化]]进入车联网空中边缘方向的代表作，因为它把“长期约束 + 在线卸载”这条主线讲得最完整。

## 实验证据卡片
- 验证类型：数值仿真；真实数据驱动仿真
- 数据来源：混合来源；涉及数据集：`Shenzhen IoV trajectory dataset`
- 平台与软件：`MindSpore`
- 硬件与算力：未说明
- 开源情况：部分资产公开
- 复现判断：`medium`
- 证据备注：论文使用真实数据或真实轨迹驱动仿真，但这仍不等同于实际部署或实飞验证。

## Introduction 写作素材
- 城市热点区域的 RSU 过载不是极端情况，而是由车辆密度、任务到达率和空间聚集效应共同导致的常见现象。
- 传统的云辅助方案通信距离长、回程开销大，传统多 RSU 协作又会引入多跳路径、连续性和信任问题。
- UAV 的价值不在于替代整个地面网络，而在于作为机动外援快速切入热点位置，缓解局部计算拥塞。
- 如果写 introduction，可以把深圳真实轨迹数据驱动的热区图作为“问题现实性”证据。

## Related Work 写作素材
- 与云辅助卸载相比，本文强调低时延的空中边缘缓冲，而不是把任务继续推向远端云。
- 与 RSU 间协作相比，本文避免了多跳协作造成的额外通信成本与信任风险。
- 与大量 UAV 直接服务终端的工作不同，本文的 UAV 只服务过载 RSU，因此不需要精确追踪车辆瞬时位置。
- 后续写 related work 时，可把它与[[Huang2024_多UAV车载边缘计算动态任务卸载]]并列为“车联网/低空经济支线”，前者偏过载缓解，后者偏可靠性保障。

## 相关系统建模页
- [[计算卸载模型]]
- [[任务队列与时延保障模型]]
- [[无人机能耗模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[UAV辅助MEC]]
- [[任务卸载]]
- [[Lyapunov优化]]
- [[任务卸载与资源分配研究主线]]
- [[空中计算与UAV辅助MEC的关系]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/dai2024UAVAssistedTaskOffloading.md)
