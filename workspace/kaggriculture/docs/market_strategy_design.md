# 市场策略设计（MARKET STRATEGY）——卖出计划器 + 攻防对抗 v1.3

- **版本**：v1.3（2026-09-03，按当前生产代码、官方引擎成交账本和双边差分结果更新）
- **当前结论**：卖出计划器、买侧策略、防御响应、EOD 腾仓和干扰载体 1 已进入生产路径；载体 2-4 保持关闭。
- **最终目标**：在官方逐件 lockstep 市场语义下，使计划卖出可执行、可重试、可对账，同时不牺牲饲料、仓容和现金安全。

---

## 1. 当前生产架构

```text
entry.agent(obs)
  -> _opp_observer_update
  -> _macro_plan
  -> _build_tasks / _solve_and_execute
  -> _market_private_after_actions
       仅镜像本回合真实 DROP 后的棚仓和随身库存
  -> _sell_plan_shadow_update
       每玩家、每日只生成一次卖出计划
  -> _market_orders
       feed / opportunity BUY / EOD SELL / gates / planner / interference
  -> 合并同商品 SELL
  -> plan_market_orders
       最多 10 单、逐件曲线、钱包、库存和仓容仿真
  -> _finalize_sell_plan_batches
       根据最终 filled 提交或回滚 planner / EOD / interference 状态
  -> 返回官方动作
```

运行时权威文件：

- `software/kaggle_simulations/agent/src/entry.py`
- `software/kaggle_simulations/agent/src/market.py`
- `software/kaggle_simulations/agent/src/observer.py`
- `software/kaggle_simulations/agent/src/mission.py`

## 2. 市场执行不变量

### 2.1 官方预算镜像

`plan_market_orders` 是最终订单预算权威：

1. 按市场优先级选取最多 10 个订单；
2. 被选订单保留原队列顺序；
3. `BUY_PRODUCT` 和 `SELL` 按官方曲线逐件重新报价；
4. 每件成交后立即更新钱包、棚仓占用和共享市场库存；
5. `$1` 地板价卖出增加现金，但不增加市场库存；
6. 返回每个源订单的 index、filled 和 abort，供状态账本确认。

测试侧已有双边 lockstep 镜像，覆盖双方同时 BUY/SELL、资金中断、地板价、不同队列长度和 seat 交换。

### 2.2 市场可见库存

官方引擎先执行单位动作，再执行市场订单。入口使用 `_market_private_after_actions` 构造市场阶段状态：

- 本回合真实执行 `DROP` 的随身货进入预演棚仓；
- 对应 carrier 的预演随身库存清空；
- `shed_count` 和 `shed_stock` 使用同一份 post-DROP 状态；
- `HARVEST` 后的货仍在 carrier，不能同回合再次 `DROP`，因此不得提前生成 SELL。

这条约束同时适用于卖出计划、EOD 事件、市场门控和最终预算。

## 3. 卖出计划器

### 3.1 日计划输入

黎明计划读取：

- post-DROP 棚仓现货；
- 当前已成熟但尚未收割的 `yield_units`，仅作为诊断 inflow；
- 城镇吸收量；
- 当前价格和 `_market_flow`；
- 对手争议线；
- P4 冻结档位；
- mission EOD overflow。

**当天计划数量只承诺棚仓中实际可卖库存。** 地块上的成熟产物不会计入 `qty_today`，直到后续回合真实收割并 DROP 入棚。

### 3.2 Hold / Clear

一般判据：

```text
hold iff projected_price >= spot_price * SELL_PLAN_HOLD_EDGE
         and item is not contested
otherwise clear
```

覆盖规则：

- 对手作物格数达到争议阈值，或对手牛/羊达到对应阈值：强制 clear；
- P4 heavy 档立即 clear，mid 档从 d26 clear；
- EOD overflow 可强制腾仓；
- sq 曲线受供给压力时立即 cut；
- linear 曲线受供给压力时执行有界 `short_hold`。

### 3.3 Linear short_hold

`STRAWBERRY` 和 `MILK` 的 `short_hold` 已具有真实行为：

1. 第一个连续压力日暂缓普通计划卖出；
2. 第二个连续压力日恢复 clear；
3. 同一日通过日计划缓存保持幂等；
4. 争议线、P4、EOD、仓容危险和破产现金线可跳过短持；
5. 旧 `_market_gates` 不得覆盖正常 hold；
6. 只有相对黎明价明显崩盘或紧急状态时，战术 override 才可接管。

