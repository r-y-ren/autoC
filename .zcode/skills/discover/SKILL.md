---
name: discover
description: 方向冷启动入口（/discover）：全自动搜索赛事名单→建首批条目→锚点回填→方向全景报告。当用户要启用新方向时使用。
---

# discover：命令入口壳（注册适配）

本技能是 `.zcode/commands/discover.md` 命令的**同名斜杠入口壳**（客户端 `/` 菜单只认技能名，命令文档不参与技能注册——2026-10-10 评审补口）。薄壳不复制流程：

按 `.zcode/commands/discover.md` 流程执行；编排细节调用 direction-discovery 技能（K-09）。

## 产物说明（收尾必做，用户审阅口径）

产物说明：① `config/directions/<方向>.yaml`；② `kb/` 新建条目；③ 方向全景报告；④ `kb/INDEX.md` 登记行。
