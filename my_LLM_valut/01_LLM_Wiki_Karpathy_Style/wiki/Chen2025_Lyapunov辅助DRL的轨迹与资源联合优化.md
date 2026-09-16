---
tags: [论文, 轨迹优化, 资源分配, 深度强化学习, Lyapunov]
created: 2026-04-06
updated: 2026-04-08
sources:
  - ../raw/markdown/chen2025JointTrajectoryOptimization.md
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
frameworks:
  - PyTorch 1.10.0
datasets: []
hardware_stack:
  - NVIDIA RTX 4070 Ti GPU
  - Intel Core i7-13650HX CPU
artifact_availability: unknown
reproducibility_level: medium
---

# Chen2025 Lyapunov 辅助 DRL 的轨迹与资源联合优化

## 单行摘要
论文提出 JTORA，将 Lyapunov 优化、SAC 与凸优化拼接为混合框架，在随机任务到达和用户移动条件下联合优化 UAV 轨迹、通信资源和计算资源。

## 题目驱动研究框架
- 研究场景：带用户移动和随机任务到达的 UAV-MEC 系统。
- 研究对象：单个带边缘服务器的 UAV、多个移动用户、长期运行中的任务队列。
- 核心问题：如何在保证 UAV 续航的同时，联合决定 UAV 位置、用户发射功率与本地 CPU 频率，以降低用户能耗。
- 标题承诺的方法：Lyapunov-assisted DRL 的 joint trajectory optimization and resource allocation。
- 期望效果：在高动态环境中实现更低能耗与更稳定的长期服务性能。
- 标题与正文的偏差：标题已经比较准确，但正文的关键突破不只是“轨迹 + 资源”，还包括把随机到达、用户移动和长期约束同时放入统一混合优化框架。

## Algorithm Design 快照
论文针对单 UAV 服务多个移动用户的 UAV-MEC 场景，研究在随机任务到达、用户移动和动态信道条件下，如何联合优化 UAV 轨迹、通信资源与计算资源。问题本质上是一个带长期能量约束的多阶段 MINLP，传统解析法和纯 DRL 都难以独立处理。为此，论文先用 Lyapunov 优化把长期约束转化为逐时隙确定性问题，再把问题拆为两部分：轨迹与通信资源由 SAC 负责，计算资源分配由凸优化求解析解。最终目标是在保证 UAV 续航和队列稳定的同时，尽可能降低移动用户总能耗。

## 图1系统框架草案
- 系统实体：一个带边缘服务器的 UAV、多个移动用户、用户本地 CPU、UAV 侧计算资源。
- 任务/数据流：用户任务到达后，一部分本地计算，一部分通过空地链路卸载给 UAV；UAV 通过机动调整位置改善链路质量。
- 控制/优化变量：UAV 位置、用户发射功率、用户 CPU 频率、UAV 计算资源分配。
- 约束来源：Gauss-Markov 用户移动、LoS/NLoS 信道、UAV 能量预算、任务队列稳定性、每时隙资源上界。
- 画图提醒：如果后续画图，建议把“任务队列 + 虚拟能量队列 + 决策模块”并置展示，这样更能体现 Lyapunov 在系统中的作用。

## System Model
- 系统采用等长时隙建模，用户位置遵循 Gauss-Markov 移动模型，任务随机到达并进入用户任务队列。
- 通信链路采用概率 LoS 模型，并基于 UAV 与用户的相对位置决定传输速率，因此 UAV 轨迹会直接影响卸载收益。
- 用户任务既可本地处理，也可部分卸载给 UAV；因此系统同时包含本地 CPU 频率控制与空口发射功率控制。
- UAV 在固定高度飞行，但受最大速度与总能量约束；论文还引入能量队列与任务队列，使长期性能分析成为可能。

## Algorithm Design 详解
- 第一步是 Lyapunov 转化：把长期能量与队列稳定性条件写入 Lyapunov drift-plus-penalty 框架，将原始多阶段 MINLP 转化为逐时隙优化。
- 第二步是问题分解：计算资源分配子问题结构清晰，可通过凸优化得到解析形式；轨迹与通信资源子问题则由 SAC 处理连续控制。
- 第三步是混合求解：SAC 负责学习 UAV 位置控制策略，凸优化负责给定位置下的功率与 CPU 分配，从而避免 DRL 独自承担全部求解压力。
- 第四步是性能分析：论文进一步给出算法复杂度和长期性能分析，使 JTORA 不只是经验性工程拼接，而是具有理论边界的混合优化方法。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：`Python 3.8`；`PyTorch 1.10.0`
- 硬件与算力：`NVIDIA RTX 4070 Ti GPU`；`Intel Core i7-13650HX CPU`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文以数值仿真为主，已经给出部分实验资产信息，但仍缺少更强的真实部署证据。

## Introduction 写作素材
- 单纯假设“用户静止”或“只有 UAV 移动”会显著简化问题，但与真实空地协同系统不符。
- 在动态场景下，传统解析优化很难快速响应环境变化，而纯 DRL 又容易在强结构问题上失去稳定性和泛化性。
- 因此，一个合理的问题表述不是“优化轨迹”本身，而是“如何让长期约束、连续控制和结构化资源分配共存”。
- 这篇论文很适合支撑 introduction 中“为什么需要混合智能优化框架”的论证。

## Related Work 写作素材
- 与只做资源分配的工作相比，本文把 UAV 轨迹真正拉进主问题，而不是视为外生变量。
- 与只做轨迹优化的工作相比，本文同时处理通信资源与计算资源，因此系统耦合度更高。
- 与纯 DRL 路线相比，本文保留了凸优化对结构化变量的解析能力；与纯 Lyapunov 路线相比，它又引入了 SAC 来应对复杂连续状态控制。
- 相关综述写作时，可以把它放在“Lyapunov + learning hybrid”方法线上，和[[Dai2024_车联网中的UAV辅助任务卸载]]形成前后衔接。

## 相关系统建模页
- [[计算卸载模型]]
- [[任务队列与时延保障模型]]
- [[无人机能耗模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[轨迹优化]]
- [[资源分配]]
- [[深度强化学习]]
- [[Lyapunov优化]]
- [[任务卸载]]
- [[轨迹优化与协同控制]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/chen2025JointTrajectoryOptimization.md)
