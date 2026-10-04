# Kaggriculture 竞赛情报 digest —— web/CLI 综合抓取（2026-09-19）

抓取方式：kaggle CLI 2.2.4（`competitions pages --content` 官方页面全文、`competitions topics` 讨论区、kagglesdk `GetCompetition` API）、榜单 CSV 下载、kernels/datasets 列表、少量 notebook 拉取。原始件归档：`references/data/web-intel-20260919/`（pages 全文 CSV + 每页 md + 43 个讨论帖 JSON）、`references/data/lb-snapshot-20260919/`（榜单快照）。除标注外抓取日期均为 **2026-09-19**。

官方页 URL 约定：Kaggle SPA 网页需 JS 渲染，以下"来源 URL"指向的正文是经官方 API `competitions pages --content` 取回的页面全文（与网页 Overview/Rules/Evaluation 标签内容一致）。

---

## 1. 排名机制（matchmaking / 最近 2 次跟踪 / Bradley-Terry 定榜 / Validation Episode）

来源：官方 Evaluation 页 https://www.kaggle.com/competitions/kaggriculture/evaluation（API 抓取，2026-09-19）

- 每天最多提交 5 个 bot；每个提交在 ladder 上与**相近 skill rating** 的 bot 对局（"Each submission will play Episodes (games) against other bots on the ladder that have a similar skill rating"）。
- **仅最近 2 次提交被跟踪**：为减少对局数量、保证匹配质量，只有 latest 2 submissions 被跟踪，且**这最新 2 个提交也用于最终榜单评估**。每个提交的 bot 在提交后会一直打到比赛结束，但新 bot 的对局频率远高于旧 bot；榜单只显示你分数最高的那个 bot。
- **Validation Episode**：上传提交时先跑一个"自己打自己副本"的校验局，确保能无错运行；失败则标记 `Error`，可下载 agent 日志调试；通过则以默认初始 rating 进入匹配池。
- Elo 规则：胜升负降，rating 差越大 beating 高分对手加分越多；平局把双方 rating 拉近；**净胜金币数不影响 rating 变化，只看胜/负/平**。
- **终榜 Bradley-Terry**：提交截止后提交锁定，游戏继续跑约 2 周以降低不确定性（尤其对新 agent），然后**对"那些 episodes"跑最终 Bradley-Terry 锦标赛产出最终榜单**。

定榜用哪些 episode —— host 明确口径：

- host Addison Howard（2026-08-05）："The Final B-T tournament will use **all episodes between active agents across the whole competition**. Any episodes your agent played against now deactivated agents will not count."；Bovard Doerschuk-Tiberi（2026-08-06）：**双方 agent 在锦标赛时刻都仍 active 的 episode 才计入**（一方被新版本替换则该局作废）。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/732931
- host Addison Howard（2026-09-04）三条澄清：**团队分取两次提交中较高者**（一个队不能占两个名次，第二个名额是无下行风险的 hedge）；**平局按每方半胜计**；截止后加跑局数"希望增加，但不承诺具体多少"。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/739410
- Bovard（2026-09-07）：计划"把 BT 写进 private leaderboard（如果技术上可行）"——即 BT 分可能替代当前 Elo 展示。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/739788
- 官方 Timeline 页：**Oct 1 – 约 Oct 15 继续跑局直到 leaderboard 收敛，此后榜单定稿**。（来源：https://www.kaggle.com/competitions/kaggriculture/overview 的 Timeline 页，2026-09-19；页内 Entry/Merger 两个日期是未渲染模板变量，真实日期见本文 §4。）

matchmaking 社区实测观察（未经 host 证实）：

- 对手强度自适应：输棋后匹配池转向更弱对手（qihuaz，2026-09-06）。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/739746
- 提交后爆发期 ~16-17 局/小时（前 4 小时），之后降至 ~2 局/小时；agent ~100 局/3 天后基本收敛；"~98% 的最终 rating 在第 60 局前达成"。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/736314、/736219、/737492
- K 值衰减实测拟合：前 ~10 局平坦在 ~220，第 20 局悬崖降到 45-55，第 80 局触底 ~8.5（Syed Asad Ali 对 Ryo Hasegawa 帖的实测回应；Ryo 自己的拟合是 200·e^(−n/26)）。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/736219
- 强 path-dependence 投诉：identical agents 差 300-1400 分；早败极难翻身；top 池匹配面窄（Rayk Kretzschmar 帖 28 赞）。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/734000
- 强 agent "退役"现象：选手不上最强 agent 挂梯（防止被 BC/克隆），host 无对策（greySnow 高赞评论：PTCG 前车之鉴——第 3 名就是对 top1/top2 做 BC）。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/739179
- rating 显示 bug 实为前端问题，后端记录正确增减（Addison Howard 回复，2026-09-05）。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/739699

