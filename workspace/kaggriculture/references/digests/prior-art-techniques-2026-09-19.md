# 同类仿真对抗赛顶解技术侦察 digest（prior-art-techniques）

- 抓取日期：2026-09-19（所有条目同日抓取）
- 侦察目标：评估"bot 内搜索/规划、自博弈 RL、从回放模仿学习、对手建模、开局库/终局求解、天梯参数爬山"在本赛（Kaggriculture，720 步回合制经济对抗，Elo 天梯 + 终局 Bradley-Terry）的可迁移性。
- 核验等级标注：
  - **[实抓]** = 当日直接抓到原文（GitHub raw README / OpenReview / 论坛页 / kaggle CLI API）。
  - **[搜索核实]** = 经搜索引擎结果片段核实标题/名次/日期，正文因 Kaggle 反爬（CAPTCHA/JS 渲染）未能直抓。
  - **[次级]** = 来自二手转述（博客/论文引用），结论待原文复核。
- 说明：Kaggle 讨论区与 docs 页面对自动抓取有反爬（reCAPTCHA），涉及 Kaggle 正文的条目只能给到"存在性 + 标题 + 名次"级事实，均已标注。

---

## 1. Lux AI Challenge Season 1（2021，NeurIPS 2021 赛，$10k 奖池，22,000+ 提交 / 1,100+ 队）

**赛事 → 顶解技术**
- 1st place：**Toad Brigade**，writeup《Toad Brigade's Approach - Deep Reinforcement Learning》（Kaggle Solution Writeup，2021-12-13）。技术：**深度 RL（PPO）+ U-Net 策略网络 + 自博弈**（对手 = 当前 self、历史 old-self、若干规则基线）。
  来源：https://www.kaggle.com/competitions/lux-ai-2021/writeups （writeup 标题/名次/日期经搜索核实 [搜索核实]；Kaggle 正文反爬未直抓）
- 2nd place：**RLIAYN**，writeup《RLIAYN's approach - Online deep reinforcement learning》（2022-01-18），在线深度 RL。来源同上 [搜索核实]。
- 社区工具（官方 README 实抓）：`glmcdona/LuxPythonEnvGym` —— 整赛环境的 Python 复刻，**比官方环境快约 45x**，自述"使更多 ML / 搜索重型方法变得可行"。来源：https://github.com/glmcdona/LuxPythonEnvGym （经 https://github.com/Lux-AI-Challenge/Lux-Design-2021 README 实抓）[实抓]
- `tonghuikang/lux-ai-2021`：规则 bot + 锦标赛评测工具链基准。来源：https://github.com/tonghuikang/lux-ai-2021 [实抓]

**实测效果**：RL（PPO 自博弈）击败全场 1,100+ 队登顶（1st）；同期 top10 中规则 bot 仍占多数（S1 官方未发布完整 top5 技术统计，此为 writeup 页面可见名单的保守结论）。

**向本赛可迁移性**：高。S1 的胜负手 = "环境提速 45x → 自博弈可承受" + "PPO + 网格 U-Net + 动作掩码"。Kaggriculture 同为网格经济收集型，先例直接成立；且**同赛已有人**把环境接 Rust 批量引擎跑 PPO（见 §7 diffmap）。

---

## 2. Lux AI Challenge Season 2（2022-2023，Kaggle 主赛 + NeurIPS 2023 Stage 2，TrueSkill 天梯）

