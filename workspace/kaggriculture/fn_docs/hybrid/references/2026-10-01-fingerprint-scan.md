# 2026-10-01 头部对手回放行为指纹判定（fingerprint-scan）

> 任务：对同门带/未知族高分队（Majkel1337、mtmr_s1、alperen、SpaTaro、shiiin9、tetsutani、DECEM 及 top10 其他队）做行为指纹判定，回答"排行榜上与我们策略相同/相似但分数更高的选手是谁"，重点裁定 mtmr_s1 与 alperen 的榜件是否与我们（磁带+订单簿卖流，haodou V82 血统）同族。
> 抓取/计算时窗：2026-09-30 18:04 – 18:45 UTC（本机 10-01 02:04–02:45）。榜分口径：公榜 CSV 快照 2026-09-30T17:41:44Z。
> 纪律：一切结论基于本次实抓数据；样本不足处明示；查不到写"未找到"。

---

## 0. 一句话结论

**与"我方策略相同/相似且分数更高"的对手分两层**：同血统（haodou 羊系开局磁带）更高分的有 **redblackbst #113/2508.5、pensukesan #213/2376.4、Driz Lo #58/2625.3、THIRD FARM CLUB #62/2611.8、Hello San Francisco #327/2236.7、kanno #486/2111.0、Terry Luo #607/2039.8**；同策略原型但**不同血统**（牛-牧场开局磁带+订单簿卖流）的是整个榜首带：M&M&P&Q #1、DECEM #2、DSM #4、UMG #6、Vadim Vasilenko #8、**mtmr_s1 #24**、Smackaveli #40、Azat Akhtyamov #36 等。**mtmr_s1 是"磁带+卖流"同原型但换开局族；alperen 是条件磁带+大批量脉冲卖流，不同卖法**（详见 §4）。

---

## 1. 数据通道（按优先序实抓结果）

| 通道 | 结果 | 说明 |
|---|---|---|
| a. ashok205 top10 回放归档 | **成功** | 真实 slug=`ashok205/kaggriculture-top10-replay-archive`（任务书给的 `top10-replay-dataset-archive` 403 系拼写错误）。3.96GB zip，2026-09-26 22:51 版，58 天（07-30→09-25）每日 top10 队及其对手共 26,527 局（parquet 分片，含完整 720 步 JSON）。来源 https://www.kaggle.com/datasets/ashok205/kaggriculture-top10-replay-archive |
| b. georgymarin(kaggressulture)-episodes | **未动用（不需要）** | 真实 slug=`georgymamarin/kaggriculture-episodes`（v29.9GB，09-30 00:43 版）。a+c+官方 replay 端点已覆盖全部目标队与我方对局，未下载。注意：该数据集 files/metadata 端点确为 403，但 download 可用（拼写正确时） |
| c. 官方日更 episodes | **09-28 期成功 / 09-29 期失败** | 09-29 期（584 局）下载 404——数据集空版本（发布失败，列表 size=0 佐证）；改拉 09-28 期（599 局，719MB zip）成功。来源 https://www.kaggle.com/datasets/kaggle/kaggriculture-episodes-2026-09-28 与 https://www.kaggle.com/datasets/kaggle/kaggriculture-episodes-2026-09-29 |
| 补充. 官方 replay 端点 | **成功** | 我方计分对逐局回放：`kaggle competitions episodes/replay`（C_final=56697824 得 118 局、S8=56708866 得 61 局，共 179 局） |

**覆盖核对**（局数=以该队为任意参赛者的局）：Majkel1337 3967、SpaTaro 3387、DECEM 993、mtmr_s1 662（实提 320）、Alperen Aydın 117（全提）、tetsu2131 10、shiiin9 1、renyxin 0（ashok 内）→179（官方端点）、DSM 2974、UMG 3108。共实提 16,411 局特征。

## 2. 方法与校准

- 特征（`fingerprint_scan.py`，逐局 720 步×2 玩家）：day0 前 8 步动作规范化（市场=类型×品类×量级分桶，农民=指令归并 PLANT/PLACE 参数）磁带签名；SELL：首卖步/单均量/订单数/时段三段占比/品类分布；BUY：BUILD 节奏（首 coop/pasture 步）、种子/动物/BUY_PRODUCT（订单簿买侧）强度；雇工/买地节奏；终局 reward。
- 磁带一致度 = 前 8 步"逐步众数稳定率"（每步取该队众数 token 串，各局命中率对 8 步平均）；另报 top 签名覆盖率。
- **校准说明**：任务书已知 Majkel"461 胜局 day0 磁带 93% 一致"——本次实抓全期 252 胜局 tape_m=0.53、09-18 后近窗 0.84、top 签名仅覆盖 0.62，即 Majkel 为**多路开局库+版本演化**，"93%"应为更窄时间窗/口径下数字，本次以实抓口径为准（不影响族判定：0.84 仍属磁带族）。
- 胜率口径注意：ashok 样本的对手主要是 top10（取样偏差），胜率≠榜分。

