---
tags: [概念, DaaS, 服务计算, 系统范式]
created: 2026-04-07
updated: 2026-04-09
sources:
  - ../raw/markdown/hamdi2025DroneasaserviceResearchChallenges.md
  - ../raw/markdown/li2025UAVassistedMicroserviceMobile.md
  - ../raw/markdown/rizvi2025MonitoringInterdroneService.md
  - ../raw/markdown/roy2025ServHUServiceHandoff.md
  - ../raw/markdown/xu2024HolisticHybridService.md
  - ../raw/markdown/xu2025WindawareServiceProvisioning.md
  - ../raw/markdown/liu2025DelaysensitiveGoodsDelivery.md
---

# 无人机即服务（DaaS）

## 定义
[[无人机即服务（DaaS）]]指把无人机的感知、配送、巡检、通信、媒体采集等能力抽象为按需调用的服务，而不是把无人机仅视为设备本体。它强调服务消费者、服务提供者和无人机能力拥有者之间的解耦，并通过平台化方式实现可发现、可选择、可组合和可计价的无人机能力供给。

## 核心特征
- 无人机能力以服务形式被调用，而不是由每个应用方自建完整机队。
- 服务能力既包括功能属性，也包括载重、速度、续航、可用性、天气敏感性等非功能属性。
- 运营重点从“买一架无人机”转向“如何发现、编排和保障一项无人机服务”。
- 服务层通常引入提供者、消费者和注册机制，因此天然关心 QoS、SLA、选择与组合问题。

## 与传统无人机部署的区别
- 传统模式强调自有硬件、自有维护和自有系统开发；DaaS 更强调外包、共享和按需租用。
- 传统模式主要优化单任务执行；DaaS 进一步讨论服务发现、服务组合、计费和跨主体协作。
- 传统模式更接近设备部署问题；DaaS 更接近服务计算和平台运营问题。

## 对当前知识库的意义
- 它给现有以 [[空中计算]] 和 [[UAV辅助MEC]] 为主的研究库补上了“服务化系统范式”这一层。
- 它把研究焦点从任务卸载、轨迹优化和资源分配，扩展到服务生命周期、用户控制、服务注册、服务组合和可部署性。
- 它特别适合作为综述页和选题页的桥梁概念，帮助你判断一篇工作是在做“设备优化”，还是在做“服务系统”。

## 在当前 wiki 中的代表页面
- [[Hamdi2025_Drone-as-a-Service研究挑战与方向综述]]：对 DaaS 的 taxonomy、架构和挑战进行系统综述。
- [[DaaS研究挑战与应用版图]]：把这条分支拆成可复用的主题结构。
- [[Li2025_灾后医疗救援的UAV辅助微服务MEC架构]]：把 UAV 服务能力组织成可编排的微服务 MEC 架构。
- [[Rizvi2025_面向韧性运行的无人机间服务干扰监测]]：把“服务是否被干扰和破坏”写成可监测的韧性问题。
- [[Roy2025_Serv-HU面向UaaS的服务接力机制]]：把服务连续性交给平台侧的接力与定价机制来保障。
- [[Xu2024_MEC无人机末端配送的整体混合服务选择]]：把末端配送中的静态选择与动态重选统一到服务选择问题。
- [[Xu2025_多包裹无人机配送的风感知服务供给策略]]：把风场、共享、组合和供给策略纳入 DaaS 服务交付逻辑。
- [[Liu2025_多任务无人机的时敏配送与在途感知]]：把低空配送与沿途感知写成同一无人机可连续提供的复合服务。

## 研究判断
DaaS 不是 [[空中计算]] 的同义词，也不是 [[UAV辅助MEC]] 的简单改名。它更像一个更上层的服务计算与部署视角，关心能力如何被包装、发现、组合、接力和持续交付。Batch_09 很重要的一点在于，它让 DaaS 不再只停留在综述层：微服务架构、服务干扰监测、服务接力和风感知供给都已经开始出现可执行的系统设计实例。

## 相关页面
- [[服务化无人机三层架构模型]]
- [[DaaS研究挑战与应用版图]]
- [[无人机即服务（DaaS）与空中计算的关系]]
- [[微服务MEC架构]]
- [[服务干扰监测]]
- [[服务接力（Service Hand-off）]]
- [[风感知服务供给]]
- [[空中计算]]
- [[UAV辅助MEC]]

## 来源
- [Hamdi2025 原文](../raw/markdown/hamdi2025DroneasaserviceResearchChallenges.md)
- [Li2025 Microservice MEC 原文](../raw/markdown/li2025UAVassistedMicroserviceMobile.md)
- [Rizvi2025 原文](../raw/markdown/rizvi2025MonitoringInterdroneService.md)
- [Roy2025 原文](../raw/markdown/roy2025ServHUServiceHandoff.md)
- [Xu2024 H2S2 原文](../raw/markdown/xu2024HolisticHybridService.md)
- [Xu2025 原文](../raw/markdown/xu2025WindawareServiceProvisioning.md)
- [Liu2025 原文](../raw/markdown/liu2025DelaysensitiveGoodsDelivery.md)
