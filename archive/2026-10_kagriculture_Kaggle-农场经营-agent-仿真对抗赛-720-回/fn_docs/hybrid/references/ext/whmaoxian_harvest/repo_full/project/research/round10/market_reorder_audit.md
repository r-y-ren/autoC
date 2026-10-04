# Round 10：出售排序的固定目标审计

冻结基线是 `submissions/release_v9/main.py`，SHA256 `6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3`。本轮没有修改它。`_v44y_reorder` 位于该文件约 6121–6158 行，最后一次生产队列排序入口位于约 7717–7730 行。

## 第二次排序为什么能改变结果

V9 每次调用 `_v44y_reorder(obs, action)`，都把传入的己方 `orders` 同时当成假想对手 `opp`。设 `m(y | x)` 为“己方采用队列 `y`，假想对手采用队列 `x`”时的报价模型利润差，函数实际计算的是 `F(x) = argmax_y m(y | x)`。再调用一次算的是 `F(F(x))`，对手模型随之变了；这不是同一个目标函数的第二轮优化。因此一次、两次调用产生不同输出，不足以证明第二次更接近真实最优。

可重复的纯 SELL 反例在 `research/round10/reproduce_market_nonidempotence.py`。初始队列 `EGG×108, MILK×98, MELON×80`，市场库存分别为 `10134, 9992, 9978`，使用冻结 V9 的官方参数和其自身的 `_v44y_factor_margin`：

| 队列 | 以**初始**队列为假想对手时的模型利润差 |
| --- | ---: |
| 初始 `EGG, MILK, MELON` | 0 |
| 一次后 `MILK, MELON, EGG` | 15,263 |
| 两次后 `MELON, EGG, MILK` | 227 |

第一次已经穷举单个 3 单 SELL 块的六种排序。第二次换了对手队列，才选出在**原目标**下更差的排序。这是目标漂移的确定性反例；它不是线上真实对战反例。运行：`.venv/Scripts/python.exe research/round10/reproduce_market_nonidempotence.py`。

另外，`_v44y_factor_margin` 用己方 `projected_shed` 同时模拟两人的库存，并忽略对手私有库存、资金和容量限制；它只是代理目标。即使某个队列的代理利润差增加，也不代表能打败 DSM、Vadim 或任何未知提交。

## 有界联合搜索验证

隔离候选 `experiments/round10_exact_sell.py` 的 SHA256 为 `54aa112b1d005290e9a0ebefddf82e39d1f14a8e832cc87f49ebf3f5eef24c1e`。它保留 V9 的最终排序位置和假想对手模型，只把多个长度 2–6 的连续 SELL 块在**固定**对手队列下联合穷举，最多 720 个组合；超过预算回退原函数。订单数量、非 SELL 槽位和其他策略层不变。`build_round10_exact_sell.py` 校验 V9 哈希，若候选文件已存在只校验一致性，不覆盖。候选仍受上述对手未知和资金近似限制，不是完整市场博弈精确解。

官方 `kaggle-environments==1.32.7`、同一个预先固定的前 8 个 Round 10 development 世界、4 对手、双方席位共 64 场，全部 `DONE` 且无脚本错误。候选与 V9 的**每一场**终局分差完全相同，商店路径 0/64 不同：DSM 旧公开代理 10/16 胜，Frontier 13/16，Master 16/16，V9 自对战 1/16；总积分率均为 73.4375%。尽管候选搜索触发了 52 次多块局面，固定目标的联合优化没有带来可观察收益。赛程哈希见 `results/round10_exact_sell_screen.manifest.json`，逐局数据见同名前缀 `.jsonl`，成对比较见 `results/round10_exact_sell_screen_compare.json`。

**结论：不晋级。** 第二次排序的表面胜场来自变化后的代理对手假设；固定目标的联合搜索在本次开发样本没有改善。Round 10 confirmation 和 reserve 世界未使用。
