# 公开 bot 源码逆向精读（v48 / kaitofukami）——点火竞速的对方解法

- 日期：2026-09-20。任务：Track-B 公开 bot 源码精读，回答"我方 500-550 分段 m5k 点火 d13-18，对方 ≥85k 巨人 d10-12 点火"的机制差。
- 上游原件：`references/data/intel-notebooks/`（抓取 2026-08-31）：
  - `v48_main.py`（108KB 构建器）与 `v48build/main.py`（107,008B 解码件，sha256 `dadee25a…2664a`，与 `v48_main.py` 内嵌断言一致、与 `v48build/submission.tar.gz` 字节一致）——**v48 bot 完整源码**，作者 kaitofukami（见 `h2h_v48.json` "opponent" 字段与 notebook `40-40-early-floor-39-46-top-10-v48-fast-routes.ipynb`）；
  - `submit/main.py`（157,899B，sha256 `59b96bd9…8b53d`，= `submit/submission102.tar.gz` 内 main.py）——**经比对是我方自家旧单文件提交（"轮作牧场" r5-P4 / v7.2-V1 实验树），不是对手 bot**（docstring 与我方 `software/kaggle_simulations/agent/src/_archive_header.py:105` 逐字同源；`h2h_v48.json` 里我方当时候选 sha 为 `39862ddc…`/`f0bcd657…`，均非此件，系 v7.2 树的姊妹版本）。
- 引用约定：`v48:模块名:L行号` = v48build/main.py 内嵌 payload 解码后各模块源码的模块内行号（本会话实读）；`v48build/main.py:L行号` = 外层驱动文件真实行号；`submit/main.py:L行号`；我方代码 `src/xxx.py:L行号`。引擎常数引自 `references/digests/engine-factsheet-2026-09-19.md`（起始 $3000、地价 1000/2000/4000、雇工日薪 fib、雇工 EOD 清零、市场逐件 lockstep、maxMarketOrdersPerTurn=10、shedCapacity=100）。
- 时效：代码为 **8 月末（2026-08-31 前）meta**，目标引擎 1.32.7。9 月公开代码锁 09-23；meta 漂移风险见 §10。

---

## 0. 一句话画像

- **v48（kaitofukami，top-10 持榜作品）**："离线轨迹记忆 + 在线稀疏路由"——把从真实快爬选手（Kaileh57、taiseiu）轨迹里搜出来的 **6 条 719 步完整对局宏脚本** 打进包里，开局一律播 `default`，到步 88/120/153/216 按公开商铺事件一次性切换（每席至多一次），再叠加**反克隆抢卖**、**影响分卖单排序**、**718 终局清仓**三个窄反馈器；全程无逐回合规划，每回合只评估一个子策略（1 秒预算内绝对安全）。
- **submit/main.py（我方旧 r5/v7.2 单文件）**：全反应式四层（宏观模式门 → 规划 → 任务调度 → 市场门控），当时代码里已自带 R3-1~R3-4 的赢家画像注释（d0 畜群爆发 / 12 头 d11 死线 / 草莓 d5 起 / crew 12），**与 v48 打 16 局 0-16 负、净负 ~6.8 万/局**——输的不是框架，是**开局序列的精确度**。

---

## 1. v48 架构（问题 1）

### 1.1 模块清单（12 个内嵌模块，v48build/main.py:L421）

