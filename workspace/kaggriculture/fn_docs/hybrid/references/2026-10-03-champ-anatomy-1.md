# 2026-10-03 冠军件解剖 1 —— syx/taeyan 字节级源码解剖 × v48 对照（"从零复刻失败根因"证据底稿）

> 任务=复刻失败根因分析的字节级证据采集。对象=池测判决（`2026-10-02-opensrc-pooltest.md`）中两件 BEATS_CEILING 开源件：**syx**（sunyuxiang136/kaggriculture-silver-agent `main.py`，vs 王座 h2h **0.9167**）与 **taeyan**（TaeyanG4/kaggriculture-strategy-meta `agent/c1200_final.py`，vs 王座 h2h **0.8333**）。对照基座=v48_derivative/main.py。归档均在 `fn_work/legacy_software/kaggle_simulations/orderbook_postseason_lab/pieces/`（provenance.md 齐，抓取 2026-10-02）。
> **方法**：静态分析为主（wc/awk/grep + Python AST + 压缩 blob 离线解包核对；未执行任何 agent 代码、未跑局）。大文件禁整读——抽样+定向检索；本文一切断言带 文件:行号/常量值。**不改 INDEX/JOURNAL/registry；不 commit**（登记行见 §九）。
> 引用纪律：本文一切结论来自本次实读的归档源码（clone HEAD 见各 provenance.md）；池测数字引自 `2026-10-02-opensrc-pooltest.md`（本仓实测）。

---

## 〇、一句话总判（先给结论）

**两件冠军件都不是"策略代码"，是"数据+引擎复刻+防御层"的工程系统**：syx 5.8MB 中 5.79MB 是三块压缩数据（磁带/检索表/预测语料），真实代码是 406 行调度器 + 约 1.6 万行版本化函数 + 9,549 行晚期模块；taeyan 21.5MB 中 21.35MB 是 **27 个完整第三方 agent 的压缩源** + 782KB 五层嵌套基座，梯子代码仅 4,593 行。两件的开局都跑在同一条 **R108 硬编码磁带**（41 条路线 × 719 步 + 64 种商店组合路由表）上——**与我们"固定带+查表 > 自研闭环"的复盘结论字节级吻合**。从零复刻失败不是因为缺少策略想法（一句话能说清的部分两件合计 <8%），而是缺：引擎语义复刻、检索语料、对手假设集合、验证基建这四样"承重墙"。

---

## 一、七维覆盖判定表

| 维度 | syx（0.9167） | taeyan（0.8333） | v48 对照（我方基座） |
|---|---|---|---|
| 1 体量与分层 | ✅ 外层 406 行（含 175 行许可证）+3 blob；解包后 hy_opening 15,975 行/627 函数/62 个 `def agent` 叠写、hy_planner 3,732 行+2.28MB k-NN 检索表、hy_eplanner 3,094 行同构、pd_modules 9,549 行×2 份 | ✅ 4,593 行梯子 + 27 个内嵌完整 agent（21.35MB）+ 5 层嵌套 lzma 基座（5,761 行 Chassis 磁带机）；**"生成器产物=少量逻辑+海量数据"判定成立** | ⚠️ 外层 1,221 行（约 1,160 行是 blob）+ 12 内嵌模块 3,443 行/126 def；总量 ≈ syx 真实代码的 1/4、taeyan 工程面的 1/20 |
| 2 引擎语义耦合 | ✅ **≥16 个耦合点**（§2.2，含 farmer-先-hands 顺序、双席同 index 逐单 lockstep、价格=库存函数精确参数、$1 地板不加库存、step%4 商店拍、hour23 日末 drop 溢出丢弃、718 最后行动步、原子 PLANT 规则、衰减每 2 步……） | ✅ **直接内嵌引擎原函数**（`_process_market`/`_apply_unit_action`/`_decay_plants`/`_daily_refresh_plants`，SHA256 钉版本 1.32.7）并逐候选调用评估 | ⚠️ 价格函数+$1 地板细节已复刻但**单边**（v23.simulator `execute_sell`，无双席同拍撮合评估） |
| 3 校准常量面 | ✅ hy_opening 62.4 个/百行、pd_market 59.0、fp_sched 41.5、pd_exec 30.6；pd_market CFG **约 60 键**且每键注释挂实验号（CS B2/B6、P8 M1-M3、R1b/R2b、R7） | ✅ 梯子 50.7 个/百行；层头自述触发窗（c405: 144≤t<647；c396: t≥216；c1017: t%24==23） | ⚠️ 有（路由门 88/120/153/216、clone_streak 24、distance 2.0 等）但**数量级更小、无实验号溯源** |
| 4 防御与卫生 | ✅ Chassis 9 层反应式守卫 + 入口三级回退 + 每层 try/except 恢复市场表 + 遥测计数器（td_* 系列） | ✅ 60 层梯子中约 2/3 是防御/修复层；c413/c414/c419 显式**层间调用契约**；每层 REPORT 遥测 | ⚠️ 有 weed_repair/原子 PLANT 规避意识弱；入口级 PASS 回退有，层间契约无 |
| 5 终局段 | ✅ **三段式**：step 648 换 route2 末日磁带 → end_step 700 起逐步抛 → 712-718 E182 物理收尾规划器 + 718 全清 + 死库存清点 | ✅ 多层接力：c379(700-718 紧凑化)/c383(终局全货缴存)/c447(终局恢复 v4)/c947(货舱后缀)/c1064(终局断料裁剪=最终层) | ⚠️ v19_terminal 仅 717/718 两步变现 + collision 规则 |
| 6 开局磁带形态 | ✅ **纯硬编码**：41 路线×719 步全动作带 + 64 商店对路由表 + 对手指纹狙击表 `{(229.0,9989):128}`；step0 即"买 43 卖 30"价格操纵 | ✅ 同一 R108 磁带表（基座 L946-947 与 syx 同名同构）；梯子对磁带做观测特定补丁（monkey-patch `_route_action`） | ✅ 同为磁带制（_V48_ROUTES + fast_route_router 门控）——形态上我方不输，**输在磁带之后的东西** |
| 7 可述 vs 承重 | ✅ 可述策略 ≈5-8%（17 牲畜/%4==1 抛售/718 清仓/禁西瓜/草莓窗口）；**>92% 是承重工程** | ✅ 可述策略（"对对手假设集合做鲁棒最优响应"+60 条已观测修复）≈3-5%；**>95% 是承重**（含 27 件 ensemble 与验证面） | ⚠️ 可述占比最高（粗估 25-35%）——**工程承重薄正是差距本体** |

