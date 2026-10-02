# postseason-github 原始拉取物 provenance（ext/postseason-github/）

- 来源 URL：api.github.com（search/repositories、search/users、search/gists、repos/*/contents/commits、users/*）、huggingface.co/api、hn.algolia.com/api、news.google.com/rss、bing.com/search?format=rss、reddit/pullpush/ddg/mojeek（拦截证据留存）、dev.to/search/feed、api.crossref.org
- 抓取方式：`gh api`（账号 r-y-ren 已鉴权）+ `curl`；README 经 `repos/{owner}/{repo}/readme`（raw 媒体类型）逐仓拉取
- 抓取日期：2026-10-02 10:40–11:25 UTC
- 重要方法学备忘：**赛名/仓名真实拼写 = kaggriculture（k-a-g-g-r-i-c-u-l-t-u-r-e，双 g）**；本目录 `gh_search_all_p*.json` 为误用单 g 另一拼写的对照语料（14 仓），`gh_search_correct_*.json` 才是 kaggriculture 语料（428 仓）；`query_slug.txt` 保存从在册文档抽取的真实拼写，所有名称敏感查询均自该文件/搜索 JSON 派生（人工键入会静默走样——本次实测教训，见报告 §四）

## 文件清单与 SHA-256（见 SHA256SUMS.txt，共 101 件）

分组：

| 组 | 文件 | 说明 |
|---|---|---|
| GitHub 搜索 | `gh_search_correct_all_p1..p4.json` | kaggriculture 全语料按 updated 排序 400 行（total_count=428） |
| GitHub 搜索 | `gh_search_correct_pushed_post.json` / `gh_search_correct_created_post.json` | 截止后新推送 35 仓 / 新建 15 仓（全量单页） |
| GitHub 搜索 | `gh_search_all_p1.json`、`gh_search_created_since0925.json` 等 | 单 g 拼写对照语料（14 仓）与误查残留（甄别为假信号的证据链） |
| GitHub 搜索 | `gh_search_gists.json`、`gh_search_users_slug.json` | search/gists 端点 404 证据、slug 用户搜索 0 命中 |
| README | `readmes/*.README.md`（35 件）+ `readme_targets.txt` + `readme_fetch_log.txt` | 35 个新推送/新仓 README 全文 |
| 账号 | `users/repos_*.json`（14 账号）、`users_census.tsv`、`users_raw.jsonl` | 账号公共仓清单与存在性普查 |
| 账号 | `target_handles.txt`、`target_probe_raw.jsonl`、`target_probe.tsv` | 64 个榜顶/目标 handle 的 user+repos+gists 探测（自 LB CSV 程序化抽取） |
| 仓普查 | `repo_census.txt`（人工键入，**拼写走样，作废**）、`repo_census2.txt`（文档派生）、`census2_results.tsv`、`repo_census_raw.jsonl` | 在册仓存在性普查：37/39 存活，仅 Kirosamurai 与 XZDang13 两个早已 404 者缺失 |
| 仓普查 | `census2_results.tsv`、`hq_names.txt`、`doanthuan_commits.json`、`doanthuan_repo_obj_from_list.json` | doanthuan 终态 b3251226、高质量仓复核 |
| HF | `hf_models.json`、`hf_datasets.json` | models=1 / datasets=4，lastModified 最新 09-17 |
| 全网 | `hn_stories.json`、`hn_comments.json`、`bing_rss.xml`、`googlenews_rss.xml`、`devto_feed.xml`、`crossref.json` | 零相关命中（bing_rss 为模糊噪声） |
| 全网 | `ddg_all.html`、`ddg_solution.html`、`ddg_lite_all.html`、`bing_all.html`、`bing_week.html`、`mojeek_all.html`、`reddit_*.json`、`reddit_rss.xml`、`pullpush_reddit.json` | 通道拦截/验证码证据（DDG captcha c21b、Bing 反爬、Reddit 403、PullPush 限流） |
| 其他 | `mlk_names.txt`、`query_slug.txt` | MLKaggleTasks 目录清单；真实拼写锚文件 |

## 甄别纪律提示

本目录仅存**公开元数据与 README 全文**（受版权文本，只登记引用不搬运再分发）；无许可（NO-LICENSE）仓的代码一律未 clone/未入库——池测判决需等用户/上游许可裁定。
