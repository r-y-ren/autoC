# 竞赛情报增量快扫（2026-09-19 存档 → 2026-09-20）

抓取日期：2026-09-20（榜单快照时间戳 2026-09-20T02:21Z，其余为当日 10:00-11:00 本机会话抓取）。
通道：`kaggle competitions topics list/show` + kagglesdk `discussions.discussion_api_client.get_topic`（主楼正文）、`kaggle kernels list/pull`、`kaggle competitions pages list --content`、`kaggle competitions leaderboard -d`、`pip index versions kaggle-environments`、WebSearch。
对照基线：`web-intel-20260919/`（12 官方页 + 43 帖）、`digests/web-comp-intel-2026-09-19.md`、`lb-snapshot-20260919/`（09-18T18:25Z）。

---

## 1. 讨论区增量

### 1.1 09-19 之后新建（6 帖，全部抓回 topic-full-*.json）

| 帖 | 时间 | 核心论点 |
|---|---|---|
| #742035 ⚠️ Scam alert：假 "Kaggle Staff"（bovarddd）索要代码 | 09-19 05:03 | 有人冒充 bovard 邮件索要完整提交代码（48h 限时否则"取消奖牌资格"）；假账号已由真 bovard 移除。**我方不给任何代码给私信索要者。** |
| #742063 Overview game discrepancies | 09-19 11:58 | Overview 表 melon 首收 10 天仍未改（实际 6，见 #732450）；"每天必须浇水"实为隔天。文档与引擎的差异未修复。 |
| #742078 Minimize time, maximaze money | 09-19 16:23 | 新手问：头部如何同时最小化时间、最大化利润（无回复）。 |
| #742083 Disproportionate Rating Drop After a Close Defeat | 09-19 17:31 | 103,148 vs 103,147 输 1 美元被扣 106 分。评论区（Gideon Oba）确认机制：**胜负只看终局钱数，赢=多 $1 也算赢；不计分差；两个确定性相同 bot 会平局**。涨落由 Elo 差驱动。 |
| #742111 🪰 果蝇 connectome 玩 Kaggriculture | 09-19 21:10 | Janelia MaleCNS v1.0（728 神经元/35,704 突触）无学习娱乐帖（notebook 见 §2）；"脑死亡变体（沉默全部下行神经元）挣得最多：种草莓等 29 天"被作者当作本游戏真理之一。 |
| #742120 agents are becoming thieves | 09-19 22:19 | 新手情绪帖：agent 互相抄袭（无回复）。 |

### 1.2 已存档帖新增回复（4 帖，新评论已抓）

- **#731587（final evaluation 官方帖）**：Alex Paul 09-19 22:16 再次追问 **BT 终榜拟合范围：只用 deadline 后的局，还是全部历史局？平局算半胜吗？** —— 截至快照**官方仍无答复**（同题 09-15 Kavinkumar 也问过）。→ 直接影响终榜预估口径，见 §8 未解问题。
- **#731215（Daily Top Episodes）**：Noberto Frota 09-18 问 BC 数据偏 top agent 是否伤泛化；Georgy Mamarin 09-12 的实测：20GiB 日预算 43/44 天顶满，日均 episode 数 928（07-31）→657（09-11），单回放 22→31MiB；**日 dumps 的 avg_score 中位数自 08-04 起稳定在 2,735–3,080**（头部对局的钱量口径）。
- **#738619（PPO to 80k）**：Alex Paul 09-19 问 hybrid 架构里 RL 到底输出什么（选整计划 vs 调参数），"动作空间设计是成败关键"。
- **#741722（generalization/overfitting）**：mikelou1 建议**直接下载公开 notebook（约占榜 90%）跑 mini-ELO 锦标赛做本地评估**；Zukas F. 给出 dev/holdout 分离方案。

### 1.3 从未存档但高相关（本次补抓主楼+评论，topic-full-*.json）

