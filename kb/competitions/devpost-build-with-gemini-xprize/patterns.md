---
competition_id: devpost-build-with-gemini-xprize
last_verified: 2026-08-28
coverage: []            # winners 2026-09-25 公布，尚未发生——无任何年份可解构，本文件全部为规则文本反推
confidence: 低           # 无获奖名单佐证；全部结论为官方规则原文反推（信源等级：官网，高；但无实证层）
sources:
  - url: https://www.geminixprize.com/rules
    title: Official Rules — Build with Gemini XPRIZE（主办方官网规则全文：日期/奖金表/Gemini 与 GCP 强制条款/评审三准则）
    accessed: "2026-08-27"
  - url: https://xprize.devpost.com/
    title: Build with Gemini XPRIZE（Devpost 赛站首页：提交物清单/AI 运营要求/评委名单）
    accessed: "2026-08-27"
  - url: https://www.geminixprize.com/
    title: Build with Gemini XPRIZE 官网首页（Builders registered 26,470）
    accessed: "2026-08-27"
---

# Build with Gemini XPRIZE 模式库（patterns）

> 快照存 `kb/raw/devpost-build-with-gemini-xprize/`（2026-geminixprize-rules.md / 2026-geminixprize-ai-policy.md / 2026-devpost-home.md，均 2026-08-27 实抓）。
> 状态声明：**该赛处于评审期**（Judging Period 2026-08-18 ~ 09-15，规则 §02），**winners 定于 2026-09-25 前后公布，尚未发生**——第二、三节为空表待刷新，全文均为规则文本反推，confidence 低。刷新触发条件见第六节。

## 一、评审偏好（从章程/评委讲评/获奖名单可观察到的取向）

- **官方评审准则原文**（规则 §01/§10，等权重三准则）：Business Viability / **AI-Native Operations** / Category Impact——"All criteria are equally weighted"。信源等级：主办方官网规则全文，高。
- **无获奖名单、无评委讲评可观察**（winners 09-25 公布），以下为从强制条款与提交物清单反推的**作品形态要求**（推断层，非实证）：
  - "Your business has to be operated by AI agents and must use at least one product from Google Cloud."（Devpost 首页 What to Build 原文）——**AI agents 运营业务是形态定义而非功能点缀**，且与独立评审准则 AI-Native Operations 呼应：agent 化运营既是资格面也是打分面；
  - 提交物含强制收入证据——"Stripe dashboard export or bank statement + profit & loss statement"，以及产品证据 "agent execution logs, API usage records"（Devpost 首页提交清单原文）——**实证驱动的评审**：评的是证据包（真实收入、真实运营留痕）而非 pitch 叙事，与赛站口号 "Real product. Real revenue. A real business."（90 天 Ideate/Build/Ship/Grow）一致；
  - GitHub repo 须共享给 testing@devpost.com 与 judging@hacker.fund（提交清单原文）——**testing 邮箱暗示部署应用将被功能实测**（推断），可运行的部署态是隐性门槛；
  - 五分类（Education & Human Potential / Entrepreneurship & Job Creation / Small Business Services / Money & Financial Access / Professional Services Access，规则 §01）+ Category Impact 准则——**类别内的问题相关性与影响力是独立打分面**，且每类设 1 名 $50k Category Prize（§06）。
- 评委名单已公开（Devpost 首页 10 人：Ryan Gates、Eva Zheng、Patti Spencer 等），但无评委背景画像分析——待 9-25 后如有讲评材料再补，不猜测。

## 二、方法论分布（获奖作品的方法/方案套路）

| 模式 | 出现频次/占比 | 代表年份与条目 | 可迁移性 |
|---|---|---|---|
| （空） | — | — | — |

**声明**：表为空——**winners 2026-09-25 公布后首刷**。当前（2026-08-28）无任何获奖名单、无参赛作品样本（参赛项目数亦无官方口径，meta 待办 4；仅注册人数 26,470，geminixprize.com 首页 × Devpost 概览双源一致）。任何"获奖作品常用什么技术栈/方案"的表述在本条目中都无依据，禁止填入。

## 三、往届差异化点（什么样的作品拿到了最高奖）

- （空——**待刷新**。首届即 2026 届，尚未出奖。）
- 9-25 后可回答的问题（预设分析框架，待数据）：$500k 总冠军与 5 名 Category Prize 得主的形态差异；25 席在五分类上的分布是否均衡（每类 Category Prize 1 名是设奖保证，但 top5 与 15 名 Runner Up 的类别分布可观察真实竞争密度）；"收入证据"门槛下获奖者的真实营收量级（若 winners 页披露）。
- 结构性事实（规则 §06，可先记）：$500k×1 + $200k×1 + $100k×3 + $50k×15（Runner Up）+ $50k×5（Category）= $2M / 25 席；**每项目最多获一项奖**——冲总冠军与保类别奖是互斥策略。

## 四、反面观察（常见失分模式，若有依据）

