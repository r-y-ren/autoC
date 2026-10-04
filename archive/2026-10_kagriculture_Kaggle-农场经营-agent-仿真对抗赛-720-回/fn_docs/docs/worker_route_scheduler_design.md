# 雇工路线调度器设计（WORKER ROUTE SCHEDULER）——四层架构 v1.4

- **版本**：v1.4（2026-09-03 实施状态更新：共享 PICKUP 资源预留、D1 缺料显式分诊、累计 ETA、d29 安全清算、EOD 通用卖出、容量增量门与 LIVE trace 已落地；v1.3 2026-09-02 三重前置检查；v1.2 容量定律与 deficit 前馈；v1.1 引擎实证版）
- **定位**：按“策略选择 → 今日任务包 → 路线求解器 → 机械执行”四层架构重构雇工调度。
  当前四层链路已经是唯一生效的动作调度路径：`mission.py` 生成/增强任务，`solver.py` 按现役船员求解，`executor.py` 机械执行，`market.py` 接收 EOD/d29 卖出事件。
- **当前实现落点**：`src/mission.py::_build_mission/_enrich_mission_tasks`、`src/solver.py::_solve_routes/_solve_and_execute`、`src/executor.py::_execute_routes`、`src/market.py::_market_orders`。
- **范围裁决**（用户 2026-09-02）：当前 `agent/main.py` 只作加载入口，行为实现走重构路径；旧 v72 调度器、`ROUTE_EXECUTOR_ENABLED` 切换开关和过渡回退均已删除。行为等价性继续以回放和测试验证，不在新代码保留旧调度器副本。
- **讨论裁决**（2026-09-02，不变）：引擎确定性 + 农场主权 + 义务自造性决定当日任务可计算；红线由任务 `deadline/tier` 表达；每回合只重解/执行/断言，失败出口为有界 REPLAN 或显式不可行状态。

---

## 1. 引擎事实表（vendored 1.32.7 源码逐条核验，2026-09-02）

| # | 事实 | 源码 | 对设计的后果 |
|---|---|---|---|
| F1 | **移动无阻挡**：仅边界检查，LOCKED 格也可走（tile 操作才被 LOCKED 拒绝） | :323-332 | 曼哈顿 ETA 精确成立，无需寻路绕行（v1.0 风险关闭） |
| F2 | **枯死阈值 `consecutive_unwatered >= 2`**（EOD 日刷新判定→WEED）；**种植当天 streak=1** | :222, :783 | "今夜枯死"集合精确可算：streak≥1 的在地作物 + 当日新种。昨日浇过（streak 0）的格有**一天宽限**——可作降级优先级而非常规手段 |
| F3 | **逃亡阈值 `consecutive_unfed >= 2`**（→逃走，畜栏保留）；**放置时 streak=0** | :236, :817 | 同宽限结构：streak≥1 的牲畜今夜必喂；新放置有宽限 |
| F4 | **FEED = 站在牲畜格 + 随身 1 小麦**，fed_today 去重；WATER 同样 watered_today 去重（重复=静默浪费一回合） | :505-513, :431-436 | 喂食腿=先 PICKUP 后配送（载货规划）；执行器发射前查 tile 态避免空转 |
| F5 | **非连续产作物（麦/萝卜/瓜）产量只来自窗口内浇水**：age∈[⌈(max_yield_day+1)/2⌉, max_yield_day] 每浇一天 +1/+2（施肥），上限 max_yield | :438-443 | 浇水任务分两类：**窗口内=产钱**（漏浇=永久减产，软死线但价值递减）、窗口外=仅保命。任务价值 v 按此标注 |
| F6 | **随身无容量上限**（_inv_add 无 cap）；**EOD 自动归还**：全部随身倒棚仓（溢出销毁），farmer 重置回出生点、hands 清空、hires_today 归零 | :299-300, :843-882 | ①季中**无需日间归还腿**——收割后随身挂着，EOD 自动入仓；②**每日 EOD 预算**：Σ(棚仓+随身) ≤ 100 否则销毁 → 卖出计划必须保证日终余量；③**每日黎明全员从棚仓/中心出生** → 家区不能用"首格"判，须负载均衡指派（§3.1 修正） |
| F7 | **日内零随机**：杂草只在 EOD 刷（weed_chance=0.005，seed+day 确定性 RNG，且只占空格）；商铺解锁只在 EOD | :836-840, :886-891 | 日内世界完全可知：断言在正确实现下除场景切换外**永不触发**（v1.0 抖动风险关闭）；城镇吸收表全日恒定 |
| F8 | **非法动作=静默 no-op** | :313 | 执行器保留发射前合法性检查（不浪费回合） |
| F9 | **市场单逐件 lockstep、先单位动作后市场单** | :544+, :941 | 同回合 SELL 不能为同回合 DROP 腾位——卖出须早一回合排程（日终预算联动，§2.5） |
| F10 | 末日（d29）：EOD 归还已无意义（奖励=资金），**当日棚仓可卖、随身不可卖** | 奖励语义 | d29 采用安全变现：空 carrier 继续收割；有货 carrier 先回仓，仅在棚仓可完整容纳时发裸 DROP，再由同回合市场段 SELL；空间不足禁止 DROP，避免溢出销毁 |

