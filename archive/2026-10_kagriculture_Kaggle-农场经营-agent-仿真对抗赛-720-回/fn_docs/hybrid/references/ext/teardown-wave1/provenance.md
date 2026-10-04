# teardown-wave1 原始拉取物 provenance（ext/teardown-wave1/）

- 任务：dff20b-2 拆解潮收割进复盘轨（拆解潮 4+1 篇全文归档 + 复盘卡 + 基座路线决策书 v2）
- 抓取窗口：**2026-10-03 06:04–06:11 UTC**（比赛 09-30 23:59 UTC 截止后 ~54h；终评窗至 10-14）
- 通道：curl（raw.githubusercontent.com / 站点直抓 / r.jina.ai reader）+ GitHub REST（`gh api`，r-y-ren 鉴权）
- 上游：拆解文清单与 URL 坐标出自 `../2026-10-02-monitor-round2-github.md` §块 5；**专名纪律**——五件 URL 全部自上轮存档文件（`w_page_zhicheng_postmortem.html`/`w_brave*.html`/`w_page_atishay.html`/`w_brave.html`）grep 正则程序化派生，派生产物存本目录 `urls_*.txt`，全程零手键专名。

## 目录结构（五个子目录 + 本 provenance）

| 子目录 | 对象 | 许可 | 拿到面 |
|---|---|---|---|
| `zhichengyellow/` | 中文赛季复盘博客（2026-09-30） | 无明示（个人博客） | **全文**（HTML+MD） |
| `dscom/` | Jin-Zhang-Yaoguang/DS_completation RETROSPECTIVE.md（PR#6 09-30 合并） | 仓 NO-LICENSE | **全文**（raw 原文件，与 10-02 档案逐字节同）+ 仓树/元数据/PR5/PR6 |
| `amey-thakur/` | KAGGLE-COMPETITIONS write-up（README+2 notebooks） | **CC-BY-4.0**（仓根 LICENSE；徽章 Apache-2.0 混态警示） | **全文**（含 CC-BY-4.0 许可文本；署名 Amey Thakur） |
| `atishay/` | atishaykasliwal.com 项目页 + github.com/atishay-kasliwal/kaggriculture | 仓 NO-LICENSE | **全文**（项目页 HTML/MD + 仓 README/submission.py/parity 测试/planner 版本/逐文件行数） |
| `hustleailab/` | hustleailab.com 文（上轮 Cloudflare 墙） | 无明示 | **全文经 jina 通道**（8 路通道矩阵，唯一命中）；定性=launch 期 PR 非拆解 |

各子目录内：`provenance.md`（URL/抓取时间/许可/来源派生链）+ `SHA256SUMS.txt` + 原始件。

## 复核要点（与上轮档案交叉）

- RETROSPECTIVE.md：diff 逐字节同（内容稳定）
- zhichengyellow：正文关键读数与 10-02 档案一致
- atishay"1,738 行"：与仓现状（submission.py 2,279 行/全仓 12,854 行）不符——页面自报口径过期，实测为准
- Amey 仓 pushed_at=09-06：write-up 系**赛前**发布（非赛后复盘）——入卡时降"赛后拆解"定位为"赛中 write-up"
- hustleailab：正文到手，定性反转（PR 介绍文），拆解潮计数维持 4 篇
