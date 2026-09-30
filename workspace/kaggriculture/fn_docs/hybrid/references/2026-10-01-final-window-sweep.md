# 2026-10-01 终窗扫描（sweep5 双通道：平台侧+站外）——截止前 7h 的新公开件与终评语义

> 抓取时点 **2026-09-30 16:12–16:35 UTC**（=CST 10-01 00:12–00:35）；通道：kaggle CLI 2.2.4 + GitHub API + Bing/HN 检索。纪律：逐条带来源 URL+抓取日期；自报数字标"自报"；查不到写"未找到更新"。
> **时间线更正**：截止=09-30 23:59 **UTC**=CST 10-01 07:59——扫描时窗仍开（余 ~7h45m），"截止后新公开"严格为空集，本篇按 09-29 后新公开口径。2026-10-01 起为真·截止后。

## 一、平台侧（kaggle CLI，来源 S1-S20 见文末）

### 1. 榜面快照（2026-09-30T16:11:16Z CSV，10216 队；对照 09-29T13:41:16Z）
| # | 队 | 分 | dS vs 09-29 | 最后提交(UTC) |
|---|---|---|---|---|
| 1 | M & M & P & Q | 3038.8 | −44.9 | 15:21 |
| 2 | DECEM | 2958.1 | −13.0 | 10:46 |
| 3 | Victor @ Tufa Labs | 2957.5 | +22.5 | 14:25 |
| 6 | CDE | 2879.6 | +509.1 | 07:36 |
| 8 | Gemini IS ALL YOU NEED | 2850.2 | +504.8 | 13:31 |
| 20 | mtmr_s1 | 2778.9 | +2178.9（换交暂态） | 13:25 |

- 我方 renyxin **#1160 / 1813.9**（LastSubmissionDate 09-30 13:36:40，SubmissionCount=2=C_final+S8）；榜面是 2 槽换交暂态（抽样 10 队全部有新提交；7467 降/2664 升），**不是终评 BT 读数**。
- SpTaro 55→744（−689.5）等大额波动=换交重置噪声。

### 2. 终评语义（官方口径，重要）
- **Addison Howard 742571（09-22）**："It will run over all episodes ever played between submissions that are still active… only those against submissions still active on the leaderboard will count" → **BT 拟合取全窗对局史、只计仍活跃（latest-2）提交之间的对局、两周期末结算**。
- 744614（09-30 14:40）"Is It Possible to Reactivate a Previous Submission Before the Deadline?"——回复（自报）"there will be two extra weeks for further estimation… time for your agents to be converged"；**重激活机制未获官方确认**，等效手段=重投字节（r34a 字节彩票先例）。
- 731587 追问 Oct 1–15 窗口/平局计半——官方未答；734000 "截止后重置 600 重爬"=类比推测未证实。
- 分享锁 bug（741281）：09-30 仍有新件发布 → 未修。

### 3. 截止前 24h 新公开件（dateRun 序）
| run(UTC) | kernel | 增量 |
|---|---|---|
| 15:56 | haodou092/kaggriculture-harvest-ledger **V94** | "Verified Spatial Mirror Gate"定稿件（自报 10 血脉×32 路筛 4 决赛圈再验 24 路；复装 V81 镜像门+改市场段） |
| 15:48/15:31 | leoprovorov god-s-mode / ice-fire | 新 run（god-s-mode v7 被 flexonafft 引用 scriptVersionId=351167531） |
| 15:46 | evgendvorkin/…bronze-going-up | anhadmahajan06 件俄语转制（Apache-2.0） |
| 13:05 | lynnsakurai/farmer-john-and-the-wheat-seller | 订单重排算子 T(a) 数学拆解（margin>0.5 接受准则/48 pass 环检测）——启发式重排族（已证负区） |
| 11:40 | flexonafft/kaggriculture-multi-route-farming-agent | **god-s-mode v7 重打包**（Apache-2.0；自报存档版公开分 2604.3） |
| 09-29 22:43 | ashok205/top10-replay-dataset-archive | top10 回放归档工具 |

榜顶队伍公开件/拆解：**未找到**（Majkel1337 等 13 名成员逐一核验：无 kaggriculture 公开件）。

### 4. 在册件版本核查：haodou **更新→V94**、leoprovorov 两件新 run；其余（haideptry/shiiin9/uninhibited/ahmed/alperen/guru×2/tetsutani/lynnsakurai idle-seller/destbreso x-ray/georgymarin）**未找到更新**；**doanthuan/kaggriculture kernel 403**（GitHub 仓仍在，见站外）。

### 5. 数据集：georgymarin/kaggriculture-episodes v79（09-30 00:43:36 后冻结）；官方日更序列 09-29 期为最新（09-30 期预计 10-01 出包）。

## 二、站外（GitHub API + 检索，来源 G1-G17 见文末）