## 3. 指纹判定表

我方基准（C_final n=119 / S8 n=62，两者指纹几乎全同）：磁带稳定率 1.00/1.00；首卖 step 1（全场最早）；10.3 卖单/日；单均量 6.0；时段 0.19/0.31/0.49；BUY_PRODUCT 66.6 单/局；不建 coop；pasture step 8；卖品 FERTILIZER>WHEAT>MILK>STRAWBERRY>WOOL。day0 市场磁带：s1 `BUY_PRODUCT:WHEAT:3|SELL:WHEAT:2|BUY_SEED:WHEAT:1`，s2 `HIRE×5|COW:1|SHEEP:1`，s3–s6 静默，s7 `BUY_SEED:MELON:1`。

| 队（榜位/分） | 样本(时窗) | 族判定 | 与我方 C_final 相似度 | 画像（关键数） |
|---|---|---|---|---|
| **DECEM**（#2/2965.4） | 437（09-22~28） | **固定磁带族**（topsig 1.00） | **中**：磁带+连续小额卖流同原型；但磁带异族（牛系）、卖流密度 1.7×（17.4 单/日、量 3.6） | 牛-牧场开局：s1 `COW:1+SHEEP:3+BUY_PRODUCT:WHEAT:2`；首卖 s2；coop s227 |
| **Majkel1337**（#12/2812.7） | 351（09-18~28） | **磁带族（多路开局库）**（近窗 tape_m 0.84、topsig 0.62；全期 3 签名各 16-18%） | **中**：磁带原型+FERTILIZER 重仓+连续卖流相似；但开局库多路、首卖近版延迟到 **step 28**、卖量更小（4.3） | 牛系骨架（s2 PICKUP COW→s3 BUILD_PASTURE）但近窗 farmer 稳定率仅 0.66；bp 50；13.3 单/日 |
| **mtmr_s1**（#24/2765.0） | 320（09-19~28） | **固定磁带族（DECEM 同族）**（09-22 后 topsig 1.00） | **中**：同"磁带+订单簿卖流"原型；磁带与我方仅 2/8 步骨架同、血统为牛系 | **与 DECEM 磁带 7/8 步全等**（唯一差异 s5 多一笔 SELL:WHEAT:1）；首卖 s2；7.9 单/日、量 7.9；bp 37.8（≈我方一半）；coop s237 |
| Alperen Aydın（#263/2318.4） | 78（**09-01~03，新鲜度打折**） | **混合族：条件磁带（双路 78%/22%）+大批量脉冲卖流** | **低-中**：有磁带、买侧强度近我方（bp 70 vs 67）；但卖法为批次倾泻（p50 34.7/单 vs 我方 6.0）、首卖 s5 | coop 双峰 255/680 两模式；coop=680 模式（晚建+大批量卖，0.14/0.30/0.55）胜率 0.60，coop=255 模式 0.29——强形态=深后置大批量 |
| SpaTaro（#330/2232.7） | 295+228（09-18~23） | **反应式**（topsig 0.00-0.09，近 11 局胜率 0.18） | **低**：无磁带；卖流画像量级接近但订单簿买侧极重（bp 470≈我方 7×） | s2-s3 即密集 BUY_PRODUCT（CARROT/TOMATO/WHEAT）；WHEAT 卖品占比全场最高 |
| shiiin9（#716/1981.6） | **1**（09-25） | 磁带族（单局无法证一致度） | 低-中：卖后置最深（0.03/0.35/0.62）、545 单/局；方向与我方知其 Layer D 订单簿血统一致，样本不足 | 首卖 s2；bp 72；**样本=1 局，结论仅方向性** |
| tetsu2131/tetsutani（#916/1897.9） | **10**（09 月） | 磁带倾向（tape 0.85） | 中：深卖前瞻（0.08/0.35/0.57）与我方后段占比同向；bp 148 偏重买侧 | 首卖 s2；量 7.8；**样本 10 局** |
| 长尾：羊系簇（§5） | — | 固定磁带族（haodou 公件血统） | **高**（磁带逐步命中 0.63-0.88） | 即"同策略同血统更高分"名单 |

