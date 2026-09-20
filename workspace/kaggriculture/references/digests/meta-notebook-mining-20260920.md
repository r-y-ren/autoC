# meta notebook 精读情报包 —— "点火重构"（2026-09-20）

Track-B pure 精读任务产物。材料为 `references/data/intel-notebooks/` 内 9 份公开 notebook 原件（ipynb JSON，2026-08-31 与 2026-09-19 两批抓取），逐 cell 解析（markdown 全文 + code 源码；这批 notebook 的 outputs 均为空/运行时生成，故一切数字以 notebook 源内嵌的静态表格与文字为准）。逐条引用格式：`[notebook简称·cell N]`。

**材料清单与简称**

| 简称 | 文件 | 抓取 | 作者/主题 |
|---|---|---|---|
| Z2M | kaggriculture-findings-from-zero-to-top-meta.ipynb | 08-31 | Rayk Kretzschmar，c14→C95 重建日记（2836.8 实测分） |
| 2600F | kaggriculture-what-2600-farms-do-differently.ipynb | 09-19 | Georgy Mamarin，每日刷新的 live 报告（模板，数字运行时计算） |
| LIVE | kaggriculture-what-the-top-farms-do-a-live-meta.ipynb | 08-31 | 引擎教学 + Elo≥3100 分带 meta 日报（2026-08-11 期已内嵌） |
| RANK | kaggriculture-rank-your-agent.ipynb | 08-31 | Rayk，10 级参照天梯 + K320（カワシギ rank-1 重建，BT 2481.9） |
| XRAY | x-ray-your-agent.ipynb | 09-19 | destbreso，每日榜首 x-ray（内嵌 2026-08-30 榜首 macro 参照） |
| V16 | v16-rc5-high-score-8c-4s-premium-market-lead.ipynb | 08-31 | boatlee，Nikita Lugovoy 55440039 重建（8C/4S+premium lead） |
| 2900 | kaggriculture-2900.ipynb | 08-31 | HarvestForge-X，与 V16 同源同评测表（同一策略的姊妹发布） |
| V48 | 40-40-early-floor-39-46-top-10-v48-fast-routes.ipynb | 08-31 | Kaito 系 v48，商店事件路由（YARN/FARMERS/BAKERY） |
| 5DAYS | kaggriculture-five-days-of-the-ladder.ipynb | 09-19 | busyaprime，09-01～09-05 五日天梯统计 |

---

## 1. 2600+（top band）与中低分段的差异到底是什么

### 1.1 2600F 的结论（结构差异比想象的小）
- 2600F 用 rating 阈值分带（top band vs 当日 45-55 百分位"middle"）对比 8 项中位数：first land day / peak crew / hires / 总种植量基本**相同**；差异集中在**种植结构（种什么）**与**final bank**。模板原话："They are not out-expanding you… What differs is what goes into the ground"（cell 1 内嵌文案）。
- 全语料相关性（cell 20）：与 final bank 的 spearman 相关**最强的是 total_hires，其次 peak_crew**；`first_land_day` 相关**≈0**（"land is the thing everyone talks about"却最不相关）。作者自注：雇佣重可能是"赢家的结果"而非原因，读作待检验线索。
- 大局形态（cell 15/35）：top farm 的钱**深季前贴地、后段复利**；头部胜局越过自身终值 10% 的时点（elbow）集中在季中（运行时计算，约 d10-15 段）。record/median 胜局银行差 **>10×**。
- 2600F §s5 明确排除 `elbow_day`（与 bank 相关 0.8 但是银行 own 函数派生量，"最自信的错误"）。

### 1.2 LIVE 日报内的"赢家 vs 输家"逐项差（Elo≥3100，148 局，2026-08-11，cell 29）
- 终局资金：赢 85,501 vs 输 81,412。
- 早期（d0-4）下种均量：赢 melon **6.7** vs 输 5.9；wheat 11.6 vs 11.2；strawberry 2.8 = 2.9。
- 草莓首卖：赢 **d14** vs 输 **d16**（前一日报告为 d14 vs d15，差距在拉大）。
- 其余（land/herd/hands）在 3100+ 带内几乎无差——**高分带内部比的是执行与卖时**。

