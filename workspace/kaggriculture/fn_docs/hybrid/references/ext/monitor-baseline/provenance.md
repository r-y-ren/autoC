# monitor-baseline/ 溯源（监控首档快照，2026-10-02）

抓取窗口 **2026-10-02 12:32–12:37 UTC**（=CST 20:32–20:37）；通道：kaggle CLI 2.2.4 + GitHub REST（`gh api`，r-y-ren 鉴权）。此档=10-07/10-15 两档监控的对照基线。同日早间另有并行件 `2026-10-02-postseason-github-scan.md`（10:40–11:25Z）与 `2026-10-02-postseason-platform-scan.md`（10:39–10:58Z），本档与其做窗口差分。

专名纪律执行记录：竞赛 slug 与 msdsm 仓名均**程序化派生**（slug 取自 `ext/postseason-platform/comp_list_entered.txt` 正则；仓名取自 `search/repositories?q=user:msdsm` JSON）；GitHub 8 handle 拼写与 `2026-10-02-postseason-github-scan.md` 文本逐位核对一致。12:25Z 一次 msdsm 仓探测 404 系本人手键走样名所致（非仓下线），更正后 12:29Z 实抓 ALIVE——教训"专名查询禁手键"再获一例。

| 文件 | 来源命令 | 戳（UTC） | 说明 |
|---|---|---|---|
| topics_list_p1..p3.json | `kaggle competitions topics list <slug> -p 1..3 --format json` | 12:32:56–12:32:58 | 讨论帖列表 3 页 60 帖（按票序分页，含 10-01/10-02 全部新帖） |
| topic_745073.json | `kaggle competitions topics show <slug> 745073 --format json` | 12:33:36 | M&M&P&Q 预告帖正文+9 条评论全文 |
| topic_745073_messages.json | `kaggle competitions topic-messages <slug> 745073 --format json` | 12:33:38 | 带 URL 原文（仓链接+3 GCS 附件图） |
| kaggriculture-publicleaderboard-2026-10-02T12:34:11.csv | `kaggle competitions leaderboard <slug> -d` | 12:34:11 | 全量榜面 10,246 队（zip 解包件） |
| submissions_2026-10-02_1234.csv | `kaggle competitions submissions <slug> --csv` | 12:34:2x | 我方全史提交读数 |
| episodes_56721643.json / episodes_56721419.json | `kaggle competitions episodes <ref> --format json` | 12:36:0x | 两活跃计分件最近对局流（136/123 行） |
| （不落盘，正文引）GitHub REST | repos/msdsm 族、users/{8 handle+变体}、search/{users,repositories} | 12:25:18–12:36:48 | msdsm 仓 meta/commits/releases/contents/readme/docs/git-tree；8 账号+变体探测；alperen 姓名候选抽验 |

sha256 见 SHA256SUMS.txt。许可：Kaggle 抓取物仅情报用途；GitHub README/doc 摘录按引文引用（msdsm 仓 NO-LICENSE，只登记不搬运）。
