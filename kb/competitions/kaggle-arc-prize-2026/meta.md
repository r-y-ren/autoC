---
id: kaggle-arc-prize-2026
name: "ARC Prize 2026（ARC-AGI-2 / ARC-AGI-3 / Paper Track 三赛道）"
tier: 编程/黑客松
directions:
  - 黑客松与数据竞赛
status: active
organizer: "ARC Prize, Inc.（非营利主办方，官网口径 'ARC Prize is a nonprofit'；赛道经 Kaggle 承办）"
award_levels:
  - name: "ARC-AGI-3 Grand Prize"
    count_or_ratio: "解锁制 $700,000：授予首个在 ARC-AGI-3 评测得 100% 的合格 agent；未颁出滚存下届年度赛"
  - name: "ARC-AGI-2 Bonus Prize"
    count_or_ratio: "$150,000：首个私榜 ≥85% 的合格方案；未颁出滚存 2027"
  - name: "ARC-AGI-2 Grand Prize"
    count_or_ratio: "$275,000：按 Solution Writeup 六项等权标准（各 0–5 分取均值）评审"
  - name: "Paper Top Paper"
    count_or_ratio: "$75,000（1st $50K / 2nd $20K / 3rd $5K，保底，横跨 AGI-2 与 AGI-3 两赛道评）"
  - name: "ARC-AGI-3 Top Score Award"
    count_or_ratio: "$75,000（1st $40K / 2nd $15K / 3rd $10K / 4th $5K / 5th $5K，保底）"
  - name: "ARC-AGI-3 Milestone Prizes"
    count_or_ratio: "$75,000（M1 与 M2 各：1st $25K / 2nd $10K / 3rd $2.5K；须在节点截止前开源方有资格）"
  - name: "ARC-AGI-2 Progress Prizes"
    count_or_ratio: "$275,000，8 档：$75K/$50K/$40K/$35K/$25K/$20K/$15K/$15K"
  - name: "Paper Outstanding Papers Pool"
    count_or_ratio: "$375,000：rubric >4.5 分者由主办方裁量分润，多名可同时获奖"
key_dates:
  competition_start:
    date: "2026-03-25"
    verified: false
    note: "单源：arcprize.org 总览 'March 25, 2026 — Competition starts'；Kaggle 页为 SPA 未能直抓核对"
  agi3_milestone_1:
    date: "2026-06-30"
    verified: true
    note: "双源：arcprize.org 总览 + AGI-3 赛道页（'Milestone #1 — June 30, 2026'）"
  agi3_milestone_2:
    date: "2026-09-30"
    verified: true
    note: "双源：arcprize.org 总览 + AGI-3 赛道页（'Milestone #2 — September 30, 2026'）"
  final_submission_deadline:
    date: "2026-11-02"
    verified: true
    note: "双源：arcprize.org 总览 'November 2, 2026 — Submissions due' + Kaggle ARC-AGI-3 页搜索快照 'November 2, 2026 - Final Submission Deadline'"
  paper_deadline:
    date: "2026-11-08"
    verified: false
    note: "单源：arcprize.org 总览 'November 8, 2026 — Papers due'；Kaggle Paper Track 页未直抓；LinkedIn 二手 '10-26' 不采信；任务包线索 11-08/09 中 11-09 未获证实"
  results_announced:
    date: "2026-12-04"
    verified: true
    note: "双源：arcprize.org 总览 'December 4, 2026 — Results announced' + Kaggle ARC-AGI-3 页快照 'December 4, 2026 - Winners'"
deliverables:
  - "Kaggle code competition notebook（两阶段：Save & Run All 验证可运行 + Competition Rerun 跑隐藏集；评测期无互联网）"
  - "开源解决方案：自有代码/方法须以 CC0、MIT-0 等公有领域/宽松许可开源；第三方代码须允许公开共享（Apache-2.0、GPLv3 等）；获官方私榜分数前必须完成开源"
  - "ARC-AGI-2 Grand Prize 参评：提交截止后 7 日内附官方 Solution Writeup 并开源全部 artifacts"
  - "Paper Track：Writeup（必含 Abstract/Intro/Prior work/Approach/Results/Conclusion），必须关联同届 ARC-AGI-2 或 ARC-AGI-3 的 Kaggle code 提交（分数不限高低）"
