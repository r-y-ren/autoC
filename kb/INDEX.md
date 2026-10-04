# KB 总索引（瘦协调者唯一入口）

> 由慢循环跑批脚本（scripts/kb/build_index.py）自动重建。**主会话只读本文件做决策路由，不逐条读取条目正文**（分片派发时由子 agent 按需读）。

## KB-1 赛事库（交付物 1）

| ID | 赛事 | 方向 | 层级 | 状态 | 关键日期 | AI 政策 | 最近核验 | 条目路径 |
|---|---|---|---|---|---|---|---|---|
| 3chuang | 全国大学生电子商务"创新、创意及创业"挑战赛（三创赛） | 创新创业大赛 | 学科竞赛 | ended | … | 待核：本次实抓页面（官网为 JS 渲染空壳、两所高校转发通知）均未载人工智能/A | 2026-09-20 | competitions/3chuang/ |
| apmcm | APMCM 亚太地区大学生数学建模竞赛 | 数模与时序预测 | 学科竞赛 | upcoming | 2026主赛_报名截止:2026-11-25… | 实抓页面（官网首页、2026 主赛与中文赛项报名通知、2020 修订版章程全文） | 2026-09-20 | competitions/apmcm/ |
| cumcm | 全国大学生数学建模竞赛（高教社杯 CUMCM） | 数模与时序预测 | 学科竞赛 | active | 2026 报名开始:2026-05-01 09:00… | 《全国大学生数学建模竞赛人工智能工具使用规定（2026年试行）》：适用于大语言模 | 2026-09-09 | competitions/cumcm/ |
| cy-innovation-2026 | 中国国际大学生创新大赛（2026） | 创新创业大赛 | 学科竞赛 | active | 报名系统开放:2026-08-10… | 2026 官方文件无 AI 专项条款（verified 口径：2026-09-0 | 2026-09-20 | competitions/cy-innovation-2026/ |
| devpost-amazon-nova-ai-2026 | Amazon Nova AI Hackathon | 黑客松与数据竞赛 | 编程/黑客松 | ended | registration_open:2026-02-02、submission_close:2026-03-16… | 强制 Nova：'Your task is to build a generat | 2026-08-27 | competitions/devpost-amazon-nova-ai-2026/ |
| devpost-build-with-gemini-xprize | Build with Gemini XPRIZE | 黑客松与数据竞赛 | 编程/黑客松 | active | submission_open:2026-05-19、submission_close:2026-08-17… | 强制 Gemini：含 LLM 功能的项目必须用 Gemini API 完成部署 | 2026-09-09 | competitions/devpost-build-with-gemini-xprize/ |
| devpost-gitlab-ai-2026 | GitLab AI Hackathon（官方规则名：The GitLab Duo Agent Platform Challenge） | 黑客松与数据竞赛 | 编程/黑客松 | ended | submission_open:2026-02-09、submission_close:2026-03-25… | 平台限定而非模型限定：必须构建运行在 GitLab Duo Agent Plat | 2026-08-28 | competitions/devpost-gitlab-ai-2026/ |
| devpost-revenuecat-shipaton-2026 | RevenueCat Shipaton 2026（真实上架 App 的移动端黑客松） | 黑客松与数据竞赛 | 编程/黑客松 | active | registration_open:2026-05-15、submission_open:2026-07-31… | 官方 rules（2026-08-28 经 webReader 直抓全文；202 | 2026-09-16 | competitions/devpost-revenuecat-shipaton-2026/ |
| devpost-treehacks-2026 | TreeHacks 2026（斯坦福全美最大高校黑客松，第 12 届） | 黑客松与数据竞赛 | 编程/黑客松 | ended | event_start:2026-02-13、event_end:2026-02-15… | Devpost 首页 Requirements 节（2026-08-28 直抓） | 2026-08-28 | competitions/devpost-treehacks-2026/ |
| goai-opensource-2026 | GOAI 世界人工智能开源大赛（首届，2026） | 黑客松与数据竞赛 | 编程/黑客松 | active | 报名开启:2026-07-16、线下启动仪式（杭州）:2026-07-21… | 实抓官网首页与新浪转载稿均未设 AI 工具使用限制/披露条款（赛事定位即"用 A | 2026-09-09 | competitions/goai-opensource-2026/ |
| gsk-pyxis-simulation | GSK Pyxis Portfolio Challenge（GSK 药企研发组合 agent 对抗赛） | 黑客松与数据竞赛 | 编程/黑客松 | upcoming | 2026开赛（官方公告）:2026-09-29、entry_deadline（官方公告）:2027-01-04… | 截至 2026-10-05 实抓的全部可用官方材料（gsk.ai 挑战页全文、k | 2026-10-05 | competitions/gsk-pyxis-simulation/ |
| heywhale-c4-bigdata-2026 | 2026年中国高校计算机大赛—大数据挑战赛（第十一届 C4-BDC） | 黑客松与数据竞赛 | 编程/黑客松 | ended | 报名开放（本届）:北京时间 2026-03-26 10:00、报名&组队截止:北京时间 2026-07-15 12:00… | 未发现 AI 政策条款：本届《大赛通知（盖章）》竞赛规程、平台"参赛须知"、清华 | 2026-09-20 | competitions/heywhale-c4-bigdata-2026/ |
| heywhale-mineru-mdic2026 | 2026 MinerU 数据智能与前沿语料挑战赛（数据智能与前沿语料挑战赛·模塑申城语料普惠计划） | 黑客松与数据竞赛 | 编程/黑客松 | active | … | 赛事本身依托开源文档解析 AI 引擎 MinerU，对 AI/开源工具持明确开放 | 2026-09-04 | competitions/heywhale-mineru-mdic2026/ |
| heywhale-yhmfc-2026 | 首届雅安人机气象预报挑战赛（YHMFC 2026，"青衣问天·雅雨先知"） | 黑客松与数据竞赛 | 编程/黑客松 | active | … | 模型技术路线开放条款（5.5(1) 原文："本赛事对机器方所采用的预报模型技术路 | 2026-09-04 | competitions/heywhale-yhmfc-2026/ |
| huashubei | 华数杯大学生数学建模竞赛（2026 年第七届官方页名称；主办方含天津市未来与预测科学研究会） | 数模与时序预测 | 学科竞赛 | ended | 2026第七届_报名:2026-05-08 00:00 至 2026-08-07 12:00… | 《华数杯大学生数学建模竞赛人工智能工具使用章程》PDF（2026-08-06【A | 2026-09-20 | competitions/huashubei/ |
| kaggle-ai-mathematical-olympiad-progress-prize-3 | AI Mathematical Olympiad – Progress Prize 3（AIMO 3） | 黑客松与数据竞赛 | 编程/黑客松 | ended | launch:2025-11-19、entry_deadline:2026-04-08… | 三层实抓：①系列 FAQ（2023-12-19，官方，"for the firs | 2026-08-27 | competitions/kaggle-ai-mathematical-olympiad-progress-prize-3/ |
| kaggle-arc-prize-2026 | ARC Prize 2026（ARC-AGI-2 / ARC-AGI-3 / Paper Track 三赛道） | 黑客松与数据竞赛 | 编程/黑客松 | active | competition_start:2026-03-25、agi3_milestone_1:2026-06-30… | 官方页面实得三组硬条款：①评测环境禁 API 型 LLM——总览页原文 "Int | 2026-09-16 | competitions/kaggle-arc-prize-2026/ |
| kaggle-kaggriculture | Kaggriculture（Google/Kaggle 农场经营 agent 仿真对抗赛） | 黑客松与数据竞赛 | 编程/黑客松 | active | start:2026-07-29、entry_deadline:unknown… | 官方 rules（2026-08-28 经 Kaggle 官方 ListPage | 2026-09-16 | competitions/kaggle-kaggriculture/ |
| kaggle-pokemon-tcg-ai-battle-challenge-playground | PTCG AI Battle Challenge — Playground（The Pokémon Company × Kaggle） | 黑客松与数据竞赛 | 编程/黑客松 | active | start:2026-09-29、entry_deadline:unknown… | 官方 rules（2026-10-05 经 Kaggle 官方 ListPage | 2026-10-05 | competitions/kaggle-pokemon-tcg-ai-battle-challenge-playground/ |
| kaggle-pokemon-tcg-ai-battle-challenge-strategy | PTCG AI Battle Challenge — Strategy Category（The Pokémon Company × Kaggle） | 黑客松与数据竞赛 | 编程/黑客松 | active | start:2026-06-16、simulation_entry_deadline:2026-08-09… | 官方 rules（2026-08-28 经 Kaggle 官方 ListPage | 2026-09-16 | competitions/kaggle-pokemon-tcg-ai-battle-challenge-strategy/ |
| kaggle-rsna-knee-abnormality-detection | RSNA Knee Abnormality Detection（RSNA 年会 AI Challenge：膝关节 MRI 多模态异常检测） | 黑客松与数据竞赛 | 编程/黑客松 | active | start:2026-07-30、entry_deadline:2026-10-15… | 官方 rules（2026-08-28 直抓）：①外部数据与模型允许（"Free | 2026-09-09 | competitions/kaggle-rsna-knee-abnormality-detection/ |
| lablabai-assemblyai-voice-2026 | AssemblyAI - Voice Agent Hackathon（lablab.ai × AssemblyAI，2026-09） | 黑客松与数据竞赛 | 编程/黑客松 | active | … | 强制技术栈条款（赛事页原文"Every participant builds o | 2026-09-09 | competitions/lablabai-assemblyai-voice-2026/ |
| mathorcup | MathorCup 数学应用挑战赛（原名 MathorCup 高校数学建模挑战赛） | 数模与时序预测 | 学科竞赛 | ended | … | 《MathorCup数学应用挑战赛人工智能工具使用规定（试行）》（组委会2026 | 2026-09-20 | competitions/mathorcup/ |
| mcm-icm | MCM/ICM 美国大学生数学建模竞赛（Mathematical Contest in Modeling / Interdisciplinary Contest in Modeling） | 数模与时序预测 | 学科竞赛 | upcoming | 2027届_竞赛开始:2027-01-28 17:00 EST（美东周四下午5:00）… | COMAP 允许负责任地使用 AI（'Solving the problems  | 2026-09-20 | competitions/mcm-icm/ |
| mlh-ghw-data | MLH Global Hack Week: Data Week 2026 | 黑客松与数据竞赛 | 编程/黑客松 | ended | event_start:2026-09-11、event_end:2026-09-17… | MLH 官方 hackathon 规则全文（2026-08-28 核对）无任何  | 2026-10-03 | competitions/mlh-ghw-data/ |
| mlh-hack-the-north | Hack the North 2026 | 黑客松与数据竞赛 | 编程/黑客松 | ended | event_start:2026-09-19、event_end:2026-09-21… | 官方 FAQ（2026-08-28 核对：资格/评审/项目边界/团队/费用/差旅 | 2026-10-03 | competitions/mlh-hack-the-north/ |
| tianchi-cross-embodied-cognition-2026 | 2026-跨本体具身认知极限联合挑战赛（2026具身世界realworld挑战赛·赛道二） | 黑客松与数据竞赛 | 编程/黑客松 | active | registration_open:2026-07-30、registration_close:2026-09-21… | 未发现 AI 工具使用限制条款（参赛协议/赛程/须知核对维度：数据使用/代码分享 | 2026-09-16 | competitions/tianchi-cross-embodied-cognition-2026/ |
| tianchi-ijcai18-alimama-cvr | IJCAI-18 阿里妈妈搜索广告转化预测（Alimama International Advertising Algorithm Competition） | 黑客松与数据竞赛 | 编程/黑客松 | ended | 赛事周期:2018-02 至 2018-05（天池用户协议原文 "from February to May 2018"）… | 抓取材料中无 AI 工具使用条款（2018 年赛前 LLM 时代，信息页与用户协 | 2026-08-28 | competitions/tianchi-ijcai18-alimama-cvr/ |
| tianchi-loreal-beauty-tech-hackathon-2026 | 欧莱雅第二届美妆科技黑客松——用 AI 造点美（天池·AI大模型赛） | 黑客松与数据竞赛 | 编程/黑客松 | active | … | 详情页全文未设任何 AI 工具使用限制、申报或披露条款；赛事本身即以 AI 应用 | 2026-09-09 | competitions/tianchi-loreal-beauty-tech-hackathon-2026/ |
| tianchi-qoder-thursday | Q力星期四（Qoder码力星期四）系列赛（天池·AI大模型赛） | 黑客松与数据竞赛 | 编程/黑客松 | active | 系列赛期:2026-07-16 至 2027-07-31… | 系列由阿里 AI 编程工具 Qoder 冠名，官方推荐并鼓励使用 AI 编程工具 | 2026-09-16 | competitions/tianchi-qoder-thursday/ |
| tiaozhanbei-chuangye | 第十五届"挑战杯"中国大学生创业计划竞赛（建设银行冠名） | 创新创业大赛 | 学科竞赛 | ended | 第十五届 校级初赛:2026-05-31 前（通知：5月底前）… | 待核：官网举办通知正文（2026-05-23，2026-09-04 直抓）未载人 | 2026-10-03 | competitions/tiaozhanbei-chuangye/ |
| ucla-ai-hackathon-2026 | LA Hacks AI Hackathon 2026 | 黑客松与数据竞赛 | 编程/黑客松 | upcoming | event_start:2026-10-17、event_end:2026-10-18… | 2026-08-28 核对赛事官网公开响应、MLH 赛季条目与 MLH 赛事奖品 | 2026-10-03 | competitions/ucla-ai-hackathon-2026/ |
| wuyi-mcm | 五一数学建模竞赛 | 数模与时序预测 | 学科竞赛 | ended | 2026第二十三届_报名:2026-04-02 08:00 至 2026-04-30 24:00（北京时间）… | 实抓页面（官网首页、本届竞赛列表、第二十三届参赛邀请函、评选结果公示）均未发现  | 2026-09-20 | competitions/wuyi-mcm/ |
| xczxcy-dasai | 第六届全国大学生乡村振兴大赛 | 创新创业大赛 | 学科竞赛 | active | 通知发布/报名启动:2026-08-08（通知落款日期）；发布页发布时间 2026-08-10… | 待核：通知正文（文档第 1-8 页已逐页视读，含联系方式与落款页）未载人工智能/ | 2026-10-03 | competitions/xczxcy-dasai/ |

