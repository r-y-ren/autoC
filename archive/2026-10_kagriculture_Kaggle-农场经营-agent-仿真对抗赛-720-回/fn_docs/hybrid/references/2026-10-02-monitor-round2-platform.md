# 2026-10-02 监控二轮增量档（monitor-round2-platform）——监控首档后 6.5 小时窗口差分

> 抓取窗口 **2026-10-02 18:57–19:13 UTC**（=CST 10-03 02:57–03:13）；通道：GitHub REST（`gh api`，r-y-ren 鉴权）+ kaggle CLI 2.2.4 + HF 公开 API。范围=监控首档（`2026-10-02-monitor-baseline.md`，12:25–12:37Z 实抓）之后的**增量**；对照基线=首档快照 + 同日早间并行件（postseason-github 10:40–11:25Z / postseason-platform 10:39–10:58Z）。任务书原定 10-07 首档复查，本次为监控档提前执行（原计划 10-07）。
> 时点：比赛 09-30 23:59 UTC 已截止，官方终评窗至 **10-14 23:59**（~10-14/15 出终榜）。
> 纪律：实抓带来源+时间戳；自报标"自报"；查不到写"未找到"；**专名一律程序化派生**（slug/仓名/handle/track 成员名均从既有文件正则派生，alperen 候选与新仓自 API JSON 提取）。原始拉取物归档 `references/ext/monitor-round2/`（provenance.md+SHA256SUMS.txt，58 件）。
> **方法注**：本档自触"专名禁手键"2 例（repo 名手键假 404×2 次、文件名映射失误致空壳件 1 次），均已用程序化取址恢复并在 provenance 记账——累计教训 7 例，宜随 P4 复盘定理入册。

---

## 〇、判据判定表（五块"增量有/无"）

| # | 判据 | 判定 | 依据（2026-10-02 18:57–19:13 实抓） |
|---|---|---|---|
| 1 | msdsm 权重/许可/写本 | **权重无增量；writeup 无增量；仅 ★+1** | releases=0/tags=0/172 树 0 权重件/HF+Kaggle dataset 0 命中/README byte-identical（11,199B）"supplied separately"原句未变；docs/ 7 件同尺寸无新增 writeup；license 仍 null（NO-LICENSE）；commit 仍唯一 84057a0f；★6→7、fork=2 |
| 2 | 闭源大户开号（8+2）+ alperen 全量 | **无增量**（alperen 抽验补齐为确证） | 8 handle 精确 404 不变；tetsutani 空号未放码（repos=0/gists=0）；track 3 成员（a2nt1as2n/ahmedberatozer/omerlleez）全 404；**alperen 21 候选全量轮询 0 命中**（首档只抽 10）；新仓闸 1 件但为规则式学生件（CheungLeeJR）非大户 |
| 3 | 讨论区二轮 | **有增量**（小） | 全量 247 帖：窗内新帖 **2**（745155/745152，均非拆解潮深帖）；745073 评论 9→11（+2 闲评）票 55→65、**writeup 承诺仍未落地**；745036 +2 闲评；731587 四追问**仍无官方答**；744811 活跃池申诉 +2 无官方答；无获奖公告/官方新帖 |
| 4 | Kaggle kernels/数据集 | **数据集有增量、kernel 无** | kernel 0 新 run/0 新建（最新 run 仍 10-01 22:57）；数据集 2 新件：kirderf/eval-tracker（#790 队 LB 分析）、**mqingcs/two-policy-source "…and Parameters"（#495 队，疑似参数/权重投放，内容 403 不可得）**；georgymarin episodes 01:16:55Z 无新版；官方 10-02 日更未出（惯例 10-03 00:0x，未到点） |
| 5 | 榜面与我方 | **有增量**（漂移持续） | 榜 19:11:44Z：M&M&P&Q 3065.5→**3090.5**（+25）；DECEM 2886.2→2872.5（#5→#7）；MarvinTMB 新进 #10；我方 **#1298/1732.6→#1313/1726.5**（−6.1/−15 名）；LastSubmissionDate 全员不变=纯 BT/Elo 漂移；**仅两活跃件分数在动**（实证官方活跃对口径）；两活跃件 episodes +14/+16 仍在打局（末局 19:11:45Z） |

---

## 一、块 1：msdsm 权重/许可/写本（头号盯防）

**仓态**（repos API 18:57Z；仓名程序化派生自 `ext/postseason-github/readmes/msdsm_*.README.md` 文件名）：

