# 2026-10-02 收官三件深挖（closing-kernels-mining）——冰火终章 / 2600+ 农场 / X-ray 拆解

- 抓取时间：2026-10-02 10:39-10:41 UTC（kaggle CLI 2.2.4 `kernels pull --metadata`；web/wayback 旁证 10:45-10:50）
- 对象：收官速扫（`2026-10-01-closing-sprint-scan.md` §1）登记的三件截止前高票分析 kernel；本篇=首次内容开挖
- 归档：`ext/closing-kernels/{leoprovorov-iaf-final, georgymarin-2600farms, destbreso-xray}/`（各含 provenance.md + SHA256SUMS.txt）
- 纪律：结论只引本次实抓文本（cell 序号可溯）；件内数字一律标"自报"；09-28 我方重算数字标"我方重算"；查不到写"未找到"。三件均**无需运行即得结论数字**（自报数字写死在 markdown / 或我方 09-28 已按其代码重算），故未做沙箱执行——逐件说明见各节"运行口径"。

## 〇、获取状态总表

| ref | 登记票数 | 本次读数 | 拉取 | 归档件 SHA 锚 | 内容版本 |
|---|---|---|---|---|---|
| leoprovorov/a-song-of-ice-and-fire-final-update | 103 | 109 | ✅ 成功 | e4e83741…（912,579B/23 cell） | 终章版（cell 19 更新至 MarketShock-M1-WR1K；分析数据窗约止 09-20） |
| georgymarin/kaggriculture-what-2600-farms-do-differently | 54 | 55（陈旧索引） | ❌ 403/网页 404/wayback 无 | 7f15418e…（fn28_cache 09-28 缓存代偿） | **收官版未找到**（09-30 22:06、10-01 22:07 两次 run 不可得） |
| destbreso/x-ray-your-agent | 52 | 52 | ✅ 成功 | 3ca5da4f…（98,686B/41 cell） | 与 09-28 缓存**逐字节同**=纯重跑，无内容增量 |

georgymarin 撤回实证（2026-10-02）：`kernels pull`×3 轮 403（kernels.get denied）、网页 404、
同账号姊妹件同 403（作者级撤回）、`datasets metadata/files` 对 kaggriculture-episodes 亦 403。
搜索索引仍滞留（55 票/lastRun 10-01 22:07:56）为陈旧缓存，不作实据。

---

## 一、leoprovorov《A Song of Ice and Fire | Final Update》（冰火终章，103→109 票）

**件性质**：研究文章+交互仪表盘（需配套数据集，仍公开）+末格可复现 agent 构建（872KB base64 载荷）。
系列定位：Part 1=RE 总览、Part 2=God's Mode 黑店、Part 3=本件（fixed vs flexible 终章）——即我方"冰火分歧诊断器"（分析29 P4）的口径源头。

### 1.1 核心结论/数据发现（口径：自报，写死在 markdown；分析数据窗约止 2026-09-20）

**A. Majkel1337 461 胜局单版本分解（cell 4/6）**——任务问的"461 胜局分解"终版：
- 11,828 个命令-单位中仅 **906（7.7%）是"冰"**（全胜局同拍同命令）；冰的 63%（572/906）是 Movement；
  **Growing 仅 3% 冰、Market sell 仅 1% 冰**——"种什么、何时卖"是分叉区，走路是固定件（cell 6）。
- **day0 是磁带**：首日 99 个命令-单位 87 个是冰、平均一致度 93%；d1-6 跌到 35-48%；d7 后稳定 25-32%（cell 6）。
- **首买地是排程**：461 局中 **459 局在 step 150 买首块地**；后三次购地堆在 step 218/220/222
  （141/409/392 次），合计占全部购地 **98%**（cell 6）。
- **分叉树根**：step 229（d9.54）把 461 局劈成 279/182；根的一个状态变量——**step 229 时手持动物的
  手的数量**——对 400/461（**86.8%**）局分边正确："The state of the farm is where the fire of
  this agent comes from"（cell 6）。最好叶子 26 局一致 2041 格=全集 2.3×。

**B. 十一队分歧画像（cell 9/11/16/17，bundle 口径=整拍 farmer+双手+市场单全同才算同）**：
- **THIRD FARM CLUB = 六日纯磁带**：step 0-72 平均分歧 0.004、72-144 为 0.007；**Majkel1337 同窗
  0.424/0.651**——首店开前 42% 的 Majkel 局已离多数 bundle（cell 11）。
