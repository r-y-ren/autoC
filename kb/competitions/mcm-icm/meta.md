---
id: mcm-icm
name: "MCM/ICM 美国大学生数学建模竞赛（Mathematical Contest in Modeling / Interdisciplinary Contest in Modeling）"
tier: 学科竞赛
directions:
  - 数模与时序预测
status: upcoming
organizer: "COMAP — Consortium for Mathematics and its Applications（非营利数学教育组织，官网 comap.org）"
key_dates:
  2027届_竞赛开始:
    date: "2027-01-28 17:00 EST（美东周四下午5:00）"
    verified: true
    note: 三源交叉（官方 instructions 页 + comap.org 赛事总览页 + 赛事中心页）
  2027届_竞赛结束:
    date: "2027-02-01 20:00 EST（美东周一下午8:00）"
    verified: true
    note: 三源交叉（同上，三页均列 Jan 28 – Feb 1, 2027）
  2027届_报名截止:
    date: "2027-01-28 15:00 EST 前"
    verified: false
    note: 单源（官方 instructions 页）；register.php 于 2026-08-27 抓取时显示报名尚未开放，待开放后第二源核验
  2027届_解决方案提交截止:
    date: "2027-02-01 21:00 EST"
    verified: false
    note: 单源（官方 instructions 页）
  2027届_成绩公布:
    date: "2027-05-08"
    verified: false
    note: 单源（官方 instructions 页）；另赛事总览页称奖学金奖每年"5月30日前"公布
deliverables:
  - "单一 Adobe PDF 解决方案报告：英文、正文字号不低于 12pt，全文（摘要页+正文+参考文献+目录+注释+附录+代码）合计上限 25 页"
  - "首页必须为 Summary Sheet（摘要页）；每页页眉含队号与页码（如 Team # 0000000, Page 6 of 25）"
  - "全文不得出现学生/导师/学校姓名，队号（control number）为唯一标识；文件名=队号（如 0000000.pdf），附件小于 25MB"
  - "经官方在线表单提交（每队限一份）；不得提交程序、软件、数据库等非解决方案文件"
  - "若使用 AI：报告末尾附加 'Report on Use of AI' 章节（无页数限制，不计入 25 页）"
ai_policy:
  summary: "COMAP 允许负责任地使用 AI（'Solving the problems does not require the use of AI tools, although their responsible use is permitted.'），但要求团队'对使用 AI 工具的一切保持公开与诚实'（Teams must be open and honest about all their uses of AI tools）。使用 AI 的团队必须：(1) 在报告中明确标注 AI 使用，含所用模型与用途，并在 25 页报告末尾附加 'Report on Use of AI' 章节（无页数限制、不计页数）；(2) 核验 AI 生成内容与引文的准确性/有效性/适当性并纠错；(3) 在正文使用行内引注并在参考文献列出所有所用 AI 工具；(4) 警惕 LLM 复现他人文本导致抄袭——无清晰引注的作品'可能被认定为剽窃并取消资格'。政策源于 LLM 与生成式 AI 兴起，覆盖从模型/代码开发到报告撰写的全环节。"
  url: "https://www.contest.comap.com/undergraduate/contests/mcm/instructions.php"
  checked: "2026-08-27"
credibility: 官网
last_verified: "2026-08-27"
sources:
  - url: "https://www.contest.comap.com/undergraduate/contests/mcm/instructions.php"
    title: "MCM/ICM 2027 官方竞赛说明（Contest Instructions，COMAP contest.comap.com）"
    accessed: "2026-08-27"
  - url: "https://www.comap.org/contests/mcm-icm"
    title: "COMAP 官网 MCM/ICM 赛事总览页"
    accessed: "2026-08-27"
  - url: "https://www.contest.comap.com/undergraduate/contests/"
    title: "COMAP 本科生赛事中心（Contests 列表页）"
    accessed: "2026-08-27"
  - url: "https://www.contest.comap.com/undergraduate/contests/mcm/register.php"
    title: "MCM/ICM 注册入口页（2026-08-27 抓取时显示报名未开放）"
    accessed: "2026-08-27"
  - url: "https://www.comap.org/"
    title: "COMAP 组织主页（主办方全称与性质核实）"
    accessed: "2026-08-27"
---

# MCM/ICM（美赛）条目笔记

> 本文一切事实均来自 frontmatter `sources` 所列页面于 **2026-08-27** 的实抓内容，引用缩写：
> **[INS]** = contest.comap.com/undergraduate/contests/mcm/instructions.php（官网·2027 届竞赛说明）
> **[OVR]** = comap.org/contests/mcm-icm（官网·赛事总览）
> **[HUB]** = contest.comap.com/undergraduate/contests/（官网·赛事中心）
> **[REG]** = contest.comap.com/.../mcm/register.php（官网·注册入口）
> **[ORG]** = comap.org/（官网·主办方主页）
> 信源等级：以上全部为**官网**一级信源。

## 主办方

COMAP 全称 **Consortium for Mathematics and its Applications**，自我描述为"an award-winning non-profit organization with the goal of improving mathematics education"，自 1980 年起与教育者、学生、企业和工业界合作，开发课程资源、教师培训项目与竞赛机会。[ORG, 2026-08-27]

