# v48 纯件协调规划机制深读（fn-analyze 子代理产物）

日期：2026-09-22。对象：`workspace/kaggriculture/fn_work/legacy_software/kaggle_simulations/opponents/v48_main.py`（107,008B，sha256 前缀 dadee25a，已核实）。解码产物：`/tmp/v48coord/modules/`（12 模块）与 `/tmp/v48coord/routes.json`（6×719 磁带）。只读分析，未改仓库。
行号引用 = 解码后模块内行号（与 digest `public-bot-reverse-eng-20260920.md` 约定一致）。

## 1. 磁带生成机制（结论：离线轨迹挖掘+编辑拼接，运行件内无生成算法）

- `scripts.v21_route_memory_search:L4-8` 仅 296B：`replay_policy(actions)` 逐字回放 `actions[step]`。**不是搜索器，是播放器**。"route memory search" 的搜索发生在作者的离线管线，未随包发布。
- 代码内血统证据：
  - `v48/fast_route_router.py:L1-8` docstring："real **fast-climber trajectories**"；"**Kaileh57 train-only** YARN continuation at step 88"；"**taiseiu train-only** continuation at step 120"；"later YARN branches retain the **validated v44** continuations"。
  - `v44/gold_floor.py:L48-50`：bakery_capital = "learned from a **public route** whose complete action prefix equals the default through this decision point"。
  - `v19_terminal.py:L4`："wrap v18, a **current-meta medoid**, or another public control"——default 骨干出自当前 meta 的 medoid 谱系。
  - `v23/planner.py:L27`："**seed-grouped holdouts**"——离线验证协议（按种子分组的 train/holdout）。
- 磁带结构实测（routes.json）：
  - 嵌套前缀树：6 条共享前 88 步；default↔各路由首个差异步 = 88/120/153/185/216，与路由器决策步**逐一精确对齐**（`v23/policy_library.py:L26-35 shared_prefix_length` + `L154-164 RouteLibrary.__post_init__` 强制"共享前缀≥触发步"——前缀共享是设计不变量）。
  - 后缀内容实测：yarn_fast/yarn_second/yarn_third 是 3 条真正不同的轨迹（farmer 动作差 406-460 步，Kaileh57 家族）；**farm_fast 与 bakery_capital 的 farmer 动作与 default 逐字相同**（0/599、0/534 差异），仅 market 被改（farm_fast=肥料卖单 ±1-3 天时移+槽位交换；bakery_capital=153 步市场单重写）。即 6 磁带 = 1 条骨干走位脚本 + 3 条异家 YARN 续篇 + 2 个骨干的市场单编辑版。
- 动作编码：每步 `{farmer:[op], hands:[[op]×N], market:[[order]×≤10]}`；BUY/SELL/HIRE 全在 market 列表（10 单上限）；产线/劳动/卖时一体化编码在 719 元素数组里，产线与卖单在同一维序列中逐字排程。

## 2. 在线协调面（决策表）

`fast_route_router.route_event`（L58-94），仅在 `selected[seat]=="default"` 时评估（L139-144）→ 锁存，**每席至多一次切换**。锁存理由（gold_floor L186-188）："Re-evaluating the same coarse signature later could jump into a suffix after its state has already diverged"；且单次切换=单一缝合点=磁带保持有效轨迹。

| 公开信号（全部来自 obs） | 步数条件 | 动作 |
|---|---|---|
| shops[0]==YARN_STORE | ≥88 | →yarn_fast |
| shops[0]==FARMERS_MARKET | ≥120 | →farm_fast |
| shops[1]==YARN_STORE 且 shops[0]∉{YARN,FARMERS} | ≥153 | →yarn_second |
| shops[2]==YARN_STORE 且 (shops[0],shops[1])∈{(BRUNCH_SPOT,PET_CAFE),(PET_CAFE,FARMERS_MARKET)} | ≥216 | →yarn_third |
| step==160（精确一步）且 shops[0]==BAKERY 且 shops[1]∈{PIZZA_SHOP} 且对手公开资产 cow≥3∧sheep≥2∧melon≥10∧goose≤0 | =160 | →bakery_capital（gold_floor L180-203；磁带 185 才分叉，160-184 切换为无害空转） |
| 其余 | — | 留 default |

- clone_veto（gold_floor L206-228）：仅在精确 step 120，shops[0]==BAKERY 且对手公开资产 sheep≥4∧cows≤1∧wheat≥8∧melon≥7∧goose≤0 → 永久置 clone_veto → 禁用抢卖（L526）。语义：识别"羊重开局"公开签名——形似克隆实为异Schedule，防克隆锁存过期误触发。
- v44→v48 演进：v44 `build_gold_floor_router`（gold_floor L706-716）每回合**评估全部子策略**；v48 只跑被选中的那个（router L148-150，"Exactly one child policy is evaluated per turn"，1 秒预算安全）。
- state_encoder（v23.state_encoder）：encode_state→StrategicState（需求/价/库存/双方 exposure/shed/种子）。运行期实际消费者只有 rebalance 制下的 `_demand_adjusted_score`（重排加权）；MPC/market_maker/phase detector 均休眠。路由器不消费它——路由器直读 step+town.unlocked_shops。

## 3. 三个闭环修正器

