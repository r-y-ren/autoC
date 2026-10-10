---
description: 归档当前战役：战役根 → archive/（项目仓库 tag+push，主库零提交），只读冻结
---

# /archive —— 归档入口（v2）

执行流程（编排细节见 `.zcode/skills/archive-run/SKILL.md`；归档器 `scripts/verify/archive_campaign.py`）：

1. 前置检查：`workspace/<cid>/acceptance/` 存在 result=pass 的记录（或用户明确知晓 pending_manual 仍要求归档）
2. 归档动作（脚本化执行，不经 agent 逐文件写；**状态注销由脚本内完成，勿手工流转**）：
   - 目标目录 `archive/<YYYY-MM>_<赛事名>_<主题>/`（战役根连同自身 `.git` 整体搬移）
   - 脚本内完成**项目仓库** commit + tag `archive/<归档名>` + push（commit 先于 tag，保证 tag 快照含归档内容；主库零提交）
3. 收尾核对：项目仓库 tag 已推远程、主库 status 干净；向用户报归档路径、tag 名与项目库远程

铁律：归档后该目录只读（守卫全局不变量）；归档是不可逆节点，前置检查不过必须停下询问用户。
