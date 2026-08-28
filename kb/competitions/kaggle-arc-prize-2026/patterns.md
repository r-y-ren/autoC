---
competition_id: kaggle-arc-prize-2026
last_verified: 2026-08-28
coverage: [2023, 2024, 2025]   # 2024/2025 为官方结果页全量（名单+分数+方法口径）；2023 仅 winners+分数（arcprize.org/history），方法细节缺口；2020/2022 为时间线上下文
confidence: 中                 # 赛制规则(2026)与 2024/2025 结果直抓自官网，等级高；扣分项：2023 方法未取得、2024 per-team 方法仅间接口径、Grand Prize 六项标准名目未渲染
sources:
  - url: https://arcprize.org/competitions/2025
    title: "ARC Prize 2025 结果页（High Score/Paper 获奖名单、分数、奖金、Top Scores 方法一句话口径）"
    accessed: "2026-08-28"
  - url: https://arcprize.org/blog/arc-prize-2025-results-analysis
    title: "ARC Prize 2025 Results & Analysis（官方博客：参赛规模、NVARC/ARChitects/MindsAI 方法、TRM/CompressARC 细节、refinement loop 叙事、商业模型对照）"
    accessed: "2026-08-28"
  - url: https://arcprize.org/competitions/2024
    title: "ARC Prize 2024 结果页（ARC-AGI-1 获奖名单、Paper 奖、ARC-AGI-Pub 高分表含 o3/GPT-4o/Claude 3.5 对照）"
    accessed: "2026-08-28"
  - url: https://arxiv.org/abs/2412.04604
    title: "ARC Prize 2024: Technical Report（经 arcprize.org/2024/report 重定向取得；摘要：SOTA 33%→55.5%，DL-guided program synthesis 与 TTT 推动）"
    accessed: "2026-08-28"
  - url: https://arcprize.org/history
    title: "ARC Prize 历史页（2020 icecuber 20%、2022 ARCathon Hodel、2023 双冠军 30%、2024/2025/2026 沿革）"
    accessed: "2026-08-28"
  - url: https://arcprize.org/leaderboard
    title: "官方 leaderboard 页（Kaggle Systems 约束口径 $50 compute budget / 120 tasks；cost-vs-performance 定位）"
    accessed: "2026-08-28"
  - url: https://arcprize.org/competitions/2026
    title: "ARC Prize 2026 总览（开源资格条款、时间线、AI 政策）"
    accessed: "2026-08-27"
  - url: https://arcprize.org/competitions/2026/arc-agi-2
    title: "ARC-AGI-2 赛道页（85% 目标、2 outputs 计分、未开源移除条款、Grand Prize Writeup 评审）"
    accessed: "2026-08-27"
  - url: https://arcprize.org/competitions/2026/arc-agi-3
    title: "ARC-AGI-3 赛道页（Grand 解锁条件、Milestone 开源门槛、五项能力）"
    accessed: "2026-08-27"
  - url: https://arcprize.org/competitions/2026/paper
    title: "Paper Track 赛道页（六维 rubric 原文：Accuracy/Universality/Progress/Theory/Completeness/Novelty；>4.5 入 Outstanding Pool）"
    accessed: "2026-08-27"
  - url: https://arcprize.org/policy
    title: "ARC Prize Verified Testing Policy（$10K/次上限、不跨次平均、不开 web search、工具 opt-in 声明）"
    accessed: "2026-08-27"
---

# ARC Prize 2026（kaggle-arc-prize-2026）模式库（patterns）

> 本文件是 KB-1 条目的解构总结层。2026 届进行中（结果 2026-12-04 公布），本版模式库基于**历届（2020-2025）官方结果页与官方博客的实抓解构**构建，供赛点检查表与赛道评估消费；12-04 后须以 2026 届实际获奖名单刷新。
> 原始快照：历届结果与分析存 `kb/raw/kaggle-arc-prize-2026/patterns/`（6 件）；2026 官方页存 `kb/raw/kaggle-arc-prize-2026/`（5 件，2026-08-27 抓）。信源等级：全部为官网/官方技术报告（arXiv 经官方链接重定向），无二手转引。

## 一、评审偏好（赛制特殊性：本赛"评审"≈基准表现，非主观打分）

ARC 系列的评奖结构与常规"评委偏好"型竞赛根本不同，实抓依据如下：

