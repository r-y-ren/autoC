---
id: kaggle-pokemon-tcg-ai-battle-challenge-strategy
name: "PTCG AI Battle Challenge — Strategy Category（The Pokémon Company × Kaggle）"
tier: 编程/黑客松
directions:
  - 黑客松与数据竞赛
status: active
organizer: "Sponsor：The Pokémon Company（Roppongi Hills Mori Tower, Tokyo）；Host：Google LLC（Kaggle）。合作方 HEROZ 与松尾研究所、支持方 Google/Google Cloud/NVIDIA/Kaggle ——此层为二手源（PokeBeach/Misprint）口径"
award_levels:
  - name: "Finalist（Top 8）"
    count_or_ratio: "8 名 × $30,000（官方 rules §7 原文 'Eight (8) Finalists will receive $30,000 each'，TOTAL PRIZES AVAILABLE: $240,000）"
  - name: "东京线下总决赛邀请（Final Stage）"
    count_or_ratio: "8 强受邀（rules 原文 'Finalists may also be invited to an in-person tournament, hosted by The Pokémon Company in Tokyo, Japan, held TBD'——决赛奖金未载于本赛 rules；二手源称决赛另设 1st +$50,000 / 2nd +$30,000，待核）"
key_dates:
  start:
    date: "2026-06-16"
    verified: true
    note: "双源：官方 Timeline 页（API 直抓 'June 16, 2026 11:00 am UTC - Start Date'）+ PokeBeach/Misprint 二手一致"
  simulation_entry_deadline:
    date: "2026-08-09"
    verified: false
    note: "参赛前置赛道 Simulation 的报名截止。多源二手（Reddit r/pkmntcg / Dexerto / 搜索快照 'Entry Deadline August 9, 2026'）；官方 API Timeline 该行为模板变量未解析，待预抓核对"
  simulation_final_submission:
    date: "2026-08-17"
    verified: true
    note: "前置赛道官方 Timeline 直抓 'August 17, 2026 - Final Submission Deadline'（其后至约 08-31 继续跑对局至榜单收敛）。⚠ 本赛 Strategy 参赛以 Simulation 报名为前提，该日期已过 → 新队伍事实无法入局"
  entry_deadline:
    date: "2026-09-06"
    verified: false
    note: "Kaggle 官方 LinkedIn 宣帖快照 'Entry Deadline: September 6, 2026 - Prize Pool: $240,000' + 任务包线索 + Kaggle 页搜索快照三线一致；官方 API Timeline 该行为模板变量未解析，待预抓核对"
  final_submission_deadline:
    date: "2026-09-13"
    verified: false
    note: "Kaggle 页搜索快照 'September 13, 2026 - Final Submission Deadline' + Reddit 二手 'write-up submissions open until September 13'；官方 API 未解析；与官方 Judging 起点 09-14 严丝合缝。Misprint 二手约数口径为 09-14"
  judging_period:
    date: "2026-09-14 ~ 2026-10-11"
    verified: true
    note: "官方 Timeline 页直抓 'September 14, 2026 - October 11, 2026 - Judging Period*'（*注：视提交量可能调整）"
  results_announced:
    date: "TBD"
    verified: false
    note: "官方 Timeline 页直抓 'TBD - Anticipated Results Announcement'"
deliverables:
  - "Kaggle Writeup（项目报告：title + subtitle + 对提交的详细分析；必须选择 Track；≤2000 词，超限 'may be subject to penalty'；官方原文 'Any un-submitted or draft Writeups by the competition deadline will not be considered'）"
  - "Media Gallery（可选：图片/视频素材；违反 Pokémon Elements 许可的图片直接不评审并可取消资格）"
  - "参赛前提：同队完成姊妹赛 Simulation Category（pokemon-tcg-ai-battle）报名与提交，两赛道队伍组成必须完全一致（rules §1c）"
  - "获奖义务：开源（Winner License Type: MIT，OSI 批准且不限商用）+ 交付最终模型代码（训练/推理/环境说明）与可复现文档"
