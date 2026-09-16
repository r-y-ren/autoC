---
tags: [论文, 综述, DaaS, 服务计算]
created: 2026-04-07
updated: 2026-04-08
sources:
  - ../raw/markdown/hamdi2025DroneasaserviceResearchChallenges.md
venue_tier: Survey
literature_type: survey
evidence_tier: supporting
paper_role: survey
use_for:
  - taxonomy
  - introduction
  - related_work
validation_type:
  - literature_review
data_origin:
  - literature_corpus
platforms: []
frameworks: []
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Hamdi2025 Drone-as-a-Service 研究挑战与方向综述

## 单行摘要
这篇综述把 Drone-as-a-Service（DaaS）正式定义为服务计算范式下的无人机系统，提出功能-研究任务-应用域三维 taxonomy、三层系统架构和不确定性感知交付模型，并系统梳理开放挑战。

## 题目驱动研究框架
- 研究场景：面向智慧城市、应急、物流、农业、媒体等场景的服务化无人机系统。
- 研究对象：由无人机所有者、服务提供者、服务消费者、无人机平台、边缘/云和服务注册机制构成的 DaaS 生态。
- 核心问题：如何把分散的无人机能力抽象成可发现、可选择、可组合、可计价的服务，并建立统一的架构、分类和挑战框架。
- 标题承诺的方法：以“research challenges and directions”为主轴，对 DaaS 进行体系化综述与未来方向梳理。
- 期望效果：为后续 DaaS 系统设计、服务选择与组合、QoS 建模和选题设计提供可复用总图。
- 标题与正文的偏差：标题强调挑战与方向，但正文的真正贡献还包括完整 taxonomy、三层架构、系统化检索方法和一个用于说明服务组合问题的 delivery QoS 模型。

## Algorithm Design 快照
本文面向以无人机交付感知、配送、通信和媒体等服务的 DaaS 场景，研究对象不再是单个 UAV 的轨迹或卸载优化器，而是由服务消费者、服务提供者、无人机、边缘/云和服务注册组成的服务生态。核心问题是如何把无人机能力抽象成可发现、可选择、可组合的服务，并系统梳理其应用、QoS 和开放挑战。论文通过 taxonomy、三层架构、系统检索方法和不确定性感知交付模型建立统一分析框架，期望为后续系统建模、服务组合和研究选题提供基础总图。

## 图1系统框架草案
- 系统实体：服务消费者、服务提供者、无人机所有者、服务注册中心、无人机集群、边缘节点、云平台。
- 任务/数据流：用户提交服务请求后，经服务注册或平台发现候选 DaaS；平台结合 QoS、天气、负载和位置状态完成服务选择与组合；边缘/云负责规划与推理；无人机执行任务并回传遥测与服务状态。
- 控制/编排变量：服务功能集合、QoS 属性、提供者选择、组合路径、用户控制权限、编队协同方式。
- 约束来源：天气不确定性、载重与续航、隐私与监管、空域限制、网络时延与可用性。
- 画图提醒：如果后续要画综述第一张图，最适合把 Fig. 2 的 taxonomy 和 Fig. 5 的三层架构合并成“上层应用/中层服务编排/下层无人机执行”的总图，而不是只画单一通信链路。

## System Model
- DaaS 的基本参与方包括无人机所有者、服务提供者与服务消费者，强调“能力拥有者”和“服务运营者”可以分离。
- 架构上采用三层模型：用户层负责请求、监控和交互，计算层负责存储、处理、边缘/云协同和接口服务，无人机层负责感知、执行、通信和群体协作。
- 服务组织方式继承 SOA 思路，由服务提供者、服务消费者和服务注册表构成松耦合关系；在群体场景下又引入 orchestration 与 choreography 两类协作机制。
- 论文给出不确定性感知的 delivery DaaS 模型：DaaS 可表示为服务标识、功能集、QoS、取货/送达时间与位置的组合；QoS 进一步包含飞行时长、载重、速度和环境条件；PDR 则刻画面向包裹交付的服务请求。
- 与现有 UAC/UAV-MEC 论文不同，这里的系统建模重点不只是算力、链路和轨迹，而是服务能力抽象、服务发现、组合与跨层运维。

## Algorithm Design 详解
- 这篇论文本质上不是求解型算法论文，而是“研究框架设计”型综述。它先定义研究问题，再用 taxonomy、架构和挑战清单组织现有工作。
- 在方法学层面，作者围绕研究问题、检索关键词、数据库来源、纳入排除标准和定量统计建立了一套可复核的综述流程，覆盖 2010-2025 年 214 篇相关研究。
- 在知识组织层面，论文把 DaaS 拆成三组维度：功能维度包括 sensing、inspection、delivery、entertainment、videography、communication；研究任务维度包括 communication/data management、uncertainty、cost、user control、scheduling、energy、selection/composition、cybersecurity、swarm、HDI 等；应用域维度则划分为 commercial 与 noncommercial。
- 在系统建模层面，论文提出一个三层 DaaS 架构，并明确指出 edge/cloud 与 swarm coordination 在服务化无人机系统中的作用，这一点对后续画系统框图特别有帮助。
- 在问题抽象层面，论文通过 uncertainty-aware delivery model 说明：DaaS 研究不能只停留在“某架无人机能不能飞”，而要处理服务请求、QoS、环境动态、组合路径和用户约束的联合建模。
- 在研究方向层面，最重要的输出不是某个最优算法，而是一张 challenge map：通信与数据管理、天气不确定性、成本估计、用户控制、隐私监管、安全保障、调度、能耗、服务组合、群智感知、网络安全、无人机群服务和 HDI。

## 实验证据卡片
- 验证类型：文献综述
- 数据来源：文献语料
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：该文的证据主体是系统性文献检索与结构化归纳，不是原型实验。

## Introduction 写作素材
- 传统无人机系统往往伴随高基础设施、维护、软件开发、存储和网络运维成本，而 DaaS 希望把这些成本外包到服务层。
- 仅从“无人机能做什么”切入已经不够，真正值得研究的是“无人机能力如何被组织成可交付、可组合、可扩展的服务”。
- DaaS 的研究价值在于把功能属性和非功能属性同时显式化，例如载重、速度、续航、天气敏感性与服务可得性。
- 对引言写作而言，这篇综述特别适合用来支撑“从设备视角转向服务视角”的问题提出。
- 如果你的论文要强调系统可部署性、服务编排、用户控制或 QoS/SLA，这篇综述可以作为总入口文献。

## Related Work 写作素材
- 现有大量综述集中于单一方向，如无人机通信、隐私安全、视觉导航、城市应用或 HDI，但较少把无人机明确放进成熟的 as-a-service 语义下。
- 论文明确区分自己与 earlier drone-service surveys 的差别：不是停留在概念性愿景，而是给出 taxonomy、三层架构和挑战清单。
- 对相关工作写作很有用的一点是：作者把“功能分类”“研究任务分类”和“应用领域分类”拆开，这比单纯按应用场景列文献更容易形成结构化综述。
- 如果后续要写“服务选择与组合”“不确定性 QoS”或“用户控制/隐私”方向的 related work，这篇综述可以充当总纲，再向下挂具体方法论文。

## 相关系统建模页
- [[服务化无人机三层架构模型]]

## 相关概念与主题页
- [[无人机即服务（DaaS）]]
- [[DaaS研究挑战与应用版图]]
- [[无人机即服务（DaaS）与空中计算的关系]]
- [[空中计算]]

## 来源
- [原文](../raw/markdown/hamdi2025DroneasaserviceResearchChallenges.md)
