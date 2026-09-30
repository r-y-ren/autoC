# 2026-09-30 Kaggle 频道第四轮扫查册（开源兑现窗口临近+终交潮泄出）——09-29 19:46Z 之后的公开增量

> 任务：扫 09-29 19:46Z（基线=2026-09-30-kaggle-sweep3.md）之后的 Kaggle 频道增量，找"可利用件"（重点：开源兑现核查/终交潮策略泄出/BUY5 族公开件/收官复盘）。窗口 **09-29 19:46Z → 09-30 05:20Z**（榜面快照 05:18:24Z；截止 09-30 23:59Z，余 ~19h）。
> 通道：kaggle CLI 2.2.4（kernels list 全量 dateRun/dateCreated + kernels pull 解包 + topics/topic-messages + leaderboard download + team-submissions + datasets list/files/download）+ 本地解包 diff（/tmp/scan7/，未入仓）。
> 纪律：逐条带来源 URL+抓取日期（均 **2026-09-30**）；自报标"自报"；我方解包/重算标"重算"；查不到写"未找到"。基线=sweep3+kaggle-channel-scan+github-sweep3。

---

## 〇、直接回答

**"有无新公开策略/可利用件？"——有 3 件硬货 + 1 个元信号。**
1. **georgymarin/kaggriculture-episodes 29.9GB 语料解封**（此前 403）：agents.csv+episode_features.csv+stream_hashes.csv+全量 replay parquet——**顶强终交件的逐局行为数据全部可取**（含 submission_id→team_id→final_bank 映射），这是本轮最大可利用件。
2. **官方 09-29 日包出包**（584 局/21.5GB，manifest v63）——终交潮前夜全量对局。
3. **haodou V91 "Patient Peak Hedge"**（09-30 03:07 run）：整件换回 V54"耐心清算"血统并**自报放弃镜像特化**——公开强手自己承认 V76 族微补丁在 clone-heavy 池失效，对焦窗/清算节奏选择是直接情报。
4. **元信号**：destbreso x-ray 日更 x 到 #1（M&M&P&Q sub 56679033）实测画像——**全局 ADAPTIVE、99.4% 变着、W105-L1、中位 +11,248**（见三）。

**开源兑现（重点①）仍未落地**：743993 仍 6 回复无新回复；Majkel1337/SpaTaro/tarosqrd2/akimaru/yaphellee/vadimvasilenko/monsaraida/ku0807/UMG/masspeaks/boey/matsu997 名下 kernels 全 "Not found"；DSM 三子/linkinpony/kurupical/proptiter 仅他题旧件；tetsutani 仍 5 件本题旧件（最新 demand-preserving 09-28 17:41 无新版）。**距截止 ~19h，兑现窗口=截止后**（与 GitHub 频道互证）。

## 一、kernels 增量对照（vs 19:46Z，dateRun 全量 200 件）

