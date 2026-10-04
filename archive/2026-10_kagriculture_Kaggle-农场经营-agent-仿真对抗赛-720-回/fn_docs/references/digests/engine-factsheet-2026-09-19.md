# 引擎事实表（kaggriculture 场景，kaggle-environments 1.32.7+nodeps）

- 日期：2026-09-19。目的：评估"提交 bot 内嵌轻量世界模型 + 前瞻规划/MPC/自博弈"路线的可行性。
- 来源：vendored wheel `software/vendor/kaggle_environments-1.32.7+nodeps-py3-none-any.whl`（与已安装 site-packages 副本 sha256 逐文件核对一致，核对日期 2026-09-19；`agent.py`/`core.py`/`utils.py`/`schemas.json` 均比对通过）。
- 引用约定：`kaggriculture.py:NN` = wheel 内 `kaggle_environments/envs/kaggriculture/kaggriculture.py` 行号；`json:NN` = 同目录 `kaggriculture.json`；`core.py`/`agent.py`/`utils.py`/`schemas.json` = wheel 内 `kaggle_environments/` 下同名文件。实测条目标注【实测】，脚本为本次 2026-09-19 本机（Win10，Python 3.14）只读快速验证。
- 场景代码体积：`kaggriculture.py` 1086 行 / 40,356 B + `kaggriculture.json` 138 行 / 6,002 B（wheel 内实测）；整个引擎为纯 Python（场景无编译依赖；wheel 内 cabt 场景的 `cg.dll` 缺失仅产生无关警告，不影响 kaggriculture）。

---

## 1. 运行时预算（决定 bot 内每回合可做多少计算）

| 项 | 值 | 来源 |
|---|---|---|
| episodeSteps | 720（=24 turns/天 × 30 天；turnsPerDay 默认 24 见 `json:28-33`） | `json:8`；实测开局 day/hour 推进 `kaggriculture.py:948-950` |
| actTimeout | **1 秒/回合**（框架默认 6，被场景覆盖） | `json:9`；框架默认 `schemas.json:65-70` |
| remainingOverageTime（总银行透支） | **60 秒/整局**（框架默认 12，被场景 obs 默认覆盖） | `json:128`；`schemas.json:103-109` |
| 超时判定 | `duration - actTimeout > remainingOverageTime` → 动作被替换为 DeadlineExceeded → 状态 TIMEOUT | `agent.py:220-222`；`core.py:279-281` |
| 透支扣账 | 每回合 `overage_consumed = max(0, duration - actTimeout)`，从 remainingOverageTime 中扣减 | `core.py:631-632` |
| URL 型 agent 的 requests 超时 | `remainingOverageTime + actTimeout + 1` | `agent.py:89-91` |
| runTimeout（整局墙钟） | 默认 **1200 秒**（场景未覆盖；超时抛 DeadlineExceeded） | `schemas.json:71-76`；`core.py:326-332` |
| 内存限制 | **本地引擎代码中无任何内存限制/RLIMIT 实现**（全包 grep 无 memory limit 逻辑）；Kaggle 线上侧若有额外配额不在本引擎内 | 全包 grep 负发现（2026-09-19） |
| agent 执行方式 | 文件/字符串 agent 在**同进程** exec（`get_last_callable` 取模块内最后一个 callable）；仅当两个 agent 都是 URL 型才走 multiprocessing Pool | `agent.py:40-72,146-156`；`core.py:740-743` |

**有效预算结论**：每回合 1s + 可透支的 60s 总池。稳健设计应按"每回合 ≤0.9s、整局透支尽量不动用"规划（透支耗尽即 TIMEOUT，reward 记 None，见 §6）。

【实测】引擎步进成本（驱动同一 state 对象反复调 interpreter，动作在原地变更并强制 status=ACTIVE）：
- 全 PASS 回合：**0.022–0.023 ms/步**；
- 带 10 条 BUY_SEED 订单（per-unit 锁步市循环实际成交 150 单位）的回合：**0.096 ms/步**（已验证确有成交：seeds 增至 150）；
- 完整 720 步 `env.run(["starter","starter"])`：**0.96 s** 墙钟（含 make 初始化）；
- 框架 `env.step` 路径（含 structify/日志簿记）：0.787 ms/步——此开销 bot 内嵌模拟时可完全绕开（直接驱动 interpreter 或自写同构模拟器）。

## 2. 观测结构（每个 agent 能看到什么）