- p10/p25/p50（≥10/25/50% 局脱离多数派的首步，cell 16 ROWS 硬数据）：
  | 队 | 胜局数 | p10/p25/p50 |
  |---|---|---|
  | M & M & P & Q | 92 | 1 / 1 / 2 |
  | SpaTaro | 81 | 2 / 2 / 2 |
  | Majkel1337 | 234（多版本混样） | 4 / 4 / 13 |
  | Orbital Terraformer | 53 | 10 / 10 / 23 |
  | DSM | 85 | 23 / 23 / 26 |
  | Mengfei Li | 105 | 4 / 81 / 181 |
  | feel the agi | 66 | 6 / 151 / 151 |
  | AI是我的豆包 | 73 | 49 / 146 / 148 |
  | THIRD FARM CLUB | 88 | 145 / 145 / 146 |
  | ymg_aq | 86 | 74 / 105 / 150 |
  | Otter Vibe | 48 | 97 / 97 / 97 |
- **强度与磁带长度无关论断（cell 17）**："The ranking by this number is not a ranking by
  strength: M&M&P&Q, the shortest script here, has the highest average winning score in the
  sample."——最短磁带（p25=1）的队在样本里平均胜局分最高。
- 64 商店世界（前两店有序对，cell 12/14）：单世界样本 ≤8 局；Majkel 最长共享开局=PET_CAFE→
  FARMERS_MARKET（3 局）对 PET_CAFE→YARN_STORE（6 局）只同意到 step 145、全场仅 22.5%——
  作者自诫"小样本长前缀是线索不是结果"。

### 1.2 重点问题作答

- **冰火最终版结论**：把 agent 切成三段（cell 18 表）——**Fixed**（磁带，heat-grid 蓝格/分歧≈0）、
  **Conditional**（店开虚线后的查表分叉；"15 shop pairs pick 11 plans at step 144"）、
  **Flexible**（无虚线抬升段=读状态的规则层）；"bar（p25 步）就是两半 agent 的边界，前半磁带、
  后半 router+rules"；并给出自检法——"把你自己的 agent 跑多种子同图叠比：Majkel 是火你却是冰=
  过刚，Majkel 是冰你却是火=白花灵活性"（cell 6 应用 5）。终版定性：**榜顶无纯磁带赢家——
  磁带只是开局，胜负在状态驱动层**。
- **榜顶最终画像**：Majkel1337=day0 磁带（93% 一致）+step150/218-222 排程购地+**d9.5 动物携带
  状态分叉**（86.8%）+卖流纯火（sell 1% 冰）；M&M&P&Q=**开局即柔性**（p25=1）且样本平均胜局分最高；
  **DECEM 未找到**（11 队样本不含；其"牛-牧场磁带"画像是我方分析50 自测，非本件）。
- **"谁赢了为什么"赛后论断：未找到**。作者明确拒绝下结论（cell 17"不是强度排名"、cell 18
  "哪条柔性规则赢由对真人的对局决定"）；无榜顶策略优劣的终审文字。另有 cell 19 版本注记：
  其自交件最终版=MarketShock-M1-WR1K（=flexonafft v106 打包同源，谱系为 yhay81 shop-router
  v3 + Tschinkel planner + kaggle-environments unit_model，全 Apache-2.0 系）。

### 1.3 机制增量（对照我方已知）

| 面 | 本件增量 | 与我方关系 |
|---|---|---|
| 磁带族 | day0 磁带 93% 一致、step150 首地、218/220/222 购地堆=98% | **印证**我方"step1009/开局书"磁带族认知，给出精确步位新刻度 |
| 牛-牧场 vs 羊系 | Majkel 根分叉被"手持动物的手数"解释 86.8%（step 229/d9.54） | **新增**：畜群执行状态=分叉变量的第三方实证；与我方分析50"动物买序零区分度（带内）"不矛盾（跨族样本 vs 带内） |
| 卖流形态 | Market sell 仅 1% 冰=全场最火区 | **印证**"卖时规则先反事实"教训（分析38 判负方向）；卖流是自适应层非磁带层 |
| 订单簿 | 未直接涉及（market order 只进 bundle 指纹） | 未找到 |
| 终评口径 | 未涉及（回放样本分析） | 未找到 |
| 镜像难题 | 未涉及 | 未找到 |
| 分歧诊断 | p10/p25/p50 三阈值+分叉树 size-weighted gain+L(A,B) 磁带共享长度（≤10% 分歧前缀） | **新增判据**，我方"冰火分歧诊断器"（分析29 P4）可直接升级刻度 |

