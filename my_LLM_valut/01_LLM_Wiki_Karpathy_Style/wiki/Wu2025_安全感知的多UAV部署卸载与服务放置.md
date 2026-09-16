---
tags: [论文, 安全, 服务放置, 多智能体强化学习, UAV辅助MEC]
created: 2026-04-06
updated: 2026-04-08
sources:
  - ../raw/markdown/wu2025SecurityawareDesignsMultiUAV.md
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
  - TensorFlow 2.6.0
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Wu2025 安全感知的多 UAV 部署卸载与服务放置

## 单行摘要
论文把多 UAV MEC 中的部署、任务卸载、服务放置和安全窃听问题统一建模，并通过 cooperative jamming 与 OE-MATD3 联合最小化设备任务完成时延。

## 题目驱动研究框架
- 研究场景：无地面基础设施或地面覆盖不足时的多 UAV-assisted MEC 网络。
- 研究对象：无线设备、多个 UAV 服务器、一个 UAV jammer、窃听者、异构服务程序。
- 核心问题：在有限缓存、安全卸载和能量约束下，设备该卸载到哪里、UAV 该如何部署、哪些服务程序该缓存、干扰该如何施加。
- 标题承诺的方法：security-aware designs of deployment, task offloading and service placement。
- 期望效果：在满足安全和缓存约束的同时，尽量降低设备总任务完成时延。
- 标题与正文的偏差：标题已经抓住了三个主变量，但正文还额外把 UAV jammer 位置/功率和设备发射功率作为关键变量，因此实际问题比标题显示的更“安全系统化”。

## Algorithm Design 快照
论文研究多 UAV 边缘计算网络中，设备在存在窃听者的情况下如何安全地把任务卸载给缓存了对应服务程序的 UAV 服务器。困难在于卸载合法性取决于服务是否已缓存，卸载安全性又受到窃听链路影响，而 UAV 部署、服务放置、干扰功率和设备发射功率彼此强耦合。为此，论文设计 cooperative jamming 方案，用 UAV jammer 抑制窃听，并把多 UAV 部署、设备关联、服务缓存、干扰功率与设备功率统一写成时延最小化问题。求解上，论文用 OE-MATD3 处理 UAV 相关离散-连续联合决策，并推导设备发射功率闭式解来嵌入学习过程。

## 图1系统框架草案
- 系统实体：多个 UAV 服务器、一个 UAV jammer、多个无线设备、多个 eavesdropper、服务程序集合。
- 任务/数据流：设备任务可本地计算，也可上传到缓存了所需服务程序的 UAV；上传过程中 jammer 发送人工噪声干扰窃听者。
- 控制/优化变量：设备-服务器关联、服务放置变量、UAV 与 jammer 位置、jamming power、设备发射功率。
- 约束来源：缓存空间、最坏情况安全卸载速率、执行时延容忍度、设备和 UAV 能量限制、UAV 最小安全间距。
- 画图提醒：画图时要把“service placement”与“secure offloading”画成同级模块，否则很容易把服务缓存误当成次要实现细节。

## System Model
- 设备生成异构任务，每类任务对应特定服务程序，因此“能不能卸载”首先取决于 UAV 服务器是否预缓存了对应服务。
- 由于空地链路具有 LoS 和广播特性，设备向 UAV 卸载任务时可能被窃听，因此论文引入 UAV jammer 发送干扰信号来提升安全卸载速率。
- 论文显式写出设备本地计算与 UAV 计算两类时延/能耗模型，同时用二元变量连接设备关联与服务放置决策。
- 目标函数是设备总任务完成时延最小化，但可行域受到缓存空间、安全卸载速率、时延容忍和能量约束共同塑造。

## Algorithm Design 详解
- 第一步是问题分解：原问题是典型的 MINLP，既有离散变量（关联与缓存），也有连续变量（位置、功率、算力分配）。
- 第二步是优化嵌入：论文先推导设备发射功率的闭式解，使一部分结构化变量不必完全交给 RL 盲搜。
- 第三步是 OE-MATD3：对 UAV 相关变量，包括部署、关联、服务放置和 jamming power，使用 MATD3 进行联合决策学习。
- 第四步是安全协同：通过 jammer 和 secrecy offloading constraints 把物理层安全显式写进系统决策，使“安全”从附加条件变成核心优化对象。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：`Python 3.8`；`TensorFlow 2.6.0`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文以数值仿真为主，已经给出部分实验资产信息，但仍缺少更强的真实部署证据。

## Introduction 写作素材
- UAV-assisted MEC 网络中，计算效率问题和无线安全问题是同时存在的，不能分开看。
- 当任务类型异构时，缓存资源限制会直接改变合法卸载集合，因此服务程序放置不是边角问题，而是系统主变量。
- 如果只优化卸载而不考虑缓存和窃听，得到的方案往往在真实系统中既不可执行，也不安全。
- 这篇论文很适合支撑“从性能优化走向安全可部署系统”的 introduction 段落。

## Related Work 写作素材
- 与只做 UAV-assisted MEC 卸载的工作相比，本文把服务放置和窃听安全一起纳入主问题。
- 与只做 secure offloading 的工作相比，本文不仅关注链路安全，还考虑了服务程序是否存在于目标节点。
- 与传统优化方法相比，本文用 optimization-embedding DRL 处理强耦合的多 UAV 决策问题，兼顾了解析结构和学习灵活性。
- 写 related work 时，可把它归入“security-aware service provisioning”分支，与[[Chen2025_Lyapunov辅助DRL的轨迹与资源联合优化]]这类偏性能导向工作形成鲜明对比。

## 相关系统建模页
- [[计算卸载模型]]
- [[服务放置模型]]
- [[无人机能耗模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[服务放置]]
- [[任务卸载]]
- [[多智能体强化学习]]
- [[安全与服务保障]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/wu2025SecurityawareDesignsMultiUAV.md)
