# KB 总索引（瘦协调者唯一入口）

> 由慢循环跑批脚本（scripts/kb/build_index.py）自动重建。**主会话只读本文件做决策路由，不逐条读取条目正文**（分片派发时由子 agent 按需读）。

## KB-1 赛事库（交付物 1）

| ID | 赛事 | 方向 | 层级 | 状态 | 关键日期 | AI 政策 | 最近核验 | 条目路径 |
|---|---|---|---|---|---|---|---|---|
| cumcm | 全国大学生数学建模竞赛（高教社杯 CUMCM） | 数模与时序预测 | 学科竞赛 | active | 2026 报名开始:2026-05-01 09:00… | 《全国大学生数学建模竞赛人工智能工具使用规定（2026年试行）》：适用于大语言模 | 2026-08-27 | competitions/cumcm/ |
| devpost-amazon-nova-ai-2026 | Amazon Nova AI Hackathon | 黑客松与数据竞赛 | 编程/黑客松 | ended | registration_open:2026-02-02、submission_close:2026-03-16… | 强制 Nova：'Your task is to build a generat | 2026-08-27 | competitions/devpost-amazon-nova-ai-2026/ |
| devpost-build-with-gemini-xprize | Build with Gemini XPRIZE | 黑客松与数据竞赛 | 编程/黑客松 | active | submission_open:2026-05-19、submission_close:2026-08-17… | 强制 Gemini：含 LLM 功能的项目必须用 Gemini API 完成部署 | 2026-08-27 | competitions/devpost-build-with-gemini-xprize/ |
| heywhale-c4-bigdata-2026 | 2026年中国高校计算机大赛—大数据挑战赛（第十一届 C4-BDC） | 黑客松与数据竞赛 | 编程/黑客松 | active | 报名开放（本届）:北京时间 2026-03-26 10:00、报名&组队截止:北京时间 2026-07-15 12:00… | 未发现 AI 政策条款：本届《大赛通知（盖章）》竞赛规程、平台"参赛须知"、清华 | 2026-08-27 | competitions/heywhale-c4-bigdata-2026/ |
| heywhale-mineru-mdic2026 | 2026 MinerU 数据智能与前沿语料挑战赛（数据智能与前沿语料挑战赛·模塑申城语料普惠计划） | 黑客松与数据竞赛 | 编程/黑客松 | active | … | 赛事本身依托开源文档解析 AI 引擎 MinerU，对 AI/开源工具持明确开放 | 2026-08-27 | competitions/heywhale-mineru-mdic2026/ |
| kaggle-ai-mathematical-olympiad-progress-prize-3 | AI Mathematical Olympiad – Progress Prize 3（AIMO 3） | 黑客松与数据竞赛 | 编程/黑客松 | ended | launch:2025-11-19、entry_deadline:2026-04-08… | 三层实抓：①系列 FAQ（2023-12-19，官方，"for the firs | 2026-08-27 | competitions/kaggle-ai-mathematical-olympiad-progress-prize-3/ |
| kaggle-arc-prize-2026 | ARC Prize 2026（ARC-AGI-2 / ARC-AGI-3 / Paper Track 三赛道） | 黑客松与数据竞赛 | 编程/黑客松 | active | competition_start:2026-03-25、agi3_milestone_1:2026-06-30… | 官方页面实得三组硬条款：①评测环境禁 API 型 LLM——总览页原文 "Int | 2026-08-27 | competitions/kaggle-arc-prize-2026/ |
| mathorcup | MathorCup 数学应用挑战赛（原名 MathorCup 高校数学建模挑战赛） | 数模与时序预测 | 学科竞赛 | ended | … | 《MathorCup数学应用挑战赛人工智能工具使用规定（试行）》（组委会2026 | 2026-08-27 | competitions/mathorcup/ |
| mcm-icm | MCM/ICM 美国大学生数学建模竞赛（Mathematical Contest in Modeling / Interdisciplinary Contest in Modeling） | 数模与时序预测 | 学科竞赛 | upcoming | 2027届_竞赛开始:2027-01-28 17:00 EST（美东周四下午5:00）… | COMAP 允许负责任地使用 AI（'Solving the problems  | 2026-08-27 | competitions/mcm-icm/ |
| tianchi-loreal-beauty-tech-hackathon-2026 | 欧莱雅第二届美妆科技黑客松——用 AI 造点美（天池·AI大模型赛） | 黑客松与数据竞赛 | 编程/黑客松 | active | … | 详情页全文未设任何 AI 工具使用限制、申报或披露条款；赛事本身即以 AI 应用 | 2026-08-27 | competitions/tianchi-loreal-beauty-tech-hackathon-2026/ |
| tianchi-qoder-thursday | Q力星期四（Qoder码力星期四）系列赛（天池·AI大模型赛） | 黑客松与数据竞赛 | 编程/黑客松 | active | 系列赛期:2026-07-16 至 2027-07-31… | 系列由阿里 AI 编程工具 Qoder 冠名，官方推荐并鼓励使用 AI 编程工具 | 2026-08-27 | competitions/tianchi-qoder-thursday/ |

## KB-2 科技库（交付物 2）

| ID | 名称 | 领域 | 方向 | 成熟度 | 比赛映射 | 发表 | 最近核验 |
|---|---|---|---|---|---|---|---|
| arxiv-2608.17293 | Beyond MSE: Rethinking the Evaluation Metric and Benchmarking for Irregular Time Series Forecasting | 时序预测、机器学习、评估方法 | 数模与时序预测 | paper | 数模-预测与评估、数模-数据分析与决策 | 2026-08-18 | 已引 |
| arxiv-2608.18675 | An Empirical Benchmark of Deep Time-Series Models for Smart Meter Energy Forecasting | 时序预测、机器学习、实证基准 | 数模与时序预测 | paper | 数模-数据分析与决策、数模-预测与评估 | 2026-08-19 | 已引 |
| arxiv-2608.20024 | Systematic Evaluation of TabPFN-TS for Zero-Shot Probabilistic Heat Load Forecasting in District Heating Networks | 时序预测、能源系统、机器学习 | 数模与时序预测 | paper | 数模-预测与评估、数模-数据分析与决策 | 2026-08-20 | 已引 |
| arxiv-2608.20052 | DecoVAE: a Lightweight Interpretable Trend-Seasonal VAE Framework for Efficient Probabilistic Time Series Forecasting | 时序预测、机器学习 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-08-20 | 已引 |
| arxiv-2608.23855 | ICI-Time: In-Context Inpainting for Time Series Forecasting | 时序预测、机器学习、跨模态学习 | 数模与时序预测 | paper | 数模-预测与评估、黑客松-数据与算法 | 2026-08-24 | 已引 |
| arxiv-2608.25871 | CEDAR: Controlled and Event-Driven Demand Forecasting via Residual Decomposition | 时序预测、机器学习、需求预测 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-08-26 | 已引 |

## 跑批记录

| 日期 | 类型 | 新增 | 更新 | 隔离 | 说明 |
|---|---|---|---|---|---|
| 2026-08-27 | tech+comp | 技术卡6 / 赛事条目3 | 0 | 0 | 首次真实跑批（T3-a）：arXiv 收紧查询后31候选→6卡；gh未登录按设计降级 |
| 2026-08-27 | discover | 赛事条目8 | 0 | 0 | 黑客松与数据竞赛冷启动（T4批次2）：4搜索分片→35候选→8入库+13留队列；Amazon Nova winners首样（6深构+1降级）；修正失真公告快照 |
