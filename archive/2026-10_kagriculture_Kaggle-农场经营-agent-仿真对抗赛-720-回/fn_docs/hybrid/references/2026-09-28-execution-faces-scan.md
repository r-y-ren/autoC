# 2026-09-28 执行面调研（analysis25 调研轮）——同拍卖单执行差：机制一手核验 + 公开执行件普查

> 任务：围绕"第 21-28 天牲畜产品变现的执行差"（榜前对手卖单更少更大、同回合成交价高 8-10%、2250+ 段 78% 局 <$1k 决出）找还没试过的改进面。只调研+写纪要，不改代码。
> 抓取日期统一 **2026-09-28**。通道：kaggle CLI 2.2.4（kernels pull/list、competitions topics/pages）、GitHub REST（gh）、引擎源码一手核验（kaggle-environments 1.32.7 官方 wheel，Apache-2.0）、arXiv API、本地仅做文本提取（缓存 /home/renyxin/fn28_cache/ 临时）。
> 纪律：逐条带来源 URL+抓取日期；他人实验数字标"自报"；查不到写"未找到公开来源"。
> 已扫勿重复：09-25 topband-strategy-scan、09-27 predict-throttle-scan、09-27 improvement-faces-scan；已证负勿推（PREDICT 抢跑、路线库两口径、推迟卖单等高价、BUY_PRODUCT 喂麦、day0 重排、换种 mix、番茄门、麦簇）。

---

## 一、同拍卖单撮合语义——引擎 1.32.7 一手核验（A 级，全部逐行读源码证实）

来源：官方 https://github.com/Kaggle/kaggle-environments （`kaggle_environments/envs/kaggriculture/kaggriculture.py`，本地产物为战役 vendor 目录内 1.32.7+nodeps wheel，与官方同源；2026-09-28 读取）。`_process_market()` 的准确语义：

1. **槽位 lockstep**：双方市场单按列表下标配对结算——第 i 槽双方当前单位轮流成交，再进第 i+1 槽（docstring 原文 "Per-unit lockstep: at each step, quote both players' current-unit prices, then commit both"）。HIRE/BUY_LAND 是原子单，先按玩家序处理，不占单位轮流。
2. **逐单位重报价**：每个成交单位都按**当前共享库存**重算 `market_price`（SELL 按 inventory；BUY_PRODUCT 按 inventory−1，注释明言"使同拍买卖对倒净额为零"）。同一槽对的双方单位在**同一库存快照**报价后一起 commit。→ 批次不锁价：单内越靠后的单位越便宜；**真正决定成交价的是单位在全局流里的位置（槽下标 + 单内位次）**。
3. **同槽交错 = 平价竞速**：我方与对手同在第 i 槽的卖单，单位 1:1 交替成交、共享同一条价格路径（各拿一半早单位）；我方卖单若落在对手同品卖单**之后的槽**，我的单位在其全部成交之后才执行 = 卖进它制造的谷底。**"少而大挂单"的机械根源就在这里**：同品拆成多单=拆到多个槽=后段单吃自己和对手的双重 glut；合并成一单放在早槽=全部单位进入 1:1 交替竞速。加上 `maxMarketOrdersPerTurn=10` 的硬截断（超出 10 单直接丢弃），和死单（剩余量 0/仓空/钱不够被 abort）虽不消耗成交轮但仍占槽位、**把后续真实卖单的配对整体后移**——三条机制共同解释"卖单更少更大、同回合成交价更高"。
4. **$1 地板的特殊规则**：`PRICE_FLOOR=1`，且 `price==1` 的成交**不增加市场库存**（源码注释 "Sales at $1 do not increase market supply"）——地板区卖出不再加深 glut，这是 prvsiyan 地板件之外的新机械细节。
5. **失败即中止**：SELL 仓空、BUY 钱不够/仓满（shedCapacity=100）→ 该单剩余单位全部作废（order_states 置 None），不是部分跳过。
6. **价格曲线**：`market_price` 以 I0 为折点、T 为尺度的分段形状函数（above/below 两支），max(1, round(price))；georgymarin 页注明 **2026-08-15 平衡补丁（引擎 1.32.7）给 TOMATO/CARROT/EGG 换了 hinge scarcity pricing**（https://www.kaggle.com/code/georgymamarin/kaggriculture-what-2600-farms-do-differently ，2026-09-28）。

结论：公开件说的 "order 1 of each list, one unit at a time"（shiiin9）与 "lockstep by list index"（uninhibitedscholar）方向正确但粒度表述各有偏差（前者"same quote"不准确、后者未提 10 槽截断与死单错位）；以上 1-5 条为源码级定论。