【实测】agent 收到的 obs 顶层键（探针 agent 实录）：`day, farms, hour, market, player, private, remainingOverageTime, step, town`。第二个位置参数收到完整 `configuration`（`agent.py:169`；按 `co_argcount` 截断 `agent.py:171-172`）。

- `farms`（**公开共享**，双方互见）：`{money, tiles[10][10], farmer, hands, unlocked_quadrants, hires_today}`（`json:86-97`；`kaggriculture.py:142-154`）。即**对手的钱、地块/作物/动物布局、单位位置、象限解锁、当日雇工数全部可见**；每步由 interpreter 重新同步给 agent 1（`kaggriculture.py:951-956`）。
- `private`（**仅自己**）：`{shed, seeds, inventories}`——棚库存、种子数、每单位随身库存；**对手 shed/种子/随身库存不可见**（`json:98-103`；`kaggriculture.py:169-175`）。
- `market`（共享）：`{inventory, prices}`——**库存与现价都直接给出**；仅当 configuration 传了 `marketParams` 覆盖时才附加 `params` 键（`json:104-109`；`kaggriculture.py:178-185`；【实测】默认对局 `params` 键不存在）。因价格是库存的确定性函数（§4），bot 可用本地同构公式精确预测任意未来价格。
- `town`（共享）：`{unlocked_shops: [...]}`（`json:110-115`；`kaggriculture.py:188-189`）。
- `day`/`hour`（共享）与 `step`：`kaggriculture.py:948-950`；`step` 由框架写 `core.py:626`。
- `remainingOverageTime`（非共享，自己剩余透支池）。
- **随机种子不暴露**：seed 经 `resolve_episode_seed` 读取后从 configuration 中清成 None，仅存 `env.info["seed"]` 进回放（`json:64-67`；`utils.py:199-229`；`kaggriculture.py:249`；【实测】探针读 `configuration["seed"]` 返回 None）。
- 注意（工程坑）：obs 经 `structify` 包装为 `Struct`，`.get()`/`[]` 与 `getattr` 在个别包装层字段上可能不一致（【实测】同对象 `getattr(f0,"money")=3000.0` 而 `f0.get("money")=0.0`）；现役 bot 自带 `_get` 帮助函数（`software/kaggle_simulations/agent/src/constants.py:510-513`），前瞻代码读写 obs 应沿用同款防御式读取或 `dict()` 展开。

## 3. 动作空间

动作结构：`{"farmer": [op,...args], "hands": [[op,...],...], "market": [[op,...],...]}`（`json:130-134`）。每回合：**farmer 恰 1 条 op；每只 hand 恰 1 条 op；market 最多 10 条订单**（超出部分**静默丢弃**：`json:22-27`；`kaggriculture.py:551,561`）。全部非法动作均为**静默 no-op**（`kaggriculture.py:313`）。

- 移动：NORTH/SOUTH/EAST/WEST（越界 no-op）；**允许走上 LOCKED 地块**（防止 hand 被困），但锁定地块上的一切地块操作 no-op（`kaggriculture.py:88-93,323-331,414-415`）。
- PASS（`kaggriculture.py:334-335`）。
- 棚操作（须站在棚 4 个内角访问格之一，`kaggriculture.py:132-139`）：`DROP`（全卸随身库存，受 shedCapacity=100 限制，溢出丢弃，343-356）、`PICKUP <item> [n]`（358-375；**种子不经过棚/随身库存**，直接由 PLANT 消耗，366-369）、`PLACE <item> [n]`（动物放上半空结构 or 普通物品入棚，377-410）。
- 地块操作（须站在已解锁地块上）：`PLANT <crop>`（417-429）、`WATER`（431-443）、`HARVEST`（446-473）、`FERTILIZE`（消耗 1 随身 FERTILIZER，持续 3 天，475-481）、`DIG`（清植物/杂草/空棚圈，不动已放动物，484-491）、`BUILD_COOP`/`BUILD_PASTURE`（493-503）、`FEED`（消耗 1 随身 WHEAT，505-512）、`COLLECT_FERTILIZER`（515-521）、`CARE`（524-530）。
- 市场订单：`BUY_SEED <crop> <n>`（固定价=CROPS.seed，602-603,673-678）、`BUY_PRODUCT <item> <n>`（**仅 WHEAT/FERTILIZER 可买**，按"买后库存"报价使往返净零，598-601,662-672）、`BUY_ANIMAL <animal> <n>`（固定价，604-605,679-686）、`SELL <item> <n>`（**从 shed 直接扣**，无需 PICKUP；按成交时库存逐单位报价，596-597,653-661）、`HIRE`（原子，571-577,702-709）、`BUY_LAND`（原子，按顺序解锁 NE→SW→SE，579-581,712-725）。
- **PLANT 原子校验**：当回合 PLANT 总需求 > 种子持有量时，该作物**所有** PLANT 全部降级为 PASS（`kaggriculture.py:922-933`）。
- 双方市场订单按 **per-unit 锁步**交错成交：第 i 单位双方以同一库存报价、按玩家序提交（`kaggriculture.py:544-628`）→ **对手同回合的卖单会推低你本回合的成交价**（前瞻模型须对对手动作做假设）。市循环有 100k 次迭代保险丝（584-589）。
- 雇工 spawn 在棚访问格（占用最小者优先，533-541）；**hands 与 hires_today 每天 EOD 清零、farmer 归位出生点**（879-882）→ 雇工是"日租制"。