- **#733924（08-09，Revanth Tambisetty）top-5 开局三簇**：**top-5 中 3 队用一模一样的开局**（逐种子数、逐雇佣数一致）= 当时的公开参考 agent，构成 **ELO 天花板 3,117–3,131**；其上只有 2 个不公开任何东西、开局签名匹配不到任何已知 notebook 的队（当时的 rank1/rank2）。附 notebook `revanthtambisetty/two-private-bots-beating-kaggriculture-meta`。→ "同开局=天花板，破顶靠私有开局"的直接证据。
- **#732623（08-03，David Pedersen）MELON 为何碾压（含数学）**：价格崩塌由 T+above 函数决定；TOMATO（T=200, sqrt）23 格规模自毁到 ~$1；MELON（T=300, sq）138 单位几乎不跌；STRAWBERRY（T=100, linear）超 T 快。**SELL 排 BUY 前**（先卖回血再买）；NE 地早买是陷阱；分列分区雇佣工人省路径。
- **#735119（08-14）终局经济学四对照实验**：day-26 后停止新种子管线 = **+781.88/局（16/16 为正）**；静态晚期雇佣上限 = **−233（7 正 9 负，不可信）**；终局原则="可达→完成→入棚→卖出→变钱"的现金转化链，非活跃度。
- **#739273（09-03，sobameshi，19 评）回放测量管线**：14 个公开实现 × 96 新种子 round-robin → **是阶梯不是猜拳**：91 个时序对中 86 个"新的赢旧的"；相邻代胜率 60–80%，隔代 90–100%；排序与终局钱数高度一致。交互面小，强经济计划几乎不依赖对手；对镜像/磁带对手加小型反应层明显受益。评论区：v40 3/4 败因是同一天 2 头牛没 FEED 死掉（每头 $12–32k）；**SpaTaro 是 top10 里唯一每场都对局出独特策略的（非静态 policy book）**；sobameshi 自述 rank~400 是 tape-router，runtime agent 1640 分 rank~2000。
- **#741320（09-14，-9 票）"RL 是方差税"热帖**：主楼称 closed-loop 输给静态 macro-schedule + 市场队列地板操纵。**关键在评论：Mahog 09-18 "2nd place 刚确认他在用 RL（而且我确信 top10 里还有更多人在用 RL）"**；aisormo P.H 称 SpaTaro 的 agent "复杂得多"，Swachhith B 附和"他好像把 RL 搞定了"。
- **#741743（09-17，27 赞）RL 进银牌区**：BC 暖启动（官方 top-match 回放或自建 top 队回放管线）→ PPO，**macro 级决策**，~300k 局；Snorlax 确认 PPO。
- **#741792（09-17）同模式对手**：**linkinpony (Sayaka Miki) 确认自己的 agent 是 RL**（macro），"学成了局部最优，可被 hack（见我与 ymg_aq 的对局）"。
- **#741258（09-14，KKY）**：RL 300M env steps 后**饱和在 80k 终局钱**；100+ 实验两周。
- **#740022（09-07，Roy Wei，26 评）**：端到端 RL 350M steps，对昨日公开静态 90k vs 122k；destbreso 建议用回放合成对手代替静态 tape（避免表示偏置）。
- **#741730（09-17，KKY self-play）**：静态对手 ckpt 转 self-play；Adam+恢复 optimizer 才 work；exp3 打不过强开源对手。Mahog 09-20 01:39："我的模型终于学会用动物了，但又不肯种庄稼了"。
- **#741891（09-18）价格公式实现**：`price = max(1, base + sign·amp·f(|inv−I0|))` 对规格表 9 资源全对上；**WHEAT/EGG 供给过剩侧是 log 曲线，2×T 时仍有 76–78% 底价；CARROT/TOMATO/MELON/STRAWBERRY/MILK/WOOL 都在自己 T 附近打到 $1 地板**（MELON T=300 vs STRAWBERRY T=100 的绝对单位差比 above_target 更重要）。
- **#741907（09-18）每日传送机制**：每天结束 farmer 传送回 (4,4)、所有 hand 消失、HIRE 价重置 → 走路税 ~15pp，收益在 ~5 格饱和；melon 收入≈wheat 的 3 倍（17 次收获 vs 61 次）；**肥料比动物本体值钱**（鹅循环 +$2,725 vs 蛋 $1,250）；三个坑（双单位同时 PLANT 1 种子=全卡死、FEED 要在单位背包、(4,4) 规则顺序）。**README 说 melon max_yield_day=10，代码是 12**。
- **#741935（09-18）寻路开销**：`action_weight/(distance+1)` 贪心 Top-10 + depth-2 look-ahead 防超时。
- **#741988（09-18）share-lock 提醒**：**公开 notebook/代码共享锁 09-23 23:59 UTC**（引 #741281 host 确认）；呼吁有 ≥2800 活体的队公开老代体（公开件 only，拒绝 DM 索码）。
- **#742005（09-18）**：Gurobi/求解器在提交环境可行性讨论（无网+许可证 → 实际用 OR-Tools/SciPy/启发式）。
- **#741653（09-16）**："这是 coding agent 互殴大赛"；评论（Exposed 09-18）：**LLM 还造不出顶级 agent，但在顶级公开 agent 上改一行拿过 +147 分**。