## 2. 提交运行时约束

来源（引擎实测，本机 kaggle-environments 内 `envs/kaggriculture/kaggriculture.json` + 实例化解析，2026-09-19；与官方 How to Play 页 Configuration Defaults 表一致）：

- `actTimeout` = **1 秒/步**（每回合行动超时）；`runTimeout` = **1200 秒/整局硬上限**；`remainingOverageTime` = **60 秒**超额池（每步超出 actTimeout 的部分从池里扣）。
- host Bovard（2026-09-07）确认 1200s 合理："两个 agent 并行运行，所以 1200s 是安全上限"。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/739874
- 社区口径与上面一致：1s/turn 软预算 + 60s/局 overage 池（首次模型加载也要靠它）+ 整局 1200s 硬帽；"1-2 秒/回合，100MB 包限制下深 MCTS 做不了"。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/737801
- 其他引擎配置默认值：episodeSteps=720（24 回合 × 30 天）、boardSize=10（四个 5×5 象限）、startingMoney=3000、maxMarketOrdersPerTurn=10（超出静默丢弃）、shedCapacity=100、weedSpawnChance=0.005、townShopUnlockInterval=3（有放回抽取、上限 8 个实例）、townShopSellInterval=4、townCenterSellInterval=24、seed 默认 null。（来源：官方 How to Play 页 https://www.kaggle.com/competitions/kaggriculture/overview，2026-09-19）

提交格式：

- 官方 Getting Started 页：提交**必须在根目录有 `main.py` 且含 `agent` 函数**；单文件直接交 `main.py`；**多文件打 tar.gz（main.py 在根）**；也可 notebook 提交；agent 文件会被放到 `/kaggle_simulations/agent/`，import 路径需自行处理。来源：https://www.kaggle.com/competitions/kaggriculture/overview 的 "Getting Started: Test Locally & Submit" 页（2026-09-19）
- 官方 FAQ 页（模板变量未在 API 渲染，网页版显示具体值）：Submission Size Limit / HDD / RAM / vCPUs 为模板 `${competition.*}`；**每日 5 次、仅最近 2 次活跃**为已确认值。来源：同上 FAQ 页。**大小上限社区口径 100MB**（Michael Timbs，"100MB package limit"）来源：https://www.kaggle.com/competitions/kaggriculture/discussion/737801 ；RAM/vCPU/磁盘具体数值未能从 API/CLI 取到（见"未解问题"）。
- 禁网（铁律级）：官方规则 §2.12 NO INGRESS OR EGRESS："episode 评估期间提交不得拉取提交与环境之外的任何信息，也不得向外发送信息"。来源：https://www.kaggle.com/competitions/kaggriculture/rules（2026-09-19）
- 第三方包：规则 §3.6.c 允许使用 **OSI 认证开源许可**的 open source code（不得限制商业使用）；引擎本体 kaggle-environments 可 pip 安装（Bovard，https://www.kaggle.com/competitions/kaggriculture/discussion/730708 ）。自带 Python 包需打进 tar.gz（社区帖演示多文件模块化提交：https://www.kaggle.com/competitions/kaggriculture/discussion/740817 ）。

## 3. 官方规则要点（外部数据 / 代码共享 / exploit / 团队纪律）

来源：官方 rules 页 https://www.kaggle.com/competitions/kaggriculture/rules（2026-09-19，全文 37KB 已存档）

