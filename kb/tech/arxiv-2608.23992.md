---
id: arxiv-2608.23992
name: "Hybrid Semantic Tool Discovery for Enterprise MCP Gateway（SCOUT）"
field: [LLM agents, MCP, 工具检索/hybrid search]
directions: [黑客松与数据竞赛]
published: "2026-08-25"
maturity: paper
signal:
  venue: "arXiv v1（cs.IR/cs.AI，页内无 venue/comments 标注；摘要自称已部署于 PayPal 生产环境，无法独立核实）"
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "MCP/工具型 agent 作品的上下文瘦身支柱：不把全量 tool schema 塞进 system prompt，而是收敛为 tool_search + execute_tool 两个元工具，BM25 稀疏检索 + 稠密向量检索经 Reciprocal Rank Fusion 融合、按查询返回 top-k 工具——论文口径 token 占用 140.2k→1.3k（上下文的 70.1%→0.8%，降 99%），且以标准 MCP 工具形态暴露、对底层模型零侵入。现场演示『接入几十个工具后上下文占用反而骤降』是硬量化差异化点"
    reuse_cost: 低
    open_source: "无（arXiv 页未附仓库链接，系 PayPal 内部部署；2026-08-28 实抓确认）"
sources:
  - url: https://arxiv.org/abs/2608.23992
    title: "Hybrid Semantic Tool Discovery for Enterprise MCP Gateway: Architecture and Implementation"
    accessed: "2026-08-28"
---

# SCOUT：企业 MCP 网关的混合语义工具发现

> 来源：https://arxiv.org/abs/2608.23992 （arXiv v1 提交于 2026-08-25 02:33:44 UTC，作者 Olympia Saha、Amy Wang、Srinivasan Manoharan，cs.IR/cs.AI；抓取日期 2026-08-28）

## 是什么

arXiv 2608.23992 提出 **SCOUT（Selective Context Optimization for Universal Tooling）**——部署在 MCP 代理网关（proxy MCP server）层的工具发现机制，把"暴露哪些工具"当做一个**上下文选择问题**而非"全部塞进去"问题（以下均来自本次实抓的摘要页）：

- **两个 MCP 元工具**：`tool_search` 与 `execute_tool`——agent 先检索再调用，工具目录不再整体进入上下文；
- **混合检索**：BM25 稀疏检索 + 稠密向量检索，经 Reciprocal Rank Fusion（RRF）融合，返回 top-k 候选工具；
- **规模与运维**：支撑 2,000+ 已索引工具、200+ 后端服务器，支持零停机的目录更新；
- **实测口径**：工具相关 token 从 140.2k（占上下文 70.1%）降到 1.3k（0.8%），约 99% 缩减；因以标准 MCP 工具形态暴露，对任意模型生效、无需改客户端；
- 摘要称该系统**已部署于 PayPal**（企业生产部署为主张，本次无法独立核实）。

## 解决什么问题

MCP 网关把大量后端工具服务器聚合到单端点后，出现两个痛点：一是全量工具 schema 在用户查询发出前就吃满模型上下文窗口；二是面对 2,000+ 工具，用户/agent 找不到最合适的那个。提示缓存只能省钱，既不释放上下文也不提升选工具的准确率。

## 相比前方法优势

- **上下文经济学**：从"工具占用 70% 上下文"到"0.8%"，长工具目录下可用上下文几乎全额返还给任务本身；
- **检索优于全列**：混合检索（稀疏+稠密+RRF）按查询动态选工具，优于把工具清单整块塞给模型靠它自己挑；
- **零侵入可移植**：对模型与客户端均为标准 MCP 工具，换底层模型不重做工程。

## 局限

- **无公开实现**：arXiv 页无代码仓库（runnable=false），PayPal 部署属企业内部系统，赛场复用需自行搭建；
- 检索内核（BM25 + 向量 + RRF）是标准 IR 组件——本文的独有贡献在"元工具化 + 上下文选择"的架构框架与企业级落地，复现时不可声称方法本身复杂；
- 评测数字（99% 缩减）绑定其企业规模（2,000+ 工具）与自建负载，黑客松规模的工具目录（几十个）下上下文压力本就小，演示需自行构造压力场景；
- 零停机目录更新、企业治理等特性超出赛场需要，论文细节（页内无 comments/venue）未过同行评审。

## 如何用于比赛（比赛映射展开）

- **黑客松-数据与算法**：任何 MCP/多工具 agent 作品（浏览器 agent、数据分析 agent、办公自动化 agent）都可加这层"工具检索网关"——工具描述入库（BM25）+ 向量化（现成 embedding）+ RRF 融合，封装成 `tool_search`/`execute_tool` 两个元工具，一天内可落地（reuse_cost=低）；
- **演示打法**：现场往目录里持续注册新工具，展示 system prompt 不变、上下文占用不涨、工具照样被找到——"规模化"叙事配合论文 70.1%→0.8% 的口径作对照；
- **风险自担**：数字引用须注明"论文企业环境口径"（铁律 4——自家作品的实测占用需自己跑出来）。
