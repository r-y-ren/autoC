---
description: 归档当前战役：workspace → archive/（只读+git tag），复位 workspace 与状态
---

# /archive —— 归档入口

执行流程（K-05 技能与 archive_campaign.py 固化前按 DESIGN.md §3.5 手工编排）：

1. 前置检查：`workspace/acceptance/` 存在 result=pass 的记录（或用户明确知晓 pending_manual 仍要求归档）
2. `python scripts/guard/init_state.py --phase archive --by archive`
3. 归档动作（脚本化执行，不经 agent 逐文件写）：
   - 目标目录 `archive/<YYYY-MM>_<赛事名>_<主题>/`
   - 移入 workspace/ 全部内容（含 strategy/blueprint/JOURNAL/metrics/四角色目录）
   - `git add` 归档目录 + `git tag archive/<YYYY-MM>_<赛事名>_<主题>`
4. 复位：重建 workspace/ 骨架（README + 各角色子目录）；`init_state --phase idle --reset --by archive`
5. JOURNAL 终结行 + git commit；向用户报归档路径与 tag 名

铁律：归档后该目录只读（守卫全局不变量）；归档是不可逆节点，前置检查不过必须停下询问用户。
