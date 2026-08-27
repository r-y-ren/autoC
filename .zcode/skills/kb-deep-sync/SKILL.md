---
name: kb-deep-sync
description: 慢循环全量深度跑批（每 3 天，D7 合并原每日轻量+每周深度）：增量拉取+分片入库、老化条目重验、拒绝台账复核、quarantine 清理、winners/patterns 解构推进、简报导出。当每 3 天 cron 触发或用户要求深度同步知识库时使用。
---

# K-08 kb-deep-sync：慢循环全量深度跑批（D7：每 3 天一次，合并双频）

原"每日轻量（K-01）+ 每周深度（K-08）"双频已合并为本技能的单次全量流程（决策 D7，
2026-08-27）：一次跑批 = 增量拉取 + 存量深度。K-01 保留为手动轻量补偿入口（/kb-sync）。

## 流程

0. **预检（无人值守自检）**：`git status --short` 应为空（有未提交变更先查明原因再继续）；`state.json` phase 应为 idle，不是则查明上一跑批是否中断
1. **切换**：`python scripts/guard/init_state.py --phase collect --by kb-deep-sync`
2. **增量拉取与入库**（原 K-01 第 2-4 步）：
   - `python scripts/kb/sync_competitions.py` + `python scripts/kb/sync_tech.py`（arXiv + gh；gh 已登录）
   - 活跃队列候选分片派发 hunter/scraper（并发 ≤ budget；**深度配额：每方向 ≤5 卡 / ≤3 条目**；遗留候选按 suggested_fields 信号挑选）
   - 已消费队列移 `kb/raw/candidates/processed/`；Hunter 拒绝者进 `.rejections.yaml` 台账
3. **老化重验**：`last_verified` 超 **12 天**的条目派 scraper 分片重验（重点关键日期/AI 政策；阈值对齐 3 天节奏）
4. **拒绝台账复核**：`kb/tech/.rejections.yaml` 拒绝理由质量抽查，明显误拒的标记下轮重评（stars×2 自动重评由 sync_tech 处理）
5. **quarantine 清理**：逐条处置 `kb/quarantine/`（修复重写或删除），处理记录进 INDEX 跑批表
6. **winners/patterns 推进**：选 1 个赛事推进历年获奖解构（每分片一个年份；扫描件先过 `scripts/kb/ocr_pdf.py`；模板 `config/templates/patterns-template.md`）
7. **质量闸与索引**：`python scripts/kb/lint_kb.py --quarantine` → `python scripts/kb/build_index.py`
8. **登记收尾**：INDEX 跑批记录追加（类型=deep）、JOURNAL 记行、git commit、`init_state --phase idle --by kb-deep-sync`
9. **简报导出（D6 交付层，idle 后执行）**：`python scripts/kb/export_digest.py --interval-days 3`——**当月最后一次跑批（下一次跑批跨月）自动转正式版**；导出后 git commit
10. **收尾断言（任一不满足 → JOURNAL 记 warn 行并如实报告，不得静默）**：
   - `python -c "import json;print(json.load(open('.flow/state.json'))['phase'])"` 输出 idle
   - INDEX 跑批表含今日行；`export/digest-*.md` 已更新
   - `git status --short` 为空

## 纪律

分片粒度 = 条目/年份级；引用纪律；winners 解构二手信源必须降级标注，宁缺毋滥；
无新候选且无推进项时不空转派发（记录一行回 idle，简报仍刷新）。
