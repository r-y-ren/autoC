# M1 预测器可行性预演（dff20b-5，2026-10-03）

混合系 M1「BC 蒸馏」立项前的可行性预演：**纯研究，不碰产线、不碰提交**。

## 任务定义（主任务）

**下一拍市场价格预测**：输入 t 拍可观察的公开状态 16 拍窗口
（9 品价格 / 库存偏差 / 推断净成交量 / 城镇排水向量 / 商店数 / 双方金钱 / 时间相位，43 维），
输出 t+1 拍 9 品价格（等价于价格增量 delta = price[t+1] − price[t]）。

备选任务（对手麦流强度预测）不单独建模——WHEAT 大变动格专项读数作为其代理（见 evaluate.py `wheat_focus`）。

## 语料与数据集

- 来源：`fn_docs/hybrid/references/ext/fingerprint-scan/raw/ashok205-shards/`（ashok205 top10 归档，58 parquet，26,527 局，replay_json ~3.8G）。
- 划分：按 episode_id md5 哈希 %100 → 80/10/10 train/val/test，**同局不跨集**（防泄漏）。
- 限界：top10 语料的对手分布非全体（见报告"异常与限界"）。

## 回放步进约定（本目录脚本实现所依，已在 20 局上实证）

- `steps[t][pi].action` 是"产生了 observation[t]"的动作（act+1 约定，判别 5755:170）；
- `inv[t+1] = inv[t] + committed_trades(action@steps[t+1]) − drain(step=t)`；
- drain：`step%4==0` 每家已解锁商店排其单品（单品类店×2）；`step%12==0` 城中心全品各−1（除 FERTILIZER）
  ——区间取自回放 configuration（townShopSellInterval=4 / townCenterSellInterval=12，非引擎默认 24）；
- `price[t] = market_price(inv[t])`（引擎确定性定价；oracle_inv 实测 MAE≈0.0007 证实）；
- 版本注意：回放 module_version=1.32.2，与本地 1.32.7 缓存在 CARROT/TOMATO/EGG hinge 支有 ±1-2 差异，
  故引擎先验基线用**训练集标定的 inv→price 映射**而非硬编码公式；
- 净成交量特征 `net_comm[s] = inv[s] − inv[s−1] + drain(s−1)`：线上 t 拍可从公开库存轨迹直接推断，无泄漏；
  请求量 vs 推断 committed 的逐格一致率 94.9%（残差=死单/$1 地板/截断）。

## 文件

| 文件 | 作用 | 运行位置 |
|---|---|---|
| `prepare_data.py` | 58 parquet → 每局 (720×9) 价格/库存偏差/排水/净成交 + 商店数/金钱，按局 8:1:1 切分存 npy + manifest | 本机（/tmp/m1env：pyarrow orjson numpy） |
| `train_model.py` | LSTM 2×192（498K 参数）+ MLP 头，窗口 16，Huber(delta/base)，bf16，≤24min 墙钟 + early stop | 远程 WSL（kag_eval_venv, CUDA） |
| `evaluate.py` | test 三对照（persistence / 查表 / LSTM）+ engine_prior + oracle_inv；分品/体制/大变动拆解；失败案例 | 远程 WSL |
| `plot_loss.py` | loss 曲线 PNG（本机 matplotlib） | 本机 |

查表基线键：(品 9) × (库存桶 8，inv_dev/T 分位) × (排水态 3) × (时段桶 6) = 1296 格，训练集条件均值。

## 结果落盘（不在本目录）

- 结果 JSON：`fn_docs/hybrid/results/2026-10-03-m1-rehearsal.json`
- 报告：`fn_docs/hybrid/references/2026-10-03-m1-rehearsal.md`

## 数据/模型归宿

- 数据集 npy 在本目录 `data/`（不入 git，见 .gitignore）；远程副本 `wsl:~/m1_rehearsal/data/`（D14：远程只放数据/模型/训练产物）。
- 模型 ckpt 只在本目录 `runs/` 与远程 `~/m1_rehearsal/runs/`。
