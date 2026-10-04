# 三件开源冠军件源码解剖 II：romansvet / WHmaoxian r4_2-r5 / mqingcs last_dance（字节级）

- 日期：2026-10-03。方法：纯静态（rg/文本比对/AST 级常量核算，bwrap 内仅做 SHAPES 求和脚本，未执行任何目标代码）。
- 对象与池测（均引自本 references 台账既有实测，非本次重跑）：
  - **romansvet** = `fn_work/legacy_software/kaggle_simulations/orderbook_postseason_lab/pieces/romansvet/`（GitHub romansvet/kaggriculture HEAD 4444cc7a，Apache-2.0；自报峰 2,858/收官 2,230 rank330）。vs 王座 H1 h2h **0.8333**（10W2L，margin +6,389.4；opensrc-pooltest 2026-10-02）。
  - **r4_2/r5** = `ext/whmaoxian_harvest/repo_full/project/submissions/release_v10_{r4_2,r5}/main.py`（各 8,327 行 / 1,102,204 B）。两件 h2h 均 **0.8333**（10W2L；margin +1320.9 / +1368.5；whmaoxian-license-harvest 2026-10-03）。
  - **last_dance** = `ext/monitor-round2-probe/policies/last_dance_56720309.py`（11,351 行 / 562,245 B）+ 上游 `ext/mqingcs_upstream/kernel_output/main.py`（6,917 行 / 1,026,965 B，sha256 a16e0e9b…）。vs H1 **0.8333**（10W2L；mqingcs-pooltest 2026-10-03）。
- 对照基座：`fn_work/legacy_software/kaggle_simulations/v48_derivative/main.py`（1,221 行 / 107KB）。
- 纪律：不改 INDEX/JOURNAL/registry；不 commit；本文为分析产物（引用纪律：全部结论出自上述本地实抓归档，行号=本仓路径现物）。

---

## ① 覆盖判定表

### 七维

