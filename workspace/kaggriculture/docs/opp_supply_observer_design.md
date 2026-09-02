# 对手供给反推观测器（OPP-SUPPLY OBSERVER）——设计与实施计划

- **状态**：已记录、未排期（backlog）。用户 2026-09-02 指示"先记录这个模块，保留反推对手策略另外"；
  同轮讨论定调策略改进走"预置策略组合 + 分段选择"路线，**开局变体 A/B 实验优先级高于本模块**。
  同日 12:12 `docs/phase_branch_plan.md` v1.0 进一步把本模块定位为 **P4 抢跑的"眼睛"/前置件**
  （时序上仍排在 P0 开局变体之后，见 §7/§8）。
- **动机**：现有博弈感知只有两个二值门——对手草莓 ≥12 格禁入 VOLUME_CROP
  （`software/kaggle_simulations/agent/main.py:1868`）、对手小麦 >10 格禁入 WHEAT_FARM
  （同文件 `:817`）。目标是把二值门升级为连续的"对手供给时间表"，服务模式选择与卖出
  时序；这正是 r5-P5 anticipated entry 实测 -312.8k 时 rollout 所缺失的"对手供给响应"
  建模（同文件 `:857-864`，`VOLUME_ANTICIPATED_ENTRY=False` 留档的原因）。
- **本文档版本**：2026-09-02 第二版。在初版备忘基础上补引擎实锤核验、估计器重构、
  接口草图、验证协议与任务拆解；代码锚点按 v10.9 工作树逐条复核无误。

## 0. 引擎实锤（2026-09-02 核验）

来源：`software/vendor/kaggle_environments-1.32.7+nodeps-py3-none-any.whl` 内
`envs/kaggriculture/kaggriculture.py`（下称"引擎"）+ 线上官方回放 JSON 抽查
（`references/data/online-replays/episode-102194478-replay.json`，720 步全量）。
以下事实**关闭初版的两个待核对项**，并修正可见性强度的假设：

1. **市场库存每回合直读**。引擎把共享 `market`（含 `inventory` 与 `prices` 两键）逐回合
   赋给双方观测（引擎 `:951-956`；线上回放复核成立）。agent() 已留读取口
   （`main.py:4009-4010`）。⇒ 初版"ΔMarketInv 优先直读、价格反解兜底"中**直读路径确认
   存在**，价格反解降级为交叉校验/缺读回退（见 §1 Ch1）。
2. **城镇吸收无下限**。`_town_consume` 无条件 `market["inventory"][item] -= n`
   （引擎 `:743-747`），库存可下穿为负、below 曲线照常抬价——**不存在"见底失效"**。
   初版混淆项 #2 关闭。吸收时点为相位化的固定步（店每 4 步、镇中心每 24 步，
   `turnsPerDay=24`），同 hour 逐日采样时吸收次数恰为整账（见 §6 采样相位）。
3. **双方 farm tile 全量共享，深度远超初版假设**。`obs.farms` 逐 tile 暴露
   `planted_day / yield_units / fertilized_until_day / watered_today /
   consecutive_unwatered`（植物）与 `placed_day / yield_units / fed_today /
   cared_today / pending_care_bonus`（动物），引擎 `:951-956` + 回放抽查确认。
   ⇒ 对手的**逐日收割量、投喂量、照料量是公开账**（HARVEST 把 tile `yield_units`
   清零、FEED 置 `fed_today=True`，均可在共享 tile 上直接读出，引擎 `:446-468/:505-511`）。
   "仓库估计"从建模积分升级为**整数记账**（§1 Ch3）。
4. **$1 地板价卖出不增加市场库存**（引擎 `:658-660` `if price > 1`）且地板价段曲线
   反解退化（多库存位映射同一价，`market_price` 在 `PRICE_FLOOR=1` 钳制，引擎 `:206`）。
   ⇒ 唯一使 Ch0 漏记卖压的场景，见 §2。