**赛事 → 顶解技术**
- Kaggle 阶段 1st place writeup 链接被官方资源帖标注为 **"Rule Based 1st Placed Solution"**（discussion/407982）。来源：https://www.kaggle.com/competitions/lux-ai-season-2/discussion/407982 [搜索核实]
- **top5 = C++/TypeScript/Python 规则 agent + 1 个 RL agent**（S3 官方提案论文原文引述）。来源：https://openreview.net/forum?id=7t8kWYbOcj [实抓摘要 + 搜索核实正文句]
- top5 中那个 RL agent 的身份：**Limburg (2023) 的 "DoubleCone"**（"The top DRL agent by Limburg (2023) in the Lux AI Season 2 competition used a 'DoubleCone' neural network backbone with critic and actor heads"）——被 arXiv:2402.08112《A Competition Winning Deep Reinforcement Learning Agent in microRTS》引用。来源：https://arxiv.org/html/2402.08112v1 [搜索核实]
- NeurIPS Stage 2 天梯头部：clist 记录 #1 ry_andy_（TrueSkill ~3442）、#2 SiestaGuru（danmctree，该 ID 暗示 MCTS 系，未逐字核实）。来源：https://clist.by （经搜索摘要）[次级]
- 官方提供 SB3 RL 入门 kit、RoboEden/Luxai-s2-Baseline 强 RL baseline、JAX GPU 加速环境。来源：https://github.com/Lux-AI-Challenge/Lux-Design-S2 README [实抓]
- 10th place：Deimos 纯 RL writeup（2023-05-20）。来源：https://www.kaggle.com/competitions/lux-ai-season-2/discussion （标题经搜索核实）[搜索核实]

**实测效果**：手写规则登顶（含 NeurIPS 阶段资源帖把 1st 归为 rule-based）；RL 需 GPU 批量环境（JAX）才能挤进 top5。

**天梯博弈侧证**：S2 讨论区有选手公开写道 "I was amazed by the strategy from ryandy. I took down my submission and in hiding I moved my strategy in the same direction" —— **撤下提交、隐藏策略方向**是天梯公开战术。来源：https://www.kaggle.com/competitions/lux-ai-season-2/discussion [搜索核实]

**向本赛可迁移性**：双向。若本赛规则引擎已够强（我方现状 4550 名说明还不够），S2 教训是"工程打磨 > 换范式"；RL 要上榜必须有"批量 GPU 环境 + 自博弈管线"，否则只是 Deimos 式 top10 边缘。

---

## 3. Lux AI Challenge Season 3（2024-2025，NeurIPS 2024，Kaggle TrueSkill 天梯）

**赛事形式（对本赛最有参照价值）**：1v1 TrueSkill 天梯；episode 以 **5 局序列**组织，序列内**游戏动态（隐藏常数）会变化**，考察 meta-learning/适应力；官方提供 JAX GPU 环境。来源：https://openreview.net/forum?id=7t8kWYbOcj [实抓摘要]、https://github.com/Lux-AI-Challenge/Lux-Design-S3 [实抓]

**赛事 → 顶解技术**
- 1st place：**Flat Neurons**，writeup《1st Place Approach by Flat Neurons》：**IMPALA 式 RL**。来源：https://www.kaggle.com/competitions/lux-ai-season-3/writeups/flat-neurons-1st-place-approach-by-flat-neurons [搜索核实 writeup 存在性与算法归属（Zenn 次级转述）]
- 2nd place：**Frog Parade**（writeup 2025-03-16），**MAPPO** 系（瑞典硕士论文与 Zenn 文章转述）。来源：同上 [次级]
- 3rd place：**andreyd41/lux3-bot —— 纯模仿学习**（完整 README 实抓，本 digest 最高价值单条）：
  - 双 UNet：Unit-UNet（28x24x24 特征图 + 17 全局特征 → 6x24x24 每格动作分布）+ SAP-UNet（逐单位目标预测）。
  - **训练数据 = 顶队（Frog Parade、Flat Neurons）公开回放**，但精选：对手输掉的 replay 只取其中我方赢的对局；已提前定胜负的对局整场丢弃。
  - **数据预处理占其 80% 工作量**：在雾战争下用自己的推断代码重建 replay agent 的观测（反推 reward 位置、障碍图、隐藏常数）。
  - 镜像对称增广 + 动作类加权交叉熵 + 丢弃 95% 全员 Center 的步。
  来源：https://github.com/andreyd41/lux3-bot [实抓]
- 其他名次：8th gregorlied/lux-s3（github.com/gregorlied/lux-s3 [实抓 README 存在]）、80th linrock《RL training on a laptop》（kaggle 笔记本，被 S3 社区引用为 1st/2nd 写手页来源）[搜索核实]。

**实测效果**：scale 过的 RL（IMPALA/MAPPO）拿金；**精选顶队回放的模仿学习拿铜（3rd）**，且 3rd 的写手明确说"预处理 > 架构"。模仿学习的材料完全公开可得（1st/2nd 的提交回放）。

