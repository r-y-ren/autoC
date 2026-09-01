---
name: archive-run
description: 归档编排：安全检查通过后将单个战役整体固化到 archive/（git tag）、注销该战役并复位其状态。当验收通过、用户触发 /archive 时使用。v2 起多战役并行，归档互不影响。
---

# K-05 archive-run：归档与复位（v2 多战役）

归档对象是**单个战役**（`--campaign <cid>`）：该战役根整体移入 `archive/<YYYY-MM>_<赛事名>_<主题>/`；
其余战役与其目录不受影响。

## 流程

1. **预检**：`python scripts/verify/archive_campaign.py --campaign <cid> --dry-run` 展示归档名/清单/tag，呈用户过目
2. **确认后执行**：`python scripts/verify/archive_campaign.py --campaign <cid>`（pending_manual 需加 `--allow-manual` 并先告知用户含义；脚本内完成 add+commit+tag，tag 快照含归档内容）
3. **收尾**：
   - 核对 `git tag --contains` / `git ls-tree <tag> --name-only` 确认 **tag 指向的提交包含归档内容**（验内容不验存在）
   - v2 战役：战役目录已删除、注册表条目已注销（`init_state --campaign <cid> --close` 由脚本调用）；legacy 战役（root=workspace）：workspace 复位为多战役容器 README
4. 向用户报告：归档路径、tag 名、人工遗留项（如有）、剩余在役战役清单

## 纪律

- 归档是不可逆节点：fail 状态拒绝归档（脚本已拦），不要用 --force 绕过用户知情
- 归档后 archive/ 只读（守卫全局不变量）；复盘请读 archive 内的 report.md 与 JOURNAL
- 并行战役禁止"搭车"归档：一次一个战役，各自的验收闸门独立满足
