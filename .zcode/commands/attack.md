---
description: 发起快循环：刷新 KB → 决策（对比矩阵/一鱼多吃/蓝图）→ 等待用户确认
---

# /attack —— 快循环入口

用法：`/attack <赛事ID或方向描述>`（省略参数时先给出建议赛道再让用户选）。

执行流程（K-02 技能固化前按 DESIGN.md §3.2 手工编排）：

1. 先触发一次慢循环增量（`/kb-sync` 的流程）确保决策基于最新 KB
2. 读 `kb/INDEX.md` + `config/profile.yaml`（画像未填先提示用户）
3. 产出两份文档写入 workspace/：
   - `strategy.md`：建议赛道对比矩阵（时间窗×技术契合×通吃度×画像匹配×竞争密度）+ 一鱼多吃路线
   - `blueprint.md`：作品蓝图（范围/技术栈引用 KB-2 卡片/接口契约/里程碑/验收清单/合规检查）
4. `python scripts/kb/lint_kb.py --file workspace/blueprint.md` 校验，不过不得呈报
5. 呈报用户请求确认——**这是全流程唯一人工闸门**；用户要求修改则改后重新校验呈报
6. 确认后交由交付编排（campaign-run，K-03）接管

铁律：蓝图未过 schema 校验禁止请求确认；推荐结论须引用具体 KB 条目 ID，禁止凭印象。
