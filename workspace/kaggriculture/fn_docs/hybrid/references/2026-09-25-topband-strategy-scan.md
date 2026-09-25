# 2026-09-25 头部对手与机制口径联网调研（analysis22 子代理 B）

> 任务：搞清游戏机制权威口径 + 头部对手"我们没有的机制"，为优化方案提供外部长板清单。
> 抓取日期统一为 **2026-09-25**（除标注 [前次] 者——那三条来自本战役已入库 digest，原始抓取日期见括号）。
> 通道：kaggle CLI 2.2.4（`competitions pages --content` / `topics list` / `kernels pull` / `leaderboard -d`）+ pipx venv kagglesdk `discussions.discussion_api_client.get_topic`（取讨论帖主楼正文）+ GitHub REST/raw + WebFetch（Kaggle SPA 对 WebFetch 不渲染，弃用）。原始抓取件缓存于 `/tmp/kbscan/`（临时，未入库；结论以本纪要为准）。
> 纪律：逐条带来源 URL+抓取日期；查不到就写"未找到公开来源"；凡他人自报实验数字均标注"自报"，不作为我方承诺。

---

## 一、评分口径结论（先答"publicScore 怎么算"）

**结论：publicScore 不是逐局均值、不是窗口/分位、不是 margin 聚合——是 Elo 式 skill rating（每局只看胜/平/负），终榜另做 Bradley-Terry 拟合。净 margin 与分数变化不对称是机制使然，官方明文。**

1. **官方明文（Evaluation 页，https://www.kaggle.com/competitions/kaggriculture/evaluation ，2026-09-25 抓取）**：
   - "The actual coin difference in a match does not affect the rating change—only the win, loss, or tie outcome matters."（钱差不影响 rating，只看胜负平）
   - 每日最多 5 提交；**只跟踪最近 2 个提交**，且这 2 个也用于最终评估；榜单只显示你分数最高的 bot；新 bot 对局频率远高于旧 bot。
   - 上传先跑 Validation Episode（自己打自己副本），失败标 `Error`；通过者以 default rating 入池，与相近 skill rating 的 bot 匹配。
   - **Final Evaluation**：截止后继续跑局约两周，然后 "A final Bradley-Terry tournament will be run on those episodes to produce the final leaderboard."
2. **BT 计入范围**（host Addison Howard，2026-08-05，https://www.kaggle.com/competitions/kaggriculture/discussion/732931 ，[前次] 2026-09-19 抓取）："The Final B-T tournament will use **all episodes between active agents across the whole competition**. Any episodes your agent played against now deactivated agents will not count."（双方当时都 active 的全程 episode 才计入；对手换代则该局作废）
3. **队伍取两提交较高者 + 平局半胜 + 截止后加跑不承诺局数**（host，2026-09-04，https://www.kaggle.com/competitions/kaggriculture/discussion/739410 ，[前次] 2026-09-19 抓取）。
4. **实测补充（社区帖 742856 "What actually predicted the ladder, and 15 things that didn't"，Avineesh Arora，2026-09-23 发，主楼正文 2026-09-25 经 kagglesdk 抓取，https://www.kaggle.com/competitions/kaggriculture/discussion/742856 ）**：
   - 有选手 **103,148 vs 103,147 输掉吃满 rating 罚**——margin 与评分彻底解耦的直接案例。
   - 两个候选各 384 配对局：A 均差 +$27,682/胜率 91.7% vs B 均差 +$25,715/胜率 97.7%，同盘对打 B 胜 A +6.0pp——**爬分要的是胜率不是均差**。2250+ 对手 100 局里 40% 由 <$100 决出、78% 由 <$1,000 决出；座位无可测影响。
   - 新提交从 ~600 起爬，rating 需 40-70 局收敛（他自己的提交峰值 1233→落 950、1815→落 1539，"Never quote the peak"）。
   - 提交顺序有陷阱：新提交顶掉的是**较旧**的那 2 个 active 之一（他因"强件早提交一分钟"被顶掉）；**要留的 agent 最后交**。
   - 本地评估器对真实天梯相关性：对 starter/random/pass 打 r=+0.014（无效）；换成"真交易强公开件联赛+自家天梯局同 seed 盘"后 corr(bank) +0.458 / corr(margin) +0.533——本地数字要这样校准才可信。