1. **CloneSellPreemption**（gold_floor L317-647）：检测=clone_distance（v19_terminal L153-187：|手数差|+3×|象限差|+Σ|11 类地块计数差|）≤2.0 连续 24 步（自 step 48）→ 一次性锁存。动作窗 [160,700)：读被选磁带 step+2 的计划 SELL，可卖量=min(计划−现有, projected_shed 余量, ≤10)，按 价格×数量 降序追加即卖。**due 账本**：欠债记在 due_step=step+2（L574-575）；到期步计划 SELL 按债扣减（L484-497）；未偿清滚动到 step+1（L500-503）；路由切换清债（L475-478）。纯时移、总量守恒、绝不增发。
2. **market_impact 槽位重排**（v22_market_impact L90-113 + policy_library L54-79）：score = q×(现价 − 加 q 后价)，用内置引擎 1.32.7 价格曲线精确副本；只对既有 SELL 槽位排序、不动非 SELL 位置、不改数量。rebalance 制加需求恢复权 ×(1+0.25×urgency)，urgency=min(1,恢复天数/10)。每回合施加。
3. **v19 终局**（router L155-161）：仅 step 718，`terminal_market(rule=collision, replace=True)` 全量替换卖单——卖空 projected_shed（含当步 DROP/PLACE 存货，v19_terminal L68-128）；排序分=(1+对手 exposure)×GLUT 权重×价格×log1p(量)（L214-219）。**注意：`monetizable_terminal_units`（717 单位强改）在 v48 驱动路径未接线**（只存在于 apply_overlay 消融包装，未被调用）——digest §4.4 的"717-718 两步机"在 v48 实际配置里只有 718 半步。
- 附加（环境闭环）：weed_repair（v22_weed_repair L26-122）——BUILD/PLANT 撞 WEED → 当步 DIG、下步重试、随后 ≤8 步回放该 actor 的磁带动作；逐 actor、market 不动。

## 4. 协调分层定量

- 离线（磁带内）：全部 719 步单位动作（farmer 活跃 716 步、hands 688 步）、全部市场单内容（default：332 个市场步，85 BUY + 580 SELL + 282 HIRE 单）——产线/劳动/卖时的完整排程全部离线定死。
- 在线可变决策点（719 步中）：路由切换 ≤1 次；克隆锁存 1 次；clone_veto 检查仅 step 120 一步；bakery 检查仅 step 160 一步；抢卖窗 [160,700) 540 步（有门控，default 磁带中实际具备 step+2 未来卖单的候选步 130 个，每步至多搬 10 单且欠债守恒）；槽位重排可作用于 138 个多 SELL 步（仅排序）；杂草修复仅随机碰撞时；终局 718 一步全量替换。
- **单位动作流在线自由度≈0%（除杂草事务修复）；市场流内容离线、在线只做排序/时移/末步替换**。粗算：719 步中在线实质可变 ≤ 1+1+1+1+~130(受限于门控)+1 ≈ 135/719 ≈ 19% 的步"可能被触碰"，但其中量的改变（时移）受守恒约束、排序不改变集合——**决策语义上的在线占比 <5%，且全部是"窄修正"而非"再规划"**。

## 5. 横向证据（opensource-bot-hunt / fresh-sweep digests）

- island-ga（MIT）：同一 construction plan，录像逐字重放 147.3k vs 重写 dispatcher 重执行 72.8k（恢复 0.49）——"走位编排值一半"，直接外证 v48 逐字回放走位磁带的合理性；"94% 座位 turn 24 前共享同一开局、score>950 是 scripted continent、计划偏差中位数 0.2%"——天梯顶部本就是磁带大陆；island-ga 自身基因组（12 数+4 表）离线 GA 搜索 + CRN 种子纪律，作者保留搜出的 schedule 不公开（"value is highest exactly while it is fresh"）。
- 2945 Farm（thomastschinkel，141 票，2944.7）：架构="路线磁带回放器 + 反射层栈"，**磁带按城镇首批商店解锁选择**——与 v48 fast_route_router 的事件选带完全同构；每个反射层读公开观测改一类决策，层层包装——v48 三个修正器的家族形态。但其对当期 top-10 七队 0-36（day-10 前领先、day-11 后全输）——磁带+反射家族的已知天花板。V49 = V48 + 2945 的 7 个经济层，holdout 96/0/0（+2807±571）。

## 6. 可行性判断："直接参考其模块算法"能否得到"生成一季协调计划"的算法

**不能。** v48 交付件里不含任何计划生成算法：replay_policy 只有 8 行；挖轨迹（Kaileh57/taiseiu 的对局）、medoid 选择、市场单编辑、种子分组 holdout 验证、缝合与前缀强制——全部在作者离线管线，未随包发布；包内只有该管线的**验证工具**（shared_prefix_length/RouteLibrary）与运行期反射件。要参考"生成一季计划"的算法应看 island-ga（MIT，完整离线 GA 搜索管线）+ cppsim（Apache-2.0，24k 局/秒位精确引擎，搜索基座）。v48 可直接移植的是反射层算法（克隆距离/锁存/欠债账本抢卖、影响分槽位排序、终局市场、杂草事务修复）与路由决策表设计。

## 7. 最反直觉发现

1. **6 条磁带实为 1 条走位脚本**：farm_fast/bakery_capital 的 farmer 动作与 default 逐字相同（0 差异），只改市场单——"6 路由"里 4 条是同一条走位编排的变体；协调的核心资产是单一被验证的走位 choreography。
2. **越强的闭环越被关掉**：最大的模块 market_maker（29.6KB）编译在包里但 enabled=False；MPC、phase detector、exposure preempt、717 单位强改全部休眠——planner docstring 明说路由切换与 MPC "deliberately absent because their seed-grouped holdouts did not improve wins"。赢家配置是消融树上最稀疏的枝。
3. **抢卖是零和时移不是增产**：due 账本保证全季总卖出量与磁带恒等（失败卖单的债滚到下一步、路由切换清债），克隆局的收益完全来自"同一件货卖得更早"的价格曲线位置。