## 二、执行/卖单编排公开件普查（09-27 后新件优先；自报数字均未独立复核）

1. **shiiin9 "Your Market List Is an Order Book"（https://www.kaggle.com/code/shiiin9/your-market-list-is-an-order-book ，2026-09-28）**：在 V55（ahmed V48 谱系）上加 **Layer D 槽位排序层**——把当回合卖单在空闲槽位上的每种摆法（≤800 种/回合，原摆法恒在内、基准分 0）按 lockstep 逐单位回放，选对"V48 族会提交的顺序"最优的摆法；只挪位不改量不改单。自报 vs 7 个 9 月 20-21 日公开强件 ×20 seeds ×双座位：**191-53 → 280-0、均差 +758/局**，镜像 40-0，真实天梯 108 局 74-34→78-30；对各对手增益稳定 +124~133/局（"排序层该有的样子：不依赖对手是谁"）。同页四个常数重测：`V9_RACE_DEFAULT 41→44`（计划卖单抢在对手之前的预留提前量）、`_OR2_SLOT_MARGIN 20→8`（挪进早槽所需最小增益）、`_V92_P_EVERY 3→2`、`_CA_MARGIN -5→-15`，各值 12-24 胜/280 局（自报）；另把 prvsiyan 番茄投资的"数店门"换成**按市场库存投影+引擎曲线逐单位定价**（TOMATO 锚 T=200 全场最窄：库存 9,600→10,200，80 单从 18,355 币跌到 1,653 币）——价格悬崖数据可复用于畜产品变现时点，但番茄门本体已判死不推。
2. **uninhibitedscholar "Beyond 48: Order Sequencing"（https://www.kaggle.com/code/uninhibitedscholar/kaggriculture-beyond-48-order-sequencing ，2026-09-28）**：V43 基座 + 四条纯市场顺序规则（不动农场计划）。机制陈述与一-1 一致（"若你的卖在槽 5、对手在槽 0，你卖进它压过的市场"）；**市场前置**（非对倒 SELL 排最前，回放校验全量可成交才改序）自报 +476/局 16-0；**两拍提前卖**（现金品计划卖在 2 拍内且已入仓就拉到本拍）单独上分无效、**必须与前置组合**；**预留地平线扫描：24 最优**，8/16 亏、36 微正、48 输镜像（"24 是真最优不是越大越好"）；step-0 麦对倒攻击最优 n≈30-50 平台（V45 的 70 在平台远肩），**全季重复攻击 0-16/2-14 判负**（day-0 有效只因对手购买"零松弛"，中期现金充足后同一价格冲击无效）。评测纪律块（world=首两店有序对、64 世界、世界级 bootstrap CI、包装单文件 main.py 审计——wrapper 对手会每拍 PASS 制造 +167k 假胜）可直接借鉴。
3. **ahmedberatozer V39-V55 系列（https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race 、/kaggriculture-v48-clear-the-queue 、/kaggriculture-v55-one-turn-market-race-edge 、/kaggriculture-v39-ready-before-the-rush ，2026-09-28）**：① V44 同拍卖单竞速——"头部对手执行同一条公开磁带，双方同拍入仓，**先报价的批次拿 pre-glut 价**"；当对手被观测在执行我方磁带时卖单预留提前 4→8 拍、若对手又在我方入仓当拍甩卖则升 24 拍；自报独立盘 paired margin +467.8、胜点 +12.5pp（95% CI [10.59,14.41]pp）；压力克隆 fastclone24 仍输（11-53，如实披露）。② V48 清队列——删 0 成交卖槽、合并同现金品重复卖单、把可执行现金卖单挪进腾出的槽（"普通市场规则使用"），自报 paired +225.89。③ V55 一拍竞速——溢价品预留 40→41 拍，+62/局（自报）；42/43 在其面板回退被拒。④ V39 "stock reserved before a turn with a full market queue"（满队列回合前置备货），CI 披露 [-0.78,2.34]pp 未过自家提升门、如实降级为候选。
4. **alperen5252525 三件（https://www.kaggle.com/code/alperen5252525/kaggriculture-first-in-line-stock-into-income 、/kaggriculture-market-rhythm-sale-policy 、/kaggriculture-ready-stock-earlier-sales ，2026-09-28）**："**A sale has a quantity, a price—and a place in the queue**"；其 8 场近期败局 5 场双方卖量相同、输在价格与队列位。First-in-Line：V48 核心 + 可执行现金卖单前移进早空槽 + 黎明前仓压记账 + `_ADV_LOOK=8` 卖前瞻，自报 136/8/0 vs V48 115/7/22、paired +412.73（95% CI 约 [+202,+650]）；Market Rhythm：提前 24 拍 + 两趟相邻交换搜索、对三种**假想对手队列**（同序/名义价优先/逆序）取 `mean(own_rev)−0.25·scenario_spread`，132/12/0 但对 opening10 的 paired +20.8、CI **[-19.0,+62.7] 过零**（如实披露=搜索层效果存疑）；Ready Stock：`_ADV_LOOK` 3→6。三件全部自报、同谱系对手，独立性弱。
5. **tetsutani/lynnsakurai 重排闭包算子（https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing 、https://www.kaggle.com/code/lynnsakurai/farmer-john-and-the-idle-seller ，2026-09-28）**：把"卖单/固定单排序"抽象成确定性重排算子——tetsutani 现版（Step1009，"34-pass closure loop + 残差闭包"）做 inventory-safe SELL/fixed-order 重排（价格阈值/数量规则/座位/对手分支全不动）；lynnsakurai 给出数学化版本（局部因子边际 >0.5 才接受、有限轨道/环检测、≤48 趟），安全不变量：**SELL 仅在投影存货覆盖总量且同拍不买该品时可动；HIRE/BUY_SEED/BUY_ANIMAL/BUY_LAND 保相对序且只能后移**——"只改时点不改经济计划"。与 2/3 的工程实现可互相印证。
6. **haideptry 2965 V79（https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine ，2026-09-28 更新）**：**V78→V79 的公开回滚**——激进 `_CA_MARGIN=-22` 局部占优但触发"价格崩塌陷阱"，天梯 2456.3→2013.3（−443 Elo），回滚至 -15；保留**双空单可靠性修复**（"zero stalled queue holes during within-turn order book evaluation / zero dead SELL slots / clean last-turn execution"）+ 41 路由 + Dmitrii Gluzdov **steps 712-718 七拍实物清算** + R42 day-0 抢跑免疫。"Order-Book Permutation"（即 1 的 Layer D 类）被列为已并入的旧代组件。
7. **haodou092 Harvest Ledger V81（https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger ，2026-09-28 更新）**："**Spatial Mirror Gate**"——当双方公开农场指纹（作物/建筑/动物/农工/手/土地逐坐标）相同且现金差小才用 **7 拍卖单提前量**，否则保持 4 拍；不用对手身份/回放指纹。自报 vs V79：30 局 paired +38.2（中位 0、8 好 20 平 2 差）——**效果小但成本低**。谱系= guruprasaathas111 top-2 master engine v4。
8. **guruprasaathas111 Top-2 Master Engine V4（https://www.kaggle.com/code/guruprasaathas111/kaggriculture-top-2-master-engine-v4 ，2026-09-28）**：`_R42_OPENING` step-0 开局免疫（对抗 BUY 15 WHEAT/SELL 60 WHEAT 前抢对倒）；step 648（day 27）终局切换 Route 2；**E182 七拍清算器 steps 712-718 按 $(-price×quantity)$ 降序卖**（大额变现优先）——与"榜前对手卖单更少更大"一致的收尾排序口径。
9. **leoprovorov Kaggricult-Man RE + God's Mode（https://www.kaggle.com/code/leoprovorov/kaggricult-man-reverse-engineering 、/god-s-mode-hacked-stores ，2026-09-28）**：① T4 镜像卖单提前——"likely mirror games 把父计划卖单提前 1 拍，探针观测到对手也在抢先则升 2 拍；每挪一单位记账抵扣原卖单防双重清算"，3 世界 6+6 局自报 lead-1 全胜 lead-2 再全胜（极小样本）；路线图口径=day 6/step 144 按首两店有序对选 10 条续段、**day 27/step 648 全部进 plan 2 终局清算**，"分析单位是 world 内 route 不是全局胜率"。② God's Mode=商店 RNG 操控（一次 DIG 使下个商店 76.6% 改变；定向 PET_CAFE seed-oracle 上限 43.8%；**正面分数影响未测**）——新面但非执行主题；附带机制事实：**农场动作与商店抽取消耗同一随机流**，改动作会改后续 shop 抽签（评估口径警示）。
10. **数据/度量新件**：ashok205 top10-replay-dataset-archive（https://www.kaggle.com/code/ashok205/top10-replay-dataset-archive ，2026-09-28）按官方日榜 rating 择 top10 队回放做追加式归档（kaggle/kaggriculture-episodes-index 数据集日更）——对手卖单微观结构取数入口；destbreso x-ray-your-agent 改版（https://www.kaggle.com/code/destbreso/x-ray-your-agent ，2026-09-28，09-27 23:00 更新）自动"给当日第一做 X 光"，新增 **endgame stranding 指标**（终拍留在仓里的钱 vs 榜首容忍度）与"market channel 单独偏离"条纹——正是 d21-28 变现执行的现成度量；beraterolelk Meta Field Guide（https://www.kaggle.com/code/beraterolelk/kaggriculture-meta-field-guide-top-30-playbook ，2026-09-28）"**SELL-queue position matters more than what you sell**"，并给出 boatlee V16-RC5（3 回放多数表决重构 Nikita Lugovoy 55440039、"one-turn market lead"、60/60）、Kaito Fukami v27、yhay81 shop-router 三支柱与重构方法论。