**向本赛可迁移性**：极高，且本赛条件更好——Kaggriculture **官方发布 episode 回放数据集**（kaggle.com/datasets/kaggle/kaggriculture-episodes-2026-08-22 等），且市场价格公开于回放，无 S3 那种雾战争重建难题。BC 管线可直接照抄 andreyd41 的"选赢局 + 动作掩码 CE + 增广"配方。

---

## 4. Kaggle Kore 2022（2022，$25k，Halite 精神续作）

**赛事 → 顶解技术**
- 官方 winning-solutions 汇总帖（列 1st/2nd/4th/5th writeup 链接）：https://www.kaggle.com/c/kore-2022/discussion/320833 [搜索核实存在；正文反爬未抓]
- 4th place：`qihuazhong/kore-2022` —— **规则 agent**（fork 自 andreyd41/kore-beta-bot 再大改），三个工程胜负手：①游戏逻辑重写为 **NumPy 向量/矩阵运算**；②**预计算候选航线**；③大量 **LRU 缓存**应对 3 秒/步约束；**RL 训过但最终弃用**。来源：https://github.com/qihuazhong/kore-2022 [实抓]
- 5th place：[1 Musketeer] 纯规则（小航线效率 vs 长航线 kore 产出的平衡调参）。来源：https://www.kaggle.com/c/kore-2022/discussion/339979 [搜索核实]
- 6th place：`andreyd41/kore22`。来源：https://github.com/andreyd41/kore22 [实抓 README 存在]
- 1st place writeup 标题《1st place solution: A brief overview of my experience》被 solutions 索引收录，但正文与作者未能核实（Kaggle 反爬）。来源：https://www.kaggle.com/code/sudalairajkumar/winning-solutions-of-kaggle-competitions [搜索核实，存疑保留]

**实测效果**：top6 全部工程化规则/启发式；RL 无一进 top（4th 明说弃用）。

**向本赛可迁移性**：中。核心可迁移物不是策略而是**工程手段**：把经济模拟向量化 + 预计算 + 缓存，直接对应本赛"720 步 × 每步时限"下做 in-bot 搜索/多方案评估的算力预算问题。

---

## 5. Halite III（2018-2019，Two Sigma，4,000+ 玩家）

**赛事 → 顶解技术**
- 冠军：**Teccles**（Java），repo 自述 "in fact it won it"。算法 = **纯启发式打分**：每艘船对全图每格用 **Dijkstra**（代价=回合数）算"移动+采矿+返程"全程期望回合数取最小；连续性设计使目标选择逐回合稳定；自述"尝试对下一块矿做显式规划，**从未带来提升**"。来源：https://github.com/teccles-halite/halite3-bot [实抓]
- 官方社区 post-mortem 汇总帖排名序：#1 Teccles、#2 SiestaGuru（Java）、#3 ReCurs3、#6 TheDuck314… 来源：https://forums.halite.io/t/collection-of-post-mortems-bot-source-code/1335 [实抓]
- 6th place TheDuck314/halite2018：C++ 启发式 + 撞击战斗 + **专门利用"过于谨慎的对手"**（对手建模/剥削先例）；工作流 = **按对手类别归档线上败局复盘最差损失** + spot AWS c5.18xlarge 跑大批自博弈验证改动。来源：https://github.com/TheDuck314/halite2018 [实抓]
- **最佳 ML bot 仅 ~#11**：Kaggle 官方 Halite 页自述 "the best machine learning bot in Halite III ranked #11"；配套论文《Mastering Halite with Reinforcement Learning》实测：从 top 选手回放训练的 SVM/DNN 分类器，表现"介于简单规则 bot 与遗传调参规则 bot 之间"。来源：https://github.com/lnmangione/Halite-III [实抓]；https://www.kaggle.com/c/halite [搜索核实]

**实测效果**：经济资源收集型赛的天花板由"逐格期望收益启发式 + 战斗/碰撞层"定义；ML（含回放模仿）显著低于顶级启发式。

**向本赛可迁移性**：高（警示 + 方法论）。①本赛"每块地每种作物的期望 $/行动"打分即 Teccles 式核心，顶部差距更可能在战斗/市场博弈层；②"败局分类复盘 + 大批量本地自博弈验证"是所有世代通用的爬榜流程；③朴素的"回放→分类器"BC 若无 S3 级数据工程，预期低于现有规则引擎。

