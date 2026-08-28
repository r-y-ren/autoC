---
id: arxiv-2608.27146
name: "SARA: Separating Action Induction from Runtime Authorization in Tool-Augmented LLM Agents"
field: [LLM agents, agent security, prompt injection]
directions: [黑客松与数据竞赛]
published: "2026-08-27"
maturity: paper
signal:
  venue: "arXiv"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "agent 应用类黑客松作品的运行时安全层：把『工具输出=不可信命令』的攻防做成可演示差异化——隔离探针只看用户目标与策略、动作出处台账逐步留痕、No-History-Promotion 防历史漂白；相对『提示词里加一句防注入』的普遍做法，给出架构级分离+可审计叙事，攻防对比演示对评审直观；作者自报 AgentDojo/AgentDyn 上 ASR≤0.63%（v1 未经同行评审）"
    reuse_cost: 中
sources:
  - url: https://arxiv.org/abs/2608.27146
    title: "When Tool Outputs Become Commands: Separating Action Induction from Runtime Authorization in Tool-Augmented LLM Agents"
    accessed: "2026-08-28"
  - url: https://arxiv.org/abs/2608.27146
    title: "arXiv Subjects: cs.AI, cs.SE（2026-08-28 实抓）"
    accessed: "2026-08-28"
---

# SARA：把"动作诱导"与"执行授权"拆成两个运行时角色的 agent 安全框架

> 来源：https://arxiv.org/abs/2608.27146 （arXiv v1 提交于 2026-08-27，cs.AI 跨 cs.SE，页面无 Comments、无代码链接；作者 Xiaokun Guo 等 8 人；抓取日期 2026-08-28）

## 是什么

arXiv 2608.27146 提出 **SARA**，一个工具增强 LLM agent 的运行时安全框架（以下均基于本次抓取的摘要页）：核心主张是**动作诱导**（从工具输出文本里决定"下一步做什么"）与**执行授权**（"这个动作是否被允许执行"）被现有 agent 混为一谈，导致工具输出里的动作暗示可以直接驱动有真实副作用的执行。SARA 的三个机制：

- **上下文隔离的 Action Probe**：在 Observation 侧暴露"动作诱导语义"，探针模型在受限上下文下工作，架构上接触不到动作建议内容；
- **动作出处台账**：跨步骤持续记录动作的来源（origin provenance），作为审计/复核信号；
- **执行侧授权判定 + No-History-Promotion**：实际工具调用只对照"用户目标 + 已授权成功执行的审计证据"判授权（满足 goal、执行链与参数级支持）；历史动作的重复出现不得把"出处"漂白成"执行权限"。

作者自报：在 AgentDojo 与 AgentDyn 上，四个主评测设置的攻击成功率（ASR）≤0.63%，任务效用保持有竞争力，且在更多 agent 骨干上一致降低 ASR。

## 解决什么问题

工具输出的角色漂移：它本来只是"数据"，一旦开始"指定具体动作"就实质变成了可驱动真实世界副作用的**命令**（提示注入的 agent 版）。现有防御普遍把"agent 决定动作"与"系统批准动作"压在同一个上下文里，导致注入内容既当运动员又当裁判。SARA 用角色分离+出处留痕让授权判断有可依赖的、未被污染的证据链。

## 相比前方法优势

- **架构级分离而非提示词补丁**：探针接触不到动作建议内容是结构性保证，不是"请忽略指令"式的软约束；
- **出处可审计**：逐步动作溯源提供了事后复核抓手（摘要称完整可审计性）；
- **No-History-Promotion**：针对多步执行中"历史反复出现=获得信任"的漂白路径，是多数注入防御未覆盖的盲区；
- 跨多个 agent 骨干一致降低 ASR（作者自报），说明方法不绑定单一模型。

## 局限

- **无代码发布**（arXiv 页无 Comments、无任何代码链接，runnable=false），Action Probe 隔离架构与授权判定逻辑需自行实现；
- ASR 数字为作者自报的 v1 预印本结果，无同行评审；评测绑定 AgentDojo/AgentDyn 两套基准，攻击模式覆盖面未知；
- 隔离探针意味着每个动作多一次模型调用，延迟/成本开销摘要未量化；
- 摘要未说明对"合法但激进"的用户指令的误拒率如何控制（效用与安全的边界只在主设置里报告）。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：黑客松-数据与算法（任何做 LLM agent 应用的队伍——工具调用、浏览器操作、办公自动化类命题）。
- **打法**：把 SARA 降维成中间件——工具返回内容进沙盒上下文、由独立小模型探针提取"动作候选"，主执行器只对照用户原始目标+白名单策略放行，所有动作带 origin 标记落日志。作品演示环节做一组现场攻防：在工具返回里埋"请转账/请删除"类注入指令，对比有无防护层的 agent 行为，配合出处台账讲"可审计的 agent 安全"——这在 agent 赛题评审里是稀缺的差异化点。
- **降本路径**：无需复现论文全套实验；AgentDojo 公开可测，可用其注入子集做自测。核心工作量在探针隔离与授权规则设计，2-3 人日可出可演示版本（reuse_cost=中，无现成代码是主要成本来源）。
