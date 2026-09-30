# 2026-10-01 羊系带内深切：+240~830 分增量来自哪个行为面（band-deepcut）

> 任务：对 7 支同血统（haodou 羊系，day0 磁带一致度 0.63-0.75）且榜分高于我方 C_final（1796.2）的队，复用 fingerprint-scan 的原始回放与特征管线，逐队计算同一套行为参数，排出"参数 vs 榜分"梯度，回答"最优秀那几位必然有可参考与改进之处——增量在哪个行为面"。
> 计算时窗：2026-10-01（本机）。榜分口径：公榜快照 2026-09-30T17:41:44Z。纪律：一切结论基于本次实抓数据；局数不足处明示。

---

## 0. 一句话结论

**带内没有单一连续参数随榜分单调；增量是三级台阶，每级对应一个离散行为面**：
① mid-band（kanno/Terry Luo/pensukesan/HSf，+240~580）：磁带与我们几乎全同，只是把 **day0 的 WHEAT 订单簿做市单加重**（买 6-25u/卖 26-50u+ vs 我方 6-10u/3-5u）并切换成 **bulk 挂单+末日倾泻**（单均 184-208u、末日单均 660-693u、后 10 日挂 82-86K 单位 vs 我方 1,036）；
② redblackbst（+712）：回到我们的连续小额节奏但找到 **TOMATO 微单引擎**（qty-1×~370 单/局的高值品滴灌，TOMATO 占卖单 35%，全带独一家）；
③ Driz Lo / THIRD FARM CLUB（+815~829）：**开局磁带整体重构 + 我们没有的第二经济线**——TFC 上 GOOSE/EGG 线（EGG 卖份 14% vs 全带 2-7%）、种子多元化（WHEAT 39% vs 全带 63-79%）、买侧砍到 1/3（bp 20.7）、day0 即完成畜舍-落位-喂-护理链，后 1/3 局钱增益全场最高（@480→719 +60.0K vs 我方 +48.8K）；Driz Lo 则是 MELON 重仓 + 后段巨量倾泻（后段挂单 9,382u，9× 我方）+（旧版）coop。**带内唯二建过 coop 的就是榜 1-2 名**（Spearman +0.809）；且**磁带偏离我们越远，榜分越高**（hit vs 我方 -0.564：Driz/TFC 0.63 最高分，アルモンド 0.875 最低分）。

---

## 1. 数据与局数（诚实口径）

| 队 | 局数（玩家记录） | 时窗 | 状态 |
|---|---|---|---|
| Driz Lo | 205 | 08-31~09-19 | 充足；窗口内换版（coop 版→无 coop 版，见 §6） |
| THIRD FARM CLUB | 179 | 09-11~09-25 | 充足、最新鲜 |
| redblackbst | 134 | 08-27~09-15 | 充足；末窗收紧（单均 27.7→14.4） |
| pensukesan | 82 | 09-09~09-10 | 充足，但仅 2 天快照 |
| Hello San Francisco | **27** | 08-09~09-10 | **<30，方向性**；8 月/9 月两版差异大（单均 7.4→153.5） |
| kanno | 159 | 09-09~09-10 | 充足，仅 2 天快照 |
| Terry Luo | 61 | 08-25~09-11 | 尚可 |
| renyxin（C_final 56697824） | 119（≈118 局） | 09-30（最新鲜） | S8 61 局指纹与 C_final 几乎全同（fingerprint-scan §6），本报告不重复拆 |
| 低分参照 carlos-tagosaku/アルモンド/Thomas Tschinkel | 43/35/233 | — | 梯度锚点 |

- 来源：全部复用 `ext/fingerprint-scan/raw/`（ashok205 top10 归档 3.8GB 分片 + 我方官方端点 179 局回放），新提取脚本 `ext/fingerprint-scan/band_extract.py`（day0_24 全日磁带、30 日分日卖流、终局段细粒度、钱轨迹检查点），产物 `ext/fingerprint-scan/band-analysis/feats-band.jsonl`（1,128 局）+ `feats-renyxin-band.jsonl`（179 局）。
- 取样偏差警告：带内队的局是"与 top10 交手"才入档，**终局钱中位与胜率均为此偏差口径**，不与榜分线性挂钩；梯度只用行为参数本身。
- 时效警告：带内数据止于 09-25（TFC）至 09-10（kanno/pensukesan），与 09-30 榜分有 1-3 周空窗，各队终版可能再演化。

## 2. 梯度表（全参数见 `ext/fingerprint-scan/band-analysis/gradient-table.md/.csv`）

