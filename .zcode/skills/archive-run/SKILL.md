---
name: archive-run
description: 归档编排：安全检查通过后将单个战役整体固化到 archive/（项目仓库 commit+tag+push，主库零提交）、注销该战役并复位其状态。当验收通过、用户触发 /archive 时使用。v2 起多战役并行，归档互不影响。
---

# K-05 archive-run：归档与复位（v2 多战役，git 拆分后口径）

归档对象是**单个战役**（`--campaign <cid>`）：该战役根整体移入 `archive/<YYYY-MM>_<赛事名>_<主题>/`（`.git`/`.gitignore` 随目录搬移）；
其余战役与其目录不受影响。**git 口径（2026-10 拆分后）**：commit + tag 落项目仓库，主库零提交；
项目库有 origin 时脚本会 push 分支与 tag——远程即归档证据链。

## 流程

1. **预检**：`python scripts/verify/archive_campaign.py --campaign <cid> --dry-run` 展示归档名/清单/tag，呈用户过目
2. **确认后执行**：`python scripts/verify/archive_campaign.py --campaign <cid>`（pending_manual 需加 `--allow-manual` 并先告知用户含义；脚本内完成项目库 commit+tag+push，tag 快照含归档内容；无库的 legacy 战役在目标位补建快照库）
3. **收尾**：
   - 在**归档目录**（项目仓库）核对 `git -C <归档目录> ls-tree <tag> --name-only` 确认 **tag 指向的提交包含归档内容**（验内容不验存在）
   - 核对 push 结果（脚本输出"已 push"或 [warn]；warn 时手动 `git -C <归档目录> push --tags` 补推）
   - 核对主库零提交：`git log --oneline -1` 无变化、`git status` 干净
   - v2 战役：战役目录已删除、注册表条目已注销（`init_state --campaign <cid> --close` 由脚本调用）；legacy 战役（root=workspace）：workspace 复位为多战役容器 README
4. 向用户报告：归档路径、tag 名、项目库远程、人工遗留项（如有）、剩余在役战役清单

## 纪律

- 归档是不可逆节点：fail 状态拒绝归档（脚本已拦），不要用 --force 绕过用户知情
- 归档后 archive/ 只读（守卫全局不变量）；归档目录自带 `.git`，历史与 tag 随身，复盘请读 archive 内的 report.md 与 JOURNAL
- 并行战役禁止"搭车"归档：一次一个战役，各自的验收闸门独立满足
