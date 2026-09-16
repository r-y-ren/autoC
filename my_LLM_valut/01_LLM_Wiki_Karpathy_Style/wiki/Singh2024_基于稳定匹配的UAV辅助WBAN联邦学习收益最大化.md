---
tags: [论文, 联邦学习, WBAN, 稳定匹配, 资源分配, DaaS]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/singh2024StableMatchingBased.md
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
  - prototype
  - trace_driven
data_origin:
  - mixed
platforms:
  - Python 3.9
  - Gurobi
frameworks:
  - stable matching
  - graph coloring
  - federated learning
datasets:
  - Shanghai Telecom dataset
hardware_stack:
  - Intel Core i7-10750H processor
  - Raspberry Pi 4 Model B
  - Dell Precision 3640 Workstation
  - Phantom 4 Pro V2.0
  - Samsung Galaxy A22 5G
  - OnePlus Nord CE 5G
artifact_availability: unknown
reproducibility_level: medium
---

# Singh2024 基于稳定匹配的UAV辅助WBAN联邦学习收益最大化

## 单行摘要
论文在 5G 支撑的 UAV-assisted [[身体域网（WBAN）]] 场景中，把联邦学习数据收集、PRB 分配与收益分成统一成一个资源分配问题，并用 [[稳定匹配]] 与图着色启发式联合最大化 UAV 与 WBAN 双方收益。

## 题目驱动研究框架
- 研究场景：医疗/生理监测场景中，多个 WBAN 通过 UAV 上传生理数据并参与联邦学习。
- 研究对象：WBAN 用户、UAV 服务提供者、MBS、PRB 资源与 FL 训练过程。
- 核心问题：WBAN 的最小/最大 PRB 需求不同，上传又会互相干扰，若资源分配不合理，数据共享与联邦学习收益都会下降。
- 标题承诺的方法：stable matching based revenue maximization。
- 期望效果：在不泄露原始数据的前提下，让 UAV 与 WBAN 双方在可接受干扰下获得更高收益。
- 标题与正文的偏差：正文实际上不只是在做匹配，而是把图着色复用、最小/最大资源需求和 FL 收益建模结合到一个近似最优的资源复用框架中。

## Algorithm Design 快照
论文研究 UAV-assisted WBAN 联邦学习中的资源复用与收益分配问题。WBAN 需要把生理数据传给 UAV 参与 FL 训练，但不同用户对 PRB 的最小/最大需求不同，且同频复用会引入干扰。难点在于系统既要保证隐私友好的 FL 数据上传，又要让 UAV 提供算力和服务仍然“值得做”。为此，作者建立总体收益最大化模型，同时考虑 WBAN 提供数据的价值、UAV 提供训练与通信资源的收益，以及 PRB 干扰关系。算法上先构造稳定匹配框架确定 UAV-PRB-WBAN 候选配对，再用图着色/独立集思想处理干扰复用，最终在多方收益和冲突约束之间取得高质量平衡。

## 图1系统框架草案
- 系统实体：WBAN、UAV、MBS、UAV 基地、FL 模型所有者。
- 任务/数据流：WBAN 采集生理数据，经 5G 上传至 UAV；UAV 回基地并在 MBS 协助下参与 FL 训练。
- 控制/优化变量：PRB 分配、UAV-WBAN 关联、最小/最大 PRB 满足量、收益函数。
- 约束来源：干扰图、一跳冲突、PRB 供给、FL 训练精度要求、数据大小与能耗。
- 画图提醒：图里建议明确画出“数据上传”和“回基地训练”两阶段，因为收益模型横跨通信和训练两个环节。

## System Model
- 每个 WBAN 采集生理数据并通过 5G 网络向 UAV 上传，UAV 作为空中采集与训练节点。
- MBS 负责 PRB 管理并辅助 UAV 完成联邦学习训练。
- 收益函数同时考虑 WBAN 贡献数据、UAV 提供训练资源以及上传所需资源成本。
- 干扰关系通过图结构表示，相互冲突的 WBAN 不能复用相同 PRB。

## Algorithm Design 详解
- 首先定义满足最小/最大 PRB 需求的资源分配可行域，并把收益最大化写成 NP-hard 优化问题。
- 随后利用稳定匹配思想为 UAV-PRB-WBAN 三方关系生成偏好与候选集合。
- 对存在干扰冲突的资源对，进一步借助图着色与最大权独立集思路实现安全复用。
- 该文说明在 UAV-assisted FL 中，资源分配不是纯通信问题，而是和数据价值、模型精度和服务收益直接耦合。

## 实验证据卡片
- 验证类型：数值仿真 + 原型验证 + 真实数据驱动
- 数据来源：`Shanghai Telecom dataset`；原型阶段使用真实生理数据采集设备
- 平台与软件：`Python 3.9`、`Gurobi`
- 硬件与算力：`Intel Core i7-10750H`、`Raspberry Pi 4`、`Dell Precision 3640`、`Phantom 4 Pro V2.0`、`Samsung Galaxy A22 5G`、`OnePlus Nord CE 5G`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：该文同时给出公开数据集驱动仿真与小型原型系统，属于这批文献里更接近真实系统的一篇。

## Introduction 写作素材
- UAV-assisted FL 的关键不只是“能不能训”，而是“数据上传与资源复用是否让各参与者都有激励”。
- WBAN 场景强调隐私、时效和有限无线资源，非常适合把收益与资源分配统一考虑。
- DaaS 视角能把 UAV 从纯技术节点重新解释为带定价能力和收益目标的服务提供者。

## Related Work 写作素材
- 传统 UAV-assisted MEC 更关注卸载或能耗，很少把联邦学习和收益分成并入主模型。
- 现有 FL 资源分配通常忽略干扰图结构或 UAV 服务成本。
- 该文把稳定匹配、图着色和原型验证同时放进 UAV-assisted FL 框架中，适合作为“机制设计 + FL + DaaS”交叉方向的代表作。

## 相关系统建模页
- [[信道与通信速率模型]]

## 相关概念与主题页
- [[联邦学习]]
- [[身体域网（WBAN）]]
- [[稳定匹配]]
- [[无人机即服务（DaaS）]]
- [[DaaS研究挑战与应用版图]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/singh2024StableMatchingBased.md)