| 项 | 12:29Z 首档 | 18:57Z 本档 | 差分 |
|---|---|---|---|
| 可见性 | public | public | 不变 |
| created / pushed | 10-02T03:17:00Z / 03:30:47Z | 同左 | **无新 push** |
| commits | 1（84057a0f "add all" 03:30:35Z） | 1（同） | 不变 |
| stars / forks / issues | 6 / 2 / 0 | **7** / 2 / 0 | ★+1 |
| license | null（NO-LICENSE） | null | **不变——池测许可裁定仍悬置** |
| releases / tags | 0 / 0 | 0 / 0 | 不变 |

**权重现状（核心判据）=仍未投放**，三路+两枚举全阴：
1. **releases/tags=0**（无 tag/asset 首投放）；`git/trees/main?recursive=1` 172 entries/150 blobs，权重后缀（pt/ckpt/pkl/safetensors/bin/onnx/jax/h5/npz/weights）**0 件**（>500KB 仅 docs/images 两张图）；
2. **README byte-identical**（11,199B，与首档快照 `diff` 零差异）：L12 原句 *"Checkpoints, replay datasets and compiled binaries are supplied separately by the user."* 未改；全文 URL 穷举 7 个=成员个人页（morim3/msdsm/BergBuch/qistripute）+ 竞赛页 + Rust blog + IsaiahPressman/kaggle-orbit-wars——**无任何权重托管链接**；`search/code` huggingface/drive.google=0/0；
3. **HF 公开 API** models+datasets × 4 查询词全 0 命中；**Kaggle datasets** -s 3 查询词全 0 命中。

**writeup 现状（第二判据）=未落地**：docs/ 仍 7 项同尺寸（architecture.md 5,938 / data.md 4,797 / operations.md 3,102 / source-provenance.json 13,628 / training-lineage.md 5,339 / training.md 7,863 / images/），无新文档、无新 commit；745073 内作者承诺（05:48:10Z，自报）"We'll share more details in a write-up later!" 后作者侧零动作。

**成员第二件检查**（清单 A 尾项）：morim3（29 仓 0 gist，无窗内 push）、msd0110（0 仓 0 gist）、qistripute（4 仓）、BergBuch（2 仓）、piii 三拼体（8i/9i/10i 均为 2014-2020 老空号）——**全员无第二件**。

---

## 二、块 2：闭源大户开号（8 账号 + track 2 新增 + alperen 全量轮询）

### 2.1 精确 handle 复查（19:0x，users API；拼写自首档 §二表正则派生）

| 目标 | handle | 本档读数 | vs 首档 |
|---|---|---|---|
| DECEM | zy1343930734 | 404 | 不变 |
| Majkel1337 | majkel1337 | 404 | 不变 |
| **alperen5252525**（头号） | alperen5252525 | 404 | 不变 |
| mtmr_s1 | mtmrs1 / mtmr_s1 / mtmr-s1 | 404×3 | 不变 |
| tarosqrd2 | tarosqrd2 | 404 | 不变 |
| tetsu2131 | tetsu2131 404；变体 tetsutani 有号 | tetsutani：repos=0/gists=0，updated 2026-02-25 | **空号未放码**（清单 B 尾项） |
| shiiin9 | shiiin9 | 404 | 不变 |
| haodou092 | haodou092 | 404 | 不变 |
| track 队友（新增盯防） | a2nt1as2n / ahmedberatozer / omerlleez | **404×3** | 首档未查；3 人零开号 |

### 2.2 alperen 21 候选全量轮询（补齐首档 10/21 抽验缺口）

`search/users q=alperen aydin` 21 候选（与首档同数）逐一 `users/{u}/repos --paginate` + `gists`：**21/21 全查，kagri 仓命中 0、gist 命中 0**（大号 aydinalperenn 48 仓 / alqeren1 20 仓 / AlperenHolat 19 仓 / aydnalperen 18 仓均逐仓扫过）。**头号目标私有产线公开=0 确证升级（抽验→全量）**。

### 2.3 新仓闸 + 自名件甄别

- `q=<slug> created:>2026-10-02T12:34:00Z` = **1**：**CheungLeeJR/<slug>-tournament-agent**（17:41:15Z 建，5 commit 至 17:58:56Z）——stdlib 规则式 submission agent（melons/wheat 开局、三象限扩张、38 草莓位角色分工），NO-LICENSE，自名"tournament agent"非 solution/writeup；同窗同账号另建 3 个无关仓（hkmu-ai-study-assistant 等）似学生作业批。LB 同名 "Ryan Cheung"（#7017/doggychip，516.6）**同名推定未证**——按"公开件≠提交件"标注。
- `pushed:>12:34Z` 活跃 4 仓：**rxymitchy/<slug>**（13:42:39Z README-only update；仓 09-10 已存在，**首档 README 快照集漏收=基线覆盖缺口本档补上**；v7-ranch 规则式"forecast+greedy planner, not a neural net"，自报 41 局 Kaggle replay 调参）、jamesidriss（18:44Z "merge: 3066 breakthrough generation" 自进化持续）、the-genius-man（auto feedback 16:56Z）、CheungLeeJR。
- 自名件 solution/final 搜索：无窗内新件（sunyuxiang136 silver-agent、amrrs、SanTanBan、TaeyanG4、JaydonJP 均在册/旧件）。