### 1.4 可迁移资产（许可）

1. **分歧度量体系**（cell 6/11/14 数学区）：a_l(t) 一致度、U(S) 冰格增益、split() 加权劈分、
   D(t)=1−max_c n_c/N、L(A,B) 磁带共享前缀长——方法口径可引用（**notebook 无许可证声明**）。
2. **cell 16 ROWS 数据表**（11 队 p10/p25/p50+胜局数）：可入 P4 对手画像基线。
3. **配套数据集 leoprovorov/a-song-of-ice-and-fire-interactive-dashboards**（3 个 HTML 仪表盘，
   2026-09-20 创建，**仍公开**）：含 461 局 overlay/11 队分歧/64 世界全交互数据，可离线开挖。
4. agent 载荷=Apache-2.0 系谱（yhay81 shop-router v3/actions.json、Tschinkel planner、
   kaggle-environments unit_model）——与我方已知 idle-seller/step1009 底盘谱系重合，非新源。

**运行口径**：结论数字全部写死于 markdown（自报）；分析 cell 仅渲染仪表盘，末格仅打包 agent，
运行不产生新数字 → 未执行，静态拆解。

---

## 二、georgymarin《What 2600+ Farms Do Differently》（54→55 票，收官版不可得）

**件性质**：随 georgymarin/kaggriculture-episodes 数据集日更的 live 仪表盘（"A live report, not a
snapshot"，cell 6）；2600+ 农场=其数据集覆盖的 245,890+ 局（deepcut §一 自述口径）。
**本节文本=fn28_cache 09-28 缓存件（36 cell）；量化数字=我方 09-28 按其代码在 09-28 00:25
数据集版上重算（deepcut-scan §二），非自报；收官版（09-30/10-01 两次 run）未找到。**

### 2.1 行为差异维度（本件设计，cell 16/17/19/20）

指纹九维=crew（peak_crew、hires/day、total_hires）+ 土地时点（first_land_day）+ 作物
（plants_carrot/melon/strawberry/tomato/wheat、tiles_planted）+ 银行形态（钱曲线剪影、elbow_day
**故意排除**：cell 19 自述其与 bank 相关 0.8 但是从 bank 本身导出（"那是算术不是策略，入图会是
本件最自信的错误"）+ 市场面（九品价格 lo/hi）+ 运气面（同 bot 跨局 bank 离散）+ 开局面
（stream_hashes 前缀共享）。**无畜群维度（BUY_ANIMAL 不入指纹）**——这是它对我方羊系问题的盲区。

### 2.2 高分 vs 低分农场行为差（对标我方"羊系带三级台阶"）

- **top band vs mid band 九项中位数全同**（我方重算，窗口 4 天，top 2500+=239 座/115 队 vs
  mid p45-55=1,538 座/587 队）：first land 6=6、peak crew 12=12、hires 268=268、plantings
  239=239、carrot 40=40、melon 12=12、strawberry 33=33、tomato 0=0、wheat 154=154；
  **final bank 99,616 vs 95,862（+4%）**。结论句（其件内口径）："top plays the middle's
  game and banks +4%"。取样偏差自述：fetcher 先抓高分——"缺口是线索不是结论"。
- 全语料 Spearman（cell 20 作者口径，标题即结论 "Labor leads, land timing does not"）：
  最强信号=total_hires（crew 紧随）、first_land_day ≈0（"土地是所有人谈论的东西但接近零"）、
  作物里 best crop 最贴 bank；作者自诫"heavy hiring 可能是赢家买得起而非赢的原因"。
- 大局剪影（cell 3/14，自报）："bank 前中期贴零复投、建成后复利接管"；elbow 排除教训同上。
- 运气面（cell 31 + caveats，我方重算）：单 bot 跨局 bank 离散 **cv 中位 26%**；**双座 bank 同世界
  相关 +0.73** → "对局内 margin 才是干净尺"；环境噪声只值几百刀、跨局离散数万（引 destbreso
  weed-spawn 消融）——"差异在对局结构不在骰子"。09 月中旬起中位胜局 ~96-100k 停涨。