1. **截止后（至抓取时点）零 push/零新仓**：kaggriculture 仓总数 393（+6 全在 09-30 白天）；`pushed:>2026-09-30`=0。
2. **赛后拆解/复盘/获奖公告：未找到**（Bing freshness=Week/Month、HN Algolia 0 命中；截止仅 ~24h，滞后常态）。
3. **锚点资产冻结在 09-30 00:4x**：doanthuan/kaggriculture 末 commit b325122 "Switch to tetsutani step1009 with a deeper sale look-ahead"（+此前 "Race premium sales 48 turns ahead to beat tetsutani copies"、"Replay top teams' ladder games as route plans"）；georgymarin 数据集 v79 停更——两者可安全视为终态。
4. **情报增量**：elrensmin/kaggriculture-not-good-sub2k（09-30 新仓）含 GAME_DYNAMICS.md 实测机制赔付+12 公开对手克隆+**DSM 榜一 123 局录像对标文档**（无许可，只登记）；graceyunliu 09-30 报告（自报）：自进化头部候选对前沿 +$15~16k/20-0 但**全部输给 clone panel −$11~13k**——"打不过镜像是普遍难题"我方 80% 镜像内耗发现获第三方同证。
5. **可复用资产（面向后续战役）**：MIT 三件套——smdesai27/TxhmPokerAgent（行为门评测+K-best league+NashConv 尺）、The-DuO-0/dog_matist（持久化 self-play 联赛+谱系追踪）、Seyamalam/Kaggriculture（败因归因 harness+席位互换锦标赛+诚实口径声明）；无许可中件：sweeden-ttu MuZero（PFSP 联赛）、elrensmin DSM 对标法、Aayush033 市场套利（MIT，数字存疑）。

## 三、两件新公开件的紧急池测判决（同日实测，详见证据 JSON）

| 件 | 判决 | 面板读数 | 结论 |
|---|---|---|---|
| godv7（flexonafft 重打包 leoprovorov god-s-mode v7） | **WEAK** | vs oc_c3 0.25 / c_final 0.208 / s8 0.167 / r40 0.083 / A 0.083（12 fold 双席/对，中性块 674000+i*131，sim 30/30 认证，0 异常） | 自报 2604.3 **不可迁移**（"自报≠可迁移"第 7 例）；弱锚面崩盘=池内真实弱势；不进计分对 |
| haodou V94（镜像门定稿件） | **COMPETITIVE** | vs oc_c3 0.4583 / c_final 0.4167 / r40 0.667 / A 0.917；镜像场景 vs V82 0.4375 / vs H1 0.4375（8 fold） | 镜像门触发率 78.5% 仍赢不了（−50/−54 margin），"仅同血脉触发"自报口径不成立；低于我方现件；不进计分对 |

证据：`fn_work/legacy_software/kaggle_simulations/orderbook_godv7_lab/evidence/godv7_arena.json`（120 局）、`orderbook_v94_lab/evidence/v94_arena.json`（128 局）；原始拉取物+provenance 归档 `references/ext/godv7/`、`references/ext/haodou_v94/`（INDEX 已登记）。

## 四、来源清单（均 2026-09-30 16:1x-16:3x UTC=2026-10-01 CST 抓取）

| # | 来源 URL | 通道 | 版本/戳 |
|---|---|---|---|
| S1 | https://www.kaggle.com/competitions/kaggriculture/leaderboard | CLI CSV | 2026-09-30T16:11:16Z |
| S3 | https://www.kaggle.com/competitions/kaggriculture | CLI describe | deadline 2026-09-30T23:59:00Z；teamCount 10217 |
| S4 | https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger | kernels pull | lastRun 09-30 15:56:57，自报 V94 |
| S5 | https://www.kaggle.com/code/leoprovorov/god-s-mode-hacked-stores | kernels list | scriptVersionId=351167531（v7） |
| S7 | https://www.kaggle.com/code/lynnsakurai/farmer-john-and-the-wheat-seller | kernels pull | 09-30 13:05:56 |
| S8 | https://www.kaggle.com/code/flexonafft/kaggriculture-multi-route-farming-agent | kernels pull | 09-30 11:40:14，123 票 |
| S11-S17 | discussion 744614/743993/742571/741281/731587/734000/744277 等 | topics show | 见正文引 |
| S18 | https://www.kaggle.com/datasets/georgymarin/kaggriculture-episodes | datasets API | v79 @ 09-30 00:43:36 |
| G1-G3 | api.github.com/search/repositories?q=kaggriculture 等 | REST | 393 仓快照 2026-10-01 |
| G4 | https://github.com/doanthuan/kaggriculture | commits API | b325122 @ 09-30 00:41:35Z，Apache-2.0 |
| G7-G10 | github.com/Seyamalam/Kaggriculture、smdesai27/TxhmPokerAgent、The-DuO-0/dog_matist、Aayush033/Kaggriculture | REST | 各 push 戳见正文，MIT |
| G5-G6 | github.com/graceyunliu/kaggriculture、elrensmin/kaggriculture-not-good-sub2k | REST | 09-30 push，无许可 |
| 全部 | 逐条 URL 见各 agent 报告留存（本篇为合并快照） | — | — |