| 维度 | romansvet | WHmaoxian r4_2/r5 | last_dance(+上游) | v48（我方基座，对照） |
|---|---|---|---|---|
| **体量分层** | 提交包 38 文件/32,141 行：`core/plan.py` **15,826 行(49%)** + `agent/v56kernel.py` 6,751 行(21%，内嵌 1MB 公开内核源码) + brain 1,445 + route_vrp 2,046 + runtime 1,093 + policy 854 | 单文件 8,327 行，但 1.1MB 中 **~647KB 是两条压缩数据字面量**（L947 `_R108_DATA` 94,551 字符 + L3419 `_V92_P_BLOB` 553,082 字符）；逻辑层=~30 个 20–60 行装饰器层（V219→R37→R85→R95→V9 系→…→IDF→NGTX→ENDX→HPX→hpx2 末入口 L8326） | 11,351 行 = 上游 6,917 行底盘 + **4,434 行 mqingcs 自有增层**（JFJH-V22W/V22Y/XRL1/WCT/EOD/V22D/d0c + v33–v40 防御链）；另有 observed 分支含 3 成员 tanh MLP 集成选择器（`observed_56713902_009.py:905-918`） | 1,221 行；12 个捆绑模块从压缩 blob 装载（L421 `_V48_MODULES`），本质=路由磁带+启发开关 |
| **引擎语义耦合点** | 全域：`spec.py` 74 常量直录引擎参数；brain 按"float32 幂二尺度、逐日 floor、tie-break 最低下标"复刻引擎决策语义（brain.py:304-312 [LAW] 注释链）；plan 按引擎动作行序（unit 先于 market）编码；route_vrp_c.c 逐 IEEE 双精度复刻 route_key | `adj={(4,4),(5,4),(4,5),(5,5)}` shed 邻接集硬编码于每层（NGTX 8118、ENDX 8198、HPX 8276）；4 步/回合市场节奏（`t%4`）与 24 步/日；价格函数 `_r37_market_price` 按 base/T/above/below 参数走库存边际 | 同 r4_2（同底盘）+ 独有：`_v18_standard`（7475）配置指纹门（boardSize/turnsPerDay/shedCapacity/maxOrders 全等于默认才启用防御层）；`_wct_draw`(10104) 按 `unlocked_shops` 精算城镇抽取 | `_V48_CONFIG` 4 个回合阈值（yarn_first_start=88 等）；`clone_*` 检测参数 12 个（L1202）；无价格走线模型 |
| **校准常量密度** | **~1,094 个模块级大写常量**（plan 501+v56kernel 209+brain 52+spec 74+ops 53+route_vrp 49+…）；plan.py 内 374 处 `[SWITCH]` 标记，`_ON=True/False` 特性开关约 66+ 个（policy.py:546-548 自述） | 逻辑区 ~265 个赋值常量 + 4 个 `_CFG` dict；核心校准=NGTX(order/margin/cap)、HPX(items 阈值)、IDF、V9_OPENING_TAPE | WCT 块 13 常量（10088-10100）+ WCTG 4（10149-151）+ WCTC 2（10189）+ WCTV 2（10224）+ HC 3 + RI/PR/MF 各若干；上游底盘继承 ~200+ | **6 个**模块级常量 + 2 个 config dict（L1201/1202） |
| **防御卫生层** | MELON_DENY/OPEN_DENY/MELON_VETO_FLOOD/LATE_STRAW_CAP（plan 1457/2098/2557/2520）；OVERFLOW_GUARD v1-v3（606-616）+ overflow.py 救援；CLIP_CAP；ZEROGATE/KERNEL2_ZERO（runtime 62-71）；对手家族分类→供应曲线投影（projector 126-147） | NGTX 仓库溢出保护（8087-8160）+ 小麦价格门（8232-8246）+ ENDX 收尾清仓（8166-8224）+ HPX 高价出货（8252-8318）——全部"只动 market 不动路线" | **全场最深**：五级防御门（见 ②-3）+ 终局实物清算模拟器（上游 E182：712-718 步 64 次确定性模拟+支配性检验） | clone 检测/先占/veto（gold_floor 配置）；无市场侧防御 |
| **终局段** | ENDROUTE/ROW2/ENDROUTE2/SPLIT（1031-1228，终日最后两行卖单/回合预算再切分）、LOT4 第 4 卖行（866-883，turn 17）、SHED_DUMP_ROW h23（944-951）、SELL_SPREAD（1267）、ENDGAME_TOMATO 彩票（2387）；overflow 的 TERMINAL_DEPOSIT_VALUE_ON | ENDX：day28 h12 起清饲料小麦+肥料（8172/8190）；NGTX `step>=718` 硬停（8109） | 上游 E182 物理收尾规划器（`plan_terminal`：max 256 次模拟、`dominates` 检验基线每个工人押金前缀、718 步整仓 liquidation）；ENDGAME 层 `_terminal_liquidation`(901) | `terminal_rule='collision'`（L1201）单开关 |
| **开局磁带形态** | 三形态并存：①`opening.py` 环境变量拼接回放录制开局（src，未随提交）；②MELON_OPEN/MIRROR_OPEN planner 原生重演（plan 1283/1712）；③**KERNEL2 双内核闩**：day-0 对手现金≤`KERNEL2_CASH_MAX` 即整局切换到内嵌 V56 公开内核 exec（runtime:22-28,660-702） | V9_OPENING_STEP0/TAPE 两步市场带（3356-3358），逐字校验上游带未被改动才替换（3370）；路线=94KB 路由字面量按商店序列选 route（948-975） | observed 分支：双专家各跑 namespace，step2 按"对手≥5 手且 farmer 未动"选支（contingent 角色交换 016）；last_dance 继承底盘开局 | v21 路由磁带记忆搜索（捆绑模块） |
| **可述策略 vs 工程承重** | **≈7% : 93%**。可述="ES 网络定当日目标（crew/种植/动物/前瞻）"一句；承重=15.8k 行 planner + 引擎位级协议 + ES 训练基础设施（JAX 位精确 sim、对手阶梯、真机门） | **≈35% : 65%**（逻辑行口径）。每层 README 一句话可述；承重=647KB 路由/生产带 + E180 底盘（283-1173） | **≈25% : 75%**。防御/清算理念可述（README 明文）；承重=对手流核算的位级精度（执行成本下界/收据配对/回合节律）+上游底盘 | **≈80% : 20%**。几乎全可述；工程承重仅压缩装载与回退 |

### 重点追查

| 追查项 | 判定 | 关键证据落点 |
|---|---|---|
| 1. theta 是什么 | **完成** | §②-1；policy.py:391-570/571/638；main.py:54 |
| 2. r4_2→r5 单参数差链 | **完成** | §②-2；r4_2:8142/8230 vs r5:8231 |
| 3. last_dance 防御门细节 | **完成** | §②-3；10155/11011/11320 等 |
| 4. degnonguidi 上游结构 | **完成** | §②-4 |
| 5. romansvet 模块切分 vs 单文件 | **完成** | §②-5 |

