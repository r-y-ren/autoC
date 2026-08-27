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
> 注：workspace 级子 agent 定义的准确目录/格式以客户端 Settings → Subagents 实测为准；
> 首个战役派发时验证，若客户端采用其他约定，移动本目录并同步更新 DESIGN.md 与 CAPABILITIES.md。