## 2. Notebook 增量（拉回 20 个 → intel-notebooks/fresh-20260920/）

### 2.1 王牌件：The 2945 Farm（thomastschinkel，141 票，09-19 发，全开源）
同文件三份克隆（laveshjadon/kagriculture-winning-notebook、sunil123kumar/kaggriculture-top-10-public-bots = 逐字节同文）。要点：
- **架构=路线磁带回放器 + 反射层栈**（每层读公开观测、改一类决策、层层包装，`agent = globals().pop('agent')` 结尾）。磁带选自城镇首批商店解锁；层来源：yhay81 shop-router、Ahmed V39/V40、prvsiyan、Dmitrii Gluzdov、tetsutani、aurax7 等。5,760 行 856KB 单文件，纯标准库 ~3ms/回合。
- 榜上 **2944.7**（submission 56269928；前代 2956.6）；**对 top-10 公开 notebook 519-21（96.1%）**，官方引擎 80-0；对 17 个 reactive bot 645/680。**最高公开 notebook 仅 2750.2**。
- 八课：①雇佣按边际定价（fib），六羊扩张的两只手是当日 #12/#13 雇=$377/天，非羊毛日 SL2 砍手 +15/−0；②**羊提前 1 天放=5 次剪毛而非 4**（day-11 放：17/20/23/26/29），VE1 在前 3 店有 2 yarn 时 day-11 承诺，+8/−1，对 reactive 24-0；③**CARE 才是动物产出大头**（care 攒 1 单位/天，牛 3 奶/羊 4 毛/鹅 2 蛋 vs 1），未喂食当天清空攒量，CAPHARV 防库存 6/4 上限溢出 +20/−0；④**市场清单是订单簿**：双方同序号 slot 锁步、逐单位同价成交，slot 位置决定谁卖进谁的洪水；⑤rival_sold = inv′−inv+town_draw−own_sold（$1 地板之上精确），RACE 提前抢卖 ≤40 回合（day 8 起），RACEPX/RACEGATE 防冲进已低于 base 的书，**PREDICT 用 451k 条售出事件（1,000 局近期 top-25）匹配对手流并抢先卖**；⑥棚 100 格，午夜超量销毁（OVERFLOW/SHEDROOM/COURIER，SHEDROOM 翻 18 局且每局差 <$1000）；⑦胡萝卜/小麦模拟择优；⑧（截断）。
- **§6 没解决的问题（最关键）**：**对 09-15~17 当期 top-10 七队 ladder 0-36**。带精确 ledger 复盘 24 局：**day 10 前领先（melon 竞速是我方的），day 11 后全部输光**。→ 公开谱系与真正顶队的差距在 day-11 之后的某段，不在开局点火。
- 实务：**Kaggle 镜像仍带 kaggle-environments 1.29.3，其 kaggriculture 引擎过时 → notebook 内需联网 pip 装 1.32.7**；评估要用 common random numbers 固定商店解锁、双席位。

