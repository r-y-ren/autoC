---
name: direction-discovery
description: 方向冷启动：用户给出新方向描述后，按信源目录自行搜索该方向赛事名单、建立方向配置与首批条目。当用户触发 /discover、要求启用新方向时使用。
---

# K-09 direction-discovery：方向冷启动（框架泛化入口）

职责边界：**发现**新方向的赛事名单并完成首跑入库（常规维护归 K-01/K-08）。
前两类交付物全自动——本技能全程无需用户确认（用户仅通过 /discover 的参数指定方向）。

## 流程

1. **建方向配置**：按 `config/directions/_template.yaml` 建 `<方向名>.yaml`（scopes 按两大类 tier 填；keywords 中英；tech_radar.fields 填 2-3 个技术领域；sources.web 首跑留空）
2. **切阶段**：`python scripts/guard/init_state.py --phase collect --by discover`
3. **搜索分片派发**（并发 ≤ budget.max_subagents_per_batch）：按 `config/sources/catalog.md` 中该类的信源**以信源为分片**派发 scraper 子 agent（冷启动期没有条目可分片）。每个分片返回结构化候选清单（≤10 条：名称/主办方/URL/关键时间/类型判断依据/信源等级），不返回原文
   **SPA 预抓（P1 规则）**：catalog SPA 清单内站点（devpost/kaggle/天池/和鲸/lablab）的关键页面，主会话先 browser-use 抓快照落 `kb/raw/<id>/` 供分片消费；搜索分片仅作线索定位时不受此限，但建条分片的事实必须有直抓原件或独立第二源
4. **候选汇合与筛选**：合并去重 → 按（信息可得性 × 赛事分量 × 时间窗）筛 **≤8 条**（冷启动一次性配额，超出者留 candidates 队列下轮消化）
5. **建条分片派发**：每分片 ≤3 条目，按 scraper 章程建 `kb/competitions/<id>/meta.md`（schema：config/templates/kb-meta.schema.json；tier 填大类；`award_levels` 实抓该赛奖项体系后填写——winners 覆盖标准=前两级）
6. **首样可选**：信息最全的 1 个赛事若公开获奖作品，按 winners-template 做首份深构样例（四节必备，含"不足与可改进点"）
7. **质量闸与索引**：`lint_kb.py --quarantine` → `build_index.py`
8. **锚点回填**：把实抓确认的官网入口写回该方向 yaml 的 `sources.web`（增量维护从此有固定锚点）
9. **登记收尾**：INDEX 跑批记录（类型=discover）+ JOURNAL + git commit + `init_state --phase idle --by discover` + `export_digest.py`
10. **产出全景报告**：该方向赛事数量/时间窗分布/信源缺口/建议下轮推进项（呈报用户）

## 纪律

引用纪律与信源分级照 AGENTS.md 铁律 1；JS 渲染页用 browser-use；失败信源记待办不阻塞；
candidates 队列超配额部分保留（增量语义）；ACM 方向维持边界备忘（只出训练体系类内容）。
