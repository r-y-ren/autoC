---
tags: [论文, NOMA, 无线覆盖, 能效, UAV基站]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/tong2023EnergyefficientUAVNOMAAided.md
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
data_origin:
  - synthetic
platforms:
  - MATLAB
  - CVX
frameworks:
  - Dinkelbach method
  - BCD
  - convex optimization
  - NOMA
hardware_stack: []
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Tong2023_面向海量连接的能效UAV-NOMA无线覆盖

## 单行摘要
论文把 `UAV-BS + G-BS + NOMA` 组合成面向海量连接的无线覆盖方案，通过联合优化 UAV 轨迹、功率分配与地面基站预编码，在提升覆盖能力的同时最大化系统能效。

## 题目驱动研究框架
- 研究场景：UAV 基站辅助地面基站的无线覆盖网络。
- 研究对象：`UAV-BS`、`G-BS`、小区边缘用户与海量连接用户群。
- 核心问题：UAV 覆盖灵活但能量受限，NOMA 能支持海量接入但资源耦合复杂。
- 标题承诺的方法：以能效最大化为目标做联合轨迹和功率分配。
- 期望效果：兼顾大范围覆盖、海量连接和 UAV 能耗可持续性。

## Algorithm Design 快照
这篇论文把 UAV 引入 NOMA 覆盖后，重点不是单独做速率提升，而是重新平衡“覆盖增益”和“飞行能耗”。作者因此把 UAV 轨迹优化和功率分配做成两个可交替求解的凸子问题，并同时考虑地面基站预编码对整体能耗的影响，使得 `UAV-BS` 不只是空中补点，而是和地面网络联合组织覆盖能力。

## 图1系统框架草案
- 地面层：`G-BS` 负责小区中心用户和部分预编码控制。
- 空中层：`UAV-BS` 负责边缘用户覆盖增强。
- 多址层：`NOMA` 使同一资源块内支持更多用户连接。
- 优化层：联合优化 UAV 轨迹、功率分配和 G-BS 预编码。
- 目标层：在 massive connections 场景下提升能效。

## System Model
### 1. 协同覆盖架构
- 地面基站和 UAV 基站共同承担无线覆盖任务。
- `UAV-BS` 主要面向边缘用户，`G-BS` 面向中心区域用户。

### 2. NOMA 接入模型
- 不同用户复用同一资源块，通过功率域区分并使用 `SIC` 解码。
- 海量连接能力来自资源块复用而非单纯增加频谱。

### 3. 优化目标
- 最大化系统能效。
- 同时约束 UAV 飞行动力学、用户平均吞吐和功率预算。

## Algorithm Design 详解
### 1. 分式目标处理
- 用 `Dinkelbach` 方法处理能效最大化的分式目标。
- 将原问题拆分为轨迹优化和功率分配两个子问题。

### 2. 交替优化
- 用 `BCD` 在 UAV 轨迹与功率变量之间交替更新。
- 再单独优化 `G-BS` 预编码，以降低地面侧功耗同时维持吞吐。

### 3. 研究意义
- 论文说明 `NOMA + UAV` 的价值不只是多连几个用户，而是能在海量连接场景中把覆盖设计和能耗设计绑定起来。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成蜂窝覆盖与海量连接场景
- 平台与软件：`MATLAB`、`CVX`
- 方法组件：`Dinkelbach method`、`BCD`、`convex optimization`、`NOMA`
- 评测指标：能效、覆盖性能、平均吞吐、功率消耗
- 对比对象：传统覆盖方案、非联合优化方案
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露代码与仿真配置脚本

## Introduction 写作素材
- 海量连接和广域覆盖的同时满足，是未来空中通信系统的基础张力之一。
- UAV 能显著改善边缘覆盖，但其能量瓶颈决定了设计目标必须转向能效而非单纯速率。
- 这篇论文适合支持“UAV 覆盖和 NOMA 多址需要被联合设计”的写作表述。

## Related Work 写作素材
- 既有 UAV 覆盖工作强调轨迹或高度设计。
- 既有 NOMA 工作强调资源块复用和 `SIC` 性能。
- 本文将两者统一到能效框架，是通信主线里“massive connections + aerial coverage”的代表之一。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[区域覆盖与部署模型]]

## 相关概念与主题页
- [[UAV-NOMA覆盖]]
- [[轨迹优化]]
- [[空中通信与协同传输]]
- [[无人机部署优化]]
- [[信道与通信速率模型]]

## 来源
- [原文](../raw/markdown/tong2023EnergyefficientUAVNOMAAided.md)
