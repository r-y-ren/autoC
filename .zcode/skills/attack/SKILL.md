---
name: attack
description: 参考方案供给入口（/attack）：刷新 KB→对比矩阵与三节方案书（赛事/方案/技术栈，纯参考）落 kb/briefs/。当用户要参赛参考、赛事推荐、制定方案时使用。
---

# attack：命令入口壳（注册适配）

本技能是 `.zcode/commands/attack.md` 命令的**同名斜杠入口壳**（客户端 `/` 菜单只认技能名，命令文档不参与技能注册——2026-10-10 评审补口）。薄壳不复制流程：

按 `.zcode/commands/attack.md` 流程执行；编排细节调用 strategy-gen 技能（K-02）。

## 产物说明（收尾必做，用户审阅口径）

产物说明：① `kb/briefs/<日期>-<赛事slug>-<方案slug>.md`；② `kb/briefs/<同slug>-grill-notes.md`；③ `kb/briefs/README.md` 登记行；④ `--to` 时 `<战役根>/docs/briefs/` 副本。