| 模块 | 大小 | 职责 | 关键行 |
|---|---|---|---|
| `v48.fast_route_router` | 5.5KB | 6 路由一次性切换 + 每回合单子策略 | L1-13 设计说明；L30-37 ROUTES；L58-94 `route_event`；L97-174 `build_fast_route_router` |
| `v44.gold_floor` | 28.8KB | 路由选择、bakery 资本分支、反克隆抢卖账本 | L39-115 GoldFloorConfig 全量旋钮；L122-157 `selected_route`；L180-204 `bakery_capital_candidate`；L206-228 `clone_veto_candidate`；L317-648 `CloneSellPreemption`；L650-755 `build_gold_floor_router` |
| `v24.market_maker` | 29.6KB | 储备安全的单 tick 做市专家（v48 现役配置**关闭**） | L38-58 config；L141-165 `demand_on_step`；L559-841 `MarketMakerExpert` |
| `v23.state_encoder` | 7.4KB | 观测→紧凑状态（需求/价格/库存/双方 exposure/shed/种子） | L21-41 价格与商铺表；L86-110 `shop_demand_per_day`；L155-208 `encode_state` |
| `v23.simulator` | 6.4KB | **引擎 1.32.7 价格曲线的精确转写** + 单边卖单逐件收益模拟 | L18-28 MARKET_PARAMS；L51-65 `market_price`；L68-78 `execute_sell`；L148-177 `best_sale_quantity` |
| `v23.policy_library` | 6.2KB | 卖单槽位重排、有界 MPC 卖量、终局清算 | L54-79 `reorder_sell_slots`；L82-131 `plan_sell_quantities`；L134-151 `terminal_liquidation` |
| `v23.planner` | 3.3KB | 每条路由的稀疏闭环封装 | L14-18 PlannerConfig；L20-64 `build_sparse_planner`（注释明说"路由切换与卖量 MPC 因 holdout 无增益而故意缺席"） |
| `scripts.v22_market_impact` | 5.9KB | 价格冲击分 + 只重排既有 SELL 槽位 | L24-34 引擎参数副本；L90-113 `impact_score`；L125-146 `reorder_market` |
| `scripts.v22_weed_repair` | 4.8KB | 杂草碰撞事务修复（DIG→重试→≤8 步回放） | L26-122 `wrap_weed_repair` |
| `v19_terminal` | 12.8KB | 终局覆写：手数对齐、棚仓投影、克隆距离、718 清仓、717-718 单位覆写 | L52-65 `align_hands`；L68-128 `projected_shed`；L177-187 `clone_distance`；L190-239 `terminal_market`；L264-308 `monetizable_terminal_units` |
| `scripts.v21_route_memory_search` | 296B | 开环回放器（整条路由照读） | L4-8 `replay_policy` |
| `scripts.v19_terminal` | 重复件 | 同上 | — |

### 1.2 状态机/规则层级

**没有经典状态机，也没有逐回合前瞻。** 层级是：

```
观测 → [路由选择器：只在 4 个预设决策点判一次，latched]     (v48:gold_floor:L122-157)
     → [子策略 = 开环 719 步脚本回放]                        (v48:v21_route_memory_search:L4-8)
     → [杂草事务修复：碰撞时 DIG，重试+≤8 步回放]             (v48:v22_weed_repair:L26-122)
     → [SELL 槽位按影响分重排；rebalance 制加需求恢复加权]     (v48:policy_library:L54-79)
     → [反克隆抢卖：近克隆锁存后把 step+2 的计划卖单提前执行]  (v48:gold_floor:L317-648)
     → [718 步终局清仓（collision 规则全量替换卖单）]          (v48:v19_terminal:L190-239, router L155-162)
```

