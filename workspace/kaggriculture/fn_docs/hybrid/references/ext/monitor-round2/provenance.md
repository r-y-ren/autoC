# monitor-round2/ 溯源（监控二轮增量档，2026-10-02）

抓取窗口 **2026-10-02 18:57–19:13 UTC**（=CST 10-03 02:57–03:13）；通道：GitHub REST（`gh api`，r-y-ren 鉴权）+ kaggle CLI 2.2.4 + HuggingFace 公开 API（urllib）。范围=监控首档（`../monitor-baseline/`，12:25–12:37Z）之后的增量；对照件另有同日早间 `2026-10-02-postseason-github-scan.md` / `-platform-scan.md`。

专名纪律执行记录：竞赛 slug、msdsm 仓名、8+2 handle、track 成员名均**程序化派生**（slug 取自 `ext/postseason-platform/comp_list_entered.txt` 正则；仓名取自 `ext/postseason-github/readmes/msdsm_*.README.md` 文件名拆分；handle 取自 `2026-10-02-monitor-baseline.md` §二表"精确 handle"列正则；track 成员取自 `2026-10-02-ahmed-deepcut.md` TeamId 行正则）。alperen 21 候选、新仓、新数据集全部自 API 返回 JSON 程序化提取。**本档方法学警示 2 例**：①首轮 `gh api repos/...` 一次文件名映射失误致 4 个空壳 .err 件（已删）；②两次手键 repo 名致假 404（CheungLeeJR/rxymitchy 仓直接件探测），改用 listing JSON 的 `url` 字段程序化取址后恢复——"专名查询禁手键"教训累计 7 例。

| 文件 | 来源命令 | 戳（UTC） | 说明 |
|---|---|---|---|
| msdsm_meta.json / _commits / _releases / _tags / _readme / _contents_docs / _contributors / msdsm_git_tree.json | `gh api repos/<msdsm>/<repo>{,/commits,/releases,/tags,/readme,/contents/docs,/contributors}` + `git/trees/main?recursive=1` | 18:57–19:0x | 头号盯防：仓态/权重/许可/写本全量（README 解码另存 msdsm_README.md，11,199B 与首档快照 byte-identical） |
| hf_search.json | HF api models/datasets × {kagriculture×2, msdsm, kagriculture-solution} | 19:0x | 权重三路之 HF 路，全 0 命中 |
| kg_datasets_weightcheck.txt | `kaggle datasets list -s` ×3 | 19:0x | 权重三路之 Kaggle dataset 路，全 0 命中 |
| blockB_users_probe.txt | `gh api users/{11 精确 handle + 3 track 成员}` | 19:0x | 闭源大户 8+2 开号复查 |
| blockB_alperen_candidates.json / blockB_alperen_poll.txt | `search/users q=alperen aydin`（21 候选全量）+ 每人 `users/{u}/repos?paginate` + `gists` | 19:0x | 头号目标全量轮询（首档只抽 10），0 命中 |
| blockB_repo_gates.txt / blockB_newrepos_retry.txt / blockB_newrepos_commits.txt / blockB_newrepos_readme.txt / blockB_knownrepos_activity.txt | `search/repositories`（created:/pushed: 闸 + solution/final 自名件）+ 新仓 commits/readme 程序化取址 | 19:0x | 新仓闸：窗内新仓 1 件（CheungLeeJR），活跃件 4 件 |
| topics_list_p1..p13.json + topics_merged_all.json | `kaggle competitions topics list <slug> -p 1..13 --format json`（全页 247 帖合并排序） | 19:0x | 讨论区全量扫描（首档 3 页 60 帖→本档 13 页 247 帖补全） |
| topic_{745073,745036,745119,745074,731587,744811,745152,745155}.json + 同 id _messages.json | `topics show` / `topic-messages` | 19:0x–19:1x | 增量评论/新帖正文 + 官方口径线（731587/744811） |
| kernels_daterun.json / kernels_datecreated.json | `kaggle kernels list --competition <slug> --sort-by dateRun|dateCreated --format json` | 19:0x | kernel 增量（0 新 run / 0 新建） |
| datasets_search.json / datasets_episodes_search.json / newdatasets_files.txt | `kaggle datasets list -s <slug>|<slug>-episodes --sort-by updated --format json` + `datasets files` | 19:0x | 数据集增量：2 新件；mqingcs files/metadata/下载均 403 |
| lb_download/<slug>-publicleaderboard-2026-10-02T19:11:44.csv（+zip 壳） | `kaggle competitions leaderboard <slug> -d` | 19:11:44 | 榜面全量 10,246 队 |
| submissions_2026-10-02_1912.csv | `kaggle competitions submissions <slug> --csv` | 19:12 | 我方全史提交读数 |
| episodes_56721419.json / episodes_56721643.json | `kaggle competitions episodes <ref> --format json` | 19:12 | 两活跃件对局流（137/152 行，末局至 19:11:45Z） |

sha256 见 SHA256SUMS.txt（payload 件全量，不含本文件与 SHA256SUMS.txt）。许可：Kaggle 抓取物仅情报用途；GitHub README/doc 按引文引用（msdsm 仓 NO-LICENSE，只登记不搬运）；mqingcs 数据集内容不可得，未下载。