## 三、榜前已知线索新动作核查

1. **haideptry**：2965 引擎 09-28 02:13 更新到 V79（二-6，回滚+空单修复是新动作）；Shepherd's Ledger 09-27 15:15 重跑无新面。**haodou092**：09-28 02:23 更新到 V81 Spatial Mirror Gate（二-7，新动作）。**Tschinkel**：无新 notebook（最新仍是 metav4-v13 与 95.5% replay routing，已扫）。**prvsiyan**：09-23 后无新动作（floor-aware/frontier 系已扫）；"删失处理"邻近的公开统计件=arXiv 1909.09495 冰山单隐藏量 Kaplan-Meier 估计（见五）。**DSM**：仍无公开面（维持 09-27 结论）；ashok205/destbreso 两个新归档是取数其回放的替代通道。**Gordeev**：kernels 全文检索无 kaggriculture 相关公开件（gordeevmax 仅他赛题），**未找到公开来源**。
2. **新出现的执行向名字**（09-27 前已有、我方前几轮未收）：boatlee V16-RC5 "one-turn market lead"（二-10）；statma "Herd-Safe Sale Window race ca25/ca20"（https://www.kaggle.com/code/statma/kaggriculture-herd-safe-sale-window-race-ca25 ，2026-09-28；畜群安全卖窗竞速、打包件未解源，C 级）；xuantianfengwu terminal-logistics（弱基线，注释"their bulk order crashes the shared price first"、"六次/日卖单节奏让城镇需求回补价格"，C 级）。