- 城镇需求面（我方重算）：**约 1/3 赛季一个 wool 买家都没有**（无 Yarn 店）；carrot 典型季 ~270
  店铺需求、双 Pet Cafe 开局 ~800、倒霉开局 <150（5× 摆幅，d6 定 world）。
- 平衡补丁（engine 1.32.7，2026-08-15，cell 24 设计+我方重算）：carrot 峰值中位 42→**56（×1.33
  唯一大涨）**、tomato 天花板 $152→**>$1,800** 但采用率仍个位数；top 座位在补丁落地前一天（08-14）
  就加种 carrot（引擎 PR 公开领先）。
- 两条推论（自报，deepcut §二-7）："When you sell moves more money than how much you grow"；
  "spread your sales into trickles…price slides while you sell"（**trickle=拆单族，与我方 R26
  跨拍拆单毒结论张力**，我方已判"拆单延售=负区族"——见 09-30 深挖 family 带 lynnsakurai 延售重写负区）。

**印证还是矛盾？——印证（方向级），不构成对"三级台阶"的反驳**：
① "top plays the middle's game and banks +4%"与我方分析50 "雇工 267-283/动物买序/买地块数零区分度、
终局钱中位不解释分差、分差在对局结构/Elo 面"同向——粗行为维度不解释分差，钱差不解释分差。
② 但其分辨率止于 crew/land/crops，**看不见畜族（牛-牧场 vs 羊系）、卖流形态、day0 市场单段**——
恰是我方三级台阶的三个台阶变量；其"无差异"是粗尺零结果，不是对台阶结构的反证。
③ 其"1/3 赛季无 wool 买家"直接**印证**我方羊系路线的 Yarn 条件性（shiiin9"无 yarn 店羊毛一文不值"）。
④ 其 luck 口径（cv 26%/+0.73/margin 尺）**印证**我方判决统计单位改"对局内 margin"（分析31 r22 已采）。
⑤ 唯一张力点：trickle 拆单建议 vs 我方 R26 拆单毒——口径差在其"不砸价"意图 vs 我方跨拍延售实测负。

### 2.3 重点问题作答

- **2600+ 农场行为差异维度**：见 2.1（crew/土地/作物/银行形态/价格/运气/开局七面九维；无畜群面）。
- **高低分行为差**：九维中位数全同、bank +4%（top=mid 的游戏）；全语料归因=劳动强度领先、
  土地时点零相关。**直接对标我方台阶：方向印证（粗维零区分），维度错位（它测不到台阶变量）**。
- **数据是否公开可复用（episodes v79）**：**现已不可用**——datasets metadata/files API 2026-10-02
  实测 403（作者级撤回，与 kernels 同步）；搜索索引显示 lastUpdated 2026-10-02 01:16:55/34,114
  下载/67 票（陈旧索引口径，v80+ 存在与否不可证实）。末次可证版本=v79 @ 09-30 00:43:36
  （final-window-sweep S18）。我方 09-27 下载的 09-26 版 CSV 派生物已随临时目录清失，**仅剩
  派生结论存于 09-27/09-28 两扫描文档**。可替代复用件：destbreso/kaggriculture-benchmark-matchups
  （45k 对局、CC0、2026-08-26 期）仍公开（datasets list 实测在列）。

### 2.4 可迁移资产（许可）

1. **elbow_day 排除纪律**（cell 19）：derived-from-outcome 变量禁入归因图——判决工具通用纪律，可入 P4。
2. **stream_hashes 判据**（cell 32）："同前缀=观测事实非相似度阈值；t48 前无可观测差异；
   stream_h719 识别的是局不是 agent，血统只活在前缀里"+席位配对 design effect 1+φ 置信修正
   （镜像局两座位非独立）——判据定义可直接引用（notebook 无许可证声明）。
3. **三安全载入器模式**（cell 10）：episode_features.csv 为行为层、单局 glob 免载全库——数据工程模式。
4. episodes 数据集本体：**许可字段未找到**（元数据 403 不可查）；且已撤回不可下载。

**运行口径**：件内数字=运行期计算（缓存 pull 无 outputs）；收官版不可得+数据集 403 →
无法运行复核；量化结论用我方 09-28 按其代码重算值（deepcut §二），已注明。

---

## 三、destbreso《X-ray your agent》（52 票，诊断工具向）

