---
id: gh-1173591564_Dynamics-memory
name: "Dynamics-memory：值动力学 + 矛盾裁决的 LLM Agent 有界长期记忆层（含因果回放评测与负结果消融）"
field: [LLM agents, agent memory]
directions: [创新创业大赛]
published: "2026-09-15"
maturity: demo
reproducibility_level: medium
signal:
  venue: GitHub
  stars: 11
  runnable: true
competition_fit:
  - track: "双创-文书与申报"
    edge: "agent 记忆中间件方向的技术方案骨架与罕见的带负结果工程证据：三组对照（记忆层 3.00 vs 全量 log 2.39 vs 无记忆 2.23 续话感）实证『全量 log 入向量库必成史山』的痛点；13 点消融证明多数花哨机制（novelty/consolidation/词法召回）默认关才对、只有 salience 半衰期是独立正贡献——申报书技术方案与工程治理章节可直接引用这套『机制证据分级』方法论作差异化叙事（对比 RAG 堆料同行）"
    reuse_cost: 中
    open_source: "https://github.com/1173591564/Dynamics-memory（无 license，仅可作设计参考，不可直接复用代码）"
  - track: "黑客松-数据与算法"
    edge: "长程 agent 作品需要『接着搞』式跨会话记忆时，其双池 + 滞回晋升降级 + 张力积压延迟裁决 + contested co-serve（未决冲突双方版本随答案同端给下游）是一套可照抄设计自研的架构图；因果回放评测协议（t 时刻提问只能用 t 之前流入的记忆，无前窥）可直接搬去验收自家记忆功能，防评审质疑记忆作弊"
    reuse_cost: 中
    open_source: "https://github.com/1173591564/Dynamics-memory（参考设计自研；官方代码无 license 且依赖单一 ZAI API）"
sources:
  - url: https://github.com/1173591564/Dynamics-memory
    title: "1173591564/Dynamics-memory 仓库页（API 元数据：11 stars/0 fork/2026-09-15 创建/2026-09-19 最后推送/无 license）"
    accessed: "2026-09-22"
  - url: https://raw.githubusercontent.com/1173591564/Dynamics-memory/main/README.md
    title: "README 全文（架构 mermaid 图、值动力学公式、因果回放评测表、13 点消融表、复现命令）"
    accessed: "2026-09-22"
---

# Dynamics-memory：有界自纠错的 agent 长期记忆层

> 来源：https://github.com/1173591564/Dynamics-memory （API 实查 2026-09-22：2026-09-15 创建、2026-09-19 最后推送、11 stars/0 fork、无 license；README 实抓 2026-09-22。单人匿名数字账号仓，但仓库为含 tests/ 与 experiments/ 的完整 Python 工程，README 双语、含负面结果与自报瓶颈，非占位仓。本卡内容出自本次抓取。）

## 是什么

单人开发者的 LLM agent 长期记忆层工程（Python；hybrid_memory/ 包含 core/candgen/embed/semantics/sim/datasets，另有 experiments/、tests/）。核心主张：**raw logs are not memory**——直接把交互 log 全量塞向量库会堆成重复、过期、互相矛盾的"史山"。架构（README mermaid 实抓）：K-unit 窗口 → LLM 候选生成（scene 携带 + 类型 + 溯源）→ 只对**蒸馏后的记忆文本**做 embedding → 经候选池进有界持久池。池由**值动力学**治理：`V ← V·e^(−λ) + η·hit + η_s·shadow`，晋升/降级滞回（θp > θd）、容量驱逐、闲置归档。矛盾处理是差异点：检索内压制即检测（过相似未入选的对全部进 tension backlog 延迟裁决），judge 四分法（同义→合并 / 更新→新替旧 / 矛盾→聚合 memory（内含全部版本+时间戳+pending_review） / 碰撞→都留）；**未决冲突不许自信出场**——入选记忆带未决 tension 时对手版本随答案一并端给下游（contested co-serve）；每条记忆携带 src 溯源。评测用**因果约束回放**（t 时刻提问只能用 t 之前流入的记忆，无前窥），在真实 6 周项目日志（106 交互单元）上：续话感 memory 3.00 / flat-log 2.39 / none 2.23（≥4 分率 38% vs 8%）；自日志 QA 36 题 acc 0.667、拒答 3/3 全对；LoCoMo 跨分布仅 0.29（README 如实披露，归因蒸馏丢细节与协议错位）。**机制证据分级**：Cfg 默认全关（confidence/salience/novelty/consolidation、lex_weight=0），13 点消融中唯一独立正贡献是 salience 半衰期（≥4 率 +15pp、归档 108→69），novelty 与逐题完全相同、词法召回修半题砸一题。自报真实瓶颈在抽取/召回而非动力学：参照要点进 top-5 上下文的仅 ~18%。

