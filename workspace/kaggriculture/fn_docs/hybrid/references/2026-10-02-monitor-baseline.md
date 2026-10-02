# 2026-10-02 监控首档快照（monitor-baseline）——10-07/10-15 两档监控的对照基线

> 抓取窗口 **2026-10-02 12:25–12:37 UTC**（=CST 20:25–20:37）；通道：GitHub REST（`gh api`，r-y-ren 鉴权）+ kaggle CLI 2.2.4。时点：比赛 09-30 23:59 UTC 截止后第 2 天，官方终评窗至 **10-14 23:59**（`competitions list --group entered` deadline 字段，见并行件），~10-14/15 出榜。
> 纪律：实抓带来源+时间戳；自报标"自报"；查不到写"未找到"；**专名一律程序化派生**（slug 取自既有抓取物正则、msdsm 仓名取自 search JSON、8 handle 与在册扫描件逐位核对）。原始拉取物归档 `references/ext/monitor-baseline/`（provenance.md+SHA256SUMS.txt，9 件）。
> 同日早间并行件基线：`2026-10-02-postseason-github-scan.md`（10:40–11:25Z）、`2026-10-02-postseason-platform-scan.md`（10:39–10:58Z）。本档与其做窗口差分，同时作为下两档（10-07/10-15）的对照基线。
> **方法注**：12:25Z 我对 msdsm 仓的首次探测 404 系**本人手键走样名**所致（非仓下线）；程序化取名后 12:29Z 实抓 ALIVE。"专名查询禁手键"教训再添一例（与 github-scan 方法学警示同源）。

---

## 〇、判据判定表（四块"增量有/无"）

| # | 判据 | 判定 | 依据（2026-10-02 12:2x-12:3x 实抓） |
|---|---|---|---|
| 1 | msdsm/kagriculture-solution 仓与**权重现状** | **权重无增量；仓态确证公开** | 仓 ALIVE/public（12:29Z）；README"supplied separately"原句未变；**releases=0、172 文件树 0 权重件、README/docs/code 0 外链投放**（HF/Drive/Kaggle dataset 均无）；唯一 commit 84057a0f（03:30:35Z）后无新增；★5→6、fork=2 |
| 2 | 闭源大户 8 账号 GitHub 开号 | **无增量** | 8/8 精确 handle 404（12:31Z）；tetsu2131 的 Kaggle 账号名 tetsutani 在 GitHub 有号但 **repos=0/gists=0**（2022 年老号，非新开）；alperen 姓名 21 候选抽验 10 个零命中；`kagri created:>11:25Z` 新仓=0 |
| 3 | 讨论 745073 详解更新 + 新帖扫描 | **帖面无增量；评论细节有增量** | 745073 commentCount **9 未变**（末评 09:11Z）、票 50→55；承诺"write-up later"**未落地**（msdsm 仓 docs 无新 commit、无新帖）；topics 3 页 60 帖最新=745119（10:31:05Z），12:32Z 时**无更新帖、无获奖公告**；但 745073 评论区新收 2 条情报（二次 BC 自愈、算力自报） |
| 4 | 榜面快照 + 我方读数（终评收敛进展） | **有增量**（收敛基线落定） | 榜 CSV 12:34:11Z 全量 10,246 队；我方 **#1298/1732.6**（10:45:33 #1257/1743.8→1.8h 纯漂移 −11.2/−41 名）；**活跃计分对={56721419, 56721643}**（latest-2）；两活跃件 12:05-12:30Z 仍在打局（136/123 局流） |

---

## 一、块 1：msdsm/kagriculture-solution 仓与权重现状

**仓态**（repos API 12:29:30Z；仓名程序化派生=k-a-g-g-r-i-c-u-l-t-u-r-e-s-o-l-u-t-i-o-n）：

| 项 | 读数 | 差分 vs 10:53-11:25 并行件 |
|---|---|---|
| 可见性 | public / ALIVE | 与 github-scan"11:25Z ALIVE"一致（platform-scan"10:55 404"按其自注记判同源误拼） |
| created / pushed | 2026-10-02T03:17:00Z / 03:30:47Z | 无新 push（commit 仍唯一：84057a0f "add all"） |
| stars / forks / issues | 6 / 2 / 0 | ★5→6（+1）；fork 2 为新增读数 |
| license | **null（NO-LICENSE）** | 不变——只登记不搬运、池测待许可裁定 |
| has_discussions / wiki | false / false | 讨论面不开，权重公告只能走 README/release/Kaggle/HF |