- **外部数据与模型**（§2.6）：允许，除非 host 明确禁止；须"公众可获得、对所有参赛者平等无成本（或满足 Reasonableness 标准）"；**LLM 订阅费在小额合理范围内可接受**（示例：Gemini Advanced 订阅可，超过奖金数的专有数据集 license 不可）；自动化 ML 工具（AMLT）允许。
- **代码共享**（§2.1 Team Limits / §3.5.d / §3.6）：队伍上限 5 人；**禁止团队外私有共享代码/数据**（含跨队，除非合并）；**公开共享允许且必须放在 Kaggle 本赛区的论坛/notebook 上**，共享即视为按 OSI 许可授权；允许把公开代码用于提交。host Addison Howard（2026-08-28）："**Anything freely and publicly available is fair use.**" 来源：https://www.kaggle.com/competitions/kaggriculture/discussion/737788
- **公开代码共享截止**：host Addison Howard（2026-09-14）："the public notebook sharing deadline is **23 Sep at 11:59pm UTC**"（与 PTCG 赛同类政策——临近截止关闭代码共享）。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/741281
- **公开回放用于训练**：host Bovard（2026-09-01）："Using public replays to train, build, inform your submission is **allowed and encouraged**."（回放含你的提交的所有行动，公开可下载——规则 §2.11）。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/738837
- **利用引擎 bug/漏洞**：规则 §3.16 保留对"篡改提交过程或比赛平台任何部分"的参赛者取消资格/修改比赛的权利；§3.8.d 作弊、欺骗或其他不公平行为可取消资格。无"禁止利用引擎机制缺陷"的更细条款；官方对 doc/engine 不一致的处理原则（host Domino Weir，2026-08-04）："**engine is the source of truth**"，随后修文档（animal care +1、SELL fertilizer 合法、种当天必须浇水等 8 项澄清）。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/732450
- **引擎中期平衡补丁先例**：2026-08-06 host 发 Balance Changes（要求升级 kaggle-environments ≥ 1.32.6），说明**赛中改引擎有先例**，且旧 agent 变 stale。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/733431
- **团队与账号纪律**（§3.1/§3.5）：禁止多账号参赛；只能加入一个队；合并须在 merger deadline 前且两队提交数之和不超上限；私人共享=违规可 DQ。
- **仿真赛无 Private Leaderboard**（§2.10）；无手标数据条款；赢家义务（§2.8）：获奖者必须在论坛公开完整可复现方法描述+代码仓库链接，可能被要求录制讲解；Winner License = CC-BY 4.0，数据 Apache 2.0；奖金文件 2 周内交回，获奖约在收到文件后 30 天。

## 4. 奖金与截止

- 奖金：$50,000，前 10 名各 $5,000。来源：https://www.kaggle.com/competitions/kaggriculture/prizes（Prizes 页 + rules §1.5，2026-09-19）
- **Entry Deadline（接受规则截止）= 2026-09-23 23:59 UTC**（API `GetCompetition.new_entrant_deadline = 2026-09-23 23:59:00` 实证；Addison 对 Entry Deadline 语义的解释见 https://www.kaggle.com/competitions/kaggriculture/discussion/737431 ）。来源：kagglesdk GetCompetition API，2026-09-19
- **Team-Merger Deadline**：API 返回 `merger_deadline = None`（未单独设定）；官方 Timeline 页该处为未渲染模板。按 Kaggle 默认规则与 Entry 同日 = **2026-09-23 23:59 UTC**；社区帖有用户理解为"9 月 24 日"（737431 评论，时区换算差异）。
- **公开代码共享锁定 = 2026-09-23 23:59 UTC**（host 原话见 §3）。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/741281
- **终交截止 = 2026-09-30 23:59 UTC**（API `deadline` 实证 + Timeline 页）。
- 终局流程：10-01 至约 10-15 继续跑局至收敛 → BT 锦标赛定榜（§1）；获奖通知 email，1 周不回复视为弃权。

## 5. 天梯现状（2026-09-18 18:25 UTC 快照，`kaggle competitions leaderboard -d`）

来源：`kaggle competitions leaderboard kaggriculture -d`，CSV 已存 `references/data/lb-snapshot-20260919/`（抓取 2026-09-19，快照时间戳 2026-09-18T18:25Z）