5. **BUY_PRODUCT 报价按买后库存**（引擎 `:598-601`），每件买入使库存 -1、钱按报价扣减；
   可买商品仅 WHEAT/FERTILIZER。种子走 `private["seeds"]` 不经棚仓（引擎 `:667-677`）。

其余引擎常量（线上配置实测）：`boardSize=10`、`shedCapacity=100`、
`maxMarketOrdersPerTurn=10`、商店抽取间隔 4 步（=6 抽/天）、镇中心 24 步（=1/天）、
新商店每 3 天末抽取解锁（有放回，实例上限 8）、`LAND_PRICES=[1000,2000,4000]`、
终局 reward=money（引擎 `:960-963`）。`_town_daily_demand`（`main.py:1102`）与
上述口径一致，含重复店铺实例的多重计数。

## 1. 估计器设计（四通道，整账优先）

符号：`d` 上标表示"在每日固定采样 hour（默认 hour=0，首个动作前）取的快照"；
所有量按商品 `item` 分列。

### Ch0 市场库存差（主通道，整数精确）

```
opp_net(item, d) = ΔMarketInv(item, d) − our_net(item, d) + town_absorb(item, d)
```

- **符号约定**：`ΔMarketInv = Inv(d) − Inv(d−1)`；卖压使库存增（`opp_net > 0` 净卖出，
  外购饲料使 `opp_net < 0`）。
- `ΔMarketInv`：直读 `obs.market.inventory`（§0.1）。
- `our_net`：精确已知——我方逐单记账已在 `plan_market_orders` 预算仿真
  （`main.py:1367`）与执行路径（`main.py:3999-4011`）中，旁路记录当日已提交
  SELL/BUY_PRODUCT 的净件数即可（SELL 分"报价>1 件数"与"地板价件数"两口径记录，
  后者对库存无贡献，见 E6）。
- `town_absorb`：按 §0.2 相位精确计数（已解锁店铺逐实例 ×2/×1 × 6 抽 + 镇中心 1），
  复用 `_town_daily_demand`；唯一误差是商店解锁当日的半日效应（E3）。

**预期精度：正常价位段整账残差=0（可逐日断言）**；地板价段见 §2。

### Ch1 价格反解（回退 + 交叉校验）

`_offset_from_price`（`main.py:2378`，`MARKET_PARAMS_EMB` 官方表 99/99 校验镜像的反函数，
`main.py:2334`）从 `Δprices` 反解 `Δoffset`。用途降级为两处：
① `market.inventory` 缺读（防御式编程）时的回退；
② 与 Ch0 的残差监控——残差持续非零即引擎/镜像失配或地板价饱和的告警信号。
现役 `_market_flow`（`main.py:2420-2445`，价格反解 EMA）可重构为 Ch0 的精确流版本，
`_project_price`（`main.py:2448`）的 `flow` 参数语义不变、数值变准。

### Ch2 钱账对账（收入口径 + 外购量）

对手 money 公开（`_farm_scan`，`main.py:1679`）。日账：

```
sell_revenue(d) = Δmoney(d) + hires(d) + land(d) + animals(d) + seeds(d) + buy_product(d)
```

- 可见支出逐项可算：雇工 fib（`_hire_cost`，`main.py:1305`；对手 `hires_today` 公开）、
  买地（象限数变化 × `LAND_PRICES`）、买畜（当日新放畜 tile 数 × `ANIMALS.cost`）、
  买种（按其当日新种 tile 数 × seed 价，为**估计量**——种子私有、以实际 PLANT 数为上界）、
  外购 WHEAT/FERTILIZER（=Ch0 的负流成分 × 当日均价）。
- 用途：① `sell_revenue ÷ 当日成交均价` 交叉验证 Ch0 卖出件数；② 单独解出**对手外购
  饲料量**（初版混淆项 #1 的修正项，见 Ch3）；③ 偏差即估计漂移信号。

### Ch3 产出/投喂公开账（tile 记账，逐日整数精确）

初版"production 由可见农场建模"升级为直接记账（§0.3）：