### 1.3 RANK 的"天梯断层"（cell 5/11/17）
- 参照天梯：tier 0-5（自写引擎、只差经济决策）tier 5 银行 **~46k**；tier 6-9（公共 meta 产线、同农场只差 market 层）**149k-165k**。**46k→150k 的断层不在农场，在市场层**（"once everyone builds the same farm, selling is the whole game"）。
- 静态 glut 曲线会骗人：**决定实现价格的是"有几家商店需求你的产品"**（cell 17 表，见 §5）。MELON 无商店需求（只有 town centre），所以"Melon Mateo"类纯瓜流封顶 ~44k。
- 我方 500-550 分段≈tier 4-5 位（结构在、市场层缺失），而对手 m5k 在 meta 带玩法上。

### 1.4 XRAY 的榜首画像 vs 中游（cell 20/22/28/30）
- 榜首参照（destbreso macro x-ray，2026-08-30 capture）：**第 2 象限 d5**、**7 头牛**、**~280 次 CARE**、季末留 13 块休耕、**只留 $442 滞留现金**（"endgame stranding sixty times less money than the leader tolerates"对比的是被检者留得更多）。
- 单位回合预算：榜首 **53.8% 单位回合在移动、3.8% PASS**；中游 agent 42.9% 移动、**11.8% PASS**——差出来的 10 个点全变成了原地发呆。**移动多≠浪费，PASS 才是浪费**。
- 雇佣共识（490 seat-seasons，field IQR 全季每天仅 ±2 手）：**d4 前 4 手，d10 爬到 8→11，d13 起 12 手直到终局**。作者定性："consensus that tight is a heuristic bound"（出带即需证据）。

---

## 2. 开局点火的标准打法（d0-d12 逐步表）

综合 Z2M（openings 表 cell 31、C94/C95 cell 48/53）、V16（扩张表 cell 2）、LIVE（8.5 日报 build order/sell rhythm cell 29）、XRAY（cell 20/30）、RANK（checklist cell 36）。时间为"日"，step=d×24。

| 时点 | 标准动作 | 数值 | 出处 |
|---|---|---|---|
| **d0 · turn 0 市场槽 0** | **BUY_WHEAT 5 份放第一个槽**（饲料保证；对手 14-19 份小麦抢购在前会把价抬到只买得起 4 份→d2 死羊，4 大败平均 -13,606） | 5 units，slot 0 | Z2M cell 47/48 |
| d0 | **BUY_ANIMAL 4 羊 + 1 牛**（V16/2900 路线：step0 即 1C+4S）；或 C0x 系 3C+1S；瓜 IPO 系 2C+16 瓜种 | 畜 d0 即到位 | V16 cell 2；Z2M cell 7/31 |
| d0 | **HIRE×4**（fib: 1+1+2+3=7 币/全天，24→120 动作） | 4 手 | RANK cell 36；LIVE cell 29 first hire day 0 |
| d0-d4 | 下种：**wheat ~11 份、melon ~6 份、strawberry ~3 份**（3100+ 带人均） | 11/6/3 | LIVE cell 29 |
| d0-d8 | 畜牧扩张：8C/4S 线 step120→2C，step161→4C，step168→6C，**step192(d8)→8C** | 8 牛 d8 齐 | V16 cell 2 |
| d5-6 | **买第 2 象限（NE $1k）**：榜首 d5，3100+ 带中位 d6 | $1k，d5-6 | XRAY cell 20；LIVE cell 29 |
| d8 | **买第 3 象限（SW $2k）**：榜首 d8 | $2k，d8 | XRAY cell 23 land3 |
| d4-6 | 开始卖 fertilizer（动物每天 1 份免费肥，首批 d1-4，batch ~5）；wool d6（batch ~10） | — | LIVE cell 29 |
| d8-10 | 卖 wheat（首卖 d8，batch ~12）+ **melon d10 大.dump（batch ~7.7）**← 对手 m5k "d10-12 点火"就是这个资本事件 | — | LIVE cell 29；Z2M cell 7 |
| d10 | **雇工 8→11**；手数爬坡 4→8→11 | — | XRAY cell 30 |
| d11-13 | milk 首卖 d11（batch ~7.7）；**d13 起 12 手满编** | — | LIVE cell 29；XRAY cell 30 |
| d13-15 | 草莓上量：首卖 **d14-15，batch 15.4**（赢家比输家早 2 天） | — | LIVE cell 29 |
| d10-15 | 现金曲线（3100+ 带中位在手现金）：**d5=545 → d10=2,172 → d15=11,782 → d20=36,414** | — | LIVE cell 29 |

