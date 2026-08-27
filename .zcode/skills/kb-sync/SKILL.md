---
name: kb-sync
description: 慢循环编排：按方向配置增量维护 KB-1/KB-2。当用户要求同步知识库、触发 /kb-sync、或快循环启动前的强制刷新时使用。
---

# K-01 kb-sync：慢循环编排

## 前置

1. `config/directions/` 至少有一个启用配置（非 `_` 前缀）；没有则按 `_template.yaml` 起草并先询问用户确认方向
2. 读取 `config/budget.yaml` 记下：并发上限、重试限额、限速

## 流程

1. **切阶段**：`python scripts/guard/init_state.py --phase collect --by kb-sync`
2. **紧循环脚本**（按方向执行，任一失败不阻断另一类）：
   - `python scripts/kb/sync_competitions.py`（快照 + 赛事候选）
   - `python scripts/kb/sync_tech.py`（arXiv/GitHub 增量 + 技术候选）
3. **分片派发**（并发 ≤ budget 上限，每分片一个全新子 agent）：
   - Scraper 分片：消费 `kb/raw/candidates/comp-*.yaml`，每分片 ≤5 个候选，按 `.zcode/agents/scraper.md` 章程执行（核实→建/更新 `kb/competitions/<id>/`；每条事实带引用）
   - Hunter 分片：消费 `kb/raw/candidates/tech-*.yaml`，每分片 ≤5 个候选，按 `.zcode/agents/hunter.md` 章程执行（写 `kb/tech/<id>.md` 成品卡片，competition_fit 必填）
4. **收拢**：只收各分片的结构化结论（新增/更新/隔离/待办计数），不收原文；**把已消费的候选队列文件移入 `kb/raw/candidates/processed/`**（队列生命周期：活跃队列只认顶层 tech-*/comp-*.yaml，processed/ 不参与下次去重）
5. **质量闸与索引**：`python scripts/kb/lint_kb.py --quarantine` → `python scripts/kb/build_index.py`
6. **登记**：`kb/INDEX.md` 跑批记录表追加一行；`workspace/JOURNAL.md` 记一行；`git add -A && git commit`
7. **回位**：`python scripts/guard/init_state.py --phase idle --by kb-sync`

## 失败处理

- 子 agent 失败：依 budget 重试一次，仍失败记待办，不阻塞其余分片
- 大量候选超出预算：按信号强度截断，剩余留队列下次跑批（增量语义）
- Hunter 拒绝的候选：要求其把 `{id, reason, stars, decided}` 追加进 `kb/tech/.rejections.yaml` 台账——sync_tech 下轮对台账内候选去重，stars 达快照 ×2 自动放行重评（科技信号随时间增长）

## 纪律

主会话不读 `kb/raw/` 原文；分片粒度 = 条目级；引用纪律与信源分级见 AGENTS.md 铁律 1/5。