- **前瞻/模拟只存在于三处窄域**：① `v23.simulator` 的市场价格 rollout（卖量 MPC，`best_sale_quantity` 在 {0, q/4, q/2, 3q/4, q} 里带 250 切换成本搜索——但 planner 注释明说 holdout 无增益、未启用，v23.planner:L26-28）；② 反克隆的"未来卖单槽位"读取（把 step+horizon 的计划卖量搬到现在，同时记账"欠债"到原槽位扣除，gold_floor:L535-587）；③ market_maker 的往返套利模拟（v48 未开）。
- **动作生成 = 照剧本 + 三个被动修正器**。作者在 docstring 里给出选型理由：每回合只跑一个子策略，"比每个子策略各带闭环控制器便宜且更安全"（router:L10-12，针对 actTimeout=1s）。
- **准点路由（v48build/main.py:L1201-1202）**：`yarn_first_start=88, farm_first_start=120, yarn_second_start=153, yarn_third_start=216`；Gold 覆盖 `clone_preempt_horizon=2, clone_streak_required=24, clone_distance_threshold=2.0, clone_detection_start=48, clone_maximum_batch=10, clone_active_start=160, bakery_capital_start=160(第二店 PIZZA_SHOP), clone_veto_step=120(BAKERY 首店且对手羊≥4/牛≤1/麦≥8/瓜≥7 时否决抢卖)`。
- 路由共享前缀 **88 步**（实测：6 条路由前 88 步逐字节相同）——**即 d0~d3.6 的开局是全路由统一、无条件执行的**。

### 1.3 反克隆机制（他们独有的对手利用）

`clone_distance`（v19_terminal:L177-187）= 双方**公开农场签名**（手数 + 3×象限数差 + 11 类地块计数逐项绝对差）之和 ≤2.0 即"近克隆"。连续 ≥24 步（自 step 48 起）→ 锁存；step≥160 后每回合检查 step+2 的计划 SELL，在 10 单限额内、按价格×数量降序把 ≤10 件搬到现在卖，同时把同等数量记为"欠债"，未来槽位执行时逐件扣回（gold_floor:L481-505 的 due 账本保证总量守恒；L445-446 的 clone_veto 防止对手"羊重开局"误触发）。另有市场库存流证据升级器（phase detector，v48 配置关闭）。**本质：镜像局里抢在对手同一件货之前卖，吃曲线顶部。**

---

## 2. d0-d3 精确开局序列（问题 2）

### 2.1 v48 `default` 路由逐日表（实测解码，前 88 步全路由共用）

引擎常数：起始 $3000；SHEEP $500/首产 d6/每 3 天 6 单位；COW $400/首产 d8/每 2 天 6 单位；MELON 种 $80/首产 d10/一次性 6 单位；WHEAT 种 $10/窗口 2-4/6 单位；雇工日薪 = fib(1..k) 之和。

| 日 | 雇工(当日 crew) | 买入（market 单，量） | 卖出 | 单位动作（全队 24 步合计） | 日终现金估算 |
|---|---|---|---|---|---|
| **d0** | **2** | **BUY_ANIMAL SHEEP×4**（2000）；BUY_SEED MELON×7（560）；BUY_SEED WHEAT×5（50）；BUY_PRODUCT WHEAT×8（≈200）；HIRE×2（2） | — | BUILD_PASTURE×4、PLACE SHEEP×4、PLANT×12（瓜 7+麦 5）、WATER×12、FEED×4、CARE×4 | **≈$190**（3000−2812） |
| d1 | 3 | BUY_SEED WHEAT×5、STRAWBERRY×2；BUY_PRODUCT WHEAT×7；HIRE×3 | **SELL FERTILIZER×4**（≈400） | COLLECT_FERTILIZER×4 起、DROP×4、PLANT×4 | ≈$400-600 |
| d2 | 3 | BUY_PRODUCT WHEAT×6；HIRE×3 | SELL FERTILIZER×4 | WATER×15、COLLECT×4 | ≈$500 |
| d3 | 3 | BUY_SEED STRAWBERRY×1、BUY_PRODUCT WHEAT×4；HIRE×3 | SELL FERTILIZER×4 | 同上 | ≈$400 |
| d4 | 3 | **BUY_ANIMAL COW×1**（400）；BUY_SEED WHEAT×5；HIRE×3 | — | HARVEST×5 起、WATER×20 | ≈$500 |