**结论：闭源大户兑现=0（8/8+3/3 零开号），alperen 全量确证；窗内唯一新仓为下游学生件。**

---

## 三、块 3：讨论区二轮

### 3.1 新帖扫描（全量 247 帖 = 13 页合并按 postDate 排序；首档 3 页 60 帖的覆盖缺口本档补齐）

| id | 时间 | 帖 | 票/评 | 判读 |
|---|---|---|---|---|
| 745155 | 14:36:57Z | "Game Theoretic Approaches"（Nikita） | 0/1 | 18:41:21Z **Krzysztof Gonia 回复**（自报）："I also started with MCTS but then switched to ALNS"——疑似 host 再现身（身份仍未核实），口径增量（MCTS→ALNS 路线） |
| 745152 | 14:35:01Z | "Kaggriculture leaderboard statistics + notebook!"（Kirderf） | 6/3 | LB 统计 notebook 帖；评者含 **Chris Deotte**（自述 bot 下行）、Russell Kirk（署名 team 16624026）、masspeaks（DSM 队）——名将围观密度高；对应 kirderf/eval-tracker 数据集（见块 4） |

- 745119（4th 深帖）0→0 无更新；**无获奖公告、无官方新帖**（247 帖内 host 发帖 0）。
- 拆解潮第二波：**未现**——窗内 2 新帖均非深帖续作（745036/745119/744999/744988 无一有续），间歇期判断维持，第二波仍在 10-14/15 终榜前后预期窗。

### 3.2 三篇 writeup 帖 + 官方口径线

| 帖 | commentCount 差分 | 读数 |
|---|---|---|
| 745073（#1 预告） | 9→**11**（票 55→65） | +2 均闲评：綿鍋 13:10 贺帖、SeaGoat 14:28:32Z（自报）"similar model (helped by claude)…not invest so much in training"（AI 辅助同路线旁证）；**作者侧末条仍是 05:48Z write-up 承诺，未落地**；topic-messages URL 仍=仓链+3 GCS 图，无新链接 |
| 745036（SFT） | 2→**4** | +2：NT 08:58 贺（"la tiao wang zi"）、WOOSUNG YOON 14:08 共情长评 + Russell Kirk 14:14 meme 回复——无技术增量 |
| 745119（4th） | 0→0 | 无更新 |
| 731587（官方 final evaluation） | **7→7** | 截止后 4 追问（Andrei Dzis 位次来源/CemBas 迟交 10 秒申诉/Densike/Jason xu sk）**仍无官方回复**（末条 08:16Z 先于首档） |
| 744811（活跃池缺件申诉） | 0→**2** | 14:43 空评 + Semyon Epanov 14:45:54Z 再 @dominoweir/@bovard/@macruzbar——"Last accepted submission missing from active pool"官方仍无答（与 744614 重激活悬案同簇） |
| 745074（games too rarely） | 5→5 | 不变；Gonia 口径（BT 现在进行时、3 局/时）与实测 2-3 局/时吻合度高 |

---

## 四、块 4：Kaggle kernels / 数据集

- **kernels：无增量**。`--sort-by dateRun` 最新 run 仍 10-01 22:57（destbreso X-ray）与 10-01 22:07（georgymarin 2600 farms）；`--sort-by dateCreated` 最新建件仍 abhinav0370（09-24）——窗内 0 新 run / 0 新建件。
- **数据集：2 新件**（对首档 20 行清单差分）：
  1. **mqingcs/<slug>-two-policy-source**（"Two Policy Source and **Parameters**"，11:41:38Z，450KB，18 下载，1 票）：**#495 mqjx 队成员**（jifengjianhao666,mqingcs；2074.4）投放——标题含 "Parameters"，**疑似对手代码+策略参数（近权重）投放**；但 files/metadata/download 三路 403，内容未验，许可未知；按 NO-LICENSE 同口径只登记不搬运。**下档必查**。
  2. **kirderf/<slug>-eval-tracker**（18:59:14Z 首版，9 文件：leaderboard.csv 30MB、leaderboard_race.gif、rank_bump_top30.gif、episodes/runs/submissions/zones_history CSV）：**#790 Kirderf 队**（1914.0）LB 分析产线，对应 745152 帖——终评期收敛可视化工具，可作终榜对表辅助（a51050-4 候选工具）。
