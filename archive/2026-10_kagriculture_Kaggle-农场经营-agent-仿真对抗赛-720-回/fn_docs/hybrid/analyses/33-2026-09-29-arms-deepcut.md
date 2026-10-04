# 分析33（2026-09-29）：公开件横测深剖析——差距归因 / R28 再归因 / 可改进点 / 第四次采纳方案

> 输入：results/2026-09-28-analysis31-tetsutani-arm.json（下称 31）、2026-09-28-analysis32-public-arms-B.json（B，haodou+lynn）、-C.json（C，alperen×2+shiiin9）、-E.json（E，leoprovorov/e087/statma/doan+prvsiyan）；
> 源码：/tmp/a30-b1/tetsu_agent/main.py（tetsutani promoted 产线 10,137 行，SHA256 55be5d5f…）、/tmp/arms_b/haodou_v82/main.py、/tmp/arms_e/pkg/mooman_e087/main.py、orderbook_r40/build/main.py、orderbook_r44_a/main.py、orderbook_r45/evidence/（R28 台账）；
> 机制册：references/2026-09-28-family-topband-deepcut-scan.md（下称深挖册）、analyses/30、31-r29-reference-map（下称映射册）。
> 纪律：数字全部引证据文件字段；源码行为推断标【推断】；公开件作者数字标【自报】；本报告新增读数标【本轮】（源=上述证据 JSON 的逐行数据二次切片与 /tmp 配对消融，只读）。

---

## 一、判决总表（五组合并 vs r40 / vs A）

主判语料：26 败局回放种子 + 补种子双席折叠（31 用 660000-660013，B 用 660000+i*7，C 用 660000+11i，E 用 660017-28/34-45/51-60 分块，各组补种子块互不相同——跨组 headline 只可近读，见 §二-0）。

| 件（来源） | 局次 | vs r40 h2h | vs r40 均差 | 实现价(中位) | vs A h2h | vs A 均差 | 判决 |
|---|---|---|---|---|---|---|---|
| tetsutani step1009（31） | 40 | 0.7875（30/7/3） | +357.4 | 1.0773 | 0.9875（39/0/1） | +1478.2 | 过（唯一 FAIL=自克隆恒平退化判据） |
| haodou V82（B） | 50 | 0.850（42/7/1） | +523.4 | 1.0724 | 0.960（48/2/0） | +1417.0 | 过 |
| lynnsakurai step1010（B） | 50 | 0.850（42/7/1） | +449.4 | 1.0726 | 0.960（48/2/0） | +1330.6 | 过 |
| mooman e087（E） | 38 | 0.8553（32/5/1） | +429.6 | 1.075 | —（未判） | — | 过 |
| statma ca25（E） | 38 | 0.5132（18/17/3） | +60.0 | 1.0585 | — | — | 不过（平手带） |
| shiiin9 订单簿件（C） | 50 | 0.020（0/48/2） | −303.7 | 1.0651 | 0.040 | −859.9 | 大败 |
| alperen first-in-line（C） | 50 | 0.020（1/49/0） | −3288.2 | 1.0553 | 0.100 | −2861.2 | 大败 |
| alperen market-rhythm（C） | 50 | 0.060（3/47/0） | −3211.8 | 1.0597 | 0.040 | −3348.7 | 大败 |
| leoprovorov MarketShock（E） | 38 | 0.0658（2/35/1） | −1780.8 | 1.0112 | — | — | 大败 |
| doan v7 鹅引擎（E） | 36 | 0.000 | −129,964 | 0.9997 | — | — | 崩（且喂对手 113-211k，镜像红利警示） |
| 我方 A=orderbook_r44_a（31 参照臂） | 40 | 0.775（30/8/2，A 视角） | +424.9 | 1.0655 | — | — | 我方最强 |
| 我方 R28 提前卖件 r45（R28 台账） | 60 | 0.3917（17/30/13） | −113.5 | 1.0475（基线 1.0666） | — | — | NEGATIVE 收档 |

（31.arms / 31.criteria / B.per_agent.*.arms / C.per_agent.*.arms / E.targets[*].judgment / orderbook_r45/evidence/archive_ledger.json；prvsiyan 真身 bonus 臂过四门但未上判决机。）