要点：① **d0 一步把 3000 花到 ~190**，畜(2000)+瓜种(560)占 85%；② 4 羊不是现金工具而是**定时炸弹**——d6 首产 4×6=24 羊毛一次变现；③ 瓜 7 株是第二颗炸弹——d10 一次性 6×7=42 单；④ **肥料从 d1 起就是日结现金流**（COLLECT 4/天→当天卖）；⑤ d0 crew 只有 2 雇，**crew 与畜群解耦、按日租随任务量爬坡**（对比：Wei Han d0 crew=7）。

### 2.2 实战对照：Wei Han（loss_weihan.json，本局 80259 分，seed 170790858）

| 日 | crew | 关键动作 | 日终现金 |
|---|---|---|---|
| d0 | **7** | **BUY_ANIMAL COW×3**（1200）+ BUY_PRODUCT WHEAT×24 + BUY_SEED MELON×6 + HIRE×7；种瓜 6 格 | **$545** |
| d1-d7 | 3→10 | 每日 SELL FERTILIZER×3；草莓每日 1-2 格慢种；7 瓜在田 | $700± |
| d8 | 11 | **SELL MILK×18**（3 牛首产 3×6 ✓，≈$4.1k）；草莓+7、瓜+4 | $2361 |
| d11 | 11 | **SELL MELON×36**（6 瓜×6 ✓）；**BUY_LAND×2**（NE+SW 同日）；BUY_ANIMAL GOOSE×4；草莓种到 28 | $2951 |
| d12-13 | 12 | 鹅到 6、MILK×12/6 续卖、草莓田 39→50 格 | $1892-2636 |

两位 ≥80k 选手的共性：**d0 把 75-95% 现金换成"定时资产"（畜+瓜），只留 <600 过夜；作物组合是设计好的现金流波次：羊毛 d6 / 牛奶 d8 / 瓜 d10-11 → 每一波到账立刻转下一轮资本开支（地/畜/crew）**。对照我方现状（d0 3-4 头畜但 d12 现金仅 ~700、m5k 点火 d13-18）：差距不在"买没买畜"，而在**没有 d0 波次设计 + 点火靠现金阈值触发而非日历触发**。

### 2.3 买地吗？——d0-d3 不买。第一块地 v48 在 d6（$1000），Wei Han 在 d11 一次买两块。

---

## 3. d4-d12 点火引擎（问题 3）

v48 没有"点火条件"，**点火是排进剧本的日历事件**（default 路由实测）：

| 日 | 资本事件 | 资金来源（同日/前日变现） |
|---|---|---|
| d5 | crew 3→6（HIRE×6）；草莓种 ×9 | 肥料 11 份 + 小麦 6 份卖出 |
| **d6** | **BUY_LAND #1（NE，$1000）+ BUY_ANIMAL COW×5（$2000）** | **SELL WOOL×24**（4 羊首产，≈$5.0k） |
| d7-d8 | COW×2、COW×1（羊群转牛群：奶 > 毛）；crew 6-7 | 肥料 5-6/日 |
| d9 | crew 8；外购 WHEAT×11（饲料不再自给） | 肥料 15、羊毛 22 |
| **d10** | **BUY_LAND #2（SW，$2000）+ COW×2 + crew 6→12 + 草莓种×13 + 瓜种×4** | **SELL MELON×48**（≈$12k） |
| d11 | crew 13；胡萝卜种×8；外购麦×11 | 肥料 13 |
| d12 | **第一波牛奶上市 SELL MILK×6**（d4 牛首产）；肥料一次性清 39 份 | — |

