---
tags: [论文, 多无人机协同, 轨迹优化, 多智能体强化学习, 路由]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/alam2024JointTrajectoryControl.md
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
  - NS-3 v3.35
frameworks:
  - PyTorch 1.7.1
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Alam2024 多UAV群网络联合轨迹频谱与路由控制

## 单行摘要
论文面向灾后监测与通信覆盖的 UAV 群网络，把轨迹控制、频段分配和多跳路由统一到同一 cross-layer 决策问题，并用带 LSTM actor 与注意力 critic 的分布式 MA-DDPG 求解。

## 题目驱动研究框架
- 研究场景：灾后监测与空中通信覆盖下的 UAV swarm network。
- 研究对象：多架协同飞行 UAV、固定基站、时变多跳链路与共享频段。
- 核心问题：在高机动、强干扰、链路易断和能量受限条件下，如何同时控制轨迹、分配频段并选择中继路由。
- 标题承诺的方法：joint trajectory control + frequency allocation + routing，并采用 multi-agent deep reinforcement learning。
- 期望效果：降低端到端时延、提高投递率，同时减少能耗并保持群体拓扑稳定。
- 标题与正文的偏差：标题较准确，但正文真正的亮点在于把两跳邻居信息、群体行为规则和 attentional critic 联合进一个分布式训练框架。

## Algorithm Design 快照
论文针对灾后任务中的多UAV群网络，研究在拓扑快速变化、频谱共享和多跳中继耦合条件下，如何联合优化 UAV 轨迹、频段选择和下一跳路由。问题本质上是一个受链路稳定性、SINR、排队时延和剩余能量共同约束的序列决策问题。为此，作者先构造 link utility maximization 问题，再将群体行为规则与分布式 MA-DDPG 结合：actor 端用 LSTM 提取一跳与两跳邻居的时序状态，critic 端用多头注意力建模邻居影响，最终输出连续轨迹控制和离散频段/中继决策，以提升路由稳定性与整体网络性能。

## 图1系统框架草案
- 系统实体：多架四旋翼 UAV、一个地面基站、共享无线信道、机载队列和电池。
- 任务/数据流：各 UAV 采集监测数据后，经多跳空空链路中继至基站；路由质量受位置、频段选择和邻居负载共同影响。
- 控制/优化变量：每架 UAV 的运动控制输入、频段选择、下一跳中继选择。
- 约束来源：最小安全间距、最大通信范围、速度/加速度上界、SINR 门限、队列长度和剩余能量约束。
- 画图提醒：如果后续画图，建议把“行为规则层 + actor/critic 决策层 + 网络链路层”三层叠放，能更直观体现 cross-layer 特征。

## System Model
- 系统在 3D 任务区域中按时隙运行，每架 UAV 通过 GPS 感知自身位置，并依赖一跳/两跳邻居信息维持连通拓扑。
- 链路质量不仅由几何距离决定，还与同时传输造成的干扰、频段占用和未来一段时间的 link duration 相关。
- 论文显式建模了信道、排队时延和能耗，使路由决策不再是纯拓扑最短路，而是跨物理层、MAC 层和网络层的综合决策。
- 轨迹控制采用群体行为规则，利用 cohesion、alignment、separation 保持编队稳定，并通过两跳信息避免局部最优和拓扑分裂。

## Algorithm Design 详解
- 第一步是问题抽象：作者把稳定链路、SINR、排队负载和剩余能量组合成 link utility，并在多项物理约束下构造联合优化问题。
- 第二步是 MDP 建模：每架 UAV 被视为 agent，观测包含运动规则、信道/频段状态、队列信息和两跳邻居特征，动作为连续轨迹控制与离散频段/中继选择。
- 第三步是 actor 设计：利用三组 LSTM state representation layers 提取时序依赖，缓解时变拓扑导致的状态非平稳。
- 第四步是 critic 设计：多头注意力 critic 不做全局集中式拼接，而是有选择地关注一跳邻居，既减少复杂度，也提高协同学习稳定性。
- 第五步是执行逻辑：通过 cooperative training 学出每架 UAV 的局部策略，在分布式执行时同时实现轨迹自组织、频段避让和稳定路由。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：`NS-3 v3.35`；`PyTorch 1.7.1`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文以数值仿真为主，已经给出部分实验资产信息，但仍缺少更强的真实部署证据。

## Introduction 写作素材
- 在 UAV 群网络里，路由性能并不只由网络层决定，而与轨迹控制和频谱复用强耦合。
- 只做最短路或只做拓扑控制，往往无法同时解决链路断裂、排队拥塞和同频干扰问题。
- 因此，更合理的问题定义是“跨层联合决策”，而不是把轨迹、MAC 和路由拆成彼此独立的模块。
- 这篇论文很适合支撑“多UAV网络控制从局部启发式走向学习型联合优化”的引言论证。

## Related Work 写作素材
- 与只优化轨迹或只优化频谱的工作相比，本文把频段分配、路由和行为控制放进同一个目标函数中。
- 与只看一跳邻居的分布式 MARL 相比，本文显式引入两跳信息和注意力 critic 来降低局部最优风险。
- 与传统路由协议相比，本文把 link duration、队列和剩余能量作为可学习决策因素，而非固定启发式指标。
- 相关综述中可把它归入“群网络 cross-layer MARL”路线，和[[Yuan2025_多UAV无线网络轨迹与功率联合优化]]形成方法互补。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[多无人机协同]]
- [[轨迹优化]]
- [[多智能体强化学习]]
- [[轨迹优化与协同控制]]

## 来源
- [原文](../raw/markdown/alam2024JointTrajectoryControl.md)
