---
tags: [论文, SAGIN, ISAC, 移动用户跟踪, 鲁棒波束赋形]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/mao2025UAVassistedCommunicationsSAGINISAC.md
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
  - EKF
  - Bernstein-type inequality
  - SDR
  - SCA
hardware_stack: []
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Mao2025_SAGIN-ISAC中的移动用户跟踪与鲁棒波束赋形

## 单行摘要
论文在 `SAGIN-ISAC` 框架下联合处理移动用户跟踪与鲁棒波束赋形，通过“卫星辅助定位”和“ISAC 本地估计”两套机制，为 UAV 在不完美位置信息下的能效最大化通信提供闭环支撑。

## 题目驱动研究框架
- 研究场景：卫星、空中 UAV 和地面移动用户构成的 `SAGIN-ISAC` 系统。
- 研究对象：多天线 ISAC-UAV、LEO 卫星系统、移动用户 `MUs`。
- 核心问题：移动用户位置不确定导致 CSI 预测失准，进一步削弱 UAV 的定向波束覆盖和能效。
- 标题承诺的方法：把移动用户跟踪和鲁棒波束赋形绑成一个统一问题。
- 期望效果：在 outage 约束下提升通信能效，并减少对卫星侧持续位置信息供给的依赖。

## Algorithm Design 快照
这篇论文的关键不是单纯“做波束优化”，而是先把用户位置获取方式做成两条路线，再把定位误差转写成信道分布不确定性。作者因此把 `space-assisted` 和 `ISAC-assisted` 两套感知机制接到同一个能效最大化问题里，让 UAV 的轨迹、发射波束和目标速率共同适应移动用户的预测分布。

## 图1系统框架草案
- 空间层：LEO 卫星向 UAV 提供精确位置辅助信息。
- 空中层：多天线 ISAC-UAV 跟踪并服务多个移动用户。
- 感知层：通过 `space-assisted` 或 `ISAC-assisted + EKF` 获取用户位置分布。
- 优化层：基于预测 CSI 分布，联合优化 UAV 轨迹、发射波束和目标速率。
- 目标层：在 outage 约束下最大化系统能效。

## System Model
### 1. SAGIN-ISAC 架构
- UAV 既承担通信节点角色，又承担感知与位置估计角色。
- 卫星与 UAV 之间存在 space-air 传输链路，用于辅助移动用户定位。

### 2. 双位置获取机制
- `space-assisted`：持续从卫星获取较精确的位置数据。
- `ISAC-assisted`：在起始时隙借助空间层校准，后续时隙由 UAV 本地观测并通过 `EKF` 递推估计。

### 3. 鲁棒优化目标
- 通过预测用户位置分布得到 CSI 分布。
- 在信息率 outage 约束、功率约束和轨迹因果约束下最大化能效。

## Algorithm Design 详解
### 1. 位置与信道分布预测
- 用 `EKF` 递推移动用户状态向量和协方差矩阵。
- 将位置分布映射为后续时隙的信道分布不确定性。

### 2. 约束可处理化
- 用 `Bernstein-type inequality` 把 outage 概率约束改写为可计算形式。
- 再用 `SDR + 一阶近似 + SCA` 得到逐步可解的凸近似问题。

### 3. 研究意义
- 论文把“位置信息如何获得”直接写进通信优化主问题，而不是把感知视为外部先验。
- 这很适合支撑 `SAGIN + ISAC` 不只是叠加，而是相互减轻信息获取成本的写作论点。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成移动用户轨迹与信道场景
- 平台与软件：未明确说明
- 方法组件：`EKF`、`Bernstein-type inequality`、`SDR`、`SCA`
- 评测指标：能效、轨迹、UAV-MU 距离、space-air 周期对性能的影响
- 对比对象：`space-assisted` 与 `ISAC-assisted` 两套用户跟踪机制
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露统一代码、训练脚本与硬件环境

## Introduction 写作素材
- `SAGIN` 解决覆盖问题，但其异构资源协调和用户位置信息获取成本都很高。
- `ISAC` 能在本地感知用户位置，但精度受限于平台资源。
- 这篇论文很适合支持“空间辅助与本地感知之间存在开销-精度权衡”的引言句子。

## Related Work 写作素材
- 既有 `SAGIN` 工作往往把通信和定位分开研究。
- 既有 `ISAC` 工作多聚焦单系统感知增强通信，而较少纳入空间层辅助。
- 本文的特色在于：先建双感知路径，再用鲁棒波束赋形把两条路径拉到同一能效框架里。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[空天地一体网络（SAGIN）]]
- [[一体化感知与通信（ISAC）]]
- [[移动用户跟踪]]
- [[空中通信与协同传输]]
- [[信道与通信速率模型]]

## 来源
- [原文](../raw/markdown/mao2025UAVassistedCommunicationsSAGINISAC.md)