---

## 6. Hungry Geese（2021，补充先例）

- 5th place：`takedarts/hungry-geese`，管线 = 训练 + **蒸馏（distill.py）** + 本地评估选模，writeup：https://www.kaggle.com/c/hungry-geese/discussion/263702 。来源：https://github.com/takedarts/hungry-geese [实抓 README]
- 可迁移点：多模型集成在推理预算内**蒸馏成单模型**再提交——本赛若走 BC+RL 双头，可用同法压缩进提交体积/时限。

---

## 7. Orbit Wars（2026，Kaggle 现役同型赛，$50k，4,729 队）—— 最新最直接的同类先例

**赛事 → 顶解技术**
- 三甲 writeup 均挂 Kaggle writeups：1st《1st place solution scaling reinforcement learning…》、2nd、3rd《ab in den orbit》。来源：https://www.kaggle.com/c/orbit-wars/writeups/1st-place-solution-scaling-reinforcement-learnin 等（经 https://kaggle.farid.one/ 索引实抓）[实抓索引/正文反爬]
- 5th place：`tonykozlovsky/orbit-wars-2026-pub` —— **BC→RL 两段式**（完整 README 实抓）：
  1. **行为克隆**：解析 Kaggle 回放重建 (obs, 合法动作)，对 top 选手动作做**掩码交叉熵**，"BC 直接教会何时扩张、该派多少船——纯随机初始化自博弈要烧大量算力才发现这些"。
  2. **RL 微调**：异步 **IMPALA（V-trace）**，奖励=终局胜负稀疏信号；对手 = 当前策略 + **冻结历史检查点池**；KL 正则拉向延迟教师；2p/4p 混训。
  - 算力：**单卡 RTX 5090 训练约 1 周**。
  来源：https://github.com/tonykozlovsky/orbit-wars-2026-pub [实抓]
- `yijieyuan/kaggle-orbitwar`：transformer（每行星一 token）+ **自博弈 PPO league**（2p 从零、4p IL 暖启动；league 准入阈值 admit_thresh 0.7）；**最终模型 = 本地候选池两两胜率均值最高者**（不依赖天梯噪声）；提供 16GB 显存小配额版。来源：https://github.com/yijieyuan/kaggle-orbitwar [实抓]
- 8th place：`sinking-point/ender`：PPO + JAX 高吞吐自博弈环境 + Kaggle Docker 复跑 harness。来源：https://github.com/sinking-point/ender [实抓]
- Silver：`hocop/orbit_wars_mcts`（**MCTS** 路线拿银牌）。来源：https://github.com/hocop/orbit_wars_mcts [实抓 repo 元数据]
- 社区 RL 库：`IsaiahPressman/kaggle-orbit-wars`（63 星）。来源：https://github.com/IsaiahPressman/kaggle-orbit-wars [实抓]

**实测效果**：2026 年的同型天梯赛里，**"BC 暖启动 + 带对手池的 PPO/IMPALA 自博弈"是 top10 标配**；单张消费级 GPU 一周即可打到 top10；MCTS 也能进前三但更依赖每步时间预算。

**向本赛可迁移性**：这是 Kaggriculture 的平行宇宙答案——同为"随机市场 + 终局资金定胜负 + Elo 天梯"。10 天窗口内最现实的路线图（BC→PPO league→本地池选模）有逐字可抄的开源实现。

---

## 8. Kaggriculture 专项侦察（本赛公开情报面，2026-09-19）

**官方与社区入口**
- 官方赛页：https://www.kaggle.com/competitions/kaggriculture [实抓：kaggle CLI]
- 官方 getting-started（Bovard，环境作者）：`bovard/kaggriculture-getting-started`（1,154 票）。来源：kaggle kernels list [实抓]
- Reddit r/reinforcementlearning：《Kaggriculture - Farming + Markets + RL - $50k prizes》（thread 1vgvuti；正文反爬未抓，存在性与标题经搜索核实）。来源：https://www.reddit.com/r/reinforcementlearning/comments/1vgvuti/ [搜索核实]
- 官方回放数据集：kaggle.com/datasets/kaggle/kaggriculture-episodes-2026-08-22（及 08-31）。来源：Kaggle [搜索核实 + 我方 INDEX 已入库]
- 中文面（知乎/B站）：未发现针对本赛的专门中文内容；B 站仅通用 Kaggle 教程合集 [搜索核实]。
- YouTube：itxKgtTDQ0g（本赛介绍向视频）[搜索核实]。

