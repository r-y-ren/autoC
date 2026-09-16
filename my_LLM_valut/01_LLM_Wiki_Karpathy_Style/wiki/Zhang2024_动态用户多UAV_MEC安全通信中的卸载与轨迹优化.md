---
tags: [论文, 物理层安全, UAV辅助MEC, 任务卸载, 轨迹优化]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/zhang2024TaskOffloadingTrajectory.md
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
platforms: []
frameworks:
  - JDPB
  - BCD
  - SCA
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Zhang2024 动态用户多UAV-MEC安全通信中的卸载与轨迹优化

## 单行摘要
论文在动态用户多 UAV MEC 系统中联合优化卸载决策、资源分配与轨迹规划，通过 BS 干扰压制窃听者并最大化最小安全计算能力。

## 题目驱动研究框架
- 研究场景：存在窃听者和动态用户的多 UAV MEC 系统。
- 研究对象：终端用户 TUs、多架 UAV、窃听者、一个负责干扰的 BS。
- 核心问题：在用户移动和窃听威胁同时存在时，如何联合组织卸载、功率、时分配与 UAV 轨迹。
- 标题承诺的方法：task offloading and trajectory optimization for secure communications。
- 期望效果：提高动态用户场景下的最小安全计算能力，并保持算法鲁棒性。
- 标题与正文的偏差：正文的重点不只是“secure communications”，而是把区域划分、竞价式卸载和资源/轨迹凸优化拼成一个分层求解器。

## Algorithm Design 快照
论文研究动态用户多 UAV MEC 系统中的安全卸载问题，其中终端用户会随机移动，窃听者会监听卸载链路，而地面 BS 通过发射干扰信号压制窃听。难点在于安全通信容量取决于用户移动、UAV 轨迹、时隙分配、发射功率和计算频率等多类变量的耦合。为此，作者提出 JDPB 方法：先把区域划分为多个子区域，通过动态规划与竞价机制分配用户到不同 UAV，再用 SCA 和 BCD 优化资源分配和轨迹。最终目标是最大化所有用户中的最小安全计算能力。

## 图1系统框架草案
- 系统实体：动态用户 TUs、多架固定翼 UAV、多个窃听者、一个干扰 BS。
- 任务/数据流：用户向 UAV 卸载任务；窃听者监听链路；BS 向窃听者方向广播干扰；UAV 对任务进行边缘计算。
- 控制/优化变量：用户到 UAV 的卸载分配、TU 发射功率、时分配因子、UAV CPU 频率、UAV 轨迹。
- 约束来源：用户最小安全计算需求、UAV 能量预算、最小/最大速度、UAV 间安全距离、每架 UAV 的服务用户数。
- 画图提醒：图里最好显式画出“BS 干扰窃听者但 UAV 可预知干扰信号”的安全机制。

## System Model
- 用户位置按 Gauss-Markov 随机模型动态更新，因此卸载和轨迹必须逐时隙适应。
- 多架 UAV 为用户提供边缘服务，窃听者尝试截获卸载数据链路。
- BS 发射干扰信号以削弱窃听能力，而 UAV 因预知干扰信号可在接收端分离，形成友好干扰机制。
- 系统目标不是简单吞吐量最大化，而是 max-min secure calculation capacity，这使其天然偏向公平安全保障。

## Algorithm Design 详解
- 先将原区域划为子区域，并通过竞价方式决定各 UAV 服务哪些区域和用户。
- 对连续变量部分，使用 SCA 与 BCD 交替优化时分配、功率、计算频率和轨迹。
- 对离散卸载决策部分，使用 bidding 机制处理用户到 UAV 的分配问题。
- 相比[[Li2024_智能窃听对抗下的UAV辅助MEC安全卸载与资源分配]]中的学习型对抗者框架，这篇论文更偏解析优化和物理层安全建模。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成动态用户与窃听者场景
- 平台与软件：文中提到使用 `CVX` 处理凸子问题
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文参数表与场景设置较完整，但没有给出实现代码和运行平台细节。

## Introduction 写作素材
- 动态用户场景下的安全卸载问题不能只依赖静态关联，因为用户移动会改变安全链路质量。
- 友好干扰 BS 的引入说明物理层安全机制可以直接嵌入 MEC 卸载系统，而不是外层补丁。
- 这篇论文可作为“安全保障正在从链路保密扩展到安全计算能力公平保障”的例子。

## Related Work 写作素材
- 与普通轨迹-卸载联合优化相比，本文把窃听者和友好干扰显式加入模型。
- 与纯学习方法相比，本文采用动态规划、竞价、SCA 和 BCD 的分层求解结构。
- 与静态用户安全卸载工作相比，本文引入 Gauss-Markov 动态用户模型。

## 相关系统建模页
- [[计算卸载模型]]
- [[信道与通信速率模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[物理层安全]]
- [[安全与服务保障]]
- [[任务卸载与资源分配研究主线]]
- [[轨迹优化与协同控制]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/zhang2024TaskOffloadingTrajectory.md)
