---
tags: [论文, 协同卸载, CoMP, 随机几何, UAV辅助MEC]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/li2025AnchorNovelModeling.md
venue_tier: Unknown
literature_type: theory
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - system_model
  - taxonomy
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
reproducibility_level: low
---

# Li2025_Anchor协同UAV-MEC的动态CoMP卸载建模

## 单行摘要
论文提出基于 Delaunay 三角剖分的协同 UAV-MEC 动态卸载模型，让每个 UE 向三 UAV 构成的 CoMP 集联合卸载，并用随机几何分析 `handoff + uplink + computing` 共同决定的 SECP。

## 题目驱动研究框架
- 研究场景：空地一体的 UAV-MEC 网络，节点持续移动、链路不稳定、业务需要可靠低时延。
- 研究对象：UAV 群、地面 UE、CoMP 卸载集合、MEC 服务器与中央服务器。
- 核心问题：单 UAV 或固定协作模型无法刻画动态场景下的协同切换行为，也难以同时评价通信成功和计算成功。
- 具体方法：基于 Poisson-Delaunay 三角剖分构造三 UAV CoMP 卸载模型，并用随机几何推导 handoff 概率、SUCP、SCP 与 SECP。
- 期望效果：给协同 UAV-MEC 提供可分析、可比较、可用于后续优化设计的统一建模方法。

## Algorithm Design 快照
这篇论文的重点不在“提出一个求解器”，而在“提出一个新的系统建模与性能评估方法”。核心思想是把每个 UE 的卸载目标从单个 UAV 扩展为由三个 UAV 构成的三角形 CoMP 集，并通过 Delaunay 三角剖分动态决定服务单元。这样既能利用协同传输提升可靠性，也引入了新的 cooperative handoff 问题。为此，论文进一步定义 `SUPH`、`SCP` 和 `SECP` 三层指标，并用随机几何把 UAV 空间分布、速度分布、CoMP 切换、上行通信成功率和计算成功率统一到同一分析框架中。

## 图1系统框架草案
- 系统实体：服从 PPP 分布的 UAV 群、地面 UE、MEC 服务器、中央服务器、动态 CoMP 集。
- 任务/数据流：UE 把任务同时卸载到三 UAV 构成的 CoMP 集；任务可在 CoMP 集内 MEC 节点执行，也可转发到中央服务器；服务单元因 UAV 运动而切换。
- 控制/优化变量：CoMP 集选择、handoff 事件、任务送往 MEC/CS 的概率 `p`、SIR 阈值和计算时延阈值。
- 约束来源：UAV 速度、UAV/UE 空间密度、切换失败概率、队列负载、计算时延阈值。
- 画图提醒：图里要把“三角 CoMP 单元”和“切换后新三角单元”都画出来，否则看不出这篇论文真正研究的是动态协同卸载。

## System Model
### A. CoMP 协同卸载单元
- UAV 在给定高度上服从 PPP 分布，UE 也服从 PPP 分布。
- 每个典型 UE 不是只关联最近一个 UAV，而是关联由三个 UAV 组成的 Delaunay 三角单元，形成卸载 CoMP 集。

### B. 通信模型与 SUPH
- 系统在 TDD 模式下工作，信道服从 Rayleigh 衰落。
- 论文定义成功上行通信概率 `SUCP`，并进一步把 handoff 失败影响纳入，得到 `SUPH`。

### C. 计算模型与 SCP
- UE 卸载后的任务可按概率 `p` 送往中央服务器，或以 `1-p` 在 CoMP 集内 MEC 节点执行。
- MEC 执行侧采用“从三台 MEC 中选择瞬时队列负载最小者”的规则。
- 由此定义成功计算概率 `SCP`。

### D. 综合指标 SECP
- 最终用 `SECP = SUPH × SCP` 把通信成功与计算成功整合成统一指标。
- 这使该模型不只是“链路可靠性模型”，而是“通信-计算协同可靠性模型”。

## Algorithm Design 详解
- 第一步是网络建模：利用 Poisson-Delaunay 三角剖分确定三 UAV CoMP 服务单元。
- 第二步是 handoff 建模：随着 UAV 独立移动，CoMP 集会变化，论文定义协同 handoff 事件并给出等效 UAV 分析方法。
- 第三步是通信分析：在考虑 handoff 的前提下推导 SUCP/SUPH。
- 第四步是计算分析：结合 MEC/中央服务器分流概率 `p` 与队列模型推导 SCP。
- 第五步是综合评估：把 `SUPH` 与 `SCP` 合并为 `SECP`，形成可直接比较不同协同卸载机制的评价框架。

## 实验证据卡片
- 验证类型：理论分析 + 数值仿真
- 数据来源：合成场景
- 平台与软件：未说明，正文明确使用 `Monte Carlo` 验证理论表达式
- 硬件与算力：未说明
- 评测指标：CoMP handoff 概率、`SUCP`、`SUPH`、`SCP`、`SECP`
- 对比基线：传统单 BS 关联模型、规则六边形三 UAV 协作模型、传统 cooperative / non-cooperative offloading
- 开源情况：未说明
- 复现判断：`low`
- 证据备注：公式和指标定义很完整，但缺少实现平台与代码资产，更适合做建模参考而非直接工程复现。

## Introduction 写作素材
- 许多 UAV-MEC 论文默认“选一个 UAV 卸载”，但这并不能反映协同网络下的可靠传输与切换行为。
- 当 UAV 群规模增大且节点持续移动时，真正决定服务质量的已不是单链路，而是动态 CoMP 集。
- 这篇论文适合支撑“UAV-MEC 需要新的建模层，而不仅是新的优化器”的论证。

## Related Work 写作素材
- 与单 UAV / 单 BS 卸载模型相比，本文从单点关联转向三 UAV 协同卸载。
- 与只研究 handoff 或只研究 MEC 卸载的工作相比，本文把 handoff 机制、通信成功和计算成功统一起来。
- 与直接给出启发式求解器的论文相比，本文更像一篇“理论建模框架论文”，适合做系统模型层面的引用。

## 相关系统建模页
- [[协同多点（CoMP）卸载模型]]
- [[计算卸载模型]]
- [[信道与通信速率模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[UAV辅助MEC]]
- [[任务卸载]]
- [[任务卸载与资源分配研究主线]]
- [[安全与服务保障]]

## 来源
- [原文](../raw/markdown/li2025AnchorNovelModeling.md)