- **纯客观指标制（主体）**：Top Score / Progress / Milestone 奖全部按隐藏私榜准确率排序。计分规则原文："For each task, you should predict exactly 2 outputs for every test input grid. If any of the 2 predicted outputs matches the ground truth exactly, you score 1 for that task, otherwise 0."（ARC-AGI-2 赛道页，2026-08-27 抓）。历届结果页即按此分数排奖金（2025：1st NVARC 24.03%/$25k → 5th G. Barbadillo 6.53%/$5k，arcprize.org/competitions/2025，2026-08-28 抓）。
- **里程碑解锁制（大奖）**：Grand Prize 不是评审出来而是"解锁"出来的——2026 届 ARC-AGI-2 Bonus 为"首个私榜 ≥85%"（$150K）、ARC-AGI-3 Grand 为"首个在 ARC-AGI-3 评测得 100% 的合格 agent"（$700K）。历届从未解锁：2024/2025 结果页首行均为 "The Grand Prize remains unclaimed."（arcprize.org/competitions/2024 与 /2025，2026-08-28 抓）。
- **开源强制 + 可复现**："All leading participants are expected to open source their solutions to be eligible for a prize"；"All prizes require reproducible, open-source submissions"；自有代码须 CC0/MIT-0，第三方须 Apache-2.0/GPLv3 等；"Participants must open source their solutions before receiving official private evaluation scores."（总览页，2026-08-27 抓）。2026 届 AGI-3 Milestone 更把开源时间做成资格线："Participants who open source their solutions by the milestone deadlines are eligible for milestone prize money."（AGI-3 赛道页，2026-08-27 抓）。历届兑现情况：官方博客 "all ARC Prize 2025 winning solutions and papers are open-source"（结果分析博客，2026-08-28 抓）。
- **唯二的主观评审位**：① ARC-AGI-2 Grand Prize（$275K）按 Solution Writeup "evaluated equally across the following six criteria. Each criterion is scored on a scale from 0 (lowest) to 5 (highest), with the final score calculated as the average of all six"——但**六项标准的具体名目未在静态快照中渲染**（AGI-2 赛道页，2026-08-27 抓；缺口，待可渲染抓取补全）；② Paper Track 六维 rubric 已实得：**Accuracy（按关联 Kaggle 提交的榜上表现）/ Universality / Progress（对"任何人达到 85% 的概率"的提升）/ Theory / Completeness / Novelty**，>4.5 分入 $375K Outstanding Pool 由主办方裁量分润（Paper 赛道页，2026-08-27 抓）。
- **效率与准确率并重的公示口径**：官方结果页与 leaderboard 把 cost-per-task 与分数并列展示（2025 冠军表 "Score: ARC-AGI-2 Private Evaluation / Cost per task: USD $0.20"；leaderboard 页对 Kaggle Systems 的描述为 "operating under strict computational constraints ($50 compute budget for 120 evaluation tasks)"，未标注适用届次；AGI-2 85% 目标原文含 "within the Kaggle efficiency limits"）。（arcprize.org/competitions/2025、/leaderboard、/competitions/2026/arc-agi-2，2026-08-27/28 抓）

**小结**：不存在"讨好评委"的问题；存在的是"在无网评测 + 开源 + 效率约束下把私榜分数做上去"的纯工程/科学问题，外加两处文书位（Solution Writeup、Paper）。

## 二、方法论分布（历届获奖方法演进表——本文件核心）

**演进总表**（全部为官方页面原文口径，逐条带源）：

