---
tags: [论文, 空中计算, HAP, 任务卸载, 资源分配]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/nabi2025JointOffloadingDecision.md
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
  - ESAC
  - matching game
datasets: []
hardware_stack: []
artifact_availability: unknown
reproducibility_level: medium
---

# Nabi2025 UAV与HAP协同层次化空中计算联合卸载

## 单行摘要
论文构建 UAV 与 HAP 协同的层次化空中计算平台，并通过匹配博弈与 ESAC 联合优化卸载决策、用户关联和资源分配。

## 题目驱动研究框架
- 研究场景：面向偏远地区和灾害场景的层次化空中计算平台。
- 研究对象：地面用户 GUs、多架 UAV、一个 HAP、异构任务与动态位置更新。
- 核心问题：如何在 UAV 接入与 HAP 上层算力支撑的体系中，同时兼顾能耗、时延与负载均衡。
- 标题承诺的方法：joint offloading decision, user association, and resource allocation。
- 期望效果：提升任务完成率并降低系统延迟和能量消耗。
- 标题与正文的偏差：正文的真正亮点是把 GUs 到 UAV 的二元卸载与 UAV 到 HAP 的部分卸载分成两层控制，并分别用匹配和连续动作 DRL 求解。

## Algorithm Design 快照
论文研究 UAV 与 HAP 协同组成的层次化空中计算系统，其中地面用户先与某架 UAV 建立关联，再由 UAV 决定任务是在本机处理还是部分转发到 HAP。难点在于用户侧关联和上层资源分配紧密耦合，且系统目标同时涉及时延、能耗和负载均衡。为此，作者提出 JOUR 方案：先用匹配博弈完成 GUs 的卸载决策与 GU-UAV 关联，再用增强版 Soft Actor-Critic 处理 UAV 部分卸载、UAV 计算资源分配和 HAP 资源分配。这样可以把离散匹配和连续控制分层处理，适配层次化空中计算平台。

## 图1系统框架草案
- 系统实体：GUs、四架 UAV、一个 HAP。
- 任务/数据流：GUs 将任务卸载至关联 UAV；UAV 再决定本地执行或部分转发至 HAP 处理。
- 控制/优化变量：GU-UAV 关联、GU 初始卸载决策、UAV 到 HAP 的部分卸载比例、UAV 与 HAP 计算资源分配。
- 约束来源：任务时延上限、计算能力、电池能量、通信带宽、系统负载均衡目标。
- 画图提醒：图中要明确表现“地面接入层 - UAV 边缘层 - HAP 稳定算力层”的三级结构。

## System Model
- 地面用户每个时隙生成一项任务，任务具有大小、计算复杂度和最大容忍时延。
- GUs 只能关联一架 UAV，而 UAV 都位于 HAP 覆盖范围内，因此 HAP 构成稳定上层计算节点。
- GUs 到 UAV 的卸载为二元决策，UAV 到 HAP 的转发允许部分卸载，这体现了两层卸载粒度差异。
- 优化目标综合考虑能耗、时延和 UAV 负载均衡，不再只是单一延迟最小化。

## Algorithm Design 详解
- 第一步通过 GOUA 算法处理地面用户的卸载与 UAV 关联，把离散匹配问题先稳定下来。
- 第二步使用 ESAC 处理 UAV 到 HAP 的部分卸载和计算资源分配，适合连续动作空间。
- 第三步在奖励设计中同时编码能耗、时延和负载均衡，使 HAP 不只是“兜底算力”，而是负载调节器。
- 与[[Jia2025_UAV与HAP协同空中MEC的分布鲁棒优化]]相比，这篇论文更强调学习驱动的分层控制，而不是不确定 CSI 下的鲁棒解析优化。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成层次化空中计算场景
- 平台与软件：未说明
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：仿真设置较完整，但实现平台、训练框架和代码开放情况未披露。

## Introduction 写作素材
- 单纯依赖地面 MEC 在灾害和偏远场景下存在覆盖与韧性不足的问题，层次化空中计算可以提供更灵活的补位。
- HAP 的意义不只是扩覆盖，更是给 UAV 提供一个稳定的上层算力与回传支撑层。
- 这篇论文适合支撑“空中计算从单层 UAV 向分层 UAV-HAP 平台演化”的写作判断。

## Related Work 写作素材
- 与传统 UAV-MEC 相比，本文把 HAP 引入空中计算而非仅作回传背景。
- 与纯解析优化工作相比，本文把离散关联和连续资源控制分成 matching + ESAC 两段求解。
- 与用户直连远端高空平台的设定相比，本文保留了 UAV 的接入灵活性与 HAP 的稳定性。

## 相关系统建模页
- [[计算卸载模型]]
- [[信道与通信速率模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[层次化空中计算]]
- [[高空平台（HAP）]]
- [[空中计算]]
- [[任务卸载与资源分配研究主线]]
- [[UAC研究路线图]]

## 来源
- [原文](../raw/markdown/nabi2025JointOffloadingDecision.md)