## KB-2 科技库（交付物 2）

| ID | 名称 | 领域 | 方向 | 成熟度 | 比赛映射 | 发表 | 最近核验 |
|---|---|---|---|---|---|---|---|
| Symmetry-Informed_MARL_A_Decentralized_and_Cooperative_UAV_Swarm_Control_Approach_for_Communication_Coverage | 对称性增强MARL的UAV集群通信覆盖控制（SiGNN） | 多智能体强化学习、图神经网络、无人机集群控制 | 黑客松与数据竞赛、数模与时序预测 | paper | 黑客松-数据与算法、数模-数据分析与决策 | 2025-01-01 | 已引 |
| alam2024JointTrajectoryControl | 多UAV群网络跨层联合控制（MA-DDPG） | UAV 自组网、多智能体强化学习、跨层优化 | 创新创业大赛、黑客松与数据竞赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| alkouz2022InflightEnergydrivenComposition | 飞行中能量共享的无人机群服务组合（EaaS） | 无人机群服务计算、服务组合、能量共享 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2022-01-01 | 已引 |
| arxiv-2608.11327 | Long-Horizon Forecasting of Complete Financial Statements with Forma | 金融时序预测、财务报表建模、机器学习 | 数模与时序预测 | paper | 数模-数据分析与决策、双创-文书与申报 | 2026-08-11 | 已引 |
| arxiv-2608.11359 | Market-Information-Aware Gated-LoRA of Foundation Models for Transferable Day-Ahead Electricity Price Forecasting | 时序预测、电力市场、参数高效微调 | 数模与时序预测 | paper | 数模-预测与评估、黑客松-数据与算法 | 2026-08-11 | 已引 |
| arxiv-2608.14106 | Forecast Collapse in Time-Series Foundation Models | 时序预测、金融时序、预测校准与排序 | 数模与时序预测 | paper | 数模-预测与评估、Kaggle-竞赛 | 2026-08-14 | 已引 |
| arxiv-2608.15291 | ReasonCast: Agentic Demand Forecasting with Selective Semantic Reasoning | 时序预测、需求预测、大语言模型智能体 | 数模与时序预测 | paper | 数模-预测与评估、Kaggle-竞赛 | 2026-08-15 | 已引 |
| arxiv-2608.16098 | AsyTO: Asymmetric Temporal Operator for Parameter-Efficient Multivariate Time Series Forecasting | 时序预测、轻量化模型 | 数模与时序预测 | paper | 数模-预测与评估、数模-数据分析与决策 | 2026-08-17 | 已引 |
| arxiv-2608.16410 | TRACE-CASH: Trial-History-Conditioned Reinforcement Learning for Adaptive Configuration Exploration in Time-Series CASH | 时序预测、自动机器学习、超参数优化 | 数模与时序预测 | paper | 数模-数据分析与决策、数模-预测与评估 | 2026-08-17 | 已引 |
| arxiv-2608.17164 | SCENARIODIFF: A Scenario-level Guidance Framework for Multimodal Time Series Forecasting（扩展版） | 时序预测、多模态学习、大模型智能体 | 数模与时序预测 | paper | 数模-预测与评估、数模-数据分析与决策 | 2026-08-17 | 已引 |
| arxiv-2608.17284 | Rethinking Irregular Time Series Forecasting from the Perspective of Basis Functions（DNBNet） | 时序预测、机器学习 | 数模与时序预测 | paper | 数模-预测与评估、数模-数据分析与决策 | 2026-08-18 | 已引 |
| arxiv-2608.17293 | Beyond MSE: Rethinking the Evaluation Metric and Benchmarking for Irregular Time Series Forecasting | 时序预测、机器学习、评估方法 | 数模与时序预测 | paper | 数模-预测与评估、数模-数据分析与决策 | 2026-08-18 | 已引 |
| arxiv-2608.17299 | LiveHouse-TS: An Open-world Living Benchmark for Time Series Foundation Models | 时序预测、基准评测、基础模型评估 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-08-18 | 已引 |
| arxiv-2608.17333 | SPACE: Sample-cloud Predictive Adaptive Conformal Ellipsoids for Multivariate Time-Series Forecasting | 时序预测、不确定性量化、共形预测 | 数模与时序预测 | paper | 数模-预测与评估、Kaggle-竞赛 | 2026-08-18 | 已引 |
| arxiv-2608.18675 | An Empirical Benchmark of Deep Time-Series Models for Smart Meter Energy Forecasting | 时序预测、机器学习、实证基准 | 数模与时序预测 | paper | 数模-数据分析与决策、数模-预测与评估 | 2026-08-19 | 已引 |
| arxiv-2608.19447 | Quantifying Event Impacts on Time Series via Multiscale Contrastive Learning | 时序预测、事件影响量化、金融科技 | 数模与时序预测 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2026-08-19 | 已引 |
| arxiv-2608.19966 | Rethinking Patch Based Multivariate Time Series Forecasting with Semantic Structured Partitioning | 时序预测、Transformer、机器学习 | 数模与时序预测 | paper | Kaggle-竞赛、数模-预测与评估 | 2026-08-20 | 已引 |
| arxiv-2608.20024 | Systematic Evaluation of TabPFN-TS for Zero-Shot Probabilistic Heat Load Forecasting in District Heating Networks | 时序预测、能源系统、机器学习 | 数模与时序预测 | paper | 数模-预测与评估、数模-数据分析与决策 | 2026-08-20 | 已引 |
| arxiv-2608.20025 | CLaST: Context-aware Contrastive VAE for Probabilistic Time Series Forecasting | 时序预测、概率预测、深度生成模型 | 数模与时序预测 | paper | 数模-预测与评估、Kaggle-竞赛 | 2026-08-20 | 已引 |
| arxiv-2608.20052 | DecoVAE: a Lightweight Interpretable Trend-Seasonal VAE Framework for Efficient Probabilistic Time Series Forecasting | 时序预测、机器学习 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-08-20 | 已引 |
| arxiv-2608.20761 | Fuzzy-MoE: Interpretable Regime-Conditioned Expert Routing for Non-Stationary Multivariate Time Series Forecasting | 时序预测、机器学习、可解释AI | 数模与时序预测 | paper | 数模-预测与评估、黑客松-数据与算法 | 2026-08-21 | 已引 |
| arxiv-2608.21277 | ConceptTS: LLM-Guided Concept Bottlenecks for Interpretable Multivariate Time-Series Forecasting | 时序预测、可解释性、大语言模型 | 数模与时序预测 | paper | 数模-预测与评估、数模-数据分析与决策 | 2026-08-21 | 已引 |
| arxiv-2608.22108 | Development and Feasibility Evaluation of an Edge AI as Medical Device System for Breast Cancer Multidisciplinary Team Meetings | on-device AI、语音识别、临床决策支持 | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-22 | 已引 |
| arxiv-2608.22634 | GeoRisk-RAG: A Hierarchy-Aware Risk Framework for Improving RAG Reliability through Selective Answering | retrieval augmented generation、可信 AI、地理空间决策 | 黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2026-08-23 | 已引 |
| arxiv-2608.22652 | Evaluating Inference-Time Defenses Against Package Hallucination in LLM-Generated Code | LLM 代码生成、软件供应链安全、评测方法 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-23 | 已引 |
| arxiv-2608.22968 | Do Time-Series Foundation Models Pay Off for Industrial Monitoring? A Cost-Aware Empirical Study | time series foundation model、异常检测与状态监测、模型选型 | 数模与时序预测 | paper | 数模-预测与评估、数模-数据分析与决策 | 2026-08-24 | 已引 |
| arxiv-2608.23011 | Coarse Indexing, Fine Evidence: Decoupling Temporal Granularity in Long-Video RAG | long-video understanding、retrieval augmented generation、高效检索 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-24 | 已引 |
| arxiv-2608.23221 | Which Histories Matter for Time Series Forecasting? Learning Predictive Relevance with Future Supervision | 时序预测、信息检索、检索增强预测 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-08-24 | 已引 |
| arxiv-2608.23241 | Retrieval-Augmented Classification of Environmental Mitigations in Hydropower Licensing Documents | 检索增强生成、文本分类、长尾学习 | 黑客松与数据竞赛 | paper | Kaggle-竞赛、黑客松-数据与算法 | 2026-08-24 | 已引 |
| arxiv-2608.23252 | The Laws of Context Allocation: Causal Measurement and Closed-Loop Orchestration in Generative Search | 检索增强生成、上下文工程、LLM评测 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法、Kaggle-竞赛 | 2026-08-24 | 已引 |
| arxiv-2608.23473 | MetaCaster: Meta-Harness-Optimized Agent for End-to-End Few-Shot Learning of Lightweight Time Series Forecasters | 时序预测、智能体、小样本学习 | 数模与时序预测 | paper | 数模-预测与评估、黑客松-数据与算法 | 2026-08-24 | 已引 |
| arxiv-2608.23855 | ICI-Time: In-Context Inpainting for Time Series Forecasting | 时序预测、机器学习、跨模态学习 | 数模与时序预测 | paper | 数模-预测与评估、黑客松-数据与算法 | 2026-08-24 | 已引 |
| arxiv-2608.23918 | MARS: Multi-Specialist LLM Relay System for Competitive Programming | 代码生成、多智能体系统、竞赛编程 | 黑客松与数据竞赛 | paper | ACM-训练体系、黑客松-数据与算法 | 2026-08-24 | 已引 |
| arxiv-2608.23965 | RAGSentinel: Certifiable Geometric Consensus for Robust Retrieval-Augmented Generation | retrieval augmented generation、LLM 安全与鲁棒性 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-25 | 已引 |
| arxiv-2608.23992 | Hybrid Semantic Tool Discovery for Enterprise MCP Gateway（SCOUT） | LLM agents、MCP、工具检索/hybrid search | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-25 | 已引 |
| arxiv-2608.24017 | WebMCP-Phalanx: Enforcing and Characterizing Trust Boundaries for Browser-Integrated LLM Agents | LLM agents、浏览器安全、MCP | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-25 | 已引 |
| arxiv-2608.24022 | What Guides the Agent? Adjudicating Unauthorized Behavior via Localizing Behavior-Guiding Instructions（AttnLocate） | LLM agents、agent 安全、可解释性 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-25 | 已引 |
| arxiv-2608.24033 | ChorusTIC: Training-Free Multivariate Time Series Classification via Chorus In-Context Learning | time series foundation model、时序分类、in-context learning | 数模与时序预测 | paper | 数模-数据分析与决策、Kaggle-竞赛 | 2026-08-25 | 已引 |
| arxiv-2608.24087 | Knowing When to Ask for Help: Bayesian Self-Escalation in Hierarchical LLM Agents | LLM agents、模型级联、推理成本优化 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-25 | 已引 |
| arxiv-2608.24103 | ACE: A Self-Correcting Agentic Canvas Editor for Multi-Slide Presentation Automation | LLM agents、文档智能、演示自动化 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-25 | 已引 |
| arxiv-2608.24303 | Causal Analysis for Time Series Foundation Models | time series foundation model、模型评估与选型、因果分析 | 数模与时序预测 | paper | 数模-预测与评估、Kaggle-竞赛 | 2026-08-25 | 已引 |
| arxiv-2608.24569 | When "Must" Becomes "Maybe": Constraint Weakening in LLM Agent Workflows | LLM agents、工作流可靠性、状态管理 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-25 | 已引 |
| arxiv-2608.24735 | Meta^n: Recursive Self-Improvement through Emergent Depth | LLM agents、测试时自我改进、智能体记忆 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法、Kaggle-竞赛 | 2026-08-25 | 已引 |
| arxiv-2608.24753 | The RAT: A Unified Bayesian Model for RAG Evaluation | retrieval augmented generation、LLM 评估与不确定性 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法、数模-预测与评估 | 2026-08-25 | 已引 |
| arxiv-2608.24977 | Retrieved But Not Reliable: A Survey on Attacks, and Defenses in Retrieval-Augmented Generation | retrieval augmented generation、LLM 安全与鲁棒性 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法、Kaggle-竞赛 | 2026-08-25 | 已引 |
| arxiv-2608.25039 | LifePlanner: Evaluating LLM Agents for Geo-spatial Planning with Social Media Data | LLM agents、geo-spatial planning、多模态证据检索 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-25 | 已引 |
| arxiv-2608.25080 | NVExplain: Explaining Time Series Forecasting with Latent Trajectory Analysis and Structure-Preserving Surrogates | 时序预测、可解释性、事后归因 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-08-25 | 已引 |
| arxiv-2608.25123 | SelfGraphRAG: Bridging the Supervision Gap in Graph-Based RAG with Synthetic QA Generation | retrieval augmented generation、knowledge graph、合成数据 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-25 | 已引 |
| arxiv-2608.25128 | When Does Context Routing Help? A Systematic Study of Multi-Modal Fusion in Time Series Forecasting | 时序预测、多模态融合、实证研究 | 数模与时序预测 | paper | 数模-预测与评估、数模-数据分析与决策 | 2026-08-25 | 已引 |
| arxiv-2608.25152 | Belief Cascades Drive Persuasion in LLM Agent Networks | LLM agents、多智能体仿真、舆情传播 | 黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2026-08-25 | 已引 |
| arxiv-2608.25198 | Tunable Tool-Call Rates in LLM Agents via Representation Steering | LLM agents、可解释性、推理时控制 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-25 | 已引 |
| arxiv-2608.25486 | PonsRAG: A Pons-Inspired RAG Bridging Cognitive Islands for Coordinated Long Narrative Reasoning | retrieval augmented generation、长上下文推理、叙事理解 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-26 | 已引 |
| arxiv-2608.25500 | CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval | LLM agents、skill library、skill retrieval | 黑客松与数据竞赛 | paper | 黑客松-数据与算法、Kaggle-竞赛 | 2026-08-26 | 已引 |
| arxiv-2608.25735 | Pointing the Way, Hiding the Destination: Practical Private Dense Retrieval at Scale | retrieval augmented generation、隐私保护检索、密码学 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-26 | 已引 |
| arxiv-2608.25871 | CEDAR: Controlled and Event-Driven Demand Forecasting via Residual Decomposition | 时序预测、机器学习、需求预测 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-08-26 | 已引 |
| arxiv-2608.25992 | ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs | LLM agents、agent orchestration、cost-aware routing | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-26 | 已引 |
| arxiv-2608.26199 | Benchmarking AI Agents for Hardware Design Automation via MCP Tool Calling | LLM agents、MCP、agent 评测/基准 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-25 | 已引 |
| arxiv-2608.26385 | Why RAGs Hallucinate: Penalty-Aware Evaluation of Retrieval-Augmented Generation Systems with Knowledge-Gap Canaries | RAG、评测方法、幻觉检测 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-26 | 已引 |
| arxiv-2608.26604 | hoBIT: A Profile-Aware Retrieval-Augmented Chatbot for University Academic Advising | RAG、个性化检索、对话系统 | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-27 | 已引 |
| arxiv-2608.26747 | AgentFold: Closed-Loop Agentic Search for Protein Folding Model Design | LLM agents、agentic search、多智能体、蛋白质折叠 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-27 | 已引 |
| arxiv-2608.26753 | ABE-Ralph: Auditing Experimental Fidelity in LLM-Driven Scientific Research | LLM agents、AI for science、evaluation audit | 黑客松与数据竞赛 | demo | 黑客松-数据与算法、Kaggle-竞赛 | 2026-08-27 | 已引 |
| arxiv-2608.26829 | SAGE: Variate-Wise Semantic Augmentation for Vision-Language Time Series Forecasting | time series forecasting、vision-language models、语义增强 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-08-27 | 已引 |
| arxiv-2608.26899 | Counterfactual Bias Testing for Application Tracking Systems | LLM agents、algorithmic fairness、audit | 黑客松与数据竞赛 | paper | 黑客松-数据与算法、数模-数据分析与决策 | 2026-08-27 | 已引 |
| arxiv-2608.26990 | DSA: Evidence-Aware LLM-Agent Orchestration for Multi-Market Stock Research | LLM agents、multi-agent orchestration、quantitative research | 黑客松与数据竞赛 | demo | 黑客松-数据与算法、数模-数据分析与决策 | 2026-08-27 | 已引 |
| arxiv-2608.27146 | SARA: Separating Action Induction from Runtime Authorization in Tool-Augmented LLM Agents | LLM agents、agent security、prompt injection | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-27 | 已引 |
| arxiv-2608.27167 | Calibrated Enough to Know, Not Calibrated to Act: Fabricated Evidence Makes LLM Agents Commit to the Unknowable | LLM agents、校准与可信性、评测方法 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-27 | 已引 |
| arxiv-2608.27182 | TraceBench: Controlled Evaluation of LLM Agents for Time-Series Root-Cause Attribution | LLM agents、时序异常检测、根因分析 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-27 | 已引 |
| arxiv-2608.27260 | What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents | LLM agents、合成数据、数据工程方法论 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-08-27 | 已引 |
| arxiv-2608.27456 | UrbanGround: From Local Perception to Spatial Agency in a Real-Scale City | LLM agents、具身导航、空间推理 | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-27 | 已引 |
| arxiv-2608.28134 | AdaRDiff：可学习可逆差分即插即用模块（长程预测通用提速器） | 时序预测、可逆差分、即插即用模块 | 数模与时序预测 | paper | 数模-预测与评估、Kaggle-竞赛 | 2026-08-28 | 已引 |
| arxiv-2608.30976 | CastClaw：人机协同预测 agent 的 harness 工程（执行报告+显式停止条件） | LLM agent、时序预测、人机协同 | 数模与时序预测 | paper | 数模-数据分析与决策、数模-预测与评估 | 2026-08-31 | 已引 |
| arxiv-2609.01126 | When Does Online Adaptation Pay on the Edge? A Leakage-Free Evaluation of Warmup, Learning-Rate Selection, and Resource Trade-offs for Time-Series Forecasting | 时序预测、在线适应、边缘计算、评测方法学 | 数模与时序预测 | paper | 数模-预测与评估、Kaggle-竞赛、黑客松-数据与算法 | 2026-09-01 | 已引 |
| arxiv-2609.02068 | DynG-Diff: A State-Aware Dynamic Guidance Diffusion Framework for Probabilistic Time Series Forecasting | 时序预测、扩散模型、概率预测 | 数模与时序预测 | paper | 数模-预测与评估、Kaggle-竞赛 | 2026-09-02 | 已引 |
| arxiv-2609.02093 | Compositional Spectral Prompts for LLM-based Online Time Series Forecasting | 时序预测、LLM、在线学习、频域提示 | 数模与时序预测 | paper | 数模-预测与评估、Kaggle-竞赛 | 2026-09-02 | 已引 |
| arxiv-2609.02783 | EarlyEval：agent 评测省钱器（早期结果预测+置信早停，HF 112 赞） | LLM agent、评测提效、早停预测 | 创新创业大赛、黑客松与数据竞赛 | demo | 黑客松-数据与算法、双创-文书与申报 | 2026-09-01 | 已引 |
| arxiv-2609.03340 | Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory | LLM agents、分布式系统、内存一致性 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-09-03 | 已引 |
| arxiv-2609.03383 | TIGPO: Temporal Instance-Graph Policy Optimization for Long-Horizon LLM Agents | LLM agents、强化学习、credit assignment | 黑客松与数据竞赛 | paper | Kaggle-竞赛 | 2026-09-03 | 已引 |
| arxiv-2609.03923 | Speak for Me: Giving LLMs the Situational Awareness to Participate in a Meeting | LLM agents、多智能体协作、对话系统 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-09-03 | 已引 |
| arxiv-2609.03937 | RATL: Learning from Retrieved Residuals for Robust Multivariate Time-Series Forecasting | 时序预测、检索增强、残差学习 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-预测与评估、Kaggle-竞赛 | 2026-09-03 | 已引 |
| arxiv-2609.04159 | SENTINEL-RL: Offloading Topological Reasoning from LLM Agents in the Security Operations Center | LLM agents、网络安全、图神经网络、强化学习 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-09-03 | 已引 |
| arxiv-2609.04170 | A Case Study on Emergent Cheating and Whistleblowing in Autonomous Research Swarms | LLM agents、多智能体系统、AI 安全 | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-09-03 | 已引 |
| arxiv-2609.09153 | Procedural Graphs：用自进化程序图给 LLM Agent 装显式『怎么做』知识（步骤级引导） | LLM agents | 黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-09-08 | 已引 |
| arxiv-2609.10357 | tsfm-bench：TSFM 的领域熟悉度陷阱（时间hold-out除不掉预训练记忆） | 时序基础模型、评测方法学、数据污染 | 数模与时序预测 | paper | 数模-预测与评估、Kaggle-竞赛 | 2026-09-09 | 已引 |
| arxiv-2609.11135 | SolCloudLLM：天空图像×时序双向融合的 LLM 光伏/辐照度短临预测 | 时序预测、多模态融合、新能源预测 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-09-10 | 已引 |
| arxiv-2609.13345 | Beyond Point Forecasts：概率预测方法统一版图（时序+时空综述） | 概率预测、综述、不确定性量化 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-09-11 | 已引 |
| arxiv-2609.13789 | PPDL：Weibull 物理先验×深度学习的工业用户留存率预测（ICDM 2026） | 时序预测、用户留存、机理数据混合建模 | 数模与时序预测 | paper | Kaggle-竞赛、数模-数据分析与决策 | 2026-09-12 | 已引 |
| arxiv-2609.13956 | Tabby：全开源配方时序基础模型（145M 三合一骨干+冻结prompt-tuning） | 时序基础模型、概率预测、开源配方 | 数模与时序预测 | demo | 数模-预测与评估、Kaggle-竞赛 | 2026-09-12 | 已引 |
| arxiv-2609.16309 | Agentic Search Spaces for Tabular Machine Learning | LLM agents、表格机器学习、超参数优化、AutoML | 黑客松与数据竞赛 | paper | Kaggle-竞赛、黑客松-数据与算法 | 2026-09-14 | 已引 |
| arxiv-2609.16804 | SOTER: A Generative Time-Series Foundation Model for Wearable Human Physiological Signals | time series foundation model、可穿戴生理信号、不规则采样、时序插补 | 数模与时序预测 | demo | 数模-预测与评估、数模-数据分析与决策 | 2026-09-15 | 已引 |
| arxiv-2609.17895 | TabPFN-3.5：表格基础模型新旗舰（时序/非i.i.d./多模态列全面扩张） | 表格基础模型、时序预测、AutoML | 数模与时序预测 | product | 数模-预测与评估、Kaggle-竞赛 | 2026-09-15 | 已引 |
| arxiv-2609.20625 | Chronicle：agent 失败的 cut-point 回放回归测试（零模型调用进 CI） | LLM agent、回归测试、record-replay | 创新创业大赛、黑客松与数据竞赛 | demo | 黑客松-数据与算法、双创-文书与申报 | 2026-09-17 | 已引 |
| arxiv-2609.21381 | KG-Chronos-2：冻结 TSFM 做水利仿真代理——知识图谱检索+残差解码降 14% RMSE | 时序基础模型、物理仿真代理、知识图谱检索、水文预测 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-09-18 | 已引 |
| arxiv-2609.21573 | Micro-Collaborative Poisoning: A Distributed Attack on RAG Systems | retrieval augmented generation、RAG 安全、对抗攻击 | 创新创业大赛、黑客松与数据竞赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2026-09-18 | 已引 |
| arxiv-2609.21666 | Samsone：99M/134M/356M 三档开源小型音频语言模型（Interspeech 2026，checkpoint 可下载 + ExecuTorch 移动端 + Android 应用） | on-device inference、音频理解、audio language model | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-09-18 | 已引 |
| arxiv-2609.22573 | Zero-Trust Authorization and Discovery for Enterprise MCP | LLM agents、MCP 安全、零信任授权 | 创新创业大赛、黑客松与数据竞赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2026-09-18 | 已引 |
| arxiv-2609.22836 | Time-aware Patch 混合注意力：不规则多变量时序的零样本预测（附 30B 观测 VersaTSA 语料） | 时序预测、时序基础模型、不规则采样 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-09-19 | 已引 |
| arxiv-2609.22977 | CASP-LLM：覆盖感知的提示选择——usage 正则替代相似度 top-K 检索（官方代码已放） | 时序预测、检索增强、提示选择、LLM | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | demo | 数模-预测与评估、黑客松-数据与算法 | 2026-09-19 | 已引 |
| arxiv-2609.23257 | CTRL：LLM 只做控制器的时序预测——误差分解控制信号+残差解码+免标签测试时自适应 | 时序预测、LLM 控制器、测试时自适应、非平稳 | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | paper | 数模-预测与评估 | 2026-09-20 | 已引 |
| arxiv-2609.24115 | EDGEGEN: Improving Tool-Calling Agents Beyond Happy Paths with Synthetic Edge Case Generation | LLM agents、数据合成与评估 | 创新创业大赛、黑客松与数据竞赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2026-09-21 | 已引 |
| arxiv-2609.24165 | APEXA: Execution-Integrity Enforcement for Multi-Agent LLM Automation of Synchrotron Data Reduction | LLM agents、执行完整性、科学数据自动化 | 创新创业大赛、黑客松与数据竞赛 | demo | 黑客松-数据与算法、双创-文书与申报 | 2026-09-21 | 已引 |
| arxiv-2609.24967 | Emergent Collusion in Long-Horizon LLM Agent Interaction | LLM agents、多智能体安全、涌现合谋 | 创新创业大赛、黑客松与数据竞赛 | demo | 黑客松-数据与算法、双创-文书与申报 | 2026-09-21 | 已引 |
| arxiv-2609.24972 | RRSI: Regularized Recursive Self-Improvement of Agent Harnesses | LLM agents、智能体自我改进、agent harness 工程 | 创新创业大赛、黑客松与数据竞赛 | demo | 黑客松-数据与算法、双创-文书与申报 | 2026-09-21 | 已引 |
| arxiv-2609.32689 | FASE：情景记忆+在线策略学习的自进化时序预测 agent（GIFT-Eval nMAE -9.1%） | 时序预测、LLM agent、持续学习 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-09-26 | 已引 |
| arxiv-2609.39386 | When Not How Much：TSFM 点预测对稀疏事件近乎无用——线性探针与分位数平均才是正解 | 时序基础模型、评估方法、稀疏事件 | 数模与时序预测 | paper | Kaggle-竞赛、数模-预测与评估 | 2026-09-30 | 已引 |
| arxiv-2609.39741 | Nixtlaverse：统计/ML/神经预测统一开源生态（M5 全层级实证，Apache-2.0） | 时序预测、开源工具生态、层级预测、评估方法 | 数模与时序预测 | product | 数模-预测与评估、Kaggle-竞赛 | 2026-09-30 | 已引 |
| arxiv-2610.00906 | ActiveSaddler：harness 自动优化的课程层——失败模式臂 + 非平稳 bandit 场景调度 | LLM agents、agent harness 工程、curriculum learning | 创新创业大赛、黑客松与数据竞赛 | demo | 黑客松-数据与算法、双创-文书与申报 | 2026-10-01 | 已引 |
| arxiv-2610.00978 | TS-Router：基础模型表示做路由——generalist 表示 + specialist 异常检测器 | 时序异常检测、时序基础模型、模型路由 | 数模与时序预测 | paper | Kaggle-竞赛、数模-预测与评估 | 2026-10-01 | 已引 |
| arxiv-2610.01256 | DeFA：依赖图引导的 LLM Agent 失败归因——事件依赖图+失败传播图定位决定性错误 | LLM agents、失败归因、多智能体系统调试 | 创新创业大赛、黑客松与数据竞赛 | paper | 黑客松-数据与算法 | 2026-10-01 | 已引 |
| arxiv-2610.02002 | Mem++：组织级 LLM Agent 的非破坏式记忆——写时零压缩、读时按时间线选择 | LLM agents、agent memory、时序知识问答 | 创新创业大赛、黑客松与数据竞赛 | demo | 黑客松-数据与算法、双创-文书与申报 | 2026-10-01 | 已引 |
| arxiv-2610.02038 | Mimir：物理模型不可变+双时间尺度修复的 LLM Agent 长程灌溉控制 | LLM agents、物理约束控制、智慧农业 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2026-10-01 | 已引 |
| arxiv-2610.02058 | SimpleTimeBench：TSFM 基础时序逻辑零样本盲点诊断基准（微调损此顾彼） | 时序基础模型、评估基准、诊断 | 数模与时序预测 | paper | 数模-预测与评估 | 2026-10-01 | 已引 |
| bai2024DelayAwareCooperativeTask | 多UAV边云协同的时延感知任务卸载 | 移动边缘计算、任务卸载、Lyapunov 优化 | 创新创业大赛、黑客松与数据竞赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| chang2024NearoptimalUAVDeployment | 时延约束IoT采集的最少UAV部署（GPUDA） | 无人机部署、组合优化、物联网数据采集 | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| chen2024AdaptiveBitrateVideo | UAV辅助MEC的码率视频鲁棒缓存（DRO） | 移动边缘计算、边缘缓存、分布鲁棒优化 | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| chen2025EneOveCom | 部分参与式UAV空中计算能效优化 | UAV 辅助边缘计算、空中计算、数据聚合 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2025-01-01 | 已引 |
| chen2025JointTrajectoryOptimization | Lyapunov辅助DRL的UAV轨迹与资源联合优化（JTORA） | 无人机轨迹优化、资源分配、深度强化学习 | 创新创业大赛、黑客松与数据竞赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| chen2025MultiuserTaskOffloading | JULTO：UAV-LEO卫星边缘多用户博弈卸载 | 移动边缘计算、博弈论、空天地一体网络 | 数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| chen2025TaskOffloadingResource | 博弈论驱动的UAV边缘卸载与资源定价 | 移动边缘计算、博弈论、资源定价 | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| chen2025TypeFlyLowlatencyDrone | TypeFly：低时延大模型无人机规划 | 大语言模型、无人机规划、具身智能系统 | 创新创业大赛、黑客松与数据竞赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| cong2024ParallEdgeExploitingComputingMobility | ParallEdge：移动边缘服务器的计算-移动并行范式 | 移动边缘计算、路径规划、任务调度 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| cui2024DataValueBased | 数据价值驱动的UAV群异步联邦学习 | 联邦学习、UAV 集群、客户端调度 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| dabiri2025NovelMRRUAVbasedRelay | MRR-UAV光网络编码双向中继 | 自由空间光通信、UAV 中继、网络编码 | 创新创业大赛 | paper | 双创-文书与申报 | 2025-01-01 | 已引 |
| dai2023MultiAgentDeepReinforcement | MADRL多机协同波束赋形（HATRPO-UCB） | 多智能体强化学习、协同波束赋形、UAV 通信 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| dai2024UAVAssistedTaskOffloading | Lyapunov在线UAV支援车联网过载卸载 | 移动边缘计算、Lyapunov 优化、车联网 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2024-01-01 | 已引 |
| dou2025SchedulingDroneMobile | 无人机-移动充电车混合动作协同调度（HaDMC） | 混合动作强化学习、充电调度、无人机持续作业 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| fu2022Energyefficient3DData | 多UAV三维节能数据采集（3DM） | 移动群智感知、三维轨迹优化、UAV 数据采集 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2022-01-01 | 已引 |
| gao2024ServiceExperienceOriented | 服务体验比导向的缓存UAV-MEC协同计算 | 边缘计算、服务缓存、分式优化 | 创新创业大赛、数模与时序预测 | paper | 数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| gao2025CSMAACMultiagentReinforcement | CSMAAC：部分可观测多UAV群智感知的安全协同飞控 | 多智能体强化学习、无人机协同控制、安全强化学习 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2025-01-01 | 已引 |
| gao2025TransferLearningJoint | PTMF-MAAC：大规模UAV-MEC的策略迁移联合轨迹卸载 | 迁移学习、多智能体强化学习、移动边缘计算 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2025-01-01 | 已引 |
| gaydamaka2024DynamicTopologyOrganization | 虚拟坐标驱动的自主UAV蜂群拓扑组织与维护 | 无人机自组网、拓扑组织、地理路由 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2024-01-01 | 已引 |
| gh-1173591564_Dynamics-memory | Dynamics-memory：值动力学 + 矛盾裁决的 LLM Agent 有界长期记忆层（含因果回放评测与负结果消融） | LLM agents、agent memory | 创新创业大赛 | demo | 双创-文书与申报、黑客松-数据与算法 | 2026-09-15 | 已引 |
| gh-BootLoops-ai_bootloops | BootLoops 1.0：给 LLM Agent 用的可认证高精度计算工具箱（49 包自检 + agent 协议技能库） | LLM agents、scientific computing、可信数值计算 | 创新创业大赛、黑客松与数据竞赛 | demo | 黑客松-数据与算法、双创-文书与申报 | 2026-10-01 | 已引 |
| gh-BraxisAI_braxis-blueprint | braxis-blueprint: 零预算免费 LLM 通道路由与自动化运维的实战脚本集 | LLM agents | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-23 | 已引 |
| gh-JordyZomer_lemmalog | Lemmalog：把 LLM Agent 记忆做成可证明的演绎数据库（Rust Datalog 引擎 + MCP 共享大脑） | LLM agents | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-27 | 已引 |
| gh-QwenLM_E-CommerceBench | E-CommerceBench：18 个 LLM Agent 各持 ¥10 万经营 365 天模拟网店的长程评测环境 | LLM agents | 黑客松与数据竞赛 | demo | 黑客松-数据与算法、数模-数据分析与决策 | 2026-08-26 | 已引 |
| gh-UditAkhourii_cdaf | CDAF: 视频的 agent 可读文本边车格式——一次生成、逐次省 token | LLM agents、多模态视频理解 | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-26 | 已引 |
| gh-Vistyy_nopus | nopus: 编码 agent 回复的确定性散文质量门 | LLM agents、输出质量评测 | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-15 | 已引 |
| gh-Zyrexnn_Cybermes | Cybermes: 自主进攻安全/赏金自动化 Agent 框架 | LLM agents、网络安全自动化 | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-19 | 已引 |
| gh-agents-universe_agents-universe | Agents Universe：知识条目驱动的企业级多角色 Agent 平台（无向量检索的项目记忆） | LLM agents | 黑客松与数据竞赛 | demo | 黑客松-数据与算法、数模-数据分析与决策 | 2026-08-18 | 已引 |
| gh-buddy_minesweeper | Minesweeper：九模型同盘同时钟同工具层的 LLM Agent 扫雷竞速基准 | LLM agents、agent 评测基准 | 创新创业大赛 | demo | 黑客松-数据与算法、双创-文书与申报 | 2026-09-21 | 已引 |
| gh-dreamers-laboratory_timeseries-atlas | Time Series Atlas：现代时序预测架构活地图（每篇一个可跑最小实现 + 基线纪律） | time series forecasting | 数模与时序预测 | demo | 数模-预测与评估、Kaggle-竞赛 | 2026-09-02 | 已引 |
| gh-hoplogic_hop3 | hoplogic/HOP 3.0：HopSpec 任务规约语言 + HopJIT 引擎强制的受控 agent 执行 | LLM agent、任务规约语言、执行引擎 | 创新创业大赛 | demo | 双创-文书与申报 | 2026-09-11 | 已引 |
| gh-joe960913_Jixu | Jixu：TypeScript 持久化单 Agent Harness（事件溯源 Thread，可恢复/重放/分叉） | LLM agents | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-18 | 已引 |
| gh-kyky2347_ALTA | ALTA：多 LLM Agent 自治研究型虚拟交易平台（证据优先 + 可回放影子账本） | LLM agents | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-27 | 已引 |
| gh-memovai_mimimodel | MimiModel: $5 ESP32-S3 上的全离线工具调用 LLM 引擎（单文件 C） | on-device inference、LLM agents | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-16 | 已引 |
| gh-only-cli_oc | oc (only-cli): 把任意网站压缩成 AI agent 可浏览的紧凑 CLI | LLM agents、retrieval augmented generation | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-18 | 已引 |
| gh-rome-os_rome | Rome: 面向人机协作的 Agentic OS 与可安装 App 模型 | LLM agents、agent 工程化 | 黑客松与数据竞赛 | product | 黑客松-数据与算法 | 2026-08-23 | 已引 |
| gh-squall01337_mixamo-llm-mocap | mixamo-llm-mocap: 视频到 Mixamo 角色动画的 agent 可操作全管线 | LLM agents、3D 动画与动作捕捉 | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-17 | 已引 |
| gh-wolfiesch_omp-best-of | omp-best-of: Best-of-N 候选 + LLM-as-a-Verifier 择优的编码 agent 编排插件 | LLM agents | 黑客松与数据竞赛 | demo | Kaggle-竞赛 | 2026-08-18 | 已引 |
| gh-zachsaw_graphify-csharp | graphify-csharp：给 LLM 编码 agent 的编译器级 C# 语义导航（Rider 语义切片的无头导出） | LLM agents、代码智能、开发者工具 | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-09-08 | 已引 |
| gong2024Energyefficient3DUAV | 最少UAV数的三维节能地面节点接入 | 三维路径规划、能耗优化、组合优化 | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、双创-文书与申报、黑客松-数据与算法 | 2024-01-01 | 已引 |
| gong2025JointlyOptimizingEnergy | 多UAV三维区域覆盖的能量-时间双目标优化 | 区域覆盖、多目标优化、能耗建模 | 创新创业大赛、数模与时序预测 | paper | 数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| gui2024CoverageProbabilityThroughput | mmWave与Sub-6GHz融合多UAV灾害网络的覆盖-吞吐联合优化 | 无人机通信网络、覆盖优化、深度强化学习 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2024-01-01 | 已引 |
| guo2024JointOptimizationTrajectory | 多UAV主动窃听的干扰功率与轨迹联合优化 | 物理层安全、协同干扰、强化学习 | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| guo2025MightyLongrangeHighthroughput | Mighty：面向无人机的远距离高吞吐回散视频回传 | 反向散射通信、无人机系统、跨层协同设计 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2025-01-01 | 已引 |
| hamdi2025DroneasaserviceResearchChallenges | DaaS：无人机即服务研究挑战与方向综述 | 无人机服务计算、服务编排、综述方法学 | 创新创业大赛、数模与时序预测 | paper | 双创-文书与申报、数模-数据分析与决策 | 2025-01-01 | 已引 |
| han2024CollaborativeRoutePlanning | 灾害响应UAV-工人-车辆异构协同路径规划 MANF-RL-RP | 群智感知、多智能体强化学习、路径规划 | 黑客松与数据竞赛、数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| han2024JointAssociationDeployment | 多UAV大规模MEC关联-部署-轨迹联合优化 | UAV 辅助移动边缘计算、部署与轨迹优化 | 创新创业大赛、黑客松与数据竞赛、数模与时序预测 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| hao2024JointTaskOffloading | 任务优先级感知多UAV协同MEC潜空间DRL联合卸载 | UAV 辅助边缘计算、深度强化学习、资源分配 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| hao2025ReliabilityawareOptimizationTask | 可靠性感知UAV辅助边缘计算任务卸载优化 | UAV 辅助边缘计算、可靠性建模、深度强化学习 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| he2024BalancingTotalEnergy | SAGIN数据卸载的总能耗与平均工期权衡 | 空天地一体网络、多目标优化、任务调度 | 数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| he2024OnlineJointOptimization | UAV-MEC QoE最大化的Lyapunov在线联合优化 | UAV 辅助移动边缘计算、Lyapunov 在线优化 | 黑客松与数据竞赛、数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| hoang2024FiniteBlockLength | 有限块长NOMA多用户配对UAV系统性能分析与优化 | 无人机通信、NOMA、有限块长 URLLC | 数模与时序预测、创新创业大赛 | paper | 数模-预测与评估、双创-文书与申报 | 2024-01-01 | 已引 |
| hoang2025Adaptive3DPlacementa | 6G空中小蜂窝多UAV基站自适应三维部署 | UAV 基站部署、深度强化学习 | 黑客松与数据竞赛、数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| hou2025AgeInformationawareMultiobjective | AoI感知异构UAV-USV-UUV水下目标围捕多目标优化 | 异构无人系统、信息年龄 AoI、多智能体强化学习 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| huang2024DynamicTaskOffloading | UVEC 多 UAV 任务卸载（SNC+Consensus ADMM） | 移动边缘计算、任务卸载、分布式优化 | 数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| huang2025ASSUMEOptimalAlgorithm | ASSUME：实测能耗驱动的无人机高度-速度联合调度 | UAV 能耗建模、高度-速度调度、数据采集 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| huang2025FastUAVTrajectory | FedX：RIS 辅助 UAV 轨迹规划的联邦加速学习 | RIS 辅助通信、轨迹规划、强化学习加速 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、Kaggle-竞赛、双创-文书与申报 | 2025-01-01 | 已引 |
| ji2024DecoupledAssociationRate | RSMA 解耦关联的 UAV 蜂窝 MADRL 优化 | UAV 辅助蜂窝网络、速率分裂多址、多智能体强化学习 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| jia2024EnergyTimeTradeoff | 多 UAV IoT 数据采集时间-能量权衡（MSMOACO） | 多目标优化、UAV 数据采集、蚁群优化 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| jia2025DistributionallyRobustOptimization | UAV-HAP 分层空中 MEC 的 CVaR 分布鲁棒优化 | 空中边缘计算、分布鲁棒优化、资源分配 | 数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| jin2025ResourceefficientContentSharing | UAV 命名数据网络的合约激励内容共享（GS 匹配） | 命名数据网络、机制设计、资源共享 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2025-01-01 | 已引 |
| kang2024AutonomousMultidroneRacing | Sim-to-Real 多无人机自主竞速（IPPO） | 多智能体强化学习、无人机竞速、Sim-to-Real | 黑客松与数据竞赛 | paper | Kaggle-竞赛、黑客松-数据与算法 | 2024-01-01 | 已引 |
| karmakar2024BlockchainBasedDistributedIntelligent | SwarmAuth：区块链+动态聚类的UAV蜂群分布式认证 | 无人机蜂群安全、区块链认证、动态聚类 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2024-01-01 | 已引 |
| karmakar2024NovelFederatedLearningBased | FairLearn：联邦学习驱动的安全公平UAV-MEC控制 | 联邦学习、移动边缘计算、公平性优化 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| kharjana2025SecuringAutonomousUAV | 链上阈值多签密钥管理的自主UAV集群安全 | 无人机集群安全、区块链、密钥管理 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2025-01-01 | 已引 |
| khochare2024ImprovedAlgorithmsCoScheduling | UAV机队航线与机载边缘分析共调度（MSP） | 任务调度、边缘计算、无人机路径规划 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| kumari2025MaximizingServiceProviders | MaDRL+图着色的多UAV 5G服务利润最大化 | 多智能体强化学习、图着色、无线资源分配 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2025-01-01 | 已引 |
| lee2025AdaptiveStabilizationControl | BAASC：浮力辅助四旋翼的DRL自适应稳定控制 | 深度强化学习、姿态控制、原型验证 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2025-01-01 | 已引 |
| li2024MultiObjectiveOptimizationUAV | 双侧虚拟天线阵列UAV辅助IoT多目标优化（EMSSA） | UAV 辅助 IoT、协作波束形成、多目标优化 | 创新创业大赛、黑客松与数据竞赛、数模与时序预测 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| li2024SecureOffloadingAdversarial | 对抗式MARL抗智能窃听的UAV-MEC安全卸载（ARL-MAPPO） | UAV 辅助 MEC、对抗式多智能体强化学习、物理层安全 | 黑客松与数据竞赛、数模与时序预测 | paper | 黑客松-数据与算法、数模-数据分析与决策、Kaggle-竞赛 | 2024-01-01 | 已引 |
| li2025AnchorNovelModeling | Anchor：Delaunay三UAV协同卸载的随机几何建模 | UAV 辅助 MEC、随机几何、协同卸载建模 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-预测与评估、黑客松-数据与算法 | 2025-01-01 | 已引 |
| li2025CooperativeNonorthogonalMultiple | 空地多UAV索引调制协作NOMA（MCU/MCCU-NOMA-IM） | 空地通信、索引调制、协作 NOMA | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| li2025DroneMADroneMobility | DroneMA：移动性一致性驱动的无人机AI欺骗检测 | 无人机安全、时间序列异常检测、物理层鉴别 | 黑客松与数据竞赛、数模与时序预测、创新创业大赛 | paper | Kaggle-竞赛、数模-预测与评估、双创-文书与申报 | 2025-01-01 | 已引 |
| li2025DynamicRoutingMechanism | LAMAIC：边缘缓存UAV群网络的动态路由与负载分配 | UAV 群网络、延迟容忍网络、边缘缓存 | 创新创业大赛、黑客松与数据竞赛、数模与时序预测 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| li2025ExploringRobustnessHierarchical | HFL-OD：抗毁伤的UAV集群层次化联邦目标检测 | 联邦学习、UAV 集群、目标检测 | 黑客松与数据竞赛、数模与时序预测、创新创业大赛 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| li2025FederatedMetalearningBased | GFL-PEARL：联邦元学习驱动的UAV辅助VEC能时延权衡卸载 | 联邦元学习、计算卸载、UAV 辅助车边缘计算 | 创新创业大赛、黑客松与数据竞赛、数模与时序预测 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| li2025TamingEventCameras | BioDrone：仿生事件相机无人机避障系统（FPGA软硬协同） | 事件相机、无人机避障、软硬件协同设计 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| li2025UAVassistedMicroserviceMobile | 灾后医疗救援UAV微服务MEC架构（Transformer资源管理） | UAV 辅助 MEC、微服务架构、智能资源调度 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| lin2024LyapunovbasedApproachJoint | LI2：灾后 PoI 及时监测的 UAV AoI 路径优化 | 信息年龄 AoI、路径优化、深度强化学习 | 黑客松与数据竞赛、数模与时序预测、创新创业大赛 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| liu2025DelaysensitiveGoodsDelivery | FH-MDP：多任务无人机时敏配送与在途感知的阈值策略 | 低空物流、有限时域 MDP、在线决策 | 创新创业大赛、黑客松与数据竞赛、数模与时序预测 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| liu2025HybridOptimizationFramework | UaMCS 混合优化框架：信任约束下的全局 AoI 最小化 | UAV 群智感知、AoI 优化、深度强化学习 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| liu2025MultiUAVassistedMECInternet | SC-MA-TD3：抗干扰多模态语义通信的多UAV车联网MEC | 语义通信、多智能体强化学习、UAV 辅助 MEC | 创新创业大赛、黑客松与数据竞赛、数模与时序预测 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| liu2025ResourceAllocationAdaptive | UAV辅助ISAC自适应波束对齐的感知-通信联合资源分配 | 一体化感知与通信、资源分配、深度强化学习 | 创新创业大赛、黑客松与数据竞赛、数模与时序预测 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| liu2025RobustTopologyRecovery | RTRA/CRTRA：UAV蜂群鲁棒拓扑恢复 | UAV 蜂群、拓扑恢复、代数连通度 | 创新创业大赛、黑客松与数据竞赛、数模与时序预测 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| liwang2021LetsTradeFuture | CoDetect：隐私保护的UAV群协同异常检测 | 协同异常检测、隐私保护、无人机集群安全 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2024-01-01 | 已引 |
| mao2025UAVassistedCommunicationsSAGINISAC | SAGIN-ISAC 移动用户跟踪与鲁棒波束赋形 | 空天地一体化网络、通感一体化、鲁棒波束赋形 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-预测与评估、黑客松-数据与算法 | 2025-01-01 | 已引 |
| mittal2024DeploymentCostawareUAV | DCE：部署成本效率驱动的空地一体UAV与BS协同 | 空地一体网络、部署优化、联盟博弈 | 创新创业大赛、黑客松与数据竞赛、数模与时序预测 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| nabi2025JointOffloadingDecision | JOUR：UAV与HAP层次化空中计算的匹配-卸载联合决策 | 层次化空中计算、匹配博弈、深度强化学习 | 创新创业大赛、黑客松与数据竞赛、数模与时序预测 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| nguyen2024DilemmaReliabilitySecurity | UAV能量采集中继的可靠性-安全性双目标优化 | UAV 通信、物理层安全、多目标优化 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| ning2024MultiAgentDeepReinforcement | MUTO：差异化服务下多UAV辅助MEC的MARL轨迹优化 | UAV 辅助边缘计算、多智能体强化学习、轨迹优化 | 创新创业大赛、黑客松与数据竞赛、数模与时序预测 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| ning2025JointOptimizationData | MCDRL：无线供能IoT的UAV数据采集与轨迹联合优化 | 无线供能物联网、轨迹规划、多智能体强化学习 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2025-01-01 | 已引 |
| pan2025CooperativeUAVmountedRISsassisted | INSGA-II-CDC：协同UAV-RIS能效通信三目标优化 | UAV-RIS 通信、多目标优化、能效设计 | 黑客松与数据竞赛、数模与时序预测 | paper | 黑客松-数据与算法、数模-数据分析与决策 | 2025-01-01 | 已引 |
| panahi2024ReliableEnergyEfficientUAV | 成本感知的激光与可再生能源UAV通信供能优化 | UAV 通信、能量采购优化、无线供能 | 数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| qian2024PathPlanningAlgorithm | 固定翼农田监测无人机的节能覆盖路径规划 | 精准农业、覆盖路径规划、固定翼无人机 | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | paper | 双创-文书与申报、数模-数据分析与决策、黑客松-数据与算法 | 2024-01-01 | 已引 |
| qin2022MultiagentReinforcementLearning | CTDE多智能体空中计算三层卸载 | 移动边缘计算、多智能体强化学习、空天地一体网络 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2022-01-01 | 已引 |
| qin2025MultiagentReinforcementLearning | PFSAC：异构UAV通信的个性化联邦抗干扰策略学习 | 抗干扰通信、个性化联邦强化学习、博弈论 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| qiu2024IntegratedHostContentCentric | IHCR：UAV蜂群主机-内容中心融合路由 | FANET 路由、内容中心网络、UAV 蜂群 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| ren2024IntelligentAdaptiveGossipBased | BDGN：UAV-MEC的智能自适应Gossip广播协议 | UAV-MEC、广播协议、深度图网络 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| ren2025AeroEchoAgriculturalLowpower | AeroEcho：空中激励的农业低功耗广域回散 | 低功耗广域回散通信、农业物联网、无人机系统 | 创新创业大赛、黑客松与数据竞赛、数模与时序预测 | paper | 双创-文书与申报、黑客松-数据与算法、数模-数据分析与决策 | 2025-01-01 | 已引 |
| rizvi2025MonitoringInterdroneService | 面向韧性运行的无人机间服务干扰监测（PIS 评估） | 无人机服务系统、时空数据分析、服务韧性 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2025-01-01 | 已引 |
| roy2025ServHUServiceHandoff | Serv-HU：UaaS 平台服务接力与最优定价机制 | 无人机服务计算、平台机制、收益定价 | 创新创业大赛、数模与时序预测 | paper | 双创-文书与申报、数模-数据分析与决策 | 2025-01-01 | 已引 |
| shao2024DeepReinforcementLearningbased | 抗干扰UAV辅助MEC的PER-MATD3联合资源管理 | 多智能体强化学习、移动边缘计算、抗干扰通信 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2024-01-01 | 已引 |
| shen2024SlicingBasedTaskOffloading | SAGIN车联网切片式任务卸载 | 网络切片、车联网、深度强化学习 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| shi2024TwoStageStrategyUAVenabled | 未知环境下UAV无线供能的搜索-补能两阶段策略 | 无线供能、路径规划、聚类 | 创新创业大赛、数模与时序预测 | paper | 双创-文书与申报、数模-数据分析与决策 | 2024-01-01 | 已引 |
| singh2024StableMatchingBased | 稳定匹配+图着色的UAV辅助WBAN联邦学习收益最大化 | 联邦学习、稳定匹配、无线资源分配 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2024-01-01 | 已引 |
| song2024AoIEnergyTradeoff | 空地协同MEC中AoI-能耗权衡的Pareto策略集学习 | 多目标强化学习、信息年龄、移动边缘计算 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2024-01-01 | 已引 |
| song2024EnergyefficientTrajectoryOptimization | 无线充电UAV辅助MEC的多目标RL轨迹优化（MORL-TER） | 多目标强化学习、轨迹优化、无线供能 | 数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| song2024MethodsAssignUAVs | IoT网络K覆盖与补能的UAV多时隙分配（MPC-MILP与MCTS） | 覆盖调度、能量管理、滚动优化 | 创新创业大赛、数模与时序预测 | paper | 数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| soorki2025CatchMeIf | 元强化学习驱动的LoRa无人机搜救轨迹控制 | UAV 轨迹优化、元强化学习、LoRa 搜救 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| sun2024AllskyAutonomousComputing | ASAP 无人机群全空域自主协同计算系统 | UAV 集群系统、协同推理、弹性调度 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| sun2024MultiobjectiveOptimizationMultiUAVassisted | 多UAV辅助MEC三目标联合优化（JTORATC） | UAV 辅助 MEC、多目标优化、凸优化 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2024-01-01 | 已引 |
| sun2024TwoTimescaleJoint | TJCCT 双时间尺度无人机辅助MEC联合优化 | UAV 辅助 MEC、双时间尺度优化、匹配与定价 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| sun2025AerialReliableCollaborative | EMOPPO-VLH：面向移动用户的空中协同可靠通信 | 无人机协同通信、多目标强化学习、协作波束赋形 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-预测与评估、黑客松-数据与算法 | 2025-01-01 | 已引 |
| sun2025JC5AServiceDelay | JC5A：空中MEC辅助工业CPS服务时延最小化 | 移动边缘计算、服务缓存、无人机轨迹优化 | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | paper | 双创-文书与申报、数模-数据分析与决策、黑客松-数据与算法 | 2025-01-01 | 已引 |
| tang2025DeepGraphReinforcement | 图强化学习双层求解UAV多用户安全通信 | 物理层安全、图神经网络、分层强化学习 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| tao2024MultiagentCooperationComputing | 多UAV空中计算的多智能体协同算力调度 | 空中计算、多智能体强化学习、无人机轨迹优化 | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| tian2024UAVAssistedWirelessCooperative | MA2T-DRL 应急编码缓存与功率联合优化 | 编码缓存、多智能体强化学习、应急通信 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| tlili2023NewHybridAdaptive | AHFFA 无人机故障与攻击混合检测框架 | 异常检测、时序深度学习、UAV 安全 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-预测与评估、Kaggle-竞赛、黑客松-数据与算法 | 2023-01-01 | 已引 |
| tong2023EnergyefficientUAVNOMAAided | 能效优先的UAV-NOMA海量连接覆盖 | UAV 通信覆盖、NOMA、能效优化 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2023-01-01 | 已引 |
| tun2025JointUAVDeployment | THz空天地网络UAV部署与资源联合优化 | 空天地一体网络、移动边缘计算、资源分配 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2025-01-01 | 已引 |
| wan2025MultimodalScaleNormalization | 视觉雷达融合UAV定位尺度归一化 | 多模态感知、无人机定位、小目标检测 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| wang2024BiobjectiveAntColony | 双目标蚁群优化的UAV-MEC轨迹与多阶段卸载 | UAV辅助MEC、多目标优化、蚁群算法 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| wang2024DecentralizedNavigationHeterogeneous | 异构联邦强化学习的UAV-MEC分布式导航 | 联邦强化学习、多UAV导航、移动边缘计算 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| wang2024EnsuringThresholdAoI | 阈值AoI约束的多UAV群智感知调度 | 信息年龄AoI、移动群智感知、多智能体强化学习 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-预测与评估、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| wang2024LSPSSConstructingLightweight | LSPSS空中计算轻量级隐私存储与共享 | 隐私计算、密文检索、空中计算 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2024-01-01 | 已引 |
| wang2024ResourceAllocationBlockchain | 区块链UAV-MEC的Stackelberg微分博弈资源定价 | 移动边缘计算、区块链、微分博弈 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| wang2024UAVassistedTargetTracking | Lyapunov空海协同目标跟踪与计算卸载 | 移动边缘计算、目标跟踪、Lyapunov 优化 | 数模与时序预测 | paper | 数模-预测与评估、数模-数据分析与决策 | 2024-01-01 | 已引 |
| wang2024WirelessPoweredMetaverse | 无线供能多设备多UAV联合调度（MURAL） | 无线供能、移动边缘计算、多任务强化学习 | 黑客松与数据竞赛、数模与时序预测、创新创业大赛 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| wang2025JointOptimizationBeamforming | GNN+SD3的UAV-RIS联合波束与轨迹优化 | UAV-mounted RIS、图神经网络、强化学习 | 黑客松与数据竞赛、数模与时序预测 | paper | 黑客松-数据与算法、数模-数据分析与决策 | 2025-01-01 | 已引 |
| wang2025JointPositioningComputation | PPO联合优化的多UAV放置与计算卸载 | 移动边缘计算、UAV部署优化、近端策略优化 | 黑客松与数据竞赛、数模与时序预测、创新创业大赛 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| wang2025JointTaskOffloading | ILCTS：动态UAV-MEC卸载与迁移模仿学习 | UAV 辅助边缘计算、模仿学习、任务调度 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| wang2025OptimizingJointSpeed | 低空巡检数据采集的联合速度与高度调度（SSF-ACO） | UAV数据采集、轨迹优化、蚁群算法 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| wang2025PracticalOptimizingUAV | 充电感知绕障UAV轨迹优化（近似保证） | UAV 轨迹优化、无线充电网络、近似算法 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| wang2025SecureBeamformingDeployment | RSMA-UAV安全波束赋形与三维部署联合优化 | UAV 通信、物理层安全、凸优化 | 数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| wang2025SmartShieldPrevent | Smart Shield：协同智能干扰反空中窃听 | 物理层安全、多智能体强化学习、友好干扰 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| wei2024HierarchicalNetworkSlicing | UAV无线网络两时间尺度分层切片 | 网络切片、UAV 通信、随机博弈 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| wu2024BeamformingPredictionBased | MRDDQN：UAV-RIS辅助THz波束预测 | THz 通信、UAV-RIS、深度强化学习 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-预测与评估、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| wu2024MACOptimizationProtocol | EC-CMAC：双感知协作UAV-MAC协议 | FANET、MAC 协议、协作传输 | 创新创业大赛、数模与时序预测 | paper | 双创-文书与申报、数模-数据分析与决策 | 2024-01-01 | 已引 |
| wu2024MultiUAVsNetworkDesign | 多UAV计算网络联合设计（VNF+流路由） | 多 UAV 网络、网络功能虚拟化、混合整数规划 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| wu2025ReconfigurableIntelligentSurface | TRAIL：RIS辅助UAV群智感知Transformer强化学习 | 移动群智感知、UAV-RIS、Transformer 强化学习 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-预测与评估、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| wu2025SecurityawareDesignsMultiUAV | 安全感知多UAV部署卸载与服务放置（OE-MATD3） | UAV 辅助边缘计算、物理层安全、多智能体强化学习 | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| wu2025TwostageDeepEnergy | IOPO：THz多UAV-MEC的IRS辅助卸载优化 | UAV 辅助边缘计算、THz 通信、智能超表面 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| xie2025BlockchainassistedLightweightCrossdomain | 双区块链轻量级跨域认证（多 UAV 网络） | 区块链认证、跨域信任、无人机网络安全 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| xu2024HolisticHybridService | H2S2：MEC无人机末端配送整体混合服务选择 | 无人机末端配送、边缘计算、服务选择 | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | paper | 双创-文书与申报、数模-数据分析与决策、黑客松-数据与算法 | 2024-01-01 | 已引 |
| xu2024RewardMaximizationDisaster | 灾害监测异构UAV奖励最大化调度（常数近似算法） | 异构无人机调度、定向问题、近似算法 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| xu2024SemanticawareUAVSwarm | 元宇宙UAV蜂群语义协同与信誉激励机制 | 语义通信、激励机制、无人机蜂群 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报、数模-数据分析与决策 | 2024-01-01 | 已引 |
| xu2025BlockchainempoweredGameTheoretical | 区块链赋能的UAV带宽分配Stackelberg博弈激励 | 区块链、博弈论、资源分配 | 数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| xu2025TrustenhancedGameIncentive | 信任增强的量子联邦学习Stackelberg激励机制 | 联邦学习、博弈论、信任评估 | 数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| xu2025WindawareServiceProvisioning | MW-DSP：多包裹无人机配送风感知服务供给 | 无人机物流、服务组合、不确定性优化 | 创新创业大赛、数模与时序预测 | paper | 数模-预测与评估、数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| xue2024MaximizingCoverageTargets | MaxCov：WRSN 多充电器目标覆盖最大化调度 | 无线可充电传感网、充电调度、目标覆盖 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| yang2023RobustTransitionTrajectory | 尾座式无人机鲁棒过渡轨迹优化（PCE不确定性传播） | 轨迹优化、鲁棒优化、不确定性量化 | 数模与时序预测 | paper | 数模-预测与评估、数模-数据分析与决策 | 2023-01-01 | 已引 |
| yang2024EnergyEfficientTransmission | 蜂窝连接UAV巡检能效传输（加权图定序+SCA/BCD） | 蜂窝连接无人机、巡检系统、能效优化 | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | paper | 双创-文书与申报、数模-数据分析与决策、黑客松-数据与算法 | 2024-01-01 | 已引 |
| yu2025HybridTransformerBased | HTransRL：空中走廊多UAV协同混合Transformer强化学习 | 多智能体强化学习、Transformer、无人机协同 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、Kaggle-竞赛、双创-文书与申报 | 2025-01-01 | 已引 |
| yuan2024DynamicEventtriggeredFaulttolerant | 具规定性能的动态事件触发容错编队协同控制 | 无人机编队控制、容错控制、事件触发 | 数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| yuan2025TrajectoryOptimizationPower | CATEN：多UAV空中基站轨迹与功率的通信型MARL联合优化 | UAV 通信、多智能体强化学习、资源分配 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| zema20243DTrajectoryOptimization | TRA/EDD：智慧城市多任务UAV补能设施与三维轨迹优化 | UAV 轨迹优化、MILP、智慧城市 | 数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| zeng2024A3DAdaptiveAccurate | A3D：边缘辅助无人机的自适应高精导航服务调度 | 边缘智能、无人机导航、服务调度 | 黑客松与数据竞赛、数模与时序预测、创新创业大赛 | paper | 黑客松-数据与算法、数模-预测与评估、双创-文书与申报 | 2024-01-01 | 已引 |
| zeng2025JointSecureMechanism | CNN-LSTM多任务学习的UAV团队FDI攻击联合防护 | 无人机安全、FDI 攻击检测、多任务学习 | 黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、数模-预测与评估、双创-文书与申报 | 2025-01-01 | 已引 |
| zhan2024InterferenceawareOnlineOptimization | 能量约束蜂窝多UAV的干扰感知在线吞吐优化 | 蜂窝连接无人机、干扰管理、凸优化 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2024-01-01 | 已引 |
| zhan2024TradeoffAgeInformation | AoI与运行时间双目标的多小区蜂窝UAV感知调度 | AoI、蜂窝连接无人机、深度强化学习 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-预测与评估、黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| zhan2025OnlineEnergyInterference | Lyapunov在线的蜂窝UAV动态目标跟踪能量干扰管理 | Lyapunov 优化、蜂窝连接无人机、目标跟踪 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| zhang2023JointTaskScheduling | 应急通信空中计算的任务调度与多UAV部署联合优化 | 空中计算、任务调度、UAV 部署优化 | 创新创业大赛、黑客松与数据竞赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2023-01-01 | 已引 |
| zhang2023RFSearchSearchingUnconscious | 非对称双视角多光谱立体成像的UAV自适应三维重建 | 多光谱成像、三维重建、无人机遥感 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2024-01-01 | 已引 |
| zhang2024TaskOffloadingTrajectory | 动态用户多UAV-MEC安全卸载与轨迹优化（JDPB） | UAV-MEC、物理层安全、轨迹优化 | 黑客松与数据竞赛、数模与时序预测 | paper | 黑客松-数据与算法、数模-数据分析与决策 | 2024-01-01 | 已引 |
| zhang2024UAVSwarmenabledCollaborative | 时间域合谋窃听下的UAV集群协同安全中继（UVAA+IMOGOA） | 协同安全中继、协作波束形成、多目标优化 | 黑客松与数据竞赛、数模与时序预测 | paper | 黑客松-数据与算法、数模-数据分析与决策 | 2024-01-01 | 已引 |
| zhang2025ImprovingDataCollection | 定向性感知链路模型驱动的UAV-LoRa数据采集（annulus+PreLoRa） | UAV 辅助数据采集、LoRa、实测链路建模 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2025-01-01 | 已引 |
| zhang2025LargeModelsAerial | 空中边缘大模型的边云三流协同演化 | 边缘智能、大模型、边云协同 | 创新创业大赛、黑客松与数据竞赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| zhang2025MultiobjectiveAerialCollaborative | GDMTD3：扩散模型驱动的多目标空中协同安全通信 | 无人机集群通信、物理层安全、扩散模型强化学习 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| zhang2025OptimizingMonitoringUtility | 兼顾监测效用与负效应的多UAV布设优化（PEACE） | UAV 部署优化、次模优化、监测效用建模 | 创新创业大赛、数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| zhang2025QuantumassistedOnlineTask | 量子辅助SATIN在线任务卸载与资源分配 | 空天地一体网络、量子优化、在线资源分配 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2025-01-01 | 已引 |
| zhao2024DesigningMultiUAVAided | 多UAV无线供能动态通信的分层强化学习（MAHDRL） | 无线供能通信、分层强化学习、UAV 轨迹优化 | 创新创业大赛、黑客松与数据竞赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |
| zhao2025JointContentCaching | UAV-MEC内容缓存-服务放置-任务卸载联合QoE优化 | UAV-MEC、边缘缓存、匹配博弈 | 黑客松与数据竞赛、数模与时序预测 | paper | 黑客松-数据与算法、数模-数据分析与决策 | 2025-01-01 | 已引 |
| zhao2025JointOptimizationTrajectory | UAV-MEC轨迹卸载缓存迁移的Lyapunov联合优化 | 移动边缘计算、在线优化、无人机轨迹 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| zhao2025MobileCollusiveEavesdroppers | 移动合谋窃听下UAV-MEC安全传输与计算协同优化（CSTC） | 无人机通信、物理层安全、移动边缘计算 | 数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| zhao2025MultiUAVCooperativeTask | 动态环境多UAV协同任务调度（TF-PPO+MOGS） | 多无人机协同、任务调度、稳定匹配 | 黑客松与数据竞赛、数模与时序预测 | paper | 黑客松-数据与算法、数模-数据分析与决策 | 2025-01-01 | 已引 |
| zheng2024ContentDeliveryPerformance | 缓存使能 UBS 内容交付性能解析（元宇宙用户） | 随机几何、边缘缓存、性能建模 | 数模与时序预测、创新创业大赛 | paper | 数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| zheng2024UAVSwarmAir | 迁移增强MARL的UAV蜂群空战机动决策 | 多智能体强化学习、迁移学习、无人机蜂群 | 黑客松与数据竞赛、数模与时序预测、创新创业大赛 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| zheng2025UAVSwarmenabledCollaborative | 低空经济灾后UAV蜂群协同通信两阶段优化 | 无人机自组网、协同波束形成、应急通信 | 数模与时序预测、创新创业大赛、黑客松与数据竞赛 | paper | 数模-数据分析与决策、双创-文书与申报、黑客松-数据与算法 | 2025-01-01 | 已引 |
| zhou2024FederatedDigitalTwin | 移动场景UAV联邦数字孪生框架 | 数字孪生、联邦学习、无人机协同感知 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2024-01-01 | 已引 |
| zhou2024JointOptimizationMobility | 可靠性保障空地通信的UAV移动性联合优化 | 空地通信、双层优化、能耗优化 | 数模与时序预测、创新创业大赛 | paper | 数模-预测与评估、双创-文书与申报 | 2024-01-01 | 已引 |
| zhou2024SymmetryaugmentedMultiagentReinforcement | 对称性增强MADRL的大规模UAV轨迹与用户调度（SymmQMIX） | 多智能体强化学习、等变网络、无人机轨迹 | 黑客松与数据竞赛、数模与时序预测、创新创业大赛 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2024-01-01 | 已引 |
| zhou2025DigitalTwinEmpowered | 数字孪生赋能的UAV辅助毫米波多跳V2X路由 | 数字孪生网络、毫米波 V2X 路由 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-数据分析与决策、黑客松-数据与算法 | 2025-01-01 | 已引 |
| zhou2025HaDTHardeningDigital | HaDT：UAV 工业物流分发的加固双数字孪生框架 | 数字孪生、UAV 物流、边缘智能 | 创新创业大赛、黑客松与数据竞赛、数模与时序预测 | paper | 双创-文书与申报、黑客松-数据与算法、数模-数据分析与决策 | 2025-01-01 | 已引 |
| zhou2025LLMQLLLMenhancedQlearning | LLM-QL：LLM增强Q学习的多无人机并行调度 | 大语言模型、强化学习、无人机调度 | 黑客松与数据竞赛、数模与时序预测、创新创业大赛 | paper | 黑客松-数据与算法、数模-数据分析与决策、双创-文书与申报 | 2025-01-01 | 已引 |
| zhou2025ReliabilityoptimalUAVassistedMobile | 面向可靠性的UAV辅助MEC联合资源与运动优化 | UAV 辅助边缘计算、无线可靠性建模 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| zhou2025UserPreferenceOriented | 用户偏好导向的UAV-MEC服务缓存与任务卸载 | 服务缓存、任务卸载、UAV 边缘计算 | 数模与时序预测、黑客松与数据竞赛、创新创业大赛 | paper | 数模-数据分析与决策、黑客松-数据与算法、双创-文书与申报 | 2025-01-01 | 已引 |
| zhou2025VerDTVersatileDigital | VerDT：工业 CPS UAV 物流的多功能双数字孪生框架 | 数字孪生、工业 CPS、UAV 物流 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法、Kaggle-竞赛 | 2025-01-01 | 已引 |
| zhu2023AttitudeControlNovel | 新型倾转翼UAV悬停姿态控制 | 倾转翼无人机、飞行控制 | 创新创业大赛、黑客松与数据竞赛 | paper | 双创-文书与申报、黑客松-数据与算法 | 2023-01-01 | 已引 |
| zhu2024CollaborativeReinforcementLearning | ZD-RL：协同强化学习的三维UAV跟踪与定位 | 多机协同强化学习、UAV 轨迹优化、无线定位 | 数模与时序预测、黑客松与数据竞赛 | paper | 数模-预测与评估、数模-数据分析与决策、黑客松-数据与算法 | 2024-01-01 | 已引 |
| zhu2024FissionSpectralClustering | FSC：FANET 无人机蜂群裂变谱聚类策略 | UAV 自组网、图聚类 | 创新创业大赛、黑客松与数据竞赛 | paper | 黑客松-数据与算法、双创-文书与申报 | 2024-01-01 | 已引 |

