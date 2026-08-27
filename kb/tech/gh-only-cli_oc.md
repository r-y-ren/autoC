---
id: gh-only-cli_oc
name: "oc (only-cli): 把任意网站压缩成 AI agent 可浏览的紧凑 CLI"
field: [LLM agents, retrieval augmented generation]
directions: [黑客松与数据竞赛]
published: "2026-08-18"
maturity: demo
signal:
  venue: GitHub
  stars: 328
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "一切'agent 需要联网查资料/读文档/采集数据'的黑客松项目的即插即用信息入口层：`oc open` 把页面渲染成编号动作 + 默认 500 token 预算视图，官方基准 15 个真实页面全通读（Jina Reader/Playwright MCP/curl 均被反爬挡住）且 token 比 raw HTML 省 142×、比 Jina 省 14×；25+ 站点快捷命令（hn/reddit/gh/wiki/各家语言文档）+ cookie 会话 + 代理支持，一行 npx 接入 Claude Code/Codex，MIT 许可——对比自建爬虫+清洗+截断方案是数量级的工期差"
    reuse_cost: "低"
    open_source: "https://github.com/only-cli/oc（MIT，npm @only-cli/oc 0.5.0）"
sources:
  - url: https://github.com/only-cli/oc
    title: "only-cli/oc: Turn any website into a compact CLI tailored for AI agents"
    accessed: "2026-08-28"
  - url: https://github.com/only-cli/benchmarks
    title: "only-cli/benchmarks: oc 官方基准方法论与逐任务数据"
    accessed: "2026-08-28"
---

# oc：网页→编号动作 CLI，让 agent 用几百 token 浏览网页

## 是什么

only-cli 2026-08-18 发布的 npm 工具（@only-cli/oc 0.5.0，MIT，registry 实查 2026-08-28）。`oc open <url>` 抓取页面后返回**紧凑编号视图**（标题 + 编号条目 + `actions: do <n> | read <n> | next | raw`）而非 raw HTML 或截图，agent 通过 `oc do/read/find/next` 在预算内翻阅；每页默认预算 500 token。请求经 impers 库模拟 Chrome TLS 指纹以绕过挡 naive fetcher 的反爬；`clis/` 内置 25+ 站点快捷方式（`oc hn top`、`oc gh repo <o> <n>`、`oc wiki/py/mdn/aws ...`，多借助服务端渲染页/RSS/公开 JSON API/Sphinx 静态索引）；cookie 会话（0600 侧车文件、https-only、默认 1h）支持登录页；代理走标准环境变量并拒绝私网地址。无 JS 渲染能力时以退出码 2 明示"页面无可读文本"而非假装渲染（来源：https://github.com/only-cli/oc README 实抓 2026-08-28）。

## 解决什么问题

agent 联网的三重成本：raw HTML 单页数万至 40 万 token（其基准中 Yahoo Finance 报价页 raw 399,881 token，经 oc 456 token）；现成 reader 被反爬挡（Reddit 挡 curl/Jina/Playwright，DuckDuckGo 挡 lynx）；截图/accessibility snapshot 同样笨重。oc 把"浏览"压缩成数百 token 的结构化动作序列。

## 相比前方法优势

- **实测省 token 且存活率高**：15 页基准中唯一全部返回真实内容的 reader；token 比 raw HTML 省 142×、比 Jina Reader 省 14×、比 Playwright MCP 快照省 49×；
- **端到端任务更便宜**：Claude Code 内 Wikipedia 五连问 $0.27 vs 内置 WebSearch $0.52（各 5/5 正确）；11 项语言文档查询 $0.57 vs WebFetch $0.74（oc 11/11，WebFetch 10/11 且错在 cppreference 403）——注意 Codex (gpt-5.6-sol) 上其自带搜索反而便宜 16%，官方如实披露；
- 比 site-specific 适配器通用：任意静态站零配置；JSON API 端点也按"编号记录"渲染并只保留字段差异。

## 局限（如实标注）

- 自述状态 "Early"：`fill`/`submit`/`back` 未实现（明报而非假装）、无 JS 渲染、硬反爬站可能仍拒接；
- 基准为项目自建（only-cli/benchmarks 仓库可复核），非第三方评审；页面预算是目标值而非硬上限；
- 私网/内网地址被主动拒绝（SSRF 防护设计），内网数据源场景不可用。

## 如何用于比赛

1. **信息检索型 agent 黑客松（主用）**：赛题含"自动调研/情报聚合/文档问答"时，在 agent 指令文件加一行（`npx @only-cli/oc open <url>` 替代 raw HTML 抓取，README 官方推荐姿势，抓取 2026-08-28）即可把上下文预算压到对手的 1/10——同样 200k 窗口，别队读 3 个页面你的 agent 能读 30 个，多轮深挖能力直接碾压。reuse_cost 低：npm 全局装或 npx 直跑，离线测试覆盖读取主路径。
2. **评测方法论复用（Kaggle/算法赛加分项）**：其双口径基准设计（页面 token 成本无模型 + 端到端任务成本含模型，正确率/费用/耗时并列）可直接搬进自项目的评测章节，回应评审"你怎么证明你的 pipeline 更省"。
3. RAG 类赛题衔接：oc 产出的是结构化蒸馏文本而非 HTML，可直接喂检索/摘要环节，省掉自写清洗器。