机制归纳（回答"规模化何时启动、条件是什么"）：
1. **没有现金阈值、没有格子数条件**——条件全部是**公开商铺事件 + 步数**（88/120/153/216），资产波次按作物/牲畜的生物钟（首产日）倒排种植/购买日。这就是"他们 d10-12 点火"的真相：d10 的瓜 flush 是 d0 种 7 株瓜时就定好的。
2. **买地节奏**：d6 一块、d10 一块（正好卡在两波变现之后），第 4 块（$4000）**从不买**——全路由 30 天只有 2 单 BUY_LAND。
3. **雇佣节奏**： crew 与畜群/田联动阶梯 2→3→6→8→**12(d10)→13(d11)**，之后每天 10-13 重雇（日薪制，d10 全天 crew 成本仅 fib 和 ≈$376）。**我方 v14 的 `_crew_target`（src/strategy.py:L184-201，随 herd 顶到 HANDS_CAP_R3=12）在"量"上已对齐赢家画像，但触发是 herd 目标而非日历**。
4. **外购饲料**：从 d0 起每天 BUY_PRODUCT WHEAT（4-11 份/日），**完全不做饲料自给**——小麦底仓只留 5-7 格给开局周转，中后期全靠外购（对比我方 FM-O3 已同向，FEED_BUY_MAX_PRICE=36 门在 submit/main.py:L757、我方 src 继承）。
5. **畜群结构按商铺世代切换**（router L58-94）：首店 YARN_STORE→yarn_fast（d7-9 改买羊×2/日，羊毛线加深）；首店 FARMERS_MARKET→farm_fast（近默认）；BAKERY+对手瓜≥10/牛≥3→bakery_capital（gold_floor:L180-204）。**即"哪个店先解锁就重仓哪个产品"被写成了路由表**——我方 phase_branch_plan 的"城镇吸收表"思想相同，但他们是 719 步粒度的完整预案而非当日参数包。

---

## 4. 卖出策略（问题 4）

1. **清仓纪律，几乎不囤**：每种产出首产即卖、当日卖清（羊毛 d6 一次 24；瓜 d10 48；肥料最多囤到 d12 一次清 39——d12 的 SELL FERTILIZER×39 是全路由最大肥料单）。唯一"囤"是 WHEAT：中期随收随卖小批，d26-29 集中倾销（d29 单日 SELL WHEAT 合计 ~150 份+胡萝卜 51+肥料 19）——利用麦 log 曲线"不崩"的特性把麦当季末储备货币。
2. **没有价格门槛卖单**（路由内没有"低于 X 不卖"逻辑；价格仅用于排序与抢卖），对比我方 WHEAT_SELL_GATE/MILK 105/WOOL 150 的门槛体系（submit/main.py:L777、src/market.py）。
3. **卖单顺序是显式资产**：同回合多 SELL 按 `impact_score = 量×(现价−卖后价)` 降序重排槽位（v22_market_impact:L90-113；policy_library:L54-79；rebalance 制加需求恢复加权 ×(1+0.25×urgency)）——10 单限额下"先卖跌得最快的"。
4. **终局 718**：`terminal_market(rule='collision')` 全量替换卖单——卖掉 projected_shed 的一切，排序分 = `(1+对手该品 exposure)×glut 权重×价格×log(1+量)`（v19_terminal:L190-239；GLUT_WEIGHT 瓜 3.6/毛 3.2/莓 2.0，恰好是 above 曲线的曲率排序）；配合 `monetizable_terminal_units` 在 717-718 强改单位动作（背包有货→DROP、距棚 1 格→走近、站在棚口熟田→HARVEST，v19_terminal:L264-308）。**比"末日清仓"多算了两步：把 717 步也变成变现步。**
5. **反克隆抢卖**（§1.3）：镜像局把 step+2 的卖单提前——卖出时机本身是对手条件的函数。

---

## 5. 与我方 v13.8/v14 的架构差异（问题 5）

### 他们有、我们没有（top-5）

