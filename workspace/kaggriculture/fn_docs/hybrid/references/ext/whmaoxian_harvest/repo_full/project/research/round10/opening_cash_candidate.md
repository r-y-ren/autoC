# 开盘资金缓冲：仅改一次等净量小麦交易的 V10 消融

冻结 V9 主源为 `experiments/round9_market_slack.py`，SHA-256 `6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3`。有效候选由 [build_round10_opening_cash_v2.py](../../build_round10_opening_cash_v2.py) 生成到 [round10_opening_cash_v2.py](../../experiments/round10_opening_cash_v2.py)，SHA-256 `2dd1f8a0ad6452cda35fd6b90423912e3bc38418ebef98bd876d8ead97021ba7`，Kaggle 入口 `round10_opening_cash_v2_agent`。编译时校验 V9 哈希，且已有候选文件不允许悄悄覆盖。末端包装以 V9 的**完整** `round9_slack_agent` 为父；首版文件 `round10_opening_cash.py` 误用了早期 `agent` 绑定，虽做过诊断但不能用于屏测或提交。

候选在 `observation.step == 0` 且完整 V9 返回的市场订单确为 `BUY_PRODUCT WHEAT 20 → SELL WHEAT 15` 时，替换为 `BUY 15 → SELL 10`。两队列均净得 5 单位小麦，不改物理动作、买种子订单或后续 V9 调度；如果开盘动作形状变化则原样返回。这是跨世界的一项可证伪的交易规模消融，不使用世界种子或对手身份。减小自买自卖规模可能减轻买卖价差和市场锁步影响，但对手同回合交易仍未知，**不保证**每场都留更多现金。

官方引擎单局诊断用公开 [112476879](https://www.kaggle.com/competitions/episodes/112476879/replay.json) 的对手动作带、公开种子及官方配置。V9 与固定动作带重现原局 `90848:107685`；v2 得 `120017:111697`。第 0 日末 V9 余额 1，v2 余额 8；第 1 日 01:00 V9 实得 1 名雇工，v2 实得 3 名；第 2 日 00:00 V9 仅余 1 牛，v2 两牛仍存；第 5 日末 V9 2 牛、606 余额，v2 4 牛、785 余额。若把原 V9 的 719 项观测原样喂给两个独立入口，动作差异**仅第 0 步**，验证包装没有改变晚期策略。完整诊断读数见 [opening_cash_v2_public_replay_smoke.json](opening_cash_v2_public_replay_smoke.json)。对手动作带在候选改变市场后不会响应，所以这一局只说明机制可发生，**不是可推广的胜率估计**。

下一步应由 Round 10 的开发世界双席位对多种现行强公开代理屏测，并按世界聚类比较获胜点、现金差、日 0/1 可用工人数及奶牛生存数。若仅少数开盘状态受益、另一些高分对手使价差反向，后续才设计利用当前公开报价、现金及下一日确定雇工需求的保守门槛；本候选只隔离改变成交量这一因子。确认/保留世界尚未接触。
