---
tags: [对比, DaaS, 空中计算]
created: 2026-04-07
updated: 2026-04-07
sources:
  - ../raw/markdown/hamdi2025DroneasaserviceResearchChallenges.md
  - ../raw/markdown/zhang2023JointTaskScheduling.md
  - ../raw/markdown/zhang2025LargeModelsAerial.md
---

# 无人机即服务（DaaS）与空中计算的关系

| 维度 | [[无人机即服务（DaaS）]] | [[空中计算]] |
|------|---|---|
| 研究出发点 | 将无人机能力抽象成可发现、可组合、可交付的服务 | 将空中节点作为主要计算/通信/服务执行体 |
| 核心实体 | 服务消费者、服务提供者、无人机所有者、注册中心、边缘/云 | UAV、任务、用户、空地网络、计算与通信资源 |
| 功能范围 | 感知、巡检、配送、影像、娱乐、通信等广义服务 | 更偏计算、通信、网络重构与任务执行 |
| 关键问题 | 服务选择与组合、QoS、用户控制、成本、可部署性 | 调度、部署、轨迹、资源分配、生存时间与协同 |
| 基础设施假设 | 可本地也可云边协同，强调服务治理与平台化 | 常见于地面设施受限、失效或需要空中主导服务的系统 |
| 当前 wiki 中的代表页面 | [[Hamdi2025_Drone-as-a-Service研究挑战与方向综述]] | [[Zhang2023_应急通信空中计算联合调度与多UAV部署]], [[Zhang2025_空中边缘大模型的边云协同演化]] |

## 判断
两者不是替代关系，而是部分相交的两个视角。[[空中计算]]更像“系统范式”，强调空中节点主导计算与服务；[[无人机即服务（DaaS）]]更像“服务计算与部署范式”，强调无人机能力如何被包装、发现、选择和交付。

## 对当前知识库的意义
- DaaS 可以把空中计算视为一种可交付能力，例如空中通信、边缘推理或群体巡检服务。
- 空中计算研究则可以从 DaaS 借用服务注册、QoS 建模、服务组合和用户控制等更上层的系统设计语言。
- 对你后续写作而言，这个区分有助于判断一篇文章是在做“空中节点能力优化”，还是在做“服务化无人机系统组织”。

## 相关页面
- [[无人机即服务（DaaS）]]
- [[空中计算]]
- [[DaaS研究挑战与应用版图]]
- [[UAC研究路线图]]

## 来源
- [Hamdi2025 原文](../raw/markdown/hamdi2025DroneasaserviceResearchChallenges.md)
- [Zhang2023 原文](../raw/markdown/zhang2023JointTaskScheduling.md)
- [Zhang2025 原文](../raw/markdown/zhang2025LargeModelsAerial.md)