**麦+牛引擎（8c/4s）的点火条件**（V16/Z2M/XRAY 综合）：
1. d0 饲料保险（5 wheat slot 0）+ 自种 wheat ~11 份 → 畜牧不因断粮死亡；
2. 羊先行（4S d0，产 wool+肥）牛随现金爬（d8 满 8C）→ milk/wool/肥三线从 d4-11 起持续变现；
3. 点火信号 = **d10 melon dump + d11 milk 首卖**，d15 草莓上量，d20 现金 36k。
Z2M 强调：成熟期结构 8C/6S/3 象限/12 手是"公共最优农场"，**但 c18 证据表明同样的农场只改 112 个市场回合就能从 9-1 变 9-1 且 margin +2,794→更陡**——农场同构后，点火差异全在卖出排程。

**第四象限（SE $4k）**：Z2M §13 大负结果——三种实现族 450 局全部 10-0 输给 C92（mean -3.7k~-4.6k），原因：手到 SE 时当日 action 用不完、额外 crew 费用、多 25 块杂草地、加深市场 glut。例外（XRAY cell 22）：某 top-30 agent **12% 的局 d18 解锁第 4 象限、恰好 10 块 tomato**，但自家银行不动（对手少存钱带来的 margin）。RANK K320（cell 19）：**Yarn Store 第一/第二解锁时**走 4 象限 6C/12S 羊毛线——商店世代的条件性例外。

**"40-40 early floor"正名**：V48 标题的 40/40 指**对冻结的前 20 对手双席位 40 局全胜的胜率地板**（39/46=对 Top-10 holdout），与 d39/d46 无关。V48 的真增量是**商店事件路由**：首个 YARN_STORE@step88→Kaileh57 快线、首个 FARMERS_MARKET@step120→taiseiu 快线、BAKERY+PIZZA@160+Cary Jin 资本态→资本续；骨架不变，只加"经验上站得住的少数续枝"。

---

## 3. meta 结构要点

### 3.1 作物×畜组合（按时间线，注意时效）
| 日期 | 主流配方 | 出处 |
|---|---|---|
| 08-03 top5（2858~2701） | 全部 **8C/5S + 5 strawberry + 12 hands** | Z2M cell 12 |
| 08-09（144 局 40 队单一 field hash） | **~8C/6S、23 strawberry、31 wheat、3 象限、12 手**，market 多为 horizon 3 | Z2M cell 22/23 |
| 08-07→08-09 | 8C+6S+4-9 wheat+10-11 手（modal share 25%→54%→26%） | LIVE cell 29 趋势表 |
| **08-10/08-11 新共识** | **9C+4S+1 wheat+10 手，NE+NW+SW，share 30%**；次主流 9C+5S+2 wheat（x73）、9C+1S（x17）、9C+4S+7W（x16） | LIVE cell 29 |
| 08 月末（商店世代） | K320（カワシギ rank-1 重建）：5 条整线 tape——3 象限 **10C/4S、8C/6S、6C/8S** + Yarn 先解时 4 象限 **6C/12S** | RANK cell 19 |

