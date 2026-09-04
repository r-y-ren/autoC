---
id: arxiv-2609.03340
name: "Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory"
field: [LLM agents, 分布式系统, 内存一致性]
directions: [黑客松与数据竞赛]
published: "2026-09-03"
maturity: paper
signal:
  venue: "arXiv v1（2026-09-03 提交，cs.AI；摘要页无代码仓库链接）"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "AI Agent 安全赛/多 agent 编排赛的现成防护层与强对比叙事：多 agent 作品最体面的现场翻车就是'评审中途改数据/改需求，agent 仍按旧计划执行'——论文给该故障正式命名（stale-plan execution）并给出轻量解法；PlanFence 协议（计划引用其依据的确切公共记录 + executor 执行前只验证可能影响该动作的依赖 + 验证不全即重规划或阻塞）纯协议层、零训练、与具体 LLM 无关，比赛作品挂上即用；'仅查新鲜度 30/30 全中招 vs PlanFence 全部完成且零无效动作'可复刻为作品的评测实验（注入修订、测失效动作率），对比冲击力强"
    reuse_cost: 低
sources:
  - url: https://arxiv.org/abs/2609.03340
    title: "Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory"
    accessed: "2026-09-04"
---

# Fresh Memory, Stale Plans：分布式 LLM-agent 内存的依赖范围验证

> 来源：https://arxiv.org/abs/2609.03340 （arXiv v1 提交于 2026-09-03，主分类 cs.AI，作者 Chen、Wang、Brinton；摘要页未附代码链接）；抓取日期 2026-09-04

## 是什么

分布式 LLM agent 团队的**动作验证协议 PlanFence**，针对作者命名的故障模式 **stale-plan execution**（陈旧计划执行）：agent 读到的共享事实是新的，但授权其动作的计划已经作废——planner 依据需求 r3 制定计划，另一 agent 提交了 r4，executor 拿到了 r4 却仍在执行基于 r3 的计划（以下均来自本次抓取的摘要页）。核心命题：**状态新鲜不等于授权动作的计划仍然有效**。

PlanFence 机制：

1. 计划必须**引用其依据的确切公共记录**；
2. executor 在外部动作前**只验证可能影响该动作的依赖记录**（dependency-scoped，不做全量同步）；
3. 验证不全则**重规划或阻塞**。

## 解决什么问题

现有分布式 agent 系统的共享内存一致性只到"数据新鲜"层，缺"计划有效性"层。实测：30 个受控实况工作流（均含计划后的修订注入）中，仅查新鲜度的 executor 在**每个任务都**照旧计划执行；PlanFence 完成全部任务且**零无效动作**。重放实验给出条件性权衡：低变更率（churn）下主动同步更优；churn 与共享键空间增大时 PlanFence 扩展性更好。作者明确定位：这是受控的**安全与系统成本**结论，不是通用任务精度改进。

## 相比前方法优势

- **故障命名与定位清晰**：把"数据新鲜但计划作废"从模糊的 agent 失误中分离为独立故障类，可测可防；
- **依赖范围限定**：只验与待决动作相关的记录，避免全量同步的一致性开销——这是它能在高 churn 下扩展的原因；
- **失败安全（fail-safe）语义**：验证不全时重规划或阻塞，而非静默执行；
- 与具体 LLM 无关，是纯协议层机制。

## 局限

- **受控实验**：30 个注入修订的工作流，作者自述非通用任务精度提升——不能宣称"装了 PlanFence 任务完成率更高"；
- **无开源实现**：摘要页无代码链接，maturity 如实标 paper、runnable=false（协议需按论文描述自实现）；
- 场景为单一团队的共享记录工作流，跨组织/更复杂依赖图未覆盖（摘要范围内）。

## 如何用于比赛（比赛映射展开）

- **黑客松-数据与算法（AI Agent 安全赛/多 agent 编排赛）**：两层用法——(a) **防护层**：把 PlanFence 协议直接加进自己的多 agent 作品，作为"计划有效性护栏"，实现成本仅是一层引用记账 + 动作前校验；(b) **评测实验**：复刻论文的修订注入法，对比"裸奔版 vs 护栏版"在评审中途改数据时的失效动作率，30/30 全中招 vs 零无效动作的对比表格是答辩里最有冲击力的页面之一；
- **差异化叙事**：多 agent 赛队比拼"谁的任务完成率高"时，展示"谁的系统在**需求变更下仍然正确**"是正交且更高的评审维度；
- **复用成本评估：低**——零训练、与模型无关、协议机制摘要级即可理解；主要工作量是把"计划引用记录"的记账嵌进既有 agent 框架的状态管理。
