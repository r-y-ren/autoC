---
tags: [论文, 大语言模型, Q学习, 调度优化, 多无人机协同]
created: 2026-04-10
updated: 2026-04-10
sources:
  - ../raw/markdown/zhou2025LLMQLLLMenhancedQlearning.md
venue_tier: CCF-A
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - idea_seed
validation_type:
  - simulation
  - trace_driven
data_origin:
  - mixed
platforms: []
frameworks:
  - LLM-QL
  - Q-learning
  - prompt engineering
  - ChatGPT-4o
hardware_stack: []
datasets:
  - Seattle city dataset
  - synthetic mFSTSP dataset
artifact_availability: unknown
reproducibility_level: medium
---

# Zhou2025_LLM增强Q学习的多并行无人机调度

## 单行摘要
论文面向卡车-多无人机协同配送中的 `mFSTSP` 问题，提出 `LLM-QL`，以 LLM 生成启发式引导 `Q-learning` 探索，在大规模调度环境中降低无效搜索并提升总完成时间、运行时间与 UAV 利用率。

## 题目驱动研究框架
- 研究场景：卡车与多架并行无人机协同配送。
- 研究对象：卡车、并行 UAV、客户点、约束集合与调度状态。
- 核心问题：大规模 `mFSTSP` 搜索空间庞大，传统启发式或强化学习易陷入高探索成本和局部最优。
- 标题承诺的方法：LLM-enhanced Q-learning。
- 期望效果：利用 LLM 的全局推理能力缩短 Q-learning 探索过程并提升大规模调度质量。
- 标题与正文的偏差：标题强调“LLM + Q-learning”，正文真正的新意是“prompt 化问题建模 + 启发式引导探索 + 幻觉鲁棒性分析”。

## Algorithm Design 快照
作者并没有让 LLM 直接输出最终调度，而是把 LLM 放在强化学习前面充当启发式生成器。系统先将 `mFSTSP` 的约束和状态以 prompt 形式喂给 LLM，获得可用于缩小搜索空间和引导探索的启发式项，再由 Q-learning 在奖励驱动下持续修正策略。这样既利用了 LLM 的全局语义组织能力，又保留了强化学习长期迭代纠错的稳定性。

## 图1系统框架草案
- 任务层：卡车、多个 UAV、客户点和配送约束。
- 提示层：把任务建模转写成 LLM 可理解的 prompt。
- 启发层：LLM 生成中间启发式项指导探索。
- 学习层：Q-learning 在启发引导下更新状态-动作值。
- 评估层：总完成时间、运行时间、UAV 利用率、鲁棒性分析。

## System Model
- 论文研究的是多飞行侧骑手旅行商问题 `mFSTSP`，卡车负责携带、回收和补能 UAV。
- 目标是最小化总完成时间，同时考虑客户规模、UAV 数量、充电与同步约束。
- LLM 不直接执行控制，而是在调度层生成启发式项。
- 数据既包括 `Seattle` 真实城市数据，也包括作者生成的合成数据。

## Algorithm Design 详解
- 第一步：把 `mFSTSP` 的状态、约束和目标函数组织成适合 LLM 理解的 prompt。
- 第二步：让 LLM 生成启发式项或中间变量，缩小 Q-learning 的无效探索区域。
- 第三步：在 Q-learning 中继续依靠奖励学习修正启发式可能带来的偏差。
- 第四步：分析启发式“幻觉”带来的扰动，并验证系统仍能在有限时间内重新收敛。

## 实验证据卡片
- 验证类型：`simulation` + `trace_driven`
- 数据来源：`Seattle city dataset` + 合成 `mFSTSP` 数据集
- 平台与软件：未说明
- 方法组件：`LLM-QL`、`Q-learning`、`prompt engineering`、`ChatGPT-4o`
- 硬件与算力：未说明
- 开源情况：未说明
- 复现判断：`medium`
- 缺失信息：未给出完整代码与调用设置，仅明确了 `ChatGPT-4o` 版本

## Introduction 写作素材
- 在复杂无人机调度问题中，LLM 的价值不一定是直接替代优化器，而是为强化学习提供更有方向感的探索。
- 把 LLM 作为启发式生成器，可以避免“LLM 一步到位求解”不稳定的问题，也比纯 RL 更高效。
- 这篇论文非常适合支撑“LLM 正在从语言交互扩展到组合优化与调度启发”的论述。

## Related Work 写作素材
- 与直接用 RL 求解无人机调度的工作相比，本文引入 LLM 辅助探索。
- 与传统启发式或 MILP 相比，本文更强调大规模问题中的自适应搜索效率。
- 与具身规划类 LLM 工作相比，本文属于“LLM 作为优化辅助器”而非“LLM 直接发动作”。

## 相关系统建模页
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[LLM增强Q学习]]
- [[大语言模型驱动无人机规划]]
- [[多无人机协同]]

## 来源
- [原文](../raw/markdown/zhou2025LLMQLLLMenhancedQlearning.md)
