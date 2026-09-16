---
tags: [论文, UAV辅助MEC, PPO, 任务卸载, UAV部署]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/wang2025JointPositioningComputation.md
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
platforms:
  - Python 3.9
  - TensorFlow 2.11.0
frameworks:
  - PPO
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Wang2025 PPO驱动的多UAV-MEC联合定位与计算卸载

## 单行摘要
论文用 PPO 联合优化多 UAV MEC 网络中的 UAV 定位与任务卸载，以降低端到端时延并提升系统韧性。

## 题目驱动研究框架
- 研究场景：缺乏蜂窝基础设施的动态多 UAV MEC 网络。
- 研究对象：地面用户簇、三架 UAV、一个蜂窝基站、任务拆分与回传拓扑。
- 核心问题：如何联合决定 UAV 放置位置和任务卸载比例，以降低低时延应用的端到端时延。
- 标题承诺的方法：joint positioning and computation offloading via PPO。
- 期望效果：在动态环境中实现更低时延、更好的负载平衡与更强的故障韧性。
- 标题与正文的偏差：正文不仅做“定位”，还让一部分 UAV 充当接入节点、另一部分承担回传桥接，形成带拓扑结构的联合放置问题。

## Algorithm Design 快照
论文研究多 UAV MEC 系统中 UAV 位置部署与任务卸载的联合优化问题。难点在于地面用户分布存在簇结构，UAV 既要靠近用户以降低接入时延，又要保持与蜂窝基站及其他 UAV 的连通以形成回传网络。为此，作者构建一个双层基线优化框架，并进一步使用 PPO 同时学习 UAV 放置与卸载决策。训练后的策略能根据不同初始位置快速重构网络，在保证连通性的同时降低响应时延，并在随机 UAV 故障下维持较好的恢复能力。

## 图1系统框架草案
- 系统实体：蜂窝基站、多个用户簇、三架或更多 UAV。
- 任务/数据流：用户任务被拆分到附近 UAV 或蜂窝基站处理；部分 UAV 作为接入节点，部分 UAV 负责回传桥接。
- 控制/优化变量：UAV 三维位置、用户任务卸载比例、UAV 之间的连通关系。
- 约束来源：通信半径、固定高度、连通性、计算资源限制、故障场景下的可恢复性。
- 画图提醒：图中应显式区分“服务用户的 UAV”和“提供 backhaul 的 UAV”。

## System Model
- 用户按照二维高斯簇分布，反映灾后或偏远地区的热点业务分布。
- 多架 UAV 在固定高度运行，其中部分直接服务用户，另一部分将接入层与基站连接起来。
- 任务可以在 UAV 与 BS 之间动态分配，因此“位置”和“卸载比例”彼此影响。
- 系统目标以时延为主，同时关注能耗和网络韧性，尤其考虑随机 UAV 故障后的恢复表现。

## Algorithm Design 详解
- 先构建双层优化基线：上层决定 UAV 网络形成与位置，下层决定任务卸载。
- 再使用 PPO 统一学习 UAV 放置与卸载动作，使策略能适应不同初始条件和网络状态。
- 测试阶段展示了任务拆分在 BS 与不同 UAV 之间的快速收敛，说明策略不只是“把 UAV 放到热点上方”，而是在学习拓扑化分工。
- 随机 UAV 故障实验表明，PPO 学到的是可恢复的放置与卸载策略，而不是只对单一静态场景有效的最优解。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成用户簇场景
- 平台与软件：`Python 3.9`、`TensorFlow 2.11.0`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文明确给出了软件环境、训练参数和用户分布设置，但没有公开代码与完整硬件配置。

## Introduction 写作素材
- 在基础设施稀缺场景里，UAV 不只是“多一个边缘节点”，更是临时网络拓扑的构成单元。
- 位置部署与任务卸载必须联合考虑，否则仅优化其中一方会造成回传断裂或资源闲置。
- 这篇论文适合支撑“UAV-MEC 研究正从单机位置优化走向多节点拓扑化部署”的判断。

## Related Work 写作素材
- 与只做轨迹跟踪用户的工作相比，本文更强调稳定位置部署和回传连接。
- 与传统确定性双层优化相比，本文用 PPO 处理更强的动态性和故障扰动。
- 与单 UAV 卸载工作相比，本文体现了多 UAV 中“有的服务、有的桥接”的角色分工。

## 相关系统建模页
- [[计算卸载模型]]
- [[信道与通信速率模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[近端策略优化（PPO）]]
- [[任务卸载]]
- [[无人机部署优化]]
- [[UAV辅助MEC]]
- [[任务卸载与资源分配研究主线]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/wang2025JointPositioningComputation.md)
