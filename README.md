# autoC — 竞赛情报与作品生成 Agent 框架

面向学科竞赛（挑战杯/互联网+/大创/数模）与编程黑客松（ACM/Kaggle/Hackathon）的自动化赛事情报与作品交付工作区。

- **交付物 1**：目标赛事名单 + 历年获奖标杆解构（`kb/competitions/`，增量维护）
- **交付物 2**：前沿科技资产库（`kb/tech/`，增量维护）
- **交付物 3**：按战役生成的攻略 + 完整作品 + 分析报告（`workspace/` → `archive/`，归档不可变）

结构设计：[docs/DESIGN.md](docs/DESIGN.md)｜全局纪律：[AGENTS.md](AGENTS.md)｜环境基线：[docs/ENVIRONMENT.md](docs/ENVIRONMENT.md)

## 快速开始

```bash
# 1. 全新克隆后的守卫引导（.flow/ 不入库，缺状态时守卫 fail-closed 全只读）
python scripts/guard/init_state.py

# 2. 阶段流转（由阶段命令/协调者调用，agent 不得手改 .flow/state.json）
python scripts/guard/init_state.py --phase collect --by <命令名>
```

## 工作流一览

```
慢循环（cron）: Scraper+Hunter 并发 → kb/ 增量 → lint → git
快循环（按需）: 指定方向 → 刷新KB → Strategy(矩阵+蓝图) → [用户确认] → 并发交付
              → 验收(失败工单回环,带熔断) → archive/ 归档(脚本,只读+tag)
```

六个阶段与守卫策略：`idle / collect / decide / deliver / verify / archive`（见 `scripts/guard/guard_path.py` 头注）。

## 目录

```
.zcode/     客户端原生配置（hooks=守卫, skills, agents）
.flow/      运行时状态（gitignore；init_state.py 引导）
config/     画像/预算/方向订阅 + templates/(Schema 与文档模板)
scripts/    kb=慢循环脚本 | guard=守卫 | verify=验收与归档
kb/         INDEX.md 总索引 + competitions/ + tech/ + quarantine/ + raw/(不入库)
workspace/  当前战役：strategy/blueprint/JOURNAL/metrics + 各角色目录
archive/    历史作品库（只读，git tag）
```

## 当前状态

- [x] Phase 0：骨架、铁律、守卫钩子、契约模板、环境基线
- [x] 能力层 T1：能力登记表（CAPABILITIES.md）+ 6 份角色章程（.zcode/agents/）+ 5 个命令入口（.zcode/commands/）+ H-02 校验钩子与 lint_kb.py（守卫回归 14/14）
- [x] T2：编排技能 K-01…K-07 + 慢循环/验收/归档脚本（S-02…S-06、S-09）+ H-03 会话播报 + metrics 分片制（守卫 16/16、lint 12/12、全链路隔离冒烟通过）
- [ ] T3：外部接入（marp/typst/pio/kicad CLI、MCP 后置评估、RSSHub、Kaggle key）

能力登记与裁决记录见 [docs/CAPABILITIES.md](docs/CAPABILITIES.md)；角色写入边界的硬度表述（L1 软边界 / L2 阶段硬边界）见 DESIGN.md §6.2。