要点：
1. **同一基座三件（tetsutani/haodou/lynn，99%+ 逐行重合）+ e087（=step1009 公共底盘）全过**，对我方 A 是 0.96-0.9875 的压倒（+1330~+1478/局）。
2. alperen"提前卖层"双件与 shiiin9 件**全败**：alperen 双件 −3.2k/局、实现价 1.055-1.06；leoprovorov 自打经济最高（96-105k，E.anomalies[0]）却实现价 1.011、h2h 0.066——**经济规模 ≠ 对局强度，卖法形态是主差异**。
3. 对 A 的 +1.4k 与对 r40 的 +357 严重非传递（A 胜 r40 +425 却被家族胜 +1.4k）【推断：A 的 dayhigh 追加块与家族订单簿手术相互作用不利；或家族对"繁忙市场单形状"有额外收割】——**禁止把对 A 的 +1.4k 线性外推为池内普适优势**。

---

## 二、差距归因：tetsutani 系 +357~+523 从哪来

### 二-0 先校准：跨组 headline 差大部分是语料块效应【本轮】
对 26 个共有回放种子做双席折叠配对（31.delta_dist.per_row / B.rows_lite / E 判决行文件 /tmp/arms_e/judgment/rows_mooman_e087.json）：

| 件 | 全语料均差 | 26 回放种子 | 各自补种子块 |
|---|---|---|---|
| tetsutani | +357.4 | **+403.3** | +272.3（660000-13） |
| haodou | +523.4 | **+425.0** | +629.9（660000+7i） |
| lynn | +449.4 | **+403.3** | +499.3（660000+7i） |
| e087 | +429.6 | **+374.8** | +548.4（660017-28） |

同一语料下四件带宽仅 375-425；"+357 vs +523 vs +449 vs +430"的组间差主要由补种子块难度差（272 vs 499 vs 548 vs 630）造成，**不能当作机制差读**。以下归因一律以 26 回放种子配对读数为准。

### 二-1 配对消融：机制增量的直接测量【本轮】
| 对照（共有种子配对，margin 逐 seed 相减） | 结果 | 解读 |
|---|---|---|
| lynn − tetsutani（26 种子） | **0.0，26/26 逐 seed 完全相同** | step1010 不动点闭包 vs 41 遍闭包链：**语义等价被我方实测证实**（作者自报【自报】）→ 闭包"实现形态"零贡献 |
| haodou − lynn（50 共有种子） | **+74.0**（CI≈[+11,+137]，20 胜 4 负；26 回放子集 +21.7，8/3） | 唯一差异=PET_CAFE 门（21 行 wrapper）→ **PET 门 ≈ +22~+74/局**，逐局散布 −741~+605（世界条件性强） |
| e087 − tetsutani（26 种子） | **−28.5**（仅 1/26 seed 有差：1918725083 148 vs 889，−741） | 番茄门在其唯一触发局为负；+430 headline 是补种子块效应，**门本身在此样本无正贡献** |