## 4. 专答：mtmr_s1 与 alperen 是否与我们同族？

**mtmr_s1（#24/2765.0）——同原型、不同血统，且榜件与 DECEM 同族。**
- 磁带：09-22 起完全固定（topsig 1.00）。其主磁带与 **DECEM（#2/2965.4）逐步 7/8 全等**：s1 买 `COW:1+SHEEP:3+BUY_PRODUCT:WHEAT:2`、s2 `SELL:WHEAT:1+HIRE×5+COW:1`、s3 `SELL:WHEAT:1`、s4 `SELL:WHEAT:1|BUY_PRODUCT:WHEAT:1`、s6 `BUY_SEED:MELON:1|BUY_PRODUCT:WHEAT:1`、s7 `BUY_SEED:MELON:1` 全同；唯一差异 s5 mtmr 多一笔 `SELL:WHEAT:1`（另有一处 PLACE 编码差异，无语义）。→ mtmr 榜件=DECEM 族磁带的近拷贝执行。
- 与我方 C_final 对比：同属"固定 day0 磁带 + 全程订单簿连续卖流"原型，但磁带内容异族（牛-牧场开局 vs 我方 haodou 羊拾取开局，stepwise 命中仅 0.247）。
- **最显著行为差异**：①开局我方 s1 即开卖（首卖 step 1，全场最早），mtmr 首卖 step 2 且开局重仓畜（1牛3羊 vs 我方 1牛1羊）；②mtmr 卖流更早段集中（early 0.27 vs 我方 0.19）、单量更大（7.9 vs 6.0）、密度更低（7.9 vs 10.3 单/日）；③买侧参与仅我方一半（bp 37.8 vs 66.6）；④迟建 coop（step 237 vs 我方不建）、早建 pasture（step 3 vs 我方 8）。同族内对照：DECEM 同磁带下卖流 17.4 单/日、量 3.6——mtmr 的 1000 分差距主要在卖流执行密度而非开局。

**Alperen Aydın（#263/2318.4）——不是同一卖法；条件磁带+大批量脉冲。**
- 磁带：两个开局签名（78%/22%）＝其公开件自述的 C9 条件开局（非 BAKERY 路线对倒）；tape_m 0.86。
- 卖流：**双峰**——55/78 局走"coop 延至 step 680+单均 34.7 大批量后置倾泻（0.13/0.30/0.59）"模式（样本内胜率 0.60），其余走"早 coop 255+微卖 6.1"模式（胜率 0.29）。与其 market-rhythm 件 `_ADV_LOOK=24`（前瞻 24 拍把计划卖单拉前）自洽：队列空则倾、队列堵则等。
- 与我方差异：我方是**连续小额**（10.3 单/日×6.0 量、首卖 s1）；alperen 是**低频大批量**（14.6 单/日×23.1 量、首卖 s5、后置 0.55）。买侧强度近我方（bp 70 vs 67）。产品结构与我方最像（FERTILIZER>WHEAT>MILK>STRAW>WOOL 完全同序）——同生态位，不同执行。
- **警告**：其样本止于 09-03（此后未再遇到 top10 对手入档），而他 09-30 仍在提交；上表为其 09-01~03 榜件指纹，当前版可能有演化。

## 5. top10 其他队识别（本次聚类新知）

- **牛-牧场开局族统治榜首带**：对 DECEM 主磁带逐步命中率——Smackaveli #40 0.875、Azat Akhtyamov #36 0.850、Orbital Terraformer #66 0.749、Vadim Vasilenko #8 0.739、mtmr_s1 #24 0.728、🐚seek inspiration🐚 #42 0.699、tetsuya&yuanzhe&guoqi #19 0.675、UMG #6 0.610、DSM #4 0.559、M&M&P&Q #1 0.530。前 8 名至少 6 队为该族变体（DECEM 自身 0.79）。该族共同点：s1 重仓畜+首卖 s2+s7 MELON 种，差异在卖流密度与后续自适应。
- **haodou 羊系簇（与我方同血统）**：アルモンド 0.875（#1782/1647.9，低于我方）、pensukesan 0.750（#213）、kanno 0.750（#486）、carlos-tagosaku 0.750（#1430）、Terry Luo 0.742（#607）、redblackbst 0.729（#113）、Thomas Tschinkel 0.656（#2727，即公开件谱系 ahmed V55/56→Tschinkel 的榜上实体）、Hello San Francisco 0.662（#327）、Driz Lo 0.630（#58）、THIRD FARM CLUB 0.627（#62）。
- 其它型：Boey（tape_m 0.25 反应式市场+farmer 磁带 0.80、bp 1230 极重买侧）、Fourth Quadrant #5（bp 2518，纯订单簿做市型，磁带 0.875/1.00 但首卖 s3）、Victor Mercklé @ Tufa Labs（首卖 s97、后置 0.66 迟卖型）、Crop Dusta（tape 0.98 但首卖 s49 迟卖型）。

