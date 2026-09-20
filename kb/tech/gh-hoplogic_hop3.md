---
id: gh-hoplogic_hop3
name: "hoplogic/HOP 3.0：HopSpec 任务规约语言 + HopJIT 引擎强制的受控 agent 执行"
field: [LLM agent, 任务规约语言, 执行引擎]
directions: [创新创业大赛]
published: "2026-09-11"
maturity: demo
venue_tier: unknown
reproducibility_level: high
signal:
  venue: "GitHub（11 stars，MPL-2.0，npm 包 @hoplogic/hopjit，2026-09-20 API+README 实抓）"
  stars: 11
  runnable: true
competition_fit:
  - track: "双创-文书与申报"
    edge: "『AI+』项目最常被评委质疑『大模型套壳、行为不可控』：HopSpec（markdown 声明任务结构：步骤类型/数据流/循环分支并行/人机介入点）+ HopJIT（引擎强制流控——循环不跳步、门不屈服、人工检查点不可绕过、retry/adaptive 修复与 None 传播）提供现成的『受控 agent 执行』组件，让参赛作品现场演示『目标对齐-边界约束-流程沉淀』的治理层而非纯 prompt 对话；复用模式外层接 Claude Code/Codex 即可、不需另配 API key，赛期接入成本极低；『自然语言 Skill 提炼为可复用流程』（/hop distill）还能作为作品的知识沉淀卖点"
    reuse_cost: 低
    open_source: "https://github.com/hoplogic/hop3（MPL-2.0；npm install -g @hoplogic/hopjit）"
sources:
  - url: https://github.com/hoplogic/hop3
    title: "hoplogic/hop3 仓库实抓（GitHub API + README 原文 2026-09-20：11 stars，MPL-2.0，topics 含 agent-orchestration/dsl/spec-driven；HopSpec=markdown 任务规约语言、HopJIT=npm 引擎 @hoplogic/hopjit、复用/独立两种驱动模式、docs/tutorials 与 examples 在仓）"
    accessed: "2026-09-20"
---

# HOP 3.0：用规约语言 + 引擎强制流控，把 agent 从"对话记忆"里解放出来

> 来源：https://github.com/hoplogic/hop3 （GitHub API + README 原文实抓，抓取日期 2026-09-20。以下分析基于本次实抓的 README 与仓库元数据）

## 是什么

面向 LLM agent 的双态融合语言/运行时（README 口径）：**HopSpec** 是用结构化 markdown 声明任务的规约语言（步骤类型、数据流、循环/分支/并行、人机介入点）；**HopJIT** 是其执行引擎（npm 包 `@hoplogic/hopjit`），负责执行状态管理、变量存储、retry/adaptive 修复、None 传播等流控——"循环不跳步、门不屈服、人工检查点不可绕过"。两种驱动模式：复用模式（外层 Claude Code/Codex 做推理引擎，HopJIT 纯流控，不需 API key）与独立模式（引擎直调 LLM API，MCP server 形态）。配套 /hop（目标转规约）、/hopspec（运行既有规约）、/hopbuild（自然语言 Skill 翻译为规约）、/hop distill（把一次探索的有效做法提纯为可复用流程，未验证分支明确标注）。仓库含引擎源码、13 份概念文档、教程与示例；MPL-2.0；11 stars；文档主体为中文（英文翻译计划中）。

## 解决什么问题

LLM agent 靠对话记忆执行多步任务时，步骤可被跳过、约束可被"说服"、中断后状态丢失；HOP 把"不能漏、必须查、先确认"从提示词层下沉到引擎层，用代码逻辑承载规则与核验，并让验证过的做法沉淀为可复用流程。

## 相比前方法优势

- **规约与执行分离**：任务结构是声明式工件（可 review、可版本化），而非埋在系统提示词里的散文；
- **引擎强制**而非提示约束：跳步/绕过在运行时不可表达，治理承诺可验证——这与 LangChain 式"编排库"（代码写死、无声明层）和纯 prompt 治理（无强制）都不同；
- **人机介入点是一等公民**：检查点不可绕过，适合有合规叙事需求的作品；
- 复用模式零 API key 依赖，教学/演示/赛期接入摩擦小。

## 局限

- **11 stars、发布快照形态**（单向同步自维护者工作仓，PR 由维护者搬运）：社区小、长期维护存在风险（2026-09-20 实抓口径）；
- DSL 本身有学习成本——赛期若只剩两天，直接用不如简化版自查表；
- 文档主体中文、生态早期，遇到引擎级 bug 时外部支援有限；
- 无公开基准数字证明其相对 ReAct 式执行的可靠性增益（其价值主张是结构性的，非跑分型）。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：双创-文书与申报（中国国际大学生创新大赛"人工智能+"高教主赛道等需要治理叙事的 AI 项目）。
- **打法**：
  (a) **治理层组件**：作品的 agent 执行内核直接换/包 HopJIT，现场演示"试图跳步会被引擎拦截、人工检查点必须确认"——这是对"套壳"质疑的具象回应；
  (b) **申报书章节**：引其"声明式规约 + 引擎强制 + 流程沉淀"三层结构作为项目技术架构图的执行层，配 /hop distill 的知识沉淀截图作运营可持续性证据；
  (c) **成本控制**：复用模式不增加 API key 与模型成本，只用现成编码助手即可跑通 demo。
- **成本**：reuse_cost=低——npm 全局安装即用；主要成本是半天读文档写第一份 HopSpec。