**GitHub 公开 bot/仓库（`kaggriculture` 全站检索 359 仓库，按星数取显著者）[实抓 API]**
- `diffmap/kaggicultureRL`（4 星）：**"Open-source Kaggriculture policy system"**——三种模式：`single_seat_rl`（PPO vs 指定对手）、`dual_seat_rl`（共享策略双座自博弈）、`behavior_mimicry`（**从官方回放文件模仿训练**）；配 **Rust 批量引擎**（maturin 扩展）做训练/评估提速。→ **本赛内"自博弈 PPO + 回放模仿"已有公开完整实现**。来源：https://github.com/diffmap/kaggicultureRL [实抓]
- `destbreso/kaggriculture-cppsim`（3 星）：C++ 高速仿真器（2026-09-14 仍在 push；同作者另有 "A DNA Test for Agents" 笔记本，即我方 replay-dna 血统数据的上游）。来源：https://github.com/destbreso/kaggriculture-cppsim [实抓]
- `CDrookieDc/kaggriculture`：公开完整策略写法的规则引擎——鹅核心（~28 coop，鹅每日 1 个 ~$90 肥料 = 全场最高单动作价值）+ 小麦骨架 + 甜瓜脉冲，规避市场崩价作物（牛/羊/草莓/番茄/胡萝卜卖 100-150 单后崩到 $1 底）；3x3 扇区所有制消除调度震荡；本地 vs starter 31k-34k : 3.4k。来源：https://github.com/CDrookieDc/kaggriculture [实抓]
- `rooklift/krobus`：回放查看器。`gytdrop/KaggressiveAgent`（原文 KaggricultureAgent）：自训练 RL 意图。其余：JaydonJP、Ziyuhua25（agent 基准迭代框架）、Alloysj、kyconf、harryii-eng（规则 bot + 失败假设记录）等 [实抓 API]。
- 注意：`deepeshumrao/kaggriculture-agent` 显示本环境亦被 Google x Kaggle "AI Agents Intensive" 用作教学 capstone——素材（规则文档）随手可得。

**公开 Notebook 生态（kaggle kernels list 按票数实抓）[实抓]**
- `boatlee/v16-rc5-high-score-8c-4s-premium-market-lead`（314 票）："Premium Market Lead" 打法。
- `kaitofukami` 系列（v20/v43/v48，133-78 票）：《40/40 Early Floor | 39/46 Top-10 | v48 Fast Routes》《22/24 Unseen Lineages | v41 Sparse Closed Loop》——**以"未见血统（lineage）H2H 胜率"为选模标准**（"12/12 vs unseen Ryo lineage, 10/12 vs unseen Crop Dusta lineage"）。
- `raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta`（192 票）+ `rank-your-agent`（137 票）：从零到顶 meta 的系统总结 + 自评工具。
- `tetsutani` 3 连发（142/126/103 票）：市场×牧场混合策略。
- `yhay81/shop-router-0909`（133 票）/`six-day-public-state-fieldbook`：商店路由。
- `pilkwang/kaggriculture-structured-economic-policy`（107 票）、`ahmedberatozer` v38/v43（89-107 票）、`thomastschinkel` Public State Router（99 票，自报 74.5% 胜率）、`georgymamarin`《What 2600+ Farms Do Differently》（2026-09-18，44 票，回放大样本 meta 分析）。
- 我方 `references/data/intel-notebooks/` 已存有其中 8 件原件（kaitofukami v48、boatlee v16-rc5、2900 分号、findings 等）。