| 届次 | 基准 | 名次/团队 | 私榜分数 | 方法（官方口径原文/摘要） | 来源（抓取日） |
|---|---|---|---|---|---|
| 2020 首届（Kaggle） | ARC-AGI-1 | 1st: icecuber | 20%（test set 成功率） | 方法未载于本次实抓页面——**缺口** | arcprize.org/history（2026-08-28） |
| 2022 ARCathon（Lab42 合办） | ARC-AGI-1 | 1st: Michael Hodel | 未载 | 官方口径仅及"后来开发出最强 ARC-AGI DSL 之一"——**DSL/程序合成取向线索，非当届方案描述** | arcprize.org/history（2026-08-28） |
| 2023 ARCathon | ARC-AGI-1 | 并列 1st: Team SM（Gholami & Kazeminia）与 MindsAI（Jack Cole） | 双 30%（private eval） | 方法未载于 arcprize.org——**缺口**（当届主办方为 Lab42，其站点未在本次分片范围） | arcprize.org/history（2026-08-28） |
| 2024 ARC Prize（Kaggle） | ARC-AGI-1 | 1st: the ARChitects | 53.5% | 官方回溯口径："test-time adaptation and data augmentation ... responsible for the top score in ARC Prize 2024 (ARChitects)"；2025 页称其 2024 系统为 autoregressive system | 结果分析博客（2026-08-28）；arcprize.org/competitions/2024（2026-08-28） |
| 2024 同上 | ARC-AGI-1 | 2nd: G. Barbadillo / 3rd: alijs | 40% / 40% | 方法名目未载于结果页（Code/Paper 链接外链）——**缺口** | arcprize.org/competitions/2024（2026-08-28） |
| 2024 技术报告口径 | ARC-AGI-1 | — | SOTA 33%→55.5% | "propelled by several frontier AGI reasoning techniques including **deep learning-guided program synthesis and test-time training**" | arXiv 2412.04604 摘要，经官方 /2024/report 链接（2026-08-28） |
| 2025 ARC Prize（Kaggle） | ARC-AGI-2 | 1st: NVARC | 24.03%（$0.20/task） | "A synthetic-data-driven **ensemble of an improved Architects-style test-time-trained model and TRM-based components**" | arcprize.org/competitions/2025 + 结果分析博客（2026-08-28） |
| 2025 同上 | ARC-AGI-2 | 2nd: the ARChitects | 16.53% | "A **2D-aware masked-diffusion LLM** with **recursive self-refinement** and perspective-based scoring ... improving substantially over the team's 2024 autoregressive system"（同队跨年换架构） | 同上 |
| 2025 同上 | ARC-AGI-2 | 3rd: MindsAI | 12.64%（访谈段落另记 15.42%，同页并存，口径差异未解释——如实双记） | "A heavily engineered **test-time-training pipeline** that combines TTFT, augmentation ensembles, tokenizer dropout, and some new pretraining tricks" | 同上 |
| 2025 同上 | ARC-AGI-2 | 4th/5th: Lonnie / G. Barbadillo | 6.67% / 6.53% | 方法名目未载于结果页——**缺口** | arcprize.org/competitions/2025（2026-08-28） |

**论文奖（方法创新的另一条主线）**：

| 届次 | 奖项/论文 | 方法要点（官方口径） | 来源 |
|---|---|---|---|
| 2024 Paper 1st | "Combining Induction and Transduction for Abstract Reasoning"（Li et al.） | 归纳+转录结合（标题口径，细节未展开） | arcprize.org/competitions/2024（2026-08-28） |
| 2024 Paper 2nd | "The Surprising Effectiveness of Test-Time Training for Abstract Reasoning"（Akyürek et al.） | test-time training（与主赛道同趋势） | 同上 |
| 2024 Paper 3rd | "Searching Latent Program Spaces"（Bonnet & Macfarlane） | 潜空间程序搜索 | 同上 |
| 2025 Paper 1st（$50k） | TRM, "Less is More: Recursive Reasoning with Tiny Networks"（Jolicoeur-Martineau） | "~7M 参数单网络递归模型，answer/latent 双状态，deep supervised refinement，ARC-AGI-1 ~45% / ARC-AGI-2 ~8%"；承自 HRM 工作 | 结果分析博客（2026-08-28） |
| 2025 Paper 2nd（$20k） | SOAR（Pourcel, Colas & Oudeyer） | "自改进的进化程序合成框架：LLM 在自身搜索轨迹上微调，无人工 DSL/解答数据集，开源 ARC-AGI-1 解达到 52%" | 同上 |
| 2025 Paper 3rd（$5k） | CompressARC, "ARC-AGI Without Pretraining"（Liao & Gu） | "仅 76K 参数，无预训练/无数据集/无分支搜索，每题单模型 test-time 训练，MDL 原则（VAE 损失+解码器正则替代组合搜索），ARC-AGI-1 ~20–34% / ARC-AGI-2 ~4%，**单张 RTX 4070 上每题约 20 分钟**" | 同上 |

**生态侧对照（非 Kaggle 获奖但官方同页公示，2024 ARC-AGI-Pub 高分表）**：o3 75.7%、Jeremy Berman 53.6%（其 2025 论文口径为自然语言进化搜索）、MARA(BARC)+MIT 47.5%、Ryan Greenblatt 43%、o1-preview 18%、Claude 3.5 Sonnet 14%、GPT-4o 5%、Gemini 1.5 4.5%（半私榜/公榜双列，arcprize.org/competitions/2024，2026-08-28 抓）。2025 商业侧：Opus 4.5 (Thinking, 64k) 37.6% @ $2.20/task；Poetiq 基于 Gemini 3 Pro 的 refinement 54% @ $30/task（基线 31% @ $0.81）（结果分析博客，2026-08-28 抓）。