## 6. 对照组（我方）落位

- C_final（56697824，n=119）与 S8（56708866，n=62）指纹几乎全同（同 chassis）：磁带 1.00/1.00、首卖 s1、卖流 10.3 单/日、量 5.5-6.0、0.19/0.31/0.50、bp 66、无 coop、pasture s8。两份榜件以 episode 清单分离（官方端点逐局拉取，2 局 C_final×S8 内战已剔除口径歧义）。
- 在"磁带+连续卖流"原型内的定位：我方卖流密度（10.3）介于 mtmr（7.9）与 DECEM（17.4）之间，买侧强度（66.6）高于牛系簇全体（33-51）、低于 alperen（70）与 SpaTaro（470）。

## 7. 局限

1. alperen 样本 09-01~03、tetsu2131 n=10、shiiin9 n=1——结论分级已标注；shiiin9/tetsutani 若需定案须从 georgymarin 全榜补样（通道 b 本次未动用，30GB 可得性已验证）。
2. Majkel"93%"口径未复现（§2）；不影响族判定。
3. 胜率均为"对 top10 对手"取样偏差口径。
4. ashok 归档止于 09-25，09-26~28 由官方日更 09-28 期补（599 局），09-29 官方期发布失败（404）无数据。
5. "冰"（低价冰山单）无法从动作流直接判定，未做。

## 8. 来源与命令清单（全部 2026-09-30 18:04–18:45 UTC 实抓）

```
kaggle datasets download ashok205/kaggriculture-top10-replay-archive -p raw/ashok205-top10/      # 3.96GB zip
kaggle datasets download kaggle/kaggriculture-episodes-index -p raw/                              # manifest.csv（日更索引）
kaggle datasets download kaggle/kaggriculture-episodes-2026-09-29 -p raw/official-0929/           # 404 失败（空版本）
kaggle datasets download kaggle/kaggriculture-episodes-2026-09-28 -p raw/official-0928/           # 719MB zip → 20GB 599 局
kaggle competitions episodes 56697824 --format csv / 56708866 --format csv                        # 我方对局清单
kaggle competitions replay <episode_id> ×179                                                      # 我方逐局回放
```
- 数据集页：https://www.kaggle.com/datasets/ashok205/kaggriculture-top10-replay-archive （v2026-09-26 22:51）、https://www.kaggle.com/datasets/kaggle/kaggriculture-episodes-2026-09-28 、https://www.kaggle.com/datasets/kaggle/kaggriculture-episodes-index 、https://www.kaggle.com/datasets/georgymamarin/kaggriculture-episodes （未下载）
- 官方 replay/episodes 端点（kaggle CLI 2.2.4）；榜分快照 `ext/lb-20261001/`（2026-09-30T17:41:44Z）
- 计算：`fingerprint_scan.py`（特征）、`analyze_fingerprints.py`+`compare_analysis.py`（聚合/对比），产物 `feats-*.jsonl`、`teams-report.json`、`compare-report.json`（均在 `ext/fingerprint-scan/`）
- 复现 09-28 期解压：`unzip kaggriculture-episodes-2026-09-28.zip -d unzipped/`（本次为省盘已删解压件，zip 保留）

## 9. 落盘清单

- `ext/fingerprint-scan/raw/`：三通道原始数据（ashok zip+58 分片 3.8GB、官方 09-28 zip、我方 179 局回放、两 CSV 清单、下载日志）
- `ext/fingerprint-scan/`：脚本×3、teams-targets.txt、feats-*.jsonl×4、teams-report.json、compare-report.json、.venv（pyarrow/pandas/orjson）
- 本报告：`references/2026-10-01-fingerprint-scan.md`；INDEX.md 已登记