ai_policy:
  summary: >-
    官方 rules（2026-08-28 经 Kaggle 官方 ListPages API 直抓全文）实得：①允许 AMLT/LLM——"Individual
    Participants and Teams may use automated machine learning tool(s) ('AMLT') ... to create a
    Submission, provided ... they have an appropriate license"；外部数据与模型允许，但受 "Reasonableness
    Standard" 约束（例：订阅 Gemini Advanced 级别费用可接受，"Purchasing a license to use a proprietary
    dataset that exceeds the cost of a prize in the competition would not be considered reasonable"）。②获奖作品强制开源（MIT，OSI 批准、不限商用），须交付训练代码+推理代码+环境说明。③数据 "Competition Use
    Only"：赛后须删除 Competition Data；Pokémon Elements（卡牌/角色/规则等）一切 IP 归 The Pokémon
    Company，参赛者不获转让且不得行使人格权。④单账号、队内最多 5 人、每队仅 1 次提交（Hackathon 类）。本赛本质是"为 AI agent 写策略分析报告"：评审三权重 Model Score 70% / Deck Score 20% /
    Report Score 10%（Evaluation 页直抓）——对 AI 辅助写作无禁令，但报告有 2000 词硬限与图片许可红线。
  url: https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/rules
  checked: "2026-08-28"
credibility: 官网
last_verified: "2026-08-28"
sources:
  - url: https://www.kaggle.com/api/i/competitions.PageService/ListPages?competitionId=131772
    title: "Kaggle 官方 ListPages API（本赛 competitionId=131772）：rules 全文（$240,000/8×$30K/MIT/队限5人/单提交）、Description、Evaluation（70/20/10）、Submission Requirements（Writeup≤2000词）、Timeline（开赛 06-16、Judging 09-14~10-11）、Data Description —— 2026-08-28 直抓，快照存 kb/raw/"
    accessed: "2026-08-28"
  - url: https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy
    title: "赛站 SSR 壳（标题/description 'Analyze data and agentic play supporting the Pokémon Trading Card Game'/赛 ID 131772）——SPA 正文经官方 API 取得"
    accessed: "2026-08-28"
  - url: https://www.kaggle.com/api/i/competitions.PageService/ListPages?competitionId=116727
    title: "姊妹赛 Simulation（competitionId=116727）官方 Timeline：Final Submission 2026-08-17、榜单收敛至约 08-31 —— 参赛前置窗口判断依据"
    accessed: "2026-08-28"
  - url: https://www.pokebeach.com/2026/06/the-pokemon-company-launches-ai-competition-to-build-the-strongest-pokemon-tcg-player-featuring-300000-in-prizes
    title: "PokeBeach 报道（二手·聚合站，2026-06-16 发布）：总盘 $300K+、Final Stage 2026-09 日本 +1st $50K/2nd $30K、合作方 HEROZ/松尾研究所——降级引用"
    accessed: "2026-08-28"
  - url: https://www.misprint.com/posts/pokemon-ai-tcg-competition-explained
    title: "Misprint 拆解（二手·聚合站，2026-06-20 发布）：$240K=Strategy 8×$30K 口径解释、Strategy 赛程至 09-14 约数、评审三要素（approach 稳定性/deck 设计/simulation 表现）——降级引用"
    accessed: "2026-08-28"
---

# PTCG AI Battle Challenge — Strategy Category（kaggle-pokemon-tcg-ai-battle-challenge-strategy）— meta

## 概况（除标注外均为 2026-08-28 官方直抓）

- The Pokémon Company 出资（Sponsor）、Google/Kaggle 承办的"PTCG AI Battle Challenge"双赛道之一。Simulation 赛道（pokemon-tcg-ai-battle）比 AI agent 对战胜负；**本 Strategy 赛道比"策略逻辑的报告"**——官方 Description 原文："While the Simulation Category competition evaluates an AI Training Agent's win rate and performance, the Strategy Category competition evaluates the participant's strategic logic behind its AI Training Agent."
- 奖金：**$240,000 = 8 名 Finalist × $30,000**（rules §7 直抓），另受邀东京线下总决赛（时间 rules 载 TBD）；二手源称决赛另设 +$50K/+$30K（PokeBeach/Misprint，降级待核）。全挑战总盘 "$300K+/$290K+" 口径为媒体报道，未见官方页。
- 评审三权重（Evaluation 页直抓）：**Model Score 70%**（方法阐述清晰度/原创性与技术稳健性/重复对局稳定性/不依赖特定初始状态与对位/赛道内表现）、**Deck Score 20%**（卡组概念与策略契合/关键卡选用）、**Report Score 10%**（结构逻辑/图表运用）。
- 官方明示"高排名不保证 Strategy 好成绩；中低排名者可凭 deep analysis, originality, and well-structured reporting 拿高分"（Description 页直抓）——报告型赛道特征显著。
- 数据集：卡牌元数据（EN/JP 双语 Card_ID_List PDF + Card Data CSV，含 HP/属性/招式/效果等字段）。
- 单队 1 次提交；队上限 5 人；两赛道队伍组成必须一致；获奖须 MIT 开源并交付全量可复现代码。

