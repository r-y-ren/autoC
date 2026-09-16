---
tags: [论文, 任务卸载, 边云协同, 多无人机协同, Lyapunov]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/bai2024DelayAwareCooperativeTask.md
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
  - prototype
data_origin:
  - mixed
platforms: []
frameworks: []
datasets: []
hardware_stack:
  - Pixhawk flight controller
  - Jetson Nano
  - T2088 power supply module
  - MorningCore star-network module
  - AXI 4120 brushless motor
artifact_availability: unknown
reproducibility_level: medium
---

# Bai2024 多UAV边云协同时延感知任务卸载

## 单行摘要
论文在弱基础设施场景下把多UAV边缘集群与远端云协同起来，研究时延最小化任务卸载问题，并用 Lyapunov 优化在长期电池预算下实现多UAV协同卸载。

## 题目驱动研究框架
- 研究场景：地面基础设施薄弱时，由多UAV构成现场边缘集群并与远端云协同。
- 研究对象：多架配备边缘计算单元的 UAV、基站、远端云和实时任务流。
- 核心问题：任务在 UAV 集群内部、UAV 到云之间如何协同卸载，才能在电池预算下压低系统总时延。
- 标题承诺的方法：delay-aware cooperative task offloading for multi-UAV enabled edge-cloud computing。
- 期望效果：缓解负载不均衡，提高实时任务处理能力，同时避免单个 UAV 过载。
- 标题与正文的偏差：标题强调 cooperative offloading，但正文真正的关键在于“UAV 集群内部并行处理 + 云端补充算力 + 长期能量约束”。

## Algorithm Design 快照
论文针对弱基础设施场景中的多UAV边缘云协同系统，研究在任务分布不均、UAV 电池有限和链路时变条件下，如何最小化总时延。系统既允许任务在 UAV 集群内部通过 LAN 协同处理，也允许任务经基站卸载到远端云，因此卸载决策同时耦合了局域协同、空地传输和云端转发。作者构建包含 LAN 传输、UAV-to-cloud 传输与并行计算的时延/能耗模型，并把长期电池预算写入约束，再用 Lyapunov 优化把长期问题转化为逐时隙决策，实现多UAV边云协同时延控制。

## 图1系统框架草案
- 系统实体：多架带边缘计算单元的 UAV、局域协同网络、地面基站、远端云。
- 任务/数据流：任务先在本机、本地 UAV 集群和远端云三类目的地之间分流；集群内部并行处理，远端云经 BS 中转。
- 控制/优化变量：卸载比例矩阵、每架 UAV 的 CPU 频率、UAV 到云的传输选择。
- 约束来源：单天线接入方式、UAV 计算能力、电池长期预算、UAV-to-BS 传输速率与云转发时延。
- 画图提醒：画图时应把“UAV cluster 内并行计算”和“UAV-to-cloud 经 BS 中转”明确画成两条路径。

## System Model
- 论文区分了三类处理方式：UAV 集群内部通过 LAN 协同分担、UAV 经 BS 向云端卸载、以及本地本机计算。
- UAV-to-cloud 传输采用加权 LoS/NLoS 空地信道模型，并显式考虑 BS 到远端云的有线中继延迟。
- 在计算侧，作者假设通过虚拟机/容器化实现异构 UAV 间任务兼容，因此来自不同 UAV 的子任务可以在集群中并行执行。
- 系统目标是在长期平均能量预算下最小化总服务时延，而不是单时隙贪心最短时延。

## Algorithm Design 详解
- 第一步是时延/能耗拆解：作者把总时延分为 LAN 传输、UAV 集群并行计算和云端卸载时延三部分，把能耗分为局域传输、UAV 计算和云方向传输能耗。
- 第二步是长期问题建模：由于 UAV 电池有限，目标函数不仅要最小化时延，还要满足长期能量预算约束。
- 第三步是 Lyapunov 转化：通过引入虚拟队列，把长期约束问题转换为逐时隙可求的控制问题。
- 第四步是逐时隙协同决策：每个时隙联合决定任务在 UAV 集群与云之间的分配比例，并考虑并行计算带来的 completion time 由最慢子任务决定这一特性。
- 第五步是实验验证：论文还给出基于真实 UAV-EC 平台的验证，而不仅仅是纯仿真。

## 实验证据卡片
- 验证类型：数值仿真；原型系统/测试床验证
- 数据来源：混合来源
- 平台与软件：未说明
- 硬件与算力：`Pixhawk flight controller`；`Jetson Nano`；`T2088 power supply module`；`MorningCore star-network module`；`AXI 4120 brushless motor`
- 开源情况：代码或资产已公开
- 复现判断：`high`
- 证据备注：论文包含物理平台或测试床验证，比纯仿真更接近工程落地，但外推到大规模系统仍需谨慎。

## Introduction 写作素材
- 在弱基础设施环境下，单个 UAV 的边缘算力和电量都难以稳定支撑实时任务。
- 仅做“UAV 辅助卸载”还不够，真正的问题是如何把多UAV边缘集群与远端云放进同一套时延模型中。
- 负载不均衡会直接破坏实时性，因此 cooperative offloading 的价值在于把局部可用算力真正组织起来。
- 这篇论文适合支撑“从单UAV边缘扩展到多UAV边云协同”的问题引入。

## Related Work 写作素材
- 与只考虑单UAV MEC 的论文相比，本文显式建模了集群内部并行协同。
- 与只研究边缘或只研究云卸载的工作相比，本文同时考虑 UAV cluster 与 remote cloud 两层目的地。
- 与静态优化思路相比，本文使用 Lyapunov 处理长期电池预算，使方法更接近持续运行系统。
- 相关工作写作时，它很适合放在“edge-cloud cooperative offloading”分支，与[[Huang2024_多UAV车载边缘计算动态任务卸载]]和[[Dai2024_车联网中的UAV辅助任务卸载]]形成层次递进。

## 相关系统建模页
- [[计算卸载模型]]
- [[任务队列与时延保障模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[任务卸载]]
- [[资源分配]]
- [[Lyapunov优化]]
- [[多无人机协同]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [原文](../raw/markdown/bai2024DelayAwareCooperativeTask.md)