### 二-2 形态分解（卖时三桶 / 单均量 / 实现价 / 品类）
vs r40 对席（31.behavior_decomposition）：
- **卖时**：tetsutani 加权平均卖日 17.22 vs r40 20.94；量份额 d0-6/d7-13/d14-20/d21-28 = 3.5/16.8/34.2/45.4% vs 2.4/9.9/19.9/67.7%（桶和口径，均不含 d29 尾；桶数据 31.behavior qty_buckets）。r40 的 d27 单日**挂出 113,759 请求量（1,422/局、约 19.5 单/日、73/单）**，tetsutani 同日 7,661（96/局）。
- **单均挂量**：6.66 vs 10.85。**但剔除 d27 墙后 r40 = 6.77/单 ≈ 家族 6.66-6.73**【本轮】——"单均量差"几乎全部是 d27 挂量墙的伪象；跨臂的单均量-实现价单调梯度（6.6→1.075、8.5→1.065、9.2-9.8→1.055-1.06、11→1.058、195→1.011、9,245→1.000，见 B/C/E behavior）真实存在，但对 r40 的直接抓手是墙不是常态批。
- **实现价**：1.0756 vs 1.0621（+1.35pt；80 局中 72 局为正）。rows_lite 切片【本轮】：haodou/lynn 逐局 margin 与实现价相关 r=0.47-0.62，与卖单数相关 r≈0.10-0.18；margin top10 局均实现价 1.083-1.096 vs bottom10 1.049-1.064——**胜差由实现价承载，不是单量**。
- **品类**：C 组对照显示 shiiin9/alperen 卖量 59-63% 是 WHEAT+FERTILIZER 对倒/肥料流（qty_by_item），家族请求挂量 2.1k/局 vs r40 3.4k/局；家族的品结构更"净卖产出"、r40 侧夹带大量对倒量【推断：对倒量拉低边际实现价并贡献 d27 墙】。
- **需求门控**：tetsutani 自报实现价表【自报】（深挖册 §三）：被自己冲垮的品 0.6-1.0×base（milk 0.61-0.67、wool 0.65-0.70）vs 被城镇排水的品 1.5-2.1×（tomato 2.08）——RACEPX/RACEGATE 把 glut 品留给磁带+城镇排水，吃稀缺 hinge。**推断贡献 +0.3~0.5pt 实现价**。

### 二-3 源码机制清单与贡献判定（tetsutani main.py 10,137 行；行号=解包件）
先更正一处认知【本轮源码实测】：**我方 r40 基座字节内已含** r36_debts/sell_lead/suppress（L431-660、L1658-1733）、RACE 预留视界 clamp(lead+12,40,48)（L3773-3882）、RACEPX 抛售门（L3911-3959，`Chassis._sell_lead=_v9_racepx_lead`）、RACEGATE（L3980-4055）、_v44y_lockstep/_v44y_reorder 锁步评分重排（L6090-6219）、E182 712-718 物理规划器（L1022 exec 块）——深挖册 §五"我方全无"清单对这几项不成立（应指我方自研执行层缺失）。家族相对我方的**真实增量**=700-1010 段步进链：

| 机制（位置） | 定义 | 贡献判定 |
|---|---|---|
| 13 路线 step144 选择（L961-980） | 首二店 shop 对→路由表（_R108_SHOP_ROUTES/_V92_TABLE，YARN 例外）；≥648 转 route2 | 贡献≈0（Georgy 九项全同判决：田层无差；我方同 router）；**唯一例外=_V93_ROUTE_BY_RIVAL/CT_TABLE（L4086-4109）身份键控——合规敏感不碰** |
| RACE/RACEPX/RACEGATE | 我方已有同款（上） | 与我方同源，非差异项 |
| r36_debts 净零账本（L1662-1733/4013-4041） | reserve 在 due_step 记债、_r36_suppress 抵扣磁带 SELL；OR2 层 advance 亦记债（L4860/4922） | **结构前提**（净零使"早卖"不冲量）；本身无独立增益 |
| **MODELPX 领卖（L7743-7812）** | MILK/STRAW/WOOL、step144-696、h12-22；对手流=库存差分滑窗 12 取近 4；`inv_next=inv+rival_avg+6−town_draw`，`p_next<p_cur−0.5` 才卖；帽 3/6/10（quote≥100→10） | 我方无此层。【推断】贡献 +0.2~0.4pt 实现价（在城镇排水前抢跑 + 有界小批）；属需求门控型提前卖 |
| **step738/809 就绪提前（L7510-7574/8185-8245）** | 只提前 4/3 拍内磁带已计划、已入仓纯现金量；保护首个计划单；跳 dawn(step%24==23)/BUY_PRODUCT 拍；809 需 quote≥50 且先扣债取残量 | 我方无此层。【推断】贡献 +0.2~0.4pt（小幅早卖+债感知=净零）；与 R28 裸提前的区别见 §三 |
| **step928/948 日新高变现（L8728-8783/8946-8987）** | 当日报价严格新高→立即卖全部可售（price×avail 排序、每拍至多 +1 单、无预测无阈值）；950-953 并入最早同品槽/移到首个花费单前；932/939 携货 DROP 变现 | A 件已补主体（+425 vs r40，31 参照臂）；家族增量=携货变现+并槽细节。【推断】贡献 +0.3~0.5pt 中我方已拿到大半 |
| **闭包重排（_s793，L7889-7953 + step1009）** | 只动槽位不动量；ΔΦ>0.5（_v44y lockstep 自对自回放收入差）才收；budget 800；41 遍链，step1009=第 41 遍 | 配对实测：41 遍 vs 不动点（lynn step1010）=0 差（§二-1）。【推断】闭包簇整体 +0.1~0.3pt（vs 我方单遍 _v44y_reorder） |
| 终局 712-718 物理规划（E182） | 我方已有同款 | 非差异项 |
| CT_TABLE 身份反击（L4086-4109） | step2 (money, WHEAT) 识别 2 支具名磁带搭车 | 泛化性差+合规敏感（映射册 #29/#30 口径），不采纳 |