### 3.2 milk 线的地位
- milk 基价 $160，**3 家商店需求（18/day）**：16 牛场整季 milk **卖价高于基价**（季末价 266，库存 -148 即短缺）——"76-unit ceiling"从不 binding（RANK cell 17）。
- 顶部配方从 8C6S→9C4S 的摇摆本质是 **milk(牛) vs wool(羊) 的商店需求再平衡**；wool 只有 1 家店（12/day），故羊封顶在 4-6 只（RANK cell 17；LIVE cell 29 双极 9c4s vs 9c5s）。
- 动物另发 1 肥/天/只 → fertilizer 从 d1-4 起每天卖，是全场唯一的"零成本常量收入"（LIVE cell 11/23；Z2M cell 5）。

### 3.3 premium-market-lead 是什么（V16/2900 同源）
- 共享市场按队列结算：SELL 入场即压价。V16-RC5 对 MELON/MILK/STRAWBERRY/WOOL 检查"下一回合排定的卖出"，若**本回合无匹配城镇需求且自家 shed 有货**，把下一回合卖单的**一部分提前一回合**执行，并把数量从原单中扣除（两回合总量不变，只有执行时间变）。
- 门（gate）：town demand(t)=0；不变量 s+(q-s)=q。买、HIRE、生产日程全部不动。
- 依据：Nikita Lugovoy `55440039` 三局公开回放（92165990/92185587/92223213），field 100% 一致、market 99.91% 一致；本地 30 seed×双席位 60/60，对 Kaito V27 公开件 24-0（+18,993）、对 Rayk C71 24-0（+18,577）。
- 同族演化（Z2M）：c15 clone-aware 前跑 1 回合（对 anchor 6-0，margin +1,865.7）→ C71 按**自致价格冲击排序** premium 卖单（MELON/STRAWBERRY/MILK/WOOL 可前插，WHEAT/FERTILIZER 保持原时——对手会买它们）→ C94 **fertilizer-only 前插 cap 10**（held-out 900 局 96.7% 胜率，十八 agent 锦标赛 BT 1837 第一）→ C95 前插≤10 wheat+5 fertilizer（对刷新 top-20 medoids 112-8）。
- 卖出节奏基线（LIVE cell 29）：全部商品**小批量多次**（batch 5-15），无人一次性倾倒；同节奏下**先动作者拿好价**——即"一回合领先"的来源。

### 3.4 世代形态（谁在赢）
- 8 月上中旬：**固定 playbook 时代**——多数 3000+ 玩家逐 turn 完全重复（LIVE cell 28：kakuteki/venks/Wufang Hong 全程 100% 复现；Seb 例外 35-66% 自适应，故其在上）。
- 8 月末：**商店路由时代**——K320 按前两家解锁商店（step72/144，day3/day6）选 5 条整线 tape；对近镜像用 2 回合 premium lead、对 legacy 5 瓜/4 羊开局用 4 回合 lead（RANK cell 19）。XRAY cell 12：最强公共路由器只 condition 在前两家店，作者实测该第二分支值 **+0.136 rating/局**（24,000 局普查）；第三分支开放问题。
- Z2M 全程主线：**农场（field tape）收敛→市场层（market timing）是全部边际**；c18 只改 20 field turns + 112 market turns；C70 83-5 却 <3000 分的教训：rating 只奖励胜负，对已赢的对手加大 margin 无用，要赢的是**近镜像的 5-11 局 close game**（一回合肥预售≈5,300-5,700 币翻转，cell 47）。

---

## 4. 低分典型错误 vs 我方现状对照

Z2M cell 37 高频错误表 + RANK cell 36 checklist，逐条对我方（用户给定现状：外购饲料 137→200u、d12 现金 700、开局 3-4 头、点火 d13-18）：

