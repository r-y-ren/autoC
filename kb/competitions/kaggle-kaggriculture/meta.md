---
id: kaggle-kaggriculture
name: "Kaggriculture（Google/Kaggle 农场经营 agent 仿真对抗赛）"
tier: 编程/黑客松
directions:
  - 黑客松与数据竞赛
status: active
organizer: "Sponsor：Google LLC（1600 Amphitheatre Parkway, Mountain View, CA）；Kaggle 平台承办（Simulation Competition，无 Private Leaderboard）"
award_levels:
  - name: "1st Place"
    count_or_ratio: "$5,000（官方 Prizes 页/rules §5：1st–10th 名各 $5,000）"
  - name: "2nd Place"
    count_or_ratio: "$5,000"
  - name: "3rd–10th Place"
    count_or_ratio: "8 名 × 各 $5,000；TOTAL PRIZES AVAILABLE: $50,000（rules §5 直抓）。⚠ $60,000 口径另见任务包线索与 Kaggle 列表页搜索快照，未获官方页证实，双口径并存待核"
key_dates:
  start:
    date: "2026-07-29"
    verified: true
    note: "官方 Timeline 页直抓 'July 29, 2026 - Start Date'"
  entry_deadline:
    date: "unknown"
    verified: false
    note: "官方 API Timeline 该行为模板变量（${competition.ProhibitNewEntrantsExplicitDeadline}）未解析；赛站 Overview 页为 SPA。待主会话预抓核对。当前（2026-08-28）赛事 active，报名应仍开放，但截止日无官方数值"
  final_submission_deadline:
    date: "2026-09-30"
    verified: true
    note: "官方 Timeline 页直抓 'September 30, 2026 - Final Submission Deadline'（11:59 PM UTC）"
  ladder_convergence:
    date: "2026-10-01 ~ 约 2026-10-15"
    verified: true
    note: "官方 Timeline 页直抓：截止后继续跑对局至榜单收敛，随后榜单定稿并跑最终 Bradley-Terry 锦标赛（Evaluation 页）"
deliverables:
  - "自主 AI agent（bot）：Kaggle 官方 Python kit 编写，部署于 /kaggle_simulations/agent/ 路径，与天梯同类评级 bot 对战"
  - "每日至多 5 次提交；仅最近 2 次提交被跟踪并用于最终评估；提交先过 Validation Episode（自博弈跑通校验），失败标记 Error"
  - "可选 2 个最终提交供评审（rules §2b）；团队上限 5 人"
ai_policy:
  summary: >-
    官方 rules（2026-08-28 经 Kaggle 官方 ListPages API 直抓全文）：①外部数据与模型允许——"The use of
    external data and models is acceptable unless specifically prohibited by the Host"，LLM/工具受
    "Reasonableness Standard" 约束（例：Gemini Advanced 级订阅费用可接受、超过奖金成本的专有数据集不合理）；②AMLT（AutoML 等）允许，须持适当许可；③获奖许可 CC-BY
    4.0（Winner License Type），竞赛数据 Apache 2.0——"You may access and use the Competition Data for any
    purpose, whether commercial or non-commercial"（在 Kaggle 仿真赛中最宽松的一档）；④资格：18+ 全球（制裁地区除外）；单账号，多账号报名/提交被禁。未见任何"禁用 LLM/生成式 AI"条款；本赛目标是 agentic
    AI（官方 abstract："design, build, and deploy an autonomous AI agent"）。
  url: https://www.kaggle.com/competitions/kaggriculture/rules
  checked: "2026-08-28"
credibility: 官网
last_verified: "2026-08-28"
sources:
  - url: https://www.kaggle.com/api/i/competitions.PageService/ListPages?competitionId=147734
    title: "Kaggle 官方 ListPages API（competitionId=147734）：rules 全文（$50,000/CC-BY 4.0/Apache 2.0）、Prizes（10×$5,000）、Timeline（开赛 07-29、终交 09-30、收敛至约 10-15）、Evaluation（天梯+Bradley-Terry）、How to Play/Foundational Rules（游戏机制全文）—— 2026-08-28 直抓"
    accessed: "2026-08-28"
  - url: https://www.kaggle.com/competitions/kaggriculture
    title: "赛站 SSR 壳（标题 'Kaggriculture'、description 'Create an agent to play in this farming simulation...'、赛 ID 147734）——SPA 正文经官方 API 取得"
    accessed: "2026-08-28"
---

# Kaggriculture（kaggle-kaggriculture）— meta

## 概况（除标注外均为 2026-08-28 官方直抓）