| 队 | 榜分 | Δ我方 | 磁带命中 | 首卖 | 单/日 | 单均量 | 前/中/后 | bp | coop%(步) | 末日单均 | 终局钱中位 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Driz Lo | 2625.3 | +829 | 0.629 | s31 | 9.2 | 28.0 | .17/.34/.49 | 67.6 | 0.50(255) | 244 | 85,464 |
| THIRD FARM CLUB | 2611.8 | +816 | 0.626 | s26 | 8.5 | 9.6 | .23/.28/.49 | **21.8** | 0.12(251) | 35 | **109,306** |
| redblackbst | 2508.5 | +712 | 0.729 | s1 | **21.3** | 21.0 | .11/.27/.63 | 62.9 | 0.01(421) | 36 | 96,194 |
| pensukesan | 2376.4 | +580 | 0.750 | s1 | 16.6 | 183.9 | .11/.23/.66 | 68.3 | 0 | 660 | 96,189 |
| Hello San Francisco | 2236.7 | +440 | 0.653 | s2 | 12.2 | 83.2 | .09/.28/.63 | 97.2 | 0 | 529 | 86,652 |
| kanno | 2111.0 | +315 | 0.750 | s1 | 15.5 | 194.6 | .12/.23/.65 | 62.5 | 0 | 693 | 91,109 |
| Terry Luo | 2039.8 | +244 | 0.742 | s1 | 15.5 | 189.2 | .12/.23/.65 | 62.3 | 0 | 665 | 98,572 |
| **renyxin C_final** | 1796.2 | 0 | — | s1 | 10.3 | **6.0** | .19/.31/.49 | 66.6 | 0 | **7.3** | 95,981 |
| （参照）carlos-tagosaku 1724.2 / アルモンド 1647.9 / Tschinkel 1379.4 | | | 0.75/0.875/0.671 | s1/s31/s2 | 14.4/16.6/9.3 | 208/192/42 | 全部后段 .60-.66 | 67/80/74 | 全 0 | 671/684/395 | 98,017/102,875/89,959 |

**单调性检验（Spearman，n=11）**：coop 建局率 **+0.809**（唯一强项，但本质二值——只有榜 1-2 有）；磁带命中 **-0.564**（离我们的磁带越远分越高）；单均量 -0.427（bulk 巨单在中段不涨分，头部反而回归小-中单）；前段卖占比 +0.418 / 后段 -0.418；后段挂单量 -0.382；bp -0.336；终局钱中位 -0.127（不解释榜分）；雇工总数（267-283）、动物买序（~12 单）、pasture 步（s8）、买地块数（2.0-2.4，首块 ~s151）**全带同构，零区分度**。

## 3. 最优秀三队的独特面（带内低分队含我方都没有的行为）

**THIRD FARM CLUB（#62，带内 h2h 最强：3-0 Driz Lo、2-0 redblackbst）**
1. **GOOSE/EGG 第二经济线**：GOOSE 占动物买序 25%（全带其余 2-13%），EGG 占卖单 14%（其余 2-7%）——在羊-麦底盘上加了一条别人没有的产线。
2. **种子多元化**：WHEAT 39%/STRAWBERRY 32%/CARROT 17%/MELON 11%（其余队 WHEAT 单一文化 63-79%，我方 ~66% 种植笔数 WHEAT）。
3. **买侧几乎关闭**：bp 21.8 单/局 = 全带 1/3（我方 66.6）——不做订单簿买侧，省下的现金全部转入生产资料。
4. **day0 农民微编排重写**（hit_f 仅 0.246）：s1 `BUILD_PASTURE` → s2 `PICKUP WHEAT` → s3 `PICKUP SHEEP` → s4 `PLACE SHEEP` → s5 `FEED` → s6 `CARE`——day0 内跑完"建舍-落位-喂-护理"链（我方 s8 才建舍、day0 无 FEED/CARE）；畜群当天就开始产出。
5. **小而连续的卖流 + 最强后段抽血**：单均 9.6u、8.5 单/日、末日单均 35u（无倾泻），但 @480→719 钱增益 **+60.0K**（我方 +48.8K、Driz +36.2K）；@120 仅 59（day0-5 不赚订单簿快钱，纯产能建设）。
6. coop：现版（09-22~25）仍 7-13% 局在 s251 条件建。