## 解决什么问题

两个：一是 agent 长期记忆的"史山"病——全量 log 入库导致检索被重复副本淹没、旧信息压过新状态、context 效率持续劣化，目标是维持"项目进度感与痛点"的活性表征而非记住所有细节；二是记忆系统评测的前窥作弊问题——用因果回放协议保证 t 时刻的问题永远看不到 t 之后的记忆。

## 相比前方法优势

- 相比朴素 log-RAG：有界、自更新（衰减/强化/晋升/驱逐）、显式矛盾处理（聚合 memory + contested co-serve），而不是把冲突留在库里静默污染检索；
- 相比库内记忆路线卡：lemmalog（gh-JordyZomer_lemmalog，Rust Datalog 演绎数据库 + MCP）走形式化证明路线、arxiv-2609.03340 走分布式陈旧性校验路线，本卡是"值动力学 + 检索内冲突自然暴露"路线，机制正交不重叠；
- **负面结果消融是稀缺品**：开源记忆仓普遍只报增益，本 README 用 13 点消融说明多数机制默认关才是对的（"拿不出评测证据的不进默认路径"），对自建记忆系统的队伍是直接省赛期试错成本的工程证据。

## 局限（如实标注）

- **无 license**（2026-09-22 API 实查）：默认版权保留，代码不可直接 fork 进作品，只能参考设计自实现；
- 单人匿名数字账号仓、0 fork、11 stars，正确性与持续性无第三方背书；API 语言字段标 TypeScript 与实际 Python 工程不符（仓内或含 TS 配置文件），元数据卫生一般；
- 评测规模小（106 交互单元 / 36 题），作者自认"方向性证据而非决定性证据"；跨分布 LoCoMo 仅 0.29，泛化未证实；
- 自报瓶颈在抽取/召回（参照要点进 top-5 仅 ~18%）：意味着直接跑其管线，记忆质量上限被上游召回卡死，动力学设计的收益打折；
- 依赖单一 LLM 供应商（ZAI_API_KEY），复现绑定该 API；
- archive 池尚无界（README 自述），长期运行的"有界"主张未完全兑现。

## 如何用于比赛

1. **双创（文书与申报）**：做 agent 记忆/知识中间件方向时，(a) 用其三组对照数字（3.00 vs 2.39 vs 2.23）论证"记忆 ≠ log 堆积"的市场痛点与技术洞察；(b) 把"机制证据分级"表（默认关、消融说话）改写进申报书的技术治理章节，作为区别于 RAG 堆料同行的工程纪律卖点。reuse_cost 中：设计模式与评测协议可搬，代码需因无 license 自行实现。
2. **黑客松（数据与算法）**：长程 agent 作品（跨会话项目助手、多日运维 agent）需要"接着搞"记忆时，照其架构图自研双池+滞回+张力裁决记忆层，并直接采用因果回放协议做验收——评委质疑"你的记忆是不是偷看未来"时，协议本身就是答案。
