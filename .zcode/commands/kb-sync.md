---
description: 手动触发慢循环：按方向配置增量维护 KB-1/KB-2（编排见 .zcode/skills/kb-sync/SKILL.md）
---

# /kb-sync —— 慢循环入口

执行流程（编排细节见 `.zcode/skills/kb-sync/SKILL.md`）：

1. 读取 `config/directions/*.yaml`（无启用方向时先询问用户并按 `_template.yaml` 创建）
2. `python scripts/guard/init_state.py --phase collect --by kb-sync`
3. 依 budget.yaml 并发上限，按**条目分片**派发 scraper / hunter 子 agent（章程：`.zcode/agents/`）
4. 收拢结构化结论 → `python scripts/kb/lint_kb.py --quarantine` → 重建 `kb/INDEX.md`；**已消费的候选队列文件移入 `kb/raw/candidates/processed/`**（队列生命周期，防重复消费）
5. 在 `kb/INDEX.md` 跑批表追加记录；`workspace/JOURNAL.md` 记一行；git commit
6. `python scripts/guard/init_state.py --phase idle --by kb-sync`

铁律：全程不读 kb/raw/ 原文进主上下文；子 agent 只回结构化结论。