5. **Elo 并发竞态 bug**（帖 742165，2026-09-20，https://www.kaggle.com/competitions/kaggriculture/discussion/742165 ，正文 2026-09-25 抓取）：同时结束的 episode 会互相覆盖 rating 增量（读同一初值再各自写回）；host（Bovard，09-21 评论 [前次] 2026-09-23 抓取）确认终榜 BT 会正确计入——**公榜分有噪声、终榜以 BT 为准**。

**对我方的含义**：本地"净 margin 涨了但分不动/不对称"不需要窗口/分位假说来解释——margin 根本不进分数；选型判据应以**胜率/胜平负翻转**为第一目标（margin 只作 tiebreak/诊断），且回合级改动（几十美元级）在 2250+ 带比"赢局里多赚几千"更值钱（742856）。

---

## 二、官方机制口径（How to Play / Description 页，https://www.kaggle.com/competitions/kaggriculture/overview ，2026-09-25 抓取；引擎源码对照 [前次] 2026-09-19 engine-factsheet，vendored kaggle-environments 1.32.7 wheel）

### 2.1 订单簿撮合（校正我们的表述）
- 官方原文："This is an ordered list and market orders will be processed in order simultaneously (one from each player) while both players have orders."；"Orders are processed concurrently across players, **one unit at a time**... take the current carrot price, give both players that price for their first carrot, then add 2 carrots to the market... and repeat until both orders complete."（按列表顺序、双方逐单位同报价锁步成交；前面单位的成交会移动后面单位的价格）
- **空 `[]` 槽位是位置性的**（讨论帖 742943，Debmalya，2026-09-24，https://www.kaggle.com/competitions/kaggriculture/discussion/742943 ，正文 2026-09-25 抓取）："Market orders settle one order index at a time, in lockstep across both players... Dropping an empty entry changes which orders settle together"——删空槽会改变**谁和谁配对成交**，不只是顺序。
- shiiin9 的机制解读（https://www.kaggle.com/code/shiiin9/beat-v48-100-0-your-herd-is-decided-on-day-6 ，2026-09-25 抓取）："A unit sold in an early slot gets a better price than the same unit sold later... the order of your list decides who sells into whose glut."；其 layer D **只在 V48 留空的槽位里排列卖单，保留 wash sales、购买单与故意空槽**。
- 买价按"买后库存"报价、卖价按"卖前库存"报价 → 同物即时买卖净零（How to Play）；$1 地板的成交**不计入库存**（地板可继续响应后续买入）；每回合市场单上限 10，超出**静默丢弃**。
- 结论：我们的 layer D（卖单槽位重排）方向正确；需复核两点——① 排列时是否保留**故意空槽**的位次语义（742943）；② 是否锁死购买/雇工序（见 §五-4 V57 资金序不变量）。

### 2.2 施肥上限（校正）
- **没有"施肥次数"上限；上限是产量封顶 + 时效**：FERTILIZE 1 袋持续 3 天（day/day+1/day+2，[前次] 2026-09-19 引擎源码 `kaggriculture.py:475-481`）。一次性作物在 bonus 窗口内"浇水 +1/天、**施肥 +2/天**"，封顶 max_yield（How to Play 2026-09-25）。
- **麦/萝卜的标称 max 只有施肥才能到**：Wheat 6（不施肥 4）、Carrot 4（不施肥 3）（How to Play 表）。
- **瓜**：bonus 窗口 6-12 龄，浇水 10 龄封顶 6，**施肥 8 龄即封顶**（早 2 天拿满/早收）。
- **常年作物（番茄/草莓）**：计划生产日"施肥且当天浇过"则当次产量翻倍 2；生产次数封顶 4（番茄 8-11 龄、草莓 10/12/14/16 龄）后衰变。
- 种植当天算"未浇"，无宽限期；连续 2 天未浇变杂草（How to Play，与引擎一致）。

