# 第 0 日末小麦种子不能安全转作雇工资金

针对零日交易机制报告指出的翌日 **4 元雇工门槛**，我单独检查了 V9 后段的 `BUY_SEED WHEAT`。可复核脚本 [audit_late_seed_liquidity.py](audit_late_seed_liquidity.py) 对冻结 V9 的 **41 条**生产路线逐一核验，逐步读数在 [late_seed_liquidity_audit.json](late_seed_liquidity_audit.json)。V9 SHA-256 仍是 `6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3`。

41 条路线在这一段完全相同：第 19 步买 1 粒小麦种子；第 20 步先种 1 处，再买 **2 粒**；第 21 步两名工人同时种 **2 处**；第 22–23 步没有新的购买；第 24 步请求雇 3 人。已公开的 [112476879 对局](https://www.kaggle.com/competitions/episodes/112476879/replay.json)中，第 20 步开局种子 1、执行后种子 2、现金 1；第 21 步恰好消耗两粒，日末余种子 0、现金 1。

官方引擎先检查一回合对同作物的种植请求总数，再执行农民/工人动作，**最后**才执行市场订单。如果请求数大于当时已有种子数，会把该作物在这一回合的**全部种植请求**改成 `PASS`，不是只少种一处。[官方实现](https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kaggriculture/kaggriculture.py) 对应本地安装的 `kaggriculture.py` 约 920–942 行。故第 20 步把购买从 2 减到 1 虽可多留 10 元、第 24 步有能力雇满 3 人，却会使第 21 步两处小麦**全部无法种植**；把第二粒推迟到第 21 步买也赶不上当回合种植。小麦种子与仓库中的小麦产品分开管理，此剪裁不会立刻减少 FEED 用的产品，但丢失未来两块作物的产出，可能继而损害喂养和现金循环。

结论：这两笔购买都不是可无损延期的“闲置资金”。不存在仅通过保留第 20 步一粒种子、同时保持既定 PLANT 和次日 FEED 的安全候选，因此**没有创建这项代码候选，也没有占用 Round 10 confirmation/reserve 赛程**。若要突破门槛，需要从可兑现库存、其他更早的投资或重新排程作物与劳工整体权衡，必须作为新策略另行验证。