**归因结论（直接回答）**：+357~+523 中——
- **需求门控**（RACEPX/RACEGATE+MODELPX 变现时机+日新高）是**主贡献**，量化 ≈ +0.8~1.2pt 实现价缺口（1.0756 vs 1.0621 的 +1.35pt 里【推断】60-80%）；
- **卖得小批**对我方是**伪命题**（剔 d27 墙后 6.77 vs 6.66），真实抓手是 **d27 挂量墙+对倒量形态**【本轮】；
- **卖得早**是辅助（wavg 17.2 vs 20.9）且必须"带账本+带门"才成立（R28/alperen 反例）；
- **路线/磁带结构**贡献≈0（九项全同+同 router）；
- **闭包重排**贡献小（+0.1~0.3pt【推断】），且 41 遍/不动点两形态零差（本轮配对 26/26 相同）。

---

## 三、R28 负结果再归因：同机制为何他们赢我们输

R28 事实（orderbook_r45/evidence/judgment_r28.json + archive_ledger.json）：r45=r40+advance_stack_block（debt_ledger 34.8KB+valley_gate 4.1KB+advance_layer），k=4、horizon=48、window[192,695]；h2h vs r40 0.3917（17/30/13）、均差 −113.5、实现价 1.0666→**1.0475**；**净恒等 604 违例/907 核对项**（逐条 `advanced>0, settled=0`，WHEAT 32/EGG 8/…）；但 26 败局重演 22W/4L、对照 20W/1L、反制臂 60/60——"对陌生磁带有效、对同基座净负"。

差异清单（我方 r45 vs tetsutani 系提前卖）：

| 维度 | tetsutani 系（账本内生） | 我方 r45（账本外挂） | 后果 |
|---|---|---|---|
| **账本归属** | 记账/抵扣同一模块：reserve 记债→`_r36_suppress` 在 due_step 抵扣磁带 SELL（L1666-1673）；OR2 advance 逐笔记债（L4860/4922）；step809 先扣债取残量（`q=planned−debts[t][item]`，L8207） | 独立 ledger 记 advance，但**基座自带 r36_reserve/sell_lead/suppress 已把 due_step 的磁带 SELL 预留/扣掉**——到期无 SELL 可抵扣（archive_ledger 原文） | 604 恒等违例=净多卖 → 自造 glut → 实现价 −1.9pt |
| **门** | RACEPX+RACEGATE 双门（quote≤base+0 整品退场）+step809 quote≥50 | valley_gate 单门，仍把 WHEAT/EGG 推进 glut 区 | 价格崩塌型自伤 |
| **视界** | clamp(lead+12,40,48) 逐品；其自报【自报】40/12 镜像 73-7、**48/12 掉到 14-26（毒角）** | **钉死 horizon=48**——正踩其自家消融的最差点 | 系统性偏差 |
| **批口径** | 只提前"已入仓+磁带已计划"，min(q,avail)，MODELPX 帽 3/6/10 | 提前量无帽、与基座预留叠加 | 单量墙 |
| **时机** | 跳 dawn 拍（step%24==23）/BUY_PRODUCT 拍、保护首个计划单、PICKUP 冲突即断 | 无此保护（违例集中在 WHEAT/EGG 正是 PICKUP/对倒高频品） | 净多卖集中在对倒品 |
| **对手谱系** | 家族内自洽（三家共用账本语义） | 同结论：对陌生磁带 22W/4L、对同基座 0.39——**提前卖在同基座对手前是零和套利，谁先裸挪谁输** | R28 判负定性成立 |