**件性质**：对任意 submission 的全自动 X-ray 报告生成器（默认 x-ray 当日榜一；scheduled 日更；
cell 0："fork it and put your own id in the next cell"）。**内容与 09-28 缓存逐字节同**——
收官 run 纯重跑，本件自 09-25 起即在我册（部分口径已引），本篇=首次全文拆解。

### 3.1 诊断方法（13 节，本次全文读毕）

1. **Ledger**（cell 1/5）：W-L-T+逐局 margin（按对局时序）；红连=匹配器找到其层级，深红单峰=一个世界/一个对手。
1b. **世界×对手评级带矩阵**（cell 7/8）：行=前两店世界、列=对局时对手 rating 带（<1200…2800+）；
   横读=胜率是否随带衰减（有无天花板）、竖读=弱行=漏血世界（n≥4 且 <50% 打印点名）。
2. **条纹面板**（cell 9-12）：逐局 vs 自身 modal 动作三色——绿=同、琥珀=仅市场通道不同、
   藏青=farmer/hands 计划不同；两排序（按世界/按时序）。签名读法：全绿=纯回放、绿+琥珀列=
   修补脚本、72/144 藏青分块=shop router、季内渐藏青=live policy。
3. **双重分类**（cell 13-15）——**核心新判据**：GLOBAL 全体互比 vs WITHIN-WORLD 同世界内互比。
   "shop router 全局看像狂适应、世界内却近乎全同；真 live policy 世界内也分叉。
   **两次读数之差即诊断**"。类目=PURE_REPLAY / REPAIRING_SCRIPT / ADAPTIVE。诚实限界自述：
   seed 与反应无法全分离，分世界组=先剥掉最大的 seed 效应（店抽）。
4. **血缘谱**（cell 16-19）：PLAN 一致（farmer+hands）找家族、WHOLE 一致（+市场）1.000=同录、
   **BARCODE**=每日 d1-4 重锚窗签名×30 天、首个不一致日=分叉日定位；镜像线 plan≥0.95、
   sibling 0.5-0.95；**t48 前无可观测差异**（早期一致=引擎确定性）。基因群=开局窗（t<144）
   plan 一致 ≥0.98 连通分量，群内战绩/margin："a group you only tie is your own chassis
   looking back at you"。
5. **宏观经济 X-ray**（cell 20-23）：二/三/四象限落位日、herd 买入、CARE 次数、季末卫生
   （d25-29 休耕地、鸣钟搁浅 $）、逐日钱曲线；参照系=**2026-08-30 实测 #1 形状**（二象限 d5、
   7 牛、~280 CARE、13 休耕、$442 搁浅——"不是目标，是最强者恰好容忍的形状"）；内嵌 245 局
   #1 分布点云做分布比较（非点估计）。四象限行附 2026-09-10 普查（自报）：top30 件 12% 局
   d18 开四象限、恰好 10 格番茄、零搁浅、吃 ~12% 季工时、own bank 不动——"instrument, not a
   recommendation"（与我方 09-25 引用同源）。
5b. **钱事件+陨石坑**（cell 24/25）：最决定性一局双钱曲线+订单标记（圆=卖、方=结构性、三角=其他，
   面积=$ 权重）；**crater 判据**=一方大卖砸价后 1 日内另一方同品卖出（红=对手卖进我砸的坑、
   蓝=反之），一阶伤害=victim 数量×吃掉的价差（"read it as the size of the hole"）。
6. **棋盘使用**（cell 26/27）：occupancy/presence 热图+**两控制**：卡方 vs 均匀+top10 格质量占比、
   **半分相关**（局交替分两堆比图，r≥+0.9 才信，"低于约 +0.9 当一季噪声"）。
7. **生产率时间**（cell 28/29）：unit-turn 四桶 work/carry/move/idle（穷尽、漏网动词打印不丢）；
   对照=当日 #1 的 p10-p90 **带**非单线；自报校准：leader 53.8% unit-turn 在走路、3.8% 站桩 vs
   中游件 42.9%/11.8%——"走路是宽棋盘的代价，PASS 才是无物可做"。
7b. **用工时间**（cell 30/31）：490 seat-seasons 全场共识=4 手到 d4、8 by d6、11 by d10、
   d13 起 12 手到鸣钟、全程 IQR 0-2 手——"这么紧的共识是启发式界：出界的用工曲线是需要证据的
   主张，不是风格"。