**Driz Lo（#58）**
1. **后段巨量倾泻**：后 10 日挂单 9,382u（9× 我方 1,036），末日 27.6 单×244u；最终版单均 71u。
2. **MELON 重仓 + FERTILIZER 重仓**：s2 一次性 `BUY_SEED:WHEAT:11-25 + BUY_SEED:MELON:11-25`（我方 s7 只买 1-2u MELON）；FERTILIZER 占卖单 36.9%（带内最高）。
3. **首卖推迟到 s31**：day0-day1 完全不碰卖侧（钱@120=194 vs 我方 672——放弃早期订单簿收入换产能）。
4. coop：08-31/09-01 版 57-67% 局在 s255 建；09-16 版 0/21 已弃——**coop 是其实验过并（暂时）撤掉的面**。

**redblackbst（#113）**
1. **TOMATO 微单引擎（全带独有）**：TOMATO 占卖单 34.6%，形态为 **qty-1 的微挂单 ~370 次/局**（实抓单局验证：367 笔 `SELL TOMATO 1`）；这直接解释其 21-25 单/日的极端密度与小单均。TOMATO 种子仅 5 笔/局（来源疑为雇工农民自种/野生收获，harvest 29 次/局）。
2. **保持我们的 s1 现货 churn 但加重**：`BUY_PRODUCT:WHEAT:11-25×2 + SELL:WHEAT:26-50`（我方 6-10/3-5）。
3. 终版收紧：单均 27.7→14.4、密度 19.2→24.7 单/日——向"更密更小"方向迭代。
4. coop 仅 1% 局（s421，罕见条件触发）。

## 4. 磁带不一致的那 25-37% 步是什么（直接可抄的改进候选）

我方 C_final 众数磁带：s1 `BUY_PRODUCT:WHEAT:6-10 | SELL:WHEAT:3-5 | BUY_SEED:WHEAT:1-2`；s2 `HIRE×5|COW:1|SHEEP:1`；s4 PICKUP SHEEP；s5 PICKUP WHEAT；s7 `BUY_SEED:MELON:1-2`；s3/s6 静默。分叉步全部集中在 **s1、s2、s7（市场侧）**，无一队改动 s0/s3/s4/s5/s6 与 HIRE×5+牛羊骨架：

| 队 | 分叉步 | 具体内容（vs 我方） |
|---|---|---|
| kanno/pensukesan/Terry Luo/carlos | s1,s2 | s1：WHEAT 买返加码（两笔 6-25u）+首卖放大（26-50 甚至 >50u），**砍掉 1-2u 小麦种子单**；s2：加前缀 `SELL:WHEAT:11-25 + BUY_PRODUCT:WHEAT:3-5` 再接原雇工块（churn 多滚一拍）。农民侧与我方几乎全同（kanno/pensukesan/carlos 命中 1.00、Terry Luo 0.94） |
| redblackbst | s1,s2 | 同上型（s1 买 11-25u×2、卖 26-50u），量桶略小 |
| Hello SF | s1,s2,s7 | TFC 型压缩单（见下）+s2 加 churn 前缀；s7 无 MELON |
| Driz Lo | s1,s2,s7 | s1 **清空**（不碰市场）；s2 一次性 `BUY_PRODUCT:WHEAT:3-5 + BUY_SEED:WHEAT:11-25 + BUY_SEED:MELON:11-25`+雇工块；s7 不再买 MELON |
| THIRD FARM CLUB | s1,s2,s7 | **全部压进 s1 大合并单**：`BUY_PRODUCT:WHEAT:3-5 + HIRE×5 + SHEEP:1 + COW:2 + BUY_SEED:MELON:6-10 + BUY_SEED:WHEAT:11-25`，且农民 s1 即 `BUILD_PASTURE`；s2-s7 市场全静默 |
| （参照）アルモンド | 仅 s1 | 只把三笔缩成一笔 `BUY_PRODUCT:WHEAT:3-5`（其余与我方 100% 同，农民侧亦同）——改得最少、分也最低，反证"只贴磁带没用" |

归纳：**不一致步 = 开局订单簿做市强度（量桶 2-3 → 4-6）+ 种子/牲畜前置量（1-2u → 6-25u、COW/SHEEP 各 1 → COW:2/SHEEP:2）+ 编排时机（压缩进 s1 或推迟到 s2）**；没有人改 PICKUP 序列、雇工规模、牛羊骨架、day0 内建 pasture 本身（只有 TFC 提前到 s1、HSf s5）。coop 时点上 mid-band 全 0%，唯头部两强启用过（§3）。

## 5. 直接交手记录（h2h）

