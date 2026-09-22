---
id: gh-buddy_minesweeper
name: "Minesweeper：九模型同盘同时钟同工具层的 LLM Agent 扫雷竞速基准"
field: [LLM agents, agent 评测基准]
directions: [创新创业大赛]
published: "2026-09-21"
maturity: demo
signal:
  venue: GitHub
  stars: 17
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "agent/模型选型的第三方可复对照场：同一 seed 生成同一雷区同一开局格、至多 9 个模型同刻开跑、同一工具层，产出 revealed（安全格揭开率）/time/token cost 三维排名表与自动图表——作品评测章节的『与 GPT-x 同台』证据不用再自建考卷；纯 HTML+vanilla JS 零依赖零构建，node server.mjs 一条命令起服务，现场投屏九模型竞速（README 明说 built to be recorded，舞台只显示棋盘与数字）天然是路演环节素材"
    reuse_cost: 低
    open_source: "https://github.com/buddy/minesweeper（注意：无 license，二改前需确认授权）"
  - track: "双创-文书与申报"
    edge: "agent 产品宣称『推理/决策能力』时的可比证据来源：同盘同时钟对照出 revealed/time/cost 表，比自测截图与自述可信一个量级；出品方为 buddy.works（DevOps 平台公司组织账号，README 内嵌一键 Run in sandbox 直达其云沙箱），评测环境出处可查、可现场复跑"
    reuse_cost: 低
    open_source: "https://github.com/buddy/minesweeper"
sources:
  - url: https://github.com/buddy/minesweeper
    title: "buddy/minesweeper 仓库页（API 元数据：17 stars/1 fork/JavaScript/2026-09-21 创建/2026-09-21 最后推送/无 license）"
    accessed: "2026-09-22"
  - url: https://raw.githubusercontent.com/buddy/minesweeper/main/README.md
    title: "README 全文（九模型并行规则、revealed/time/cost 指标、turn vs move 口径、运行方法）"
    accessed: "2026-09-22"
---

# Minesweeper：九模型同盘竞速的 LLM Agent 微基准

> 来源：https://github.com/buddy/minesweeper （API 实查 2026-09-22：2026-09-21 创建，17 stars/1 fork，JavaScript，无 license；README 实抓 2026-09-22。本卡内容出自本次抓取的仓库元数据与 README 全文。）

## 是什么

buddy.works（DevOps 平台公司）组织账号 2026-09-21 开源的 LLM agent 扫雷竞速基准（17 star，纯 HTML + 本地 CSS + vanilla JavaScript，无依赖无构建；README 内嵌 Run in sandbox 按钮可一键在其云沙箱启动）。设定（README 实抓）：一个种子生成所有赛道——至多 9 个模型拿到**同一雷区、同一开局格**，同一时刻在同一时钟下开跑，共用同一工具层，"what separates them is the reasoning rather than the setup"。评分三维：**Revealed**（安全格揭开率，100% 即全胜）、**Time**、**Cost**（token 成本）。口径上区分 turn（一次把棋盘交给模型）与 move（一次真正改变棋盘的调用）——"读三次边界再行动不算三次 move"，防刷操作数。运行结束自动弹出揭示速度曲线与排名表。运行方式：Node 22+，`cp .env.example .env` 填各 provider key（ANTHROPIC/OPENAI/XAI/TYPESAFE 四个槽位），`node server.mjs` 监听 127.0.0.1:8787，key 全部留服务端由其代理模型请求；缺 key 的赛道明确报错、其余赛道继续。仓库含 server.mjs（10.4KB）、js/、tests/ 目录。

## 解决什么问题

模型 agent 能力对比的"口径不对齐"病：各家 demo 各自任务、各自脚手架、各自评分，"谁更强"取决于考卷而不是推理。本基准把考卷（同一雷区种子）、节奏（同一时钟）、工具层全部锁死，让模型间差异只剩推理本身；并用 token cost 作为一等指标——同盘同分之下"花了多少"也是差距。

## 相比前方法优势

- 相比多任务 agent 基准（WebArena 类）：单局短平快、零依赖零构建，赛期内随时可跑，结果天然可视化，适合路演与评测章节直接引用；
- 相比 LLM 竞技场式自由对话评分：扫雷是可验证的确定性任务，雷区同种子可复现，分数不含评委主观性；且"读边界不算 move"的口径设计防住了用多余工具调用刷存在感的行为；
- 相比自建对比脚本：turn/move 区分、缺 key 降级续跑、自动出图与排名表都是现成的，"built to be recorded" 的舞台化界面省掉演示工程。

## 局限（如实标注）

- **无 license**（2026-09-22 API 实查 license: null）：代码默认版权保留，fork 进作品或二改前需向作者确认授权；
- 极年轻仓库：创建仅一天（2026-09-21），17 stars/1 fork，未经社区检验，持续性存疑；
- 单一游戏探针：扫雷测的是不确定性下的概率推断 + 工具调用纪律，不等于通用 agent 能力，高分≠全面强；
- provider 槽位窄：README .env 仅 Anthropic/OpenAI/xAI/TypeSafe 四家，接国产模型需改代码；token cost 对比依赖各家定价口径，横比需换算；
- 榜单型价值的时效风险：模型版本迭代快，单日快照的排名很快过期（好在重跑成本低）。

## 如何用于比赛

1. **黑客松（数据与算法）**：两类用法——(a) 选型证据链：赛前把候选模型/自家 agent 在同一棋盘跑一遍，revealed/time/cost 表放进作品评测章节，作为"与商用模型同台"的第三方可复数字；(b) 现场环节：九模型同屏竞速直接投屏，配合其自动排名表做互动展示。reuse_cost 低：Node 22 起服务一条命令，但需自备 API key 且注意无 license 的二改限制。
2. **双创（文书与申报）**：申报书/路演中声称 agent 推理能力时，用它给出同盘对照数据代替自测截图；出品方为可查的公司组织账号，环境出处经得起追问。