**权重现状（核心判据）=未投放**：
1. README（11,199B，12:29:57Z 抓）第 12 行原句：*"Checkpoints, replay datasets and compiled binaries are supplied separately by the user."* —— **"另发"承诺未兑现**；
2. `releases` API=**0**（无 tag/asset）；`git/trees/main?recursive=1` **172 文件**中权重类后缀（pt/ckpt/pkl/safetensors/bin/onnx/jax）**0 件**；
3. 全仓 `search/code` huggingface / drive.google = **0/0**；README 与 docs/*.md 外链穷举=GitHub 个人页（morim3/msdsm/BergBuch/qistripute）+ 竞赛页 + Rust blog + IsaiahPressman/kaggle-orbit-wars——**无任何权重托管链接**；
4. 讨论区 745073 全部 URL（topic-messages 12:33Z）= 仓链接 + 3 张 GCS 附件图（overview/model_detail/training_detail.png）——亦无权重链接。

**docs/ 现状**（对复盘轨 a51050-2 有用）：architecture.md(5.9K)/data.md(4.8K)/operations.md(3.1K)/training-lineage.md(5.3K)/training.md(7.9K)/source-provenance.json(13.6K，含 submission_archives A/B 的 sha256 与逐组件 source_sha256)/images/。源码打包产线（pyproject/Dockerfile/scripts/python/native/tests/k8s）齐备，唯权重缺席。

---

## 二、块 2：闭源大户 8 账号开号检查（alperen=头号情报目标）

12:31Z 精确 handle users API + 12:36Z 关键词补查（handle 拼写与在册 `2026-10-02-postseason-github-scan.md` 文本逐位核对一致）：

| 目标 | GitHub 精确 handle | 关键词/变体补查 | 判定 |
|---|---|---|---|
| DECEM | zy1343930734 → **404 无号** | users 搜 zy1343930734=0 | 未开号 |
| Majkel1337 | majkel1337 → **404** | "majkel" 699 候选（majkel/tenmajkl/…）无一可确证 | 未开号 |
| **alperen5252525**（头号） | alperen5252525 → **404** | "alperen aydin" 21 候选（与并行件同数）；抽验 10 个（aydinalperenn 48 仓/alperen0420 13 仓/aydnalperen 18 仓/aydinalperen/alqeren1/alpervnm/ThisIsAlperen/aydinalperen7/alperenaydinn）kagri 仓命中 **0**、gists **0** | **未开号；私有产线仍未公开** |
| mtmr_s1 | mtmrs1/mtmr_s1/mtmr-s1 → **404×3** | "mtmrs" 3 候选（mtmrstr/mtmrshocked/mtmrsudi） | 未开号 |
| tarosqrd2 | tarosqrd2 → **404** | "tarosqrd" 搜=0 | 未开号 |
| tetsu2131 | tetsu2131 → **404**；变体 **tetsutani 有号**（created 2022-06-10，repos=0，gists=0） | "tetsu2131" 搜=0 | **有号但空**（2022 老号非新开；无任何公开仓/gist） |
| shiiin9 | shiiin9 → **404** | "shiiin" 87 候选（Shiiin/shiiinji/…） | 未开号 |
| haodou092 | haodou092 → **404** | "haodou" 16 候选 | 未开号 |

新增仓总闸：`search/repositories?q=kagriculture created:>2026-10-02T11:25:00Z` = **0**（11:25Z 并行件后无新仓）。**结论：闭源大户 8/8 截至 12:36Z 零兑现，与 10:56-11:02 并行件窗口一致——此档即下两档的"开号前状态"基线。**

---

## 三、块 3：讨论区（745073 详解承诺 + 新帖扫描）

### 3.1 745073（M&M&P&Q "[1st Place (currently)] A preview of our solution"，作者 msd0110）

- **承诺的详解更新：未落地**。末条评论 2026-10-02T09:11:35Z（democatXamer 贺帖），commentCount 9（10:46 并行件读数相同→12:33Z 无新评论）；votes 50→**55**。作者在 05:48:10Z 评论中重申（自报）："**We'll share more details in a write-up later!**"——write-up 本体未出现（无新帖、msdsm 仓 docs/ 无新 commit）。
- **评论区新收情报（并行件未入账，2 条）**：
  1. **二次 BC 自愈现象**（msd0110，05:16:44Z，自报）：对 PPO 训好的模型再跑 BC，产出 checkpoint **100 局全负于 BC 前**；但从该二次 BC checkpoint 恢复 PPO 自对弈，约 **6 万局后反超** BC 前 checkpoint——"二次 BC 退步≠该弃"的训练动力学个案（对 a51050-5 神经系路线侦察直接有用）。
  2. **算力自报**（msd0110，05:48:10Z）：10M PPO 峰值 17×A100+29×A30（均值 ~7×A100+20×A30）；20M PPO 峰值 26×A100。
  3. 旁证：MarvinTMB（05:43:35Z，自报）自家模型"just under 1M parameters, same self-play and BC ideas but no heuristics"——榜上他家也走 BC+自对弈小参数路线。
- 附件：3 张 GCS 图（overview/model_detail/training_detail.png）未下载（沿用并行件限界）。

### 3.2 新帖扫描（topics list 3 页 60 帖，12:32:56Z）

- **最新帖=745119**（2026-10-02T10:31:05Z，"[4th Place (currently)] No RL, no search: a one-forward-pass transformer"，15 票/0 评）——即 10:43 并行件所见同一批的末件；**10:31Z 之后无任何新帖**（12:32Z 时点）。
- **获奖公告/官方新帖：未找到**（60 帖内无 host 发帖、无 final results）；731587"final evaluation"帖 commentCount=7（并行件 10:46 记 3 条截止后追问未获答→现 +4 条同为追问，官方仍未答——细节以并行件为准，本档不重复抓正文）。
- 745074"Games are played too rarely" commentCount=5（内含"疑似 host"Krzysztof Gonia 06:31 口径，身份未核实，沿用并行件限界与降权口径）。
- 结论：赛后拆解潮主体已过第一波（744788→745119 共 20 篇 09-30 23:38 后），当前进入**间歇期**——第二波预期在 10-14/15 终榜前后（获奖感言潮）。

---

## 四、块 4：榜面快照 + 我方读数（终评收敛进展）

### 4.1 榜面（LB CSV `kaggriculture-publicleaderboard-2026-10-02T12:34:11Z`，10,246 队；对照 10:45:33Z）

| # | 队 | 12:34 读数 | vs 10:45:33 | LastSubmission |
|---|---|---|---|---|
| 1 | M & M & P & Q | 3065.5 | −1.4 | 09-30 15:21:46 |
| 2 | 1x5090 potato run | 3033.6 | +5.8 | 09-30 23:54:28 |
| 3 | DSM | 2945.5 | +3.3 | 09-30 23:26:15 |
| 4 | Farmcore | 2901.6 | +8.2 | 09-30 23:18:04 |
| 5 | DECEM | 2886.2 | −4.7 | 09-30 19:08:29 |
| 6-10 | 有辣条有权 2885.2 / CDE 2879.4 / Anton Tikhonov 2849.7 / KawattaTaido 2820.4 / Azat Akhtyamov 2804.0 | — | — | 均 09-30 |
| 279 | Alperen Aydın | 2293.6 | +3.6（#283→#279） | 09-30 15:02:03 |
| 474 | track（ahmed·track） | 2090.0 | −1.8（#471→#474） | 09-30 20:28:30 |
| **1298** | **renyxin（我方）** | **1732.6** | **−11.2（#1257→#1298）** | 09-30 23:36:00 |

全员 LastSubmissionDate 两快照间不变→**榜面变动全部=BT/Elo 收敛漂移**（终评窗第 2 天常态）。我方相对读数：距 Alperen −561.0、距 track −357.4、距 DECEM −1153.6。

### 4.2 我方 submissions 读数（12:34Z，`competitions submissions --csv`）

| ref | 槽位描述 | 提交时间 | 状态 | publicScore 现读 | 计分地位 |
|---|---|---|---|---|---|
| 56721643 | H1X-a（V82 衍生+order-hygiene+spike capture+endgame declaration calibration） | 09-30 23:36:00 | COMPLETE | **1732.6** | **活跃（latest-2）=队分** |
| 56721419 | composite（V82 衍生：hygiene/wool defense/focused window/drop-half/fertilizer split/state hardening） | 09-30 23:26:44 | COMPLETE | 1696.7 | **活跃（latest-2）** |
| 56716525 | H1X | 09-30 19:05:47 | COMPLETE | 1642.1 | 非活跃 |
| 56708866 | S8 composite v2 | 09-30 13:36:40 | COMPLETE | 1476.8 | 非活跃 |
| 56697824 | C_final composite | 09-30 05:06:10 | COMPLETE | 1783.1 | 非活跃 |

**终评收敛进展三条**：
1. **活跃计分对确证={56721419, 56721643}**（10-01 裁决所称"定格"的 C_final/S8 已被 09-30 23:26/23:36 两件新提交顶出 latest-2）——与 platform-scan 更正一致，本档固化为基线；
2. **C_final 现读 1783.1 > 队分 1732.6 但不计分**：按官方口径（742571，Addison Howard）终评 BT "only those against submissions still active will count"→只拟合 {56721419, 56721643} 与各队活跃件之间的对局。C_final 的历史对局**不进终评**——读数高≠计分高；
3. **收敛对局仍在跑**（episodes 流 12:36Z）：56721643 136 局（末局 create 12:05:07→end 12:08:00）、56721419 123 局（末局 12:25:04→12:30:23），全部 COMPLETED（PUBLIC 为主，各 1 局 VALIDATION）——收敛窗打局速率正常，我方队分随每批对局持续缓漂（1796.2→1743.8→1732.6 三点）。

---

## 五、10-07 / 10-15 复查清单（下两档必查项）

**A. msdsm 权重与 #1 官方解（最高价值战利品）**
- [ ] `releases/tags` 有无首个投放（权重/二进制/replay 数据集）；README"supplied separately"是否补链接（HF/Kaggle dataset/Drive/Release asset）；git tree 权重后缀复查
- [ ] docs/ 是否新增 writeup（对应 745073 承诺）；license 是否明示（现 null→决定能否池测）
- [ ] commit 数是否 >1、stars/forks 增速；成员个人号（morim3/msd0110/piiiiiiii/qistripute）有无第二件

**B. 闭源大户开号（8 账号 + 2 新增）**
- [ ] 8 handle 精确 users API 复查 + 关键词搜索新候选；**alperen（头号）**：21 候选全量轮询（本档只抽验 10 个）+ 仓库/ gist / 新号三面
- [ ] 新增盯防：track 队成员 **a2nt1as2n / omerlleez**（ahmed·track 队友，ahmed-deepcut 篇遗留）；mtmr_s1/tetsutani 的空号是否开始放码
- [ ] `q=kagriculture created:>2026-10-0X` 新仓闸 + "final solution/writeup"自名件甄别（公开件≠提交件标注、许可标注）

**C. 讨论区**
- [ ] 745073 commentCount/末评时间戳（承诺 writeup 是否落地）+ 745074/731587 官方口径是否更新（731587 追问是否获答；Krzysztof Gonia 身份核实）
- [ ] 新帖扫描（topics list 全页按 postDate 排序）：10-07 档看**拆解潮第二波**（745036/745119/744999/744988 类深帖续作）；10-15 档看**获奖公告/获奖感言潮**（官方 final results 帖出现=事件锚）
- [ ] 深帖技术拆解入复盘轨候选（a51050-2）：745073（神经系）、745119（4th，one-forward-pass transformer）、745036（SFT）、744988（ES planner+residual RL）、744999（RL experiments postmortem）

**D. 榜面与我方读数**
- [ ] 榜 CSV 全量下载存档（对表 top20/Alperen Aydın/track/renyxin 四点）；10-14 23:59 收敛窗结束→10-15 档拍**终态榜**（官方 BT 定榜）
- [ ] `submissions --csv`：latest-2 是否再变（注意：截止后不可再交，活跃对已冻结={56721419, 56721643}，除非官方开重激活——744614 未确认）；两活跃件 episodes 是否停跑
- [ ] 交付链：终榜对表完成后回填 registry `a51050-4` expected_signal"终榜对表完成"

**E. 事件锚（两档之间）**
- [ ] 10-14 23:59 收敛窗结束；~10-14/15 官方 BT 定榜与获奖公告；届时预期=获奖感言/开源二次潮（闭源大户开号概率最高窗口）

---

## 六、异常与限界

1. **手键走样 404 一例**（本档 12:25Z msdsm 仓误拼探测）——已更正并写入 provenance；与并行件"专名查询禁手键"教训同源，建议该教训定理随 P4 复盘一并入册。
2. kaggle CLI 2.2.4：`episodes` 只收 submission_id（无 competition 参数，12:36 首试报错后更正）；`topics list/--format json` 输出尾带 `Next Page Token` 行（raw_decode 解析）；topics 分页**按票序非时间序**（新帖检测须全页合并排序）；LB CSV 列名带 BOM（`﻿Rank`）。
3. Krzysztof Gonia 身份未核实（`competitions hosts` 403）——其 745074"BT 已在进行、3 局/小时"口径按"疑似 host"降权，与 731587 官方口径并读。
4. alperen 姓氏变体（Aydın 土耳其字符）致姓名搜索候选含大量假阳；本档抽验 10/21，剩余 11 个未验。
5. 745073 附件 3 图（GCS）未下载；README/docs 全文仅摘引关键句，全文在 msdsm 仓（NO-LICENSE，只登记不搬运）。
6. GitHub search/code 对无命中返回 0 不可单独作为"文件不存在"证据——本档权重判定另有 git tree 172 文件全量枚举背书。
7. 两活跃件 episodes 行数（136/123）为 API 最近返回窗（非全史）；全史对局数需官方终评口径侧证。

---

## 七、来源清单（均 2026-10-02 12:25–12:37 UTC 实抓）

| # | 来源 | 通道 | 戳 |
|---|---|---|---|
| G1 | api.github.com/repos/msdsm/<kagriculture-solution>（meta/commits/releases/contents/readme/docs/git-trees） | REST | 12:29:30–12:30:5x |
| G2 | api.github.com/users/{zy1343930734, majkel1337, alperen5252525, mtmrs1, mtmr_s1, mtmr-s1, tarosqrd2, tetsu2131, tetsutani, shiiin9, haodou092} | REST | 12:31:12 |
| G3 | search/users{alperen+aydin, alperen5252525, zy1343930734, majkel, tarosqrd, shiiin, haodou, mtmrs, tetsu2131} + 10 候选 users/{u}/repos,gists | REST | 12:31:22–12:36:48 |
| G4 | search/repositories（q=kagriculture created:>2026-10-02T11:25Z、user:msdsm） | REST | 12:25:56–12:36:48 |
| K1 | kaggle competitions topics list <slug> -p 1..3 --format json | CLI 2.2.4 | 12:32:56 |
| K2 | kaggle competitions topics show/topic-messages <slug> 745073 | CLI | 12:33:36 |
| K3 | kaggle competitions leaderboard <slug> -d（CSV 12:34:11Z，10,246 队） | CLI | 12:34:10 |
| K4 | kaggle competitions submissions <slug> --csv | CLI | 12:34:2x |
| K5 | kaggle competitions episodes 56721643 / 56721419 --format json | CLI | 12:36:0x |
| X1 | 并行件 2026-10-02-postseason-github-scan.md / -platform-scan.md（窗口差分基线） | 档案复读 | 10:39–11:25Z |
| X2 | ext/postseason-platform/comp_list_entered.txt（slug 程序化派生源） | 档案复读 | — |

## 需登记行（INDEX.md，勿在本篇代改）

1. `references/ext/monitor-baseline/`（provenance.md + SHA256SUMS.txt + topics×3 + 745073 双件 + LB CSV 12:34:11Z + submissions + episodes×2）｜kaggle CLI + GitHub REST｜2026-10-02｜监控首档原始拉取物（10-07/10-15 对照基线）
2. `references/2026-10-02-monitor-baseline.md`｜本轮｜2026-10-02｜监控首档快照：msdsm 权重未投放确证/8 账号零开号/745073 writeup 未落地+2 条评论情报/榜面与我方终评收敛三点读数/下两档复查清单
