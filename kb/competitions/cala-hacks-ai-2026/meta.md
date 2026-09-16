---
id: cala-hacks-ai-2026
name: LA Hacks AI Hackathon 2026
tier: 编程/黑客松
directions:
  - 黑客松与数据竞赛
status: upcoming
organizer: LA Hacks（南加州大学/洛杉矶学生黑客松组织方，旗舰活动为春季 LA Hacks）；MLH（Major League Hacking）2026 赛季挂靠赛事
award_levels: []
key_dates:
  "比赛（线下 36 小时窗口）":
    date: "2026-10-17 14:00 UTC 至 2026-10-18 20:00 UTC（北京时间 10-17 22:00 至 10-19 04:00；官网落地页'October 17-18, 2026'与 MLH 目录记录双源一致）"
    verified: true
  "报名（Apply Now 入口已开放）":
    date: "apply.lahacks.com 已上线（重定向至 /sign-in 登录墙）；开放申请的起始日期未公布"
    verified: false
  "报名截止 / 结果公布":
    date: "未公布"
    verified: false
deliverables: []
ai_policy:
  summary: >-
    未发现 AI 政策条款：官网为 React SPA 单页落地页，实抓 HTML 外壳与 JS bundle 全部字符串（2026-09-09），仅含赛事名称/日期/场地/报名与赞助入口/社交链接，无任何参赛规则、奖项或 AI 工具使用条款；apply.lahacks.com 为登录墙，规则正文不可匿名抓取。官网挂 MLH Code of Conduct 链接（行为准则，非 AI 条款）。后续报名通过登录墙后须补核规则页。
  url: https://ai.lahacks.com
  checked: "2026-09-09"
credibility: 交叉验证
last_verified: "2026-09-09"
sources:
  - url: https://ai.lahacks.com
    title: 官网首页（React SPA 外壳；title "AI Hackathon | LA Hacks"；MLH 2026 赛季 trust badge）
    accessed: "2026-09-09"
  - url: https://ai.lahacks.com/static/js/main.28b4f32a.js
    title: 官网 JS bundle 原件（正文全部内容所在：h1 "AI Hackathon 2026"、日期场地行、Apply/Sponsor/CoC 链接、社交链接）
    accessed: "2026-09-09"
  - url: https://apply.lahacks.com
    title: 官方报名入口（重定向至 /sign-in；页面 title "LA Hacks AI Hackathon 2026"）
    accessed: "2026-09-09"
  - url: https://www.lahacks.com
    title: "LA Hacks 主站（\"NEW: AI HACKATHON\" 导航位 + Apply to AI Hackathon 指向 apply.lahacks.com；旗舰 LA Hacks 2027 于 Pauley Pavilion）"
    accessed: "2026-09-09"
  - url: https://mlh.io/na
    title: MLH 北美赛事目录（内嵌 JSON 事件记录：name/slug=ucla-ai-hackathon-2026/起止 UTC 时间/physical/Los Angeles/status=pending）
    accessed: "2026-09-09"
  - url: https://mlh.io/events/ucla-ai-hackathon-2026
    title: MLH 赛事详情页（2026-09-09 实抓为 404——详情/奖项页未上线，与目录 status=pending 一致）
    accessed: "2026-09-09"
---

# LA Hacks AI Hackathon 2026

以下正文全部基于 2026-09-09 实抓（快照存 `kb/raw/cala-hacks-ai-2026/`：index.html、main.28b4f32a.js、strings_extract.txt（bundle 字符串抽取件）、apply-portal.html、lahacks-main.html、mlh-na.html、mlh-event.html）。**官网为 SPA（React）**，HTML 外壳无正文；事实取自官网 JS bundle 原件（内容硬编码于 bundle，直抓原件非搜索转引），并经 MLH 目录 JSON 与 LA Hacks 主站两处独立直抓原件交叉。

## 赛事定位

- LA Hacks 组织的**全新秋季 AI 主题黑客松**，主站导航标注"NEW: AI HACKATHON"（来源[4]）；区别于其旗舰春季活动 LA Hacks（2027 届为 4 月中旬 Pauley Pavilion，来源[4]）。
- MLH（Major League Hacking）2026 赛季挂靠赛事：官网嵌 MLH trust badge（"Major League Hacking 2026 Hackathon Season"，来源[1]）与 MLH Code of Conduct 链接（来源[2]）；MLH 目录收录 slug `ucla-ai-hackathon-2026`（来源[5]）。
- 线下赛（MLH 目录 formatType=physical），地点 UCLA James West Alumni Center (JWAC)（来源[2]官网 bundle 日期场地行；MLH 目录仅记 Los Angeles, CA，来源[5]）。

## 关键信息（实抓现状）

- **时间**：2026-10-17 至 10-18（MLH 目录记录起 10-17 14:00 UTC / 讫 10-18 20:00 UTC，约 30-36 小时窗口口径；官网落地页"October 17-18, 2026"一致，来源[2][5]双源）。
- **报名**：Apply Now → https://apply.lahacks.com ，已上线但为登录墙（来源[2][3]）；报名截止未公布。
- **奖金/奖项**：未公布——官网无奖项内容，MLH 赛事详情页 404（status=pending，详情/奖项页未上线，来源[6]）；`award_levels` 暂空。
- **评审**：未公布。
- **日程/赛道/参赛资格**：未公布。
- **赞助**：官网开放赞助意向入口（lahacks.com/sponsor-us，来源[2]），提示奖金池尚未定档的常见前期状态。

## AI 政策核查

官网（HTML 外壳 + JS bundle 全字符串）与 MLH 目录记录中均无 AI 工具/大模型使用条款；MLH Code of Conduct 为行为准则链接，非 AI 条款。apply 登录墙内的规则页待报名通道进一步开放后补核（checked 2026-09-09）。

## 待办

1. **奖项与评审未公布**：watch MLH 赛事详情页（当前 404）与官网更新，公布后补 `award_levels`/评审/日程/资格。
2. **规则页在登录墙内**：需注册账号后抓取规则/提交要求，补 `deliverables` 与 ai_policy 复核。
3. 线索级待核（搜索所见，无直抓原件，不入事实）：社交媒体称 hacker 报名已开放、组委会自述"SoCal 最大黑客松"及 1400+ 人规模——均需官方原件佐证方可采信。