| # | 作者总结的典型错误 | 我方对应现状 | 差距定性 |
|---|---|---|---|
| 1 | **d0 买牛无饲料储备→d2 死畜**（Z2M bug 表；C94 教训：5 wheat 必须放 slot 0） | 外购饲料 137→200u——自种 wheat 缺位（top 在 d0-4 自下 ~11 份），只能市价买，还暴露在对手抢购涨价下 | 结构性：自种麦+slot0 买麦双保险缺失 |
| 2 | **CARE/浇水优先级错→melon 70/96**（d6-12 浇水窗漏浇是常见静默泄漏） | 点火 d13-18（晚 3-5 天） | melon d10 dump 的资本事件整个缺席；3100+ 带 d0-4 人均 6.3-6.7 瓜种 |
| 3 | **开局畜量不足**：top d0 即 4S+1C 或 3C+1S（首 cow/首 sheep 中位 d0） | 开局 3-4 头 vs top 4-5 头 | 表面差 1-2 头，实质差"d0 是否到位"——d0 到位才有 d4 起的肥收入与 d8 满 8 牛 |
| 4 | **现金曲线落后**：3100+ 带中位 d10=2,172、d15=11,782 | 我方 d12 现金 700 | d10 段落后 ~4×；主因是 melon/milk/肥三条卖出线没开，而非少花钱 |
| 5 | **HARVEST 后不 DROP→市场看不见货、卖不出**（IPO 资金断链） | 未证实，需自查 | RANK checklist #2 |
| 6 | **固定 10 牛到底→镜像局银行塌向 40k** | 未证实 | 需 sheep/草莓/对手感知路由 |
| 7 | **只优化对 starter 的 mean bank** | 我方本地评测若以银行计会高估 | RANK/Z2M 反复强调 W-L 与 BT |
| 8 | **囤种**（25 瓜种=2000 币睡大觉；RANK checklist #4）、**d28 后还在投资**（终局不清仓=0 分） | 未证实 | K320 做法：种子采购 cap 在"d30 前能到首收"的量 |
| 9 | **无效 PASS**：中游 11.8% 单位回合 PASS vs 榜首 3.8% | 未证实，x-ray 可测 | XRAY cell 28 |
| 10 | 两个几乎相同的活跃提交被 meta 切换一锅端（Z2M bug 表 #7） | 未证实 | 提交组合多样性 |

**一句话诊断**：我方不是"农场差一点"，而是**点火包（d0 饲料保险 + d0 畜到位 + d0-4 下种 11/6/3 + d10 瓜 dump + d11 milk + d13 12 手 + 一回合 market lead）整段缺失**——对应 RANK 天梯上"tier 5 农场、无 tier 6-9 market 层"的形态，故被 m5k（meta 带玩法）在 d10-12 完成点火后压制。

---

## 5. 关键数值常数表（全部摘自 notebook 源码/内嵌表）

**引擎与经济**（Z2M cell 2/3；RANK cell 23/36；LIVE cell 2/10）
- 720 turn = 30d×24；起始现金 $3,000；board 10×10；shed 100 非种子件（溢出销毁）。
- 地价：第 2 象限 $1k（NE）、第 3 $2k（SW）、第 4 $4k（SE）；NW 免费。
- 雇佣 fib(n) 复利：4 手=7 币；~10 手≈$143/天；12+ 变陡。
- 一-market-槽序、一单位一 field op/turn；step 718 可执行、719 不可（Z2M cell 19）。
- 端日自动把单位库存倒进 shed；SELL 只看 shed。

**基价 / glut 曲线**（LIVE cell 2 MARKET_PARAMS；RANK price_curves 定性；Z2M cell 6）
- WHEAT base25 T400 log above0.20；CARROT base35 T450；TOMATO base60 T200；STRAWBERRY base120 T100；MELON base250 T300 above_target3.6（二次）。
- 从 10,000 库存打到 $1 地板所需卖出量：**WOOL 59、STRAWBERRY 62、MILK 76、MELON 158、TOMATO/CARROT ~500-850、WHEAT/EGG ~3000**（LIVE cell 10 硬断言表）。
- ⚠️ strawberry cliff=62 仅在 1.32.x；别的 build ~247（LIVE cell 1 警告）。