## 2. L2 今日任务包（_build_mission）——按事实表修订

### 2.1 数据结构（同 v1.0）

task = {key, op, x, y, act, deadline, v, cls, deps, need, scenario, units}；
mission = {day, player, plan, scenario, tasks, events, capacity_deficit}。

### 2.2 deadline 分级（F2/F3/F5 重写）

| 集合 | 判据（黎明可算） | deadline | 语义 |
|---|---|---|---|
| **D1 今夜必死** | 作物 streak≥1 / 当日计划新种；牲畜 streak≥1 | 浇 h21 / 喂 h16 | 硬保证对象（§5 定理） |
| D2 明夜必死 | 作物/牲畜 streak=0（用宽限） | 次日 D1 | 正常仍当日做（优先级次之）；只在容量赤字时显式动用宽限 |
| D3 产钱窗口 | 非连续产作物 age∈窗口（F5） | 当日 | 漏浇=永久减产；v 按窗口剩余价值标注 |
| D4 收割/照料/DIG | 过熟衰减 / 加成 / 无 | 当日/无 | 密度排序项 |

### 2.3 喂食的前置条件（F4）

黎明检查：棚仓+随身小麦 ≥ D1∪D2 牲畜数；不足 → mission.events 注入 h0 BUY_PRODUCT WHEAT。
市场层在 h0-h2 消费该事件，并以棚仓+所有 carrier 的系统小麦重验缺口；到货后幂等跳过，
与常规 feed-security 采购共用 committed-spend 账，避免重复买麦。缺料 D1 不再静默消失，
由 solver 记录到 `material_deficits`（见 §3.2）。

### 2.4 EOD 预算（F6，现役硬约束）

```
eod_projected =
    shed_count
  + carried_count
  - planned_sell
  + planned_harvest_yield

overflow = max(0, eod_projected - 100)
```

任务包同时统计棚仓与所有 worker 随身库存，不再只看 shed。出现 overflow 时，按当前棚仓中
可交易商品的库存量降序、商品名稳定排序，生成有界 `eod_budget` SELL 事件；不再限定为
WHEAT。市场层在计划小时消费事件、与同商品其他 SELL 合并并按实际库存封顶。执行器每回合
复核棚仓+随身总量；当前实现不做激进 HARVEST 尾部裁剪，是否削减收益任务留给后续回放消融。