**"Crop Dusta" 考证**
- 结论 1：**"Crop Dusta" 是本赛圈内公认强队"血统（lineage）"名**，与 "Ryo lineage" 并列作为未见强敌测试基准（"scores 12/12 against the unseen Ryo lineage and 10/12 against the unseen Crop Dusta lineage"，出自 kaitofukami《22/24 Unseen Lineages | v41 Sparse Closed Loop》）。来源：kaggle.com（经搜索核实该笔记本标题与引文）[搜索核实]
- 结论 2：Crop Dusta 亦是**连续在线的真实天梯 agent**——busyaprime《Kaggriculture, five days of the ladder》（kaggle.com/code/busyaprime/kaggriculture-five-days-of-the-ladder，原件已存 `references/data/intel-notebooks/kaggriculture-five-days-of-the-ladder.ipynb` [实抓本地件]）统计：五日（09-01~09-05）唯一全勤 agent，178 局，日胜率 54/52/62/53/75%，总胜率 **56.2%**（与 Jesse Bullard 的 56.3% 并列统计头部）。即：Crop Dusta 是按胜率口径的持续头部选手，而非仅他人命名的一族提交。[实抓]
- 未发现 Crop Dusta 的公开 repo / writeup / 访谈（方法不公开）；2026-09-19 公榜 top20 显示名中无该名（榜首 Majkel1337 3208.4）——与"私榜口径/隐藏式持续提交"假说相容。[实抓 CLI + 搜索]

**公榜头部快照（kaggle CLI，2026-09-19）**：Majkel1337 3208.4；SpaTaro 3122.5；Sida Zuo 3087.4；DSM 3081.3；THIRD FARM CLUB 3073.9；ymg_aq 3067.9；Orbital Terraformer 3039.1；QQ 3035.8；Arda Ceylan 3034.3；Otter Vibe 3023.3；Planned Economy 3021.1 …（我方 ~4550/6806）。[实抓]

---

## 9. 技术可行性事实（官方/权威来源）

**Kaggle Notebooks 配额**
- 每周 **~30 GPU 小时**（Colab Pro 联动再 +15h、Pro+ +30h/周——Kaggle 官方博客，间接证明基线 30h）。来源：https://www.kaggle.com/blog （《Unlock extra GPU on Kaggle with Colab Pro》，搜索核实）[搜索核实]
- 会话上限 **12 小时**、交互会话 40-60 分钟闲置断开、CPU RAM ~30GB、/kaggle/working 磁盘 ~73GB。来源：https://www.kaggle.com/docs/notebooks 与 https://www.kaggle.com/docs/efficient-gpu-usage （官方 URL；正文 JS 渲染反爬未直抓，数字由 luminoai.in / blog.paperspace.com 次级一致转述）[次级，多源一致]
- **Code competition 提交重跑禁网**（模型权重需作为 dataset 附件离线加载）。来源：https://www.kaggle.com/docs/code-requirements [次级，行业共识 + 我方本赛经验]
- 推论：10 天窗口内靠 Kaggle 免费配额做大规模自博弈（S3 级）不现实；**自博弈训练必须在本地 GPU 完成**（Orbit Wars 5th 用单卡 5090 一周，量级吻合）。Orbit Wars 8th 提供了用 Kaggle **公开 Docker 镜像本地复跑评估**的 harness 方案（github.com/sinking-point/ender [实抓]）。

**RL 框架适配性（对 720 步回合制经济自博弈）**
- **Stable-Baselines3（+sb3-contrib）**：官方支持 **Maskable PPO（invalid action masking）**（SB3 README 明列）；**无内建自博弈循环**（README 无 self-play 痕迹）→ 需自管对手池/ league。来源：https://github.com/DLR-RM/stable-baselines3 README [实抓 grep]
- **CleanRL**：单文件 PPO 哲学，**不宣传 self-play/多 agent 工具**（README grep self-play/multi-agent 为空）→ 适合魔改起步，但分布式吞吐要自建。来源：https://github.com/vwxyzjn/cleanrl README [实抓 grep]
- **Sample Factory 2.x**：README 明示 **"Single- & multi-agent training, self-play, supports training multiple policies at once on one or many GPUs"** + 论文级 100k FPS 吞吐 → 三者中**唯一原生支持自博弈/多策略**，前提是把环境向量化接入（本赛已有 Rust 批量引擎先例可桥）。来源：https://github.com/alex-petrenko/sample-factory README [实抓 grep]
- 简明建议：10 天窗口 = **SB3 MaskablePPO 起步**（工程摩擦最小，同赛 diffmap 即 PPO）；若环境向量化顺利再升 Sample Factory。