- 参赛队伍数 **9,460**（API team_count 同值 9,460；此前工作区记的 6,806 已过时）。
- 分位：**#1 Majkel1337 = 3208.4**；#10 = 3023.3；#50 = 2887.4；**#100 = 2831.8**；#200 = 2772.8；#500 = 2630.1；#1000 = 2373.9；**中位数 = 780.9**；p75 = 1571.4。
- 门槛带：≥3000 共 12 队；≥2800 共 150 队；≥2500 共 745 队；≥2000 共 1598 队；≥1000 共 3971 队；score≤0 共 54 队。
- **prize 区（top 10）当前需要 ~3020+**；top 100 需要 ~2830。本队（约 4550 名档）所在分数 ~826，与 skill ~550-600（v9.2 现役最高 663.3）一致。
- 前 10：Majkel1337 3208.4 / SpaTaro 3122.5 / Sida Zuo 3087.4 / DSM 3077.5 / THIRD FARM CLUB 3073.9 / ymg_aq 3067.9 / Orbital Terraformer 3044.1 / QQ 3035.8 / Arda Ceylan 3034.3 / Otter Vibe 3023.3（注：CLI leaderboard 表与 CSV 分数在 #2-#6 略有分钟级抖动，以 CSV 为准）。
- 每行 SubmissionCount=2，印证"仅 2 个提交被跟踪"。

## 6. 讨论区与公开 notebook 情报

### 6a. 热门帖（标题 | 核心论点 | URL；全文 JSON 在 `references/data/web-intel-20260919/topic-*.json`）

- **Beware of scammers asking for source code**（51 赞，host Bovard 发）：有人私聊骗源码；只走 Kaggle 公开工件。| https://www.kaggle.com/competitions/kaggriculture/discussion/737885
- **1st Place(previously)- Submission Strategy for beginners**（88 赞，Ryo Hasegawa，2026-08-19）：前第一名的新手向提交/Elo 收敛攻略（K 衰减、爬分节奏、勿轻易重提未受损 bot：首败对最终分区间伤害极大）。| https://www.kaggle.com/competitions/kaggriculture/discussion/736219
- **How path dependent is the current leaderboard rating?**（28 赞）：早败 path-dependence、identical agents 分差 300-1400、"3k 掉到 2k"案例、刷初始爆发期赌分现象。| https://www.kaggle.com/competitions/kaggriculture/discussion/734000
- **Crucial Information...: Documentation vs. Engine Discrepancies**（28 赞）：8 项文档/引擎差异官方逐条确认，"engine is source of truth"。| https://www.kaggle.com/competitions/kaggriculture/discussion/732450
- **Balance Changes**（41 赞，host）：8 月初引擎平衡补丁+需升级 ≥1.32.6，旧 agent 变 stale。| https://www.kaggle.com/competitions/kaggriculture/discussion/733431
- **Will the competition be easily solved?**（20 赞）：top 选手 turns 1-51 在 13 个实例 8 个种子上 byte-identical、不响应价格 → 开局是硬编码剧本；公共 notebook 同源克隆泛滥。| https://www.kaggle.com/competitions/kaggriculture/discussion/732902
- **Are Agents Really Competing Against Each Other?**（15 赞）：交互主要通过共享市场+商店解锁 RNG（与 weed spawn 共享随机流，固定 seed 无法完全固定商店——yhay81 实测）。| https://www.kaggle.com/competitions/kaggriculture/discussion/732613
- **End-to-End RL Is Harder Than It Looks**（19 赞）/ **Is Pure Self-Play PPO viable?**（19 赞）/ **Determinism is an argument against RL here**（8 赞）/ **Learnings from PPO to 80k terminal cash**（17 赞）：RL 共识=样本效率低、720 步长视野、AMM 定价难学；PPO 天花板 ~20k-80k vs 规则系 150k+；top 中 **hwe owe 自述第 8 名不用 RL**（在试 ML 学卖出时机）；混合（规则主导+RL 门控）是目前最现实的 RL 形态。| /discussion/736567、/734952、/737937、/738619
- **If I'm Going to Write Rules Anyway, Why Train a Model? (BC)**（34 赞）：Zhenyu Zhang 自述 LB 十强用的是 heuristic agent（非 BC）；BC 只能到 50k vs 公开 NB 140k；BC+RL 超不过"父母"的多方复现。| https://www.kaggle.com/competitions/kaggriculture/discussion/738079
- **does copying opponent help?**：destbreso——克隆系"销售提前一回合"是系统性小优势（对手卖价折旧），克隆军备竞赛互反；行为克隆检测容易（确定性强）。| https://www.kaggle.com/competitions/kaggriculture/discussion/740588
- **Your opponents are probably replaying the same tapes you are**：公开回放有效行为多样性远低于回放数。| https://www.kaggle.com/competitions/kaggriculture/discussion/740437
- **RNG seed recovery? / Reverse engineering the seed**：种子可暴力恢复但需 9-24 天观察且依赖双方动作（weed/shop 共享 RNG），赛中不可行，多人独立复现结论。| https://www.kaggle.com/competitions/kaggriculture/discussion/739084、/739388
- **Why aren't top solutions using 4th quadrant?**：第 4 象限 ROI 不足（买地+fib 雇人+晚投产），有人留外圈空地减少走路。| https://www.kaggle.com/competitions/kaggriculture/discussion/734308
- **Will code sharing also be closed...（PTCG 先例）**：见 §3/§4（host 确认 9-23 共享锁）。| https://www.kaggle.com/competitions/kaggriculture/discussion/741281
- **runTimeout is inherited at 1200s**（Bovard 确认并行安全）| /discussion/739874；**Is there a time limit on each agent's turn?** | /discussion/737801。
- **mikelou1**：没有 private test，无法对 LB 过拟合；公开 notebook 约占 LB 的 90%。| https://www.kaggle.com/competitions/kaggriculture/discussion/741722

