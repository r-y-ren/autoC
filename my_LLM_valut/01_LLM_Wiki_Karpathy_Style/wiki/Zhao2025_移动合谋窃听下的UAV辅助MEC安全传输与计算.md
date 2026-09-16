---
tags: [论文, 合谋窃听, 安全卸载, 计算调度, UAV辅助MEC]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/zhao2025MobileCollusiveEavesdroppers.md
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
  - BCD
  - SDR
  - randomization
  - CVX
  - UDoU
hardware_stack: []
datasets: []
artifact_availability: partial
reproducibility_level: medium
---

# Zhao2025_移动合谋窃听下的UAV辅助MEC安全传输与计算

## 单行摘要
论文面向移动合谋窃听者威胁下的 UAV-assisted MEC 网络，提出 `CSTC` 策略，联合优化 UAV 轨迹、干扰波束、发射功率、卸载决策与基于 `UDoU` 的实时计算调度，以同时满足保密传输和时延约束。

## 题目驱动研究框架
- 研究场景：时隙化 UAV-assisted MEC 网络。
- 研究对象：移动用户、UAV、远程设备 RDs、BS 与移动合谋窃听者。
- 核心问题：窃听者可协同机动并优化截获路径，导致两跳卸载链路保密性急剧下降。
- 标题承诺的方法：cooperative secure transmission and computation。
- 期望效果：在任务时延约束下最大化 sum secrecy transmission rate。

## Algorithm Design 快照
这篇论文不把安全与计算调度分开做，而是把“安全传输”和“实时计算”捆成同一个系统问题。作者让 UAV 与 RDs 同时扮演中继和干扰器，前者在传输侧联合调轨迹、波束、功率和卸载量，后者在计算侧用 `UDoU` 优先级指标做实时调度，从而把保密链路和时限任务真正联通起来。

## 图1系统框架草案
- 接入层：多个用户向 UAV/RDs 卸载任务。
- 威胁层：多个 eavesdroppers 协同移动并动态跟踪用户。
- 传输层：UAV 与 RDs 兼任数据中继和干扰节点。
- 计算层：BS 按 `UDoU` 对任务做实时调度。
- 目标层：在满足时延约束下提升 sum STR。

## System Model
### 1. 时隙化 MEC 拓扑
- 用户向 UAV 或静态 RDs 卸载任务，再由其转发至 BS。
- UAV 是一种特殊 RD，同时具备机动性和干扰能力。

### 2. 合谋窃听威胁
- 窃听者可在时隙间调整轨迹，提高截获增益。
- 多个窃听者之间可协同分工和共享截获收益。

### 3. 联合目标
- 优化保密传输速率。
- 满足任务延迟约束。
- 协调传输与计算资源。

## Algorithm Design 详解
### 1. 安全传输优化
- 联合优化 UAV 轨迹、干扰波束、发射功率和卸载决策。
- 通过 `BCD` 将原问题分解为多个子问题。

### 2. 波束与轨迹求解
- 对含秩约束的子问题使用 `SDR` 与随机化恢复解。
- 相关凸子问题可借助 `CVX` 求解。

### 3. 实时计算调度
- 定义 `UDoU` 度量用户剩余计算负载与剩余可用时间。
- 用该指标驱动任务抢占与优先计算。

## 实验证据卡片
- 验证类型：`simulation`
- 数据来源：合成时隙化 MEC 与窃听场景
- 平台与软件：`CVX` 用于部分子问题求解
- 方法组件：`BCD`、`SDR`、`randomization`、`UDoU`
- 评测指标：sum STR、时延满足情况、运行时间
- 对比对象：`CSTC-UO`、`CSTC-RO`、`CSTC-UJ`、`CSTC-RJ`、`CSTC-WBF`
- 开源情况：补充材料已提供，但代码未明确公开
- 复现判断：`medium`
- 缺失信息：缺少统一实现代码与补充材料中的关键脚本索引

## Introduction 写作素材
- 在 UAV-assisted MEC 中，安全传输和计算调度实际上共享同一组时隙、能量与中继资源。
- 如果只优化保密速率而不考虑任务时限，很多安全方案并不能落到真实 MEC 服务场景里。
- 这篇论文适合支撑“安全 MEC 需要 transmission-computation co-design”的论点。

## Related Work 写作素材
- 以往安全卸载工作常只处理窃听链路或只处理计算时延。
- 与静态窃听者模型相比，这篇论文明确引入移动合谋窃听者，更接近高威胁环境。
- 它把物理层安全、卸载控制和实时调度串成一个完整系统，非常适合做 related work 中的桥梁论文。

## 相关系统建模页
- [[计算卸载模型]]
- [[信道与通信速率模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[合谋窃听]]
- [[任务卸载]]
- [[物理层安全]]
- [[任务队列与时延保障模型]]
- [[安全与服务保障]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [原文](../raw/markdown/zhao2025MobileCollusiveEavesdroppers.md)