**alperen 双件大败是同一根因的第三人称复证**：`_ADV_BOOK=False`（不记账，映射册 #25）+24 拍窗+中段 84% 量堆（192-648）+单均 9.2-9.8 → 实现价 1.055-1.06、−3.2k/局。**结论：R28 败因不是"提前卖"方向错，是"净量变+无门+视界毒角+与基座预留双计"四错叠加；tetsutani 同机制赢在账本内生、双门、40 档、小批有帽。**

---

## 四、可改进点清单（对我方 r40/A 基座；字段=机制/证据/挂接面/预期信号/禁区冲突度/实施成本）

> 禁区在册口径：农场计划层=已判死（Georgy 九项全同+R15/R17 双负）；换种 mix 变体不再试（haideptry `_CA_MARGIN=−22` 在线 −443 Elo）；跨拍卖量移动=禁区同族（R23/R26 双向第三轨、镜像提前 −80k）；启发式重排=禁区（R25 −25k）；镜像条件加卖=禁区（haodou 自撤）；终局清算器不碰（R29）；身份键控=合规敏感。

**① PET_CAFE 需求门控 wrapper（haodou V82 全量增量，21 行）**
- 机制：`pet_any_demand_agent`（haodou_v82/main.py L10137-10155）——day 10-23 且 `PET_CAFE` 已解锁（town.unlocked_shops 实际揭示）时 `_CA_MARGIN −15→−22`（麦→胡萝卜置换边际），调用后 `finally` 还原。**需求揭示门控+临时窗+用后即还原**，非盲 mix。
- 证据：配对 +74.0/局（50 共有种子，CI[+11,+137]，20W/4L；26 回放子集 +21.7）【本轮】；在线 V82=2215.6 保留该门（haodou 09-28 12:01Z run）；但其本地自报 +49.56【自报】与 haideptry 无门 −22 在线 −443 Elo 的矛盾仍在册（深挖册 §七-⑤）。
- 挂接面：r40 `_V9_CARROT` 麦→胡萝卜置换层（r40 main.py L3040-3110，同一经济学：麦 4 单位 vs 胡萝卜 3 单位+$10 种子差）——在置换判据上加"PET_CAFE 揭示∧d10-23"条件并把 margin 倾到 −22（等效口径需按我方常数换算），用后还原。
- 预期信号：判决机 A/B（R26 仪器四件套）+20~+80/局、实现价不降、触发世界占比、触发/非触发拍零足迹；上线走在线读数门（max() 语义，沿 R26 先例）。
- 禁区冲突度：**中**——与判死的"换种 mix 变体"同参数族（`_CA_MARGIN` 同名），但形态是"需求揭示门控+临时化+还原"，与判死的"无门常驻 −22"结构不同；**须用户解锁 + 在线读数门双保险**，禁盲扫参数。
- 实施成本：低（wrapper 形态 ~30 行 + 换算常数；判决半日）。

**② mooman e087 番茄晚市放量门（对手供给预测+排水余量）**
- 机制：`_cxtb_*`（mooman_e087/main.py L6700-6825 + 尾部 L10143）——step432 资格门（10 格/象限 NW-NE-SW/钱≥12000/无番茄在田等）+ **期望收入门**：把 80 单元（10 格×d26-29 收）按库存递推定价——对手番茄供给 `_cxtb_their_supply`（读公开 planted_day，0.75/格/日至季末，96 局回放标定【自报注释】）、排水余量 `_CXTB_DRAIN_SLACK=2.4/日`、店铺解锁期望（d22/d24 各 0.25）；e087 唯一增量=门槛 9000→7500（作者标注 UNMEASURED at build time）。
- 证据：E 判 +429.6/0.855；**但共有种子配对 −28.5（1/26 触发，触发局 1918725083 为 148 vs 889）【本轮】**——+430 headline 是补种子块效应，门本身在本样本无正贡献。机制结构（对手供给预测+排水余量标定法）是真资产，阈值/条件是噪声级待校准。
- 挂接面：需我方新增"番茄晚市"路线分支（d18 条件换种 10 格、d26-29 收）+ 资格门 + 递推收入模型——**农场外科**。
- 预期信号：先离线统计触发世界占比（<5% 不立项）；触发局 paired 差为正；再谈构建。
- 禁区冲突度：**高**——农场计划层已判死 + 换种 mix 判死史直接同族。默认战后议程/用户解锁才立项。
- 实施成本：中-高（路线分支+收入模型 1-2 日+判决）。