---

## 二、syx 解剖（七维详证）

### 2.0 装载形态与外层调度器（main.py，406 行/5,814,850B）

- L1-3 头部署名：基于 haideptry 公开 notebook "The 2965 Master Hybrid Engine"（Apache-2.0），V39/V46 谱系（Thomas Tschinkel 等 9 人链）。**syx 本身就是公开谱系的再衍生**。
- L207-215：`_HPD=24, _LD=21, _ED=9 → _ET=216（day 9）, _LT=504（day 21）`；`_K=(90,165,60)`（三 blob 的 XOR 钥）。
- L220-222：三个数据块——`_OPEN_B` 891,009B、`_LATE_B` 2,457,763B、`_EARLY_B` 2,448,361B（b85 + 逐字节 XOR + zlib；`_load()` L218-223 解出后 `exec`，取命名空间**最后一个 callable**——贴合官方 last-callable 语义，文件尾 L405 `agent = globals().pop('agent')` 再保险）。
- 调度器 `class _S`（L240-401）三分段：
  - **对手侦察**：L322-326 `act()` 在 step 2 记 `m2=rival money`、step 47 记 `mel1=rival MELON 数`；L337-342 `if st==215 and m2<1000 and mel1!=12 → mode='early'`（对手既没钱又不是标准 12 瓜流 → 提前 9 天切换早熟规划器 hy_eplanner）。
  - **换挡与重放**：前 21 天每步把 `(obs, market_orders)` JSON 序列进 `self.buf`（`_remember` L287）；day 21 `  _catch()`（L302-316）调用晚期规划器 globals 里的 `_pd_fp_make(seat)` / `_pd_fp_replay(ctx, buf)` 把 504 步历史**灌进其预测上下文 `_FP_CTX`**——晚期规划器不是无状态的，它需要整局重放才能重建预测状态。这是复刻时极易漏掉的架构点。
  - **死亡探测**：L281-286 `_dead()` 读开局件遥测 `_ASH_REPORT['ash_dead']`；开局 bot 若已死则 day21 后继续用磁带不用规划器。
- `_has_replay`（L225-228）以 `globals['_PD_FP_SCHED']`/`['_pd_fp_make']` 探测规划器是否支持重放——**两模块间协议**。

### 2.1 维一：体量与分层