- **收割量**：`harvested(item, d) = Σ_tiles yield_units(d−1) + 夜间产出(d) −
  Σ_tiles yield_units(d)`。两快照公开；夜间产出按引擎确定性规则（产期表、
  水肥加成 `fertilized_until_day`/`watered_today` 亦公开）可算至逐 tile。
  动物产品同理（畜龄 `placed_day` → 产夜表，`fed_today/cared_today/pending_care_bonus`
  公开 → 加成可算）。
- **投喂量**：`fed(d) = Σ 动物 tile fed_today=True`（公开），即对手当日饲料小麦消耗，
  初版混淆项 #1 的修正项从"畜群规模 × 耗量模型"升级为精确值（注意 FEED 从随身库存扣、
  PICKUP 从棚仓取，时点差只影响棚/随身拆分，不影响"持有-消耗"总账）。
- **未变现持有量（核心输出）**：

```
opp_held(item) ≈ Σ_d [ harvested(item,d) + bought(item,d) − sold(item,d)
                       − fed(item,d) − fertilized_use(item,d) ]
```

  `bought` 来自 Ch0 负流（WHEAT/FERTILIZER）/钱账，`sold` 来自 Ch0，其余公开。
  种子不经棚仓（§0.5）不入账；FERTILIZER 的田间 GATHER 计入 harvested。
  **棚/随身拆分不可知也不需要**——决策关心的"未来可砸向市场的供给"就是 `opp_held`。
  定位不变：趋势与拐点可信、绝对量用于决策，不当账本。

### Ch4 轨迹辅助（定性旁证）

farmer/hands 每回合坐标可见：仓库↔市场往返=卖货节奏、成片巡走=养护，仅作 Ch0/Ch2
冲突时的 tie-breaker 与遥测旁证，不入数值。

## 2. 误差源清单（可枚举、有界）

| # | 误差源 | 影响 | 缓解 |
|---|---|---|---|
| E1 | $1 地板价卖出不入库存（§0.4） | Ch0 漏记卖压（该段对市场价也无影响，对手自己也白卖） | 钱账 Ch2 捕捉（收入仍入 money）；地板价段降置信度标记 |
| E2 | 棚溢出丢弃（日终 DROP 超容量丢弃，量私有） | `opp_held` 高估 | 容量 100 已知 + 持有量接近上限时降置信度；超额囤货档本就稀有 |
| E3 | 商店解锁当日半日吸收 | `town_absorb` 半日 ±3 件级 | 解锁日（每 3 天）单独校准或标记低置信 |
| E4 | 采样相位（hour 选择与 4/24 步吸收相位） | 吸收计数错位 | V0 用整账残差=0 断言经验标定固定采样 hour（§5） |
| E5 | 买种量以实际 PLANT 数估计 | Ch2 中 `seeds(d)` 有 ±（跨日种） | 仅影响钱账交叉验证精度，不影响 Ch0/Ch3 整数账 |
| E6 | 我方地板价卖出不增库存 | `our_net` 口径需与引擎一致（成交≠库存） | 我方逐单记"报价>1 件数"与"地板价件数"两口径 |

初版混淆项 #1（外购饲料表现为负销售）由 Ch0 符号自然容纳 + Ch3 `fed(d)` 精确修正；
#2 已关闭（§0.2）；#3（双方同市场归因依赖我方精确记账）保持，已具备。

## 3. 工程落点

- **纯旁路 `_OPP_OBSERVER`**，照 telemetry 模式（`main.py:253-389`：独立开关、
  sink、快照、per-player 时钟倒退重置）：
  - 状态 per-player dict：`{"day", "inv_prev", "flow_acc", "held", "conf", "money_prev",
    "tile_yield_prev", "fed_seen"}`；对局结束/时钟倒退重置。
  - 更新时序：每日首个动作回合做日账（快照+差分+积分），回合内不再重算
    （与 `_macro_plan` 的日缓存同型，`main.py:1923`）；异常整体 try/except 吞掉并置
    `conf=0`，**fail-open、不碰决策路径、字节级零侵入**（先影子后消费，见 §5）。
  - 输出接口（只读 getter，全部 `est_` 前缀，见 §5 边界纪律）：
    `est_opp_net(item, days)`、`est_opp_held(item)`、`est_opp_supply_horizon(item, h)`
    （=held + 产期表未来产出）、`est_opp_conf(item)`。