| # | 机制 | v48 出处 | 我方现状 |
|---|---|---|---|
| 1 | **" validated 波次开局"作为可执行剧本**：d0 资产配置→首产日→变现日→下一笔资本开支，整条链按生物钟倒排并整段验证过（40/40、39/46 holdout，v48_main.py 尾部 manifest） | 路由表 + v48_main.py manifest | 我方有目标画像（R3-1~R3-4、phase_branch_plan P0 v1.5）但仍是"计划约束 + 反应执行"，无逐日逐单的验证基准；d12 现金 ~700 说明波次没接上 |
| 2 | **公开签名克隆检测 + 抢卖账本** | v19_terminal:L177-187 + gold_floor:L317-648 | opp_supply_observer_design.md 在册（反推系统）但无"对手近似我→卖单前移"这条市场侧利用 |
| 3 | **SELL 槽位影响分排序**（同回合 10 单内的微观 sequenc­ing） | v22_market_impact:L90-113 | 我方 market.py 有价格门与分批，但未见"同回合卖单按价格冲击重排" |
| 4 | **717-718 两步终局机**（单位动作强改 + 市场单全量替换 + 对手 exposure 加权排序） | v19_terminal:L190-308 | 我方 d29 清算完整（scheduler v1.4 F10）但 d28/29 边界的两步级变现与 exposure 排序未做 |
| 5 | **商铺世代→完整预案路由**（首店身份一次性定整局经济线） | router:L58-94 + 6 条路由 | 我方 `_decide_mode`（src/strategy.py:L398+）以价格/ readiness 为主，商铺键只在城镇吸收表层面，无"首店→整局预案" |

### 我们有、他们没有（勿误伤）

- **逐回合闭环任务调度**（mission→solver→executor，worker_route_scheduler_design v1.4）：对任意扰动的鲁棒性远高于开环剧本——v48 只用 DIG 事务补丁（weed_repair）兜底，剧本一旦大偏移无法自愈；我方红线层（断水/断粮/末日归还）与流动性台账他们完全没有。
- **价格红线族**（CROP_FLOOR/CROP_PHASE、WOOL_CUT_LOSS=45、FEED_BUY_MAX_PRICE=36、死价冻结，submit/main.py:L581-582/757/777；src/strategy.py:L680-703 `_curve_gate_ok`）：v48 剧本内零价格门，好年景是优势、坏年景（价格崩/需求 drought）会硬撞。
- **NPV 扩栏门 + 容量定律 + 熔断**（src/strategy.py:L228-277 `_npv_herd_decision`、L654-677 `_capacity_gate`、L925 熔断）：v48 的畜群量是剧本常数。
- **对手开局分类器 / 阶段检查点 / B 分支**（src/strategy.py:L590 `_classify_opponent_opening`、d1/d6/d10/d14 checkpoint）：比他们的 4 个静态步数判断语义更丰富。
- ** rebalance 双制适配**他们有（regime_from_configuration），我方亦需确认 TownCenter 参数读取（我方 entry/configuration 处理已有）。

---

## 6. 可移植性分级（问题 6）

### A. 直接抄数值（进 constants.py / plans.py 旋钮即可，K 系杠杆直接拧）

| 项 | 值 | 落点 |
|---|---|---|
| d0 现金花度 | 花到 **≤$600**（v48 ~$190 / Wei Han $545），OPENING_RESERVE 800→≤600 | src/strategy.py 开局包 / phase_branch_plan §3"日终现金 ≥500"已对齐，**收紧执行** |
| d0 crew | v48=2 / Wei Han=7：**d0 crew 按畜群规模定（≥4 头→5-7 雇）**，不是固定 5 | `_crew_target` d0 项 |
| 瓜开局量 | **7 株（$560）**，d10 一次性 42-48 单 | phase_branch_plan §3 "西瓜 8-12 格"已在带内 |
| 羊/牛波次 | 羊首产 d6×6 单；牛首产 d8×6 单——**按首产日倒排购买日**：要 d6 毛就在 d0 买羊、要 d10-12 奶就 d4-6 买牛 | plans.py 畜群日程 |
| 买地日 | **d6 一块 + d10-11 一块**，第 4 块永不买 | `_macro_plan` 土地日程（我方现状 NE d4/SW d7 偏早但量级同） |
| crew 阶梯 | d5=6, d8=8, d10=12, d11=13（日租、每天重雇） | HANDS_RAMP 校准 |
| 肥料日结 | COLLECT 从 d1 起全员化，**当日清仓不隔夜**（v48 d12 一次 39 份说明允许小囤但 ≤3 天） | mission 任务权重 + market 卖线 |
| 饲料姿态 | 外购从 d0 起、麦底仓仅 5-7 格开局周转 | `_wheat_cap` d0 档（现 16 格偏重，v1.5 已在改） |
| 终局 glut 权重 | 瓜 3.6/毛 3.2/莓 2.0/奶 2.0/蛋 1.5 | d29 清算排序直接可用 |