**演进脉络归纳（每一步均有上表出处）**：
1. **纯 LLM prompt 路线已出局**：2024 Pub 表中裸 GPT-4o/Gemini 1.5 仅 4.5–5%，Claude 3.5 Sonnet 14%；而工程化系统（TTT、进化搜索）40%+。
2. **test-time training/adaptation 是 2024→2025 的持续主线**：2024 冠军（TTA+数据增强）→ 2025 前三名全部为 TTT 系（NVARC 集成、ARChitects 换扩散架构+自精炼、MindsAI TTFT 管线）；2024 技术报告把 TTT 与 DL-guided program synthesis 并列为当年两大推动力。
3. **2025 官方叙事收敛到 "refinement loop"**：进化式程序精炼（Berman 自然语言程序 / Pang Python 程序+动态抽象库）与"权重空间程序"（TRM/CompressARC 零预训练 test-time 训练）被并列为本年度方法主题。
4. **模型规模两极分化**：一端是重工程 TTT 集成（冠军），另一端是超小模型（7M/76K 参数）拿论文头奖——"小模型+新机理"与"大管线+合成数据"两条路都被官方重奖。
5. **团队跨年迭代特征显著**：ARChitects（2024 冠军→2025 二名）、MindsAI（2023 ARCathon 并列冠军→2025 三名）均为多年连续参赛并换架构升级。

> 频次声明：上表为**历届 Top5+论文奖的非随机小样本**（覆盖 2024/2025 全部公示获奖者与 2023 冠军），频次不代表全体 1,455 支参赛队（2025 规模口径，结果分析博客）的方法分布。

## 三、往届差异化点（拿到奖的 vs 没拿到的）

- **拿到 Top Score 奖的共性**（2024/2025 前三可证）：① 全部走 TTT 系路线而非纯 prompt/纯 DSL；② 重数据工程——NVARC 明示 "synthetic-data-driven"，MindsAI 明示 "heavily engineered ... augmentation ensembles"；③ ARChitects 两年均在前二，第二年主动换范式（自回归→masked-diffusion+递归自精炼），官方以 "improving substantially" 肯定。（arcprize.org/competitions/2025 + 博客，2026-08-28）
- **拿到里程碑/解锁大奖的：无一人**。2024/2025 两届 "The Grand Prize remains unclaimed."；2025 最高 24.03%，距 85% 目标差约 61 个百分点。官方归因："the Grand Prize accuracy gap is now primarily bottlenecked by **engineering** while the efficiency gap remains bottlenecked by **science and ideas**"（结果分析博客，2026-08-28）。即：分数差距=工程量差距，成本差距=科学想法差距。
- **拿到 Paper 奖的共性**：rubric 六维中 Progress/Theory/Novelty 权重与 Accuracy 等权——TRM（7M 参数、AGI-2 仅 ~8%）与 CompressARC（AGI-2 仅 ~4%）分数远低于主赛道冠军仍拿 $50k/$5k，证明论文赛道奖励"机理新颖+对 85% 目标的推进论证"而非绝对分数；且**必须关联一个真实 Kaggle 提交**（"Each paper must include a corresponding Kaggle submission confirming it describes a real, working entry"，其分数计入 Accuracy 维）。（Paper 赛道页 2026-08-27；博客 2026-08-28）
- **2026 新增的"差异化捷径"——Milestone 奖的资格差异**：AGI-3 M1/M2（6-30/9-30）奖金只发给"节点截止前已开源"者——开源时点本身成为与同分者拉开资格差的变量。（AGI-3 赛道页，2026-08-27）
- **没拿到的常见位置**：2025 年 1,455 队提交 15,154 次，Top5 门槛 6.5%，头部断层极大（24.03% → 6.53%）——进 Top5 与夺冠之间隔着一个方法代差（TTT 集成 vs 单一方法）。（博客 + 结果页，2026-08-28）

## 四、反面观察（合规红线与失败模式）

**历届 DQ 案例：本次实抓范围内未取得任何"高分但违规被取消资格"的公开案例**（2024/2025 结果页、技术报告摘要、博客均未见；不凭记忆补写）。已实抓的是**条款化的红线与执行机制**：

