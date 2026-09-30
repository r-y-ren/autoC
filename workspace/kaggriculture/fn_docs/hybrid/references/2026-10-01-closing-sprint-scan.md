# 2026-10-01 收官冲刺速扫（closing-sprint-scan）

- 抓取时间：2026-09-30 23:30-23:38 UTC（提交窗 23:59 UTC 前最后 29 分钟）
- 范围：仅 2026-09-30 19:00 UTC 之后增量；上一轮止点见 `2026-10-01-final-window-sweep.md`、`2026-10-01-lb-sweep6.md`
- 纪律：只读速扫，未做任何在线提交；条目均带来源与时间戳

## 1. 新公开件（kaggle kernels list --sort-by dateRun，抓取于 23:31 UTC）

| lastRunTime (UTC) | ref | 标题 | 作者 | votes | 备注 |
|---|---|---|---|---|---|
| 2026-09-30 23:15:01 | leoprovorov/a-song-of-ice-and-fire-final-update | ❄️🔥 A Song of Ice and Fire \| Final Update | AlekseiProvorov | 103 | 系列收官篇，最高票 |
| 2026-09-30 23:01:45 | destbreso/x-ray-your-agent | X-ray your agent | destbreso | 52 | agent 拆解/诊断向 |
| 2026-09-30 22:06:38 | georgymamarin/kaggriculture-what-2600-farms-do-differently | Kaggriculture \| What 2600+ Farms Do Differently | Georgy Mamarin | 54 | 大样本农场行为分析 |
| 2026-09-30 21:31:03 | anhadmahajan06/kaggriculture-autonomous-ai-farming-agent | Kaggriculture: Autonomous AI Farming Agent | Anhad Mahajan | 23 | 新 agent 公开件 |
| 2026-09-30 19:12:49 | evgendvorkin/kaggriculture-version-31-26-09-bronze-going-up | Kaggriculture. Version 31, 26.09, bronze, going up | Дворкин Евгений Владимирович | 73 | 落在上轮扫描窗口边缘（19:12），补录 |

来源：kaggle CLI `kaggle kernels list --competition kaggriculture --sort-by dateRun`（2026-09-30 23:31 UTC 抓取）

## 2. 讨论区增量（kaggle competitions topics list，23:33-23:36 UTC 抓取）

- 19:00 UTC 后新帖：**未找到**。全量页 1-2（含 `-s new`/`-s recent`）postDate 最新为 744614 "Urgent: Is It Possible to Reactivate a Previous Submission Before the Deadline?"（2026-09-30 14:40 UTC，1 评论）。
- 开源帖 743993 "Will the submissions be open sourced after the competition ends?"（2026-09-28 07:02 UTC）：评论级增量无法经 CLI/WebFetch 核实（WebFetch 仅返回 JS 壳），commentCount 仍为 6（与上轮一致，未见新增）。**官方终评口径澄清新帖：未找到**。
- 注意排序：CLI 对 `-s new/recent` 未见生效差异，若存在仅评论更新的线程可能漏检。

## 3. 开源动作

GitHub API（无需鉴权，23:34 UTC 抓取）：
- `q=kaggriculture pushed:>2026-09-30T19:00:00` → total 6：
  - 2026-09-30T23:25:44Z Amar-Sayed/Maro_Agent-（规则型经济决策 agent，建仓 23:23:01Z）
  - 2026-09-30T21:36:30Z the-genius-man/kaggriculture-agent
  - 2026-09-30T21:32:16Z amrrs/kaggriculture-feel-the-agi（"final agents, evaluation harness and research note"，建仓 21:30:23Z）
  - 2026-09-30T21:26:50Z jamesidriss/kaggriculture
  - 2026-09-30T21:04:33Z meghanai28/kaggriculture_hybrid
  - 2026-09-30T20:35:37Z Driw0x/Kaggriculture
- `created:>2026-09-30T19:00:00` → total 2（上列 Maro_Agent-、feel-the-agi）。
- 均 0 star，无榜顶队身份线索；未发现 top20 队账号对应开源仓。

HF API（23:36 UTC 抓取）：datasets/models 搜 kaggriculture 最新 lastModified 为 2026-09-17（sweeden-ttu/kaggriculture-season-training）→ 19:00 后增量 **未找到**。

## 4. 榜面终态快照（kaggle competitions leaderboard kaggriculture -d，23:33 UTC 抓取）

| Rank | Team | Score | LastSubmission (UTC) |
|---|---|---|---|
| 1 | M & M & P & Q | 3073.5 | 09-30 15:21 |
| 2 | 6x8 B200 Galaxy Run | 2948.6 | 09-30 14:25 |
| 3 | DECEM | 2933.8 | 09-30 19:08 |
| 4 | DSM | 2916.5 | 09-30 22:53 |
| 5 | Anton Tikhonov | 2864.1 | 09-30 20:42 |
| 6 | Farmcore | 2860.4 | 09-30 23:18 |
| 7 | MarvinTMB | 2853.4 | 09-30 23:08 |
| 8 | TKNP | 2835.9 | 09-30 18:00 |
| 9 | Gemini IS ALL YOU NEED | 2833.9 | 09-30 19:41 |
| 10 | Yizhou | 2823.3 | 09-30 22:14 |
| 11 | CDE | 2821.5 | 09-30 21:34 |
| 12 | Luca | 2815.8 | 09-30 23:05 |
| 13 | Majkel1337 | 2809.0 | 09-30 17:30 |
| 14 | tetsuya & yuanzhe & guoqin | 2801.1 | 09-30 22:03 |
| 15 | 😗アナコンダ🤭 | 2769.9 | 09-30 20:44 |
| 16 | monsaraida | 2769.8 | 09-30 08:17 |
| 17 | Boey | 2766.3 | 09-30 18:42 |
| 18 | Christoffer Thimsen | 2759.2 | 09-30 23:19 |
| 19 | . | 2759.0 | 09-30 14:49 |
| 20 | mtmr_s1 | 2753.6 | 09-30 13:25 |

我方（官方榜单读数，非自报）：**rank 1715 / renyxin / 1646.1 / 末次提交 09-30 23:26:44 UTC**（榜 CSV 行 1716，全量解压于 lb_final/）。

## 5. 判读

19:00 后增量以"收官展示型"公开件为主（leoprovorov 终更、destbreso 拆解工具、georgymamarin 行为分析），无 top20 队可直接回收的策略开源、无官方终评口径新澄清；冲刺窗内可行动增量**基本为零**，维持现有终态即可。
