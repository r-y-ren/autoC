---
id: arxiv-2608.25992
name: "ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs"
field: [LLM agents, agent orchestration, cost-aware routing]
directions: [黑客松与数据竞赛]
published: "2026-08-26"
maturity: paper
signal:
  venue: "arXiv (EMNLP 2026 Findings)"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "预算内多智能体管线的编排差异化：黑客松作品普遍是 planner→coder→reviewer 式多步 agent 管线，token 免费额度烧穿后迭代被迫中断——ProgRouter 把'时间/成本预算'变成编排的一等约束（多视图进度打分 + 双路进度预测 + 自适应元门控，按每步'预测进度增益'决定调用哪个 LLM），在 HumanEval Plus/MBPP/MATH-500/ASQA 四类任务上以更低运行成本保持性能；EMNLP 2026 Findings 接收构成答辩引用强度，'预算内自适配路由 + 成本仪表盘'是评委可感知的工程差异化"
    reuse_cost: 高
sources:
  - url: https://arxiv.org/abs/2608.25992
    title: "ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs"
    accessed: "2026-08-28"
---

# ProgRouter：质量-成本权衡下的在线进度引导多智能体编排

> 来源：https://arxiv.org/abs/2608.25992 （arXiv v1 提交于 2026-08-26 16:42:02 UTC，cs.AI 主分类、交叉 cs.MA；Comments 标注 Accepted in Findings of the Association for Computational Linguistics: EMNLP 2026；作者 Songyuan Li、Ahmed M. Abdelmoniem、Shiqiang Wang；抓取日期 2026-08-28）

## 是什么

arXiv 2608.25992 提出 ProgRouter——一个在线（online）进度引导路由框架，用于多智能体 LLM 工作流的逐步编排：在给定的时间与成本预算内，跨工作流步骤自适应选择调用的 LLM agent。三个核心组件（摘要原文归纳）：

- **多视图任务进度打分器（multi-view task progress scorer）**：估计当前步骤对任务的推进程度；
- **双路进度预测器（dual-path progress predictor）**：预测候选 LLM 接手后的进度走向；
- **自适应元门控（adaptive meta-gating）**：估计每个候选 LLM 的"进度增益"，据此决定这一步把工作交给谁。

页面索引词：collaborative agentic workflows、LLM agent orchestration、quality-cost trade-off、task progress prediction、online decision-making。

## 解决什么问题

多智能体 LLM 工作流能对复杂任务做协同推理，但重复调用与长程上下文使其成本高企。静态编排（固定模型、固定流程）要么全程烧旗舰模型迅速打爆预算，要么全程廉价模型掉性能。ProgRouter 把"每一步该花多少钱"变成在线决策：用预测的进度增益对冲候选模型的调用成本，在预算约束下保住质量。

## 相比前方法优势与局限

**优势**：在 HumanEval Plus、MBPP（agentic 代码生成）、MATH-500（数学推理）、ASQA（检索增强长文 QA）四类任务上，相对关键基线降低运行成本且保持强性能（摘要未给具体百分比）；EMNLP 2026 Findings 接收，方法学经过评审；在线决策不依赖对任务的事先完整规划，适合动态工作流。

**局限**：
- **无开源**：Comments 只写接收信息，页面无任何代码链接（signal.runnable=false）；
- 摘要未说明进度打分器与预测器是否需要训练数据/标注，复现前必须读原文核对——这直接决定复用成本；
- 收益叙事以"成本下降 + 性能保持"为主，绝对性能数字未在摘要层披露；
- 评估域限于代码生成/数学/RAG 长文 QA，迁移到其他工作流类型（如数据分析管线）的效果未知；
- 每步额外的进度打分与预测调用本身有开销，短任务上可能得不偿失。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：黑客松中任何"多步 agent 管线"型作品（planner→coder→reviewer、多 agent 数据分析、自动报表生成），尤其 API 免费额度有限、需要向评委演示"预算感知工程能力"的场合。
- **打法（简化变体，reuse_cost=高）**：完整方法无代码需自实现，且打分器/预测器的训练需求待原文核对；48 小时内可做轻量版——用廉价模型对每步产物打进度分，预测进度增益低于阈值就把下一步降级到小模型、关键步骤（最终代码合成等）升级旗舰模型，配合 token 消耗仪表盘展示"同等预算下比固定模型队伍多跑数轮迭代"。与库内已收的贝叶斯自升级卡片（不确定性触发单点升档）互补：ProgRouter 是预算-进度维度的连续路由。
- **差异化话术**：答辩时以"quality-cost tradeoff 下的在线编排"命名自家管线调度逻辑，引用 EMNLP 2026 Findings 说明该问题已被顶会确认为开放研究问题，比"我们用了多智能体"高一个论证层级。
- **风险**：路由器自身的 API 调用次数会增加；任务步骤少（<5 步）时编排收益不成立，赛前用题面估步数再决定是否引入。
