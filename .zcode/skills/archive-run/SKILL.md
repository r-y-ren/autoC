---
name: archive-run
description: 归档编排：安全检查通过后将 workspace 整体固化到 archive/（git tag）、复位工作区与状态。当验收通过、用户触发 /archive 时使用。
---

# K-05 archive-run：归档与复位

## 流程

1. **预检**：`python scripts/verify/archive_campaign.py --dry-run` 展示归档名/清单/tag，呈用户过目
2. **确认后执行**：`python scripts/verify/archive_campaign.py`（pending_manual 需加 `--allow-manual` 并先告知用户含义；脚本内完成 add+commit+tag，tag 快照含归档内容）
3. **收尾**：
   - 核对 `git tag --contains` / `git ls-tree <tag> --name-only` 确认 **tag 指向的提交包含归档内容**（验内容不验存在）
   - 状态已由脚本复位为 idle
4. 向用户报告：归档路径、tag 名、人工遗留项（如有）

## 纪律

- 归档是不可逆节点：fail 状态拒绝归档（脚本已拦），不要用 --force 绕过用户知情
- 归档后 archive/ 只读（守卫全局不变量）；复盘请读 archive 内的 report.md 与 JOURNAL