### B. 需要结构改动（但接口现成）

1. **SELL 槽位影响分排序**：economy.py 已有 `price()` 同构镜像 → 在 `src/market.py` 下单前对同回合 SELL 按 `q×(p(i)−p(i+q))` 排序；~50 行。
2. **717-718 终局两步机**：在 scheduler v1.4 d29 逻辑前加 d28 EOD 判定 + 717 步"近棚/有货/熟田"单位覆写 + 718 步 `terminal_market(collision)` 全量替换；需要 executor 暴露步级覆写点。
3. **首店→预案分支**：`_decide_mode` 增加最高优先键 `shops[0]/[1]`（YARN_STORE→羊重线；FARMERS_MARKET→田线；BAKERY+对手签名→资本线），复用现有 B1/B2/B3 框架，把 phase_branch_plan §"阶段×分支"的 P1 分类器加一维。
4. **克隆锁存+抢卖**：opp_supply_observer（设计在册）落地后，加 `clone_distance`（公开签名 11 计数版，~20 行）+ 24 步 streak + 卖单前移账本；中等工作量，先做检测做观测指标、抢卖后做。
5. **波次基准测试**：把 v48 default 路由 d0-d12 的逐日逐单表（本文 §2.1/§3 表）做成**回归 fixture**——我方 sim 里 d6 应有 ~24 毛、d10 应有 ~42-48 瓜、crew/d10≥12；m5k 阈值点火改为**日历+波次兑现触发**（如"d10 瓜款到账即启动 SW 地+crew 12"，而非现金 ≥5000 才动）。

### C. 与我方冲突（不抄）

- **719 步开环剧本回放**：与我方闭环 mission/solver 架构对立；v48 的鲁棒性缺口（weed repair 只能救 8 步内小偏移）正是我方架构的强项。**只抄"剧本当测试基准"，不抄"剧本当执行体"**。
- **market_maker 做市套利**：v48 自己都没开（wheat_market_maker=False，v48build/main.py:L1202 无此键）；与资金门/饲料储备语义冲突，收益薄。
- **无价格门的清仓流**：需保留我方 WOOL_CUT_LOSS/CROP_FLOOR 红线，否则坏年景会复现我方 500-550 段的死价螺旋。
- ** weed replay wrapper**：闭环架构下无意义。

---

## 7. 佐证小件解读（问题 7）

