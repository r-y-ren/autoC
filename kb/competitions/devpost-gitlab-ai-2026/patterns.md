---
competition_id: devpost-gitlab-ai-2026
last_verified: 2026-08-28
coverage: [2026]
confidence: 中       # 单届样本 + 官方评审标准与评委评语齐备，但获奖项目工程细节多缺（仅博客级描述）
sources:
  - url: https://gitlab.devpost.com/rules
    title: Official Rules（两阶段评审 + 四项等权标准）
    accessed: 2026-08-28
  - url: https://about.gitlab.com/blog/gitlab-ai-hackathon-2026-meet-the-winners/
    title: 官方博客 winners 详版（评委评语 6 条）
    accessed: 2026-08-28
  - url: https://devpost.com/software/lore-living-organizational-record-engine
    title: LORE 项目页（Grand Prize 工程细节）
    accessed: 2026-08-28
---

# GitLab AI Hackathon 模式库（patterns）

## 一、评审偏好（从章程/评委讲评/获奖名单可观察到的取向）

- 规则明文两阶段：Stage One 主题+平台 API/SDK 合格筛选 → Stage Two 四项**等权**（Technological Implementation / Design / Potential Impact / Quality of the Idea）——无单项偏科空间，四边形能力都要出示证据。（/rules，官网级）
- 评委评语的重复关键词（6 条评语样本）："polished / beautifully designed / world-class presentation / easy to use / well-documented / thoroughly documented"——**呈现与文档质量在 Design 权重里被反复计分**，不低于技术新颖度。（官方博客，官网级）
- "action-oriented"被评委逐字引用为主题契合标准（RedAgent 评语）——触发器→动作闭环是硬取向。（官网级）
- 工程完备度信号被点名：LORE 的 "43 automated tests + 40-page report" 直接写进获奖描述；Gitdefender 被评 "production-grade"。（官网级）

## 二、方法论分布（获奖作品的方法/方案套路）

| 模式 | 出现频次/占比 | 代表年份与条目 | 可迁移性 |
|---|---|---|---|
| 触发器→自动动作闭环（commit/MR/事件驱动） | 主奖级 6/6（非随机小样本，频次不代表总体） | 2026：LORE（MR）、Gitdefender（commit）、Launch Control（工作流） | 高：任何 CI/事件源均可接 |
| 多 agent 分工 + 路由 | 3/6 | 2026：LORE（router+8）、Launch Control（Jira/GitHub/监控三 agent） | 中：需 router 与测试基建 |
| 知识图谱/RAG 组织记忆 | 2/6 | 2026：LORE（RAG+防环）、GraphDev（Neo4j 图谱） | 中：图库+抽取管线 |
| 静态分析工具 × LLM 混合推理 | 1/6 | 2026：Gitdefender（Snyk/CodeQL + Gemini） | 高：SAST 免费层可用 |
| 状态镜像/回放（diff→SQL） | 1/6 | 2026：Time-Traveler | 中：需版本化存储设计 |
| 单一云厂商全家桶绑定 | 赞助商 GP 2/2 | 2026：Gitdefender（GCP 全栈）、GraphDev（Claude SDK） | 高：厂商赛道对位策略 |

## 三、往届差异化点（什么样的作品拿到了最高奖）

- Grand Prize（LORE）vs 专项奖的分野：命题纵深（"80% 决策不被讨论"的组织记忆问题）+ 工程完备度（43 测试/40 页报告）+ 评委可感知的完成度（dashboard）三者叠加，而非单一技术亮点。（官方博客，官网级）
- 赞助商赛道拿奖路径清晰：完整使用该厂商栈（Vertex AI+Cloud Run / Claude Agent SDK+Neo4j）即可对位 $10,000 赛道，与主奖池并行不冲突（限奖条款：1 Grand + 1 Category）。（/rules + winners，官网级）
- 单人多次提交可行且被官方表彰（Zelong Wang 三专项一赛道大奖）——产量×完成度策略在本赛制有实证回报。（官网级）

## 四、反面观察（常见失分模式，若有依据）

- 规则红线（官网级）："Chat alone won't qualify"——纯聊天机器人无触发-动作闭环直接不合格（Stage One 筛除）。
- 非开源/无可见许可证的项目 URL 不合格（Stage One）："must be a public project with a visible open source license"。
- 视频>3 分钟或未清楚展示 trigger→action 不合格（/rules）。
- 评委对复杂系统的观感风险：LORE 被评 "several moving parts"（虽为正面语境）——多 agent 架构若呈现混乱会反噬 Design 分。（评委评语推断，标注为推断）

## 五、赛点检查表（评审标准 → 可执行检查项）

- [ ] Technological Implementation：作品含至少 1 个自定义公开 agent/flow，且演示中可见"触发器→动作"完整闭环（规则硬性）
- [ ] Technological Implementation：配套自动化测试与 CI 流水线证据（LORE 获奖模式）
- [ ] Design：dashboard/UI 打磨 + 演示视频脚本化排练（评委 "world-class presentation" 导向）
- [ ] Design：文档层完整（README + 架构说明 + 长篇设计报告）
- [ ] Potential Impact：量化目标用户与痛点（如 "80% 决策丢失"式的可引证问题陈述）
- [ ] Quality of the Idea：命题选在 SDLC 非写码环节（安全/合规/部署/规划），避开同质化 chat 类
- [ ] 平台合规：项目在官方 GitLab group 内公开 + MIT + GitLab DCO v1.1；视频 ≤3 分钟公开托管
- [ ] 赞助商赛道（若冲击）：完整使用 Google Cloud 或 Anthropic 栈并在提交说明中显式标注

## 六、对本框架的启示（喂给 K-02 / 验收报告）

- 方向契合：本赛已结束（2026-04-22 放榜），对快循环无在赛价值；留作 agent 类黑客松的**模板库**与 Zelong Wang 式"多项目复用基建"策略样本。
- 作品工程要点：router+专职 agent、防环逻辑、测试/文档双件套是本项目可复用的获奖三件套。
- 合规栈：MIT + GitLab DCO v1.1 + 平台内公开部署；地区排除名单（巴西/魁北克/俄等）影响队员构成时需在 decide 阶段核查。
- 策略性观察：devpost 系 SPA 渲染抓取有两类污染（旧赛事缓存、失真摘要），KB 流程对 devpost winners 必须双源核对后才可落盘——本条已按此执行。
