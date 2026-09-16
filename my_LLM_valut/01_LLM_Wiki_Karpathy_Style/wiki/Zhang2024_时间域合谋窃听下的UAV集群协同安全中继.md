---
tags: [论文, 协同安全中继, 时间域合谋窃听, 协作波束形成]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/zhang2024UAVSwarmenabledCollaborative.md
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
  - collaborative beamforming
  - improved multi-objective grasshopper algorithm (IMOGOA)
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Zhang2024_时间域合谋窃听下的UAV集群协同安全中继

## 单行摘要
论文利用 UAV swarm 作为协同安全中继，为配备平面阵列的地面微基站与 IoT 终端之间建立 collaborative beamforming 中继链路，并针对时间域合谋窃听者联合优化阵列激励、接收 UAV 选择、机群位置与用户关联顺序。

## 题目驱动研究框架
- 研究场景：IoT 终端与地面微基站之间的空中安全中继通信。
- 研究对象：配备 PAA 的地面 MBS、UAV swarm 虚拟阵列、IoT 终端与时间域合谋窃听者。
- 核心问题：如何同时提升合法用户可达速率、抑制窃听者收益并控制机群能耗。
- 标题承诺的方法：以 UAV swarm-enabled collaborative secure relay communications 应对 time-domain colluding eavesdropper。
- 期望效果：在多目标权衡下获得更好的安全中继折中。

## Algorithm Design 快照
论文的关键不只是“用 UAV 做中继”，而是把 UAV swarm 组织成可协作波束赋形的虚拟阵列，让基站阵列和机群阵列共同参与安全传输设计。围绕这一点，作者构造 US2RMOP 多目标问题，联合优化基站与 UAV 阵列激励电流权重、UAV 接收节点选择、UAV 空间位置和用户服务顺序。由于问题非凸、NP-hard 且规模较大，作者提出 IMOGOA 做近 Pareto 求解。

## 图1系统框架草案
- 源节点：配备平面阵列的地面微基站。
- 中继层：由多架 UAV 组成的虚拟阵列中继系统。
- 目的端：多个 IoT 终端。
- 威胁模型：时间域合谋窃听者跨时隙汇聚截获信息。
- 优化变量：PAA/UVAA 激励权重、UAV 接收器选择、UAV 位置、用户关联顺序。
- 目标：合法总速率最大、窃听总速率最小、机群能耗最小。

## System Model
### 1. 协同安全中继结构
- 地面 MBS 通过 UAV swarm 中继向 IoT 终端传输数据。
- UAV 集群可以形成 UVAA 风格的协同波束赋形结构。
- 这让空间位置与阵列权重耦合为同一安全中继问题。

### 2. 窃听威胁模型
- 窃听者被假设为时间域合谋窃听者，可跨时隙合并信息。
- 因而仅靠瞬时链路优化不足，必须兼顾全局多目标安全折中。

### 3. 多目标问题
- 目标 1：最大化 IoT 终端可达总速率。
- 目标 2：最小化窃听者可达总速率。
- 目标 3：最小化 UAV swarm 能耗。

## Algorithm Design 详解
### 1. US2RMOP
- 问题同时包含阵列权重、UAV 选择、空间位置和关联顺序。
- 变量既有连续空间变量，也有组合离散变量，因此直接求全局最优非常困难。

### 2. IMOGOA
- 论文采用改进多目标蚱蜢优化算法搜索 Pareto 折中。
- 相比传统多跳中继或固定阵列间距策略，IMOGOA 能更充分利用 UAV swarm 的可重构性。

### 3. 实验结论
- 在不同 hop 数和不同传统中继策略对比下，所提策略取得了更好的三目标折中。
- 这篇论文把“协作波束形成”和“安全中继”真正合并成了一个 UAV swarm 问题。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：IoT 中继与窃听场景合成拓扑
- 平台与软件：未说明
- 硬件与算力：未说明
- 场景设置：比较传统多跳中继、LAA relay 与所提 UVAA relay；考察 `2/4/8/16` 架 UAV 等设置
- 对比基线：`MRS`、`LRS` 等传统 UAV 中继策略
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露仿真平台与算法代码

## Introduction 写作素材
- UAV 中继研究若只看覆盖增益，会忽略协同阵列和窃听威胁带来的复杂性。
- 当 UAV swarm 能形成虚拟阵列时，位置控制和阵列控制会强耦合。
- 这篇论文很适合支撑“安全中继已从单链路保密走向机群级协同设计”的写作判断。

## Related Work 写作素材
- 传统 UAV relay 往往重视链路延伸或多跳覆盖，而非安全协同阵列。
- 单 UAV 安全通信难以直接扩展到 swarm 虚拟阵列场景。
- 时间域合谋窃听进一步提高了问题复杂度，使多目标优化更有必要。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[协同安全中继通信]]
- [[时间域合谋窃听]]
- [[协作波束形成]]
- [[安全与服务保障]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/zhang2024UAVSwarmenabledCollaborative.md)