- **`_farm_scan` 扩展**：增加全作物集（carrot/melon/watermelon）、逐 tile
  `yield_units` 合计、动物 `yield_units` 按物种合计、`fed_today/cared_today` 计数。
  现签名返回 dict 可增量加键，消费方（`_decide_mode` 等）不受影响。
- **`_market_flow` 重构**：从价格反解 EMA 改为 Ch0 精确流（保留 EMA 输出形状，
  `_project_price` 无感切换）；价格反解留作 Ch1 校验分支。
- **遥测对接**：日账残差、逐商品估计与（离线时的）真值差，经既有 telemetry sink
  落 `.json`，供 §5 验证与线上回放复盘。

## 4. 消费方映射（按收益排序）

> 2026-09-02 12:12 `docs/phase_branch_plan.md` v1.0 对齐注记：opp_contesting 已由用户裁决
> 从 VOLUME 入场门移除（"镜像=时序战，不是避战"，`main.py:1878`，solvency veto 保留），
> 本模块不再服务该门；`_opp_production_calendar`（对手 tile 上市日历，纯公开信息
> ~20 行）是 Ch3 产出侧的轻量前置实现，本模块在其上补齐"已卖/在持"侧；本模块按该
> 计划 §7 兜底定位为 P4 抢跑的前置件，接管 P3 卖出节奏与 P4 出清时点两职。

1. **P4 对手囤货三档抢跑出清**（phase_branch_plan §7/P4）：`est_opp_held` 分档
   （重囤/中囤/零囤）驱动终局抢跑时点（受 P2 倾销限速约束不变）；未就位前按
   ENDGAME 三门态（phase_branch_plan §9 已留此依赖）。M-H 允许的 d28
   `public_liquidation_pressure` 探针即本项的最小实现。
2. **争议线零囤货门的连续化**（`_market_gates` contested 分支）：触发条件从
   "对手该作物格 ≥12"的存量二值，升级为 `opp_supply_horizon` 在途供给速率连续量，
   "收获当日全量出清、第一批卖进最低库存"政策不变。
3. **`_project_price` 注入对手供给项**（`main.py:2448`）：`flow` 从"含对手混合流"变为
   显式对手项 `opp_net`，投影更准；P3 卖出节奏（phase_branch_plan 指派的另一职）与
   止损三态判据直接受益。
4. **策略组合选择器**（2026-09-02 讨论的"预置组合+分段选择"路线）：本模块是其
   "状况评估"输入件——对手供给时间表是分段（开局/中期/终局）选择的共享证据层。
5. WHEAT_FARM 入场门（`main.py:817`）的连续化（次要，该模式默认关闭）。

## 5. 验证协议（先离线后在线）

**语料**：线上官方回放 JSON **含双席每步 `private.shed/seeds/inventories` 真值**
（episode-102194478 抽查确认，720 步×2 席）——真值获取比初版预想更强：
直接用真实线上对局（`references/data/replay-corpus/` 60 局 + `online-replays/` 各轮 +
`.tmp-tetsuya/` 6 局），不必依赖本地引擎自造对局。

- **V0 离线影子（纯函数，无引擎依赖）**：observer 以"仅合法观测字段"
  （`obs.farms/market/town` + 我方 own private）为输入，逐 replay 步进回放，
  对双席输出 `est_opp_held` 序列，与 replay 内对手席 `private.shed+inventories`
  真值逐日比对。**门**：① 正常价位段 Ch0 整账残差=0 的天数占比 ≥95%（标定采样
  hour，关闭 E4）；② 拐点日误差 ≤1 天、量级误差 ≤30%（初版达标线保留）；③ 逐商品
  终局 `held` 误差分布出报告（MAE/最大值），地板价段单列。