**闭环（2026-09-04 激进波 B）**：两遍构建已接线——mission 先按 planned_sell=0 保守构建（供卖计划读 overflow），卖计划算出后 `_mission_refresh_planned_sell` 以真实 `planned_total` 重建并覆写缓存，eod_budget 事件精确化。历史注记：此前生产路径的 `planned_sell` 恒为 0——mission 在 entry
的黎明时序里先于当日卖出计划构建（`_mission_shadow_update` → `_sell_plan_shadow_update`），
该时刻计划卖出量不可得。投影因此系统性**高估**日终占用，方向保守（只多生成 eod_budget
卖单、防溢出销毁，不会漏报）。接线闭环（卖出计划前移或 mission 二次更新）列为战后项，
audit-repairs 波不改动 entry/mission 调用链。

### 2.5 卖出排程耦合（F9）

计划卖出分散在固定小时段（如 h6/h12/h18），为 EOD 和 d29 清算提前腾位。市场层逐回合
按门控微调**卖什么**；`eod_budget` 事件在计划小时到达后消费，同商品 SELL 合并并按
当前库存封顶。预算截断/部分成交的卖出批次按 pending 状态可重试；d29 DROP 队列则在
单位动作先执行后由市场层消费。

### 2.6 容量定律与 deficit 前馈（v1.4 实施口径，与 phase_branch_plan §5.3 对偶）

> 分工裁定：**策略层（branch plan §5.3 容量前置门）负责只生产可行计划；本层负责证明
> 或标记**。本节是两层之间的焊点。

**容量定律**（M1 已定标并回填现役常量）：

```
最大资产单位(d) ≈ 24 × (1+H) × 0.89 ÷ 3.3
资产单位：莓/麦/瓜格=1，萝卜格=0.5，牲畜头=2；H 为 hands 数，不含 farmer
crew 12（H=12）容量约 84.1，采购上界取容量 × 0.85
```

牲畜容量基数包含地块上已放置牲畜、棚仓和所有 carrier 中待安置的 COW/SHEEP/GOOSE；
同回合 capex 使用累计 `reserved_units`，土地按 +25、种子按 +n、牲畜按 +2n 预留，批量
逐步缩到可行边界或拒绝。定标交叉锚为 top-20 约 3.29/0.89、tetsuya 约 3.46/0.84、
local 约 4.43/0.93；现役采用 3.3/0.89。

**前馈接线（当前实现）**：

1. `_build_mission` 对当前资产计算 `capacity_deficit/capacity_slack`，供策略层和 telemetry 诊断；
2. 实际 capex 截断落在 `market.py::_market_orders`：土地、种子、牲畜共享同回合
   `reserved_units`，逐批缩量到容量 ×0.85 内；超限订单不进入最终市场预算；
3. 低于 0.65 时阶段计划附加 backfill 候选；峰值日由 mission 计算 `peak` 做诊断。

`capacity_deficit` 只表示资产容量越界；任务缺料由 solver 的 `material_deficits` 独立表达。

**M1 定标任务（已完成）**：telemetry 按资产类别实测"回合/单位/日"系数
（浇水/收割/喂食/照料/走路分项），与参考回放交叉后，现役定律采用 3.3 与利用率 0.89；
C1 的 crew 上限继续由分支参数包和容量门共同约束。

### 2.7 capex 事件与三重前置检查（已实现；政策定义见 branch plan §5.4）

**当前计算落位**：种植、买畜、买地仍由 `mission.py::_build_tasks`、`market.py::_market_orders`
协作生成，而不是统一的 mission capex 事件表。种植任务按真实种子预算和当日种植配额生成，
避免原子 PLANT 超发；买地/买畜集中在早段，所有采购共享容量与现金账。

**三重前置检查（一票否决）**——每个 capex 候选进入订单前过三门：

1. **劳动力**：§2.6 容量定律（> 0.85 就地缩量）；
2. **曲线**：该产品线投影价（`_project_price` + 观测器 Ch0 对手流量）≥ 地板
   （奶/毛 90、蛋 30、作物 CROP_FLOOR）——**迁移自运行时死价红线**，升级为
   投影价判据；
3. **现金**：黎明现金流不变式——投影日终钱包 ≥ 次日黎明 crew 账单 + 饲料裕量
   （卖出所得按投影价折减计入）——**迁移自 LIQUIDITY_FLOOR**，从每笔地板升级
   为整日一次解。