- **georgymarin/<slug>-episodes**：lastUpdated **2026-10-02T01:16:55 无变化**（首档记 ≥v80 同戳）——窗内无新包。
- **官方日更**：`-2026-10-02` 期**未出**（惯例次日 00:0x 发，19:12Z 未到点）；`-index` 仍 10-02 00:03:29。09-30/10-01 期出包戳不变。

---

## 五、块 5：榜面与我方读数

### 5.1 榜面（LB CSV 19:11:44Z 全量 10,246 队；对照 12:34:11Z 首档）

| # | 队 | 12:34 | 19:11 | 差分 | LastSubmission |
|---|---|---|---|---|---|
| 1 | M & M & P & Q | 3065.5 | **3090.5** | **+25.0** | 09-30 15:21:46 |
| 2 | 1x5090 potato run | 3033.6 | 3028.8 | −4.8 | 09-30 23:54:28 |
| 3 | DSM | 2945.5 | 2954.5 | +9.0 | 09-30 23:26:15 |
| 4 | Farmcore | 2901.6 | 2915.4 | +13.8 | 09-30 23:18:04 |
| 5 | CDE | 2879.4（#7） | 2898.4（#5） | +19.0 | 09-30 23:36:56 |
| 6 | 有辣条有权 | 2885.2 | 2895.8 | +10.6 | 09-30 23:29:22 |
| 7 | DECEM | 2886.2（#5） | 2872.5（#7） | −13.7 | 09-30 19:08:29 |
| 10 | MarvinTMB | #11 之外 | 2806.4 | **新进 top10**（Azat Akhtyamov 跌出） | 09-30 23:53:20 |
| 280 | Alperen Aydın | 2293.6（#279） | 2287.2 | −6.4 | 09-30 15:02:03 |
| 465 | track | 2090.0（#474） | 2095.0 | +5.0（**+9 名**） | 09-30 20:28:30 |
| **1313** | **renyxin（我方）** | **1732.6（#1298）** | **1726.5** | **−6.1（−15 名）** | 09-30 23:36:00 |

全员 LastSubmissionDate 两快照间不变→**变动全部=BT/Elo 收敛漂移**。头部两极：#1 连续上漂（1796→…→3090.5 视角下的头部收敛上翘），DECEM 反跌 2 名；MarvinTMB（745073 评内"1M 参数 BC+自对弈"自报者）挤进 top10。我方相对距：Alperen −560.7、track −368.5、DECEM −1146.0。

### 5.2 我方 submissions（19:12Z）与 episodes（19:12Z）

| ref | 槽位 | publicScore 12:34→19:12 | 计分地位 |
|---|---|---|---|
| 56721643 | H1X-a | 1732.6→**1726.5**（−6.1） | 活跃（latest-2）=队分 |
| 56721419 | composite | 1696.7→**1688.1**（−8.6） | 活跃（latest-2） |
| 56716525 | H1X | 1642.1 不动 | 非活跃 |
| 56708866 | S8 composite v2 | 1476.8 不动 | 非活跃 |
| 56697824 | C_final | 1783.1 不动 | 非活跃（读数高≠计分） |
| 56687451 / 56685176 | 早期件 | 1657.1 / **1829.8** 不动 | 非活跃 |

**读数要点**：①**仅两活跃件分数在动、非活跃件全冻结**——官方"BT 只拟合活跃对"口径（742571）第一次拿到窗口内双快照实证；②队分四点漂移 1796.2→1743.8→1732.6→**1726.5**（约 −1.0/时）；③56685176 全史最高读 1829.8 亦不计分，进一步坐实"历史读数≠终评输入"。

**episodes 收敛进展**（API 窗口行数，非全史口径同首档）：
- 56721419：**137 行**（首档 123，+14）；末局 create 19:06:40→**end 19:11:45Z**；
- 56721643：**152 行**（首档 136，+16）；末局 create 18:57:17→end 18:59:22Z；
- 全部 EpisodeState.COMPLETED，各 1 局 VALIDATION + 余 PUBLIC；打局速率 2-3 局/时（与 Gonia"3 games during an hour"自报吻合）——**收敛窗打局正常，未停**。

---

## 六、异常与限界