ai_policy:
  summary: >-
    官方页面实得三组硬条款：①评测环境禁 API 型 LLM——总览页原文 "Internet access is not
    available during Kaggle evaluation (no API-based systems like GPT/Claude/etc.)"，AGI-2 与
    AGI-3 赛道页均有 "No internet access during evaluation"，即 GPT/Claude 等 API 系统在评测期不可用（方案本身可以基于本地预训练模型/agent）；②强制开源——"Participants
    must open source their solutions before receiving official private evaluation
    scores"，自有代码 CC0/MIT-0、第三方须 Apache-2.0/GPLv3 等，未开源者被移除奖金资格；③验证榜 Testing
    Policy——单次评测成本上限 "$10,000 USD"、不跨次平均、明确不开 web search、不默认挂工具（"tool
    use should be opt-in, not opt-out"，任何工具使用必须声明）。任务包所称"AI 生成代码/方案专门条款"未见于本次实抓的任一官方页面（总览/三赛道/policy/terms/docs），Kaggle
    Rules 页为 SPA 渲染未能直抓，如实列为待核验，不作猜测补全。
  url: https://arcprize.org/competitions/2026
  checked: "2026-08-27"
credibility: 官网
last_verified: "2026-08-27"
sources:
  - url: https://arcprize.org/competitions/2026
    title: "ARC Prize 2026 总览（$2M 总池、三赛道、时间线、无互联网/API 条款、开源要求）"
    accessed: "2026-08-27"
  - url: https://arcprize.org/competitions/2026/arc-agi-2
    title: "ARC-AGI-2 赛道页（$700K 拆分、85% 目标、Bonus/Grand/Progress 评法、2 outputs 规则）"
    accessed: "2026-08-27"
  - url: https://arcprize.org/competitions/2026/arc-agi-3
    title: "ARC-AGI-3 赛道页（$850K 拆分、Grand 解锁条件、M1/M2 金额、Kaggle 提交通道）"
    accessed: "2026-08-27"
  - url: https://arcprize.org/competitions/2026/paper
    title: "Paper Prize 赛道页（$450K 拆分、六项 rubric、须关联 Kaggle 提交）"
    accessed: "2026-08-27"
  - url: https://arcprize.org/policy
    title: "ARC Prize Verified Testing Policy（$10K/次评测上限、无 web search、工具 opt-in、开源方可验证）"
    accessed: "2026-08-27"
  - url: https://arcprize.org/terms
    title: "站点通用条款（无竞赛 AI 条款，仅原创性担保；已核）"
    accessed: "2026-08-27"
  - url: https://docs.arcprize.org/arc-prize-2026
    title: "ARC Prize 2026 Starter Kit 文档（code competition 两阶段提交流程、RTX 6000 限 AGI-3、加速会话禁网）"
    accessed: "2026-08-27"
  - url: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2
    title: "Kaggle ARC-AGI-2 赛站（SPA；标题与描述经直抓，日程经搜索索引快照交叉）"
    accessed: "2026-08-27"
  - url: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3
    title: "Kaggle ARC-AGI-3 赛站（SPA；'November 2, 2026 - Final Submission Deadline / December 4, 2026 - Winners' 经搜索索引快照取得）"
    accessed: "2026-08-27"
  - url: https://www.kaggle.com/competitions/arc-prize-2026-paper-track
    title: "Kaggle Paper Track 赛站（SPA；'Writeup documenting the submission... for either' track 经搜索索引快照取得）"
    accessed: "2026-08-27"

---
# ARC Prize 2026（kaggle-arc-prize-2026）— meta

## 概况（全部为 2026-08-27 实抓）