### 2.3 牲畜收益公式与 CARE（校正：CARE 是"逐日银行+下次生产整包兑现"）
- 动物表（How to Play 2026-09-25）：Goose/Egg $300/首产 4 天/每日产/持产 4；Cow/Milk $400/首产 8 天/**每 2 天**/持产 6；Sheep/Wool $500/首产 6 天/**每 3 天**/持产 6。持产=tile 上未收产品上限，非终身总量。
- **CARE 机制（官方原文）**：当天"fed 且 cared"则 `pending_care_bonus` +1；下一个计划生产日若已喂，**整个银行**加到该次产量上（base 1 之外）并清零；生产日没喂则只出 base 1 且银行清零；银行上限被 max_held 间接封顶。→ d0 买的羊若持续喂+理，d6 首产可带最高 6 毛（base 1+银行 5~6 受 6 封顶），不是只产 1。
- **喂养**：每兽每天 1 麦（随身，须先 PICKUP）；连续 2 天未喂**逃逸不可恢复**；新放置动物首日不喂也能活（consecutive_unfed 从 0 起）。
- **肥料副产品**：每只存活动物每天可用 COLLECT_FERTILIZER 收 1 袋，**不喂不 care 也给、不累积**（放 5 天不管也只得 1 袋）→ 重畜群=每天 17 袋肥料的自供闭环（喂麦→产奶/毛 + 集肥→施肥增产/卖肥）。
- 雇工：日内第 n 次 HIRE 价 fib(n)（1,1,2,3,5,8…）日清；棚 100 容量溢出丢弃；地 NE/SW/SE $1000/$2000/$4000（How to Play + [前次] 引擎）。

### 2.4 复利节奏与市场
- 大局形态（georgymarin "what-2600-farms-do-differently"，2026-09-24 lastRun、2026-09-25 抓取，https://www.kaggle.com/code/georgymamarin/kaggriculture-what-2600-farms-do-differently ）："the bank stays near zero deep into the season while everything is reinvested, then compounding takes over once the farm is built"（前中期贴零复投、建成后复利接管）；同局双方 bank 相关 +0.73（共享市场/世界），margin 比裸 bank 更干净；"环境噪声只值几百刀，差异都在对局结构"。
- 价格：9 品各有 base/T/双侧形状（hinge/sqrt/log…），**价格只随共享库存变动**（卖增/买减/城镇消费减），无均值回归；稀缺侧 hinge（萝卜/番茄/蛋）平段后陡升；溢价品（莓/瓜/奶/毛）glut 侧 above_target>1 易砸到 $1 地板（How to Play "The Price Function"，2026-09-25；参数表 [前次] 2026-09-19 引擎）。城镇店每 3 天开一家（有放回抽样、封顶 8 实例）、每实例每 4 回合消费其 1 件产品（单品店 2x：**Yarn Store=wool 2x、Pet Cafe=carrots 2x**）、镇中心每 24 回合各 1 件（除肥）。店铺表：Bakery(egg,wheat)/Pizza(milk,tomato,wheat)/Brunch(egg,wheat,strawberry)/Yarn(wool×2)/IceCream(strawberry,milk,wheat)/PetCafe(carrot×2)/Smoothie(strawberry,milk)/FarmersMarket(wheat,carrot,tomato,strawberry)。

---

## 三、重畜群（羊 11+牛 6）d10-d20 中段收益来源拆解（核心问题的答案）

**一句话：这是"抽到 Yarn 店（羊毛需求）后的条件化畜牧路线"——中段收入=羊毛/牛奶的 CARE 加成批量产出卖给被城镇店撑住的价格 + 全队免费肥料流反哺作物 + 单手群饲压低人工；不抽 Yarn 店时羊毛"一文不值"，所以它是商店抽样赌注而非普适长板。**

逐条证据：