1. **专名手键 2 例（本档新增）**：CheungLeeJR/rxymitchy 仓直接探测手键 repo 名致假 404（正体名含双 g，肉眼渲染不可辨），改 API listing `url` 字段取址后恢复；另有文件名映射失误致 4 个空壳件（已删）。教训累计 7 例。
2. **首档覆盖缺口 2 处本档补上**：topics 首档仅 3 页 60 帖（票序分页），本档全量 13 页 247 帖——旧帖增量（744811 等）系缺口内补见而非新发；rxymitchy 仓首档 README 快照集未收，本档补记（窗内增量仅 README 一笔）。
3. **mqingcs 数据集内容不可得**：files/metadata/download 三路 403（kirderf 同命令可取，疑为该件权限/审核态）——"Parameters"是否为模型权重**未验证**，按最坏假设列入下档必查。
4. Krzysztof Gonia 身份仍未核实（`competitions hosts` 403）；本档新增 745155 回复一条（MCTS→ALNS 自报），继续"疑似 host"降权。
5. CheungLeeJR 与 LB "Ryan Cheung"（#7017/doggychip）为**同名推定**（未证同一人）；公开件≠提交件标注沿用。
6. episodes 行数为 API 返回窗（起点=提交时刻，或为全史但不承诺）；官方全史对局数需终评侧证。topics 评论 voteCount 列表字段在 list 端为 None（show 端可得），不影响计数判定。
7. HF 搜索 0 命中≠权重不存在的充分证据（私有仓/非索引渠道不可见）；本档权重判定另有 releases/tags/tree/README/Kaggle-datasets 五路背书。
8. 榜 CSV BOM 列名（`﻿Rank`）沿用 utf-8-sig 处理；LB 快照戳取自 zip 内文件名 19:11:44Z。

---

## 七、来源清单（均 2026-10-02 18:57–19:13 UTC 实抓）

| # | 来源 | 通道 | 戳 |
|---|---|---|---|
| G1 | repos/<msdsm>/<repo> 族（meta/commits/releases/tags/readme/contents/docs/contributors/git-trees） | REST | 18:57–19:0x |
| G2 | users/{zy1343930734,majkel1337,alperen5252525,mtmrs1,mtmr_s1,mtmr-s1,tarosqrd2,tetsu2131,tetsutani,shiiin9,haodou092} + track{a2nt1as2n,ahmedberatozer,omerlleez} | REST | 19:0x |
| G3 | search/users q=alperen aydin（21 候选全量 repos+gists 轮询） | REST | 19:0x |
| G4 | search/repositories（created:/pushed: 闸、solution/final 自名件）+ CheungLeeJR/rxymitchy/jamesidriss/the-genius-man commits | REST | 19:0x |
| G5 | HF api models/datasets ×4 查询 | HTTPS | 19:0x |
| K1 | kaggle competitions topics list <slug> -p 1..13 --format json（247 帖） | CLI 2.2.4 | 19:0x |
| K2 | topics show / topic-messages {745073,745036,745119,745074,731587,744811,745152,745155} | CLI | 19:0x–19:1x |
| K3 | kernels list --competition --sort-by dateRun/dateCreated；datasets list -s {<slug>,<slug>-episodes}；datasets files（kirderf 可/mqingcs 403） | CLI | 19:0x |
| K4 | competitions leaderboard <slug> -d（CSV 19:11:44Z，10,246 队） | CLI | 19:11 |
| K5 | competitions submissions <slug> --csv；episodes {56721419,56721643} | CLI | 19:12 |
| X1 | monitor-baseline.md + ext/monitor-baseline/（12:25–12:37Z 基线） | 档案复读 | — |
| X2 | postseason-github-scan.md / postseason-platform-scan.md / ahmed-deepcut.md（窗口差分与专名派生源） | 档案复读 | 10:39–11:25Z |

## 需登记行（INDEX.md，勿在本篇代改）

1. `references/ext/monitor-round2/`（provenance.md + SHA256SUMS.txt + msdsm 族×8 + HF/权重查×2 + 账号探测×4 + topics 全量 13 页 + 8 帖双件 + kernels/datasets×4 + LB CSV 19:11:44Z + submissions + episodes×2，共 58 件）｜GitHub REST + kaggle CLI + HF API｜2026-10-02｜监控二轮原始拉取物（18:57–19:13Z 窗口差分）
2. `references/2026-10-02-monitor-round2-platform.md`｜本轮｜2026-10-02｜监控二轮增量档：msdsm 权重/写本双未投放（★+1）/闭源大户+track 全零开号（alperen 21 候选全量确证）/讨论区 2 新帖+745073 承诺仍未落地/数据集 2 新件（mqingcs 疑似参数投放待验）/榜面与我方漂移四点（队分 1726.5、仅活跃件在动实证）
