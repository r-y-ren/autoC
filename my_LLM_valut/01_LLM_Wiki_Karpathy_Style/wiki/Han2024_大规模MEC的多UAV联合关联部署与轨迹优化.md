---
tags: [论文, 大规模MEC, UAV辅助MEC, 部署优化, 轨迹优化]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/han2024JointAssociationDeployment.md
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
  - MATLAB
frameworks: []
datasets: []
hardware_stack:
  - Windows 10 (64-bit)
  - 32 GB RAM
artifact_availability: unknown
reproducibility_level: medium
---

# Han2024 大规模 MEC 的多 UAV 联合关联、部署与轨迹优化

## 单行摘要
论文面向百级以上 IoT 设备的大规模 MEC 场景，联合优化设备关联、UAV 落脚点部署与飞行轨迹以最小化系统总能耗。

## 题目驱动研究框架
- 研究场景：多个 UAV 作为移动边缘节点，为大规模 IoT 设备提供任务采集、执行与结果返回服务。
- 研究对象：IoT 设备集合、多架 UAV、若干 UAV 落脚点与飞行路径。
- 核心问题：在设备数量很大且 UAV 资源有限时，如何同时决定设备归属、落脚点数量/位置和访问轨迹。
- 标题承诺的方法：joint association, deployment and flight trajectory optimization。
- 期望效果：在保证所有设备任务被服务的前提下降低整体能耗。
- 标题与正文的偏差：正文真正的亮点是把关联、部署和轨迹拆成 k-means、IFWA 与贪心轨迹三个协同子模块。

## Algorithm Design 快照
论文把大规模 MEC 场景中的多 UAV 决策拆分为三个强耦合层面：首先通过改进 k-means 完成设备到 UAV 的关联划分；然后用带可变长度编码的改进烟花算法优化每架 UAV 的落脚点数量与位置；最后在既定落脚点上使用预计算贪心策略缩短飞行距离。这样做的核心思想不是追求单一子问题最优，而是通过结构化分解，把原本难以直接求解的大规模能耗最小化问题转化为可协同迭代的组合优化流程。

## 图1系统框架草案
- 系统实体：大规模 IoT 设备、多架 UAV、每架 UAV 的若干 footholds。
- 任务/数据流：IoT 设备上传任务数据，UAV 在落脚点附近采集后本地执行并回传结果。
- 控制/优化变量：设备-无人机关联、落脚点数量与位置、各 UAV 的访问轨迹。
- 约束来源：UAV 飞行与计算能耗、设备规模大、访问顺序与飞行距离耦合。
- 画图提醒：图里应把“聚类关联 -> 落脚点部署 -> 轨迹串联”画成三级流水线。

## System Model
- 每架 UAV 既承担通信采集也承担边缘执行，因此设备归属关系直接影响飞行和计算能耗。
- 论文用 foothold 机制近似连续飞行与服务空间，使落脚点成为部署与轨迹之间的中介变量。
- 目标函数是总能耗最小化，意味着系统同时关注 UAV 访问长度和服务组织结构。
- 由于 IoT 设备数量超过百级，模型重点不再是单一精细轨迹，而是大规模系统可分解求解。

## Algorithm Design 详解
- 第一步用改进 k-means 处理 IoT 设备到 UAV 的关联，把大规模设备集划分成多个服务簇。
- 第二步用 IFWA 优化每架 UAV 的落脚点部署，动态决定落脚点个数与位置。
- 第三步在给定落脚点上使用预计算贪心算法生成低飞行距离轨迹。
- 第四步对比多种基线，并用 Friedman 排名与 Wilcoxon 检验验证性能优势。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景或参数仿真
- 平台与软件：`MATLAB`
- 硬件与算力：`Windows 10 (64-bit)`；`32 GB RAM`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：论文给出了大规模实例与统计显著性检验，适合作为“多 UAV 部署 + 轨迹 + 关联”联合设计的结构化参考。

## Introduction 写作素材
- 当设备规模上升到百级以上时，只研究单一 UAV 的轨迹或单独的卸载变量已经不足以反映系统真实复杂度。
- 大规模 UAV-MEC 的前置问题往往是设备该由谁服务、UAV 应落到哪里，而不是直接求连续轨迹。
- 这篇论文适合支撑“系统规模上升后，关联、部署与轨迹必须一起设计”的引言转折。

## Related Work 写作素材
- 与只做 UAV 部署或只做轨迹规划的工作相比，本文把关联、部署和轨迹统一起来。
- 与纯解析优化不同，本文采用聚类、进化算法与贪心路径的组合式求解。
- 与小规模多 UAV 协作不同，本文强调大规模 IoT 任务场景下的可扩展组织方式。

## 相关系统建模页
- [[计算卸载模型]]
- [[区域覆盖与部署模型]]
- [[无人机能耗模型]]

## 相关概念与主题页
- [[无人机部署优化]]
- [[UAV辅助MEC]]
- [[覆盖与部署优化主线]]
- [[轨迹优化与协同控制]]

## 来源
- [原文](../raw/markdown/han2024JointAssociationDeployment.md)