---

## ② 关键读数

### 1. theta 形态（romansvet）：7,692 维扁平向量 = 小 MLP + 25 个"基因块"，参数化的是 planner 的偏置而非策略本身

- **载体**：`submission/theta.npy` = **float32[7692]**（30,896 B，npy 头直读）；另有 `core/eswork_theta.npy`=float32[10] 与 `residual_head.npz`（PPO 残差头，v1 版 18 槽位/92 logits，residual_head.py:18-24）。随仓第三类权重=`core/opp_supply/S_{MEL,OTH,P48,pop,PQ4,V56}.npy` 各 (720,9) f4——6 个对手家族的**逐回合供应曲线**（`extract_opp_supply.py` 从 81 盘录像提取，projector.py:43/99）。
- **加载**：`main.py:54` `_THETA = np.load(...)`，每游戏日调用一次 `brain.decide(np, _THETA, po)`（main.py:87）；`policy.unpack(xp, theta)`（policy.py:638）按 `SHAPES`（policy.py:391-570，**43 个命名块**）切片成 NamedTuple。布局是**冻结律 [LAW]**：只能尾部追加，旧 theta 永远是新布局的零填充前缀（唯一例外 g9 桶复制，policy.py:660-671）。
- **作用面（这是复刻难度核心）**：theta 不是策略网络，是"规则骨架的偏置向量"——
  - 共享编码器 `36→64→2`（每产品 grow/sell 分）+ 全局头 `24→32→18`（policy.py:780-810 `forward`）；
  - 追加基因块各参数化 planner 的一个决策旋钮：`g8` 雇工偏置、`g9` 雇工偏置按日分桶（brain.HIRE_BIAS_BUCKETS：0-5/6-10/11-20/21+）、`g10` 雇crew目标 logistic（高度/中点日/陡度+动物延迟）、`cm/cd` 作物对数份额偏好及其按日桶版、**`sw/swb` 21 个开关基因**（把 plan.py 里 `*_ON` 布尔开关变成可学习列，policy.py:333-379 逐次加宽史）、`g12` 施肥前瞻天数、`g11` 雇工扫描前瞻天数等；
  - 开关基因解码=`round(SWITCH_GAIN*z)>0` 翻转模块默认（policy.py:549-556）——**学习调参+规则骨架**的字面实现：ES 学的是"该翻哪些开关、偏置加多少"，15,826 行 plan.py 决定这些旋钮接到哪根杠杆。
- **布局算术（本次 AST 级核算）**：现码 N_PARAMS=**7,791**（21 开关布局）；theta.npy=**7,692** 恰为 19 开关布局（7,065+32×19+19+33）——**随仓权重比随仓代码落后一次布局修订**，靠前缀零填充兼容。布局史：3,827→3,892→4,584→…→6,789（README 所称"shipped champion"）→7,692（随仓）→7,791（代码）。
- **训练产物语义**：`es/train.py:3` OpenAI-ES（antithetic+秩归一+Adam，sigma=0.02/lr=0.02，train.py:212-213），目标=绝对金币（≥2×kagg2≈300k）+少数胜局项；对手池本身也是 theta（`archetypes.py:458 archetype_theta(**knobs)`，expander/rusher/rancher/…/wheat_clone/wool_specialist 阶梯 + kagg2_proxy 残局开局代理）——**训练环境、对手、被训策略三者同一参数空间**。

### 2. r4_2→r5 唯一语义差：`_NGTX_CFG margin` 15→20，通到"仓库+携带溢出保护带"的触发阈值