## 四、规则面（Evaluation/Updates/讨论区）

1. **Evaluation 页与 09-25 缓存逐字一致**（https://www.kaggle.com/competitions/kaggriculture/evaluation ，2026-09-28）：仅最新 2 个提交计分并进终评；胜平负按 BT/Elo、**币差不影响评分**。Timeline（https://www.kaggle.com/competitions/kaggriculture/overview/timeline ，2026-09-28）：9/30 终提、10/1–10/15（约）续打至收敛后 BT 终榜。**无新公告**。
2. 讨论区 09-27 后仅两新帖且均无官方回复：743890"23 Sep sharing deadline 后更新 notebook 版本算不算违规"、743829"MIT 公开 agent 代码在 Rules 3.6(c)/3.14(a) 下的资格"（https://www.kaggle.com/competitions/kaggriculture/discussion/743890 、/743829 ，2026-09-28）——比赛尾段规则不确定性，不影响执行面。旧帖补扫：741891 市场价公式实证（log 曲线品 T=100-1000 时 2×T 下跌仅比 T 大 10-15%，麦/蛋长期贴在 base 76-78%、$1 地板几乎不触发，https://www.kaggle.com/competitions/kaggriculture/discussion/741891 ，2026-09-28）；740823 商店=市场排水口不是独立买家（/740823）；741320 楼中楼"2nd place 确认用 RL"（/741792#3525520 间接，二手）。

## 五、市场微观结构文献可迁移判断（宁缺毋滥；只收实际抓到页的）