## 4. 市场价格模型（**确定性供给曲线，无随机游走、无噪声**）

- 定价公式：`price(inv) = base ± amp·f(|inv-I0|)`，低于 I0 加价（稀缺）、高于减价（过剩）；`amp = target·base/f(T)`；下限 PRICE_FLOOR=1（`kaggriculture.py:27-39,192-206`）。
- 形状函数 f ∈ {linear, sq, sqrt, log, log10, hinge}；hinge 在 x>T 后二次起飞，`f(T)==1`（`kaggriculture.py:54-58,61-74`，HINGE_GAIN=8.0）。
- 每商品参数（base / T / below / above，`kaggriculture.py:41-51`）：WHEAT 25/400/sqrt·0.80/log·0.20；CARROT 35/450/hinge·1.00/sqrt·0.70；TOMATO 60/200/hinge·0.40/sqrt·0.60；STRAWBERRY 120/100/sqrt·0.70/linear·1.60；MELON 250/300/log·0.20/sq·3.60；EGG 50/332/hinge·0.40/log·0.20；MILK 160/122/sqrt·0.60/linear·1.60；WOOL 200/105/log·0.20/sq·3.20；FERTILIZER 100/200/linear·0.40/linear·0.40。I0=10000（38）。
- **价格变化的唯一来源是共享库存变化**：玩家 SELL +1（成交价 >$1 才计入，$1 倾倒不增库存，`kaggriculture.py:656-660`）、BUY_PRODUCT −1（671）、城镇消费 −1。无均值回归项、无事件冲击价格——"事件"即商店解锁带来的需求抬升。
- 城镇需求：每 `townShopSellInterval=4` 回合每家已解锁商店各抽 1 件其产品（单一产品店抽 2 件，736-743）；镇中心每 24 回合各抽 1 件全部非肥料品（745-747）；商店每 3 天解锁一家、**有放回抽取、上限 8 家**（`json:46-51`；`kaggriculture.py:118,884-891`）。8 家店全部解锁后总需求定型 → 后季价格轨迹完全可由 bot 推演（初始解锁抽样依赖 seed，见 §7）。
- 价格刷新时机：市处理末尾一次（628）+ 城镇消费后一次（749）。
- configuration 允许 `marketParams` 逐商品稀疏覆盖（`json:75-79`；`kaggriculture.py:77-85`）——线上若用默认则与上表一致。

## 5. 经济学常数

**作物**（`kaggriculture.py:11-17`）：种子价 / 首收日 / 峰值日 / 间隔 / 峰值产量 / 常年性：
- WHEAT $10 / 2 / 4 / 0 / 6 / 否；CARROT $20 / 2 / 3 / 0 / 4 / 否；TOMATO $50 / 8 / 8 / 1 / 4 / 是；STRAWBERRY $100 / 10 / 10 / 2 / 4 / 是；MELON $80 / 10 / 12 / 0 / 6 / 否。

- WATER：一次性作物在 `ceil(峰值日/2) ≤ 苗龄 ≤ 峰值日` 窗口内每浇一天 yield +1（施肥 +2），封顶 max_yield（`kaggriculture.py:431-443`）；**连续 2 天没浇 → 变杂草**（种植当天算未浇，`kaggriculture.py:223,783-785`）。
- 常年作物（TOMATO/STRAWBERRY）：自首收日起每 interval 天自动 +1（施肥且当天浇过则 +2），累计封顶 max_yield，达峰后 `max_lifespan_step=(次日+1)×24`（`kaggriculture.py:786-802`）。
- 衰烂：过 max_lifespan_step 后每 2 步 yield −1，归零变 WEED（`kaggriculture.py:752-766`；max_lifespan 定义 224）。
- FERTILIZE：1 袋肥有效 3 天（day, day+1, day+2）（`kaggriculture.py:480-481`）。