1. **路线本体**：Ahmed V52（https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v52-lean-flock-yarn-route ，2026-09-25 抓取）："**every first-two-shop pair containing a yarn store plays recorded route 9 (6 cows + 11 sheep)**"（前两店含 Yarn → 走 6 牛+11 羊）——就是"羊 11+牛 6"出处（承 Metav4 v13 的 YARN 路由表）。
2. **时机价值**：Ahmed V50 "Early Yarn Commit"（https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v50-early-yarn-commit ，2026-09-25 抓取）：六羊扩张从 d12 提前到 **d11**（条件=当日已知 3 店中 2 店为 yarn，且现金覆盖 d12 前全部计划购买）："**sheep placed on day 11 produce on days 17, 20, 23, 26 and 29, five harvests instead of four**"——d17/d20 两刀就在 d10-d20 中段，之后 d23/26/29 续三刀；yarn 世界实测 80/0/0（均差 +2526±418 自报）；触发窗 79/1（+3674±380 自报）。
3. **价格支撑**：shiiin9（同上 URL，2026-09-25 抓取）："**A shop count is a price**"——35 局校准：羊毛二段价随 yarn 店数、奶价随奶类店（pizza/icecream/smoothie）数；"**With no yarn store, wool is worthless whatever the size of the herds**"；奶价在第 4、5 家奶类店后陡升。店数概率：未开槽位 3/8 奶类、1/8 yarn（均匀抽取）。
4. **产出机制**（§2.3）：羊 d6 首产、每 3 天一产；牛 d8 首产、每 2 天；CARE 银行把每刀抬到 base+银行（封顶持产 6）——**d10-d20 正是 d5-d11 段买入的牛羊"首产大刀"落地窗口**（羊首产=买后第 6 天，牛=第 8 天）。
5. **肥料闭环**：17 兽×1 袋/天=免费肥料流（不累积、须每天收）→ 施肥把麦 4→6、萝卜 3→4、瓜早 2 天封顶（§2.2）——重畜群同时是"肥料厂"，这是作物侧增产的隐性补贴。
6. **人工压缩**（否则 17 兽吃掉太多工时）：V52 "Single-hand sheep service"（承 2945 Farm）：非收割日一只 hand 能在余下小时喂理全部 6 羊时**不雇第二只羊工**（省 12-13 号日雇）；V50 尾盘纪律：d28 起不再 CARE、不喂当晚不产的羊、d29 不买饲料不挂闲工。DSM 的本地服务段也是打包访问：Animal = HARVEST→CARE→COLLECT_FERTILIZER→FEED 一次走完（§四-DSM）。
7. **卖侧护价**：Shepherd's Ledger（https://www.kaggle.com/code/haideptry/the-shepherds-ledger-herd-safe-sovereign ，2026-09-25 抓取，自报数字不外引）主张"protected sale windows——只有货到棚才卖，避免自砸"、"4-turn forecast 在市场崩盘前把奶/毛/莓的卖单前拉"；Gluzdov herd-safe 谱系开局面包：保住初始 5 麦+1 种、饲料储备优先、**0 兽挨饿**（2 天未喂=逃逸=整只报废）。

---

## 四、头部对手面板（2026-09-25 榜快照 2026-09-25T04:35:36Z，9,991 队；https://www.kaggle.com/competitions/kaggriculture/leaderboard ）