### 6b. 公开 notebook（`kaggle kernels list --competition kaggriculture`，2026-09-19；原件快照在 `references/data/intel-notebooks/`）

- **bovard/kaggriculture-getting-started**（1154 票）：官方教程（Melon Maxxer 示例、提交流程）——事实上的官方 baseline 教程。| https://www.kaggle.com/code/bovard/kaggriculture-getting-started
- **boatlee/v16-rc5-high-score-8c-4s-premium-market-lead**（314 票）：8 胡萝卜/4 草莓 高分开局+溢价市场前置。| https://www.kaggle.com/code/boatlee/v16-rc5-high-score-8c-4s-premium-market-lead
- **kaitofukami 系列**（v27/v48/v21.1 等，130-203 票）：Holdout 记分法（X/Y 对 Fixed panel 胜率）+ 路线快速化迭代流派。| https://www.kaggle.com/code/kaitofukami/25-27-strict-future-v27-midgame-meta-reset
- **raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta**（192 票）：回放狩猎笔记——引擎细节（melon 窗口、SELL 只看 shed、化肥可卖）+ 公开 meta 策略簇与强度排序。| https://www.kaggle.com/code/raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta
- **raykkretzschmar/kaggriculture-rank-your-agent**（137 票）：对固定阶梯打本地天梯的评测框架（reference agents 见其 dataset `kaggriculture-reference-agents`，3498 下载）。| https://www.kaggle.com/code/raykkretzschmar/kaggriculture-rank-your-agent
- **yhay81/shop-router 系列 + six-day-public-state-fieldbook**（123-133 票）：商店路由/公开状态实测流派。| https://www.kaggle.com/code/yhay81/shop-router-0909
- **tetsutani 系列**（103-142 票）：自适应耕作/商店-牧场分工。| https://www.kaggle.com/code/tetsutani/adaptive-farming-strategy-for-kaggriculture
- **thomastschinkel public-state-router**（99 票，自称 74.5%/93.8% 胜率）。| https://www.kaggle.com/code/thomastschinkel/kaggriculture-public-state-router-74-5-win-rate
- **busyaprime/kaggriculture-five-days-of-the-ladder**（2026-09-05）：见 §6c Crop Dusta 分析。| https://www.kaggle.com/code/busyaprime/kaggriculture-five-days-of-the-ladder
- **destbreso/x-ray-your-agent**（44 票）：每日自动 x-ray 当前榜首（ kinship/克隆检测/经济剖面）；salemali7/kaggriculture-2900（77 票）自称 2900+；mzcao7 LightGBM+XGBoost 2476.8。| https://www.kaggle.com/code/destbreso/x-ray-your-agent
- 数据集侧：`kaggle/kaggriculture-episodes-*` 官方每日回放包（每日 ~500-700 局，20GiB/日上限约束）；`georgymamarin/kaggriculture-episodes`（20GB 全量整合，25408 下载）；`raykkretzschmar/kaggriculture-reference-agents`（3498 下载，本地评测阶梯的 reference agents）。| https://www.kaggle.com/datasets/georgymamarin/kaggriculture-episodes

### 6c. Crop Dusta / 顶部选手线索