**动物**（`kaggriculture.py:19-23`）：买价 / 结构 / 首产日 / 间隔 / 持产上限 / 产品：
- GOOSE $300 / COOP / 4 / 1 / 4 / EGG；COW $400 / PASTURE / 8 / 2 / 6 / MILK；SHEEP $500 / PASTURE / 6 / 3 / 6 / WOOL。

- 每天必须喂 1 WHEAT（随身库存，须先 PICKUP）；**连续 2 天没喂 → 动物逃走**（结构保留）（`kaggriculture.py:505-512,813-819`）。
- CARE：当天"又喂又理"则累积 +1 次日奖励，在下一个"喂饲 production 日"兑现 +1 产量（`kaggriculture.py:821-830`）。
- 每只动物每天可收 1 袋 FERTILIZER（`kaggriculture.py:515-521,831`）。

**雇佣/土地/棚**：
- 日内第 n 次雇工价格 = `farmHandCostMult(默认1) × fib(n)`（1,1,2,3,5,8,…，`kaggriculture.py:99-101,690-699`；配置 `json:68-74`）；hands 次日清零 → 日薪总额 ≈ fib(k+1)−1。
- 土地：第 2/3/4 象限（NE/SW/SE 固定顺序）价 **$1000/$2000/$4000**（`kaggriculture.py:95-97,712-725`）。
- shed 容量 100（`json:34-39`）；EOD 随身库存自动回棚、**溢出丢弃**（`kaggriculture.py:843-857,878`）；买动物/买商品同样占棚容（667-668,682-683）。

**资金机制**：**无利息、无信贷**；money 只在市成交/雇工/购地时变动（`kaggriculture.py:657,669,676,684,704,719` 负发现）。起始 $3000（`json:16-21`）。

## 6. 计分与终止

- **最终分数 = 终局资金**：`reward = float(farms[player]["money"])`，在 `step >= episodeSteps - 2`（即 step 718）时双方置 DONE（`kaggriculture.py:958-964`）。全程无逐步 reward。
- 框架兜底：到步数上限时 ACTIVE/INACTIVE 全置 DONE（`core.py:295-299`）；`done` = 所有 agent 状态 ≠ ACTIVE（`core.py:526-527`）。
- **无提前终止条件**（无破产判定、无投降）：唯一非 DONE 出局途径是 TIMEOUT/ERROR/INVALID——此时该 agent reward=None（`core.py:636-637`；`agent.py:220-222`；`core.py:279-289`）。
- 胜负由 reward 比较（引擎本身不判胜者）；钱多者胜，相等为平局（本地 kgenv 约定 winner=None/tie：`software/kgenv/engine.py:197`）。

## 7. 确定性与体积

- **同 seed + 同动作序列 ⇒ 完全可复现**：【实测】seed=12345 跑两遍 48 步 episode，逐步轨迹、终局 reward、状态全同；`software/kgenv/engine.py:159` 亦如此声明。
- 随机性来源只有两处，且都由"每『天』重播种的 `random.Random((seed*1_000_003) ^ day)`"驱动：① 空未锁地块杂草生成 p=0.005/格/天（`kaggriculture.py:836-840`；`json:40-45`）；② 商店解锁抽取 `rng.choice(sorted(SHOPS))`（`kaggriculture.py:891`）。价格、生长、市场全部确定性。Python `random.Random` 跨版本稳定（Mersenne Twister）。
- seed 对 agent 不可见（§2），但记录在回放 `env.info["seed"]`（`json:64-67`）——离线复盘可精确重建杂草/商店轨迹；bot 在线上只能把已解锁商店序列当作观测增量。
- 纯 Python、无编译依赖；场景代码 46KB（py+json），框架核心（core/agent/utils/schemas）合计亦仅数百 KB；vendored wheel 768 KB。**整份引擎可轻松打包进一个提交 tar.gz**（现役提交已是 9 模块 tar.gz：`software/kaggle_simulations/agent/main.py:1-16`；官方 loader 明确支持同目录导入）。

## 8. 现有自建资产盘点

