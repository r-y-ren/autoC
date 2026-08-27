---
description: 方向冷启动：搜索新方向的赛事名单并完成首跑入库（K-09 编排，前两类交付物全自动）
---

# /discover —— 方向冷启动入口

用法：`/discover <方向描述>`（如 `/discover 黑客松与数据竞赛`、`/discover 挑战杯类创新创业`）。

执行流程（编排细节见 `.zcode/skills/direction-discovery/SKILL.md`）：

1. 建方向配置 `config/directions/<方向名>.yaml`（按 _template）
2. `init_state --phase collect --by discover`
3. 按 `config/sources/catalog.md` 以信源为分片并发派发搜索（scraper 章程；结构化候选清单返回）
4. 汇合筛选 ≤8 条（冷启动一次性配额）→ 建条分片（meta 过 kb-meta.schema，含 award_levels 奖项体系）
5. 信息最全赛事可选做 winners 首样深构（winners-template 四节必备）
6. lint → build_index → 官网锚点回填 sources.web → 跑批记录/JOURNAL/commit → idle → 简报刷新
7. 呈报方向全景报告（赛事数/时间窗分布/信源缺口/下轮推进建议）

铁律：全程无需用户确认（前两类全自动）；但**发现 ≠ 深化**——深构推进仍走 K-08 配额；
ACM 方向只出训练体系类内容（边界备忘）。