### 2.2 开局点火微观结构（解释 2600+ 打法的核心新料）
- **goodpjw2008/melon-threshold-squeeze-2749**（09-19，2749 实测）：①引擎把双方同序号订单锁步逐单位同价成交 → **turn-0 wheat round-trip 谁小谁赢**（10 单位对 70/69/78/5 全部 ≥0.98 胜率；V45 默认 70）；②**melon 阈值**：V4x 谱系 day-0 种子购买由 R124 资金层按现金裁剪，镜像局 step-17 约 $212 买 2 个 melon 种子，**被对手磨掉 ~$50 就只买 1 个 → 终局差 ~$1.3k**（一颗 melon 果实 ≈ $1.2k）；③**step-1 squeeze**：V4x 全系 step-1 固定发 `[SELL 13(空), BUY 5, HIRE×5, COW 2, SHEEP 2]`，我方改发 `[BUY 90(slot0), SELL 90(slot1), BUY 5(slot2), …]`：slot0 我买 90 抬价，slot1 对手 BUY 5 对着抬高的书成交、我 SELL 90 回填 —— 对不在此窗口买的对手**精确中性**；④sale race 层（4 回合 tape 售卖提前 + 前置 SELL + 预留窗 24，源 sdy623 [2842]）。**诚实边界：三改全是对公开谱系的赛跑，对私有 top 无效（他们既不 round-trip 也不在 step-1 slot2 买）；两天内私有 V46 fork 已比任何公开版卖得更早；~2700 段位的惜败多由同回合卖单竞速决定**。
- **tetsutani/demand-preserving-turn-sale-timing**（54 票；09-19 时最高分公开 notebook 2750.2）：step-1 现金 ≥$2,860 时买 22 单位临时 WHEAT、step-2 静回合回卖；其余 production stack（route/clone/race/storage/herd/weed-repair/compaction/3 回合售卖提前/terminal）原样。
- **nathanjacob/pipe-7-wheat-microstructure**（62 票）与 **jaxa623/2802-two-identical-agents**（70 票，sdy623）：同源微结构线（已拉回，供 chain 溯源）。
- **dmitriigluzdov/a-smaller-market-shock**（Big3 之一）：day-0 在 (2,4) 微种 wheat、day-2 收割后重建牧场（已拉回）。
- **haideptry/countering-the-big-3-meta**：把公开 meta 归纳为 **Big3 = V50（Ahmed）/ tetsutani 22-wheat / Gluzdov Shock**；克隆潮导致共同调度→市场灾难（day-17 羊毛集体倾销）；反制三件套（Anti-Shock 吸收 step-1 抢购 / 羊毛 front-run 提前 1-2 回合 / day-12 起 tomato pivot 吃无人竞争的次级书）。100 局自测 84%（**自我背书数字，谨慎引用**）。
- **haideptry/the-2950-peak-farm**（09-20 02:14，最新）：zero-idle 开局（(2,4) 预插微小麦日循环，宣称 +$1,045 复利）+ day-11 yarn 抢承诺 + RACE 反射引擎；对 2200-2600 池 +$28,864。**营销味重（三行表格全是 +$1,045、"climb straight to the top"），机制描述可读，数字不可外引。**

### 2.3 V4x 谱系本体（补拉源头件）
- **ahmedberatozer/V49**：= V48 + 2945 Farm 开源的 7 个经济层（COURIER/CARROT/HERD/FERT/ORDERPRI2/CAPHARV/SHEDROOM），holdout vs V48 副本 **96/0/0（+2807±571）**；明确不采纳 Thomas 的 SL2/VE/VT（与 V48 自身 V233 六羊项目冲突 −12k~−16k）。
- **ahmedberatozer/V50 Early Yarn Commit**：V49 + v233x（前 3 店 2 yarn 时 day-11 六羊承诺：yarn 世界 79/1 +3674±380）+ weedlag（weed 阻塞恢复）。
- **ahmedberatozer/V48 Clear the Queue**（82 票）、**V47 Reactive Market Coordination**（56 票）：队列清理/反应式市场协调本体（已拉回）。
- **alperen5252525/First-in-Line 2746**（59 票）：V48 核 + `_ADV_LOOK=8` 售卖前移 + 黎明前库存压力记账；**Market-Rhythm**（16 票）：售卖前移 ≤24 回合 + 对三种假想对手队列（同序/名义价优先/反序）做有界相邻交换搜索，目标函数 `mean(own−0·rival) − 0.25·scenario_spread`。
- **aurax7/shop-router-reactive-v7**（31 票）：reactive 路线代表（已拉回）。

