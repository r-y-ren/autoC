# postseason-platform 原始拉取物 provenance

- 抓取窗口：**2026-10-02 10:39–10:58 UTC**（kaggle CLI 2.2.4 + GitHub REST + curl 全站页探测）
- 任务：`2026-10-02-postseason-platform-scan.md`（赛后平台侧增量扫描，基线=`2026-10-01-closing-sprint-scan.md`，止于 2026-09-30 23:38 UTC）
- 竞赛 slug 取自 INDEX.md 字节精确抽取（`kaggriculture`，k-a-g-g-r-i-c-u-l-t-u-r-e）；拼写错误的 slug 会得到 404/Not found（`kernels_daterun_p1_2026-10-02.json` 即为错拼失败记录，保留作证）

## 文件清单

| 文件 | 内容 | 命令/来源 | 抓取时刻 (UTC) |
|---|---|---|---|
| `describe_2026-10-02.txt` | `competitions describe` 不存在于 CLI 2.2.4 的报错记录 | kaggle CLI | 10:40 |
| `submissions_2026-10-02.csv` | 我方全量提交（首轮，后续 comp_status 再抓一份） | `kaggle competitions submissions -c kagriculture --csv` | 10:40 |
| `comp_status_2026-10-02.txt` | 榜 zip 下载记录 + 我方提交 CSV 复抓 | `kaggle competitions leaderboard -d`、`submissions --csv` | 10:45 |
| `kaggriculture.zip` + `lb_20261002/kaggriculture-publicleaderboard-2026-10-02T10:45:33.csv` | 官方公榜全量（10,246 队，7 列含 TeamMemberUserNames） | `kaggle competitions leaderboard kagriculture -d` | 10:45:33 快照 |
| `comp_list_entered.txt` | 竞赛状态行（deadline 2026-10-14 23:59 / reward 50,000 Usd / teamCount 10246 / userRank） | `kaggle competitions list --group entered -v` | 10:40、10:57 |
| `topics_list_2026-10-02.json` | 竞赛讨论区 topics 全量 5 页（100 帖） | `kaggle competitions topics list kagriculture -p 1..5 --format json` | 10:43–10:44 |
| `topics_key_1.txt` | 745073（M&M&P&Q 预告）、745119（Farmcore）全文+评论树 | `kaggle competitions topics show` | 10:45 |
| `topics_key_2.txt` | 745074/744811/744788/744939/745036 全文+评论树 | 同上 | 10:46 |
| `topics_key_3.txt` | 744858/744814/744819/744999/744988/744823/744820/744808/744786/744790/744791（截前 25 行） | 同上 | 10:46 |
| `topics_baseline_check.txt` | 743993/742571/744614 复查（commentCount 比对） | 同上 | 10:46 |
| `topics_eval_threads.txt` | 731587（官方终评口径帖）+ 742571 全文 | 同上 | 10:46 |
| `kernels_daterun_p1.json` | 本赛 kernel dateRun 排序前 100 | `kaggle kernels list --competition kagriculture --sort-by dateRun --page-size 200 --format json` | 10:43 |
| `kernels_datecreated.json` | 本赛 kernel dateCreated 排序前 100（判新建件） | `kaggle kernels list --competition kagriculture --sort-by dateCreated` | 10:51 |
| `kernels_daterun_p1_2026-10-02.json` | 错拼 slug 的 "Not found" 失败记录（环境注记用） | 同上（slug 错） | 10:41 |
| `authors/authors_scan.txt`、`authors/authors_fix.txt` | 在册 22 作者 + 榜顶成员账号逐人 `kernels list --user` 扫描 | `kaggle kernels list --user <u>` | 10:52–10:53 |
| `datasets_list_2026-10-02.json` | 数据集三次列举（--user / -s kagriculture / -s …-episodes） | `kaggle datasets list` | 10:41、10:51 |
| `episodes_56697824/56708866/56716525/56721419/56721643.json` | 我方 5 件提交的 episode 表（判活跃对/收敛） | `kaggle competitions episodes <id> --format json` | 10:50–10:51 |
| `episodes_activity.txt` | episode 汇总读数 | 上者汇总 | 10:49 |
| `github_and_topic745073_raw.json` | GitHub 搜索原始 JSON ×2 + msdsm/kagriculture-solution 404 证据 + 745073 topic-messages 原文（含 GitHub 链接） | curl api.github.com + `kaggle competitions topic-messages` | 10:53–10:57 |

校验：`SHA256SUMS.txt`（25 文件）。
