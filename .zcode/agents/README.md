# .zcode/agents/ —— 角色章程（子 agent 定义）

T1 已落盘六份章程（能力契约本体，与 CAPABILITIES.md C-01…C-06 对应）：

| 文件 | 角色 | 允许写根 |
|---|---|---|
| scraper.md | 赛事情报采集（KB-1） | kb/competitions/、kb/raw/ |
| hunter.md | 前沿科技猎手（KB-2） | kb/tech/、kb/raw/ |
| software.md | 软件工程 | workspace/software/、workspace/metrics.json |
| hardware.md | 硬件工程（CLI 路线） | workspace/hardware/ |
| document.md | 竞赛文档 | workspace/docs/ |
| acceptor.md | 验收（只开工单不修作品） | workspace/acceptance/ |

> Strategy 不设章程：决策需与用户交互，运行在主会话，规程并入 K-02 技能（见 CAPABILITIES.md）。
> ✅ 已验证（2026-08-27，T3-a 首跑）：本目录章程被客户端原生注册为子 agent 类型
> （scraper/hunter/software/hardware/document/acceptor 可直接按 subagent_type 派发）。