| 面 | 增量 | 判定 |
|---|---|---|
| 新 run | **7 件**（19:46Z 后）：adilshamim8 101（09-30 04:36）、kunaldesale2408 v1（03:58）、haodou092 V91（03:07）、farhanabidtech786 beginner-friendly（02:06）、destbreso x-ray（09-29 22:58）、ashok205 归档器（22:43）、georgymarin 2600-farms（22:13） | 7 新 run |
| 新建 kernel | dateCreated 全量翻页：09-29 12:00 后**仅 god-s-mode 19:05 一件**（=基线在册 v27 件）；**无新建件** | 未找到新建 |
| **haodou092 V89→V91**（重算 diff） | **整件换装**：V91=base85+zlib 内嵌 main.py 1,018,142B（SHA fd39dffa，"Kaggriculture v25 EXP-149"分层族），外皮明文自述"deliberate independent hedge……restores the patient capital and sale schedule from the historically strongest **V54 lineage**, whose **slower liquidation** produces a different market path against today's **clone-heavy pool**……accepts lower mirror specialization in exchange for less correlation with V90"。**G793 门/PET_CAFE/_s793/_r37 全部消失**（v89 有 v91 零命中）。自报：同 12 个梯子回放种子 5 胜、均 +899 币、避开 V76 重交线的异质对手崩盘；对 V76/cha22 两种子 smoke 略负；**双件对冲**（V90 与 V91 分开交比收敛） | **有增量（换血统+对冲战术）** |
| 3 新公开 notebook | adilshamim8/kaggriculture-101（教程故事型 15 cell，无策略值）；kunaldesale2408/kaggriculture-2026-v1（SUBMISSION/ARTICLE 双模式渲染壳，**无引擎无 payload**，dashboards 展示件）；farhanabidtech786/kaggriculture-beginner-friendly（**BL-MDgogo-10C4S-R0**："public-replay consensus route with generic execution guards"，自述**十二份公开回放行为重建**+公开盘口适配器改卖量，clone preemption 关闭——54KB 明文 main.py，重建路线非原创强件） | 1 件重建路线可读，余 2 件低值 |
| destbreso x-ray 22:58 新 run | 日更例行，但**产出 #1 实测 x-ray**（见三） | 有情报增量 |
| georgymarin 2600-farms 22:13 新 run | 其 403 的 kernel pull **恢复可取**（36 cell 全文到手）；内容=顶段 vs 中段指纹对照（种植物/买地日/班组规模）+ 个人报告模板；引用 destbreso **kaggriculture-benchmark-matchups 45k 对局 CC0**（resolved seeds）与 stream_hashes 血统法 | 可取回，分析基建 |
| votes | haodou 115、flexonafft 120、icefire 121、tetsutani 137 微动；**无爆款** | 常态 |

## 二、数据集增量（重点③）

1. **georgymarin/kaggriculture-episodes v?（09-30 00:43 重建，29.9GB）——403 解封**（https://www.kaggle.com/datasets/georgymamarin/kaggriculture-episodes ）：文件=episodes.csv（47.9MB 全对局台账）/**agents.csv**（28.3MB：episode_id×seat→submission_id→team_id→final_bank→rating_after，**顶强终交件 id 全映射**）/**episode_features.csv**（55.7MB：engine_version、peak_crew、total_hires、first_land_day、tiles_planted、五作物分项、全价格 min/max）/**stream_hashes.csv**（动作流 SHA 八切片 24/48/100/136/200/300/400/719，血统/"同一开局线"判定）/replays_2026-07…09h parquet（9 个分片 ~21GB，replay_json 全 720 步）/teams.csv/per_submission_coverage.csv。README 称"每晚定时重建"。
2. **官方日包 kaggle/kaggriculture-episodes-2026-09-29**（https://www.kaggle.com/datasets/kaggle/kaggriculture-episodes-2026-09-29 ，09-30 00:05 出包，584 局/21.5GB，12 个 34-40MB JSON）+ episodes-index v63（manifest.csv）。manifest 显示 09-29 top_avg_score 3036.3/median 2926.7（09-28：3033.2/2938.5，池面分位平稳）。
3. **daily_stats.csv**（georgy 件内）：09-29 ladder_games **1247**（09-28 3336）、teams_active **864**（1768）——**终交潮活跃对局腰斩**，replay_coverage 0.001（爬虫滞后，回放后补）。
4. destbreso/kaggriculture-benchmark-matchups（CC0，45k 对局 resolved seeds）为 2600-farms 引用件（本轮仅登记未下载）。

## 三、#1 实测画像（destbreso x-ray 09-29 22:58 run 输出，重算读取）

