---
tags: [论文, 协同安全通信, 扩散模型强化学习, UAV集群]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/zhang2025MultiobjectiveAerialCollaborative.md
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
  - Ubuntu 22.04.3 LTS
frameworks:
  - PyTorch 2.2.2
  - CUDA 11.8
  - GDMTD3
  - TD3
  - diffusion model
datasets: []
hardware_stack:
  - NVIDIA GeForce RTX 3090 GPU
  - Intel Core i9-13900K CPU
  - 128 GB RAM
artifact_availability: unknown
reproducibility_level: medium
---

# Zhang2025_生成扩散模型驱动的多目标空中协同安全通信

## 单行摘要
论文面向移动窃听者威胁下的 UAV 集群协同波束安全通信，联合优化激励电流权重与 UAV 位置，并用 GDMTD3 在保密速率和飞行能耗之间学习多目标折中策略。

## 题目驱动研究框架
- 研究场景：UAV 蜂群将敏感监视数据远程回传到基站，并受到移动窃听者威胁。
- 研究对象：构成虚拟天线阵列的多架 UAV、远端基站和移动窃听者。
- 核心问题：如何在提升保密速率的同时抑制队形调整带来的额外飞行能耗。
- 标题承诺的方法：generative diffusion model-enabled DRL for multi-objective aerial collaborative secure communication optimization。
- 期望效果：在高维连续动作空间中获得更好的保密-能耗折中性能。

## Algorithm Design 快照
这篇论文把 UAV 集群安全通信写成“协同波束形成 + 机动控制”的连续多目标优化问题。每架 UAV 都既是阵列单元又是运动体，因此需要同时决定激励电流权重和空间位置。作者没有直接用普通 TD3，而是引入[[扩散模型强化学习]]来更好刻画高维动作分布，从而在保密速率和飞行能耗之间学到更平滑、更稳定的折中策略。

## 图1系统框架草案
- 通信层：多架 UAV 构成空中虚拟天线阵列。
- 威胁层：移动窃听者持续改变位置。
- 控制层：联合决定 UAV 位置与阵列激励权重。
- 学习层：GDMTD3 处理高维连续动作分布。
- 目标层：最大化保密速率并最小化飞行能耗。

## System Model
### 1. UVAA 安全通信场景
- 多架 UAV 通过协同波束形成增强期望方向信号。
- 移动窃听者使最优阵列构型和飞行位置持续变化。

### 2. 动作与状态
- 动作包括各 UAV 激励电流权重和三维位置调整。
- 状态包括基站位置、窃听者位置、当前编队状态和链路信息。

### 3. 多目标优化
- 一类目标是提升空地链路保密速率。
- 另一类目标是限制 UAV 编队调整带来的飞行能耗。

## Algorithm Design 详解
### 1. ASCEE-MOP
- 论文先把问题形式化为保密速率与能耗的双目标优化。
- 该问题非凸、NP-hard 且环境动态变化。

### 2. GDMTD3
- 在 TD3 的 actor 生成过程中加入扩散模型。
- 这样比常规全连接 actor 更适合高维连续动作分布建模。

### 3. 研究意义
- 论文把“空中协同安全通信”从传统轨迹/功率优化推进到生成模型辅助控制。
- 也说明多 UAV 安全通信正逐步吸收生成式 AI 工具链。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成安全通信场景
- 平台与软件：`Ubuntu 22.04.3 LTS`、`PyTorch 2.2.2`、`CUDA 11.8`
- 硬件与算力：`RTX 3090 GPU`、`Intel i9-13900K CPU`、`128 GB RAM`
- 对比对象：四类部署策略与五类 DRL 基线
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露统一代码与更细粒度超参数脚本

## Introduction 写作素材
- 多 UAV 协同安全通信的关键矛盾已经从“能不能保密”转向“保密性能和机动成本如何动态平衡”。
- 当动作空间同时包含阵列权重和三维位置时，传统 DRL 表示能力开始受限。
- 这篇论文适合支撑“生成式模型正在进入空中协同安全通信优化”的写作判断。

## Related Work 写作素材
- 传统 UAV 安全通信多关注单 UAV 或低维轨迹/功率控制。
- 传统多 UAV 协同波束问题又较少引入生成模型处理高维连续动作。
- 这篇论文把扩散模型、TD3 和空中协同安全通信真正连到一起。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[空中协同安全通信]]
- [[扩散模型强化学习]]
- [[协同波束赋形]]
- [[安全与服务保障]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/zhang2025MultiobjectiveAerialCollaborative.md)
