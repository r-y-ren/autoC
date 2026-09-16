---
id: gh-kyky2347_ALTA
name: "ALTA：多 LLM Agent 自治研究型虚拟交易平台（证据优先 + 可回放影子账本）"
field: [LLM agents]
directions: [黑客松与数据竞赛]
published: "2026-08-27"
maturity: demo
signal:
  venue: GitHub
  stars: 248
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "金融/Agent 黑客松的『负责任自治系统』参考架构：Scouts 独立找信号→Foundry 冻结可证伪机会→bull/bear 对辩→组合感知排序→独立风控审计→影子账本回放归因，单 agent 无法自造证据、自批风险、自动员资金（确定性代码守所有权边界）——评审问『模型说错怎么办』时，答案是把模型输出当证据输入而非权威的系统设计；自带双语操作台与决策账本，演示叙事完整；0.26.0 有 CI，Apache-2.0"
    reuse_cost: "中"
    open_source: "https://github.com/kyky2347/ALTA（Apache-2.0；需 PostgreSQL + Redis + LLM 密钥）"
sources:
  - url: https://github.com/kyky2347/ALTA
    title: "kyky2347/ALTA: Autonomous LLM Trading Asterism"
    accessed: "2026-09-09"
  - url: https://raw.githubusercontent.com/kyky2347/ALTA/main/README.md
    title: "README 全文（生命周期心智模型/席位分工/实现状态表）"
    accessed: "2026-09-09"
---

# ALTA：多 LLM Agent 自治研究型虚拟交易平台

## 是什么

kyky2347 开源的研究专用虚拟交易平台（248 star，Python，Apache-2.0，release 0.26.0 带 CI，API 实查 2026-09-09：推送至 2026-09-09 当天，活跃维护）。定位是回答"一队自治研究 agent 能否在不放弃证据、问责、恢复与组合纪律的前提下保持好奇心"：专门化 LLM agent 独立检索公开市场线索，把弱信号变成可证伪的机会（Opportunity），多空对辩、比较表达载体（个股/ETF/期权）、过独立风控审计，全部决策进可回放的 Shadow 影子账本。README 明确标注：实验性、research-only、非投资建议、无实盘模式，唯一券商边界是需操作员授权的 Tiger Paper 模拟执行。架构原则是"LLM 负责开放性研究与判断，确定性代码负责必须精确的部分（schema、lineage、权限、资金限额、幂等、租约、状态机、恢复、记账）"。席位分工：Scouts（检索并允许诚实弃权）、Foundry（归一化/去重/冻结 claim lineage）、Underwriters（独立多/空/催化/实施案例，产出结构化分歧而非共识表演）、Research Director（注意力分配与组合感知排序）、Expression desk（载体比较）、Risk & audit、Execution & monitoring、Learning loop（仅下行方向的校准与 Trader Mind 演化）。实现状态表（README 实抓 2026-09-09）：机会全生命周期、多车道自治检索（有界工具/来源健康/引用检查）、到期调度与断点恢复、组合集中度控制、时点前向结局评估与基准相对 Alpha、双语操作台、PostgreSQL 真相源 + Redis 支撑态的容灾。作者同时声明不宣称这些契约能产生 Alpha——系统的职责是让这个主张可被检验。

## 解决什么问题

LLM 交易/研究 agent 演示的通病： persuasive 输出被当成结论、无证据链、无事后问责、单 agent 既当运动员又当裁判。ALTA 把"一个想法"当作受管生命周期而非一次聊天回复，用确定性所有权边界 + 可回放账本让自治系统的每个决策可归因、可复盘、可失败恢复。

## 相比前方法优势

- 相比"一行 prompt 让 GPT 选股"类 demo：证据优先（citation 检查、来源健康、诚实弃权）、结构化多空对辩、独立风控否决权、Shadow 账本时点归因——把"模型说得像真的"与"证据"明确分开；
- 相比纯回测框架：评估走 point-in-time 前向结局 + 基准相对 Alpha + 预测校准，避免前视偏差；决策历史可搜索、可回放；
- 相比黑盒自治 agent 框架：故障恢复（周期恢复/孤儿清理/有界降级）与权限模型是一等公民，长程运行（365 天级）才是设计目标——多数 agent demo 只撑一场演示的时长。

## 局限（如实标注）

- 无任何盈利性主张：作者明确不证明 Alpha，Shadow 记录不等于真实市场成交（滑点/深度未建模为真实盘口）；
- 部署栈不轻：PostgreSQL 真相源 + Redis + LLM API 密钥 + （可选）Tiger 券商 paper 接入，黑客松现场从零跑通需预案；
- 信号面依赖公开数据源与工具配额，Scouts 检索质量受 API 限制约束（README 提及 bounded tool use）；
- 项目 2026-08-27 创建、迭代极快（当天仍有推送），接口稳定性与文档滞后续跟；
- 中文资料仅有 README 译文与双语控制台，深度文档（architecture/overview 等）以英文为主。

## 如何用于比赛

1. **金融科技/量化/Agent 黑客松（主用）**：以 ALTA 为骨架做"自治研究团队"作品——价值不在交易策略本身（作者自己不宣称 Alpha），而在可讲的设计故事：证据链、多空对辩、风控一票否决、影子账本回放，评审现场可抽任意历史决策看归因；双语控制台直接用于路演。reuse_cost 中：一天量级完成本地部署与演示剧本，赛前务必演练断网/断连恢复卖点（README 称断连保数据）。
2. **架构模式移植（低成本）**：其"LLM 提判断、确定性代码握权限与记账""Underwriters 结构化分歧而非共识""Learning loop 只做下行校准"三条设计律，可平移到任何多 agent 决策类作品（供应链、风控、运维）——这是本仓库对非金融赛题最通用的部分。
