---
tags: [论文, 有限块长通信, NOMA, AoI, URLLC]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/hoang2024FiniteBlockLength.md
venue_tier: CCF-A
literature_type: theory
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - system_model
validation_type:
  - theory
  - simulation
data_origin:
  - synthetic
platforms: []
frameworks: []
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Hoang2024 有限块长 NOMA 多用户配对 UAV 系统性能分析与优化

## 单行摘要
论文在 UAV 辅助 NOMA 多用户配对系统中分析有限块长条件下的 BLER、吞吐、goodput、时延与 AoI，并进一步优化高度、块长和发射功率。

## 题目驱动研究框架
- 研究场景：多天线 UAV 辅助的 NOMA 多用户配对系统。
- 研究对象：UAV、成对用户、有限块长传输、NOMA 调度与功率控制。
- 核心问题：在 URLLC 约束下，如何同时兼顾 BLER、吞吐、时延、AoI 与能效。
- 标题承诺的方法：finite block length performance analysis and optimization。
- 期望效果：得到可解释的闭式性能表达式，并据此优化关键通信参数。
- 标题与正文的偏差：正文不仅是性能分析，还把高度、块长、发射比特数与功率优化一起纳入。

## Algorithm Design 快照
论文以有限块长 NOMA-UAV 系统为对象，先基于高斯-切比雪夫求积和不完全 Gamma 函数推导 BLER、吞吐、goodput、时延、可靠性与 AoI 的闭式表达式，再用一维搜索、迭代算法和贪心用户配对优化高度、块长、传输比特数和功率配置。与无限块长近似不同，论文强调短包传输场景下 BLER 与时延之间的真实折中。

## 图1系统框架草案
- 系统实体：多天线 UAV、NOMA 用户对、有限块长编码与反馈机制。
- 任务/数据流：UAV 下发短包数据，用户在有限块长条件下进行 SIC 解码与 ACK 反馈。
- 控制/优化变量：用户配对、发射功率、UAV 高度、块长、传输比特数。
- 约束来源：BLER 阈值、URLLC 时延要求、有限块长误差和 LoS/NLoS 条件。
- 画图提醒：图里应突出“有限块长 -> BLER/latency/AoI -> 参数搜索优化”的分析链条。

## System Model
- 论文将 UAV 视作多天线发射端，采用 NOMA 用户配对和有限块长编码。
- 性能指标从传统吞吐扩展到 BLER、goodput、可靠性和 AoI。
- 有限块长假设使得 Shannon 极限不再足够，误码与时延之间形成显式折中。
- UAV 高度不仅影响覆盖，也直接影响 BLER 与 AoI 最优值。

## Algorithm Design 详解
- 第一步推导有限块长 NOMA-UAV 系统的 BLER 与相关性能指标闭式表达式。
- 第二步分析 AoI、时延和 goodput 与块长/比特数的关系。
- 第三步利用一维搜索和迭代算法优化高度、块长和功率。
- 第四步用贪心配对优于随机调度，验证用户调度策略的重要性。

## 实验证据卡片
- 验证类型：理论分析；数值仿真
- 数据来源：合成场景或 Monte-Carlo 仿真
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文的强项是可解释通信分析，对 UAC 中“可靠性-时延-AoI”建模很有价值。

## Introduction 写作素材
- 当任务进入 URLLC 或短包传输场景时，经典无限块长近似会系统性高估链路性能。
- 有限块长条件让 BLER、goodput 和 AoI 成为必须同时考量的指标。
- 这篇论文适合支撑“空中通信系统已从平均速率优化走向时效与可靠性联合建模”的论点。

## Related Work 写作素材
- 与无限块长的 UAV 通信建模不同，本文显式处理有限块长误差。
- 与只看吞吐或 BLER 的通信论文不同，本文同时引入 AoI、goodput 与时延。
- 与随机用户调度不同，本文采用贪心配对获得更优表现。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[有限块长通信]]
- [[信息年龄（AoI）]]
- [[空中通信与协同传输]]
- [[安全与服务保障]]

## 来源
- [原文](../raw/markdown/hoang2024FiniteBlockLength.md)