8. **收敛判定**（cell 32/33）：DRIFT（每局评分变化均值）+SIGN FLIPS+n 三件套；阈值 1.0 分/局
   **随判决声明**（"a verdict quoted without its threshold is not a verdict"）；判词=
   WARMING UP/SETTLING/SETTLED；配对速率图**故意不进判决**（匹配器调度所致；只用于换算
   "多久后再读数"）。
9. **报告块**（cell 34/35）：report.txt 可贴可 diff。
10. **语言指纹**（cell 36/37）：5 连非空拍=短语（丢移动/PASS/数量），日带 6-11/12-19/20-29 的
    跨局复现率中位；校准锚（自报 2026-09-04）：磁带族 1.00/0.91-1.00/0.74-0.91、カワシギ
    0.89/0.15/0.00（brancher）、keiz 0.75/0/0、tetsuya&yuanzhe zhou 0.02/0/0、Crop Dusta
    0/0/0；盲测=对手工逆向过的 8 局恢复全部 7 个已知分叉点（精确率全对、零漏零误）；类目=
    SCRIPT/BRANCHER/SCHEDULER/MIXED。
11. **BRANCHER 决策树提取**（cell 38/39）：分叉点=局间停止一致的拍；决策桩搜索可见特征
    （自己钱/对手钱/9 品价格@t/t-1/t-24）；置换检验 1500 次 p≤0.05 剔运气分叉；留一预测验真；
    配套件"97% predictable"（自报）。
12. **告示**（cell 40）：turn 约定=拍 t 的动作存 steps[t+1]（错位一拍全图偏移）；mode 随样本弱。

### 3.2 重点问题作答：诊断方法？有无超越我方 P4 判决尺的评测思路？

**方法**=公开回放驱动的六轴 X-ray（战绩/条纹/双重分类/血缘/宏观/收敛），数据源=公开 episode
端点+回放 CDN（**无需 token**，致谢 georgymarin 爬虫端点出处；cell 3 自带 ladder-climb fallback）。

**超越/补齐我方 P4 判决尺的点（逐条）**：
1. **GLOBAL vs WITHIN-WORLD 判定差**（cell 13/14）——把"路由"与"反应"分开的判据，我方 P4 现无
   此双读数；直接补 doanthuan eval 口径的"行为门"。
2. **败因归因配套**：世界×对手带弱行点名（1b）+crater 卖压归因（5b）+基因群"该打谁"清单（4）——
   比我方手工五因解剖更可自动化（呼应分析47 P2 的 MIT 三件套方向，本件是同族第四件）。
3. **半分相关控制**（cell 27）：热图必须过 r≥+0.9 才信——我方指纹/热图类判决现无此反伪影闸。
4. **收敛三件套+阈值随判决**（cell 33）：与我方 09-25 已引口径同源（destbreso §9），本件给出
   完整判词与配对速率换算——可直接并入 P4 读数纪律。
5. **语言指纹 SCRIPT/BRANCHER/SCHEDULER 三分**（cell 37）+校准锚+盲测记录：行为门的第三种测法
   （在我方磁带一致度/bundle 分歧之外），且自带验证。
6. **用工共识界**（cell 31）："出界=需要证据的主张"——给 P4 加"先验界+越界举证"测试法。
- 不足/边界：一切读数只用已发生的公开对局（事后镜），对未提交变体无预测力；mode 随样本、
  t48 前盲区、turn 约定陷阱（cell 40 自述）。

### 3.3 机制增量（对照我方）

| 面 | 本件增量 | 与我方关系 |
|---|---|---|
| 磁带族 | 语言指纹锚：field tapes 读数 1.00/0.91-1.00/0.74-0.91（日带） | **印证**磁带族存在并给出量化锚 |
| 卖流形态 | crater 判据（卖=武器，一阶伤害=victim 数量×价差） | **新增**：卖流对抗性读法，补我方订单簿/实现价研究 |
| 订单簿 | 市场通道单列（amber vs navy 分层）：全场"市场通道修修补补"为主流形态 | **印证**"卖流是自适应层"（与冰火终章 sell 1% 冰互证） |
| 终评口径 | 收敛三件套+1.0 分/局阈值+配对速率解耦 | **印证**我方 09-25 已采口径，本件补全判词体系 |
| 镜像难题 | 血缘谱镜像线（plan≥0.95）+BARCODE 分叉日+席位 design effect 1+φ | **新增**：镜像/克隆的量化认定法（我方 C3/EXP283 门的评测侧补齐） |
| 牛-牧场 vs 羊系 | 宏观参照=7 牛 #1 形状（08-30）；四象限 d18 番茄 12% 线 | 旁证（其 #1 形状=牛系；与我方"榜顶牛系族统治"同向） |