| 队 | 榜位/分 | 公开面（2026-09-25 时点） | 我们没有/未验证的机制 |
|---|---|---|---|
| DSM（denden12/masspeaks/shimishige） | #1 / 3065.1 | **未找到官方公开来源**（三成员 GitHub 无 repo、无公开 notebook；仅第三方逆向） | 第三方逆向 XZDang13/kagglefarm（2026-09-25 创建）称：**Waypoint 模板库+人力档位选模板（可截断/复制/重叠）+按 tile 的 Local Service 循环**（Animal: HARVEST→CARE→COLLECT_FERTILIZER→FEED；Crop: DIG→PLANT→WATER→HARVEST），同 labor family 内 waypoint 路由高度稳定（F2/F8=1.000）——第三种排程架构（非磁带非纯贪心）。无 license、单方 RE、未经证实，只可作结构假设 |
| shiiin9 | #330 / 2540.4 | beat-v48（herd/day-6，09-19）+ your-market-list-is-an-order-book（09-21，[前次] 09-23 digest） | **O-B 畜群预测层**：d9 用"剩余店位多项式枚举"给牛/羊定价并换购，**以≥95% 可达城镇中获胜为门槛（不是 EV）**；"expected value is the wrong objective——赢定局别赌成抛硬币"；+204/局（自报）。店数=价格表 |
| haodou092 | #1389 / 2100.3 | harvest-ledger 已更到 **V67 "Harvest-Window Crop Allocation"**（09-24 lastRun，2026-09-25 抓取）："**local DSM-replay-inspired production experiments**...not copies of the private DSM agent" | 收获窗口作物分配 + DSM 回放挖出的生产结构（别人已在挖 DSM 的 production 层）；V59 正主订单簿（[前次] 09-23）只排现金卖单、锁买/雇/空槽 |
| haideptry（队 prairieee） | #3944 / 1015.4 | the-2965-master-hybrid-engine 已换代为 "**2965+ Master Harvest（V59 Order-Book）**"（09-25T04:09 lastRun，2026-09-25 抓取）+ Shepherd's Ledger v2（同日） | 组合层：V59 订单簿排列 + **镜像对手模型**（"models the rival as an active mirror player to front-run price decay"）+ V57 资金序不变量 + EXP402/410；其自报数字（+$928/局等，单 seed 101/102）不外引 |
| kaitofukami | #1987 / 1820.4 | 09-23 后无新公开件（kernels 全量扫描 09-25） | 磁带谱系已被公开面超越（[前次] 09-23 digest："v48 被全线横扫"）；无新机制 |
| prvsiyan | #1109 / 2230.9 | Frontier 双件+floor-aware ledger（09-22/23，[前次] 09-23 digest）；09-23 后无新件 | 对手观测边界声明（$1 地板处 rival_sold 只是下界）；"本地钱差≠官方评分" |
| 竞争带对照（我方 ~1988-2012，#1634 附近） | — | — | — |

讨论区新增（09-23 共享锁后，2026-09-25 全量扫 topics 180 帖对照）：742856（评估方法论，见 §一）、742943（Rust 位相同模拟器 + 引擎细节）、743009（**"已有 notebook 截止后仍可更新"的平台 bug**——"Existing notebooks can still be updated after the deadline"，09-24/25 评论，https://www.kaggle.com/competitions/kaggriculture/discussion/743009 ）、742737/742886（RL/BC 训练成本，BC 微观层"挣扎到 $1k 终局钱"）。外部工具：debmalyaroy/kaggriculture-simulation（Apache-2.0，Rust 位相同引擎 ~550k 步/s、kagg tournament 配对 McNemar、selfplay 数据管线；经帖 742943 + GitHub 2026-09-25 核实存在）。

---

## 五、外部长板清单（按预期收益排序；来源见各条）