因此当前所有权是：**黎明计划器决定常规节奏，旧门控只处理计划外突变。**

### 3.4 数量和批次

计划清仓量：

```text
qty_today = min(executable_shed_supply, daily_absorption_cap)
```

EOD 强制事件可突破普通吸收限速，以避免仓容损失。

批次规则：

- 时点为 `h6 / h12 / h18`；
- 每条线最多 3 批；
- 最多 4 条计划卖出线；
- 余数均匀分配，始终满足 `sum(batches) == qty_today`；
- 例如 10 件拆为 `[4, 3, 3]`。

### 3.5 Pending / Committed

planner、EOD 和 interference SELL 均遵守两阶段确认：

```text
生成候选 -> pending
最终预算 filled == requested -> committed
零成交或被 10 单截断 -> 清除 pending，下一回合重试
部分成交 -> planner 扣减剩余量；EOD 保持可重试
```

同商品 SELL 合并时，sidecar 来源标识同步重映射到合并订单，避免对象重建后丢失确认关系。

## 4. EOD 与终局

### 4.1 通用 EOD 腾仓

mission 可针对任意可交易商品生成 `eod_budget` SELL，不再只依赖 WHEAT：

- 按当前可交易棚仓库存分配腾仓量；
- 市场层数按实际库存钳制；
- 事件被预算拒绝后可重试；
- 多商品事件可共同完成 overflow 释放。

### 4.2 WHEAT 储备

非终局 WHEAT 卖出计划必须先扣除：

```text
未喂牲畜口粮 + WHEAT_FEED_RESERVE - carrier 随身小麦
```

只有超过系统饲料安全线的棚仓 WHEAT 可进入普通卖出计划。EOD 强制腾仓可覆盖该储备规则。

### 4.3 d29

终局只保留 SELL：

- carrier 先执行安全 DROP；
- 只有实际能进入棚仓的数量进入市场预算；
- 已在棚仓中的所有可交易商品参与清算；
- 不伪造尚未入棚的 HARVEST 货物。

## 5. 买侧策略

### 5.1 饲料义务

`feed_precondition` 是 D1/D2 生存义务：

- 在 h0-h2 消费 mission BUY_PRODUCT WHEAT 事件；
- 棚仓和所有 carrier 的 WHEAT 共同计入系统库存；
- 已满足事件时不得重复购买；
- 正常饲料购买受价格护栏，真实饥饿状态使用更高止损上限。

### 5.2 机会性 WHEAT

机会采购已与即时缺粮分支解耦：

```text
WHEAT price < OPPORTUNE_WHEAT_PRICE
and cash remains above reserve
and shed has room
-> buy toward OPPORTUNE_WHEAT_DAYS target
```

即使当前没有待喂牲畜，也允许建立小额低价储备。存在已满足的同日 `feed_precondition` 时不额外扩张，防止安全垫窗口重复购买。

### 5.3 多笔 BUY_PRODUCT

同回合多笔 WHEAT 采购共用一个 `buy_product_units` 偏移：

- 后一笔 affordability 从前一笔采购后的库存开始；
- committed spend 使用相同偏移计算；
- 每笔最多 `BUY_CHUNK_MAX_UNITS`；
- 最终仍由 `plan_market_orders` 做官方逐件校验。

## 6. 干扰模块

### 6.1 当前触发器

当前生产触发量采用双方可比的 7 日流量口径：

```text
R_opp = opponent calendar * min(supply, absorption) * projected price
R_us_flow = our calendar * min(supply, absorption) * projected price
raw_trigger iff R_opp > R_us_flow + INTERFERENCE_MARGIN
```

`_plan_rollout` 终值只写入日志用于校准，不直接与 7 日流量混合比较。

触发要求连续 2 天确认；同日重复调用不推进或重置 streak。状态和日志按 player/day 隔离。

### 6.2 三闸

1. `confirmed`：连续日触发成立；
2. `gate_exposure`：对手顶线价值至少为我方同线暴露的规定倍数；
3. `gate_budget`：计划雇工后的容量定律允许干扰资产预算。

触发消失即停止生成新干扰订单。

### 6.3 载体状态