### 3.4 可迁移资产（许可）

1. **13 节诊断 harness 全代码**（cell 3-39）：**无许可证声明**，但作者明示 fork 自用（cell 0）；
   端点用法（EpisodeService/ListEpisodes POST、kaggleusercontent 回放 CDN、
   LeaderboardService/GetLeaderboard，competitionId=147734）+fallback 纪律可移植。
2. **判据定义**（可引用）：镜像线 plan≥0.95 / sibling 0.5-0.95 / 基因群开局窗 ≥0.98 /
   BARCODE 每日 d1-4 签名 / 收敛阈值 1.0 分/局随判声明 / 半分相关 r≥+0.9 / crater 窗 24 拍。
3. **参照数据**（自报，内嵌于件内）：08-30 #1 宏观形状 245 局分布（cell 23 LEADER_REF 硬编码
   数组，可直接复用）、490 seat-seasons 用工共识、语言指纹校准锚。
4. 配套数据集 destbreso/kaggriculture-benchmark-matchups（45k 对局重放、**CC0**、仍公开）；
   配套件 "a DNA test for agents"/"97% predictable"/"Which language does your agent
   speak"/"Measure Your Agent"（在册待挖）。

**运行口径**：结论数字为自报 markdown；运行需逐局拉 ~25MB 公开回放且比赛已截止（实时榜语义
已死）→ 未执行，静态拆解。

---

## 四、三件对照表（判据×机制增量×我方关系）

| 判据 | leoprovorov 终章 | georgymarin 2600+ | destbreso x-ray | 我方结论关系 |
|---|---|---|---|---|
| 可迁移增量判定 | **有**（分歧度量体系+p10/p25/p50 队表+磁带步位刻度） | **有但降级**（elbow 排除纪律+stream_hashes 判据；收官版缺、数据撤回） | **有**（双重分类/血缘谱/收敛判词/语言指纹/crater/半分闸） | 三件合计补 P4 判决尺 6 项（见 3.2） |
| 磁带族 | day0 93% 一致、step150/218-222 购地 | 开局前缀=事实判据 | tapes 语言锚 1.00/0.91-1.00/0.74-0.91 | 印证（三方互证磁带族） |
| 牛-牧场 vs 羊系 | 动物携带手数=分叉变量 86.8% | **盲区**（无畜群维度） | #1 形状=7 牛（旁证） | 印证+新增；分析50 台阶不被反证 |
| 卖流形态 | sell 1% 冰（最火区） | "卖比种移动更多钱"+trickle 建议（与 R26 张力） | crater 卖压判据 | 印证自适应层定性；trickle 条记张力 |
| 订单簿 | 未找到 | 价格 lo/hi 每局（半数局毛/奶/蛋/肥触 $1 地板） | 市场通道 amber 分层 | georgymarin 价格区间为旧知补充 |
| 终评口径 | 未找到 | 未找到 | 收敛三件套+阈值随判 | 印证我方已采口径 |
| 镜像难题 | 未找到 | 席位 design effect 1+φ | 镜像线 0.95+BARCODE 分叉日 | x-ray 新增认定法 |
| 高低分行为差 | 强度≠磁带长度（M&M&P&Q p25=1 最高均分） | top=mid 九维全同、bank +4% | 弱行=世界级漏血 | 共同印证"分差在对局结构非粗行为/钱" |

## 五、异常与限界

1. **georgymarin 收官版未找到**（403/404/wayback 无）：本篇该件=09-28 缓存版拆解+09-28 我方
   重算数字；09-30 22:06 与 10-01 22:07 两次 run 的增量**不可复核**。其 episodes 数据集同步撤回
   （metadata/files 403），"数据公开可复用"的答案从 v79 可用翻转为**现已不可用**。
2. 自报口径不可复核处：冰火终章 461 局/11 队数字（作者未附可复跑数据集，仪表盘为成品 HTML，
   可看不可重算）；x-ray 全部校准数（53.8%/490 seasons/08-30 形状/语言锚）系作者自测；
   georgymarin 数字系我方 09-28 重算（数据集当时版），非本次实算。