**商店需求表**（RANK cell 17，决定实现价格的正确口径）
| 产品 | 需求商店数 | 基价 | 商店消耗/day |
|---|---:|---:|---:|
| WHEAT | 5 | 25 | 30 |
| STRAWBERRY | 4 | 120 | 24 |
| MILK | 3 | 160 | 18 |
| EGG | 2 | 50 | 12 |
| CARROT/TOMATO | 2 | 35/60 | 12 |
| WOOL | 1 | 200 | 12 |
| **MELON** | **0** | 250 | **0** |

- 实测：16 牛场季末 milk 库存 -148（短缺）、价 **266**；16 鹅场季末 egg +104、价 42。畜组合对照（16 动物同约束）：10C6S=52,957；12C4S=54,512；**16C=57,407**；10C6鹅=38,845；16鹅=10,602（全部 tuning seeds 上，all-cow 在 held-out 却 3-9 输给 Rita——换种子再判）。

**生长/浇水**（Z2M cell 5；LIVE cell 8）
- one-shot 作物 bonus 窗 = age ceil(max_yield_day/2)..max_yield_day；窗内每浇一天 +1（施肥 +2）；melon max_yield_day=12→窗 6..12，cap6，纯浇水 d10 满；**wheat 纯浇水到不了 6，必须施肥**。
- 16 tiles×6=96 melons 满执行；漏浇 d6-10 → ~70。

**槽位/行动细节**（RANK cell 36/17；Z2M cell 19）
- 仅 NW 解锁时 (4,4) 是唯一可用 shed 访问块（其余在锁区，PICKUP/DROP 静默 no-op）；雇工出生在锁区块浪费 1 回合。
- 规则书写错而引擎实况：CARE 实际 +1/天（非 +2）。
- 同回合 SELL 排 BUY 前可即时融资（市场按列表序结算，seat0 先成交）。

**顶部行为参照**（XRAY cell 20/22/28/30；LIVE cell 29；5DAYS cell 0/11）
- 榜首（08-30）：Q2 d5、7 牛、~280 CARE、13 块晚季休耕、$442 滞留。
- 雇佣 IQR：d4 前 4 手 → d10 8-11 → d13-30 12 手。
- 榜首 53.8% 移动 / 3.8% PASS；中游 42.9% / 11.8%。
- 3100+ 带（08-11，148 局）：first land d6、first hire/cow/sheep d0；早种 wheat11.4/melon6.3/straw2.8；卖 rhythm：fert d4(4.9)、wool d6(9.8)、wheat d8(11.6)、melon d10(7.7)、milk d11(7.7)、straw d15(15.4)、carrot d25(5.3)；cash d5=545/d10=2,172/d15=11,782/d20=36,414；终款中位 84,151、max 154,941。
- 5 日池化（09-01..05，747 decisive 局）：赢家中位 91,678 vs 输家 84,882，gap 6,796；局内 margin 中位 3,436-6,210；各日前十胜率隔夜只留 2-5 人。

**本地评测方法学常数**（Z2M cell 8/10/21；RANK cell 28/37；V16 cell 6）
- 双席位必测（market 按 player 序处理，seat0 先手）；tuning/held-out 种子分离（+4,450 的 all-cow 在 held-out 翻车 3-9）；18-agent 锦标赛 918 局 0 错；引擎 pin 1.32.7 + 行为 fixture（回放一局对账到币）。
- 世界（world）= 前两家店组合（step72/144 揭晓），64 个世界；第二分支 +0.136 rating/局。

---

## 6. 时效性风险（08-31 与 09-19 抓取，引擎 8 月初后仍有 patch）