**③ 小批+早卖卖法形态（真实抓手=d27 挂量墙，不是拆单）**
- 机制：两刀——(a) **d27 挂量墙卫生**：r40 route2（≥648）卖块请求量 1,422/局、73/单（其余日 6.77/单）【本轮】，按实存/计划量 clamp 挂单（不改总计划量、不跨拍挪量）；(b) 有账本有门的微早卖沿 ⑥（战后）。
- 证据：31.behavior_decomposition（d27 墙 113,759/80 局 vs tetsutani 同日 7,661）；剔墙后单均 6.77≈家族 6.66【本轮】；实现价 +1.35pt 与墙共现（72/80 局）；rows_lite margin~实现价 r=0.47-0.62。
- 挂接面：orderbook_r40 运行时块 `apply_slot_hygiene`/route2 卖块（尾块锚行"r40 运行时尾块"）；同拍改挂单量=订单层卫生。
- 预期信号：d27 请求量 <200/局、实现价 +0.3~0.8pt、h2h vs r40 ≥0.55、非改动拍零足迹（安慰剂恒等）。
- 禁区冲突度：**低-中**——同拍 clamp 挂单量不动计划、不跨拍挪量=低；若把墙挪到早拍=跨拍卖量移动=禁区同族，**不做**（R26 gran −102.6k 在册）。
- 实施成本：低（判决先行半日；构建 1 日）。

**④ 不动点闭包作工具（lynn step1010）**
- 机制：把 41 遍 `_s793` 闭包链压成一次不动点调用（≤48 趟+环检测+41 相位快进 `_S1010_REFERENCE_PASSES=41`）。
- 证据：我方配对 26/26 逐 seed 与 tetsutani 完全相同【本轮】=语义等价实测背书（作者自报【自报】）。
- 挂接面：判决工具层（P4 一并）：作为卖单实验目标函数（ΔΦ lockstep）+ A 件 dayhigh 自评；可给闭包簇消融当基线。
- 预期信号：同输入同输出（回归断言）；闭包耗时下降；ΔΦ 分布入台账。
- 禁区冲突度：**无**（工具级）。
- 实施成本：低。

**⑤（并入①/③的补充）日新高簇补全**：A 件已有 dayhigh 主体（+425 vs r40）；家族增量=step932/939 携货 DROP 变现 + 950-953 同品并槽/移到首个花费单前。禁区低（同拍追加族）；成本低-中。预期：实现价再 +0.1~0.3pt【推断】。

**⑥ MODELPX+step809 债感知提前卖三件套（红区有条件重访，战后）**：MODELPX 领卖+step809（quote≥50+扣债残量）+内生账本口径重建（把基座 r36_reserve/sell_lead/suppress 并入我方 ledger 对账——R28 research_note 明文重访前提）。禁区=禁区同族（跨拍卖量移动）；须整套不拆+判决先行+视界 40 档（不碰 48 毒角）。成本高。

---

## 五、第四次采纳方案：直接以 tetsutani 系字节为新候选

### 五-1 合规四轴核查（沿 r30/2965 先例口径：license/发布时间三渠道交叉/血统 tie/公开衍生标注）

