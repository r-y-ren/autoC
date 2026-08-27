---
id: devpost-build-with-gemini-xprize
name: Build with Gemini XPRIZE
tier: 编程/黑客松
directions:
  - 黑客松与数据竞赛
status: active
organizer: "XPRIZE（Sponsor，Culver City, CA）× Google（presented by Google / Google Cloud 背书）；Devpost, Inc.（Administrator）"
award_levels:
  - name: "1st place"
    count_or_ratio: "1 名 × $500,000"
    note: 总冠军现金奖（USD）
  - name: "2nd place"
    count_or_ratio: "1 名 × $200,000"
    note: USD
  - name: "3rd–5th place"
    count_or_ratio: "3 名 × $100,000 each"
    note: USD
  - name: "Category Prize（5 类：Education & Human Potential / Entrepreneurship & Job Creation / Small Business Services / Money & Financial Access / Professional Services Access）"
    count_or_ratio: "5 名 × $50,000"
    note: 每类别 1 名
  - name: "Runner Up"
    count_or_ratio: "15 名 × $50,000"
    note: USD
key_dates:
  submission_open:
    date: 2026-05-19
    verified: true
    note: "Submission Period 起 2026-05-19 10:00 PT（geminixprize.com/rules 全文 × devpost /rules 搜索快照双源）"
  submission_close:
    date: 2026-08-17
    verified: true
    note: "Submission Period 止 2026-08-17 13:00 PT（双源同上）"
  judging_start:
    date: 2026-08-18
    verified: true
    note: "Judging Period 起 10:00 PT"
  judging_end:
    date: 2026-09-15
    verified: true
    note: "Judging Period 止 17:00 PT"
  winners_announcement:
    date: 2026-09-25
    verified: true
    note: "官方口径 'On or around September 25, 2026 (2:00 pm PT)'，含 Finalist Pitch；尚未发生，关注节点"
deliverables:
  - "GitHub 仓库（须共享给 testing@devpost.com 与 judging@hacker.fund）"
  - "3 分钟视频（公开托管）"
  - "Written Narrative（500–1000 词）"
  - "收入证据（Stripe dashboard export 或银行对账单 + P&L）"
  - "费用证据（expenses）"
  - "产品证据（agent execution logs、API usage records）"
  - "客户证据（early customer interactions / testimonials，如有）"
ai_policy:
  summary: "强制 Gemini：含 LLM 功能的项目必须用 Gemini API 完成部署应用中至少一次 LLM 调用（可并用其他 LLM 提供商）；必须至少使用一个 Google Cloud 产品；业务须由 AI agents 运营（'Your business has to be operated by AI agents and must use at least one product from Google Cloud.'）。评审含 AI-Native Operations 维度。"
  url: https://www.geminixprize.com/rules
  checked: 2026-08-27
credibility: 交叉验证
last_verified: 2026-08-27
sources:
  - url: https://xprize.devpost.com/
    title: Build with Gemini XPRIZE（Devpost 赛站首页：奖金块/提交物/AI 运营要求）
    accessed: 2026-08-27
  - url: https://www.geminixprize.com/rules
    title: Official Rules — Build with Gemini XPRIZE（主办方官网规则全文：日期/奖金表/Gemini 条款）
    accessed: 2026-08-27
  - url: https://www.geminixprize.com/
    title: Build with Gemini XPRIZE 官网首页（26,470 builders registered）
    accessed: 2026-08-27
  - url: https://xprize.devpost.com/rules
    title: Official Rules - Build with Gemini XPRIZE - Devpost（直接抓取失败，事实经搜索快照交叉，详见正文降级说明）
    accessed: 2026-08-27
  - url: https://xprize.devpost.com/winners
    title: Winners 页（获奖者 2026-09-25 公布后启用，winners 深构分片入口）
    accessed: 2026-08-27
---

# Build with Gemini XPRIZE — meta

## 概况（全部为 2026-08-27 实抓）

- 90 天黑客松（Ideate/Build/Ship/Grow），要求"真实产品、真实收入、真实业务"（Real product. Real revenue. A real business.），总奖金 $2,000,000、共 25 个获奖名额。
- 主办：XPRIZE（Sponsor）× Google（presented）；承办：Devpost（Administrator）。
- 注册规模：26,470 builders/participants（geminixprize.com 首页计数 × devpost 概览页搜索快照，双源一致；devpost 子页计数微增至 26,473–26,477 属计数器时点差异）。
- 当前状态（2026-08-27）：提交已截止（08-17），处于评审期（08-18 ~ 09-15），获奖者定于 2026-09-25 前后公布 → 本条目 status 取 active（赛事未终局，关注节点临近）。
- 评审标准（等权重）：Business Viability / AI-Native Operations / Category Impact。
- 资格：个人（≥18 岁）、团队、以及 <25 人小型组织的雇员。

## AI 政策原文（geminixprize.com/rules §04，2026-08-27 抓取）

- "Projects that include LLM functionality must use the Gemini API for at least one LLM call in the deployed application. Teams may use additional LLM providers alongside Gemini at their discretion."
- "A Project must use at least one product from Google Cloud."
- Devpost 首页（What to Build）："Your business has to be operated by AI agents and must use at least one product from Google Cloud."

## 奖金结构核对

$500k×1 + $200k×1 + $100k×3 + $50k×15（Runner Up）+ $50k×5（Category）= $2,000,000，与官网 "$2M in prizes across 25 winners" 口径吻合（每 Project 最多获一项 Prize）。获奖者未公布。

## 信源与快照

- `kb/raw/devpost-build-with-gemini-xprize/2026-geminixprize-ai-policy.md`（原文摘录）
- `kb/raw/devpost-build-with-gemini-xprize/2026-geminixprize-rules.md`（规则全文）
- `kb/raw/devpost-build-with-gemini-xprize/2026-devpost-home.md`（首页要点 + 失败记录）

## 待核验清单

- [ ] 2026-09-25 获奖者公布后：核抓 winners 页，派发 winners 深构分片。
- [ ] devpost /rules、/details 子页直接抓取持续 -302（超 budget 重试上限），当前依赖 geminixprize.com 全文 + 搜索快照；下轮同步时重试直接抓取以补原始快照。
- [ ] Finalist Pitch 名单与流程细节（规则提到 top finalists 现场路演，具体名单待公布）。
- [ ] 参赛作品数（entries/projects 数）尚无官方口径，仅有人数 26,470。
