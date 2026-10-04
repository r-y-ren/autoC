# hustleailab 文换通道重试 provenance（teardown-wave1/hustleailab/）

- 来源 URL：`https://hustleailab.com/kaggriculture-win-5000-by-teaching-an-ai-to-run-a-farm-yes-its-real/`（自上轮 Brave 存档正则派生，存 `../urls_hustle.txt`）
- 抓取时间：**2026-10-03 06:08–06:10 UTC**
- 上轮状态：curl/WebFetch 双路 403（Cloudflare JS 墙）、Wayback 无快照——"内容未核实"（monitor-round2-github §三.4）

## 本轮通道矩阵（8 路）

| # | 通道 | 结果 | 证据 |
|---|---|---|---|
| 1 | curl + Chrome UA（-L） | **403**（5,887B Cloudflare 挑战页） | `try1_chrome.html` |
| 2 | curl 不跟随重定向 | **403**（5,656B） | `try2_noredirect.html` |
| 3 | 直接 IP + Host 头（66.235.200.147） | **403**（151B——Cloudflare SNI/指纹校验，非源站） | `try7_directip.html` |
| 4 | **r.jina.ai reader 代理** | **200，全文 4,021B markdown**——唯一命中通道 | `article_via_jina_reader.md` |
| 5 | Wayback availability API | 仍空 `{"archived_snapshots": {}}` | `try5_wayback.json` |
| 6 | Wayback CDX（prefix 通配） | 空 `[]` | `try6_cdx.json` |
| 7 | Google webcache | 200 但返回通用 Google Search 页（cache 服务已下线，无快照） | `try8_gcache.html` |
| 8 | RSSHub（rsshub.app/hustleailab） | 403 | `try9_rsshub.xml` |

## 正文核实结论（经 jina 通道，2026-10-03 首次全文到手）

- 页面 Title（jina 读出）："Kaggriculture: $50,000 Kaggle AI Challenge Explained"；**Published Time: 2026-08-07T10:32:25+00:00**
- 内容定性：**launch 期赛事介绍/PR 文，非赛后拆解**——全文为"比赛是什么/奖金结构/为何 agentic AI 值得做"三层，无任何策略细节、成绩自报或复盘教训（与上轮"从标题判为赛事介绍/PR 口径可能性大"的预判一致）
- 与拆解潮的关系：**不计入拆解潮第 5 篇**；其价值仅剩"赛事奖金结构第三方转述"一条
- 自报数字（未复核）：奖金池 $50,000、Top 10 每队 $5,000（与官方页核对未做——登记待核；注意 Brave 索引标题"Win $5,000"与此一致）
- 许可：页面无明示 license；jina 通道系第三方代理渲染，正文版权归原站——只存档通道产物与摘引，不再分发

## 通道纪律备注

r.jina.ai 为第三方 reader 代理：正文经其转写（markdown 化），非源站原始字节——**同源校验**：文中奖金数字与 Brave 索引标题（"Win $5,000"）互证；URL/发布时间由 jina 头部元数据给出。若需源站原字节级证据，仍待 Wayback 未来收录。