- 无评委讲评、无获奖名单，**实际失分模式零实证**；以下仅为规则原文可证的红线（信源：geminixprize.com/rules §04/§06/§07 与 Devpost 首页提交清单，2026-08-27）：
  - **技术栈资格红线**（§04 原文）：含 LLM 功能的项目未在**部署应用**中用 Gemini API 完成至少一次 LLM 调用 = 资格不符（可并用其他 LLM 提供商，但 Gemini 调用不可缺）；未使用任何 Google Cloud 产品 = 资格不符；
  - **提交物完整性红线**：提交清单 7 项中仅 Customer Evidence 标 "(if any)"，其余（GitHub repo 共享指定双邮箱 / ≤3 分钟公开视频 / 500–1000 词叙事 / 收入证据 / 费用证据 / 产品证据）按清单表述均为必备——**无真实收入与无运营留痕的项目过不了提交清单本身**（推断，Devpost 平台必填性待复核）；
  - **资格红线**（§07）：参赛者须 ≥18 岁；团队可参赛；仅 <25 人小型组织的雇员可参赛——大型组织雇员不在资格内；
  - **奖项策略红线**（§06）："A Project is only eligible for a maximum of one Prize"；
  - **时区红线**（§02）：所有截止为太平洋时间（提交止 2026-08-17 13:00 PT）；
  - **待核验条款**：协调者任务包提示的"窗口期外开发无效"类条款，在现有规则快照提取正文中**无原文对应**（快照章节跳号，05/08/09 节未见于提取正文；Devpost /rules 子页直抓 -302 失败，meta 待办 2）——记待核验，不作为结论引用。

## 五、赛点检查表（评审标准 → 可执行检查项；快循环验收清单的派生源）

- [ ] 部署应用中存在 ≥1 次 Gemini API LLM 调用且留有调用记录（§04 强制；可与其他 LLM 并用）
- [ ] 使用 ≥1 个 Google Cloud 产品并在叙事中明示（§04 强制）
- [ ] 业务流程由 AI agents 运营，agent execution logs + API usage records 归档可查（AI-Native Operations 准则 × 产品证据）
- [ ] 收入证据格式合规：Stripe dashboard 导出或银行对账单 + P&L（提交清单原文）
- [ ] 费用证据齐备（提交清单）
- [ ] GitHub repo 已共享 testing@devpost.com 与 judging@hacker.fund，部署态可被实测（提交清单 + 推断）
- [ ] 视频 ≤3 分钟且公开托管（提交清单硬指标）
- [ ] Written Narrative 500–1000 词（提交清单硬指标）
- [ ] 五分类择一，叙事逐条对齐 Category Impact（评审准则）
- [ ] 商业可行性量化呈现：收入/费用/单位经济口径一致（Business Viability 准则 × 收入/费用证据交叉）
- [ ] 截止时间按 PT 换算自查（§02）
- [ ] 奖项策略自查：每项目限一奖（§06），冲总冠军/保类别奖二选一

## 六、对本框架的启示（喂给 K-02 / 验收报告）

- **第一 watch 项 = 9-25 winners 深构分片**：刷新触发条件为 2026-09-25 前后（官方口径 "on or around September 25, 2026 2:00 pm PT"，含 Finalist Pitch）核抓 `xprize.devpost.com/winners`（URL 已预埋于 meta sources）→ 派发 winners 深构分片 → 首刷本文件第二、三节。评审期（08-18~09-15）结束与公布之间的窗口约 10 天，建议 09-16 起进入 watch 节奏。
- **本届参赛窗口已过**（提交 08-17 截止）：本条目情报价值在于 9-25 后的获奖模式解构，作为下届或同类"真实收入型" AI 黑客松的策略输入，不构成本届行动项。
- **本队 Gemini API 经验评估（如实）**：库内（kb/tech/）**无本队直接使用 Gemini API / Google Cloud 的工程经验档案**；唯一相关记录是第三方项目 Cybermes（kb/tech/gh-Zyrexnn_Cybermes.md，2026-08-28 实抓）提及其 MCP 服务器"面向 Claude Code/Cursor/Gemini 等 AI 客户端"——属客户端兼容性旁证，非本队开发经验。结论：该赛技术栈（Gemini API + GCP）对本队为**未验证栈**，任何参赛/复用决策前须先由 K-02 结合团队画像补栈评估。
- **"证据驱动"赛制对作品工程的提示**：该赛把 agent 运营日志、API 用量记录、收入凭证作为提交物——获奖作品的工程核心是**可审计的运营留痕**而非 demo 完成度；此取向与本框架验收清单"评审标准 × 可验证动作"的派生思路同构，可反哺赛点检查表设计（第五节已按此结构落地）。
- **竞争密度参考（粗算，低置信）**：25 席 / 26,470 注册人 ≈ 0.09% 获奖率（注册口径，参赛项目数无官方口径，实际按项目计的获奖率会更高但无法核算）——用于同类赛的投入产出预期校准，不用于决策。