| 轴 | tetsutani/demand-preserving-turn-sale-timing | haodou V82（备选） | lynn（备选） |
|---|---|---|---|
| ①license | **Apache-2.0**：归档成员 LICENSE.txt（全文，无具名版权授予人）+NOTICE.txt（血统链全文）；解包 sha 与件内自声明一致（ARCHIVE 33532d53…、main 55be5d5f…=判决证据 subject.main_sha256 同值） | Apache-2.0：LICENSE.txt+NOTICE.txt（"Apache-2.0 public ancestry"，直系 guruprasaathas111 master-engine-v4，本地改动明文） | Apache-2.0：LICENSE.txt+NOTICE.txt（"Rescue controller refresh 2026-09-22. Apache-2.0"） |
| ②发布时间三渠道 | kaggle CLI lastRunTime **2026-09-27 02:50** ×判决抓取 2026-09-28 ×notebook 自述（"exact promoted submission bytes"，cell 时间戳 2026-09-20 轮） | lastRunTime **2026-09-28 12:01Z**（B 组 anomaly A1：23:27 已漂 V85，判决钉 V82） | lastRunTime **2026-09-27 09:29** |
| ③血统 tie | NOTICE 直系=shiiin9/your-market-list-is-an-order-book → **=我方 base_sha_chain 锚 a16e0e9b**（shiiin9 解包 main sha）；往下 ahmed V55/V56→Tschinkel→yhay81→Gluzdov；kaggle-environments 1.32.7 提取件 Apache-2.0 注明 | NOTICE 直系=guru v4（与我方锚异源，tie 靠其 NOTICE 自述） | 同 tetsutani（NOTICE 同链） |
| ④公开衍生标注 | 发行 tar 三成员（LICENSE/NOTICE/main.py）+ build_manifest description 以 "public derivative (verbatim …)" 起头（沿 gates_r40 门①判据） | 同 | 同 |

**缺口如实标注**：Kaggle 平台 licenseName 字段本轮不可读（api v1 kernels/view 404、内部 GetKernel 403、页面 JS 渲染）——②轴以 CLI lastRunTime+抓取日期+件内自述三源替代，与 2965 先例的"三渠道"内容不同，按实际口径留痕。mooman e087 若作候选：GitHub 仓库元数据 **MIT**（gh_kagr.json），底盘=公开 step1009 字节（Apache-2.0 系）→ 兼容但需双归属，故不作首选。

**许可结论：Apache-2.0，可采纳。** 义务=①LICENSE.txt 随包②修改文件标注（无本地修改则标 verbatim）③NOTICE.txt 归属全文保留+追加我方署名段。竞赛面：公开 kernel 代码衍生系本族通例（我方三次采纳同 SOP），符合"AI 辅助原创+人机分工留档"口径，无规则冲突（archive 时登记采纳来源）。

**署名文案建议（入 tar NOTICE.txt 追加段）**：
```
Fourth adoption, 2026-09-29. Verbatim adoption of public submission bytes from
tetsutani/demand-preserving-turn-sale-timing (kaggle.com/code/tetsutani,
author tetsu2131, kernel run 2026-09-27T02:50Z, self-declared "exact promoted
submission bytes"). main.py SHA-256 55be5d5f124c8daaaa63c1a29ba4aab096004909
666f04748007603c67b7d2a8; archive SHA-256 33532d53ca12d49f2af7e817a6b17cf7dad3
d81c0036a109c63a4fb57778181a. No local modifications. Packaged and submitted by
renyxin as a public derivative work under Apache License 2.0 (LICENSE.txt).
All upstream attribution notices above are retained verbatim.
```

### 五-2 发射算术（终榜 ~24h 窗）
- **现状**：榜 1772.8@1779（09-28 15:36Z，B.anomaly A2；在飞件=A，13:06:27Z 提交）；板面=**最近 2 提交取优（max() 语义）**（analysis30 P1 在案）；额度 5/日·UTC。
- **自然分带**：同字节在线 2307.3（tetsutani）/2215.6（haodou）/2210.6（lynn）；对我方 A +1330~+1478（h2h 0.96-0.9875）——若收敛充分期望 +300~500 榜分。
- **收敛约束**：新提交 ~600 起爬，200-400 局/30-40h 收敛（analysis30）；余 24h → **大概率半收敛（保守 1800-2000 区间落地）**。
- **窗口纪律（计分对挤压控制）**：只发 **1 件**新字节 → last-2={A=1772.8, new}，max() 保证**零下行**；**第二件新字节/重投仅当首件读数 ≥1772.8 后**再发（否则 A 被挤出 last-2，双半收敛件可能把板分拖回 1600-1900）。同字节重投=重新抽收敛轨迹，5/日额度内至多 2 次，终榜前 <4h 停手。
- **内耗**：池内已有 tetsu2131/Lynxx/haodou092 自家提交（同基座）→ 我方克隆件会抽到镜像平局局，拖慢收敛【推断】；接受此损耗，不因此换件。
- **风险清单**：①半收敛不达 1772.8（则板分停在 A，无损失）②池对手换血漂移（mooman 判定法）③非传递性（对 A +1.4k 不可外推）④镜像内耗⑤合规执行瑕疵（打包必须 LICENSE/NOTICE+署名随包，四门走 gates_r40 形态）。

