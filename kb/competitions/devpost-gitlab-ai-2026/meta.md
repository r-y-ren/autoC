---
id: devpost-gitlab-ai-2026
name: "GitLab AI Hackathon（官方规则名：The GitLab Duo Agent Platform Challenge）"
tier: 编程/黑客松
directions:
  - 黑客松与数据竞赛
status: ended
organizer: "GitLab Inc.（Sponsor，San Francisco）；Devpost, Inc.（Administrator）"
award_levels:
  - name: "Grand Prize"
    count_or_ratio: "1 名 × $15,000 + 1000 GitLab Swag points"
  - name: "赞助商赛道 Grand Prize（Most Impactful on GitLab & Google / Most Impactful on GitLab & Anthropic）"
    count_or_ratio: "2 名 × $10,000 + 500 points"
  - name: "专项奖（Most Technically Impressive / Most Impactful / Easiest to Use）"
    count_or_ratio: "3 名 × $5,000 + 1000 points"
  - name: "赞助商赛道 Runner Up（Google / Anthropic）"
    count_or_ratio: "2 名 × $3,500 + 500 points"
  - name: "Green Agent Prize"
    count_or_ratio: "1 名 × $3,000"
  - name: "Sustainable Design Bonus"
    count_or_ratio: "4 名 × $500"
  - name: "Honorable Mention"
    count_or_ratio: "6 名 × $500"
    note: 规则表载 5 席，获奖实发 6 席（首页奖池部件亦为 6 winners）
key_dates:
  submission_open:
    date: 2026-02-09
    verified: true
    note: "Submission Period 起 2026-02-09 10:00 ET（/rules 原文 × 首页赛程条 'Feb 9 – Mar 25, 2026' 双源）"
  submission_close:
    date: 2026-03-25
    verified: true
    note: "Submission Period 止 2026-03-25 14:00 ET（/rules；首页横幅 'as of March 25, 9 AM ET we are no longer accepting access requests' 互证）"
  judging_start:
    date: 2026-03-30
    verified: true
    note: "Judging Period 起 2026-03-30 09:00 ET（/rules 原文）"
  judging_end:
    date: 2026-04-17
    verified: true
    note: "Judging Period 止 2026-04-17 17:00 ET（/rules 原文）"
  winners_announced:
    date: 2026-04-22
    verified: true
    note: "GitLab 官方博客发布日 2026-04-22；规则计划口径 'on or around April 22, 2026 (2:00 p.m. ET)'（双源一致）"
deliverables:
  - "GitLab AI Hackathon group 内的公开项目 URL（必须开源，MIT + GitLab DCO v1.1 或同等商业友好许可）"
  - "可运行的 AI agent 或 flow（构建于 GitLab Duo Agent Platform，覆盖 SDLC 任一环节；须至少 1 个自定义公开 agent 或 flow）"
  - "文本描述"
  - "≤3 分钟演示视频（公开托管；必须清楚展示项目对触发器作出反应并执行动作）"
ai_policy:
  summary: "平台限定而非模型限定：必须构建运行在 GitLab Duo Agent Platform 上的 agent/flow，主题限软件开发全生命周期；'Chat alone won't qualify'——agent 须对触发器反应并执行动作；模型选择自由（获奖方案分别用了 Anthropic Claude、Gemini 2.5 Pro on Vertex AI、Claude Sonnet 4.5 等，用 Google Cloud 或 Anthropic 可解锁对应赞助赛道奖金）；成果须开源（MIT + GitLab DCO v1.1）；地区排除：巴西/魁北克/俄罗斯/古巴/伊朗/朝鲜/叙利亚及克里米亚等地区。"
  url: https://gitlab.devpost.com/rules
  checked: 2026-08-28