### 2.4 方法论件
- **destbreso/every-community-agent-one-arena**（09-20）：61 个社区 agent 公开数据集 + arena.py；**bit-exact C++ 引擎 50μs/局 vs 官方 241ms（~4800×）**，15,872 局全矩阵 4 分钟；行为族=同参考场终局钱向量相同才算同 agent；64 个"前两店"世界；**seat-0 结算优先只在接近平局的 pairing 上起作用**（98/124 pairing 席位差 0）；**全部区分度 92% 来自 top 四分位对手**（26% 的计算量）；强 notebook 面板排序对真实 ladder 对手**会反转**（面板对、总体错）→ 评估须 population weighting。x-ray 系（destbreso）一贯方法论升级。
- **takamichitoda/flyfarmer-connectome**（果蝇，玩笑件，结论见 §1.1 #742111）。
- **guruprasaathas111/game-theoretic-master / master-engine-v4**：数学包装厚、可验证提升低，仅存档不采信。

## 3. 引擎 / 规则变动

- **kaggle-environments：最新仍为 1.32.7**（pip index 实测；本机 vendor 1.32.7+nodeps 与其一致）→ **09-19 后无引擎更新**。
- **官方 12 页（pages list --content 全文 diff）：与 09-19 存档逐字节一致，零变化** → 无新 balance change 公告（最后一次社区可见的平衡调整是 08-15 #735311 讨论期）。
- 实务坑（来自 2945 Farm）：**Kaggle 提交镜像自带 1.29.3，kaggriculture 引擎过时**，构建期需联网升级 1.32.7（与 09-19 digest 的包限制口径一致）。
- 时间线未变：**公开 notebook/代码共享锁 09-23 23:59 UTC；entry deadline 09-23；终交 09-30**（#741988 重申锁）。

## 4. 榜单动态（09-18T18:25Z vs 09-20T02:21Z，原始件 lb-snapshot-20260920/）

| 指标 | 09-18 | 09-20 | Δ |
|---|---|---|---|
| 队伍数 | 9,460 | 9,597 | +137（≈82/天，仍在新队涌入） |
| #1 | Majkel1337 3208.4 | Majkel1337 3295.1 | **+86.7**（≈52/天） |
| #2 | SpaTaro 3122.5 | DSM 3140.5（SpaTaro→#6 3043.6） | **头部洗牌** |
| #3 | Sida Zuo 3087.4 | THIRD FARM CLUB 3058.6（Sida Zuo→#10 3014.1） | 洗牌 |
| prize 线（#10） | 3023.3 | 3014.1 | **−9.2** |
| top50 | 2887.4 | 2871.7 | −15.7 |
| top100 | 2831.8 | 2820.4 | **−11.4** |
| top500 | 2630.1 | 2646.3 | +16.2 |
| 中位 | 780.7 | 780.8 | ≈0 |

解读：
- **头部高波动、边界反而在"通缩"**：#1 两日 +87，但 #10/#100 线下移 ~10 分 —— 上段 K 因子下输局扣分狠（与 #742083 的 −106 案例一致），近似分数段互吃。**对终榜名次预估：prize 线不应按当前分数线性外推上涨；终局 BT 重拟合口径未定（§8）是更大不确定性。**
- 冲进 top20 的新面孔：Artem The Farmer（2795.5→3002.2）、吃白饭的大肥鱼（2466.8→2983.9）、Kaggledew Valley（2353.3→2951.9）、THUNDER THUNDER（2914.0→2986.7）——**终局期 500+ 分的两日跃迁真实存在**（提交活跃 + 上段 K 因子 + 对手洗牌）。
- top500 以下缓慢通胀（+16/两日），中位不动 → 场内"2,600+"人口在扩大（与 daily dumps avg_score 中位 2,735–3,080 互证）。

## 5. 外部网页（09-19 后）