## 入局窗口判断（2026-08-28，对本框架的关键结论）

- Strategy 自身 entry deadline 2026-09-06（未直抓证实）尚未到，**但参赛前提是已参加 Simulation 赛道**（rules §1c + Description 页明示），而 Simulation Final Submission **2026-08-17 已过**（官方直抓）、其 entry deadline 二手口径 2026-08-09 亦已过 → **新队伍已无法完整入局，本条目对本框架定位为"风向标样本"而非可参赛目标**。
- 可参赛价值留待下一届（如续办）；agentic RL + 卡牌不完全信息博弈 + "策略报告型赛道"的评审范式（70/20/10）是本条目的主要情报价值。

## 线索纠错（对任务包线索，2026-08-28 核）

- "$240K 分析赛道"：**成立**，官方 rules §7 直抓确认 $240,000（8×$30K）。
- "报名截止 2026-09-06"：与 Kaggle LinkedIn 官帖快照及页面搜索快照一致，但官方 API 该字段未解析，记 verified: false 待预抓。
- 全挑战 "$300K" 口径：媒体总盘口径（含决赛加码），非本赛页官方数字；决赛 +$50K/+$30K 未见于本赛官方 rules。

## AI 政策原文（rules 全文直抓，2026-08-28）

- "Individual Participants and Teams may use automated machine learning tool(s) ('AMLT') (e.g., Google AutoML, H2O Driverless AI, etc.) to create a Submission, provided that the Participant or Team ensures that they have an appropriate license to the AMLT such that they are able to comply with the Competition Rules."（§2 RE)
- "By way of example only, a small subscription charge to use additional elements of a large language model such as Gemini Advanced are acceptable if meeting the Reasonableness Standard of Sec. 8.2."（外部数据/LLM 费用"合理性标准"）
- "You hereby license and will license your winning Submission and the source code used to generate the Submission under an Open Source Initiative-approved license ... that in no event limits commercial use"（Winner License Type: MIT）
- "Upon the conclusion of the Competition, you shall promptly delete the Competition Data."（数据 Competition Use Only）
- Pokémon Elements IP 全归 Pokémon；"Submissions containing images that violate the license granted for Pokémon Elements will not be evaluated and are subject to disqualification."（Submission Requirements 页）

## 获奖情况

- 当届未放榜：官方 Judging Period 2026-09-14 ~ 10-11，结果公布日 TBD（Timeline 页直抓）。winners/2026.md 已建并声明数据缺口。

## 信源与快照

- `kb/raw/kaggle-pokemon-tcg-ai-battle-challenge-strategy/2026-kaggle-pages-api.json`（本赛全页官方 JSON，含 rules 全文）
- `kb/raw/kaggle-pokemon-tcg-ai-battle-challenge-strategy/2026-kaggle-page-*.md`（rules/description/timeline/evaluation/submission-requirements/data-description 等逐页导出）
- `kb/raw/kaggle-pokemon-tcg-ai-battle-challenge-strategy/2026-kaggle-simulation-pages-api.json`（姊妹赛官方 JSON）
- `kb/raw/kaggle-pokemon-tcg-ai-battle-challenge-strategy/2026-kaggle-overview.html`、`2026-kaggle-simulation-shell.html`（SSR 壳）
- `kb/raw/kaggle-pokemon-tcg-ai-battle-challenge-strategy/2026-pokebeach-announcement.md`、`2026-misprint-explainer.md`（二手·聚合站，降级标注）
- 抓取通道备注：Kaggle 页面为 SPA，本次经 Kaggle 官方 ListPages API（competitions.PageService）匿名直抓取得页面正文原件，等效直抓官网。

## 待核验清单

- [ ] entry_deadline 2026-09-06 / final_submission 2026-09-13：官方 Timeline API 文本为模板变量（`${competition.Deadline}` 等）未解析——建议主会话 Browser Use 预抓赛站 Overview 页核对后置 verified: true。
- [ ] Final Stage 东京总决赛：时间（rules 载 TBD）与奖金（二手称 1st +$50K / 2nd +$30K）待官方页更新。
- [ ] 二手源提到的示例 Writeup（如社区 "Alakazam Strategy Writeup" notebook）可作为下轮 winners 预研线索（搜索快照级，未直抓）。
- [ ] 全挑战总盘 "$300K+/$290K+" 的官方口径（若 The Pokémon Company 官网/官推发布）。
