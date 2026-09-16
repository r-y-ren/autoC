---
tags: [论文, UAV辅助MEC, 任务迁移, 模仿学习, 任务卸载]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/wang2025JointTaskOffloading.md
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
  - Python 3.8
  - PyTorch 1.10
  - BonnMotion-3.0.1
frameworks:
  - GAIL
  - IPPO
datasets: []
hardware_stack:
  - Intel Xeon Gold 6148 CPU
  - GeForce RTX 3090 GPU
  - 128 GB RAM
artifact_availability: unknown
reproducibility_level: medium
---

# Wang2025 动态UAV-MEC网络中的任务卸载与迁移优化

## 单行摘要
论文针对移动用户导致的链路波动问题，引入任务迁移并提出 ILCTS 模仿学习框架，以联合优化 UAV-MEC 中的卸载与迁移时延。

## 题目驱动研究框架
- 研究场景：动态移动用户驱动的 UAV-enabled MEC 网络。
- 研究对象：多架固定部署 UAV、持续移动的用户 MUs、中央 SDN 控制器、硬/软时延任务。
- 核心问题：当用户移动导致原有服务 UAV 不再合适时，如何在卸载之外进一步做任务迁移以维持 QoS。
- 标题承诺的方法：joint task offloading and migration optimization。
- 期望效果：降低平均时延并提高训练准确性与策略适应性。
- 标题与正文的偏差：正文的亮点不只是“joint”，而是把改进 PPO 生成专家策略、GAIL 模仿学习和在线持续探索串成一条学习流水线。

## Algorithm Design 快照
论文研究动态 UAV-MEC 网络中计算任务的服务选择问题，其中用户会持续移动，导致原先的服务 UAV 可能在任务执行过程中失去优势。难点在于系统不仅要决定任务最初卸载到哪架 UAV，还要在执行过程中判断是否迁移任务以满足硬时延和软时延要求。为此，作者定义 CTMiG 问题，并提出 ILCTS 框架：先用改进 PPO 训练专家策略并生成高质量状态-动作对，再利用生成对抗模仿学习逼近专家行为，同时通过在线学习持续修正策略。这样系统能在复杂动态场景中更快获得高质量迁移与卸载决策。

## 图1系统框架草案
- 系统实体：多架 UAV、移动用户、SDN 控制器。
- 任务/数据流：用户把任务卸载到某架 UAV 执行；当网络状态变化时，控制器决定是否把任务迁移到另一架 UAV。
- 控制/优化变量：初始卸载决策、迁移决策、每时隙服务选择策略。
- 约束来源：硬/软时延要求、带宽波动、UAV 计算能力、用户移动轨迹。
- 画图提醒：图中最好把“初始卸载”与“执行中迁移”画成两段流程，突出迁移不是卸载的重复，而是二次调度。

## System Model
- 多架 UAV 固定在区域中提供 MEC 服务，用户连续移动并随机生成计算任务。
- 任务分为硬时延和软时延两类，服务目标是最小化平均时延并满足不同任务截止期。
- SDN 控制器统一收集状态并做任务服务决策，因此系统属于集中式在线决策框架。
- 问题本质类似受限资源下的动态分配与重分配，而不是一次性匹配。

## Algorithm Design 详解
- 首先将 CTMiG 问题转化为 Markov 决策过程，状态包含移动用户、UAV 服务状态和任务时延要求。
- 离线阶段用改进 PPO 训练专家策略，为后续模仿学习提供高质量样本。
- 在线阶段用 GAIL 学习专家行为，并继续与环境交互更新策略，避免只会“复刻专家”而缺乏自适应性。
- 该方法说明[[任务迁移]]在 UAV-MEC 中是一个独立且重要的决策层，尤其适合动态用户场景。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成动态移动场景；`BonnMotion-3.0.1` 生成 1000 条移动轨迹
- 平台与软件：`Python 3.8`、`PyTorch 1.10`、`BonnMotion-3.0.1`
- 硬件与算力：`Intel Xeon Gold 6148`、`RTX 3090`、`128 GB RAM`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文较完整披露了训练平台、轨迹生成工具和网络结构，但没有开放代码。

## Introduction 写作素材
- 在移动用户场景里，仅决定“任务先卸载到哪”还不够，执行中的服务连续性同样决定 QoS。
- 任务迁移是 UAV-MEC 从静态调度走向动态服务维持的重要标志。
- 模仿学习在这里的价值不是替代 RL，而是用高质量专家数据提升复杂动态决策的训练效率。

## Related Work 写作素材
- 与传统卸载优化相比，本文显式把迁移作为独立决策变量。
- 与纯 RL 方法相比，本文利用专家策略和 GAIL 改善收敛速度与策略质量。
- 与车联网边缘迁移工作相比，本文更关注 UAV 动态服务网络中的移动用户。

## 相关系统建模页
- [[计算卸载模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[任务迁移]]
- [[模仿学习]]
- [[近端策略优化（PPO）]]
- [[任务卸载与资源分配研究主线]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/wang2025JointTaskOffloading.md)
