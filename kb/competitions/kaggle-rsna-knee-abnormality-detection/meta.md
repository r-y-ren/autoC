---
id: kaggle-rsna-knee-abnormality-detection
name: "RSNA Knee Abnormality Detection（RSNA 年会 AI Challenge：膝关节 MRI 多模态异常检测）"
tier: 编程/黑客松
directions:
  - 黑客松与数据竞赛
status: active
organizer: "Sponsor：The Radiological Society of North America（RSNA，820 Jorie Blvd #200, Oak Brook, IL）；Kaggle 承办。挑战组织团队 15 人（Cleveland Clinic/UT Southwestern/Toronto/Mayo 等多中心，Acknowledgements 页直抓）"
award_levels:
  - name: "Main Leaderboard — First Prize"
    count_or_ratio: "$9,000（Prizes 页与 rules §5 双证；Main LB 十档合计 $59,000）"
  - name: "Main Leaderboard — Second Prize"
    count_or_ratio: "$7,000"
  - name: "Main Leaderboard — 3rd~10th Prize"
    count_or_ratio: "3rd $6,500 / 4th $6,000 / 5th $5,500 / 6th–10th 各 $5,000"
  - name: "Efficiency Track — First/Second/Third Efficiency Prize"
    count_or_ratio: "$7,000 / $6,000 / $5,000（合计 $18,000；TOTAL PRIZES AVAILABLE: $77,000，rules §5 直抓，与任务包 $77K 口径一致）"
key_dates:
  start:
    date: "2026-07-30"
    verified: true
    note: "官方 Timeline 页直抓（本次全日程字段均已解析，无模板变量）"
  entry_deadline:
    date: "2026-10-15"
    verified: true
    note: "官方 Timeline 页直抓；Team Merger Deadline 同日"
  final_submission_deadline:
    date: "2026-10-22"
    verified: true
    note: "官方 Timeline 页直抓（11:59 PM UTC），与任务包口径一致"
  winners_requirement_deadline:
    date: "2026-11-05"
    verified: true
    note: "官方 Timeline 页直抓：获奖者须提交训练代码、演示视频与方法说明"
deliverables:
  - "Notebook 提交（Code Competition）：CPU/GPU 运行各 ≤9 小时、运行期断网、submission.csv 命名"
  - "12 类膝关节异常的置信度预测（ACL/MCL/内外侧半月板/内外侧 OA/PF OA/积液/滑膜炎/Baker 囊肿/挫伤/骨折），macro-AUC 评测"
  - "获奖者附加义务（Prizes 页直抓）：①方案短视频；②论坛公开开源代码与权重链接；③最终模型公开可供分发与验证（官方示例：kaggle.com/models/tom99763/9th-place-models-rsna-iad）"
ai_policy:
  summary: >-
    官方 rules（2026-08-28 直抓）：①外部数据与模型允许（"Freely & publicly available external data is
    allowed, including pre-trained models"，Code Requirements 页），LLM/工具按 Kaggle "Reasonableness
    Standard" 放行；AMLT 允许；②**运行期断网**（"Internet access disabled"）——API 型 LLM 在推理期不可用，文本侧只能用本地化方案；③Winner
    License CC-BY-NC 4.0（**非商用**）；数据许可 "Commercial and Academic Research - MIRA license"；④RSNA
    年会联动：获奖者受邀参加 AI Challenge Recognition Event（免注册费，需通过方案审查并履行获奖义务）。本赛是多模态医学影像赛：首个"每个影像研究配原始放射报告"的 RSNA
    AI Challenge 数据集（Description 页直抓），报告文本可作第二模态。
  url: https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/rules
  checked: "2026-08-28"
credibility: 官网
last_verified: "2026-09-09"
sources:
  - url: https://www.kaggle.com/api/i/competitions.PageService/ListPages?competitionId=154281
    title: "Kaggle 官方 ListPages API（competitionId=154281）：rules（$77,000/CC-BY-NC 4.0/MIRA）、Prizes（Main 10 档 + Efficiency 3 档）、Timeline（07-30 开赛~11-05 获奖者义务截止）、Evaluation（macro-AUC×12）、Code Requirements（9h/断网）、Efficiency Prize Evaluation（效率分公式）、Acknowledgements（组织团队与数据贡献机构）——2026-08-28 直抓"
    accessed: "2026-08-28"
  - url: https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/overview
    title: "赛站 SSR 壳（标题 'RSNA Knee Abnormality Detection'、description 'Create a model that can detect knee abnormalities based on multimodal imaging data'、赛 ID 154281）——SPA 正文经官方 API 取得"
    accessed: "2026-08-28"
---

# RSNA Knee Abnormality Detection（kaggle-rsna-knee-abnormality-detection）— meta

## 概况（全部为 2026-08-28 官方直抓）