1. **队列位次估值**：arXiv 1902.10743 "From Glosten-Milgrom to the whole limit order book"（https://arxiv.org/abs/1902.10743 ，2026-09-28）——可定量给限价单队列位次估值。映射：本游戏槽下标即"队列位次"，1-1 交替=同位平权，位次差即成交价差（一-2/3）。B 级（文献自述，未与我方数据合算）。
2. **做市成交概率 vs 成交后收益的取舍**：arXiv 2502.18625 "The Market Maker's Dilemma"（https://arxiv.org/abs/2502.18625 ，2026-09-28，Binance 实盘订单簿）——挂得越靠前越易成交但成交后逆向选择越重。映射：卖单前移拿 pre-glut 价，但"抢太早"会把货卖在需求吸收之前（V55 42/43 拍回退、uninhibitedscholar 36/48 拍输镜像是同款取舍的实测拐点）。
3. **冰山单/隐藏量估计（与 prviyan 删失处理同族）**：arXiv 1909.09495 "CME Iceberg Order Detection and Prediction"（https://arxiv.org/abs/1909.09495 ，2026-09-28）——Kaplan-Meier 删失估计推断隐藏挂单量。映射有限：本游戏对手挂单在成交前不可见，冰山单（拆小隐藏量）无收益面；可迁移的是**删失统计口径**（对手不可见卖量的下界估计），服务于卖窗判断而非挂单技巧。C 级（远类比）。
4. **"少而大挂单/抢价"的文献对应**：模型记忆中的优先权竞争/latency race 类文献本轮**未抓到可引用页面，不写入结论**（抓到的 NBER w19834 是另一主题，已排除）。机制结论以一-1~5 引擎一手为准，文献只作旁证。

## 六、与执行差主题的映射与候选清单（A=一手实测/官方源码；B=自报实验或多源互证；C=单方 RE/未证）

| # | 改进面 | 证据等级 | 依据 |
|---|---|---|---|
| 1 | **卖单槽位编排层（d21-28 畜产品直接套用）**：同品同拍合并为单（避开 10 槽截断+同槽 1:1 平权）、清死单、可执行现金卖单前移早槽、对 V48 族顺序做≤800 摆法回放择优 | **A/B** | 引擎一手（一-1~5）+ shiiin9 +758/局（二-1）+ V48 +225.89（二-3）+ alperen +412.73（二-4）+ 三支柱"queue position>what you sell"（二-10） |
| 2 | **同拍提前量条件化（镜像门控卖窗）**：公开农场指纹相同且现金差小→卖单提前 7 拍（或探针升级 2 拍），否则维持常规；只用自家+公开状态 | **B** | haodou V81 +38.2 中位 0（二-7）+ leoprovorov T4 6+6 小样本（二-9）+ V44 竞速升级（二-3）；**与已判死 PREDICT 的区别：不做对手来单预测，只做公开指纹相等判断+提前量切换** |
| 3 | **收尾清算执行（d27-30 尾段）**：step 648 终局切换 + steps 712-718 按 $(-price×qty)$ 降序实物清算 + endgame stranding 归零 | **B** | E182 清算器（二-8/二-6 采用）+ destbreso stranding 指标（二-10）+ cha22 d18-29 转化败因（[前次] 09-27） |
| 4 | 预留地平线/提前量元参数（24 vs 41-44 vs 4/7 拍）按对手族与产品分层 + 世界级 CI 验证基建（64 世界/世界 bootstrap/克隆压力板） | **B** | 三组公开扫描给出三个互斥最优（二-1/2/3/4），说明该参数强元耦合；验证纪律见二-2 |
| 5 | 商店 RNG 操控（DIG 换商店） | **C** | 二-9：改变率 76.6% 但分数影响未测；非执行主题 |

对我方"卖单更少更大、同回合 +8-10%"的落点：一-3 三条机制（同槽 1:1 交错平权、后槽吃双 glut、10 槽截断+死单错位）是该现象的**机械解释**；1 号面是直接补法（合并+前移+清死槽），预期最贴 2250+ 段 <$1k 的执行精度战；2 号面是廉价的条件增强（区分镜像/非镜像世界）；3 号面对准"第 21-28 天变现执行差"的尾部（d27 起进清算、712-718 收尾排序）。

## 七、本轮收进的公开负结果（勿再踩）

1. `_CA_MARGIN=-22`（更薄的麦→胡萝卜置换）：局部占优、天梯 −443 Elo 回滚（haideptry V78→V79，二-6）。
2. 预留地平线 42/43 拍回退（V55 面板）、36/48 拍输镜像（uninhibitedscholar）：抢太远反噬。
3. 两拍提前卖**单独**上分无效，必须与市场前置组合（uninhibitedscholar K0003）。
4. 全季价格攻击（每拍麦对倒）0-16/2-14 判负（二-2）；day-0 对倒收益的真因是"打破零松弛购买"不是"抬价"，R42 类免疫已在头部普及（二-8）。
5. alperen 队列搜索层 paired CI 过零（[-19,+62.7]，二-4）；实验证据强度不足以单独立项。
6. 评估陷阱两则：wrapper 对手在官方 runner 下每拍 PASS → 假 +167k；sys.modules 泄漏 OOM 杀长扫描（二-2）。
7. 动作改动会改 shop 抽签（共享随机流，二-9）：同 seed 不同动作≠同世界，配对实验要按"世界"而非 seed 陈述。