1. **[最高] 商店条件化畜群路由（route 9：6牛+11羊）+ d11 早提交 + CARE 全程喂理**——我方羊 ~8 只固定结构，无"前两店→畜群构成"分支，无 O-B 式换购。V52 Yarn 世界 +$5,058/局（800 局，自报）；V50 提前一天 +$3,674（触发窗，自报）；shiiin9 O-B +$204（自报）。触发率参考：首二店含 yarn ≈ 1-(7/8)²≈23%，另加后段 yarn 店撑毛价。来源：ahmedberatozer v50/v52、shiiin9 beat-v48（均 2026-09-25 抓取）。
2. **[高] 卖前拉预测/对手成交预判（PREDICT 类对手建模）**——V52：从公开库存增量+城镇消费−自家成交**反推对手已成交的溢价品卖单**，对"当前首二店"的记录卖流库匹配，我方奶/毛/莓计划卖单**提前一步**压对手成交。1280 局 +0.1094 点/+$1,314（自报）。Gluzdov 谱系：对手轨迹 ≤3 假设（匹配分差≤1）→ 提前卖。我方明示不做对手建模=此面全空。注意 prvsiyan 边界：$1 地板区 rival_sold 只是下界。来源：同上 + [前次] 09-23 digest。
3. **[高] 胜率优先的选型口径改造**（机制外但直接决定分数）：按 §一，margin 不进分；742856 的配对规则=同 (seed,对手,座位) 三元组+双座位+bootstrap CI+**分对手分解**（公开强件非传递：A 胜 B 100%、B 胜 C 85%、C 胜 A 100%）+爬分带全模拟（"在 2250+ 强的件可能在 <2000 带爬不上去"）。来源：742856（2026-09-25 抓取）。
4. **[中高] 我方 layer D 的两处合规复核**：① 保留**故意空槽**的位次（742943：空槽是位置性的，删槽改变撮合配对）；② **V57 资金序不变量**——不得把 HIRE/BUY 挪到为其供资的卖单成交之前（V57 320 局 30 改善/0 退化，[前次] 09-23 digest；haideptry 2965+ 也把 "funding invariance" 列为标配）。来源：742943 + 2965+ notebook（2026-09-25）。
5. **[中] DSM 排程架构假设（模板库+Local Service 打包访问）**——若属实，DSM 赢在"路由模板×人力档位"的执行稳定性和"每到一兽=收割+理+集肥+喂"的捆绑服务节拍；我方磁带+反应层可考虑吸收"捆绑动物服务趟"与"路线模板复用"。证据等级 C（第三方 RE、无 license、创建当日、未经证实）：https://github.com/XZDang13/kagglefarm （Template Mining.md / FINAL_DISPATCH_REPORT.md，2026-09-25 抓取）。
6. **[中] 尾盘负空间精确化**：我方已有 step≥624 截种（EXP402）+施肥双算（EXP410）；外部另有 **d28 停 CARE、d29 停饲料/停闲工/不买饲料**（V50）、d27 后种子/d29 肥=纯浪费（busyaprime，[前次] 09-23）、**终局卖单不要合并**（busyaprime 8 局全负实测）。来源：v50（2026-09-25）+ [前次]。
7. **[中低] 番茄/SE 象限 d18 线**（如采纳需判据实验）：destbreso 2026-09-10 普查（x-ray-your-agent notebook 内引用，2026-09-25 抓取）：top-30 件 12% 对局在 **d18 开第 4 象限、恰好 10 格番茄**，不留残货但吃 ~12% 季度工时，"owner's own bank does not move"——作者自评"是仪表不是推荐"。与 haideptry"私有 top-10 优势=番茄（d12 起）"[前次] 并读。
8. **[低/工具面] 评估吞吐**：debmalyaroy Rust 位相同模拟器 550k 步/s（kagg tournament 0.15s/局 vs 官方 env.run 2.5s/局，16x）可作 CRN 快筛基座（Apache-2.0）；其 differential 纪律（银行按 IEEE-754 位模式逐状态比对）值得抄。来源：742943 + GitHub（2026-09-25）。

---

## 六、异常/失败面

1. **共享锁有洞**：09-23 23:59 UTC 公开代码锁之后，**已发布 notebook 仍可更新**（帖 743009，09-24/25 社区确认是平台 bug）——haideptry（2965+/Shepherd's）、haodou092（V57→V67）、guruprasaathas111 等 09-24/25 仍在换代；公开面情报不会停更，但"新发布"通道理论上关闭。
2. **公榜读数噪声**：Elo 并发竞态 bug（742165）+ 新提交 40-70 局才收敛（742856 峰落 1233→950、1815→1539）——我方 r34a 分数带读数需按"每局漂移+符号翻转+局数"三件套判收敛（destbreso x-ray §9 同口径，2026-09-25 抓取），且提交顺序会顶掉旧 active（要留的最后交）。
3. **本地评估器失真**：对 starter/random/pass 的本地分与天梯 r≈0.014；须用"真交易强件联赛+自家天梯局同 seed 盘"校准（742856）。
4. **信源质量分层**：DSM 全部机制=第三方 RE（XZDang13，无 license、当日创建）；haideptry/guruprasaathas 自报数字（单 seed 101/102）不采信；742856 的 103,148:103,147 案例是社区自述。**DSM 本体无公开来源**。
5. **工具面**：WebFetch 打 Kaggle SPA 只回标题；`topics show` 不含主楼正文（需 kagglesdk get_topic）；`kaggle competitions pages` 的 CLI 语法= `pages --content`（竞争名走 config）。/tmp/nk 一度出现"列表可见/stat ENOENT"沙箱不稳（与 09-23 事故同款），georgymarin 件已换目录重拉复核。
6. **规则红线不变**：截止 09-30 23:59 UTC 终交；§2.12 禁网（评估期不得外联）；只跟踪最近 2 提交（[前次] 2026-09-19 官方规则页）。

