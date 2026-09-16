---
tags: [论文, 目标跟踪, 无人机定位, 协同强化学习]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/zhu2024CollaborativeReinforcementLearning.md
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
frameworks:
  - ZD-RL
  - distributional reinforcement learning
  - TSWLS
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Zhu2024_协同强化学习的三维UAV跟踪与定位

## 单行摘要
论文利用 `1` 架主动 UAV 与 `4` 架被动 UAV 组成协同定位系统，联合优化主动 UAV 发射功率与多机轨迹，并提出基于 Z function decomposition 的协同强化学习方法，在三维目标 UAV 跟踪中显著降低定位误差。

## 题目驱动研究框架
- 研究场景：需要实时定位并跟踪三维空间中移动目标 UAV 的无线定位系统。
- 研究对象：一架主动发射 UAV、四架被动接收 UAV、地面 BS、目标 UAV。
- 核心问题：目标高速移动、三维坐标估计复杂、功率与轨迹共同影响定位精度。
- 标题承诺的方法：以 collaborative reinforcement learning 做 3D UAV tracking 的 trajectory design。
- 期望效果：通过协同决策降低目标 UAV 定位误差。

## Algorithm Design 快照
与常见“单机跟踪”不同，这篇论文让一架主动 UAV 发射信号，四架被动 UAV 接收反射信号，再由 BS 做目标位置估计。由于定位精度取决于几何布局和 SNR，主动 UAV 的功率控制与全部 UAV 的轨迹设计被统一建模。作者进一步用 ZD-RL 替代普通 value decomposition，直接学习未来回报分布，从而改善协同训练的稳定性与定位精度。

## 图1系统框架草案
- 主动层：一架主动 UAV 发射定位信号。
- 感知层：四架被动 UAV 接收反射信号并估计传播距离。
- 融合层：BS 汇聚多 UAV 距离信息并估计目标位置。
- 控制变量：主动 UAV 发射功率、主动/被动 UAV 轨迹。
- 优化目标：最小化目标 UAV 的实时三维定位误差。

## System Model
### 1. 主动-被动协同定位结构
- 一架主动 UAV 发射信号，四架被动 UAV 接收回波。
- 多个接收节点共同提供三维定位所需的几何约束。
- BS 利用多路测距信息估计目标 UAV 坐标。

### 2. 功率与轨迹耦合
- 被动 UAV 与目标间距离会影响测距精度。
- 主动 UAV 发射功率影响 SNR，从而影响定位误差。
- 因此功率和轨迹必须联合优化。

### 3. 定位误差分析
- 论文不仅做学习算法，还分析了受控 UAV 相对目标的位置如何影响最小可达定位误差。
- 这让它兼具方法论文和几何建模论文属性。

## Algorithm Design 详解
### 1. ZD-RL
- 相比传统 value decomposition，ZD-RL 学习未来奖励分布而非单一期望值。
- 这有助于多 UAV 协同定位中的稳定训练和更精细回报评估。

### 2. 协同控制
- 多架受控 UAV 共同决定轨迹，主动 UAV 还需决定发射功率。
- 所有动作共同服务于定位误差最小化，而不是通信吞吐最大化。

### 3. 实验结论
- 相比 `VD-RL` 和独立 DRL，ZD-RL 分别可将定位误差最多降低 `39.4%` 和 `64.6%`。
- 在代表性场景中，所提方法获得约 `1.61m` 的最小定位误差。
- 它代表了“协同 RL + 无线定位”这条很有潜力的交叉方向。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：三维 UAV 跟踪合成场景
- 平台与软件：未说明
- 硬件与算力：未说明
- 场景设置：`5` 架受控 UAV 与 `1` 个 BS 协同定位目标 UAV；时隙长度 `1s`，UAV 速度 `10m/s`
- 对比基线：`VD-RL`、独立 DRL
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露训练平台、代码与完整超参数实现细节

## Introduction 写作素材
- UAV 跟踪若进入三维高速目标场景，单传感器或单控制器方法很快失效。
- 定位精度不仅取决于感知算法，也取决于多 UAV 空间布局与发射功率。
- 这篇论文适合支撑“轨迹优化正在从服务提供扩展到协同定位与空中感知”的写作判断。

## Related Work 写作素材
- 传统 UAV 跟踪往往只优化观测或只做路径规划。
- 现有定位方法往往假设中心控制器掌握完美信息，或忽略发射功率对定位精度的影响。
- 本文把功率控制、轨迹设计和三维定位精度统一进协同强化学习框架。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[目标跟踪]]
- [[无人机定位]]
- [[轨迹优化与协同控制]]
- [[多无人机协同]]

## 来源
- [原文](../raw/markdown/zhu2024CollaborativeReinforcementLearning.md)