对 **M&M&P&Q sub 56679033**（榜一 3038.3，106 局）：W105-L1-T0、边际中位 **+11,248**、最差 −988；**GLOBAL ADAPTIVE**（99.4% 变着、首分叉 t=4、三通道全动）；0 镜像/0 同胞对局（78 个基因组）；宏观指纹：二象限 d6、care 364、herd COW10/SHEEP1/GOOSE8、d25-29 休耕 10、**搁浅金 0**、**floor sells 5**（≤$2 地板卖）、shed 满载 2 回合；工时结构 work 46.8%/carry 5.4%/move 43.2%/idle 4.6%；占用热图半分相关 r=+0.998（结构稳定非噪声）；**WARMING UP**（近 20 局 +3.28/局漂移，配对率 13 局/h）。= **#1 是全程变着的自适应体，非脚本回放；其对手池 78 组基因=高度异质**。

## 四、讨论区增量

1. **744458** "Using LLM's only to solve problems: Looking for a partner"（https://www.kaggle.com/competitions/kaggriculture/discussion/744458 ，09-29 21:48，14 回复 −5 票）：LLM 舰队组队闲聊；**唯一旁注**："With 19 hours remaining, all you can do honestly is upload that llm_tuned_to_max.tar.gz" + 一用户自述 harness 路线"maximum score around 3000 (didn't last long)"——尾日舆情=放弃深改、交卷了事。
2. **743993 开源帖：未找到新回复**（仍 6）；744277 队列帖已 RESOLVED；742856 评估帖 0 回复无新；**无新策略分享/开源兑现帖**。

## 五、榜面变动（19:46:18Z → 05:18:24Z，重算 CSV diff，队伍 10174→10190）

**前 30**：M&M&P&Q **3109.2 #1**（19:46 曾 −103 噪声，现回补 +129）；DECEM 2945.6 #2；Victor@Tufa 2928.7 **#3**（回补）；DSM 2914.8 #4（−68）；CDE 2890.4 #5；UMG/Vadim/Boey #6-8；TKNP 2840.4 #9；Majkel 2796.3 #15（04:52 仍在交）；matu997 2776.2 #22（大额收敛回稳）；TheEggman 2758.8 #25；**matsu997/seek inspiration 热度退潮回落**。前 30 名 09-29 20:00 后大量新交=终交潮收敛噪声持续，勿读死。

**同门带**：Georgy 2065.5→1967.8（#829，无新交纯漂移）；tetsu2131 1970.7→1860.6（23:50 新交）；Lynxx 1899.4→1791.1（09-27 后仍无交）；shiiin9 2036.4；**Alperen Aydın 2260.5 #329（+342 大额回补）**；statma 1752.8（05:13 新交）；**haodou 1396.5（03:08 交 V91，双件对冲未收敛显示）**。

**我方（renyxin 16784420）**：活跃对 **56687451=1720.6**（09-29 20:57 交，已收敛）+ **56697824=1131.8**（09-30 05:06 交 = C_final ref，**12 分钟未收敛**，786→1131 爬升中，40-70 局口径勿读死）；榜面取高 1720.6，#1628。

## 六、可利用件清单（复刻授权口径：Apache 件可署名移植/无许可件干净室）

| # | 件 | 许可 | 复刻价值 |
|---|---|---|---|
| 1 | **georgy 29.9GB 语料**（agents/stream_hashes/episode_features/replays parquet） | 数据集无 LICENSE 文件（自建爬取）→ **无许可件，干净室**（仅作观测/评测燃料不移植代码） | **最高**：顶强终交件行为数据+A1 画像语料+血统判定，直接喂我方结构轮对表 |
| 2 | **官方 09-29 日包**（584 局） | Kaggle 官方数据（竞赛条款） | 高：终交潮前夜全量对局，焦窗卖法对表 |
| 3 | **haodou V91（V54 血统慢清算）** | 其件明文 LICENSE.txt（Apache 系）→ 可署名移植 | **高（方向性）**：公开强手实证"clone-heavy 池下放弃镜像特化、改慢清算"——与我方 h14-22 焦窗快卖反向，须对表验证谁优；V91 内嵌 1.02MB 明文 main.py（EXP-149 分层族）可读 |
| 4 | **#1 x-ray 画像**（sub 56679033：ADAPTIVE/99.4% 变着/herd COW10 SHEEP1 GOOSE8/搁浅金 0/floor sells 5/WARMING UP +3.28） | 分析产出（destbreso 公开件） | 高（A1 画像）：#1 非脚本、全程变着、二象限 d6 开、重牛轻羊鹅；对我方对手建模=别指望抓脚本指纹 |
| 5 | farhanabidtech786 BL-MDgogo 公开回放重建路线（54KB 明文） | 无许可→干净室 | 中低：十二回放共识路线+盘口适配器=对手池"平均脸"参照 |
| 6 | destbreso benchmark-matchups 45k 对局 CC0 | CC0 | 中：评测对表基建（登记未取） |