### 8.1 kgenv 包装层（software/kgenv/）
- `engine.py`：`run_episode(agent0, agent1, seed, episode_steps, act_timeout=60)`——官方引擎单局跑批，返回结构化结果（winner/rewards/逐日资金序列/活跃度诊断 ActivityPolicy）；声明同 seed 确定性。
- `gym_env.py`：`KaggricultureGym`——单 agent gym 式 reset/step/render（对手可插拔），动作清洗 `_sanitize`。
- `economy.py`：引擎经济学的**离线同构镜像**——`price()`/`price_after_selling()`/`sell_revenue()`、`CropCycleModel`、`AnimalModel`、`latest_planting_day`、`glut_sensitivity_report`、`hire_costs`、`land_cost`。前瞻 planner 可直接复用或对齐。
- `arena.py`：`load_submission_agent`（载入 submission 入口）、`run_match`、回放日志、汇总。
- `redlines.py`：farm 状态不变式违规检查（check_farm/summary）。
- `replay_profile.py`（1911 行）：回放取证画像（逐日单位操作、买卖事件、兽群/作物结构、双方对比）。
- `variance.py`：t95/Wilson CI/margin 统计；`elo.py`、`bradley_terry.py`：Elo 与 BT/Davidson 等级拟合。
- `regression.py`：冻结对局集回归判定；`eval_contract.py`/`holdout_contract.py`/`external_h2h_contract.py`/`candidate_identity.py`：fail-closed 评估契约（git 身份、seed 域、AB/BA 赛程、原子发布）。
- `online_probe.py`：线上发射/采样台账与回放完整性检查。
- `bots/`：对局内对手池——`baseline_wheat_agent`、`greedy_carrot_agent`、`cow_baron_agent`、`expansionist_agent`、`melon_hoarder_agent`、`online_style_agent(obs, p)`（参数化线上风格 bot）、`llm_provider`（预算化 OpenAI 兼容 provider）。

### 8.2 scripts/（一句话功能）
- `run_eval.py`：席位平衡本地评估 + 事务性发布（fail-closed）。
- `iterate_gate.py`：候选迭代 AB/BA 门（fail-closed）。
- `run_holdout.py`：一次性冻结候选 holdout 的执行/校验。
- `ablate.py`：成对消融实验与合并门。
- `check_eval_contract.py`：m2a 门/导出安全/正式结果校验执行器。
- `check_candidate_identity.py`：现役候选身份只读自检。
- `check_dna_forensics.py` / `analyze_dna_forensics.py`：回放 DNA 工件校验 / 离线取证生成。
- `check_external_h2h.py` / `h2h_external_probe.py`：外部黑盒 H2H 证据校验 / 生成。
- `check_opponent_strength.py`：对手池成员强度门。
- `corpus_fetch.py` / `corpus_build.py` / `corpus_integrity.py`：m1 回放语料抓取 / 建库 / 完整性校验。
- `fit_bradley_terry.py`：由已录对局拟合 BT/Davidson 等级。
- `forensic_harvest.py`：限量法证回放采样（终交冲刺①）。
- `kill_table.py`：MK-1 kill 表 + 市场事实自检。
- `capacity_calibration.py`：M1 产能律校准。
- `m4_switchover_regression.py`：M4 切换回归。
- `market_ledger.py`：市场引擎追踪账本（逐回合价格/库存/成交对账）。
- `observer_v0_validator.py`：OBS-4 对手观测 V0 离线校验器。
- `probe_v9_wheat_gate.py`：WHEAT_FARM 进入条件在真实对局的触发探针。
- `profile_v48_gap.py`：我方 vs 外部对手的行为差距画像。
- `quickwin_probe.py`：单变量成对 A/B 快赢探针。
- `r3_trajectory_probe.py`：候选逐日轨迹探针。
- `replay_deep_stats.py`：回放逐日单位操作深统计。
- `sell_plan_reconciliation.py`：卖出计划 vs 引擎实际成交对账。
- `solver_shadow_stats.py`：M3 分歧度 harness。
- `sprintA_structure_probe.py`：sprint-A 结构复刻自对局逐日快照。
- `sync_online_probe.py`：线上发射/采样台账同步。
- `verify_milk_economics.py`：牛奶/商店需求经济学在真实引擎上的复算。
- `analyze_failure_modes.py`：对完整对手池多 seed 失败模式探查。
- `run_llm_ab.py`：席位平衡 LLM A/B（含 per-game 预算）。