3. leoprovorov 分析数据窗约止 09-20（仪表盘创建日），晚窗榜顶演化（M&M&P&Q 终态 3073.5 等）
   未覆盖；Majkel 461 局样本为单版本、234 局样本混版本（cell 17 自述混版失真风险）。
4. scriptVersionId 三件均未获取（CLI 不暴露+GetKernel RPC 对本机 token PERMISSION_DENIED）；
   以 id_no+SHA+lastRunTime 代锚（provenance.md）。
5. x-ray 无内容增量（SHA=09-28 缓存）；其"scheduled 日更"的 10-01 run 只是重渲染。
6. DSM 分歧口径张力（待核）：leoprovorov p25=23/p50=26（DSM 胜局 d1 即分叉）vs 我方 09-27
   stream_hashes（DSM top1 前缀 0.769@t24→0.557@t300=半数局 5.7 天逐字节同）——样本窗
   （其 85 胜混版本 vs 我方 09-26 版 307 局）与口径（bundle vs 字节）不同，数据源已撤回无法复核。

## 六、建议（分级）

1. **[入池测·高]** 冰火终章 p10/p25/p50 队表 + step150/218-222 购地刻度入 P4 对手画像基线：
   我方 C_final/S8 自测同口径曲线（"冰在火位=过刚、火在冰位=白花"自检法，cell 6 应用 5）。
2. **[入池测·高]** x-ray 双重分类（GLOBAL vs WITHIN-WORLD 判定差）+半分相关闸并入判决基建
   （与分析47 P2 MIT 三件套同轨合流，本件为同族第四件、代码最完整）。
3. **[入池测·中]** crater 卖压判据（24 拍窗、一阶伤害=数量×价差）入订单簿/卖流实验读数
   （可测我方 S8 尖拍捕获对对手的砸价伤害）。
4. **[入情报纪律·中]** "elbow 排除纪律"（derived-from-outcome 禁入归因图）+收敛"阈值随判声明"
   写入引用纪律/判决尺模板。
5. **[入情报纪律·中]** georgymarin 撤回事件登记：作者级 403（kernels+datasets 同步）、搜索索引
   陈旧不可信——开源潮二轮（分析47 P1，10-07/10-15）复扫时优先查其是否恢复/换址。
6. **[仅登记]** leoprovorov 配套仪表盘数据集（3 HTML 仍公开）与 destbreso benchmark（CC0）列入
   可下载资产清单；MarketShock-M1-WR1K=已知 idle-seller/step1009 底盘谱系，不重复拆解。
7. **[仅登记]** DSM 分歧口径张力（§五-6）挂账；若 10-07 扫到 episodes 镜像/恢复再做同窗对质。

## 七、来源登记

| 来源 | 通道 | 抓取日期 |
|---|---|---|
| https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-final-update | kernels pull --metadata（ipynb+metadata 全文，23 cell 读毕） | 2026-10-02 |
| https://www.kaggle.com/code/destbreso/x-ray-your-agent | kernels pull --metadata（ipynb 全文 41 cell 读毕；SHA 与 fn28_cache 09-28 件比对） | 2026-10-02 |
| https://www.kaggle.com/code/georgymarin/kaggriculture-what-2600-farms-do-differently | **pull 403**；fn28_cache/nb/ 09-28 缓存 ipynb（36 cell 读毕）+ /home/renyxin/fn28_cache/txt/ 摘录 | 2026-10-02（缓存 09-28） |
| https://www.kaggle.com/datasets/georgymarin/kaggriculture-episodes | datasets list（索引读数）/ metadata+files 403 | 2026-10-02 |
| https://www.kaggle.com/datasets/leoprovorov/a-song-of-ice-and-fire-interactive-dashboards | datasets files（3 文件清单在列） | 2026-10-02 |
| https://www.kaggle.com/datasets/destbreso/kaggriculture-benchmark-matchups | datasets list（在列，CC0 转述自 georgymarin 件 cell 6） | 2026-10-02 |
| [前次] 2026-09-28-family-topband-deepcut-scan.md §二（georgymarin 数字=我方 09-28 重算）、2026-10-01-closing-sprint-scan.md（三件登记）、2026-09-27-improvement-faces-scan.md（stream_hashes 前缀实测） | 本战役档案 | 见各文件 |
