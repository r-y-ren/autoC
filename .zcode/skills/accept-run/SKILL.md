---
name: accept-run
description: 验收编排：执行蓝图验收清单、失败工单路由回责任角色修复重验（带熔断）、通过后产出分析报告。当用户触发 /accept 或交付完成时使用。v2 起多战役并行，全程 --campaign <cid>。
---

# K-04 accept-run：验收-修复回环（v2 多战役）

## 流程

1. **切阶段**：`python scripts/guard/init_state.py --campaign <cid> --phase verify --by accept-run`
2. **执行器**：`python scripts/verify/run_acceptance.py --campaign <cid>`
   - 带 cmd 的验收项自动执行并存证据（<战役根>/acceptance/evidence/）
   - 不带 cmd 的项输出 pending：由你以 **acceptor 章程**逐项核验（browser-use 实测截图、读产物、查 metrics），把结论补进 run-*.json 并附证据路径——**无证据不判定**
3. **分支**：
   - `pass` → 第 5 步
   - `fail` → 为每个失败项开工单（`<战役根>/acceptance/ticket-<验收ID>-r<n>.md`：失败证据 + 责任角色 + 期望），`init_state --campaign <cid> --phase deliver` 派回责任角色修复，完成后回到第 1 步重验
   - `pending_manual` → 整理 MANUAL_TEST 清单呈报用户，等待人工结果
4. **熔断（战役级）**：仅 **fail** 计入该战役 retry 计数（pending=等待人工/核验，不是修复回环；T2.1 裁决）；`retry.count ≥ retry.max`（执行器自动置 tripped）→ **停止自动重试**，向用户呈报全部失败证据与已尝试记录，等待人工决策。cmd 类验收项超时（默认 600s）自动记 fail 并存 TIMEOUT 证据
5. **分析报告**：`<战役根>/acceptance/report.md`——**按 `config/templates/report-analysis-template.md` 六节产出**（评审标准自评/赛点检查表核对/历年基准对比/人工项/人机分工合规留痕/可复用资产清单；数字仅引该战役 metrics.json）；JOURNAL 记行 + git commit
6. 提示：`/archive <cid>`

## 纪律

验收者不修作品（裁判不做运动员）；不放宽清单；manual 项不得自行判定通过；并行战役各自独立验收与熔断，工单/证据不得跨战役混放。