| 结论 | 采集期 | 风险 |
|---|---|---|
| **1.32.7 = Aug15 patch**（hinge scarcity pricing：tomato/carrot/egg；BUY_PRODUCT/BUY_SEED 在 shed 满时失败） | 2600F cell 24；Z2M cell 2 | 我方 vendored 引擎即 1.32.7（见 engine-factsheet），Z2M/RANK 的 1.32.7 实测**可直接用**；1.32.2 时代回放-derived 数字（V16 重建 921xxxxx、LIVE 08-11 日报）在 patch 前后边界，**tomato/carrot/egg 经济已变** |
| LIVE 的教学数字（cliff 62 等）标明仅 1.32.x 成立 | 08-31 | 若线上已推进 1.32.8+，strawberry cliff 可能已非 62（LIVE 自述他 build ~247）——以本机 1.32.7 实测为准 |
| **8c/5s、8c/6s、9c/4s 配方** | 08-03/09/11 | 已被商店世代（K320 五线、V48 商店路由）替代性刷新；9 月初 meta 中位 Elo ~2,880-2,930（5DAYS cell 3）。**配方数字可当"起点模板"，不要当现状** |
| "SE 几乎无人买（≈0%）" | 08 月初 | 09-10 已有 top-30 以 12% 频率 d18 开 4 象限种 10 tomato（XRAY cell 22）；K320 在 Yarn 世界走 4 象限 6c12s——**条件性 4 象限已上线** |
| Z2M 的 C70 83-5 <3000、live 对手名（Jince/WBF/Gould/Ueddy…） | 08-10 | 个体名次全过期；但"rating 只看 W-L、close game 决定名次"的机制不变 |
| melon-IPO（16 瓜 d10 dump）| 08 上旬 | MELON 零商店需求的结论（RANK，1.32.7）使其只宜作**期初资本事件**而非主收入；对手 m5k 的 d10-12 点火若仍是瓜 dump，则其后续靠 milk/草莓接续 |
| V48 的 YARN/FARMERS/BAKERY/PIZZA 事件路由 | 08 月末 | 商店名与解锁节奏与 engine-factsheet（每 3 天解锁、cap 8 家、townShopSellInterval=4）一致，**方向可信**；具体 step88/120/153/216/160 触发值是他人 tape 的轨迹值，不可直接照抄 |
| 5DAYS：胜率日际不可区分、top10 隔夜大换血 | 09-01..05 | 结论是"单日榜噪音大"，与我方 500-550 分段问题（结构性落后）不冲突 |

**总时效判定**：经济学常数（价格/商店/雇佣/生长）在 1.32.7 内可信；**配方与点火时点以 08-11 日报 + V16 扩张表为骨架、以 K320/V48 的商店条件化为修正方向**；一切"对手特定"数字（margin、评分）仅作量级参考。

---

## 7. 对我方"点火重构"的可实施要点（标注：前 6 节为 notebook 证据，本节为其在我方语境的机械映射）

1. **d0 市场单序**（对齐 C94/K320）：`BUY_WHEAT×5`（slot0）→ `BUY_ANIMAL SHEEP×4` → `BUY_ANIMAL COW×1` → `HIRE×4` → `BUY_SEED WHEAT×~11 / MELON×~6 / STRAWBERRY×~3`（现金 3000 内需按价格裁剪并实测）。
2. **自种麦替代外购**：外购 137→200u 应转化为 d0-4 自种 ~11 份 + slot0 买 5 份的保险库存；外购量目标归零（对手抢购会把价抬到买不起）。
3. **d5-6/d8 买地**（Q2 $1k / Q3 $2k），SE 默认不买；仅在 Yarn 早解锁世界评估 4 象限 6c/12s。
4. **d8 满 8 牛**（V16 扩张表节奏），milk d11 起卖、肥 d4 起每天卖、wool d6 起。
5. **卖出纪律**：小批量 5-15；premium 四品（MELON/MILK/STRAW/WOOL）对近镜像前插 1-2 回合（两回合总量守恒）；WHEAT/FERTILIZER 不前插；d25+ 清仓一切。
6. **12 手 by d13**，出 PASS 前 grep 队列（XRAY 的 idle 诊断口径）；对 starter 的银行只当 smoke test，晋级门槛用双席位 H2H/BT。

---

*来源登记：见 references/INDEX.md 同日行；本 digest 只读材料为 intel-notebooks/ 内 9 份 ipynb，未产生其他写入。*