| 层 | 文件/位置 | 行数 | 说明 |
|---|---|---|---|
| 开局磁带+守卫 | hy_opening.py | 15,975 | 627 函数/8 类/**62 个 `def agent` 叠写**（最后定义生效，前代作为 parent 被闭包引用）；含 94KB R108 磁带 + 553KB V92 预测语料 + 12KB 引擎提取 + 22.9KB E182 末段 |
| 晚期规划器壳 | hy_planner.py | 3,732 | 内含 2.28MB `_CLONE_TABLE`（265 局训练局 k-NN 检索表）+ 250KB `_PD_BLOB`（pd_modules 源+数据） |
| 早熟规划器壳 | hy_eplanner.py | 3,094 | 同构（_CLONE_TABLE 同数据不同 XOR=46） |
| 晚期模块 | pd_modules_late/（early 同份拷贝） | 9,549 | pd_exec 2,340 / pd_plan 1,029 / pd_supply 940 / pd_replant 857 / fp_rival 878 / fp_sched 751 / pd_market 735 / fp_ownfc 561 / fp_fsim 549 / pd_tasks 448 / pd_state 291 / fp_sched_hook 168 |
| 数据模块 | fp_rival_params.py 164KB、ownfc_lags.py 164KB | 2 行代码/328KB | 对手贝叶斯分类器参数 + 自产滞后系数表 |

**pd_modules_late 9,549 行职责占比**（按文件拆）：执行卫生（pd_exec+pd_supply）**34%**；计划层（pd_plan+pd_replant+pd_tasks+fp_ownfc+fp_sched+fp_sched_hook）**40%**；市场订单层（pd_market+fp_fsim）**13%**；对手侦察（fp_rival+参数）**9%**；状态/工具（pd_state）**3%**。终局逻辑分散在 pd_market（end_step/FINAL_STEP）、fp_sched（718 边界）与 hy_opening 的 E182 内嵌模块中。

**重大发现（维一追加）**：hy_planner 的 `_CLONE_TABLE` 解包后为 `{acts_s: 13,292 去重动作串, rows_t: 216 个步索引行, games: 265 局}`；消费类 `_q53`（hy_planner L88-107）docstring 自述："per unit, the training (game, step, unit) of the same step with the same position, carried items and tile under it (backing off to the same position), ranked by … then the money distance, then the game followed last step. Market orders: the best whole-state neighbour on MKT_KEYS"——**晚期"规划器"的底层是一台 265 局语料的同分步 k-NN 检索机**（状态哈希 pos/tf/tn/tn/inv/sh 匹配+money 距离排序+粘性）。连"动态规划期"的主体都是检索，不是闭环搜索。

### 2.2 维二：引擎语义耦合点（复刻成败核心，逐点带证据）

1. **步内执行顺序**：pd_market.py docstring L11-15 "a step runs every unit command first, then the market (orders index by index, lockstep with the rival; at most maxMarketOrdersPerTurn per player), then the town consumption (every shop instance every 4 steps: step % 4 == 0), then plant decay, then (hour 23) the end-of-day refresh and the drop of every unit inventory into the shed, capped at shedCapacity (overflow DISCARDED)"。
2. **unit 循环顺序（farmer 先、hands 后）**：pd_market.py `shed_after_units` L173-206 "shed run through this turn's unit commands (**farmer first, then hands**)"——逐 unit 模拟 PICKUP/DROP/PLACE 重建"市场时刻的仓库"。
3. **双席同 index 逐单 lockstep**：fp_fsim.py `_lockstep` L444 "Both seats trade the same item at the same index: unit-by-unit lockstep (engine _process_market)"——同一 index 双方逐单位交替成交的精确复刻。
4. **价格=库存函数的精确参数**：pd_market.py L122 `MARKET_PARAMS` 九商品 `(base, T, 上升形状, 上升系数, 下降形状, 下降系数)`，如 MILK `(160,122,'sqrt',0.6,'linear',1.6)`；L123 `I0=10000` 平衡库存；L154-163 `market_price` 复刻引擎原函数（floor $1）。
5. **$1 地板不加库存**：fp_sched.py docstring "A unit at the $1 floor adds no inventory"（v48 的 v23.simulator 也有此条——我方已有）。
6. **BUY 按 quote(inv−1)**：pd_market docstring L17 "BUY_PRODUCT at quote(inv - 1)"；fp_fsim.buy_price L137 同。
7. **商店 4 步拍与售卖行**：pd_market L273-275 `is_sale_row: step % 4 in lot_rows(=(1,))`——拍后第一行（hours 1,5,9,13,17,21）为售卖行；CFG L124 `lot=6`（陡商品每行限额）。
8. **hour-23 日末与 day-29 无 drop**：pd_market L19-20 "the last acting step is 718 (hour 22 of day 29): the day-29 end-of-day drop never happens"；L602-643 hour-23 room guard（今晚 drop 后仓库+携带 ≤ end_target 96，超了按"便宜损失先卖"序清）；wheat_reserve L353-366 "At hour 23 the FEEDs still left are missed (the units acted before the market and no step of the day follows): they count 0"。
9. **FEED 先于市场吃小麦**：pd_market `carried_wheat_after` L382-387（每个 FEED 命令在市场前消耗 1 wheat）。
10. **原子 PLANT 规则**：pd_supply.py 头注 "the engine drops ALL PLANTs of a crop in a step whose PLANT count exceeds the seeds held (atomic PLANT rule); FEED needs a carried WHEAT, FERTILIZE a carried FERTILIZER"。
11. **植物衰减确定性**：hy_opening L727 exec 内嵌"kaggle-environments 1.32.7, SOURCE_SHA256 bc8a548…"的引擎提取件，含 `(step - mls) % 2` 每 2 步 yield−1、归零转 WEED——**用 SHA256 钉死的引擎语义复制品做确定性预测**。
12. **HIRE 斐波那契/BUY_LAND 顺序价**：pd_market L119 `LAND_PRICES=(1000,2000,4000)`（NE→SW→SE）、L133-137 `fib`、L208-224 `order_cost`。
13. **每回合 10 单窗口**：`window_orders` cap=10；L47-48 h22_window=10；h0_hires=8 / h0_min_sells=2（hour-0 窗口内 HIRE 与 SELL 的配额制）。
14. **同拍对手单可读**：pd_market L325-344 `rival_tile_stock` 从公开 tile 网格算对手可收库存（day−planted_day<first_yield 剔除）；V92 `_v92_p_update` 用 `inv−prev_inv+town_draw−own_sales` 反解对手本拍卖出量（含精确 town draw）。
15. **对手单 index 枢轴利用**：fp_sched docstring `rho_idx0=0.5 (a tie at the same index: unit alternation)`——同 index 平局时单位交替的语义被显式建进边际价值模型；V92 预测器把抢跑 SELL `market.insert(0,…)` 插到 index 0（hy_opening L3321）。
16. **last-callable 语义**：外层 `_load` 取 `filter(callable)[-1]`；两件文件尾都有 `agent = globals().pop('agent')` / taeyan 每层 `del agent` 再重定义。

### 2.3 维三：校准常量面

- 密度（数值字面量/百行，AST 统计）：hy_opening **62.4**、pd_market **59.0**、fp_sched **41.5**、pd_exec **30.6**。
- pd_market CFG（L124）约 **60 键**，例：`end_target=96`（每晚 drop 后目标库存）、`floor=300`（现金地板）、`buy_slack=2`（BUY_PRODUCT 报价+2 防滑）、`hinge_hold={'TOMATO':2.0,'CARROT':2.0}`（铰链商品持有=2×base 价）、`hinge_late_day=28.5`（终局铰链 spike 日）、`h22_share={TOMATO:0.91,EGG:0.87,CARROT:0.74,WHEAT:0.75}`（DSM 式 h22 清仓比例）、`wc_lot=7/wc_lot_cheap=3/wc_cheap=0.8/wc_med_len=72(=3 天)/wc_leg_from=18/wc_leg_cap=15`（小麦储备控制器全套）、`h0_straw_share=0.2`。
- **每个开关键的 docstring 都挂实验号**（L32 "CS task B2, 27 Sep 2026"、L50 "CS task B6"、L83 "P8 task market, 28 Sep 2026 … M1-M3 … R1b/R2b"、L36 "fix R7, 27 Sep"）——常量不是拍的，是 A/B 实验沉淀，且默认 off 保持回归等价。
- fp_sched 构造参数面：`lam=1.0, near=12, mid=48, far_hour=13, chunks=12, margin=4, margin_future=10, rho_future=1.0, rho_idx0=0.5, min_mv=0.0, max_cap_moves=80`。
- V92 预测器（hy_opening L3201-3207）：`_V92_P_H=48`（预测窗）、`_V92_P_K=4`（对手 ≥4 单才抢跑）、`_V92_P_TOP=1`（top-1 回放匹配）、`_V92_P_EVERY=3`（每 3 步重匹配）、活动窗 150≤step<700、匹配窗 240 步、±1 步容差。
- fp_rival_params.py（164KB 单行 JSON）："fp.rival 28 Sep 2026"——5 类对手（v2/v1/other/v46/gen）× 9 商品 × 24 小时 hazard 曲线 + `typefeat{m2lo, mel12}`（正是外层 step2 钱/step47 瓜探针）+ `typeprior{v46:0.35,…}` + `n_train{v46:913, other:361, v1:309, gen:251, v2:206}`——**206-913 局/类的拟合语料**，标注日期=截赛前 2 天。

### 2.4 维四：防御与卫生层清单

hy_opening `Chassis`（L152-634）反应式守卫链（`DEFAULT_SETTINGS` L38 全开；实际 `_SETTINGS` L669 仅留 hand_align/weed_repair/sell_lead，其余由后继版本层接管）：`_hand_align`(L248)、`_weed_repair`(L257)、`_apply_suppression`(L339)、`_sell_lead`(L367)、`_front_run`(L398)、`_block_requirements`(L427)、`_budget_guard`(L485)、`_room_guard`(L531)、`_clamp_sells`(L586)、`_dead_stock`(L608)、`_terminal_liquidation`(L628)。入口三级回退（make_agent L635-657）：层失败→裸磁带动作→PASS+hands 补齐。最终 agent（L15878-15974）再包一层市场卫生：`maxMarketOrdersPerTurn` 截断（td_trunc 计数）、洗单检测（td_cp_wash）、每层 try/except 失败即恢复前层市场表、ms 级耗时遥测（td_ms_sum/max）。pd_exec `_timeout` L1131（perf_counter vs t_end，LNS 全程让路）；pd_supply 保饲料（断粮即叛逃）；cap_purchases（pd_market L226）逐单现金/库容裁剪并返回 drop 原因（cash/room/all_land/malformed）。

### 2.5 维五：终局段

三段式：① step **648**（day 27）`_router` 强制换 route 2 末日磁带（hy_opening L691-693）；② pd_market `end_step=700`（day 29.2）起**每步都是售卖行**、day 29 陡商品按 `rows_left` 剩行数 pro-rata 均摊（L448-455）；③ `FINAL_STEP=718` 全清（L443-446）+ E182 "Shop0909 last-seven-turn physical closure planner"（hy_opening L729 exec 串，22.9KB）：`START, FINAL = (712, 718)`，末 7 拍物理收尾（把单位走到仓库缴存），FINAL 拍 `shop_liquidation`。另有 hinge_late_day=28.5 终局铰链 spike 持有策略（hinge_late_price L126-131：预估 town drain 后再入库的边际报价）。

### 2.6 维六：开局磁带形态

**纯硬编码查表制，非条件分支生成**：
- `_R108_DATA`（hy_opening L665，94KB）= `{actions: 3,982 个去重完整动作字典, routes: 41 条路线 × 719 步（引用 action id）, shops: 64 条（8×8 商店对）→路线}`。route0 实测 719 步中 414 步有市场单、共 969 单——高密度磁带。
- step 0 动作=`[BUY_PRODUCT WHEAT 13, BUY_PRODUCT WHEAT 30, SELL WHEAT 30]`——**买 43 抬价、卖 30 套现**的价格操纵开场；step 1=SELL 13 + BUY 5 + HIRE×5 + COW×2 + SHEEP×2。L694-697 `_R42_OPENING` 对全部 41 条带强制覆写第 0 步。
- 路由决策：step 2 指纹 `(rival money, WHEAT inv)` → step 144（day 6）按 `unlocked_shops[:2]` 查 64 行路由表（`_R108_SHOP_ROUTES`/`_R110_OLD_SHOPS`/`_V92_TABLE` 三代表决，L685-686）→ YARN_STORE 特例查 `_V93_ROUTE_BY_RIVAL={(229.0,9989):128}`（L672，**对单一已知对手的定向狙击**）→ step 648 强制 route 2。
- V92 市场预测层（L3208-3346）：553KB blob 按 `(shops[0], shops[1])` 索引候选"回放剧集"（delta 编码事件表），用近 240 步观测的对手卖出事件做 `m−0.5f−0.5miss` 匹配评分，top-1 剧集若预测对手 1-2 步内将卖 MILK/WOOL/STRAWBERRY ≥4 单，则把我们的同商品 SELL **插到市场单 index 0** 抢跑。
- **判定**：day0-21 完全磁带+查表+反应式守卫；"固定带+查表 > 自研闭环"复盘结论在此得到字节级验证——**且磁带本体是离线搜索产物（41 条 719 步），仓库不含其生成器**。

### 2.7 维七：可述 vs 承重（syx）

可述策略（一句话能讲清）：17 牲畜双牧场（pd_plan）、step%4==1 拍后首行抛售、陡商品 lot=6 限额、草莓 day12-17 窗口/禁西瓜、718 清仓、抢跑截胡。这些在 pd_plan/pd_market 中合计约 800-1,200 行 ≈ 真实逻辑的 **5-8%**。承重（缺了就崩）：引擎复刻（market_price/shed_after_units/_lockstep/衰减提取）、504 步重放上下文、265 局 k-NN 检索、LNS 执行器（morning kit + ruin&recreate + 超时预算）、对手分类器与 hazard 预测、9 层守卫+三级回退+遥测、60 键实验面——**>92%**。

---

## 三、taeyan 解剖（七维详证）

### 3.0 装载形态与结构判定（c1200_final.py，4,593 行/21,479,707B）

- L1 `# Generated by research/tools/build_localbest_operator_submission.py` + L6-8 `_decode = lzma.decompress(base64.b85decode(...))`——**生成器产物实锤**。
- L11：782KB blob → `local_best.py`，但其内部再嵌 `_decode` 串，**共 5 层 lzma 套娃**（766,948→729,520→692,330→665,604→642,381→**856,427B/5,761 行真源码**）。最内层 L946-947 `_ROUTES={int(k):[_R108_DATA['actions'][i] …]}`、L959 `def _router`、L404 `Chassis`(501 行)、L908 `make_agent`——**与 syx hy_opening 同名同构的 R108 磁带机**（同一条公开谱系的"Local Best"基座）。
- 11 张 `*_SOURCES` 表（L1095/1214/1225/1350/1686/1849/2017/2088/2328/3307/4129），union **27 个完整第三方 agent 源**（key 222..373，每个 0.65-1.03MB 压缩源码），合计 **≈21.35MB=文件 99.5%**。c397 层头自述来源："Adds Harvey Zhang V15 Market Stack, Dmitrii Gluzdov Herd-Safe Sale Window, and statma's ca20 variant"。
- 梯子：**60 个 `# cNNN` 层头**（c358→c1064），每层 `del agent` 后重定义；最终 agent=c1064（终局断料裁剪）包装；HANDOFF.md 确认 "c1200 … byte-identical qualified c1064"。
- **"代码 vs 数据"判定：梯子逻辑 4,593 行（含基座 5,761 行共约 1.04 万行） vs 内嵌他件源 21.35MB——是"少量逻辑+海量数据（对手假设集合）"的极端形态**。

### 3.1 维二：引擎语义耦合点（taeyan 特色=直接调用引擎原函数）

1. **内嵌引擎本体**：`_C396_ENGINE['_process_market']`（L1118，`_c396_market` 内逐候选调用）、`['_apply_unit_action']`（L1112、c1017 L4140 区）、`['_decay_plants']`、`['_daily_refresh_plants']`、`['_new_private']`（L1183）、`['SHOPS']`/`['CROPS']`——把提取的引擎函数当库用，**不做近似**。
2. **标准局门**：L1174 `all(cfg.get(k,v)==v for … episodeSteps=720, turnsPerDay=24, boardSize=10, shedCapacity=100, maxMarketOrdersPerTurn=10)`——配置不符即全部旁路（防非常规调用方）。
3. **对手克隆集合**：step 0 把 27 件源 `exec` 各取最后 callable（L1180-1183）；每步构造**假对手视角** `fake=deepcopy(obs); fake['player']=1-own; fake['private']=…`（L1190）跑每件策略得预测动作；`_C396_TRACK['matches']` 逐局核验预测 vs 实际观测，不符即从集合剔除（L1187-1188）。
4. **鲁棒最优响应**：`_c396_response`（L1123-1166）对自有市场单的**槽位排列组合**（≤64 个候选，L1143-1151）逐个在**每个存活对手模型**上过 `_process_market`，约束"完成的购买/种子/货舱/雇工/田面完全不变、现金不降"（L1158），目标 `quality=(min(deltas), sum(deltas))`——对存活假设集合的**极小极大边际**改进。
5. **F11 束搜索（c461）**：邻居算子含"整批拆分 (q//2, 1, q−1)"、槽位交换、以及**围绕对手单枢轴 index 的库存中性往返**（`left/right ≤/≥ pivot`，量取 {rival_qty,64,32,16,8,1}）——纯同拍 lockstep 语义利用；束宽 2/深 2/≤192 候选（"Bounded operation count rather than machine-speed-dependent behavior"——**确定性算量，防机器相关违规**）。
6. **层间调用契约**：c413 "commit funding BEFORE c396 public-state projections and settlement"、c419 "preserve the two-leg slot contract … c396 can move a single SELL across BUY_SEED; c418's assumption was too weak"、c405 "Do not move any inherited order across a rival's simultaneous slot. The new sale must follow the buy; empty earlier slots stay empty"（L1284-1286）——**修复层的修复**，语义耦合的二级衍生物。
7. **c1017 精确死亡模拟**：hour 23 对 FERTILIZE→WATER 替换决策，用引擎函数在虚拟 tile 上跑两种时间线比 yield_units/died_step（L4129 区 `_c1017_yield`），只在"不浇水必死且 0 产、浇水后活且 >0 产"才换。
8. **719 步磁带越界保护**：`min(718, …)` 多处；c4346 区 "The terminal route has 719 actions, indexed 0..718"。

### 3.2 其余维度速览

- **维三 常量**：梯子密度 50.7/百行；典型触发窗 c405 `144 ≤ t < 647 且 t%24≠23`（L1260）、c396 `t≥216`、c1017 `t%24==23`；c418 用 `_C396_ENGINE['SHOPS'][s]` 数 WHEAT draw（L1718）。
- **维四 防御**：60 层中约 2/3 为观测修复/防御层（c410 pickup/溢出修复、c412 晚间订单先融资、c414 响应否决、c465/c461 守卫式 F11、c580 无效服务命令移除、c612 空tile WATER/HARVEST 清除、c833 原子种子需求防取消）；每层 REPORT 遥测键 + ChainMap 汇入最终 `agent.telemetry`。
- **维五 终局**：接力链 c379（700≤step≤718 终局紧凑化，L897）/c383（o302 终局全货缴存）/c447（xox787 Terminal Recovery v4 移植）/c947（货舱后缀预装）/c1064（终局断料裁剪——**最终层就是终局层**，HANDOFF 自证 c1064 单层 ≈ +120 margin，为全链最大单项）。
- **维六 开局**：基座 R108 磁带同 syx；梯子对磁带打观测特定补丁：c405 以债务账本 monkey-patch `_C365_CA_NS['Chassis']._route_action`（L1235-1247，身份失配即 `RuntimeError`）；c544/c579 "Narrow observed FARMERS/FARMERS whole-calendar route"、"observed BAKERY then SMOOTHIE" 的 route110——**磁带之上的条件改写层**。
- **维七 可述 vs 承重**：可述="以 27 件公开件为对手假设集合，逐拍剔除不符假设，对存活集合做极小极大槽位搜索"+60 条修复；≈3-5%。承重=27 件内嵌源、引擎提取、5 层解包装载、层间契约、**验证基建**（HANDOFF/AGENTS.md：每次采纳 108 valid 局/38,826 步全对账、chain ladder 256 局、自建 league 449GB 工件/124.5GB 回放、提交号追踪 56719658/56722176）——>95%。

---

## 四、v48_derivative 对照（七维快过）

形态：外层 1,221 行（L37-1196 为 `_V48_MODULES` 压缩 JSON，12 模块 3,443 行/126 def：v24.market_maker 853、v44.gold_floor 756、v19_terminal 341、v23 四件 681、v22 两件 288、v48.fast_route_router 174、v21 9）。同磁带制（_V48_ROUTES）。

| 维 | v48 现状 | 与冠军件差距点 |
|---|---|---|
| 1 体量 | 真实逻辑 ≈3,500 行 | ≈syx 的 1/4；无检索语料/无对手假设集合/无预测器 |
| 2 耦合 | v23.simulator `execute_sell` 注释"Exact unit-lockstep revenue for one unilateral SELL order"+$1 地板不加库存（有！） | **单边**：无双席同 index 撮合评估、无引擎函数内嵌、无 farmer-first/hands 顺序重建、无 hour23 drop 溢出丢弃的 room guard、无 town drain 反解对手卖出 |
| 3 常量 | 路由门 yarn_first 88/farm_first 120/yarn_second 153/yarn_third 216；GoldFloorConfig clone_streak_required 24/clone_distance_threshold 2.0/clone_detection_start 48/clone_active_start 160/clone_veto_step 120/bakery_capital_* 等（约 30 键） | 键数约为 syx pd_market 的 1/2，且**无实验号溯源、无默认 off 的 A/B 面** |
| 4 防御 | v22_weed_repair 123 行；入口 PASS 回退（L1206-1215） | 无层间契约、无遥测面、无逐层市场表恢复 |
| 5 终局 | v19_terminal：step∈(717,718) 只覆盖"还能走到仓库的单位"（monetizable_terminal_units）+ terminal_market(rule='collision') | 无 648/700/712 分段、无 pro-rata 剩行摊销、无终局断料/货舱后缀链 |
| 6 开局 | 磁带+路由门+clone 抢跑（gold_floor 67 处 clone 引用） | 形态对齐；缺 V92 式剧集匹配与 64 商店对路由的覆盖密度（fast_route_router 仅 4 门+2 前缀组） |
| 7 可述/承重 | 可述占比粗估 25-35%（策略想法密度不低） | **承重墙缺失即差距本体**：引擎复刻、语料检索、假设集合、验证基建四件全缺或薄 |

---

## 五、关键读数汇总

| 读数 | syx | taeyan | v48 |
|---|---|---|---|
| 文件体量 | 5.81MB/406 行 | 21.48MB/4,593 行 | 107KB/1,221 行 |
| 数据占比 | 99.5%（三 blob 5.79MB） | 99.5%（27 件源 21.35MB+基座 782KB） | ~96%（blob） |
| 真实代码行（解包后单份） | ≈29,300（hy_opening 15,975+planner 3,732+eplanner 3,094+pd 9,549 取单份+外层 80，去重口径≈25,000-29,000） | ≈10,400（梯子 4,593+基座 5,761） | ≈4,700（外层 60+模块 3,443+配置） |
| 引擎耦合点（本次实计） | ≥16 | ≥8（含引擎原函数直调） | ~5（价格函数/地板/终局步/磁带/路由门） |
| 常量密度（/百行） | 30.6-62.4（四个文件实测） | 50.7（梯子） | 未逐一测（体量小，估 20-40） |
| 可述:承重 | ≈1:12 | ≈1:20 | ≈1:3 |
| 磁带 | 41 路线×719 步+64 商店表 | 同款（基座内） | 有（_V48_ROUTES） |
| 对手建模 | 贝叶斯 5 类分类器（913 局最大类）+V92 剧集匹配+单点狙击表 | 27 件克隆 ensemble+逐拍剔除 | clone 距离检测（gold_floor） |
| 同拍撮合利用 | _lockstep 双席复刻+rho=0.5 交替+index0 抢跑 | _process_market 原函数逐候选评估+对手枢轴往返 | 无（单边 execute_sell） |
| 验证基建 | 仓外（README 自报 <3ms/step） | 仓内：108 局/38,826 步对账+256 局 ladder+league | 无（对照面） |

---

## 六、异常与限界（本文结论的边界）

1. **静态分析为主**：未实际执行任何 agent；行为推断全部来自源码与解包数据。"62 个 agent 叠写中各版本 live/dead 划分"未做插桩追踪（AST 从最终 def 直引仅 20 函数可达，但链路经模块级 parent 赋值与 `_IMPL` 全局延伸，精确 live 集需运行时插桩）；行数占比按文件边界估算，误差 ±5%。
2. **blob 解包核对范围**：R108（全解：3,982/41/64 实数）、_CLONE_TABLE（顶结构与键数）、V92（结构+常量，未全量展开 64 对语料）、fp_rival_params（全键）、taeyan 基座（5 层全解到 5,761 行源）、27 件 ensemble 源**未逐件解包审计**（仅统计尺寸与层头来源说明）——若某件源与层头声明不符，不在本次覆盖内。
3. **池测数字**（0.9167/0.8333）引自 2026-10-02 池测报告（本仓实测），本文未重跑。
4. taeyan 层号与功能映射来自层头注释+代码抽样；c596 层头自述 "owner decision, not self-adopted"（demand-gated 移植是**所有者决策**），提示梯子含"所有者拍板"成分，不可全归因自动化。
5. taeyan 提交 56722176（10-01）晚于比赛截止（09-30 23:59 UTC），池测报告已标注"存疑"；其 h2h 0.8333 为池测实测，与是否计入正式榜无关。
6. v48 常量密度未做 AST 实测（体量小、时间预算留给两件冠军件），标"估"。

## 七、对"从零复刻为何失败"的代码证据建议（结论条目化）

1. **复刻对象本体判定错误**：两件冠军件的"策略"含量 <8%（可述:承重 ≈1:12 与 1:20）。从零复刻默认在写"策略代码"，而冠军件 92-95% 的行数在写承重墙——引擎复刻、语料、防御、验证。**失败第一根因：把工程系统当策略来复刻**。
2. **引擎语义是乘法门，不是加分项**：syx 16+ 个耦合点里，"farmer 先 hands 后"、"同 index 双席逐单交替"、"hour23 drop 溢出丢弃"、"day29 无 drop"、"BUY 按 quote(inv−1)"、"原子 PLANT"——任何一条错，磁带行为整体漂移且难归因。taeyan 干脆内嵌引擎原函数（SHA256 钉版本）。**建议**：复刻路线必须以"引擎语义对账表+差分测试"为第一交付物（我方 v48 已有价格函数与 $1 地板，但单边、无撮合、无日末/衰减/原子规则——缺口清单见 §四）。
3. **磁带不可再生**：41×719 步磁带与 265 局检索表、27 件对手源都是**离线语料资产**，仓库不含生成器。复刻=先建语料产线（自博弈/回放采集/离线搜索），不是先写在线逻辑。这直接支持我方"固定带+查表>自研闭环"结论——**冠军件连 day21-29 的"规划"主体都是 265 局 k-NN 检索**。
4. **对手建模是第二引擎**：syx 分类器（913 局语料拟合）+剧集匹配+定向狙击表；taeyan 27 件 ensemble 逐拍剔除+极小极大响应。v48 的 clone 检测只是其 1/10 的形态。**建议**：把我方已有对手指纹（gold_floor）升级为"假设集合+剔除+鲁棒响应"三件套。
5. **层间契约与遥测是迭代速度的来源**：taeyan 60 层能叠起来靠"每层 REPORT 键+调用顺序契约（c413/c414/c419）+108 局对账门"；syx 靠"CFG 60 键全默认 off+实验号注释+td_* 遥测"。没有这层，任何修复都会回归破坏前修复——**从零复刻在无验证基建下迭代，等于每次改动都在盲改**。
6. **终局是分段函数**：648/700/712/718 四段接力（换带→每步抛→物理收尾→全清+断料）。v48 只有 717/718。终局每一分都是纯现金差，是性价比最高的补课点。
7. **量化对照**（供根因报告引用）：真实代码 syx≈2.5-2.9 万行 / taeyan≈1.04 万行+21MB 语料 / v48≈4.7 千行；引擎耦合点 16+/8+/~5；同拍撮合利用 双席/原函数/无。**差距不在策略密度（v48 可述占比反而最高），在承重墙厚度**。

## 八、与既有复盘结论的互证/修正

- ✅ 互证："固定带+查表 > 自研闭环"——两件开局全在 R108 硬编码磁带上，且 syx 晚期主体亦为检索制。
- ✅ 互证："引擎语义提取"路线（2026-09-28-engine-pricing-extraction.md）——两件均以不同形式内嵌引擎语义；建议升格为"引擎函数级内嵌+差分对账"。
- ⚠️ 修正：若既有复盘把 syx 优势归因于"17 牲畜/拍点抛售"等策略要点，本解剖显示这些是表层（<8%）；真正护城河是 V92 剧集抢跑+fp_sched 边际价值调度（lam=1.0 把对手收入当负目标）+重放上下文。
- ⚠️ 新增：taeyan 证明"开源件集合本身可以成为组件"（27 件 ensemble）——对手假设集合可以是采购来的，不必自造。

## 九、需登记行清单（主会话统一登记；本任务未改 INDEX/JOURNAL/registry/requirements）

- `references/2026-10-03-champ-anatomy-1.md`：两件冠军件（syx 0.9167/taeyan 0.8333）七维字节级解剖 + v48 对照 + 复刻失败根因证据（R108 磁带实数 41×719/64 表、_CLONE_TABLE 265 局 k-NN、27 件 ensemble、引擎耦合点 16+/8+、可述:承重 1:12 与 1:20）。
- 关联：`2026-10-02-opensrc-pooltest.md`（件源与 h2h 数字出处）、`2026-09-28-engine-pricing-extraction.md`（引擎提取路线，本报告 §七.2 升格建议）。
- 后续建议（若主会话采纳）：① v48 引擎语义缺口清单入改进面（§四表）；② "语料产线"（磁带/检索表/对手源）立项前可行性；③ 本报告 §七 可直接作为复刻失败根因分析报告的证据章。