同回合逐件结算的钱包记账（committed_spend 语义）**保留在 `plan_market_orders`
逐件仿真内**（引擎语义层，非策略）——多订单回合的 3256→16 事故类由仿真网兜底。
自洽红利：干扰模块主动砸某线时，同一黎明的曲线门自动停该线扩张（进攻与建设
不打架）。

## 3. L3 路线求解器（_solve_routes）

### 3.1 分区（当前实现）

当前求解器不承诺固定的象限×cls LPT 分区；它以 D1 EDF 先分配，再用价值密度、旅行成本、
跨象限惩罚和连续性奖励填充各 worker 路线。跨区任务作为带惩罚的候选，不是硬隔离。
象限×cls 负载均衡仍是效率优化遗留项，不能写成正确性保证。

### 3.2 成路与抛光（现役实现）

EDF×密度×老化最近邻 → 2-opt 无 deadline 尾段抛光 → 逐站累计 ETA 重验。
排序键终结于 key 字典序（确定性前提）。求解器维护跨工人的共享 `available_shed[item]`：
显式与合成 PICKUP 排入路线即扣减共享余额，取货总量不得超过棚仓现货；WHEAT/FERTILIZER/
牲畜均适用。缺物料任务进入 `drop_reasons.material` 与 `material_deficits`，D1 缺料令
`feasible=false`，不再静默过滤。

### 3.3 回放与确定性对照

四层调度已经 LIVE；v10.9/tetsuya 回放只作为行为与效率对照，不再承担影子切换门。
同输入确定性、任务包哈希和 deterministic package 继续由测试锁定；线上公共局仍是收益裁决轴。

## 4. L4 机械执行（_execute_routes）

```
每回合每工人：到站且 tile 态未完成（F4/F8 去重+合法性）→ 发动作；否则走一步；
季中无归还腿（F6 自动）；d29：空 carrier 继续 HARVEST 路线，有货 carrier 安全回仓，
仅在 room 足以完整接收整份背包时 DROP，并把落仓货加入同回合 SELL；
断言（只读）：从当前 hour/位置沿全部剩余站点累计移动+动作成本，检查路线内所有后续 D1；
EOD 断言是**当前溢出快照**（只读现时棚仓+随身存量，不含路线剩余 HARVEST/PICKUP 入仓与
计划卖出——非前瞻投影，触发=溢出已存在）。失败触发一次有界 REPLAN：重建消费同一世界
输入（首趟执行只返回动作、不改 farm/private），重解与首解相同、幂等闸抑制重复触发；二次
仍存活的触发以 `replan_repeat` 记入 trace（F7 持续断言信号），不追加第三次求解——有效
修正依赖下回合现役重解。
```

solver 的最终 `feasible`、`dropped`、`drop_reasons`、`material_deficits`、`feed_legs`、
`replanned` 与 `replan_repeat` 写入 `_SCHEDULER_TRACE[player]`，供 LIVE telemetry 消费；整体
try/except 继续提供合法 PASS 兜底。

## 5. 保证定理（审查结论：能否保证完成任务）

**定理（proved-or-flagged）**：在 F1/F6/F7（无阻挡、日零随机、工人集合日内恒定）下，
求解器输出的每条路线其逐站 ETA 是**精确**的；因此：

1. **断水枯死**：每个 D1 作物任务必须得到显式结果：累计 ETA 在 deadline 内；或有物料但无法按时完成，记录 `no_fit/late_best_effort` 并令 `feasible=false`；或物料不足，记录 `material_deficits` 并令 `feasible=false`。`capacity_deficit` 只表示资产/劳动力容量越界，不再兼任缺料状态。
2. **断粮逃亡**：同构；`feed_precondition` 在 h0-h2 买麦，solver 按共享棚仓余额建 PICKUP 腿，缺口在求解时显式暴露而不是深夜才发现。
3. **末日归还**：季中归还由 F6 自动完成；d29 只在棚仓能完整容纳 carrier 时执行裸 DROP，禁止以销毁溢出换取形式清零。随身清零仅在剩余回合和棚仓空间足够时保证。
4. **EOD 溢出销毁**：由 §2.4 的棚仓+随身+计划收割投影、通用 SELL 事件和执行断言共同防护。