- **引用链（rg 全量）**：`_NGTX_CFG` 全文件 7 处。定义 L8092（默认 `hours=(22,23), cap=100, margin=0, order=(FERTILIZER,WHEAT,…)`）；核心公式 **L8142** `over = sum(shed.values()) + carried - cfg["cap"] + cfg["margin"]`；按 `order` 顺序卖出仓内低价品直至 `over<=0`（L8146-8152）。r4_2 L8230 覆写为 `hours=全 24 小时, margin=15, order=('WHEAT','FERTILIZER')`；r5 同行 `margin=20`。外层 L8232-8246 再包一层：白天（非 22-23 点）小麦价 `<40` 时撤掉 NGTX 的额外小麦卖单。
- **语义**：夜间自动 DROP 前的溢出保护。margin=15 → 预计(仓库+携带)>**85** 格即开卖；margin=20 → >**80** 格即开卖（提前 5 格清出）。README（r5, 09-30 21:15）自述："R4.2 加一处改动，仓库保护余量 20 格"。
- **单常量敏感度（三方读数汇合）**：
  - WHmaoxian 自测（固定商店模式，排除商店运气）：R4.2 与 R5 在 186 局线上重打**同分 113W73L**，强队 100 局 42W vs 41W——"差 0–1 局，属于噪声，这一类规则已经到顶"（README 表格+结论原文）；
  - 我方 12-fold 池测：两件 h2h 均 0.8333（10W2L，margin +1320.9/+1368.5）；
  - 即：**±5 格余量在这层规则族上已处于收益平台区**——它调的是"保险带松紧"而非"产能"，天花板由上游路线带决定。README 同页的输局分析（"近距离输局=对手每局多卖 4 草莓 6 牛奶；大比分输局=另一套农场规划"）明说这类 market-only 层无法追平产能差。

### 3. last_dance 防御门：五级"检测器不记账"结构，全部建在公开字段的差分核算上

对手麦流观测（`_wctg_observe`, 10155-10187）：
- **公开字段**：`obs['market']['inventory']['WHEAT']`（市场库存）、`obs['town']['unlocked_shops']`（城镇抽取，`_wct_draw` 10104-10112 按 `t%4==0` 店面抽取 + `t%24==0` 中心抽取精算）、自家上回合买卖单（`_wctg_record` 10245-10258）。
- **累积**：`rival = inv_prev - inv - prev['buy'] + prev['sell'] - _wct_draw(shops, t)`（10164）——每回合重构对手净流。回合节律门：t%4==3 的 pre-draw 买入≥`_WCTG_MIN=20` 且 t%4==0 的 draw-turn 卖回≥60%（`_WCTG_SELL_FRAC`）计一对"guard_event"；**满 `_WCTG_EVENTS=6` 对→`predator=True`**，WCT 携带交易停开新仓（10338）。

carry 清算的"执行成本下界"（`_mr_cost_lower`, 11011-11037）：
```
cost_lower = prev_money - now_money + other_lower - fee_upper
normal     = Σ_{k=1..qty} price_WHEAT(inv_prev - k)     # 库存边际走线的理论成本
rival_net  = inv_prev - inv_now - draw - qty
```
- `fee_upper`（`_mr_fee_upper` 10970-10981）：HIRE 按斐波那契 `_WCT_FIB` 爬价、BUY_LAND (1000,2000,4000)、种子/动物按 `_WCT_SEED` 表——**同回合混合订单的费用上界**；
- `other_lower`（11014-11033）：混合收据里其他品卖出的收入下界（对手卖出全部排在我方之前的最低价排列；FERTILIZER 特判对手持有上限 100）；
- **判定**：`rival_net==0`（对手当回合零净流）且 `cost_lower > normal`（实际花销超过纯走线成本）→ 记一次事件（`_hg_receipt` 11039-11056）；满 6 次→激活防护。"检测器不记账"：这些事件**只计数不进损益**，WCT 的盈亏估计仍用走线模型 `_wct_gain`（10143-10146）与对手锁步模型 `_wctc_gain`（10194-10207，双方按同快照报价交错走库存边际）。

realized-loss 检测与试用期状态机：
- `_ri_receipt`（11232-11241）：反转往返单（reverse_roundtrip，同回合 BUY+SELL 队尾配对）实收 upper<0 → `losses>=2 → disabled`（本轮永久禁用反转层）；
- `probation_entry`（11320-11345）：**试用期 = `el_until = step+24`（一个游戏日）**；到期时若自家独立 lot 未清→等清仓；若三种可见证据（g_events/dg_events≥6 或 v_stop）均无→`predator=False` 恢复，否则继续防；events≥6 则 `el_until=None`（永久）；
- `risk_probation_entry`（11352-11363，**文件末位 callable=实际入口**，pooltest 报告 13 行确认 entry=risk_probation_entry）：报价缺口见证——`quoted = Σ price(inv+k)`（当前报价的清仓值），`cost_lower > quoted` 时无需等 realized loss 即临时激活（24 步试用）。
- `_wctv`（10229-10242）：跨 lot 边界的对手"卖出≤−15 再买回≥+15"模式，4 次→`v_stop`。
- 全链前有 `_v18_standard`（7475）配置指纹门 + `_MR_ALLOWED`（11061-11064）市场参数指纹门——**任何环境参数偏离即整体退化为底盘**。

