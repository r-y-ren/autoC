# .zcode/skills/ —— SOP 纯函数技能库（占位）

Phase 2 起逐个落盘。每个技能一个子目录 + `SKILL.md`，规划清单：

- `blueprint-gen/`  从 KB 索引生成对比矩阵与蓝图草稿（decide 阶段）
- `kb-lint/`        KB 条目校验流程（调用 scripts/kb/lint_kb.py）
- `marp-deck/`      从模板生成答辩 PPT
- `typst-report/`   从模板生成项目报告
- `campaign-run/`   快循环阶段编排（状态流转 + 任务包派发）

约束：技能只承载流程（怎么做的顺序与判断要点），不承载状态；状态一律落 `.flow/` 与 `workspace/JOURNAL.md`。
