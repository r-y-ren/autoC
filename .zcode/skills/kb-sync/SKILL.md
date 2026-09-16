---
name: kb-sync
description: 慢循环编排：按方向配置增量维护 KB-1/KB-2。当用户要求同步知识库、触发 /kb-sync、或快循环启动前的强制刷新时使用。
---

# K-01 kb-sync：慢循环编排

## 前置

1. `config/directions/` 至少有一个启用配置（非 `_` 前缀）；没有则按 `_template.yaml` 起草并先询问用户确认方向
2. 读取 `config/budget.yaml` 记下：并发上限、重试限额、限速

## 流程

0. **预检（无人值守自检）**：`git status --short` 应为空（有未提交变更先查明原因再继续）；`state.json` phase 应为 idle，不是则查明上一跑批是否中断
0.5. **SPA 预抓（P1 规则）**：核对本方向 `sources.web` 锚点与 `config/sources/catalog.md` 的 SPA 清单——命中 SPA 站点的待抓页面，先由主会话用 browser-use 抓快照落 `kb/raw/<id>/`，再把快照路径写进分片任务包（分片消费本地快照，不上网）
1. **切阶段**：`python scripts/guard/init_state.py --phase collect --by kb-sync`
2. **紧循环脚本**（按方向执行，任一失败不阻断另一类）：
   - `python scripts/kb/sync_competitions.py`（快照 + 赛事候选）
   - `python scripts/kb/sync_tech.py`（arXiv/GitHub 增量 + 技术候选）
   - `python scripts/kb/inbox_intake.py`（投递箱消费：kb/inbox/ 已溯源资料并入本轮候选队列 `inbox-comp-*/inbox-tech-*`，未溯源进 raw/leads 并点名催补；"与活跃战役相关"提示只在战役会话人工裁决，本跑批不改战役文件）
3. **分片派发**（并发 ≤ budget 上限，每分片一个全新子 agent）：
   - Scraper 分片：消费 `kb/raw/candidates/*comp-*.yaml`（含 inbox-comp-*），每分片 ≤5 个候选，按 `.zcode/agents/scraper.md` 章程执行（核实→建/更新 `kb/competitions/<id>/`；每条事实带引用）
   - Hunter 分片：消费 `kb/raw/candidates/*tech-*.yaml`（含 inbox-tech-*），每分片 ≤5 个候选，按 `.zcode/agents/hunter.md` 章程执行（写 `kb/tech/<id>.md` 成品卡片，competition_fit 必填；inbox 来源候选无 URL 溯源不得建卡）
4. **收拢**：只收各分片的结构化结论（新增/更新/隔离/待办计数），不收原文；**把已消费的候选队列文件移入 `kb/raw/candidates/processed/`**（队列生命周期：活跃队列只认顶层 *comp-*.yaml / *tech-*.yaml（含 inbox-* 投递队列），processed/ 不参与下次去重）
5. **质量闸与索引**：`python scripts/kb/lint_kb.py --quarantine` → `python scripts/kb/build_index.py`
6. **登记**：`kb/INDEX.md` 跑批记录表追加一行；`workspace/JOURNAL.md` 记一行；`git add -A && git commit`
7. **回位**：`python scripts/guard/init_state.py --phase idle --by kb-sync`
8. **收尾断言（任一不满足 → JOURNAL 记 warn 行并如实报告，不得静默）**：
   - `python -c "import json;print(json.load(open('.flow/state.json'))['phase'])"` 输出 idle
   - INDEX 跑批表含今日行
   - `git status --short` 为空

## 失败处理

- 子 agent 失败：依 budget 重试一次，仍失败记待办，不阻塞其余分片
- 大量候选超出预算：按信号强度截断，剩余留队列下次跑批（增量语义）
- Hunter 拒绝的候选：要求其把 `{id, reason, stars, decided}` 追加进 `kb/tech/.rejections.yaml` 台账——sync_tech 下轮对台账内候选去重，stars 达快照 ×2 自动放行重评（科技信号随时间增长）

## 纪律

主会话不读 `kb/raw/` 原文；分片粒度 = 条目级；引用纪律与信源分级见 AGENTS.md 铁律 1/5。
