---
id: gh-JordyZomer_lemmalog
name: "Lemmalog：把 LLM Agent 记忆做成可证明的演绎数据库（Rust Datalog 引擎 + MCP 共享大脑）"
field: [LLM agents]
directions: [黑客松与数据竞赛]
published: "2026-08-27"
maturity: demo
signal:
  venue: GitHub
  stars: 295
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "Agent 类作品的『可审计记忆』差异化卖点：记忆不是向量库相似度而是演绎数据库——每条事实带溯源、why() 给出证明树、矛盾候选自动派生、双时间戳（valid_from/valid_to）区分事实有效期与断言期；评审可现场追问『你为什么记得这个』并得到机器可验证的回答，这是 RAG 系 agent 作品普遍答不出的；MCP server（12 工具）+ 现成 agent skill 直接挂进 Claude Code/Kimi CLI 当共享大脑，赛道内叙事成本低"
    reuse_cost: "中"
    open_source: "https://github.com/JordyZomer/lemmalog（MIT，Rust；MCP server 需 --features mcp 编译）"
sources:
  - url: https://github.com/JordyZomer/lemmalog
    title: "JordyZomer/lemmalog: A Datalog engine for LLM agent memory"
    accessed: "2026-09-09"
  - url: https://raw.githubusercontent.com/JordyZomer/lemmalog/main/README.md
    title: "README 全文（实现状态表/实体消解/MCP 部署/agent skill）"
    accessed: "2026-09-09"
---

# Lemmalog：把 LLM Agent 记忆做成可证明的演绎数据库

## 是什么

JordyZomer 于 2026-08-27 开源的 Rust crate（295 star，MIT，API 实查 2026-09-09：推送至 2026-09-02），论点是"agent 的记忆应该是演绎数据库"：在摄取边界用 LLM 抽取基础事实，规则负责推导闭包、时间投影、矛盾候选与相关性扩散；每条事实回指来源片段（provenance），每轮对话增量更新派生视图而不是重新推理。实现清单（README 实抓 2026-09-09）：运行时解析的分层 Datalog（含负环拒绝的 negation-as-absence）、半朴素不动点 + 每 epoch 增量维护、双时态事实列 + `now()`、半环标注（置信度乘积 t-范数 × 溯源集合并，重推导时取最大置信/合并溯源）、`why()` 证明树、magic-sets 按需求值（`ask_deep` 点查询免全量不动点）、BM25 + 实体/图加成的混合检索（预算感知）、确定性更新策略（ADD/UPDATE/NOOP/升级人工）、实体消解（星形别名 + 方向性规范视图，拓扑违例派生 `alias_conflict` 而非静默合并）、快照持久化、`what_if` 假设推演（字节级还原存储）、REPL。质量手段：450 个随机程序对朴素不动点 oracle 的差分测试 + 解析器 fuzzing；点查询在 400 万事实规模约 100µs（README 自述）。交付形态三种：库、MCP server（stdio JSON-RPC，12 工具，注册进 Claude Code/Kimi CLI）、通用 agent skill（把引擎当任意长程任务的工作记忆，编码 assert-as-you-verify/先查询再推理/why 之后才信等纪律）。

## 解决什么问题

LLM agent 记忆的"记住但不可信"：向量库只做相似度召回，无法回答"这条知识从哪来、是否仍然有效、和别的知识矛不矛盾"，且每轮把记忆塞进上下文重新推理既贵又漂移。Lemmalog 把"记忆"改成可机械检验的对象——知识变更可推导、可增量、可撤销（scoped recompute 只重算传递依赖），让 agent 拿到的每条上下文都带证明与置信度。

## 相比前方法优势

- 相比向量库/RAG 记忆（同库方向已收的 graph-memory 类方案多为论文无码）：确定性演绎 + 溯源 + 证明树，"为什么"可当场验证；BM25+图加成只是读路径，语义相似度降级为侧索引（`Embedder` trait，默认 HashEmbedder）而非记忆本体；
- 相比"把对话史塞长上下文"：增量派生视图 + epoch 变更日志（`changes_from/since`、"new in memory"区段），长会话下不必每次全文重读；
- 相比 LangChain 系 memory 模块：撤销/取代（supersession）走 DRed-lite 局部重算，且实体消解的冲突显式派生而非静默合并——README 记录了差分测试抓出的两个真实引擎 bug（同层依赖漏重算、首跑失效序错），工程诚实度高。

## 局限（如实标注）

- 摄取质量取决于 LLM 抽取器（`Extractor` trait 的 `LlmExtractor`）：基础事实错则闭包整层错，引擎只保证"从事实出发的推理正确"，不保证事实本身正确；
- 语义侧索引默认是 HashEmbedder（玩具级），真要语义召回需自接嵌入模型；
- README 明确标注 leapfrog triejoins、DBSP 流式增量属"future phases"未实现；
- 单人研究项目（创建 2026-08-27），无生产部署案例；规则/本体设计仍需使用者自己写，冷启动成本在规则层不在代码层；
- Rust 编译（`cargo build --release --features mcp`）对纯 Python 队伍有一道工具链门槛。

## 如何用于比赛

1. **黑客松 Agent 赛道（主用）**：做多轮/多日长程 agent 作品（调研助手、运维诊断、多 agent 协作）的共享记忆层——差异化叙事是"我们的记忆可审计：每个结论能展开证明树、矛盾会被引擎点名"，演示时当场 `why()` 一条结论给评审看，与清一色向量 RAG 作品拉开身位；MCP 12 工具现成，挂 Claude Code/Kimi CLI 半天内可跑通。reuse_cost 中：接入快，但要赛前设计好本体 schema 与规则集（建议直接抄其 agent skill 的最小互操作模式：located/describes/hypothesis/decision）。
2. **工程纪律移植（零成本）**：其"assert-as-you-verify、规则即实验、query 之后再推理、报告由引擎生成"的 skill 纪律，即使不用引擎也值得抄进任何长程 agent/数据分析作品的操作规范——防的是长轨迹里目标漂移与自欺式结论。