## 八、未找到公开来源

① Gordeev 的 kaggriculture 公开动作（检索无果）；② DSM 本体一手公开面（延续 09-27）；③ "少而大挂单锁价"的公开文献正面引用页（机制已由引擎源码定论，文献只作旁证）；④ 畜产品（毛/奶/蛋）专属卖窗的公开拆解件——statma 系列为打包件未解源；⑤ 本轮自报数字（shiiin9/alperen/V44-V55/haodou/leoprovorov）均未独立复核；⑥ 743890/743829 两个规则问题无官方回复。

## 九、来源清单（除标注外均 2026-09-28 抓取）

| 来源 URL | 通道 | 日期 |
|---|---|---|
| https://github.com/Kaggle/kaggle-environments （kaggle_environments/envs/kaggriculture/kaggriculture.py，1.32.7 wheel 源码行级核验：_process_market/_commit_unit/market_price） | 本地 vendor wheel（与官方同源） | 09-28 |
| https://www.kaggle.com/code/shiiin9/your-market-list-is-an-order-book | kernels pull | 09-28 |
| https://www.kaggle.com/code/uninhibitedscholar/kaggriculture-beyond-48-order-sequencing | kernels pull | 09-28 |
| https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race 、/kaggriculture-v48-clear-the-queue 、/kaggriculture-v55-one-turn-market-race-edge 、/kaggriculture-v39-ready-before-the-rush | kernels pull | 09-28 |
| https://www.kaggle.com/code/alperen5252525/kaggriculture-first-in-line-stock-into-income 、/kaggriculture-market-rhythm-sale-policy 、/kaggriculture-ready-stock-earlier-sales | kernels pull | 09-28 |
| https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing 、https://www.kaggle.com/code/lynnsakurai/farmer-john-and-the-idle-seller | kernels pull | 09-28 |
| https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine 、https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger | kernels pull | 09-28 |
| https://www.kaggle.com/code/guruprasaathas111/kaggriculture-top-2-master-engine-v4 、https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-7-turn-rescue-historical-lb-2800 | kernels pull | 09-28 |
| https://www.kaggle.com/code/leoprovorov/kaggricult-man-reverse-engineering 、/god-s-mode-hacked-stores （part-1: /kaggricult-man-reverse-engineering-part-1） | kernels pull | 09-28 |
| https://www.kaggle.com/code/destbreso/x-ray-your-agent 、https://www.kaggle.com/code/ashok205/top10-replay-dataset-archive 、https://www.kaggle.com/code/beraterolelk/kaggriculture-meta-field-guide-top-30-playbook 、https://www.kaggle.com/code/georgymarin/kaggriculture-what-2600-farms-do-differently | kernels pull | 09-28 |
| https://www.kaggle.com/code/statma/kaggriculture-herd-safe-sale-window-race-ca25 、https://www.kaggle.com/code/xuantianfengwu/kaggriculture-terminal-logistics | kernels pull（标题/代码注释） | 09-28 |
| https://www.kaggle.com/competitions/kaggriculture/evaluation 、/overview/timeline | kaggle CLI competitions pages | 09-28 |
| https://www.kaggle.com/competitions/kaggriculture/discussion/743890 、/743829 、/741891 、/740823 、/741320 | kaggle CLI competitions topics | 09-28 |
| https://arxiv.org/abs/1902.10743 、https://arxiv.org/abs/2502.18625 、https://arxiv.org/abs/1909.09495 | arXiv API/WebFetch | 09-28 |
| https://github.com/OpenKaggle/kaggriculture-research （09-27 单提交"public-source boundary"）、https://github.com/Applied-Agent-Works/kaggriculture （README=规则口径，09-25 提交）；repo 搜索新增 mooman0222/Kaggriculture-opencode 等 0 星工程仓 | gh REST | 09-28 |
| [前次] 2026-09-25-topband-strategy-scan.md、2026-09-27-predict-throttle-scan.md、2026-09-27-improvement-faces-scan.md（cha22 同回合 +8-10%、742856 <$1k 口径、已判死清单） | 见该三篇 | 09-25/27 |
