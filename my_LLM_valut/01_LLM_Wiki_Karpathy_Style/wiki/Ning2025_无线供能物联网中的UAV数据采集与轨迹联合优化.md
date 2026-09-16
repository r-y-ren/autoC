---
tags: [论文, 无线供能, 数据采集, 轨迹优化, 多智能体强化学习]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/ning2025JointOptimizationData.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - related_work
validation_type:
  - simulation
  - trace_driven
data_origin:
  - mixed
platforms:
  - Python 3.7
  - PyTorch 1.1.0
frameworks:
  - CMDP
  - MCDRL
  - personalized attention
  - matching theory
datasets:
  - APNIC Melbourne geolocation data
  - YouTube video service dataset
hardware_stack:
  - Intel Xeon Silver 4210R CPU @ 2.40 GHz
artifact_availability: unknown
reproducibility_level: medium
---

# Ning2025 无线供能物联网中的UAV数据采集与轨迹联合优化

## 单行摘要
论文面向多 UAV 辅助的无线供能物联网，联合优化三维轨迹和 `ISD-UAV` 连接分配，在飞行安全、设备 QoS 和任务完成约束下最大化系统能效。

## 题目驱动研究框架
- 研究场景：多 UAV 为大量低电量感知设备提供无线能量补给并回收数据。
- 研究对象：UAV、智能感知设备 ISD、三维飞行位置、安全距离、链路连接关系。
- 核心问题：单靠静态部署难以兼顾供能效率、数据采集效率和多 UAV 安全飞行。
- 标题承诺的方法：joint optimization of data acquisition and trajectory planning。
- 期望效果：在能源受限 IoT 中实现更安全、更高效的多 UAV 数据采集。
- 标题与正文的偏差：正文的关键不只是“联合优化”，而是把安全约束显式写进 `CMDP` 并用多智能体注意力机制学习三维机动。

## Algorithm Design 快照
作者先把多 UAV 轨迹规划写成一个带安全惩罚约束的 `CMDP`，再用 `MCDRL` 学习每架 UAV 的三维移动策略。与普通 MARL 不同，这里每个 UAV 维护奖励 critic 和惩罚 critic，并通过个性化注意力机制动态关注更关键的邻居状态，从而兼顾能效目标与避碰约束。轨迹确定后，论文再用基于匹配理论的分配算法，为覆盖范围内的 ISD 选择最合适的 UAV 服务者，以提升单时隙能效。

## 图1系统框架草案
- 感知层：分布式 ISD，具有剩余电量、数据量和 QoS 需求。
- 空中层：多架 UAV 在三维区域中移动、供能并回收数据。
- 决策层：`MCDRL` 负责轨迹，matching 负责连接分配。
- 约束层：碰撞安全、覆盖半径、任务时限、能量消耗。
- 画图提醒：建议把“轨迹控制”和“连接分配”画成两级决策链，而不是单层联合求解黑盒。

## System Model
- 网络由多 UAV 与大量 ISD 构成，UAV 先移动到合适位置，再对范围内 ISD 供能和采集数据。
- UAV 位置是三维变量，且需要满足最小安全间距，避免空中碰撞。
- ISD 的 QoS、剩余数据量和能源状态会影响连接与服务收益。
- 目标函数本质上是在“系统能效最大化”和“飞行安全约束”之间做平衡。

## Algorithm Design 详解
- 先把 UAV 轨迹子问题写成 `CMDP`，把安全距离违反视为惩罚约束。
- `MCDRL` 使用 actor-critic 与个性化注意力，提升多 UAV 下的协同和可扩展性。
- 再设计 `ISD-UAV` 连接分配算法，根据覆盖范围内的能效优先级确定服务匹配。
- 整体框架说明无线供能数据采集不是单纯路径问题，而是供能、链路、覆盖和安全的多因素联动系统。

## 实验证据卡片
- 验证类型：`simulation` + `trace_driven`
- 数据来源：Melbourne CBD 真实地理位置数据 + YouTube 视频服务数据集驱动的仿真场景
- 平台与软件：`Python 3.7`、`PyTorch 1.1.0`
- 硬件与算力：`Intel Xeon Silver 4210R CPU @ 2.40 GHz`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：真实地理分布和业务数据增强了外部有效性，但仍是数据驱动仿真而非原型系统。

## Introduction 写作素材
- 无线供能 IoT 的核心矛盾不是“能不能连上”，而是“能量先补给谁、数据先采谁、UAV 怎么飞才安全”。
- 多 UAV 带来的收益伴随着碰撞风险和连接管理复杂度，安全约束必须显式进入学习框架。
- 因此，供能型数据采集系统更适合被写成 `轨迹 + 匹配 + 约束` 的分层联合优化。

## Related Work 写作素材
- 既有无线供能 IoT 方法多偏单 UAV 或二维轨迹。
- 既有 RL 轨迹方法常把安全只作为隐含奖励，而非明确约束。
- 该文把 `CMDP + attention-based MARL + matching` 三者组合在一起，是无线供能数据采集线的重要代表。

## 相关系统建模页
- [[无人机能耗模型]]
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[无线供能数据采集]]
- [[无线供能移动边缘计算]]
- [[无人机辅助群智感知与持续作业]]
- [[轨迹优化与协同控制]]

## 来源
- [原文](../raw/markdown/ning2025JointOptimizationData.md)