### 4. degnonguidi 上游（1MB）："血统源头"承载的是两条巨型压缩常量 + 终局物理清算器

- 结构（6,917 行 / 1,026,965 B）：L1-23 谱系注记（thomastschinkel 93.8% State Router ← V39/V55/V56 ← prvsiyan V221B/V224C ← yhay81 shop-router 磁带 ← …）；**L947 `_R108_DATA` = 94,490 字符 base85+zlib**（81 条路线/商店序路由表）；L1020/1022 `exec()` 内嵌 **E182 终局收尾规划器**（712-718 步，`max_simulations=64`，`dominates` 支配检验：候选不得损溢出、不得低于基线各工人押金前缀/可卖量）；**L3419 `_V92_P_BLOB` = 553,065 字符**（整季生产磁带）；末段 L6642-6654 `final_price_guard`（卖价阈值 31）→ `kaggle_submission_agent`。
- **下游依赖方式（为何是"源头"）**：mqingcs 包把两条巨型字面量**替换为 AST 前缀匹配取数**——`publication_assets.value()` 用 `dependency_spec.json` 的 `characters+prefix` 在上游 main.py 的 >1024 字符字符串常量中唯一匹配（publication_assets.py:13-42；PROVENANCE.md 26-39 实测 5 常量 {1823,12009,22861,94490,553065} 全 UNIQUE-OK）。即 last_dance/observed 的路由与生产数据**物理上只存在于上游仓**，下游按 (长度,前缀) 引用。
- kernel 日志自报（best-agent-ranking.log）：入口 `_cxd_agent wraps _cxtb_agent`；装载 measurements(per_opponent/round_robin/total) 后报告 "280 paired games: 191-53 → 280-0; 89 losses turned into wins; mean margin +758"——该 kernel 本身是个**候选层选择/排名器**，输出优选后的 main.py+tar。

### 5. romansvet 37 文件工程的模块切分 vs 我方单文件传统；numpy/C 用在哪

- 切分逻辑（submission/ 38 文件=37+lock）：`main.py` 100 行纯入口（自述"曾是 hand-copy 的 Runtime.act 因脱Patch而漂移，改为委托"）→ `agent/`（运行时/解析/渲染/路由 12,130 行）+ `core/`（brain/policy/plan/valuation/sell/budget/projector/ops 20,011 行）+ 权重三组随包（theta/residual/opp_supply）。src/ 侧另有 sim/（JAX 位精确环境）、es/（训练器）、S/pipeline（跑批判决）、scripts 30 件、tests——**训练基础设施与提交物同仓同构**（plan.py 写成 xp= numpy/jax 双后端同码）。
- **C 扩展**：`agent/route_vrp_c.c`（254 行，-nostdlib，ctypes 装载，无 Python ABI）——route_vrp 热循环（route_eval/_sim、best_insert、2-opt）的**位精确移植**（`-ffp-contract=off`，route_key=elapsed+0.01*moves 的 IEEE 双精度同序），加载失败自动回退 Python 路径。numpy 用于：每步 forward（纯 numpy）、plan 的数组化整日规划（`PLAN_FASTPATH_ON`）、opp_supply 曲线插值。
- 与我方 v48 对照差距点：①**无权重 vs 三组权重**（theta 7,692+残差头+6 对手曲线）；②**6 个常量 vs ~1,094 个**；③v48 无价格走线模型/无对手流观测/无溢出保护层，路由碰撞即终局；④v48 失败回退=PASS（1206-1220），romansvet 的等价层是 KERNEL2 双内核+VRP 修复重解。

---

## ③ 异常与限界

