# monitor-round2-github 原始拉取物 provenance（ext/monitor-round2-github/）

- 抓取窗口：**2026-10-02 18:56–19:35 UTC**（比赛 09-30 23:59 UTC 截止后 ~43h；官方终评窗至 10-14 23:59）
- 通道：GitHub REST（`gh api`，账号 r-y-ren 鉴权）+ `curl`（Brave Search HTML、Bing RSS、Google News RSS、HN Algolia、dev.to、Bluesky public API、StackExchange API、arXiv API、crossref、fxtwitter API、Reddit HTML、Wayback availability）+ kaggle CLI 2.2.4（datasets list）
- 对照基线：`../postseason-github/`（GitHub 语料 428 仓 @10:57Z + 全网零命中）与 `../monitor-baseline/`（12:25–12:37Z 快照）；三件超王座件基线 sha 取自 `fn_work/legacy_software/kaggle_simulations/orderbook_postseason_lab/pieces/{syx,taeyan,romansvet}/provenance.md`
- **专名纪律执行记录**：本目录所有赛名/仓名/handle 查询均程序化派生——赛名 slug 取自 `../postseason-github/query_slug.txt`（k-a-g-g-r-i-c-u-l-t-u-r-e）；五件仓（syx/taeyan/romansvet/carson/debmal）的 owner/repo 与基线 sha 自各 `provenance.md` 正则抽取；msdsm 仓名=owner 自 `../postseason-github/msdsm_full/provenance.md` 抽取 + repo 自 gh 搜索 JSON 匹配该 owner 得出（存 `msdsm_repo_name.txt`）；LB 队名/成员 handle 自 `../monitor-baseline/kaggriculture-publicleaderboard-2026-10-02T12:34:11.csv` 抽取（存 `lb_top_teams.txt`、`lb_top_members.txt`）；web 检索的单 g 拼写变体由派生 slug 程序化变异（sed 's/kagg/kag/'）生成，非手键。全程零手键专名（首扫教训 5 例后第 6 次复核无新增）。

## 文件分组（SHA-256 见 SHA256SUMS.txt，共 147 件）

| 组 | 文件 | 说明 |
|---|---|---|
| GitHub 语料 | `gh2_search_all_p1..p4.json` | q=<slug> 全语料 updated desc 400 行（total=**431** vs 基线 428）+ `gh2_all_names.txt` |
| GitHub 过滤 | `gh2_pushed_post.json` / `gh2_created_post.json` / `gh2_created_after1002.json` | pushed:>09-30=38 / created:>09-30=17 / created:>10-02=0（日界语义，见报告限界） |
| GitHub 变体 | `gh2_case_variant_title.json` / `gh2_case_variant_upper.json` | 大小写变体 431/431（搜索大小写不敏感） |
| 新仓甄别 | `repo_*` / `commits_*` / `contents_*` / `readmes2/{CheungLeeJR,WHmaoxian123,rxymitchy}.*` | 3 件新增/新现仓的元数据+README 全文+提交列表 |
| 新仓甄别 | `releases_WHmaoxian123.json`、`contents_WHmaoxian123_project_all.json`、`tree_WHmaoxian123.json`、`events_WHmaoxian123.json`、`readmes2/WHmaoxian123_*`、`commit_rxymitchy_readme_update.json` | WHmaoxian123 归档 Release 9 assets（2.15GB）+6997 blob 树 + Apache-2.0 逐件 LICENSE 样本；rxymitchy 去 private 标记的 README diff |
| 三件超王座 | `repo3_{syx,taeyan,romansvet}.json` / `commits3_*` / `releases3_*` / `readmes2/3_*.README.md` | HEAD==基线 sha（be16043a/9e7daeb3/4444cc7a）三仓零新增；README 与首扫副本 byte-identical |
| 缺件复测 | `repo3_{carson,debmal}.json` / `commits3_*` / `tree3_*` / `releases3_*` | Carson 303 blob 0 权重 / debmal 1100 blob 无 base/routes.json；两仓 HEAD==基线 sha |
| msdsm 复查 | `repo4_msdsm.json` / `commits4_msdsm.json` / `releases4_msdsm.json` / `tree4_msdsm.json` / `contents4_msdsm_docs.json` / `forks4_msdsm.json` / `readmes2/4_msdsm.README.md` / `msdsm_repo_name.txt` | 150 blob 与本地 msdsm_full 快照逐文件相同；releases=0；forks 2 均无自身提交 |
| 全网-可用通道 | `w_hn_*.json`、`w_gnews_*.xml`、`w_bing*.xml`、`w_devto.xml`、`w_bsky*.json`、`w_so.json`、`w_dsse.json`、`w_arxiv.xml`、`w_crossref.json` | HN/Bluesky/StackExchange/arXiv/crossref/dev.to/Google News 全 0；Bing RSS 模糊噪声 |
| 全网-Brave | `w_brave.html`、`w_brave_q1..q9.html`、`w_brave_team*.html` | **本轮唯一命中通道**：q1-q5 有效（q6-9/team2-5 限流），命中 zhichengyellow/DS_completation/Amey-Thakur/atishaykasliwal/hustleailab/Reddit 1vgvuti/x.com 3 帖等 |
| 全网-拦截证据 | `w_ddglite.html`、`w_ddghtml.html`、`w_mojeek.html`、`w_ecosia.html`、`w_startpage.html`、`w_marginalia.html`、`w_searx.json`、`w_reddit_json.json`、`w_pullpush.json`、`w_medium.html`、`w_oldreddit_rss.xml` | DDG captcha/403、Mojeek 403、Ecosia firewall、Startpage/Marginalia 跳转、SearX 验证码、Reddit JSON 403、PullPush 限流、Medium JS 墙 |
| 拆解文收割 | `w_dscom_retrospective.md`（RETROSPECTIVE.md 全文）、`w_page_zhicheng_postmortem.html`、`w_page_zhicheng.html`、`w_page_atishay.html`、`w_page_hustleailab.html`（Cloudflare 墙残片）、`w_ameythakur_kagri_readme.md`、`w_reddit_thread2.xml`、`w_tweet_*.json`（fxtwitter 3 帖）、`w_wayback_hustle.json` | 4 篇独立拆解正文/元数据 + 推文 3 条（launch 期）+ Reddit 1 帖 |
| 平台交叉 | `w_page_georgymarin_dataset.html`、`lb_top_teams.txt`、`lb_top_members.txt` | Kaggle datasets 线索（CLI list 输出入报告）+ LB 前队名/成员 handle 派生文件 |
| 日志 | `pull_log.txt`、`PULL_END.txt`、`brave_queries.txt` | 各阶段抓取时点 |

## 甄别与版权纪律提示

本目录仅存**公开元数据、README/拆解文正文抓取**（受版权文本，只登记引用不搬运再分发）；WHmaoxian123 的 2.15GB Release 备份、msdsm NO-LICENSE 源码、各仓代码均**未下载入库**；池测/搬运需先过许可裁定（WHmaoxian123 根级无许可、逐件 LICENSE.txt=Apache-2.0；CheungLeeJR/rxymitchy=NO-LICENSE）。