## MCM 与 ICM 的区别（题目类型 A–F）

- **MCM**（Mathematical Contest in Modeling，数学建模竞赛）对应 **A/B/C 三题**：
  - **Problem A — 连续**（continuous）
  - **Problem B — 离散**（discrete）
  - **Problem C — 数据洞察**（data insights）
- **ICM**（Interdisciplinary Contest in Modeling，交叉学科建模竞赛）对应 **D/E/F 三题**：
  - **Problem D — 运筹学/网络科学**（operations research/network science）
  - **Problem E — 可持续性**（sustainability）
  - **Problem F — 政策**（policy）
- 每队从六题中**任选一题**作答并提交一份解决方案；两个赛事面向高中生与大学本科生开放，MCM/ICM 均为 COMAP 注册商标。[OVR, 2026-08-27; INS, 2026-08-27]

## 2027 届状态与关键日期（status: upcoming 的依据）

- 官方已公布 2027 届竞赛窗口：**2027-01-28（周四）17:00 EST 至 2027-02-01（周一）20:00 EST**；题目于开赛日 16:50 EST 起在镜像站点可见。[INS, OVR, HUB, 2026-08-27]
- **报名尚未开放**：注册入口页当前显示 "We're sorry, but registration for MCM/ICM is not available at this time."。[REG, 2026-08-27]
- 报名截止：**2027-01-28 15:00 EST 前**（逾期一律不受理）；报名费 **每队 $100**、不可退、仅信用卡在线支付；流程为先"导师注册"再"队伍注册"，取得 control number 即为报名成功（不发邮件确认）。[INS, 2026-08-27]
- 解决方案提交截止：**2027-02-01 21:00 EST**（20:00 后不可再修改）。[INS, 2026-08-27]
- 成绩公布：**2027-05-08**；评审于 4–6 月完成。[INS, 2026-08-27]

## 参赛规则要点

- **队伍组成**：1–3 名**同校**学生组队；每名学生只能属于一支队伍；不限制每校报名队数。导师（advisor）可为该校教职工或学生，一名导师可带多队；辅导机构/考试培训/STEM 学习中心不算"学校"。**开赛（2027-01-28 17:00 EST）后队伍成员锁定，可移除不可新增**。[INS, 2026-08-27；OVR 概述"teams of up to three students"]
- **参赛资格**：高中生与大学本科生均可参赛。[INS, OVR, 2026-08-27]
- **报告与提交**：见 frontmatter `deliverables`——单一 Adobe PDF、英文、≥12pt 字体、全篇（含代码附录）25 页上限、首页 Summary Sheet、页眉含队号页码、全文匿名、文件名=队号、<25MB、经官方在线表单提交且每队限一份、不收非解决方案文件。[INS, 2026-08-27]

## AI 使用政策（ai_policy 依据）

以下要点均出自 [INS, 2026-08-27]（原文为英文，关键句摘译）：

1. 背景：政策源于"大语言模型（LLM）与生成式 AI 辅助技术的兴起"，覆盖从模型/代码开发到报告撰写的全环节。
2. 基本立场："Solving the problems does not require the use of AI tools, although their responsible use is permitted."（解题不需要 AI，但允许负责任地使用）；"Teams must be open and honest about all their uses of AI tools."（必须对一切 AI 使用公开诚实）。
3. 申报义务：使用 AI 的团队须在报告中"clearly indicate the use of AI tools in their report, including which model was used and for what purpose"，并在 25 页报告之后附加 **"Report on Use of AI"** 章节——该章节"has no page limit and will not be counted as part of the 25-page solution"。
4. 引注义务：正文使用行内引注（inline citations），并在参考文献部分列出所有使用的 AI 工具。
5. 核验义务：团队须自行核验 AI 生成内容与引文的"accuracy, validity, and appropriateness"并纠正错误；警惕 LLM 复现他人文本——"无清晰引注的作品可能被认定为剽窃并取消资格"。

## 奖项结构（供作品策略参考）

- 评级序列（由低到高）：Successful Participant → Honorable Mention → Meritorious → Finalist → Outstanding Winner（另有 Disqualified / Unsuccessful 类别）。[INS, 2026-08-27]
- 国际 COMAP 奖学金奖：最优秀六支队，$9,000 由队员均分（每人上限 $3,000）另奖学校 $1,000；总览页称该奖"每年 5 月 30 日前公布"。[INS, OVR, 2026-08-27]
- 命名奖项：MCM 侧 Ben Fusaro / Frank R. Giordano / Veena Mendiratta；ICM 侧 Leonhard Euler / Rachel Carson / Pareto；外部学会奖：INFORMS、SIAM、MAA、ASA（仅 C 题）、AMS。[INS, 2026-08-27]

## 待办

- [ ] 2027 届报名开放后：第二源核验报名截止时间与费用（当前单源 [INS]）。
- [ ] 成绩公布节点（2027-05-08）目前单源，待官方日历/FAQ 页二次核验。
- [ ] 历年 Outstanding Winner（O 奖）论文深度解构（本分片未做，待协调者另行派发 winners 分片）。
- [ ] 原始页面快照归档至 `kb/raw/`（本次 collect 阶段写入范围限 `kb/competitions/mcm-icm/`，未落 raw 快照）。