- **未开源即除名**（条款原文）："participants eligible for a prize will be removed from the competition if they do not open source their solutions."（2026 ARC-AGI-2 赛道页，2026-08-27 抓）。
- **评测期禁 API 型 LLM**（结构性约束，非抽查）："Internet access is not available during Kaggle evaluation (no API-based systems like GPT/Claude/etc.)"（2026 总览页，2026-08-27 抓）——依赖在线 API 的方案在评测期直接不可运行，属于"方案设计即违规"型红线。
- **Testing Policy 红线**（官方验证侧）：单次评测成本上限 "$10,000 USD per run"；"we do not average scores across runs"（不刷分取平均）；"We specifically do not enable web search, because that could leak Semi-Private data to the web."；"tool use should be opt-in, not opt-out, so any tool use will always be declared"（任何工具使用必须声明）。（arcprize.org/policy，2026-08-27 抓）
- **官方承认的"灰色地带"——知识过拟合**：博客 "Overfitting on Knowledge" 段指出 frontier 模型可能已在训练数据中见过 ARC 数据（Gemini 3 验证中出现未被告知的正确 ARC 颜色映射为证），"either incidentally or intentionally, we cannot tell"——主办方将其列为推动 AGI-3 新基准设计的动因之一。对参赛者的含义：借公榜/泄露数据过拟合的路线在官方叙事中已被标记为不可持续方向。（结果分析博客，2026-08-28 抓）
- **可证的失败模式**（数据侧，非评委讲评）：
  1. 纯 LLM/prompt 路线：2024 Pub 表裸 GPT-4o 5%、Gemini 1.5 4.5%（ARC-AGI-1，更易的基准）——在 AGI-2 上更低；
  2. 忽视成本约束：商业推理系统准确率够但单价超限（Opus 4.5 $2.20/task、Poetiq refinement $30/task，对 Kaggle "efficiency limits" 是数个量级的差距；对照 2025 冠军 $0.20/task）；
  3. 低估基准换代难度：同一批顶级方法从 AGI-1（53.5%）到 AGI-2（16.5–24%）分数腰斩再腰斩。

## 五、赛点检查表（ARC 型竞赛检查项 → 快循环验收清单派生源）

- [ ] **无网可运行**：方案在断网环境完整跑通（模型权重随 notebook/Kaggle dataset 携带，无任何 API 调用残留）——依据："No internet access during evaluation / no API-based systems"（2026 总览+两赛道页，2026-08-27）
- [ ] **开源合规双栈**：自有代码 CC0/MIT-0（或同等公有领域/宽松许可）；第三方依赖逐个核对为 Apache-2.0/GPLv3 等"允许公开共享"许可并留存清单——依据：总览 Rules Open Source License 节（2026-08-27）
- [ ] **开源时点**：私榜分数产生前完成开源；若冲 AGI-3 Milestone，M1（6-30）/M2（9-30）节点前开源——依据：总览 + AGI-3 赛道页（2026-08-27）
- [ ] **计分规则对齐**：每个 test 输入恰输出 2 个预测（多/少/格式错均直接丢分）；最终分 = 全部任务平均——依据：AGI-2 Scoring Methodology（2026-08-27）
- [ ] **可复现包**：提交包含从零复现私榜分数所需的全部 artifacts（数据/种子/流程），Solution Writeup 与 artifacts 在截止后 7 日内挂出（冲 AGI-2 Grand 时）——依据：总览 "reproducible, open-source submissions" + AGI-2 Grand 条款（2026-08-27）
- [ ] **效率预算自证**：记录并公示 cost-per-task 口径（历届官方公示格式为 "分数% + $/task"），对照 Kaggle efficiency limits 做压力测试——依据：2025 结果页表头、leaderboard 页、AGI-2 85% 目标原文（2026-08-27/28）
- [ ] **提交流程两阶段**：Kaggle code competition 先 Save & Run All 验证可运行、再 Competition Rerun 跑隐藏集；AGI-3 才可用 RTX 6000；加速会话本身禁网——依据：docs.arcprize.org starter kit（经 meta.md 载录，2026-08-27）
- [ ] **验证侧声明**：若方案使用任何工具（搜索/执行器等），在文档中显式声明（opt-in 原则）；不假设官方会跨次平均分数——依据：Testing Policy（2026-08-27）
- [ ] **Paper 关联**（若走论文赛道）：论文关联同届真实 Kaggle 提交（分数计入 Accuracy 维），六维 rubric 自查（尤其 Progress=对 85% 目标的推进论证、Theory=为什么有效）——依据：Paper 赛道页（2026-08-27）
- [ ] **本地-线上一致性**：本地复现官方 baseline 与历史开源获奖方案（如 2025 全部获奖方案开源可复现）后再谈改进——依据：博客 "All scores & papers below are open source & reproducible" + 结果页 Code 链接（2026-08-28）