- Google 自办自承办的 **Simulation Competition**：回合制农场经营博弈——两名玩家在各自农场中经营 30 个游戏日（每日 24 回合、共 720 回合），**赛季结束银行存款多者胜**（How to Play 页：'the winner is determined by who has the most money in the bank at the end'）。
- 玩法要素（Description/How to Play 直抓）：种植/浇水/施肥/收获 6 类作物；饲养鹅/牛/羊产蛋奶毛；买地扩张；动态市场（价格随你的出货与小镇需求反应）；雇佣 farm hand 扩大操作规模。官方定位："models the exact same dynamics found in real-world supply chains, dynamic market pricing, and industrial resource allocation under uncertainty"——**agentic RL 风向标赛事**（任务包判断与官方口径一致）。
- 排名机制（Evaluation 页直抓）：Elo 式天梯（胜=加分，净胜金币数不影响评分，只看胜负平）；提交后持续对局；终交后约两周继续跑局降方差，最终跑 **Bradley-Terry 锦标赛**定榜；Simulation 赛无 Private Leaderboard（rules 直抓 'There is no Private Leaderboard in Simulation competitions'）。
- 赛程：2026-07-29 开赛 → 09-30 终交 → 10-01~约 10-15 收敛定榜。**当前处于可提交期（entry deadline 官方数值缺失，见待核）**。
- 关键机制红线（How to Play 直抓，供赛点检查表）：作物两天不浇水变杂草；动物两天不喂（小麦）会逃跑不可找回；番茄/草莓为有限次产出（4 次）后衰败成杂草；西瓜加肥 8 天达产上限。

## 奖金口径（任务包双口径核验结论）

- **$50,000**：官方 rules §5 "TOTAL PRIZES AVAILABLE: $50,000" + Prizes 页（1st–10th 各 $5,000）**双处直抓证实**——当前采信口径。
- **$60,000**：任务包线索；另搜索快照显示 Kaggle 竞赛**列表页**对同描述赛事标 "$60,000"（列表页为 SPA，ListCompetitions API 匿名不可访问，未直抓证实）。可能为奖池上调后的列表页新口径或列表页数据不一致。**双口径并存，标待核**——建议主会话 Browser Use 预抓 https://www.kaggle.com/competitions 列表页与赛站 Overview 头部奖池徽标核对。
- 二手线索（搜索快照级，未直抓）：Reddit r/reinforcementlearning 称首周 2k+ 队伍参赛、有 Kaggle 员工参与规则制作——仅作热度参考。

## AI 政策原文（rules 直抓，2026-08-28）

- "The use of external data and models is acceptable unless specifically prohibited by the Host."（外部数据/模型默认允许）
- "a small subscription charge to use additional elements of a large language model such as Gemini Advanced are acceptable if meeting the Reasonableness Standard"（LLM 使用按费用合理性标准放行）
- "Individual Participants and Teams may use automated machine learning tool(s) ('AMLT') ... provided that ... they have an appropriate license"（AMLT 放行）
- Winner License Type: CC-BY 4.0；Data Access and Use: Apache 2.0（商用亦允许）
- "You cannot sign up to Kaggle from multiple accounts and therefore you cannot enter or submit from multiple accounts."

## 获奖情况

- 当届未放榜：终交 2026-09-30，榜单收敛至约 10-15，无任何名单。winners/2026.md 已建并声明数据缺口。官方页面未见历届记录，按首届处理（待核）。

## 信源与快照

- `kb/raw/kaggle-kaggriculture/2026-kaggle-pages-api.json`（全页官方 JSON：rules/foundational-rules/how-to-play/prizes/evaluation/timeline/description/FAQ 等 12 页）
- `kb/raw/kaggle-kaggriculture/2026-kaggle-page-*.md`（逐页导出 12 件）
- `kb/raw/kaggle-kaggriculture/2026-kaggle-overview-shell.html`（SSR 壳）
- 抓取通道备注：Kaggle SPA，正文经 Kaggle 官方 ListPages API（competitions.PageService）匿名直抓，等效直抓官网。

## 待核验清单

- [ ] 奖池 $50K vs $60K：主会话预抓 Kaggle 列表页 + 赛站 Overview 奖池徽标定分。
- [ ] entry_deadline 官方数值（API 模板变量未解析）。
- [ ] "首届"判断（未见历届，但未做穷尽检索旧届记录）。
- [ ] Reddit "首周 2k+ 队伍"热度口径（二手，未直抓）。
- [ ] agent 运行环境资源限额（FAQ 页 HDD/RAM/vCPU 字段均为模板变量未解析；Docker 基镜像 github.com/Kaggle/kaggle-environments 已知）。