1. **池测分口径**：任务简报称 r4_2/r5"各 0.8333/0.75"，但本仓既有实测（2026-10-03-whmaoxian-license-harvest.md §快筛表）为 r4_2 0.8333 / r5 **0.8333**（10W2L 各 margin +1320.9/+1368.5）。本文按实测口径；0.75 出现于该表 r3 行与 romansvet/taeyan 的 r40、A 弱锚面。对 margin 敏感度结论无影响（两读数都=平台区）。
2. romansvet 提交包内 `v56kernel.py` 含 1,056,142 B 公开 V56 内核源码（Apache-2.0，sha256 a1ad0fd1 自报未复核）；KERNEL2 闩默认值（`KERNEL2_CASH_MAX` 等）未逐常量摘录——该件 0.8333 的战功中 V56 内核贡献占比**未能从静态分析分离**（需动态逐局统计 k2_mode）。
3. last_dance 的 observed 分支任务库（`observed_56713902_009_010`）按 PROVENANCE 属 UNRUNNABLE（私有资产未随包），其 NN 选择器（3 成员、98 维归一）只读了代码未跑。
4. degnonguidi 上游"280-0"等自报数字来自 kernel 日志，未独立复核；其与 WHmaoxian r4_2/r5 的共同祖先关系是**同头注+同字面量行位**的推断（L947/L3419 两 blob 前缀与 dependency_spec 精确匹配），未做全文件 diff 谱系学。
5. 本次静态核算 N_PARAMS 用的环境常量值（N_PROD_FEAT=12 等）取自 policy.py 自身声明与 spec 语义，若 spec 与本核算有出入以仓内 `python -c "from kagg3.core import policy; policy.N_PARAMS"` 为准（未执行，bwrap 纪律下的自愿限界）。
6. v48_derivative 仅审 main.py 装载层；捆绑模块（v23.planner 等）在压缩 blob 内未解包逐行审。

---

## ④ 对"从零复刻为何失败"的代码证据建议

三件 0.8333 冠军件给出同一结论的三种证据形态——**可述策略层很薄，工程承重层才是分差来源，且承重层各自锁死在一个不可从描述重建的资产上**：

1. **romansvet：复刻难点不在"ES 训了个网络"，在"网络只占 7%"**。theta[7692] 参数化的是 15,826 行 planner 的偏置与开关（21 个开关基因把 `*_ON` 布尔变成可学习列）；没有那份 plan.py（501 常量、374 处 SWITCH 标记、引擎 float32 幂二尺度律），theta 是无锚向量。从零复刻=重建"骨架"而非"调参"——我方 v48 的 6 常量骨架与该骨架之间差三个数量级的引擎语义耦合。
2. **r4_2/r5：单常量敏感度证据反过来说明"末梢规则不可救"**。margin 15→20 在作者 286 局与我方 12-fold 两套度量下都是 0-1 局噪声；README 明言产能差（路线层）才是输局根因。任何"再调一个防护常量就能上去"的复刻路线被这份 A/B 证据直接否决——**收益在 647KB 路由/生产磁带里，不在末梢 CFG**。
3. **last_dance：防御门的护城河是核算精度而非检测理念**。对手流=rival 差分公式人人可写；但"执行成本下界"要同时压住斐波那契雇工费上界、对手持有上限特例、混合订单收入下界的最不利排列、4 步市场节律与商店抽取精算，且任何环境指纹偏离即整体退化为底盘（`_v18_standard`/`_MR_ALLOWED` 双门）。复刻漏任何一项，检测器从"不记账的计数器"变成"误触发/漏触发的噪声源"。
4. **degnonguidi：血统资产的物理依赖**。下游件按 (长度,前缀) 从上游 1MB 中"借"两条数据常量——冠军生态是**层叠复用+按字节锚定**的，从零复刻没有可锚的源头字节。
5. **共同形态**：三件的终局段（ENDROUTE 系列/E182 物理清算/ENDX）与开局资产（KERNEL2 闩/V9 磁带/双专家选择）合计都超过其"策略描述"的信息量。建议复刻失败根因报告把这三条写为主证据链：**(a) 权重/磁带资产不可重造、(b) 末梢常量平台区、(c) 防御核算的位级契约**；对照我方 v48（6 常量、无价格模型、无防御层、终局=碰撞规则）逐项标差。

---

## 需登记行（INDEX.md，按台账格式，本报告不自行写入）

```
| 2026-10-03-champ-anatomy-2.md | 本地实抓归档静态分析（来源同 2026-10-02-opensrc-pooltest / 2026-10-03-whmaoxian-license-harvest / 2026-10-03-mqingcs-pooltest 各自登记的拉取） | 2026-10-03 | 三冠军件字节级解剖：theta 形态/_NGTX_CFG 链/防御门/上游分层 | 复刻失败根因分析（champ-anatomy 系列） |
```