## 六、对本框架的启示（对 4070 laptop 单卡画像的如实评估）

**定位判断：主赛道（Top Score/解锁奖）冲奖不现实；Paper Track 与练手性参与匹配度最高。依据如下（全部来自实抓口径，无估计数字）：**

- **顶级方案的算力/工程门槛与本队约束的差距是结构性的**：2025 冠军 NVARC 是"合成数据驱动的 TTT 模型 + TRM 组件"集成（合成数据生产与集成评测的工程量大）；第三名官方用词即 "heavily engineered"；头部团队均为多年连续迭代（ARChitects、MindsAI 跨 2-3 届）。本队单卡 + 首次参赛，在该轴线上无比较优势。（arcprize.org/competitions/2025 + 博客，2026-08-28）
- **但"小模型+新机理"路线被官方重奖且算力兼容**：CompressARC 官方口径 "76K 参数 ... 单张 RTX 4070 每题约 20 分钟" 拿 Paper 3rd（$5k）；TRM 7M 参数拿 Paper 1st（$50k）。注意 4070 **桌面版**与笔记本版算力有差（相对倍数未实测，不引用数字），耗时会上升——可行性要以本机实测为准，但方法量级（十万级参数、单题级训练）明确落在单卡可及范围。（结果分析博客，2026-08-28）
- **正式评测算力由 Kaggle 承担**：提交为 Kaggle notebook（cpu/t4/p100，RTX 6000 限 AGI-3），本地卡只用于开发迭代——本地算力不是参赛硬门槛，**迭代速度和方法新颖度才是**。（docs starter kit 经 meta.md，2026-08-27）
- **赛程现实**：当前 8-28，M2（9-30）一个月内，提交截止 11-02，论文截止 11-08——若做 Paper Track，方法开发窗口约 2 个月，须关联一次真实 Kaggle 提交（分数不限高低但计入 Accuracy 维）。（2026 总览 + Paper 页，2026-08-27）
- **方法切入建议**（从演进表直接派生）：TTT/refinement loop 是当前被验证的主线且方向上未被做尽（85% 远未达到，官方判定 accuracy 瓶颈在工程、efficiency 瓶颈在科学想法）；小模型递归精炼（TRM 后继）与 MDL 式零预训练（CompressARC 后继）两条已被证明"单卡可做+能拿论文奖"。纯 prompt 工程与裸 LLM 调用是被数据淘汰的路线。
- **合规栈**：无网运行 + CC0/MIT-0 开源 + 2 输出格式 + 工具声明，四项在开发第一周就要进 CI（详见第五节检查表）；AI 辅助原创的合规底线与本届"强制开源"天然兼容，但需在 writeup 中保留人机分工记录以对齐本仓库合规要求。
- **刷新点**：2026-12-04 结果公布后，本文件第二节演进表须补 2026 届行（三赛道首届获奖方法），第六节定位判断须复核。

## 数据缺口声明（本版如实记录，未猜测补全）

1. **2023 ARCathon 方法细节**：arcprize.org 仅载 winners+分数（history 页）；当届详情在 Lab42 侧（arcathon.lab42.global），未在本分片抓取范围。arcprize.org/competitions/2023 返回 404（2026-08-28 实测，快照已弃置）。
2. **2024 年 2-5 名与 2025 年 4-5 名方法名目**：结果页仅给 Code/Paper 外链，未内嵌方法描述；深构需另抓其外链论文/GitHub（下轮分片候选）。
3. **ARC-AGI-2 Grand Prize 六项标准名目**：静态快照未渲染列表内容（仅"六项等权 0-5 取均值"总述），需可渲染抓取（Browser Use 主会话）补全。
4. **2026 届 compute limits 具体数值**：官方页面仍为 "will be announced with the competition launch" 表述（meta.md 待核验清单已记）。
5. **2025 MindsAI 分数双口径**（12.64% 榜格 vs 15.42% 访谈段）来源页未解释，双记待核。
