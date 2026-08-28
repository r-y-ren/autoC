# KB 总索引（瘦协调者唯一入口）

> 由慢循环跑批脚本（scripts/kb/build_index.py）自动重建。**主会话只读本文件做决策路由，不逐条读取条目正文**（分片派发时由子 agent 按需读）。

## KB-1 赛事库（交付物 1）

| ID | 赛事 | 方向 | 层级 | 状态 | 关键日期 | AI 政策 | 最近核验 | 条目路径 |
|---|---|---|---|---|---|---|---|---|
| cumcm | 全国大学生数学建模竞赛（高教社杯 CUMCM） | 数模与时序预测 | 学科竞赛 | active | 2026 报名开始:2026-05-01 09:00… | 《全国大学生数学建模竞赛人工智能工具使用规定（2026年试行）》：适用于大语言模 | 2026-08-27 | competitions/cumcm/ |
| devpost-amazon-nova-ai-2026 | Amazon Nova AI Hackathon | 黑客松与数据竞赛 | 编程/黑客松 | ended | registration_open:2026-02-02、submission_close:2026-03-16… | 强制 Nova：'Your task is to build a generat | 2026-08-27 | competitions/devpost-amazon-nova-ai-2026/ |
| devpost-build-with-gemini-xprize | Build with Gemini XPRIZE | 黑客松与数据竞赛 | 编程/黑客松 | active | submission_open:2026-05-19、submission_close:2026-08-17… | 强制 Gemini：含 LLM 功能的项目必须用 Gemini API 完成部署 | 2026-08-27 | competitions/devpost-build-with-gemini-xprize/ |
| devpost-gitlab-ai-2026 | GitLab AI Hackathon（官方规则名：The GitLab Duo Agent Platform Challenge） | 黑客松与数据竞赛 | 编程/黑客松 | ended | submission_open:2026-02-09、submission_close:2026-03-25… | 平台限定而非模型限定：必须构建运行在 GitLab Duo Agent Plat | 2026-08-28 | competitions/devpost-gitlab-ai-2026/ |
| devpost-revenuecat-shipaton-2026 | RevenueCat Shipaton 2026（真实上架 App 的移动端黑客松） | 黑客松与数据竞赛 | 编程/黑客松 | active | registration_open:2026-05-15、submission_open:2026-07-31… | 官方 rules（2026-08-28 经 webReader 直抓全文）**未 | 2026-08-28 | competitions/devpost-revenuecat-shipaton-2026/ |
| devpost-treehacks-2026 | TreeHacks 2026（斯坦福全美最大高校黑客松，第 12 届） | 黑客松与数据竞赛 | 编程/黑客松 | ended | event_start:2026-02-13、event_end:2026-02-15… | Devpost 首页 Requirements 节（2026-08-28 直抓） | 2026-08-28 | competitions/devpost-treehacks-2026/ |
| goai-opensource-2026 | GOAI 世界人工智能开源大赛（首届，2026） | 黑客松与数据竞赛 | 编程/黑客松 | active | 报名开启:2026-07-16、线下启动仪式（杭州）:2026-07-21… | 实抓官网首页与新浪转载稿均未设 AI 工具使用限制/披露条款（赛事定位即"用 A | 2026-08-28 | competitions/goai-opensource-2026/ |
| heywhale-c4-bigdata-2026 | 2026年中国高校计算机大赛—大数据挑战赛（第十一届 C4-BDC） | 黑客松与数据竞赛 | 编程/黑客松 | active | 报名开放（本届）:北京时间 2026-03-26 10:00、报名&组队截止:北京时间 2026-07-15 12:00… | 未发现 AI 政策条款：本届《大赛通知（盖章）》竞赛规程、平台"参赛须知"、清华 | 2026-08-27 | competitions/heywhale-c4-bigdata-2026/ |
| heywhale-mineru-mdic2026 | 2026 MinerU 数据智能与前沿语料挑战赛（数据智能与前沿语料挑战赛·模塑申城语料普惠计划） | 黑客松与数据竞赛 | 编程/黑客松 | active | … | 赛事本身依托开源文档解析 AI 引擎 MinerU，对 AI/开源工具持明确开放 | 2026-08-27 | competitions/heywhale-mineru-mdic2026/ |
| kaggle-ai-mathematical-olympiad-progress-prize-3 | AI Mathematical Olympiad – Progress Prize 3（AIMO 3） | 黑客松与数据竞赛 | 编程/黑客松 | ended | launch:2025-11-19、entry_deadline:2026-04-08… | 三层实抓：①系列 FAQ（2023-12-19，官方，"for the firs | 2026-08-27 | competitions/kaggle-ai-mathematical-olympiad-progress-prize-3/ |
| kaggle-arc-prize-2026 | ARC Prize 2026（ARC-AGI-2 / ARC-AGI-3 / Paper Track 三赛道） | 黑客松与数据竞赛 | 编程/黑客松 | active | competition_start:2026-03-25、agi3_milestone_1:2026-06-30… | 官方页面实得三组硬条款：①评测环境禁 API 型 LLM——总览页原文 "Int | 2026-08-27 | competitions/kaggle-arc-prize-2026/ |
| kaggle-kaggriculture | Kaggriculture（Google/Kaggle 农场经营 agent 仿真对抗赛） | 黑客松与数据竞赛 | 编程/黑客松 | active | start:2026-07-29、entry_deadline:unknown… | 官方 rules（2026-08-28 经 Kaggle 官方 ListPage | 2026-08-28 | competitions/kaggle-kaggriculture/ |
| kaggle-pokemon-tcg-ai-battle-challenge-strategy | PTCG AI Battle Challenge — Strategy Category（The Pokémon Company × Kaggle） | 黑客松与数据竞赛 | 编程/黑客松 | active | start:2026-06-16、simulation_entry_deadline:2026-08-09… | 官方 rules（2026-08-28 经 Kaggle 官方 ListPage | 2026-08-28 | competitions/kaggle-pokemon-tcg-ai-battle-challenge-strategy/ |
| kaggle-rsna-knee-abnormality-detection | RSNA Knee Abnormality Detection（RSNA 年会 AI Challenge：膝关节 MRI 多模态异常检测） | 黑客松与数据竞赛 | 编程/黑客松 | active | start:2026-07-30、entry_deadline:2026-10-15… | 官方 rules（2026-08-28 直抓）：①外部数据与模型允许（"Free | 2026-08-28 | competitions/kaggle-rsna-knee-abnormality-detection/ |
| lablabai-assemblyai-voice-2026 | AssemblyAI - Voice Agent Hackathon（lablab.ai × AssemblyAI，2026-09） | 黑客松与数据竞赛 | 编程/黑客松 | upcoming | … | 强制技术栈条款（赛事页原文"Every participant builds o | 2026-08-28 | competitions/lablabai-assemblyai-voice-2026/ |
| mathorcup | MathorCup 数学应用挑战赛（原名 MathorCup 高校数学建模挑战赛） | 数模与时序预测 | 学科竞赛 | ended | … | 《MathorCup数学应用挑战赛人工智能工具使用规定（试行）》（组委会2026 | 2026-08-28 | competitions/mathorcup/ |
| mcm-icm | MCM/ICM 美国大学生数学建模竞赛（Mathematical Contest in Modeling / Interdisciplinary Contest in Modeling） | 数模与时序预测 | 学科竞赛 | upcoming | 2027届_竞赛开始:2027-01-28 17:00 EST（美东周四下午5:00）… | COMAP 允许负责任地使用 AI（'Solving the problems  | 2026-08-28 | competitions/mcm-icm/ |
| mlh-ghw-data | MLH Global Hack Week: Data Week 2026 | 黑客松与数据竞赛 | 编程/黑客松 | upcoming | event_start:2026-09-11、event_end:2026-09-17… | MLH 官方 hackathon 规则全文（2026-08-28 核对）无任何  | 2026-08-28 | competitions/mlh-ghw-data/ |
| mlh-hack-the-north | Hack the North 2026 | 黑客松与数据竞赛 | 编程/黑客松 | upcoming | event_start:2026-09-19、event_end:2026-09-21… | 官方 FAQ（2026-08-28 核对：资格/评审/项目边界/团队/费用/差旅 | 2026-08-28 | competitions/mlh-hack-the-north/ |
| tianchi-cross-embodied-cognition-2026 | 2026-跨本体具身认知极限联合挑战赛（2026具身世界realworld挑战赛·赛道二） | 黑客松与数据竞赛 | 编程/黑客松 | active | registration_open:2026-07-30、registration_close:2026-09-21… | 未发现 AI 工具使用限制条款（参赛协议/赛程/须知核对维度：数据使用/代码分享 | 2026-08-28 | competitions/tianchi-cross-embodied-cognition-2026/ |
| tianchi-ijcai18-alimama-cvr | IJCAI-18 阿里妈妈搜索广告转化预测（Alimama International Advertising Algorithm Competition） | 黑客松与数据竞赛 | 编程/黑客松 | ended | 赛事周期:2018-02 至 2018-05（天池用户协议原文 "from February to May 2018"）… | 抓取材料中无 AI 工具使用条款（2018 年赛前 LLM 时代，信息页与用户协 | 2026-08-28 | competitions/tianchi-ijcai18-alimama-cvr/ |
| tianchi-loreal-beauty-tech-hackathon-2026 | 欧莱雅第二届美妆科技黑客松——用 AI 造点美（天池·AI大模型赛） | 黑客松与数据竞赛 | 编程/黑客松 | active | … | 详情页全文未设任何 AI 工具使用限制、申报或披露条款；赛事本身即以 AI 应用 | 2026-08-27 | competitions/tianchi-loreal-beauty-tech-hackathon-2026/ |
| tianchi-qoder-thursday | Q力星期四（Qoder码力星期四）系列赛（天池·AI大模型赛） | 黑客松与数据竞赛 | 编程/黑客松 | active | 系列赛期:2026-07-16 至 2027-07-31… | 系列由阿里 AI 编程工具 Qoder 冠名，官方推荐并鼓励使用 AI 编程工具 | 2026-08-27 | competitions/tianchi-qoder-thursday/ |