## 跑批记录

| 日期 | 类型 | 新增 | 更新 | 隔离 | 成本 | 说明 |
|---|---|---|---|---|---|---|
<!-- 成本列=分片数/token/墙钟（T4.3 起新行必填；旧行无此列属历史格式） -->
| 2026-09-16 | deep-small | 技术卡+2 拒3（SOTER 域专用生成式 TSFM 入族；Agentic Search Spaces 入库；评测/后训练/社会模拟三拒）+MLH GHW 翻转 ended | 0 | 3 | 1 分片/0.83M tok | 同日小增量轮（手动重复触发）：C4 重查/老化滚动距上轮 1.4h 无意义跳过 |
| 2026-09-16 | deep | 技术卡+4 拒1（FINESSE 同名异物识破）/重验 6 条（Shipaton 奖金 685K→740K 修正、宝可梦口径纠偏、ARC M1 放榜新发现、Qoder 系列信源劣化降级）/MLH 转活跃/C4 冠军方案未到窗口如实记录/P2 双族 survey 刷新（时序 25 卡、agents 34 卡） | 0 | 1 | 4 分片/约 7.5M tok/40min | comp 队列 2 条为已知日历刷新，归档不建条 |
| 2026-09-09 | deep | 技术卡+5（gh 代码型 4 张高星）/赛事+1（CALA Hacks）/重验 7 条（lablabai 转活跃、C4 转 ended+冠军三源）/小鹏期 winners 补构（名单图双视觉+1 深构） | 0 | 0 | 4 分片/约 8.3M tok/45min | 到期 watch：小鹏✅ C4✅；顺延：XPRIZE 9-25、GOAI 9-22 |
| 2026-08-29 | tech+comp | 赛事条目0 / 技术卡0 | 1 | 0 | 主会话直办1分片/约3min | /attack 预刷新：tech 72 拉取 0 新候选（台账去重）；comp 候选2=LA Hacks 复查（仍 JS SPA，待核维持）+MLH 聚合噪声弃置；子 agent 通道故障（Model provider not configured）降级主会话直办；CDEC 留尾继续待 browser-use 预抓；KB lint 101/101 |
| 2026-08-28 | tech+comp | 赛事条目1 / 技术卡0 | 0 | 1 | 1分片/约14min | /attack 审计后重开预刷新：UCLA AI Hackathon 入库但章程/奖项/AI 政策待 SPA 深核；MLH 赛季日历判聚合噪声；tech 73 拉取后 0 新候选；KB lint 101/101 |
| 2026-08-28 | refresh | 技术卡1 | 0 | 0 | 1分片/0.11M tok/2.5min | /attack 预刷新：tech 增量1条（UrbanGround 强映射入库）；comp 增量2条全噪（LA Hacks 与在队重复+锚点自指）已弃；LA Hacks 留 8-31 cron 消费 |
| 2026-08-28 | full | 赛事23三层全量：patterns 23/23、winners 12赛15文件、深构40+篇；技术卡 76/台账 133；surveys 4 族 | 6 波次/50+分片/约 55M tokens（D11 全量） |
| 2026-08-27 | tech+comp | 技术卡6 / 赛事条目3 | 0 | 0 | 首次真实跑批（T3-a）：arXiv 收紧查询后31候选→6卡；gh未登录按设计降级 |
| 2026-08-27 | discover | 赛事条目8 | 0 | 0 | 黑客松与数据竞赛冷启动（T4批次2）：4搜索分片→35候选→8入库+13留队列；Amazon Nova winners首样（6深构+1降级）；修正失真公告快照 |
| 2026-08-28 | tech+comp | 技术卡9 / 赛事条目12 | 0 | 0 | 5分片/19.8M tok/33min | 增量：comp消费discover留存13→12入库+1留尾(CDEC待预抓)；tech 160候选→9卡+100台账+50留队；两脚本缺陷待修(gh行内star限定词失效/build_index注释行断表) |
| 2026-09-16 | vault-distill | 173 | 0 | 0 | 26 hunter 分片 / ≈20.35M 子agent tokens / 墙钟约 95min | my_LLM_valut 一次性提炼（升级票05）：369 论文页→175 篇判定（173 收+2 拒入台账）；194 枢纽/概念页折叠进锚卡（4 个随拒收消亡）；bib 回填 DOI 覆盖 91%；citekey 错配 5 例实证修正；batch/vault-distill 分支合并回 deliver/kaggriculture-audit |
| 2026-09-20 | tech+comp | 赛事条目3 / 技术卡8 | 6 | 0 | 4分片/约36.6M子agent tokens/约39min | /kb-sync 主题跑批（用户任务：搜寻 2027-07 前出结果赛事+含金量证据）：数模分片（mcm-icm/mathorcup 更新+apmcm/wuyi-mcm/huashubei 新建；成绩日 MCM 2027-05-08 官方、MathorCup 推断 06 下旬、APMCM 推断 2027-01/02）；计算机类报告分片（蓝桥杯/GPLT/4C/服创/C4-BDC 时间线核验，仅 heywhale-c4 更新入条，其余 KB 外仅回结论：蓝桥杯与 GPLT 满足窗口、4C/服创/C4-BDC 不满足）；双创分片消费 comp 队列 10 条（ucla/cala/xczxcy 更新、7 归档）+cy-innovation/三创/大挑核验（大挑届数修正 2027=第二十届；仅 cy-innovation 满足窗口 2027-02~04）；hunter 8 卡+13 拒（台账 153）；tech 队列 103→84 留下轮；CAHE 目录核验为二手转载级（学会官网原文未直抓，待办）；lint 311/0；9-19 cron 中止顺延队列部分消化；⚠ workspace/JOURNAL.md 记行被守卫拦截（多战役标准布局下该路径无战役 root 覆盖、全局 collect 仅放行 kb/**，技能规程步骤5与之冲突——契约缺口上报用户，改由本行留痕） |
| 2026-09-22 | tech+comp | 技术卡13 | 赛事条目2 / 技术卡1 | 0 | 9分片/约8.8M子agent tokens/约35min | /kb-sync 增量跑批：comp 10 候选全消费——tiaozhanbei-chuangye 通知双源补全（8 赛道/揭榜挂帅/配套活动）+黑新浙三省赛实况并入+届次修正 2028（verified:false）；ucla-ai-hackathon-2026 复核无实质变化；同赛伪影条目合并 cala→ucla canonical 唯一化（8 快照迁移，id 防复发规则入条目）。tech 47 候选消费 26（hunter 5 片）：13 新卡（数模线 IMTS 零样本/CTRL 闭环控制/CASP-LLM 覆盖检索/KG-Chronos-2 水力代理；agents 线 RRSI/EDGEGEN/Emergent Collusion/APEXA/MicroPoisoning/ZeroTrustMCP；混合 buddy-minesweeper 基准/Dynamics-memory/Samsone）+SOTER 卡开源落地升级（paper→demo，stars=73）+13 拒（台账 166 无重复）；21 留队。SPA 锚点（Kaggle/devpost/天池）增量发现本轮未做（消化存量优先）留下轮；MLH 2027 季 74 pending 线索提取（3 数据语义赛★）供下轮候选；mlh-hack-the-north 状态出入（ended 09-18~20 vs 条目 upcoming 09-19~21）留下轮老化重验。lint 323/0；JOURNAL 记行沿 09-20 先例由本行留痕（collect 态 L2 仅放行 kb/** 契约缺口未修）。hunter-4 任务包 id 转录错位 1 处（22573/21573）子 agent 两篇均评估建卡，良性。⚠收尾断言：git status 残留 3 处跑批前既有外来变更（.zcode/config.json 钩子关闭=用户有意勿动、.zcodeignore 本地工具面、workspace/kaggressulture fn_docs/results 战役产物），均非本轮产物不入本轮 commit |
| 2026-10-03 | tech+comp | 技术卡10 | 赛事条目3 | 0 | 4分片/约4.9M子agent tokens/墙钟约25min（含SPA预抓） | /kb-sync 增量跑批：SPA/API 四锚点快照补抓落地（终结 09-04 以来两轮顺延）——Kaggle 20 卡/devpost 6 卡/天池 18 条/和鲸 12 条 落 kb/raw/*-list/snapshot-20261003.md（和鲸列表 API 端点未命中改走页面渲染；快照注：kaggriculture 10246 队 12 天截止、Gemma4 DevAgent $65k 一月截止，均在库/在役）。comp 10 候选全消费：挑战杯五文+xczxcy+3 列表页共 8 条 skipped（tiaozhanbei 文章 09-22 已消费、今日跨日逐字节一致复核；tiaozhanbei-chuangye/xczxcy-dasai 仅 last_verified 维护），ucla-ai-hackathon-2026 增补 la-hacks-27 精确时刻 2027-04-16~18、mlh-hack-the-north 翻转 ended（1 天出入待办续）、mlh-ghw-data ended 确认（startsAt 2h 口径差待核）。tech 新 92 候选按信号截断消费 10、0 拒（台账 166 不变）：数模线 5 卡（SimpleTimeBench TSFM 零样本盲区/Nixtlaverse 产品级生态 paper→product/TS-Router 路由/FASE 自进化/稀疏事件 TSFM 评测反直觉打法），agents 线 5 卡（Mem++ 组织记忆/ActiveSaddler harness 课程调度·AutoSaddler 233 星/Mimir 物理农业 agent/DeFA 失败归因/BootLoops 168 星工具包）；tech 留队 82+老三队 105 存量（下轮截断续消）。lint 333/0；JOURNAL 记行沿 09-20 先例由本行留痕（collect 态 L2 仅放行 kb/** 契约缺口未修）。⚠收尾断言：git status 残留跑批前既有外来变更 2 处（workspace/chuangxin2026/docs 两文 10-03 15:53 用户新存，用户资料非本轮产物不入本轮 commit）；跑批期间用户并行会话 /deliver-entry+fn-grill 登记 guojichuangxin2026 战役并入库安航云盾计划书（9d17b614，16:01），本行"未登记目录"点名随之消解，并行安全对（kb×campaign 子树不相交）全程成立 |
| 2026-10-05 | tech+comp（定向） | 赛事条目2 | 0 | 0 | 3分片/约3.8M子agent tokens/墙钟约40min（含主会话SPA预抓+广搜分片） | /attack 预刷新（用户任务：为 compete-strategy 方法论找对抗测试赛）：sync 三脚本（comp 10 候选=挑战杯动态/MLH 噪声留队列下轮；tech 0 新；inbox 空）；主会话 browser-use 预抓 Kaggle 列表快照（kaggle-list/snapshot-20261005.md，raw 不入库）+Kaggle CLI 鉴权通过（E-08 素材齐，方向 api 信源登记留 idle 窗口补——D14 圈禁中）。定向建条 2——kaggle-pokemon-tcg-ai-battle-challenge-playground（任务包 13 预核全证实 0 修正+9 新事实：Winner License=None 不强制开源/对局禁联网/μ0=600/至多 2 终交；引擎=cabt 入 wheel 铁证）与 gsk-pyxis-simulation（upcoming；**重大修正**：gsk.ai 已公布完整时间线与奖金——开赛公告 09-29、entry 2027-01-04、终交 2027-01-11、$50k 池（15k/12k/9k/8k/6k）+论文共同作者邀请；Kaggle 站延期 404 双通道复核成立，上线核验=条目最高待办）。非 Kaggle 广搜分片（结论入 strategy 不建条）：Battlecode 2027=窗口内最优待官宣（2026 届>$20k、引擎开源、2027 仓库预计 11-12 月落地）、CodeCup 2027（Tumbleweed）即刻可报决赛 2027-01-23、Battlesnake=开源引擎沙盒；SSCAIT 停摆/riddles 双死/AIcrowd 非 PvP/AIIDE 出窗、Terminal/CodinGame 报名窗已关或未开。lint 335/0；JOURNAL 记行沿 09-20 先例由本行留痕（collect 态 L2 仅放行 kb/** 契约缺口未修）；收尾断言三项全过 |