---

## 七、来源清单（除标注 [前次] 外均 2026-09-25 抓取）

| 来源 URL | 通道 | 抓取日期 |
|---|---|---|
| https://www.kaggle.com/competitions/kaggriculture/evaluation （Evaluation 页全文） | kaggle CLI `competitions pages --content` | 2026-09-25 |
| https://www.kaggle.com/competitions/kaggriculture/overview （How to Play / Description / Timeline 页全文） | 同上 | 2026-09-25 |
| https://www.kaggle.com/competitions/kaggriculture/leaderboard （9,991 队快照 2026-09-25T04:35:36Z） | `kaggle competitions leaderboard -d` | 2026-09-25 |
| https://www.kaggle.com/competitions/kaggriculture/discussion/742856 | `topics list` + kagglesdk get_topic | 2026-09-25 |
| https://www.kaggle.com/competitions/kaggriculture/discussion/742943 | 同上 | 2026-09-25 |
| https://www.kaggle.com/competitions/kaggriculture/discussion/743009 （及 742737/742886/742449/742341/742165/739410/732931） | `topics list/show` + kagglesdk | 2026-09-25 |
| https://www.kaggle.com/code/shiiin9/beat-v48-100-0-your-herd-is-decided-on-day-6 | `kernels pull` | 2026-09-25 |
| https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v50-early-yarn-commit | `kernels pull` | 2026-09-25 |
| https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v52-lean-flock-yarn-route | `kernels pull` | 2026-09-25 |
| https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine | `kernels pull` | 2026-09-25 |
| https://www.kaggle.com/code/haideptry/the-shepherds-ledger-herd-safe-sovereign | `kernels pull` | 2026-09-25 |
| https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger | `kernels pull` | 2026-09-25 |
| https://www.kaggle.com/code/destbreso/x-ray-your-agent | `kernels pull` | 2026-09-25 |
| https://www.kaggle.com/code/georgymamarin/kaggriculture-what-2600-farms-do-differently | `kernels pull` | 2026-09-25 |
| https://www.kaggle.com/code/evgendvorkin/kaggriculture | `kernels pull` | 2026-09-25 |
| https://github.com/XZDang13/kagglefarm （Template Mining.md、FINAL_DISPATCH_REPORT.md） | GitHub REST + raw | 2026-09-25 |
| https://github.com/debmalyaroy/kaggriculture-simulation | GitHub REST（README 要点经帖 742943 主楼） | 2026-09-25 |
| [前次] https://www.kaggle.com/competitions/kaggriculture/discussion/732931 、/739410 （host 计分口径） | 本战役 `fn_docs/references/digests/web-comp-intel-2026-09-19.md` | 2026-09-19 |
| [前次] 引擎源码（kaggle-environments 1.32.7 wheel 逆向） | 本战役 `fn_docs/references/digests/engine-factsheet-2026-09-19.md` | 2026-09-19 |
| [前次] 09-23 公开生态（shiiin9 order-book 280-0、V59、番茄门、忙时核对） | 本战役 `fn_docs/references/digests/fresh-sweep-20260923.md` | 2026-09-23 |

*原始抓取件（pages 全文 JSON、topics JSON、kernels 原件、榜 CSV）缓存于 `/tmp/kbscan/`（临时工作区，未入战役库）；如需固化请在主会话指令下迁 `references/data/` 并登记。*