- ARC Prize, Inc. 主办的年度 AGI 奖金赛（非营利），2026 届总池 **$2,000,000、三赛道**：ARC-AGI-3（交互式推理，AI agent）、ARC-AGI-2（静态推理）、Paper Prize（论文）。三赛道奖池 $850K + $700K + $450K = $2M，与总览口径自洽。
- 赛程：2026-03-25 开赛 → 06-30 AGI-3 M1 → 09-30 AGI-3 M2 → 11-02 提交截止 → 11-08 论文截止 → 12-04 公布结果。当前（2026-08-27）处于赛中，M2 将近。
- AGI-2 目标："Reach 85% accuracy on the ARC-AGI-2 private evaluation dataset within the Kaggle efficiency limits"；评测无互联网、仅 notebook 提交；每任务对每个 test 输入预测恰 2 个输出，任一精确匹配即该任务得 1 分。
- AGI-3 Grand Prize 解锁条件："Awarded to the first eligible agent that scores 100% on the ARC-AGI-3 evaluation"。
- Starter Kit（docs.arcprize.org）：提交为 code competition notebook，Kaggle 跑两阶段；加速器选项 cpu/t4/p100/rtx6000，"RTX 6000 is reserved for ARC-AGI-3 notebooks"；"All accelerated Kaggle sessions have internet disabled"。
- 硬件/算力限额：赛道页原文 "Hardware and compute limits will be announced with the competition launch"（AGI-2/AGI-3 页面如此表述，页面未给具体数值）。

## 线索纠错（对任务包线索，2026-08-27 复核）

- "AGI-2 在赛至约 2026-11-09"：**不成立**。总览页与 Kaggle ARC-AGI-3 快照双源均为 **2026-11-02** Final Submission Deadline。
- "AGI-3 总池 $850K + 解锁 $700K"：口径修正为 **$850K 总池（内含 $700K 解锁制 Grand Prize）**，非两笔叠加。
- "Paper Track 论文截止 2026-11-08/09、$75K"：$75K 实为 Top Paper（保底）一档，Paper 赛道总池 **$450K**（另含 $375K Outstanding Papers Pool）；截止日实抓仅得 11-08（单源），11-09 未证实。
- "Milestone 2 截止 2026-09-30"：双源确认。

## AI 政策原文（arcprize.org，2026-08-27 抓取）

- "Internet access is not available during Kaggle evaluation (no API-based systems like GPT/Claude/etc.)"（总览）
- "No internet access during evaluation"（AGI-2 / AGI-3 赛道页）
- "All code and methods must be open sourced to be eligible for prizes." / "Participants must open source their solutions before receiving official private evaluation scores."（总览与赛道页）
- Testing Policy："We cap our evaluations at $10,000 USD per run." / "we do not average scores across runs" / "We specifically do not enable web search, because that could leak Semi-Private data to the web." / "tool use should be opt-in, not opt-out, so any tool use will always be declared"
- 注：Kaggle 各赛站 Rules 全文为 SPA 渲染，直抓与 r.jina.ai 代理均未取得；"AI 生成代码专门条款"未在已抓官方页面出现，不臆测。

## 获奖情况

- 进行中（结果 2026-12-04 公布），winners 深构分片待 12 月后启动。

## 信源与快照

- `kb/raw/kaggle-arc-prize-2026/2026-arcprize-overview.html`
- `kb/raw/kaggle-arc-prize-2026/2026-arcprize-arc-agi-2.html`
- `kb/raw/kaggle-arc-prize-2026/2026-arcprize-arc-agi-3.html`
- `kb/raw/kaggle-arc-prize-2026/2026-arcprize-paper.html`
- `kb/raw/kaggle-arc-prize-2026/2026-arcprize-testing-policy.html`
- Kaggle 三赛站为 SPA，无有效静态快照可存；其日程/描述事实经搜索索引快照交叉后引用。

## 待核验清单

- [ ] Kaggle Rules 全文（三赛站 /rules）：任务包所称"AI 生成代码/方案专门条款"是否存在及原文；建议下轮用可渲染抓取（Browser Use 主会话或 OCR 流程）补。
- [ ] competition_start 2026-03-25 的第二官方源（Kaggle 页直抓）。
- [ ] paper_deadline 11-08 的第二官方源（Kaggle Paper Track 页直抓）。
- [ ] "Hardware and compute limits will be announced with the competition launch" 落地后的具体算力限额数值。
- [ ] 总览页是否载明团队人数上限——已抓页面均未见，暂缺省。