- **V1 本地引擎遥测联调**：observer 接入 agent() 旁路，对既有对手池跑 telemetry，
  断言零决策影响（动作序列与关闭时逐字节一致）+ 遥测落盘完整。
- **V2 门控消费（分消费方逐个开）**：每接一个消费方跑配对消融——**注意 2026-09-02
  用户裁定：本地同族对手池不再作候选强度参考与上线门禁**，消融仅作回归诊断
  （防灾难类/防动作污染），真实效应裁决轴 = 线上 A/B（对打天梯，采样协议沿
  SOP v4 轮次节奏）。
- **边界纪律（对齐 M-H NO-GO 审计，2026-09-01 11:05）**：M-H 否决的是"在对局内
  合法观测对手库存"（在线无通道、线上台账无逐日快照可校准）——本模块不违反该结论：
  在线运行时只消费合法公开字段做**估计**（接口一律 `est_` 前缀，不得称直接观测），
  replay 私有字段**仅离线校验器可读**、绝不进入 agent 代码路径；d29 全清硬约束不因
  估计松动。

## 6. 风险与开放问题

1. **地板价饱和段**（E1）：若线上对手频繁死价抛售，Ch0 在该段降级为钱账口径，
   `est_opp_conf` 联动下调；V0 会给出该段占比实测。
2. **采样相位标定**（E4）：`turnsPerDay=24`、吸收步 4/24 相位固定，理论上 hour=0
   采样即整账；以 V0 门①实证，若非零再调。
3. **买卖同回合交错定价**：per-unit lockstep 下双方同回合 SELL/BUY 互相影响成交价，
   Ch2 的"当日成交均价"用 ΔInv 加权近似即可（验证用途，不追求逐单）。
4. **置信度聚合不做在线拟合**：`est_opp_conf` 的衰减/融合系数用 V0 语料离线定死，
   遵守"nothing is learned online"纪律（`_decide_mode` 既有原则）。
5. **对 tetsuya 式零库存种子流**：对手 held 常近 0、供给即时变现——正是本模块想要
   捕捉的"高周转"形态，V0 语料已含其 6 局可专测。

## 7. 任务拆解（排期占位，开工时再细化）

| 包 | 内容 | 前置 | 量级 |
|---|---|---|---|
| OBS-1 | `_farm_scan` 扩展 + Ch3 tile 记账（纯函数 + 单测） | 无 | 0.5 会话 |
| OBS-2 | Ch0/Ch1（`_market_flow` 重构 + 我方逐单记账旁路） | OBS-1 | 0.5 会话 |
| OBS-3 | Ch2 钱账 + `est_*` getter + telemetry 日账输出 | OBS-2 | 0.5 会话 |
| OBS-4 | V0 离线影子验证器（replay 语料 + 真值比对 + 门①②③） | OBS-1..3 | 1 会话 |
| OBS-5 | V1 零侵入断言 + V2 首个消费方（P4 三档出清或争议线零囤货连续化）+ 线上 A/B | OBS-4 过门，且按 phase_branch_plan §9 顺序排在其 P0-P3 之后 | 1-2 会话 |

## 8. 关联

- `docs/phase_branch_plan.md` v1.0（2026-09-02 12:12）：本模块为其 P4 抢跑的"眼睛"与
  前置件，接管 P3 卖出节奏/P4 出清时点两职；其 `_opp_production_calendar` 是 Ch3 产出侧
  的轻量前置实现，`opp_contesting` 已按用户裁决移出 VOLUME 门；
- 策略组合选择器（2026-09-02 讨论）的"状况评估"输入件（§4.4）；
- 开局变体 A/B 实验优先级高于本模块（用户判断：开局是当前最大变数）；
- M-H 终盘对手库存审计 NO-GO（2026-09-01）的合规边界（§5）；
- r5-P5 anticipated entry 失败归因（`main.py:857-864`）——对手供给项是其"完整评估器
  + 对手情景"重开路线（P6 方向）的前置输入之一。
