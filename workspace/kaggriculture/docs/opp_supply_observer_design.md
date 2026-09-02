# 对手供给反推观测器（OPP-SUPPLY OBSERVER）——设计备忘

- **状态**：已记录、未排期（backlog）。用户 2026-09-02 指示"先记录这个模块，保留反推对手策略另外"。
- **动机**：现有博弈感知只有两个二值门——对手草莓 ≥12 格禁入 VOLUME_CROP
  （`software/kaggle_simulations/agent/main.py:1868`）、对手小麦 >10 格禁入 WHEAT_FARM
  （同文件 `:817`）。目标是把二值门升级为连续的"对手供给时间表"，服务模式选择与卖出
  时序；这正是 r5-P5 anticipated entry 实测 -312.8k 时 rollout 所缺失的"对手供给响应"
  建模（同文件 `:857-864`）。
- **可见性边界**：`obs.farms` 为共享状态——田块（作物/`planted_day`/长势）、已放畜群、
  **money**、象限、雇工数均可见；棚仓 `shed`、随身 `inventories`、种子库存为私有
  （`_farm_scan` `main.py:1679` 及其 docstring）。

## 三通道估计器

1. **价格反推净流量（严格成立）**：
   `opp_net(item,day) = ΔMarketInv + our_net − town_absorb`（符号约定：ΔInv 增=卖压）。
   - ΔMarketInv：优先从 `obs.market.inventory` 直读（`agent()` 已留读取口
     `main.py:4009`，需确认引擎是否每回合暴露）；否则经已知曲线反解——
     `_offset_from_price`（`main.py:2378`）是 `MARKET_PARAMS_EMB`（官方表 99/99
     校验镜像）的反函数。
   - our_net：精确已知（`plan_market_orders` 逐件记账）。
   - town_absorb：`_town_daily_demand`（`main.py:1102`，每店 6 抽/天、单商品店 ×2、
     镇中心 1/天）。
2. **钱账交叉验证（更硬的信号）**：对手 money 公开。`Δmoney + 可见支出 = 净销售收入`；
   可见支出全部可算——雇工 fib 价（`_hire_cost` `main.py:1305`）、买地
   （LAND_PRICE 1000/2000/4000）、买畜（ANIMALS.cost）、种子（按其当日新种格 ×seed 价）。
   与通道 1 的"销量×当时价"对账，偏差即估计漂移信号。
3. **轨迹辅助（定性）**：farmer/hands 每回合坐标可见，行为模式（仓库↔市场往返=卖货、
   成片巡走=养护）作旁证。

## 仓库状态估计（最后一步积分）

`opp_shed(item) ≈ Σ(opp_production − opp_sales)`：

- production 由可见农场建模（草莓 `straw_days` 产期表、畜群畜龄→产夜表）；
- sales 来自通道 1/2。

**定位**：趋势与拐点可信、绝对量 ± 若干——用于决策，不当账本。

## 已知混淆项

1. 对手 BUY_PRODUCT WHEAT（外购饲料）在流量上表现为"小麦负销售"——用其畜群规模 ×
   耗量模型修正；
2. 城镇吸收在市场库存见底时是否失效，需对引擎语义核对一次；
3. 双方同市场归因依赖我方精确记账（已具备）。

## 工程落点

- 照 telemetry 模式做**纯旁路** `_OPP_OBSERVER`（fail-open、不碰决策路径；
  `_MARKET_MEM`/`_STATE` 已按玩家分键）；
- 消费方：`_decide_mode` 的连续折扣版 `opp_contesting`、`_project_price` 注入对手供给项、
  终局 d28-29 对手清算前提前出清。

## 验证计划（先离线后在线）

本地回放含 ground truth（对手 shed 真值可从回放 JSON 读出）：对照估计精度，达标线建议
"拐点日误差 ≤1 天、量级误差 ≤30%"，验证通过后再接入门控。

## 关联

- 策略组合选择器（2026-09-02 讨论）的"状况评估"输入件；
- 开局变体 A/B 实验优先级高于本模块（用户判断：开局是当前最大变数）。
