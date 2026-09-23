# 反射层配置空间（R4 空间定义文档）

真值：v48 深读档 modules/（v44.gold_floor / v23.policy_library /
v24.market_maker / scripts.v19_terminal）+ v48_hybrid/main.py
_V48_GOLD_CONFIG 参数转录；死价护栏为本管线新增保险层。

- 候选库件：10 件（2 路由 + 8 市场变体）
- 反射层开关面：5 轴 （clone_preempt、slot_reorder、market_maker、terminal_forced、dead_price_guard）
- 布尔基空间规模：10 × 2^5 = **320 候选**（全枚举=粗筛面）
- 阈值微轴：{"clone_streak_required": [24, 16], "dead_guard_ratio": [0.5, 0.65]}（缺省 {"clone_streak_required": 24, "dead_guard_ratio": 0.5}；精化扇出 ≤2，仅在最佳配置邻域展开，不进基空间乘法）
- v48 gold 常量（开关不改写部分）：{"clone_active_start": 160, "clone_detection_start": 48, "clone_distance_threshold": 2.0, "clone_maximum_batch": 10, "clone_phase_detector": false, "clone_veto_enabled": true, "clone_veto_first_shop": "BAKERY", "clone_veto_maximum_cows": 1, "clone_veto_maximum_geese": 0, "clone_veto_minimum_melons": 7, "clone_veto_minimum_sheep": 4, "clone_veto_minimum_wheat": 8, "clone_veto_step": 120}
- 稀疏惩罚：score = winrate − λ×启用模块数（λ 登记于账本；启用模块数=开关面 ON 计数，库件与阈值不计入）
- 候选 id："<件>#<掩码>"（位序 clone_preempt|slot_reorder|market_maker|terminal_forced|dead_price_guard）；全序确定（件序字典序，掩码二进制升序）

| 件 | 来源 |
|---|---|
| route:default | routes.json |
| route:fork_s73_e72 | routes.json |
| variant:cap_c120 | market_variants.json |
| variant:cap_c240 | market_variants.json |
| variant:scale_r0p75 | market_variants.json |
| variant:scale_r1p25 | market_variants.json |
| variant:shift_dm1 | market_variants.json |
| variant:shift_dm2 | market_variants.json |
| variant:shift_dp1 | market_variants.json |
| variant:shift_dp2 | market_variants.json |