- **"Crop Dustas" 现列公榜第 34 名，score 2912.2**（2026-09-18 榜快照）。来源：`references/data/lb-snapshot-20260919/`（kaggle.com，2026-09-19）
- busyaprime《five days of the ladder》（2026-09-05，分析 09-01~09-05 每日回放）：**Crop Dusta 是 103 个采样 agent 中唯一 5 天全勤的**：178 局，日胜率 54/52/62/53/75，总胜率 56.2% [48.8, 63.3]（最后一天 75% 仅 8 局）；同榜高频对手 Giulio Ravasio（88 局，57/60/33）、Jesse Bullard（71 局）、MtN、OceanMix。来源：https://www.kaggle.com/code/busyaprime/kaggriculture-five-days-of-the-ladder（2026-09-19 抓取，原件在 intel-notebooks/）
- 741281 帖中社区用户 Joseph Ayanda 称呼 **"peikopon (Crop Dustas)"** 并请求其在 9-23 共享锁前开源——即 Crop Dustas 团队账号疑为 **peikopon**，未获回应；无更多公开技术细节。来源：https://www.kaggle.com/competitions/kaggriculture/discussion/741281
- 现榜首 Majkel1337 无公开 notebook/技术帖可检索（WebSearch 2026-09-19 无结果）。

## 7. 官方 baseline bot 与示例代码

来源：官方 "Getting Started: Test Locally & Submit" 页与 "Quick Start Agent" 页（https://www.kaggle.com/competitions/kaggriculture/overview ，2026-09-19）

- **三个内置 agent**（可按名调用）：`"pass"`、`"random"`、**`"starter"`（确定性 baseline）**——`env.run([agent, "random"])` 或 `env.run(["main.py", "starter"])`。
- 官方 Quick Start Agent = 一个小麦循环 agent（BUY_SEED→PLANT→WATER→HARVEST→SELL，age≥2 收割），页面含完整代码；本地包另有 `kaggriculture_beginner` 环境（kaggle-environments 内 `envs/kaggriculture_beginner/`）。
- 环境安装：`pip install -U kaggle-environments`；本地跑+回放导出全流程见 Getting Started 页；engine 源码在 https://github.com/kaggle/kaggle-environments （`kaggle_environments/envs/kaggriculture/kaggriculture.py`）。
- 官方教程 notebook：bovard/kaggriculture-getting-started（1154 票，§6b）。

## 附：本队状态快照（2026-09-19，kaggle CLI）

- `kaggle competitions submission-limits`：今日已提交 1，剩余 4；生涯提交 27。
- 最新提交 56336584（v13.8 sprintA，2026-09-18）公榜 533.4；队内现役最高为 v9.2（55902180）663.3、v10.3（55943264）658.2（来自 `kaggle competitions submissions`，2026-09-19）。
- 对照 §5：要进 top 100 需 ~2830，top 10 需 ~3020——本队分数段（~530-660）与 prize 区差一个数量级段位；desk 上下文"爬 prize 区"以 §5 分位表为锚。

## 未解问题

1. **RAM / vCPU / 磁盘的具体配额**：FAQ 页模板变量（`${competition.AgentRam}` 等）经 API/CLI 无法解析成数值；仅有社区口径 100MB 包限制。网页 FAQ 需 JS 渲染，后续可用浏览器抓一次。
2. **Team-Merger Deadline 的官方显式日期**：API merger_deadline=None；按默认=Entry 同日 09-23 23:59 UTC 推断，未获 host 直接确认（社区帖 737431 有"24 Sept"的说法）。
3. **BT 锦标赛是否含截止前全部历史局**：732931 host 已答"全程、且双方 active 才算"；但 731587（09-15 提问）再次追问"只算 10-01~10-15 还是全程"截至抓取时无 host 回复——两处口径以 732931 为准，但 10 月加跑局的局数/速率无承诺（739410）。
4. **新提交初始 rating 的官方数值**：官方只说"default rating"；社区口径 ~600（737571/739746 评论），未证实。
5. **"starter" baseline 的强度与脚本位置**：内置名已确认，但其具体策略代码未逐行核对（在 `envs/kaggriculture/kaggriculture.py` 内，未读）。
6. **Crop Dustas 的技术与人员背景**：仅 34 名/2912 分 + five-days 统计 + peikopon 账号猜测；无公开代码或作者自述。
7. **终局 10 月跑局的算力/局数是否提升**：host 明示"希望但不承诺"（739410）。
