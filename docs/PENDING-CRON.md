# 待恢复：每 3 天全量深度 cron（D11 全量构建期间暂停）

> 全量构建（W0–W5）完成并收尾后，在新会话中恢复注册（或说"恢复慢循环 cron"），随后删除本文件。

注册规格：CronCreate，cron=`0 9 * * *`，intervalUnit=`daily`，interval=`3`，recurring=true，
title=`autoC 慢循环每3天全量深度（kb-deep-sync）`

prompt（与暂停前最后一版一致，含 T4.4 HF 源后的口径）：

```
执行 autoC 工作区（C:\Users\OSS\Desktop\autoC）的慢循环全量深度跑批（每 3 天一次，SOP 见 .zcode/skills/kb-deep-sync/SKILL.md K-08，以 SOP 为准）。要点：
0) 预检：git status --short 应为空、state.json phase=idle；
0.5) watch 项扫描：检索条目 meta 正文"待办/待核验"中带日期的项（如 XPRIZE 获奖者 2026-09-25 公布后深构、devpost rules 失真批次原件重抓），到期者列为本轮必做；
0.6) SPA 预抓（P1 规则）：本轮要抓的 SPA 站点页面（config/sources/catalog.md SPA 清单），主会话 browser-use 预抓快照落 kb/raw/<id>/ 后交给分片——分片消费本地快照，搜索快照禁作唯一事实源；分片任务包含"返回前 lint_kb --file 自检 PASS"条款；
1) init_state --phase collect --by kb-deep-sync；
2) 增量拉取：sync_competitions.py 与 sync_tech.py（arXiv+gh+HF Papers）→ 候选分片派发 hunter/scraper（并发 ≤ budget.max_subagents_per_batch；配额以 config/budget.yaml quotas 为唯一事实源）→ 已消费队列移 processed/；
3) 老化重验：last_verified 超 12 天条目重验（关键日期/ai_policy）；
4) 拒绝台账 kb/tech/.rejections.yaml 质量抽查；
5) quarantine 处置；
6) winners/patterns 推进：1 个赛事 1 个年份分片（扫描件先过 ocr_pdf.py；模板 patterns-template.md）；
6.5) _surveys 必查（P2）：技术族 ≥3 卡无 survey、或超 30 天、或 maturity 变化 → 派 Hunter 建立或刷新；
7) lint_kb.py --quarantine（含结构 WARN 消化）→ build_index → INDEX 跑批记录追加（类型=deep；成本列必填）→ JOURNAL → git commit → init_state --phase idle；
8) 简报导出（idle 后）：export_digest.py --interval-days 3（当月最后一次跑批自动转正式版），导出后 git commit；
9) 收尾断言（任一不满足 → JOURNAL 记 warn 不得静默）：phase==idle、INDEX 跑批表含今日行、digest 已更新、git status --short 为空。
收尾后 git push（origin=r-y-ren/autoC 私有仓）。
纪律：遵守 AGENTS.md；宁缺毋滥；无新候选无推进项则记录一行回 idle（简报仍刷新）。
```