credibility: 交叉验证
last_verified: 2026-08-28
sources:
  - url: https://gitlab.devpost.com/
    title: GitLab AI Hackathon 赛站首页（主题/奖金部件/提交物/评审标准/注册 6,936）
    accessed: 2026-08-28
  - url: https://gitlab.devpost.com/rules
    title: Official Rules（日期/资格/奖金表/开源与视频要求/两阶段评审全文）
    accessed: 2026-08-28
  - url: https://gitlab.devpost.com/updates/41783-meet-the-winners
    title: Devpost 官方获奖公告帖（22 项获奖名单 + LORE 官方评语；页面计数 Participants 6958）
    accessed: 2026-08-28
  - url: https://about.gitlab.com/blog/gitlab-ai-hackathon-2026-meet-the-winners/
    title: "GitLab AI Hackathon 2026: Meet the winners（主办方官方博客，2026-04-22，各项目 How it works + 评委评语）"
    accessed: 2026-08-28
  - url: https://devpost.com/software/lore-living-organizational-record-engine
    title: LORE Grand Prize 项目页（多 agent 路由架构/43 测试/挑战与经验原文）
    accessed: 2026-08-28
  - url: https://gitlab.devpost.com/submissions
    title: 官方项目画廊（winners-first 排序，LORE 居首）
    accessed: 2026-08-28
---

# GitLab AI Hackathon — meta

## 概况（全部为 2026-08-28 实抓）

- GitLab 主办、Devpost 承办的线上黑客松（2026-02-09 ~ 03-25 提交，04-22 放榜），已结束。规模：**~6,900+ 注册**（首页横幅 6,936 / 公告帖页面计数 6,958，计数随时间微调）；官方博客口径 "Nearly 7,000 developers built **600+ AI agents and flows**"。
- 命题：在 GitLab Duo Agent Platform 上构建服务 SDLC（规划/安全/合规/部署等非写码环节）的 AI agent 或 flow；**纯聊天不达标**，须"对触发器反应并执行动作"，至少 1 个自定义公开 agent 或 flow。
- 赛制：两阶段评审——Stage One 主题+API/SDK 合格性筛选，Stage Two 四项等权（Technological Implementation / Design / Potential Impact / Quality of the Idea）。
- 奖金：规则表现金合计 **$64,500**（营销口径 "$65,000 in prizes"）；单项最高 Grand Prize $15,000；Google Cloud 与 Anthropic 各设 $13,500 赞助赛道；限奖条款：每项目最多 1 Grand + 1 Category。
- 获奖名单（22 项）双源核验：Devpost 公告帖 41783 × GitLab 官方博客完全一致。深构见 `winners/2026.md`。

## 线索纠错（对任务包线索与抓取事故，2026-08-28 核）

- 任务包线索 "$65K 多赞助商赛道制"：成立（$13,500 Google + $13,500 Anthropic + 主奖池），总额精确值 $64,500。
- **渲染污染事故**：博客单页 webReader 首抓返回失真名单（MERMAID/Gorm/Climate Scope 等虚构项目），经公告帖+独立检索证伪后整体弃用——devpost 系站点渲染抓取须双源核对（教训已记入快照）。
- /updates 列表页返回 2024 旧赛事（同子域复用串页），弃用。

## AI 政策原文（/rules 与首页，2026-08-28 抓取）

- "a working AI agent or flow built on the GitLab Duo Agent Platform that helps with some aspect of the software development lifecycle"
- "Chat alone won't qualify. We're looking for agents that react to triggers and take action."
- "It must be a public project with a visible open source license."（MIT + GitLab DCO v1.1）

## 信源与快照

- `kb/raw/devpost-gitlab-ai-2026/2026-devpost-home.md`
- `kb/raw/devpost-gitlab-ai-2026/2026-gitlab-rules.md`
- `kb/raw/devpost-gitlab-ai-2026/2026-winners-announced.md`（双源公告+事故记录）
- `kb/raw/devpost-gitlab-ai-2026/winners/2026-lore-project.md`

## 待核验清单

- [ ] 获奖团队完整成员名单：官方页面仅载 GraphDev 等 4 项署名 Zelong Wang；LORE/Gitdefender 等 18 项团队名未公布（画廊与项目页未渲染 Built by）。
- [ ] 提交总量（submissions 计数）未捕获——画廊分页渲染不全，仅确认 LORE 居首。
- [ ] Honorable Mention 规则载 5 席实发 6 席的差异原因（是否含特殊嘉奖）官方未说明。
- [ ] 除 LORE 外 21 个获奖项目的 devpost.com/software 详情页未抓（/submissions 路由 500），深构仅基于官方博客描述，下轮补抓。