**行为克隆（json 回放 → 分类器）常规做法**（三源一致）：
1) 解析回放重建每步观测（能推断的隐变量尽量重建）；
2) 动作掩码交叉熵（只对合法动作算损失）；
3) 只取赢家对局 / 丢弃已定胜负对局；
4) 对称性增广 + 类频率加权；
5) 产出作为 RL 初始化或直接策略。
来源：https://github.com/andreyd41/lux3-bot [实抓]、https://github.com/tonykozlovsky/orbit-wars-2026-pub [实抓]、https://github.com/diffmap/kaggicultureRL [实抓]。

---

## 10. 天梯博弈策略先例（提交节奏 / 对手分布 / 最终提交管理）

- **天梯机制**：Lux 系（S2/S3）用 TrueSkill 连续天梯、终局 Bradley-Terry/决赛定榜（S3 提案实抓摘要；neurips.cc S2 页 [搜索核实]）——与本赛 Elo + Bradley-Terry 同构。
- **策略隐藏**：S2 有选手公开承认"撤下提交、隐藏策略方向再改"（见 §2）[搜索核实]。
- **最终提交管理**：Kaggle 通用规则允许**选 2 个最终提交**；仿真赛实践 = "天梯最高者 + 本地评测最稳者" 双保险（amontgomerie.github.io 转述 [次级]）；Lux S1 社区标准工具 = `lux-ai-2021` CLI 本地锦标赛选模（`huikang/lux-ai-agent-evaluation`，kaggle.com/code/huikang/lux-ai-agent-evaluation [搜索核实]）；Orbit Wars 用"本地候选池两两平均胜率"替代天梯信号（github.com/yijieyuan/kaggle-orbitwar [实抓]）。
- **本赛已公开的对应实践**：kaitofukami 用"未见血统 H2H（Ryo/Crop Dusta lineage）"做选模基准；raykkretzschmar 提供 rank-your-agent 自评器——**"本地 H2H 池选模"在本赛是公开明牌**。[实抓 CLI + 搜索核实]
- **败局驱动迭代**：TheDuck314（Halite III #6）"下载全部线上对局 → 按 2p/4p/对手/地图分类 → 按损失惨重度排序 → 只改最差损失暴露的问题"（github.com/TheDuck314/halite2018 [实抓]）。

---

## 11. 汇总：技术 × 跨赛证据矩阵

| 技术 | 有谁用过 | 效果 | 条件 |
|---|---|---|---|
| 自博弈 PPO/IMPALA | Lux S1 Toad Brigade(1st)、Lux S3 Flat Neurons(1st)、Orbit Wars top10 多队、diffmap(本赛) | 登顶（S1/S3） | 环境提速 45x~100kFPS、GPU 数天-数周、对手池/league |
| 从顶队回放 BC | Lux S3 andreyd41(3rd)、Orbit Wars 5th、Halite ML(~#11)、diffmap(本赛) | 银/铜级（数据工程到位时）；裸 BC 仅中游 | 回放可得 + 赢局筛选 + 掩码 CE + 增广 |
| 纯规则/启发式 | Halite III 冠军、Lux S2 冠军、Kore top6、本赛榜首系 | 冠军（2018-2023 主旋律） | 工程打磨 + 败局复盘流程 |
| in-bot MCTS/搜索 | Orbit Wars silver(hocop)、Kore 4th(预计算路由近似) | 银~铜 | 每步时间预算 + 向量化引擎 |
| 对手建模/剥削 | TheDuck314(利用保守对手)、S2 meta 追赶 | 局部显著增益 | 对手行为可分型 |
| 开局库/终局求解 | 未找到直接公开先例 | — | 可能是未开发空间 |
| 参数爬山(A/B 自博弈) | TheDuck314(大批自博弈验证)、Teccles(逐参数打磨) | 冠军级选手的日常工作流 | 本地批量对局 + 只接受显著改进 |
| 天梯提交管理 | S2 隐藏策略、双最终提交惯例、本地池选模 | 稳排名、防 shake-up | 本地评测基建 |