- **h2h_v48.json**（2026-08-31）：v48 vs 我方当时两个候选（`agent/main.py` sha 39862dd… 与 `v72_main.py` sha f0bcd65…），seeds 101-104/201-204 × 双座，**各 16 局 0-16 全负**，平均净负 -68.4k / -71.0k，最惨 -91.1k（seed 202）；dev/reg 两域无差别。**这是"543 分段（当时）与 top-10 的真实差距测度"**：不是偶发，是开局结构性落后。
- **v48_pool.txt**：v48 对我方本地陪练池 11 个 bot（cow_baron/melon_hoarder/expansionist/baseline_wheat/crop_rotator/template_wheat/self_feed_ranch/near_band_diversified/scale_ranch/wheat_straw_monster/two_quad_denser）**44W-0L**，v48 场均奖励 98k-191k——注意我方陪练池整体强度低于 v48 一个档次，本地池胜率对线上 top 段**无预测力**（与 phase_branch_plan"本地同族池不再作门禁"裁决互证）。
- **milk_replication.json**：对 "rayk rank-your-agent §3：16 头牛奶均价 266 全季稀缺" 断言的复现实验（40 局/场景）：16 牛无 CARE → 奶价 291.4、收入 50.5k；**16 牛全 CARE → 奶价 230.8、收入 92.5k（+83%）**；8 牛全 CARE → 55.9k；16 牛+4 羊 → 毛价 225.8。结论：① **CARE 是奶收入的第一杠杆**（覆盖 vs 不覆盖差 4.2 万）；② 奶全季高于基准价 160（稀缺），牛是优质资产——v48/Wei Han 重牛与 d5-6 起 crew 6-12 的 CARE 覆盖正是这条证据的执行。
- **v92/v101/v10_episodes.json**：我方 v9.2（23 局）、v10.1（19 局）、v10（11 局）2026-08-30/31 的 `kaggle competitions episodes` CLI 抓取清单（含 1 VALIDATION 验证局），当时的线上采样台账。
- **loss_weihan.json**（21MB 完整回放，episode 103783585，seed 170790858）：Wei Han 80259 vs renyxin 8381——我方被 ~80k 选手碾压的实局。本 digest §2.2 即从该回放提取的 Wei Han 逐日轨迹（d0 3 牛+7 雇+$545 过夜、d8 奶×18、d11 双地+鹅）。**该文件是"对方开局解法"的一手证据，建议进 tetsuya-probe 式的解剖流程**。
- **v48 manifest**（v48_main.py 尾部）：`old_first20_both_seats 40/40`、`current_top10_holdout 39/46`、`current_top30_holdout 97/140`、`v43_public58_both_seats 103/116`、`one_child_call_per_turn: true`、**`future_opponent_actions: false`**（作者自证无未来动作，合规）。

## 8. notebook 语境交叉验证

`40-40-early-floor-39-46-top-10-v48-fast-routes.ipynb`（120KB）即本构建器的发布 notebook；标题数字=manifest 的 40/40 与 39/46。配合已登记的 `references/digests/meta-notebook-mining-20260920.md`（其 §"开火标准逐步表"与本文 §2/§3 独立互证：slot0 买麦+4 羊 1 牛 d0+地 d5/d8+12 手 d13+瓜 dump d10+milk d11 为另一采样口径，本文为源码级精确值）。

## 9. 风险与保留

1. 路由是**种子集验证**（官方 720 步确定性 + seed 抽商铺），线上遇未见商铺序列时 v48 只能走 default——我方分支 richness 在该域占优。
2. v48 的 39/46 是对 8 月末 top-10 的 holdout，9 月 meta（K320 商店世代、8c6s→9c4s-1w 配方，见 meta-notebook digest §配方时间线）已再漂移；**抄结构不抄数值时以 §6A 为带、以本文日历机制为骨**。
3. `submit/main.py` 系我方旧谱系一件，本文仅用于"当时为何 0-16"的归因，不作为对手情报源；其 R3-1~R3-4 注释与我方 docs 一致。

## 10. 时效性标注（问题 8）

- 代码抓取 2026-08-31，引擎 1.32.7（与当前一致，未见 1.33 公告）；公开代码共享锁 **09-23**（web-comp-intel digest）。
- 已知漂移点：① 雇佣/现金曲线画像来自 2600+ 局 8 月样本；② 商铺世代 meta（首店分布与需求结构）9 月讨论区有新帖；③ 若官方在终交前改 `townCenterSellInterval`（rebalance 制），v48 的 legacy 路径数值失效——我方移植时全部走 regime 感知包装。
- 结论有效期建议：**结构结论（波次点火/日历触发/卖单排序/终局两步机）按 ≥2 周有效对待；具体数值（crew 阶梯、瓜株数）按 1 周复核对待**。
