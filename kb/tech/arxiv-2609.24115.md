---
id: arxiv-2609.24115
name: "EDGEGEN: Improving Tool-Calling Agents Beyond Happy Paths with Synthetic Edge Case Generation"
field: [LLM agents, 数据合成与评估]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-09-21"
maturity: paper
venue_tier: arXiv
reproducibility_level: medium
signal:
  venue: "arXiv"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "48 小时赛期内可复刻的『beyond happy paths』自测流水线：从自家 agent 的规格与数据库 schema 提取合规规则 → 用 LLM 生成击穿规则的数据库接地边界任务 → 测出崩溃点再修——评委压力测试环节的差异化防线，且全程合成数据、零真实用户数据零隐私合规负担；无官方代码但 pipeline 模式纯 LLM 调用即可实现"
    reuse_cost: 低
  - track: "双创-文书与申报"
    edge: "『AI+软件质量保障 / agentic 测试』选题的技术叙事：企业场景真实任务数据受隐私约束不可得，EdgeGen 的『规则提取+数据库接地合成』给出合规闭环数据引擎的完整故事（tau2bench airline 微调 +2~42% mean progress、harness 优化较人工精选 +10%），测试/质量保障细分在人工智能+赛道里竞争者少、痛点真实"
    reuse_cost: 中
sources:
  - url: https://arxiv.org/abs/2609.24115
    title: "EDGEGEN: Improving Tool-Calling Agents Beyond Happy Paths with Synthetic Edge Case Generation（arXiv abs 页，v1 2026-09-21，CC BY 4.0）"
    accessed: "2026-09-22"
---

# EdgeGen：从合规规则合成边界任务，给工具调用 agent 补 happy path 之外的课

> 来源：https://arxiv.org/abs/2609.24115 （v1 提交 2026-09-21，cs.AI；Comments 字段为"NA"，页面无任何代码链接；抓取日期 2026-09-22。本卡内容出自本次抓取的摘要页。）

## 是什么

arXiv 2609.24115（Harshavardhan Abichandani、Penny Chong、Daniel Dahlmeier 等 10 人，业界团队风格）提出 **EdgeGen**，一个面向工具调用 agent 的合成任务生成框架：

- 从 agent 的**规格（specification）中提取合规规则**，再用这些规则生成**数据库接地的边界任务（database-grounded edge-case tasks）**，任务被刻意设计成违反规则——即 agent 真实使用中会撞上的坑，而非通用题库；
- 与既有合成数据技术组合后，可用于**微调**与 **harness 优化**两条改进路径，整体形成**无需人工标注的全自动闭环**。

效果（摘要自报）：在 **tau2bench airline** 域上微调带来 **+2% 到 +42%** 的 mean progress 一致提升，而部分基线方法在某些模型上反而退化；harness 优化路线上，对 **Gemma-4-e4b** 模型较人工精选 harness **+10%**、较裸 harness **+30%**。

## 解决什么问题

工具调用 agent 的评测与优化需要高质量、多样的任务数据集，但企业场景因隐私等约束拿不到；既有合成任务方法产出泛化题目，无视 agent 底层状态/数据库，反映不了真实使用的多样性——尤其是 happy path 之外的边界情况。EdgeGen 用"规则 + 数据库接地"两个锚点让合成任务既贴身又刁钻。

## 相比前方法优势

- 相比通用合成任务生成（摘要指其无视 agent 底层状态）：任务从 agent 自己的数据库状态与合规规则里长出来，边界用例天然对准该 agent 的真实薄弱面；
- 相比人工标注/人工精选任务集：全自动闭环无标注成本，harness 优化即超人工精选 +10%；
- 相比只报微调增益的工作：给出微调与 harness 优化**两条路径**的对照证据，且指出部分基线在某些模型上退化——评估口径更诚实。

## 局限

- **无代码**：arXiv 页无仓库链接、Comments 为"NA"（2026-09-22 实抓），全部 pipeline 需按正文自实现；
- 摘要只报 tau2bench airline 单域微调结果与 Gemma-4-e4b 单模型的 harness 优化结果，跨域/跨模型泛化未证；"mean progress"是 tau2bench 特有指标，横向可比性有限；
- 规则提取质量依赖规格文档的完善度——规格本身含糊时，合成出的"边界"可能打偏；
- v1 预印本无 venue，业界团队工作有不开源先例，可获取性存疑。

## 如何用于比赛（比赛映射展开）

- **黑客松（数据与算法）**：把论文方法降维成赛期可执行的轻量版——赛前/赛中用一次 LLM 调用批量跑"读我的工具 schema 与业务规则 → 生成 20 条击穿规则的任务 → 跑崩了的记录下来修"，demo 环节展示"我们自己生成的边界用例集 + 修复前后对比"，正面回应评委最爱的现场压力测试；不需要论文的微调路线，纯 harness 侧收益已可演示（reuse_cost=低，模式复刻无代码依赖）。
- **双创（文书与申报）**：做 agent 测试/质量保障方向的项目书时，EdgeGen 提供"隐私合规 × 数据引擎"的完整技术叙事：客户数据出不了域，但规则和 schema 可以——合成边界任务既是卖点也是护城河论证；引用其 +2~42% 的微调证据支撑"数据引擎驱动 agent 持续改进"的产品闭环主张（reuse_cost=中，需自建 pipeline 并补齐跨域验证）。
