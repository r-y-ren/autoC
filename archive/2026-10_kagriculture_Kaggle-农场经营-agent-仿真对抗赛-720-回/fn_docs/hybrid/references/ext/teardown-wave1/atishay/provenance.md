# atishaykasliwal 项目页 + GitHub 仓 provenance（teardown-wave1/atishay/）

- 项目页 URL：`https://atishaykasliwal.com/projects/kaggriculture/`（自上轮存档 `../monitor-round2-github/w_page_atishay.html` 正则派生，存 `../urls_atishay.txt`）；抓取 **2026-10-03 06:04 UTC**（HTTP 200，无拦截）
- GitHub 仓：`github.com/atishay-kasliwal/kaggriculture`（URL 自项目页 HTML 正则派生，存 `../urls_atishay_gh.txt`）；API 抓取 **06:06–06:10 UTC**
- 发布日期：项目页**无明示**（上轮已记）；仓 created 2026-08-06T19:05:00Z、pushed **2026-08-08T17:00:16Z**（赛后冻结——8 月即停更，**非赛后复盘，系赛中工程页**）
- 许可：**仓 NO-LICENSE**（repo API `license=null`）——只登记与摘引，不搬运代码
- 页面标题："Kaggriculture — A Farming-Game Agent, Built in Phases"（与 Brave 索引描述句 "An agent that plans ahead by simulating the real rules. Nine versions, each built to beat the last" 系同页副题）

## 文件清单

| 文件 | 内容 | 校验 |
|---|---|---|
| `project.html` / `project.md` | 项目页原始 HTML + Markdown 转换 | SHA256SUMS.txt |
| `repo_meta.json` | 仓元数据（license=null、pushed 08-08、Python、314KB） | SHA256SUMS.txt |
| `default_branch.txt` / `tree_blobs.txt` | 默认分支 master + 90 blob 全列（API） | SHA256SUMS.txt |
| `repo_README.md` | 仓 README 全文（25,003 字节：完整规则书——含价格函数 shape/锚定吞吐 T/I0=10,000、商店消耗表、 CARE 银行bonus 机制等） | SHA256SUMS.txt |
| `submission.py` | 提交件源码（**2,279 行**） | SHA256SUMS.txt |
| `test_sim_matches_env.py` | **sim vs 官方引擎逐状态一致性测试**（136 行：同 seed 重放断言 tiles/market/shed/shops/positions 全匹配） | SHA256SUMS.txt |
| `planner_versions.py` | planner 版本谱系（V1/V2 stable specs；import 9+ my_agents 家族） | SHA256SUMS.txt |
| `py_linecounts.txt` / `linecounts_summary.txt` | 56 个 .py 逐文件行数（raw 直拉计数） | SHA256SUMS.txt |

## 页面自报 vs 仓实测（我方复算）

| 项 | 页面自报 | 仓实测（2026-10-03） | 读法 |
|---|---|---|---|
| Python 行数 | "1,738 lines of Python" | submission.py 单文件 **2,279 行**；全仓 .py 合计 **12,854 行**（56 文件） | 页面口径疑似指当时主模块或未含后两次 push；**自报数与仓现状不符**（仓 08-08 冻结后页面未同步或口径不同）——以仓实测为准并标"页面自报不符" |
| 9 版本 | "Nine versions, each built to beat the last" | my_agents/ 含 v7/v8/v9 + 6 个具名策略 + path_planner/market_formula/pass_agent；planner/versions.py 存 V1/V2 阶梯 | 方向相符（版本阶梯存在），精确计数口径未对齐 |
| 逐位对齐模拟器 | "checked turn by turn against Kaggle's own engine" | `tests/test_sim_matches_env.py` 实存（"assert every piece of state matches — not just money, but tiles, market inventory/prices, shed, seeds, town shops, farmer/hand positions"） | **属实**（测试源码在册） |