## 七、来源清单（均 2026-09-30 抓取）

| 来源 URL | 通道 | 读数 |
|---|---|---|
| https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger | kernels pull 解包（base85+zlib 内嵌 1,018,142B，SHA fd39dffa；与 /tmp/scan_k/haodou_v89_main.py diff） | V91 换 V54 血统 |
| https://www.kaggle.com/datasets/georgymamarin/kaggriculture-episodes | datasets files/download（agents/episode_features/daily_stats/README） | 29.9GB 解封 |
| https://www.kaggle.com/datasets/kaggle/kaggriculture-episodes-2026-09-29 、/kaggriculture-episodes-index | datasets files/download manifest.csv | 584 局/v63 |
| https://www.kaggle.com/code/destbreso/x-ray-your-agent | kernels pull + kernels output（log 重算提取） | #1 实测画像 |
| https://www.kaggle.com/code/georgymarin/kaggriculture-what-2600-farms-do-differently 、/did-you-leave-a-better-medal-unsubmitted 、/how-safe-is-your-medal-spot-on-the-public-board | kernels pull | 2600-farms 可取回；后二件=跨赛 medal 方法学非本赛策略 |
| https://www.kaggle.com/code/adilshamim8/kaggriculture-101 、/kunaldesale2408/kaggriculture-2026-v1 、/farhanabidtech786/kaggriculture-beginner-friendly | kernels pull 全文 | 3 新公开件 |
| kernels 全量（dateRun 200/dateCreated 120）+ 顶强开号复验 20 账号 | CLI kernels list | 7 新 run/0 新建；顶强全未开号 |
| https://www.kaggle.com/competitions/kaggriculture/discussion/744458 、/743993 、/744277 | topics list + topic-messages | 743993 仍 6 |
| https://www.kaggle.com/competitions/kaggriculture/leaderboard （快照 2026-09-30T05:18:24 vs 09-29T19:46:18）+ team-submissions 16784420 | leaderboard download + CLI | 见五 |
| [前次] 2026-09-30-kaggle-sweep3.md、2026-09-29-kaggle-channel-scan.md | 见各篇 | 基线 |

## 八、限制

① V91 自报 5 胜/+899、"V76 崩盘"全部未复核；V91 内嵌件为多代层累叠源，V54"慢清算"具体参数无法从 1.02MB 源唯一钉版（仅 `_sell_lead` 提前一拍卖/`_dead_stock`/`_terminal_liquidation` 层名可见）；② georgy 语料 replay_coverage 09-29 仅 0.001（爬虫滞后），终交潮回放需等其补爬；agents.csv 的顶强 sub_id 为截至 00:43 快照，非终交定稿；③ x-ray #1 画像基于 106 局快照且 WARMING UP（+3.28/局漂移），读数随收敛变；④ 榜面大额 dScore（Alperen +342、M&M&P&Q +129 等）为收敛噪声非实力跳变；⑤ 我方 56697824=1131.8 为 12 分钟未收敛读数，C_final 以 40-70 局后为准；⑥ benchmark-matchups 45k 对局集仅登记未下载核验；⑦ 744458 为组队闲聊帖，无策略内容；⑧ 官方 09-30 日包按 00:05 规律将于 10-01 00:05 后出，本轮未覆盖。