## KB-2 科技库（交付物 2）

| ID | 名称 | 领域 | 方向 | 成熟度 | 比赛映射 | 发表 | 最近核验 |
|---|---|---|---|---|---|---|---|
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
| gh-agents-universe_agents-universe | Agents Universe：知识条目驱动的企业级多角色 Agent 平台（无向量检索的项目记忆） | LLM agents | 黑客松与数据竞赛 | demo | 黑客松-数据与算法、数模-数据分析与决策 | 2026-08-18 | 已引 |
| gh-BraxisAI_braxis-blueprint | braxis-blueprint: 零预算免费 LLM 通道路由与自动化运维的实战脚本集 | LLM agents | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-23 | 已引 |
| gh-joe960913_Jixu | Jixu：TypeScript 持久化单 Agent Harness（事件溯源 Thread，可恢复/重放/分叉） | LLM agents | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-18 | 已引 |
| gh-memovai_mimimodel | MimiModel: $5 ESP32-S3 上的全离线工具调用 LLM 引擎（单文件 C） | on-device inference、LLM agents | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-16 | 已引 |
| gh-only-cli_oc | oc (only-cli): 把任意网站压缩成 AI agent 可浏览的紧凑 CLI | LLM agents、retrieval augmented generation | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-18 | 已引 |
| gh-rome-os_rome | Rome: 面向人机协作的 Agentic OS 与可安装 App 模型 | LLM agents、agent 工程化 | 黑客松与数据竞赛 | product | 黑客松-数据与算法 | 2026-08-23 | 已引 |
| gh-squall01337_mixamo-llm-mocap | mixamo-llm-mocap: 视频到 Mixamo 角色动画的 agent 可操作全管线 | LLM agents、3D 动画与动作捕捉 | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-17 | 已引 |
| gh-UditAkhourii_cdaf | CDAF: 视频的 agent 可读文本边车格式——一次生成、逐次省 token | LLM agents、多模态视频理解 | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-26 | 已引 |
| gh-Vistyy_nopus | nopus: 编码 agent 回复的确定性散文质量门 | LLM agents、输出质量评测 | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-15 | 已引 |
| gh-wolfiesch_omp-best-of | omp-best-of: Best-of-N 候选 + LLM-as-a-Verifier 择优的编码 agent 编排插件 | LLM agents | 黑客松与数据竞赛 | demo | Kaggle-竞赛 | 2026-08-18 | 已引 |
| gh-Zyrexnn_Cybermes | Cybermes: 自主进攻安全/赏金自动化 Agent 框架 | LLM agents、网络安全自动化 | 黑客松与数据竞赛 | demo | 黑客松-数据与算法 | 2026-08-19 | 已引 |

## 跑批记录

| 日期 | 类型 | 新增 | 更新 | 隔离 | 成本 | 说明 |
|---|---|---|---|---|---|---|
<!-- 成本列=分片数/token/墙钟（T4.3 起新行必填；旧行无此列属历史格式） -->
| 2026-08-27 | tech+comp | 技术卡6 / 赛事条目3 | 0 | 0 | 首次真实跑批（T3-a）：arXiv 收紧查询后31候选→6卡；gh未登录按设计降级 |
| 2026-08-27 | discover | 赛事条目8 | 0 | 0 | 黑客松与数据竞赛冷启动（T4批次2）：4搜索分片→35候选→8入库+13留队列；Amazon Nova winners首样（6深构+1降级）；修正失真公告快照 |
| 2026-08-28 | tech+comp | 技术卡9 / 赛事条目12 | 0 | 0 | 5分片/19.8M tok/33min | 增量：comp消费discover留存13→12入库+1留尾(CDEC待预抓)；tech 160候选→9卡+100台账+50留队；两脚本缺陷待修(gh行内star限定词失效/build_index注释行断表) |