### 8.3 现役 main.py bot 架构（v13.1 多模块 tar.gz）
- 入口 `main.py`：按拓扑序把 src/ 九模块 exec 进同一扁平命名空间（constants → telemetry → observer → strategy → mission → solver → executor → market → entry），`def agent` 为最后 callable（`main.py:46-78`）。
- 每回合流水线（`src/entry.py:55-193`）：对手观测更新（`_opp_observer_update`）→ **日级宏观 plan**（`_decide_mode` 经济 regime 门：DEFENSIVE / WHEAT_FARM / VOLUME_CROP / SCALE_RANCH / MIXED，含保持规则与价格/吸收阈值，`src/strategy.py:30-134,394-492`）→ 任务构建 `_build_tasks` → mission 影子调度 → 路径求解 `_solve_routes`（**贪心 + 2-opt 局部搜索，含小时截止检查**，`src/solver.py:71-179,542-603`）→ 机械执行 `_execute_routes` → 市场订单（黎明卖单计划、hour≤2 雇工爆发、买前卖后、max-10 官方语义预算闸 `plan_market_orders`）→ 遥测。整体 try/except fail-open 兜底 PASS。
- 已内嵌**部分**前向模型：`_market_private_after_actions`（镜像 DROP 后棚态）、`_market_price_emb`（引擎价格公式镜像，`src/market.py:203-221`）、城镇逐日需求推演 `_town_daily_demand`——即"轻量世界模型"的地基已存在，但**尚无整局/多日前瞻仿真**（无对对手动作的显式建模，对手侧只有观测定账 `_opp_note_orders/_note_fills`，`src/observer.py:220-296`）。

---

## 9. 可行性判断（前瞻规划/MPC 路线）

**结论：可行，且预算宽裕。** 依据：

1. 引擎 interpreter 每步 0.02–0.1 ms（§1 实测，不含框架 structify 开销）；bot 内嵌时可直接驱动 `interpreter(state, env)` 或等价同构模拟器，完全绕开 0.787 ms/步的框架路径。
2. 单回合预算 1 s（actTimeout）+ 60 s 可透支池。保守取安全预算 0.5–0.9 s：
   - **1-step lookahead**：单步推演 ~0.1 ms → **每回合可评估数千~上万**个候选动作集；
   - **1 天（24 步）horizon MPC**：~0.6–2.4 ms/条（空场~中盘）→ **每回合 200–1500 条**候选日计划；中盘满负荷农场估 0.2–0.5 ms/步 → 仍可 **40–180 条/回合**；
   - **3 天 horizon**：约再除以 3 → **15–450 条**（视农场规模）；
   - **整局前瞻（剩余 360–720 步）**：~20–70 ms/条 → **每回合 8–40 条**完整"终局资金"评估——足以支撑"每回合对 5–10 个战略方案各做 1–3 次终局 rollout"的浅层搜索。
3. 确定性 §7 意味着 rollout 无需多样本平均（杂草/商店由 seed 定，不可在线预测但影响小：p=0.005/格/天）；真正的不确定性只有**对手动作**，而市场是共享的——对手卖单直接压你成交价（§3 锁步语义），这是前瞻模型最需要对手模型/鲁棒化的地方。
4. 工程侧：整引擎 46 KB 纯 Python 可整包入提交（§7），kgenv/economy.py 已有离线同构经济学、market.py 已有价格公式镜像——"轻量模拟器"可直接以 `kaggriculture.interpreter` 为参照逐函数裁剪（去掉 renderer/日志/框架），预计 300–500 行内完成。

**主要风险**：
- **Kaggle 线上单核速度未知**：本地 0.02–0.1 ms/步在评审机上可能慢 2–5×；深搜索须做回合预算自适应（时间片预算 + 随时可中断返回贪心解）。
- **对手动作耦合**：per-unit 锁步市使"我方价格推演"依赖对手当回合订单假设；固定对手假设（如"维持近 3 日卖出节奏"，observer 已有账本）+ 对成交价做悲观裕度是低风险起步。
- **状态深拷贝成本**：720 步 rollout 若每步 deepcopy 整个 state 会吃掉预算；应实现增量/写时复制克隆（farms tiles 是嵌套 dict/list，须小心原地变异）。
- **种子不可见**：商店解锁序列在线上只能观测到已发生部分；前瞻到"未来第 8 家店是哪家"只能按期望/鲁棒集处理（影响限于 4 回合一次的消费增量）。
- 维护性风险：提交内嵌引擎副本与 vendored 上游漂移，需在 eval_contract 中加指纹一致性检查。