**不保证的**（诚实边界）：路线的**最优性**（同约束下是否有更短路线）——这由 M3 影子
门（与参考回放的分歧统计）和消融矩阵背书，不由定理背书。调度器也不能无中生有容量：
15 头牲畜×喂食腿超过全队 24×n 回合物理上限时，任何算法都只能选择谁先死——
本设计的价值是让这个不可能在**黎明显形**（deficit → 策略层停止扩栏），而非深夜暴雷。

## 6. 风险表（v1.1 重审）

| 风险 | 历史状态 | v1.4 现状 |
|---|---|---|
| 阻格导致 ETA 失真 | 开放 | **关闭**（F1） |
| 重建抖动循环 | 开放 | **关闭**（F7 日零随机 + 幂等闸） |
| 日内意外义务 | 开放 | **关闭**（F7：义务只来自我方决策，场景变体覆盖） |
| 库容×市场耦合 | 对策=断言 | **强化**（F6/F9：EOD 预算 + 卖出排程前置） |
| 家区指派退化 | 未知 | **部分修正**（实时位置 + 跨区惩罚 + 连续性；固定象限×cls LPT 分区仍开放） |
| 求解质量次优 | 开放 | 保持开放（M3 影子门 + 消融） |
| 宽限期误用导致连锁死 | 新识别 | D2 只在显式赤字时动用，且动用即记 deficit（策略层次日必补） |

## 7. 里程碑（范围裁决后修订）

| 里程碑 | 内容 | 门禁 |
|---|---|---|
| M1 记分卡 | telemetry 已接入任务/容量/路线 trace；容量定律采用 3.3 回合/单位、0.89 利用率 | 完成；仍以所属战役 metrics 做线上裁决 |
| M2 任务包 | `_build_mission`/`_enrich_mission_tasks`、任务 schema、D1 分诊、EOD 投影和事件 | 完成；聚焦测试覆盖 |
| M3 求解器 | current-roster、实时位置/时钟、共享 PICKUP 预留、累计 ETA、有限重解 | 完成；效率最优性仍开放 |
| M4 执行切换 | 四层路径已成为 LIVE 唯一调度路径；旧开关和 v72 fallback 已删除 | 完成；本地回归通过 |
| M5 冻结清理 | 删除过渡代码，保留 deterministic package、identity 和 smoke 契约 | 完成；新候选仍须线上公共局验证 |

## 8. 验证状态（2026-09-03，audit-repairs 波后）

- 调度器聚焦回归：`test_scheduler_w2.py`，`29 passed`。
- 全量软件回归：`python -m pytest workspace/kaggriculture/software/tests -q`，`821 passed, 2 skipped`。
- 确定性提交包：`build.py --check` 通过，layout `pkg.1`；当前包 SHA-256 为
  `f4bffb0563e80b0e53f48f11a9baba7b22493b686e947d7f9d30a98423087c0d`。
- candidate identity 检查通过；working 状态仍为 development，未据此宣称线上强度或晋级。
- 审计修复（2026-09-03）：FERTILIZE 重施死区（`_stop_done` 判据 day 相对化——引擎字段是
  绝对截止日且过期不重置；quickwin 4 种子 A/B +6.13%，escapes/overflow 0/0，compare
  pass）；`replan_repeat` 遥测；`_d29_template` 死代码删除；过时注释纠偏（mission 头注/
  MK-4 干扰/V-T3 水窗引擎语义）。

## 9. 规模与关联

重构净 ~800 行（不再有平移折扣）；关联 phase_branch_plan.md（L1）、
opp_supply_observer_design.md v2（并行线，无耦合）。