- RSNA 年会 AI Challenge 当届赛事，膝关节 MRI 异常检测：**12 类临床重要异常**多标签预测，主榜指标 **macro-averaged AUC ROC**（Evaluation 页：Final Score = 12 个目标 AUC 的均值）。
- **多模态是本届最大卖点**（Description 页原文）："the first RSNA AI Challenge dataset that pairs every imaging study with its original radiology report"——影像 + 放射报告文本双模态。
- 双轨奖金（合计 $77,000，rules §5 直抓）：Main Leaderboard 十档（$9,000 递减至 $5,000，合计 $59,000）+ Efficiency Track 三档（$7,000/$6,000/$5,000）。
- Efficiency Score 公式（Efficiency Prize Evaluation 页直抓，目标最小化）：Efficiency = AUC/(Benchmark − maxAUC) + RuntimeSeconds/32400——**在逼近最优 AUC 的同时压缩运行时**；参赛资格：须为该队主榜选定提交、私榜高于 sample_submission 基准；同一提交可兼得两轨奖。
- 赛程：07-30 开赛 → 10-15 报名/合队截止 → **10-22 终交**（与任务包一致）→ 11-05 获奖者义务截止（训练代码+视频+方法说明）。**当前报名与提交窗口开放**。
- 工程约束（Code Requirements 页直抓）：Notebook 提交、CPU/GPU ≤9h、**运行期断网**、外部公开数据与预训练模型允许、submission.csv。
- 数据贡献：AZ Delta（比利时）、Centro Rossi（阿根廷）、清迈大学、中国医药大学附设医院（台湾）、摩洛哥 CHU Mohamed VI、Hacettepe（土耳其）、孔敬大学、Koç 大学医院等多中心去标识 MRI+报告（Acknowledgements 页直抓）。

## 线索纠错（对任务包线索，2026-08-28 核）

- "$77K 医学影像旗舰"：**成立**，rules §5 "TOTAL PRIZES AVAILABLE: $77,000" 直抓（$59K 主榜 + $18K 效率轨）。
- "截止 2026-10-22"：**成立**，官方 Timeline 直抓；另有关键前哨日 10-15（报名/合队截止）。
- 页面 slug 注意：赛站实际 slug 为 rsna-knee-abnormality-**ity**-detection；官方 rules 与 Efficiency 页内链使用 abnormalit**ies** 变体（官方页面自身不一致，如实记录）。

## AI 政策原文（rules/Code Requirements 直抓，2026-08-28）

- "Freely & publicly available external data is allowed, including pre-trained models"（预训练模型明确放行）
- "Internet access disabled"（运行期断网——API 型 LLM 推理不可用）
- 外部数据/LLM 费用 Reasonableness Standard（同 Kaggle 通用条款）；AMLT 放行
- Winner License Type: CC-BY-NC 4.0（获奖方案非商用开源）；Data: "Commercial and Academic Research - MIRA license"
- 获奖三义务（Prizes 页）：短视频介绍 + 论坛公开代码/权重链接 + 最终模型公开放置（官方给出往届 9th-place 模型页为格式示例）

## 获奖情况

- 当届未放榜（终交 2026-10-22，获奖者义务 11-05）。RSNA AI Challenge 为年度系列赛（往届为不同赛题的独立赛事，非本赛历届）；winners/2026.md 已建并声明数据缺口。

## 信源与快照

- `kb/raw/kaggle-rsna-knee-abnormality-detection/2026-kaggle-pages-api.json`（全页官方 JSON：rules/prizes/timeline/evaluation/code-requirements/efficiency-prize-evaluation/data-description/acknowledgements 等 10 页）
- `kb/raw/kaggle-rsna-knee-abnormality-detection/2026-kaggle-page-*.md`（逐页导出）
- `kb/raw/kaggle-rsna-knee-abnormality-detection/2026-kaggle-overview-shell.html`（SSR 壳）
- `kb/raw/kaggle-rsna-knee-abnormality-detection/2026-09-09-kaggle-pages-api.json`（**2026-09-09 重验快照**：ListPages API 重抓，rules 内 Timeline 四节点与上表**逐字一致**——"July 30, 2026 - Start Date / October 15, 2026 - Entry Deadline / October 15, 2026 - Team Merger Deadline / October 22, 2026 - Final Submission Deadline / November 5, 2026 - Winners' Requirement Deadline"，均为 11:59 PM UTC → **重验无变化**，`status: active` 维持，报名与提交窗口开放中）
- 抓取通道备注：Kaggle SPA，正文经 Kaggle 官方 ListPages API 匿名直抓，等效直抓官网。

## 待核验清单

- [ ] RSNA Annual Meeting 2026 的 AI Challenge Recognition Event 具体日期/地点（Prizes 页仅称与年会联动，未给日期；RSNA 年会通常 11 月末芝加哥，未直抓不写死）。
- [ ] 数据集规模（study 数/机构数总量）——data-description 页有文件结构但样本量字段未在本次抓取文本中确认，下轮补 Data 页明细。
- [ ] 往届 RSNA AI Challenge 赛事（不同赛题）是否单独立条目（建议 Hunter 分片处理，不并入本条）。