- **无重大新外部情报**。Reddit r/reinforcementlearning 帖为开赛期旧帖；X/LinkedIn/YouTube 均为 Google 5-Day AI Agents Intensive 课程宣传（Kaggriculture 为结业挑战）；新见一个课程向 GitHub 学习仓 deepeshumrao/kaggriculture-agent（入门水平，无情报价值）。GitHub/博客无终局 meta 新料。

## 6. 对"开局点火竞速"问题的新线索

1. **点火=同序号 slot 锁步订单簿上的三段微观竞速**（2749 号 notebook 给出最完整机制）：turn-0 round-trip 谁小谁赢；step-1 squeeze（slot0 大买抬价→对手 slot1 付费→slot1 回卖填书）对窗口外购买者精确中性；**day-0 step-17 的 melon 种子现金阈值（~$50 → 少种一颗 → ~$1.3k 终局差）** 是点火攻击的真实目标函数。V45 系的 step-1 订单序列是公开固定的 → 可精确针对；但**私有 top 既不 round-trip 也不在 slot2 买，点火武器对他们无效**。
2. **开局面不决定终局**：2945 Farm 对 top-10 七队 0-36，**day-10 前领先、day-11 后崩**；同开局=公开簇天花板 3,117-3,131（#733924，08-09 口径）。→ 我方若以点火为主攻，只能赢公开谱系，赢不了 day-11 后的真差距段。
3. **终局 meta 双轨**：公开面 = V4x/2945 谱系的磁带+反射+售卖竞速（2750 公开顶）；私有面 = **RL 实锤进入最顶部**（#2 名确认 RL；linkinpony RL；RL 银牌区路线 BC(top回放)→PPO(macro)；SpaTaro 每局出独特策略=疑似非静态）。BT/W-L 口径下"稳赢公开谱系"与"RL 泛化"两条路线都活着。
4. 售卖竞速已军备化到**同回合**：PREDICT 用 451k 售卖事件库预测对手卖点抢先卖；私有 fork 两天内卖得比公开版更早；~2700 段位惜败多由同回合卖单竞速决定 → 2650-2750 段的提升点在 sale-timing 层而非开荒层。
5. 单行改动 +147 分的个案（#741653 评论）→ 终局期对 top 公开件做外科手术式 patch 的性价比可能高于自研整套。

## 7. 未解问题

1. **BT 终榜拟合范围官方未答**（#731587 两度追问）：只用 10-01 后的局还是全部历史？平局是否半胜？→ 直接决定终榜预估公式。
2. **top-10 在 day-11 之后赢公开谱系的东西到底是什么**（2945 Farm 作者都没 solve；唯一量化线索是"mel on竞速赢、day-11 后崩"）。
3. SpaTaro 的"每局独特策略"= 在线规划还是 RL+随机化，无公开证据（只有他人描述）。
4. 2950-peak-farm / countering-big-3 的自测数字未经第三方复核，haideptry 两件存营销动机。
5. 头部 K 因子下 prize 线两日 −9~−16，终局 BT 重拟合后的 prize 线口径无法从公榜直接外推。

## 8. 原始件清单（本 digest 上游）

| 路径 | 内容 |
|---|---|
| `references/data/web-intel-fresh-20260920/topics-page-1..10.csv` | 全论坛 197 主题清单（按最近活跃） |
| `references/data/web-intel-fresh-20260920/topic-full-*.json`（28 件） | 新建/新回复/补抓主楼正文（kagglesdk get_topic，含 content HTML） |
| `references/data/web-intel-fresh-20260920/topic-*.json`（27 件） | topics show 的评论流存档 |
| `references/data/web-intel-fresh-20260920/pages-all-content-fresh.csv` | 官方 12 页全文（与 09-19 diff=零变化） |
| `references/data/web-intel-fresh-20260920/bodies-digest.txt` | 主楼正文可读版 |
| `references/data/intel-notebooks/fresh-20260920/*.ipynb`（20 件）+ `notebooks-digest.txt` | 新增 notebook 原件与要点摘要 |
| `references/data/lb-snapshot-20260920/kaggriculture-publicleaderboard-2026-09-20T02_21_40.csv` | 公榜全量快照（9,597 队） |
