实施范围严格限定为 phase_branch 的阶段/分支决策与其市场消费，不修改 `observer.py`、observer 逻辑或并行对话正在处理的文件。

1. 修正 `strategy.py` 的分支状态与阶段组装
   - 保留当前代码已验证的 P0-P5 日期边界，避免无依据地改动阶段时间窗；修复 d6 首次错过时永久写入 `None` 的问题：首次进入 P2 时补算五问并保存稳定的 `questions/c_branch`，同时记录实际检查日。
   - 将 B 分支显式写入阶段状态/plan（`B1/B2/B3`），保持 d1 分类冻结；B2 使用现有标准序列，不引入未经验证的大规模新 capex，B1 继续保留物种优先级，B3 输出有界的早期瓜探针配额而不是布尔“全禁购”。
   - 重写 d6 C 分支判定：C1 仅在五问全真时成立；C2 仅在 q1、q2、q5 和乳业存活且作物时序条件未满足时成立；其余统一 C3，移除当前“乳业不活时反而回退 C1”的错误兜底。q5 使用实际候选 VOLUME 计划的 crew/容量预算计算，使 C1/C2 在合理公开状态下可达，而不是固定按 12 手导致 q1 与 q5 矛盾。
   - 增加唯一的 C1/C2/C3 参数映射：C1 选择现有 `_VOLUME_PLAN`（仍受现金/曲线/rollout 等安全否决），C2 无条件选择现有 `_MIXED_PLAN`（熔断时仍由 DEFENSIVE 覆盖），C3 选择保守畜牧/DEFENSIVE 框架，确保 `c_branch` 不再只是标签。
   - 调整 d14 冻结顺序，在完成 C 分支映射和熔断覆盖后保存最终有效 mode/c_branch；P3+ 冻结守卫使用该最终快照，防止 C2 在 d14 注入后被错误记录成旧 DEFENSIVE。
   - 修正熔断寄存器：同一阶段触发后保持 active 到阶段结束；阶段切换时明确解除旧 active，下一阶段再次触发才增加计数，避免同阶段自动恢复和跨阶段泄漏。保留每阶段一次计数与畜群下降检测。
   - 让每日缓存只缓存 `_decide_mode` 的基础结果，阶段覆盖在每次规划时重新应用，保证当天后续回合的熔断/checkpoint 状态能生效；阶段层异常改为返回带 `stage` 的 DEFENSIVE 计划，不保留可能绕过保护的宽计划。
   - 将 d10 readiness 与 d22 快照整理成可供下游读取的 plan/state 字段；d22 在不触碰 observer 的前提下继续调用现有 `est_opp_held/est_opp_conf`，并生成稳定的 P4 clear tier。

2. 修正 `market.py` 的实际消费与容量账
   - 在 `_market_orders` 增加本回合 `reserved_units` 账本；土地按 25 单位、种子按批量单位、牲畜按每头 2 单位累计，所有后续 `_capacity_gate` 调用使用“当前资产 + 已排队增量”，覆盖开局买畜、普通买畜、土地、种子和同回合组合订单。保留现有现金/曲线/市场吸收门。
   - B3 改成 d3-d5 的小批量、总量有上限的 MELON probe；超过 probe 配额或离开窗口后不再追加，且不阻断草莓/小麦主线。把计划中的 MELON 上限真正接到 `_field_alloc` 和种子购买路径，避免计划与订单分叉。
   - SE 购买路径消费 plan 中的 d10 readiness（缺失该字段的直接单元调用保持兼容），同时保留实时现金、容量和现金安全门。
   - 抽出共享的 P4 清仓 tier 判断，让 `_sell_overrides` 与 `_sell_plan_dawn` 优先消费 d22 保存的快照/tier；没有快照时继续使用现有实时估计作为兼容回退。仅调用已有 observer API，不编辑 observer 实现。

3. 更新 phase_branch 回归测试
   - 在 `test_landing_w1.py`/`test_branch_w2.py` 修正被旧错误行为钉死的断言：C1/C2/C3 精确分支、合理容量 q5、熔断同阶段锁存/跨阶段解除。
   - 新增覆盖：C 分支驱动不同 plan、B1/B2/B3 状态与 B3 d3-d5 probe、买后容量不越界、错过 d6 的补算、d14 保存最终 mode、d10 readiness 被 SE 消费、d22 tier 被 P4 清仓消费、阶段异常 fail-closed，以及跨日/跨阶段 plan 状态隔离。
   - 测试 fixture 只清理 phase_branch/市场计划的进程内状态；不改 observer 测试内容或 observer 全局实现。

4. 验证与边界检查
   - 先运行 phase_branch 相关的定向测试，再运行 `workspace/kaggriculture/software` 全量 pytest；处理由新契约暴露的直接回归，但不改动 observer 并行变更。
   - 运行语法/导入检查，检查最终 diff 仅包含 strategy/market 及 phase_branch 测试（必要时不改 README/规范文档），确认没有触碰 `observer.py`。