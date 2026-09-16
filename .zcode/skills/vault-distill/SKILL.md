---
name: vault-distill
description: 一次性有监督跑批：把 my_LLM_valut 深度精读库按比赛相关性提炼成 kb/tech 技术卡（K-10 full-build 模式 + 分支隔离 + bib 回填溯源）。仅在用户显式发起 vault 提炼时使用；完成后本技能随升级收尾清理。
---

# vault-distill：my_LLM_valut 一次性提炼跑批（升级票04 管线 / 票05 执行）

## 定位与不变量

- **一次性**有监督跑批，复用 K-10 full-build 模式（停 cron、配额豁免、分片派发、波次 commit 断点可续），非 cron 常态。
- 铁律 1 受控例外（AGENTS.md）：产物卡 sources 用 **paper-distill 形态**——论文标题必标，DOI/URL 从 bib 尽力回填，回填不到留空，**禁止编造**。
- 溯源链：wiki 论文页 frontmatter `sources: ../raw/markdown/<citekey>.md` → citekey → `kb/raw/vault-bib-map.yaml`（由 `scripts/kb/vault_bib_backfill.py` 生成）。

## 前置

1. 升级票 02 已落地（tech-card schema 含 4 枚举 + paper-distill sources）；
2. `git status --short` 为空、state phase=idle；
3. 两台机器的 kb-deep-sync cron 均已暂停（无人值守窗口声明，结束恢复）。

## 流程

0. **建分支**：`git checkout -b batch/vault-distill`（多机安全：跑批窗口另一台不碰 kb，完成合并前 main 无半成品）。
1. **回填准备**：`python scripts/kb/vault_bib_backfill.py`（535 条目、DOI 覆盖 ~91%，实测 2026-09-16；产物在 kb/raw/ 不入库）。
2. **清点与归并**：扫 `wiki/`（384 页）——**以论文页为主建卡单元**；概念页（通常 <30 行、tags 含"概念"）不独立成卡，折叠进其锚定论文卡的"关联概念"节；`tags` 含"归档/示例"的页直接跳过。
3. **方向交集筛选（可审计）**：每张候选卡判断与 kb 现有 directions 的交集（UAV/MEC/SAGIN/FL/LLM 前沿 ↔ 智慧农业·创新创业 / 黑客松 / 数模 / Kaggle）。收录/拒绝决策**逐条落 `kb/tech/.rejections.yaml`**（拒绝理由必含交集判断依据）；`competition_fit` 写不出有说服力映射 → 拒收。
4. **切阶段**：`python scripts/guard/init_state.py --phase collect --by vault-distill`。
5. **分片派发**（并发 ≤ budget.max_subagents_per_batch；每分片 ≤8 个论文页，每片一个全新 hunter 子 agent）。任务包必备条款：
   - 按 tech-card schema 建卡：`venue_tier/evidence_tier/paper_role/reproducibility_level` **强制**（从 valut 页 frontmatter 同名字段迁移）；`id`=citekey（规范化）；`published`=bib year-01-01 并在正文注明"仅年份已知"；
   - sources 用 paper-distill 形态：`paper_title`（bib 回填标题，回填不到用 valut 页名）+ `doi`（有则填）+ `distilled_from: my_LLM_valut` + `distilled_date`；
   - 正文含：单行摘要 / 方法快照 / 比赛映射要点 / 关联概念（折叠的概念页）/ 溯源说明；
   - `signal` 空值字段（stars/citations_90d）**省略不写**（schema 为 integer，null 不过 lint——样本实测教训）；
   - 拒收的分片内条目按第 3 步格式回传，由主会话统一落台账。
6. **波次推进**：每波结束 `lint_kb.py --quarantine` + `build_index.py` + 一条 commit（断点可续；中断恢复从 INDEX 跑批表与 commit 历史定位）。
7. **质量闸**：全量完成后 `lint_kb.py` 0 不合格、INDEX 收录全部新卡、`.rejections.yaml` 完整。
8. **合并回位**：`git checkout main && git merge batch/vault-distill && git push`；恢复两机 cron；`init_state --phase idle --by vault-distill`；INDEX 跑批表追加一行（类型=vault-distill，成本列必填）。
9. **通知用户**：跑升级票 06（删除 my_LLM_valut 的前置校验 = 第 7 步三项全绿）。

## 边界

- `raw/` 未编译论文原则上**不提炼**（wiki 页已是其编译产物）；仅当拒收台账显示某方向卡不足时例外回补。
- 原始语料宁缺毋滥：拒绝理由不含交集判断依据的拒收记录视为不合格，复核重写。