| 载体 | 当前状态 | 结论 |
|---|---|---|
| 现有库存倾销 | **LIVE** | 零新增 capex；按反解目标价计算数量；最终预算成功后才写 fired；拒单可重试 |
| 胡萝卜伏击 | **LIVE（激进波 C 2026-09-04）** | 跨日状态机实装：确认触发（2 日 streak）→ 战略层 d5-12 一次性钉定目标日（stage register `iv_state`）→ 分配层种 ≤8 格萝卜（`iv2_carrot`）→ 目标日到点且触发仍确认时 `_interference_v2_orders` 全量倾销（走正常预算截断） |
| 一次性羊群 | **教义算术否决（维持）** | 15% 容量 ≈6 只羊低于其自身暴露闸要求的杀伤量——武装它违反教义算术而非仅其谨慎；提高 `INTERFERENCE_BUDGET_FRAC` 可重开 |
| 早期镜像产线 | **LIVE（激进波 C 2026-09-04）** | d4-6 确认触发时读对手公开 tile 优势作物，`iv4_mirror` ≤6 格经 `_field_alloc` extras 直接落格（先于对手既有 block 进入产出曲线）；自身暴露由分线封顶与容量门约束 |

载体 2-4 不得通过简单追加 BUY 单上线。它们需要独立的跨日状态、预算后确认、资产标记、收手逻辑和 A/B 验证。

## 7. 真实成交验证

### 7.1 OfficialMarketLedger

`software/scripts/market_ledger.py` 包装官方 `_commit_unit`，不替换市场解析器和成交器。每个尝试记录：

```text
seed / day / hour / player / order_column /
op / item / unit_price / success
```

context 结束后恢复官方函数，避免污染后续测试。

### 7.2 Reconciliation v2

`software/scripts/sell_plan_reconciliation.py`：

- 只把官方 `_commit_unit` 成功的 SELL 计为真实 fill；
- 不使用 action.market 或回合前 spot 代替成交；
- 输出 planned qty、fill qty、未成交量、数量加权均价、价格偏差；
- 输出 loader + 全部 `src/*.py` 的组合 SHA；
- 输出官方引擎版本和源码 SHA；
- 默认门禁：fill coverage ≥ 0.80 且 P90 绝对价格偏差 ≤ 15%。

### 7.3 当前实测

当前源码，官方完整回合，seed 7、8：

```text
planned_qty:            890
real fill_qty:          890
fill coverage:          1.0000
line coverage:          1.0000
P90 abs price deviation: 3.87%
gate:                   PASS
strategy source SHA256: a68e5a2300f95b262b750e83bf428fc7205dd16e1a6b04b622308d334bd49291
```

证据文件：

`software/exports/probes/sell_plan_reconciliation_seed7_8_final_current.json`

## 8. 测试与构建状态

- 市场专项、真实 ledger、双边 lockstep：`59 passed`；
- 完整软件测试：`817 passed, 2 skipped`；
- 确定性提交包：`submission.tar.gz`，114955 bytes；
- package SHA256：`1c9d74754c4da344f7c606618671925b4e2348ea9f7fa07e93734d6e4eba8dff`；
- `build.py --check`：PASS；
- candidate identity：PASS。

新增验证文件：

- `software/tests/test_market_strategy_repairs.py`
- `software/tests/test_market_bilateral.py`
- `software/tests/test_market_reconciliation_ledger.py`

## 9. 实施里程碑

| 步 | 当前状态 | 门禁结论 |
|---|---|---|
| MK-1 曲线/杀伤事实工具 | 部分完成 | 曲线反解和地板价已有测试；杀伤收益仍需按载体单独验证 |
| MK-2 黎明卖出计划器 | **完成** | 真实成交 reconciliation PASS |
| MK-3 计划器接管 | **完成** | 计划器主导，门控仅战术覆盖；全量回归 PASS |
| MK-4 干扰触发器 | **完成基础接线** | 连续日、玩家隔离、日志和三闸已接线 |
| MK-5 载体 1 | **LIVE** | 预算后确认、拒单重试、日内幂等 |
| MK-5 载体 2-4 | **NO-GO** | 不满足当前最小闭环与验证要求，保持关闭 |

## 10. 后续工作

1. 将载体 2-4 分别作为独立实验，不共用一次大改；
2. 先实现统一 `_INTERFERENCE_PLAN[player]` 跨日状态机，再接资产动作；
3. 每个载体必须先证明杀伤量在 15% 容量内可达，否则直接拒绝启动；
4. 胡萝卜载体需验证完整 BUY_SEED → PLANT/WATER → HARVEST → DROP → SELL；
5. 羊群载体需验证 BUY_ANIMAL → PLACE → 产出 → 清仓 → 停喂退出；
6. 镜像载体必须在 d4-6 内证明首卖时序优势，d7 后禁止新建；
7. 新载体上线前必须重复官方真实成交对账、双边差分、完整回归和线上 A/B。
