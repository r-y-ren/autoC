---
tags: [论文, 光学RIS, QKD, FSO, HAP, UAV安全通信]
created: 2026-04-09
updated: 2026-04-09
sources:
  - ../raw/markdown/trinh2025OpticalRISsImprove.md
venue_tier: CCF-A
literature_type: theory
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - related_work
validation_type:
  - theory
  - simulation
data_origin:
  - synthetic
platforms:
  - MODTRAN
frameworks:
  - extended Huygens-Fresnel
  - Monte Carlo
  - decoy-state QKD
  - finite-key analysis
hardware_stack: []
datasets: []
artifact_availability: unknown
reproducibility_level: medium
---

# Trinh2025_光学RIS提升HAP-UAV场景FSO量子密钥率

## 单行摘要
论文针对 `HAP-to-UAV` 量子光通信中“终端只能挂载在无人机下方”的实际限制，引入建筑屋顶 `ORIS` 反射链路，并从大气湍流、悬停波动和有限密钥效应出发分析秘密密钥率提升机制。

## 题目驱动研究框架
- 研究场景：`HAP-LAP/UAV` 之间的自由空间量子密钥分发链路。
- 研究对象：高空平台、低空平台、屋顶光学 RIS、量子光束与接收端波动。
- 核心问题：无人机上行直连高空平台受安装结构和姿态波动限制，导致稳定量子链路难以建立。
- 标题承诺的方法：用 `ORIS` 改善 FSO-QKD 的秘密密钥率。
- 期望效果：在 pointing error 和大气湍流存在时仍提升 `SKR` 与安全性能。

## Algorithm Design 快照
这篇论文的重点并不在“做一个新协议”，而是在物理链路层重新设计量子光束传播路径。作者利用 `ORIS` 把来自高空平台的量子光束反射到挂载于无人机下方的接收终端，再把 `PE + turbulence + beam profile` 一起写进解析模型，最终比较线性、二次和聚焦三类相位配置对密钥率的影响。

## 图1系统框架草案
- 高空层：`HAP` 发射量子光束。
- 城市场景层：楼顶 `ORIS` 负责光束重定向与宽度控制。
- 低空层：挂载接收终端的 UAV/LAP 接收量子信号。
- 信道层：大气湍流与无人机悬停波动共同引入几何损耗和 pointing error。
- 安全层：评估 `SKR`、`QBER` 与 finite-key 下的安全性。

## System Model
### 1. HAP-ORIS-LAP 光链路
- 直接上行链路受 UAV 结构限制，不适合把量子终端安装于机体顶部。
- `ORIS` 将高空入射光束反射到无人机下方接收终端。

### 2. 光学传播与误差模型
- 基于 `extended Huygens-Fresnel` 原理刻画光束传播。
- 联合建模大气湍流、几何损耗和无人机悬停带来的 `pointing error`。

### 3. 安全性能目标
- 分析 `PLOB bound`、`QBER`、secret key length 等安全指标。
- 比较不同 `ORIS` 相位配置在不同误差条件下的最优性。

## Algorithm Design 详解
### 1. ORIS 相位控制
- 讨论线性、二次和聚焦三类相位轮廓。
- 本质上是在“收束光束提升接收功率”和“发散光束缓解波动失配”之间找平衡。

### 2. 安全分析框架
- 用 `Monte Carlo` 验证解析表达式。
- 进一步引入 `two-decoy-state DV-QKD` 的有限密钥分析，避免只停留在理想无限长密钥假设。

### 3. 研究意义
- 论文把 `RIS` 从经典无线电传播控制扩展到量子光安全链路，是很有代表性的跨领域空中通信工作。

## 实验证据卡片
- 验证类型：`theory`、`simulation`
- 数据来源：合成大气湍流与悬停波动参数场景
- 平台与软件：`MODTRAN`
- 方法组件：`extended Huygens-Fresnel`、`Monte Carlo`、`decoy-state QKD`、`finite-key analysis`
- 评测指标：`SKR`、`QBER`、secret key length、几何与失配损耗
- 对比对象：不同 `ORIS` 相位轮廓与不同 pointing error 强度
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未披露完整仿真脚本和参数生成代码

## Introduction 写作素材
- 非地面网络不只是传统保密速率问题，还开始吸收量子安全链路设计。
- `RIS` 的作用不再局限于射频传播调控，也可以延展到光学量子链路可达性。
- 这篇论文很适合支撑“空天地安全通信正在从物理层保密扩展到量子安全”的论述。

## Related Work 写作素材
- 既有 QKD 研究多集中于卫星-地面或无人机-地面链路。
- 既有 RIS 研究则大多聚焦射频系统而非光学量子系统。
- 本文将 `ORIS`、`HAP-LAP` 和有限密钥分析统一起来，是很有辨识度的前沿切口。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[光学可重构智能表面（ORIS）]]
- [[量子密钥分发（QKD）]]
- [[自由空间光通信（FSO）]]
- [[安全与服务保障]]
- [[空中通信与协同传输]]

## 来源
- [原文](../raw/markdown/trinh2025OpticalRISsImprove.md)
