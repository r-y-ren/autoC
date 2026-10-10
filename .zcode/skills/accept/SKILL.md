---
name: accept
description: 验收入口（/accept）：执行战役验收清单（cmd 自动执行+取证），失败开单回人工修复（熔断按战役独立）。当用户要终检验收时使用。
---

# accept：命令入口壳（注册适配）

本技能是 `.zcode/commands/accept.md` 命令的**同名斜杠入口壳**（客户端 `/` 菜单只认技能名，命令文档不参与技能注册——2026-10-10 评审补口）。薄壳不复制流程：

按 `.zcode/commands/accept.md` 流程执行；编排细节调用 accept-run 技能（K-04）。

## 产物说明（收尾必做，用户审阅口径）

产物说明：① `<战役根>/acceptance/run-N.json`；② `report.md`；③ `evidence/` 证据文件；④ 失败工单（如有）。
