---
name: kb-deep-sync
description: 每周深度评估：老化条目重验、拒绝台账复核、quarantine 清理、INDEX 全量重建、winners/patterns 解构推进。当周六深度 cron 触发或用户要求深度同步知识库时使用。
---

# K-08 kb-deep-sync：每周深度评估（DESIGN §3.1 双频承诺的"每周深度"半边）

与每日轻量增量（K-01）的区别：不追求新候选量，追求**存量质量与解构深度**。配额可用每日的 2-3 倍。

## 流程

0. **预检（无人值守自检）**：`git status --short` 应为空（有未提交变更先查明原因再继续）；`state.json` phase 应为 idle，不是则查明上一跑批是否中断
1. **切换**：`python scripts/guard/init_state.py --phase collect --by kb-deep-sync`
2. **老化重验**：扫描 KB 条目 `last_verified`，超过 14 天的列入重验分片（Scraper 派发，重点：关键日期/AI 政策等易变字段）
3. **拒绝台账复核**：读 `kb/tech/.rejections.yaml`——stars×2 自动重评由 sync_tech 处理；本步抽查拒绝理由质量，明显误拒的标记下轮重评
4. **quarantine 清理**：逐条处置 `kb/quarantine/`（修复重写或删除），处理记录进 INDEX 跑批表
5. **winners/patterns 推进**：选 1-2 个赛事推进历年获奖解构（每分片一个年份），从 `config/templates/patterns-template.md` 生成/更新 patterns.md；扫描件 PDF 先过 `scripts/kb/ocr_pdf.py`
6. **INDEX 全量重建**：`python scripts/kb/build_index.py`（跑批表自动保留）
7. **登记收尾**：INDEX 跑批记录追加（类型=deep）、JOURNAL 记行、git commit、`init_state --phase idle --by kb-deep-sync`
8. **简报导出（D6 交付层，idle 后执行）**：`python scripts/kb/export_digest.py`——月末最后一个周六自动转正式版，其余周为草稿；导出后 commit
9. **收尾断言（任一不满足 → JOURNAL 记 warn 行并如实报告，不得静默）**：
   - `python -c "import json;print(json.load(open('.flow/state.json'))['phase'])"` 输出 idle
   - INDEX 跑批表含今日行；`export/digest-*.md` 已更新（本步新增产物）
   - `git status --short` 为空

## 纪律

与 K-01 相同：分片粒度 = 条目/年份级；引用纪律；winners 解构二手信源必须降级标注，宁缺毋滥。