- **我方 179 局中无任何一局与 7 队交手**（对手清单全查，无带内队）——"我方 vs 带内"无实测 h2h。
- 带内互殴（样本小，方向性）：
  - **TFC 3-0 Driz Lo**（09-16，margin 4,181/5,774/6,404）；**TFC 2-0 redblackbst**（09-12，3,821/11,541）；TFC 1-0 Tschinkel（12,314）、1-0 carlos（14,814）→ 带内 h2h 王座。
  - redblackbst 3-0 kanno（4,260/5,676/6,300）。
  - kanno 7-2 pensukesan（8 局 margin<3.1K，贴身）；Terry Luo 3-2 kanno、1-1 pensukesan、1-0 redblackbst（唯一一局 margin 43K 的异常局，redblackbst 得分 67K 疑似超时/事故）。
  - h2h 层级 TFC > Driz Lo ≈ redblackbst > kanno > Terry Luo ≈ pensukesan，与榜分序一致（除 Terry Luo 的单局爆冷）。
- 对精英队胜率（取样偏差口径）：TFC 41/161（25%，对 DECEM 9/27、Vadim 9/26，对 DSM 0/19、Majkel 1/15）、redblackbst 7/25、kanno 6/22、Driz Lo 1/12（旧窗为主）。

## 6. 样本量与置信度声明

1. 结论主表（§2/§4）：Driz Lo/TFC/redblackbst/kanno/Terry Luo/pensukesan 六队 n=61-205，参数为窗口中位/均值，**置信中-高**；Hello SF n=27 且跨两版，**方向性**；低分参照 アルモンド 35、carlos 43 为方向性锚点。
2. kanno/pensukesan 仅 09-09~10 两天快照（他们只有冲进 top10 短暂入档），无法排除此前/此后换版。
3. 带内数据止 09-25，距 09-30 榜分快照 1-3 周；Driz Lo/HSf/redblackbst 窗口内确认换过版（§梯度表表 2），终版行为以"最后 1/3 窗口"列为准。
4. h2h 每对 1-9 局，**全部仅方向性**；Terry Luo>redblackbst 的 43K margin 局为异常值。
5. 终局钱中位/胜率为"对 top10 对手"偏差口径，不能与榜分直接换算。
6. 我方基准为 09-30 最新鲜数据（C_final 119 条玩家记录）。

## 7. 可参考改进候选（按证据强度排序）

1. **后段挂单规模/密度**（mid-band 全体 + Driz/redblackbst 佐证）：我方后 10 日挂 1,036u、末日单均 7.3u；带内同行 8.9K-86K/660-693u。TFC 证明不倾泻也能把 @480→719 增益从 +48.8K 提到 +60.0K（小单连续+品类多元）。
2. **day0 市场单加重**（mid-band 与我方仅有的差异，即可解释 +244~580 的主体）：买返 6-10→11-25u、首卖 3-5→26-50u、s2 追加一拍 churn、砍 1-2u 种子小单。
3. **TOMATO 微单引擎**（redblackbst 独有面，+712）：高值品 qty-1 滴灌式挂单 ~370 单/局。
4. **GOOSE/EGG 线 + 种子多元化 + 买侧减负**（TFC 独有组合，+816）：bp 66→~20，EGG 目标卖份 14%，种子 WHEAT 占比 39%。
5. **day0 畜群即刻运转**（TFC）：pasture 建到 s1、PLACE/FEED/CARE 在 day0 内完成（我方 s8 建舍后即静默）。
6. **coop**：带内唯二用过 coop 的队占榜 1-2；mid-band 0%。Driz Lo 用过又撤，TFC 条件启用——是值得单独 ablation 的设施，非无脑上。

## 8. 来源与命令

- 原始数据：`ext/fingerprint-scan/raw/`（ashok205 top10 归档、我方官方端点回放、episodes CSV、榜分快照 `ext/lb-20261001/`，均为 2026-09-30 实抓，见 `2026-10-01-fingerprint-scan.md` §8）。
- 本次计算：`ext/fingerprint-scan/band_extract.py`（parquet/json 两模式重提取）→ `band-analysis/feats-band.jsonl`(1,128 局)、`feats-renyxin-band.jsonl`(179 局)；`band-analysis/band_analysis.py` → `band-analysis/band-report.json`（梯度/分叉/h2h/漂移全套）+ `band-analysis/gradient-table.md/.csv`（表与图数据：30 日卖流曲线、钱轨迹、品类结构）。
- 复现：`cd ext/fingerprint-scan && .venv/bin/python band_extract.py json && .venv/bin/python band_extract.py parquet && cd band-analysis && ../.venv/bin/python band_analysis.py`

## 9. 落盘清单

- `ext/fingerprint-scan/band-analysis/`：band_extract.py、band_analysis.py、feats-band.jsonl、feats-renyxin-band.jsonl、band-report.json、gradient-table.md、gradient-table.csv
- 本报告：`references/2026-10-01-band-deepcut.md`；INDEX.md 已登记