---

## 六、战略菜单

### 终榜前（~24h，按期望值排序）
| # | 动作 | 期望 | 风险 |
|---|---|---|---|
| 1 | **第四次采纳发射：tetsutani 系字节 1 件**（首选 tetsutani step1009；haodou V82 备选但含 PET 门=禁区敏感、且 V85 漂移在案） | +300~500（收敛充分）/ 0~+200（半收敛）；max() 保底零下行 | 半收敛、镜像内耗、池漂移；合规随包义务 |
| 2 | **窗口纪律：保持 A 在 last-2**（首件 ≥1772.8 前不发第二件；额度内同字节重投 ≤2；终榜前 <4h 停手） | 保住 1772.8 保底 | 无（纪律项） |
| 3 | （备选，与 #1 二选一）r34a 字节重投（P1 遗留，+50~230） | 小 | 争 last-2 槽位——选 #1 则弃 |
| 不推 | A 件微调/混合件/PET 门压窗上线 | — | 违"判决先行"；24h 不够判决+在线读数门 |

### 战后议程（按期望值排序）
| # | 动作 | 期望 | 风险/前提 |
|---|---|---|---|
| 1 | ③d27 挂量墙卫生 + ⑤日新高簇补全（低禁区、判决先行） | +0.3~0.8pt 实现价【推断】 | 低 |
| 2 | ⑥三件套内生账本重访（MODELPX+step809+把基座预留并入对账；视界 40 档） | R28 红区翻案的唯一路径 | 禁区同族，须整套+判决先行 |
| 3 | ①PET 门移植 A/B（用户解锁 mix 禁区+在线读数门） | +20~+80/局（配对口径） | 禁区中；haideptry −443 阴影 |
| 4 | ④闭包工具化 + P4 判决尺（种子簇 CI/frozen 复盘/official parity/ΔΦ 双报） | 尺子换代，后续判据可信度 | 无 |
| 5 | ②番茄门/BerryBook 农场计划层（禁区解锁前提；先统计触发率 <5% 即弃） | 不明（本样本 −28.5） | 禁区高 |
| 6 | 名录/对手池回灌（mooman 调查、frapercan BT 尺、doan 鹅线） | 评测面资产 | 无 |

---

## 附：本轮新增读数复现口径
1. 配对消融：31.delta_dist.per_row（40 seed×2 席同值）、B.per_agent.*.behavior.vs_r40.rows_lite、/tmp/arms_e/judgment/rows_mooman_e087.json → 逐 seed 双席均值后共有 seed 相减；26 回放种子=31.source.seeds[:26]。
2. 剔墙单均量：r40 侧（274,410−113,759）/（25,291−1,556）=6.77（qty/orders 均取 31.behavior_decomposition opp_side，d27=qty_by_day[27]/orders_by_day[27]）。
3. license 解包：tetsutani notebook ARCHIVE_B85 → base64.b85decode → tar 成员 LICENSE.txt/NOTICE.txt/main.py（sha 33532d53… 与件内 EXPECTED 一致）；haodou/lynn 件内 LICENSE.txt/NOTICE.txt 直读（/tmp/arms_b/haodou_v82、/tmp/arms_b/lynnseller_pkg）。
4. 平台元数据：kaggle CLI `kernels list`（lastRunTime/author/votes）可用；licenseName 字段 API 不可读（404/403）——缺口在案。
