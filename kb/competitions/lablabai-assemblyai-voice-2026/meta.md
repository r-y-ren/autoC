---
id: lablabai-assemblyai-voice-2026
name: AssemblyAI - Voice Agent Hackathon（lablab.ai × AssemblyAI，2026-09）
tier: 编程/黑客松
directions:
  - 黑客松与数据竞赛
status: upcoming
organizer: lablab.ai（平台，运营主体 NativelyAI Inc.）× AssemblyAI（协办/API 赞助方，Voice AI 基础设施公司）
award_levels:
  - name: Winner（获奖团队）
    count_or_ratio: 5 组
    note: 每组 $1,000 现金 + $1,000 AssemblyAI API credits（总池 $10,000 = $5k 现金 + $5k credits）
key_dates:
  "开赛/开幕（kick-off）":
    date: 北京时间 2026-09-01 23:00（页面按 CST 本地化显示；publishedTime 元数据 19:00 GMT+0400 与之一致）
    verified: true
  "报名窗口":
    date: 全程开放（2026-09-01~09-30 可随时加入，官方原文"registration stays open for the whole build window"）
    verified: true
  "提交截止":
    date: 北京时间 2026-09-30 23:00
    verified: true
deliverables:
  - 语音代理应用（二选一路线：AssemblyAI Voice Agent API 端到端语音代理；或 Realtime STT API 实时转写应用+自选 LLM/TTS）
  - 提交包（官方清单）：项目标题/短描述/长描述/技术与类别标签、封面图、视频演示、幻灯片演示、公开 GitHub 仓库、demo 应用平台、应用 URL
  - 队伍 1~6 人
ai_policy:
  summary: >-
    强制技术栈条款（赛事页原文"Every participant builds on AssemblyAI"）：所有参赛作品必须构建在 AssemblyAI 平台（Voice Agent API 或 Realtime STT API）之上，报名可得免费 API credits。开源/原创条款（获奖免责节原文）："Submissions must be original and MIT-compliant"——提交须原创并符合 MIT 开源合规。未设生成式 AI 工具使用限制（赛事本身即 AI 应用赛，LLM/TTS 组件自选属比赛内容）。风险条款原文要点：prizes depend on eligibility, availability and third-party sponsors；rules, prizes and terms may change or be canceled at discretion；prize distribution may take up to 90 days。
  url: https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon
  checked: "2026-08-28"
credibility: 聚合站
last_verified: "2026-08-28"
sources:
  - url: https://lablab.ai/ai-hackathons/assemblyai-voice-agent-hackathon
    title: 赛事页（赛程/挑战路线/提交物/评审四维/奖金结构/风险条款/评委名录）
    accessed: "2026-08-28"
  - url: https://lablab.ai/
    title: lablab.ai 平台首页（运营主体 NativelyAI Inc./合作品牌/往期获奖公布证据；平台可信度评估）
    accessed: "2026-08-28"
---

# AssemblyAI - Voice Agent Hackathon（lablab.ai）

以下正文基于 2026-08-28 实抓（来源编号对应 frontmatter `sources`；快照存于 `kb/raw/lablabai-assemblyai-voice-2026/`：home-lablab、event-page）。

## 定位与组织

- 月度线上赛（2026-09-01~09-30，完全线上、全球可参与、免费报名），lablab.ai 与 AssemblyAI 联办；AssemblyAI 为 Voice AI 基础设施公司（官网自述其模型支撑 Granola、HeyGen、Ashby、ClickUp 等产品）（来源[1]）。
- 当前报名 385 人（2026-08-28 首页卡片显示，来源[2]）。

## 赛题（来源[1]）

- 在 AssemblyAI 上构建语音代理，二选一路线：
  1. Voice Agent API 端到端语音代理——Universal-3 Pro 语音识别 + LLM 路由 + 语音输出，turn-taking/VAD，JSON-Schema 工具调用；
  2. Realtime STT API 实时转写应用——WebSocket 亚秒级多语言转录、说话人分离，自选 LLM/TTS 组合。

## 评审与奖励（来源[1]）

- 评审四维：Application of Technology / Presentation / Business Value / Originality。
- 5 组获奖，每组 $1,000 现金 + $1,000 API credits。
- 风险条款（官方免责节）：奖金依赖第三方赞助方资格与可用性；规则与奖金可变更或取消；发放最长 90 天。

## 平台可信度评估（任务包前置条件，如实）

- 官方主办方：存在——协办方 AssemblyAI 为具名公司，其 DevRel 工程师 Harnoor Singh 列名开赛演讲者；评委含 Google、PayPal、Hippocratic AI、AI/ML API 等具名公司从业者（来源[1]）。
- 平台运营主体：NativelyAI Inc.（首页页脚，来源[2]）；平台与 AMD/IBM/WeAreDevelopers/TechEx 等品牌有在办/往期合作，页面实见多届已收官事件的获奖公布帖（来源[2]）。
- 往届兑现记录：公开页可证"事件办完+获奖公布"闭环，但奖金实际发放记录不可直证——按任务包口径整体标注：**平台一手（新平台，往届兑现记录待核）**；frontmatter `credibility` 字段枚举无此粒度，取最接近的"聚合站"并在本节显式说明实际等级。

## 对快循环的策略含义（简要）

- 时点优势：9 月赛期与 GOAI 决赛（09-22/23）同窗，Voice Agent 作品可评估"一鱼多吃"（AssemblyAI 强制栈 + MIT 开源与 GOAI 开源要求兼容）。
- 硬约束：必须用 AssemblyAI 技术栈；MIT 合规；提交包含视频+幻灯片+公开仓库——交付物清单可直接映射本框架 Document/Software 角色分工。

## 待办

1. winners：赛事未开始（2026-09-01 开赛），放榜后（预计 10 月，含 90 天发放窗口）建 winners/2026.md 并解构获奖项目（lablab.ai 往期获奖公布帖可作名单源）。
2. 往届兑现记录待核：可检索往期获奖者公开反馈（社区帖/LinkedIn）佐证奖金发放。
3. 官方 Rules 全文页（独立条款页，赛事页仅摘要免责要点）与 Slack/Discord 细则未抓取，AI 政策以赛事页为准的结论待 Rules 页复核。
