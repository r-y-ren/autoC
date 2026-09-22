---
id: arxiv-2609.22573
name: "Zero-Trust Authorization and Discovery for Enterprise MCP"
field: [LLM agents, MCP 安全, 零信任授权]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-09-18"
maturity: paper
venue_tier: arXiv
reproducibility_level: medium
signal:
  venue: "arXiv"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "MCP 工具类作品的安全层速赢：论文实测证明『让模型看不见未授权工具』（permission-filtered tool visibility）能把禁用工具暴露从 152/720（21.1%，仅靠调用时校验）压到 0/720，且在 FastMCP 上只需声明式注解+过滤 list_tools 即可复现——现场演示 prompt injection 下隐藏工具零暴露，配合『只藏不拦会被猜名绕过（最高 94% 命中）』的反例展示纵深防御，是 MCP 赛道少有的带数字的安全差异化"
    reuse_cost: 中
  - track: "双创-文书与申报"
    edge: "企业 agent 平台的零信任授权叙事：六个官方 MCP SDK（Python/TS/Go/Rust/C#/Swift）的三项授权缺口调研（单头凭证提取、无预认证发现、基础 SDK 无逐工具授权）是现成的市场痛点证据；2160 次尝试×4 个前沿模型的实测数字支撑『授权不能依赖模型自觉』的产品主张——企业级 MCP 网关/安全中间件方向的立项依据"
    reuse_cost: 中
sources:
  - url: https://arxiv.org/abs/2609.22573
    title: "Zero-Trust Authorization and Discovery for Enterprise MCP（arXiv abs 页，v1 2026-09-18，Huan Li/Yuwei Wang/Srinivasan Manoharan）"
    accessed: "2026-09-22"
---

# Zero-Trust MCP：企业 MCP 的零信任授权与发现（六 SDK 缺口调研 + 2160 次实测）

> 来源：https://arxiv.org/abs/2609.22573 （v1 提交 2026-09-18，cs.CR/cs.AI；页面无 Comments、无代码链接；抓取日期 2026-09-22。本卡内容出自本次抓取的摘要页。）

## 是什么

arXiv 2609.22573（Huan Li、Yuwei Wang、Srinivasan Manoharan）处理企业场景下 MCP（Model Context Protocol）的授权问题：agent 把自然语言上下文——其中可能含攻击者可控文本——翻译成特权工具调用，因此**授权必须在 agent 被提示注入或对抗性操纵时仍然有效**。两个部分：

- **缺口调研**：审计六个 MCP 官方 SDK（Python、TypeScript、Go、Rust、C#、Swift），发现三项缺口——单头（single-header）凭证提取、无预认证工具发现、基础 SDK 无逐工具授权；作者以 FastMCP 扩展形式补齐：跨头凭证规范化、跨 IdP 的缓存 token 校验、未认证的发现元数据端点、经一条声明式注解实现按权限过滤的工具可见性——不改协议；
- **实证**：2160 次尝试×四个前沿 LLM——仅靠调用时（in-body）校验仍暴露禁用工具 **152/720（21.1%）**，而权限感知的可见性控制做到 **0/720**；但发现控制单独可被绕过（模型靠名字猜中隐藏工具的比例最高 **94%**），证明发现层过滤不能替代调用时刻的强制执行。

## 解决什么问题

MCP 官方 SDK 的授权原语达不到企业要求：凭证提取面窄、工具发现不设防、逐工具授权缺位，而"相信模型会自觉不调不该调的工具"在注入攻击下被实测证伪（21.1% 暴露率）。本文给出零信任的分层改法：可见性层（模型看不到未授权工具）+ 发现层（预认证元数据）+ 调用层（逐工具强制），并用数字证明单层不够、组合有效。

## 相比前方法优势

- 比"运行时拦截"多一层**可见性防御**：库内 SARA（arxiv-2608.27146）解决调用时刻的授权判定，WebMCP-Phalanx（arxiv-2608.24017）划浏览器 agent 信任边界，本文补的是**工具可见性/发现层**——模型看不见的工具注入提示词也调不动（0/720），三者是纵深防御的不同层而非重复；
- 有 SDK 级工程落点：结论落在 FastMCP 声明式注解与元数据端点这种可直接抄的改法上，不是纯框架论述；FastMCP 本身开源，复现路径明确；
- 数字带反例：既证明可见性有效（0/720 vs 152/720），也证明"只藏不拦"会被猜名绕过（94%）——防止被简单化滥用，这类正反数字在 MCP 安全文献里少见。

## 局限

- v1 预印本无 venue，作者的 FastMCP 扩展未见官方仓库发布（GitHub 检索无对应实现，2026-09-22 实查），runnable 只能落在"基于开源 FastMCP 自行实现"；
- 实测的"绕过"（94% 猜名）与"拦截"（0/720）绑定四个前沿模型的当时能力，模型与 MCP 生态迭代快，数字时效性存疑；
- 企业场景（IdP、跨头凭证）重，比赛/原型场景用不到全部组件，需自行裁剪；
- 与 SARA/WebMCP-Phalanx 同属"别信模型"家族，引用时需分层表述，避免同质化叙事。

## 如何用于比赛（比赛映射展开）

- **黑客松（数据与算法）**：做 MCP 工具/MCP server 类赛题时加一层"权限感知可见性"——用 FastMCP 的声明式注解给工具标权限，list_tools 按调用者权限过滤，调用层再做逐工具校验；演示双条件对比：注入攻击下"仅调用时校验"会暴露禁用工具、"可见性+校验"零暴露，再补一个"只藏不拦被猜名"的反例演示纵深防御必要性。论文数字（0/720 vs 152/720、94% 绕过）直接用作评审说服材料（reuse_cost=中：FastMCP 开源，扩展代码需自写但量小）。
- **双创（文书与申报）**：企业 agent 平台/安全中间件方向的立项论据——六 SDK 缺口调研直接当"市场痛点：官方生态授权原语缺位"的证据，2160 次实测当"威胁真实性"的证据，产品方案按"可见性/发现/调用三层强制"架构展开；做 MCP 网关、agent 权限管理类产品的申报书里，这是极少数带同行可验证数字的痛点论证（reuse_cost=中：调研结论可引用，产品化需自建扩展）。
