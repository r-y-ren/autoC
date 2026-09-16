---
tags: [论文, UAV-RIS, RIS辅助通信, 多目标优化, 能效通信]
created: 2026-04-10
updated: 2026-04-10
sources:
  - ../raw/markdown/pan2025CooperativeUAVmountedRISsassisted.md
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
  - synthetic
platforms:
  - MATLAB
  - Python
frameworks:
  - EEComm-MOF
  - INSGA-II-CDC
datasets: []
hardware_stack:
  - Raspberry Pi 4B
artifact_availability: unknown
reproducibility_level: medium
---

# Pan2025_协同UAV挂载RIS能效通信优化

## 单行摘要
论文面向多用户 6G 蜂窝场景，联合优化 BS 波束、协同 UAV-RIS 的三维部署与离散相位，提出 `INSGA-II-CDC` 多目标进化算法，在公平速率、总速率与总能耗之间求 Pareto 折中。

## 题目驱动研究框架
- 研究场景：直达链路受限的蜂窝网络，需要多 UAV 挂载 RIS 协同为地面用户服务。
- 研究对象：BS、多个 UAV-RIS、多个地面用户。
- 核心问题：如何同时兼顾最小可用速率、总可用速率和系统总能耗。
- 标题承诺的方法：cooperative UAV-mounted RISs-assisted energy-efficient communications。
- 期望效果：利用三维机动部署和离散相位控制提升链路质量，并保持系统能效。

## Algorithm Design 快照
作者把多 UAV-RIS 辅助通信写成一个三目标多目标优化框架 `EEComm-MOF`，决策变量同时包含 BS 波束向量、UAV-RIS 三维位置和离散相位。由于该问题既有连续变量又有离散变量，且目标彼此冲突，论文提出 `INSGA-II-CDC`，分别用连续、离散和复数解处理机制增强进化搜索能力，并在最后补上 Raspberry Pi 侧的实现性分析。

## 图1系统框架草案
- 系统实体：地面 BS、多个 UAV-RIS、多个地面用户。
- 控制变量：BS 波束向量、UAV-RIS 三维位置、RIS 离散相位。
- 目标函数：最小可用速率、总可用速率、总能耗。
- 画图提醒：把“3D 部署 + 波束 + 相位”画成三类决策层，能更直观看出多目标耦合。

## System Model
- 网络中直达 BS-GU 链路不可用，通信主要依赖多个 UAV 挂载 RIS 形成的反射链路。
- 每个 RIS 元件采用离散相位量化，更贴近 UAV 硬件负载约束。
- 目标不仅是系统总速率，还显式保留最小可用速率，以体现用户公平性。
- 系统总能耗同时计入 UAV 飞行能耗与通信相关能耗，因此部署位置直接影响能效。

## Algorithm Design 详解
- 第一步：构建三目标 `EEComm-MOF`，统一公平速率、总速率和能耗。
- 第二步：把 UAV-RIS 三维部署、离散相位和 BS 波束写成联合决策变量。
- 第三步：设计 `INSGA-II-CDC`，针对连续/离散/复数变量分别做定制化处理。
- 第四步：通过大规模仿真比较收敛性、稳定性和多目标最优性。
- 第五步：在 Raspberry Pi 4B 上做实现性分析，验证算法在 UAV-RIS 实用平台上的运行时间可接受。

## 实验证据卡片
- 验证类型：`simulation` + `prototype`
- 数据来源：合成场景参数
- 平台与软件：`MATLAB`、`Python`
- 方法组件：`EEComm-MOF`、`INSGA-II-CDC`
- 硬件与算力：`Raspberry Pi 4B`
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未提供统一的工程代码与通信栈实现细节

## Introduction 写作素材
- UAV-RIS 的价值不只是“可移动 RIS”，而是把三维部署自由度引入传播环境设计。
- 多 RIS 协同场景下，公平性、容量和能耗往往天然冲突，单目标最优不足以支撑实际系统设计。
- 因此这类论文很适合支持“UAV-RIS 研究已从单链路增强走向系统级能效设计”的论断。

## Related Work 写作素材
- 与单 UAV-RIS 或二维部署工作相比，本文把多个 UAV-RIS 和三维部署真正联合起来。
- 与连续相位假设不同，本文显式保留离散相位，更接近硬件实现。
- 与单目标速率最大化不同，本文保留了公平性与能耗三目标张力。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[UAV-RIS协同通信]]
- [[RIS辅助通信]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/pan2025CooperativeUAVmountedRISsassisted.md)
