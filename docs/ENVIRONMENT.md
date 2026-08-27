# 环境基线（Phase 0 检测于 2026-08-27，Windows 10 22H2 / Git Bash）

## 已就绪

| 工具 | 版本 | 用途 |
|---|---|---|
| git | 2.48.1.windows.1 | L3 审计、归档 tag |
| python | 3.14.7（`python` / `py`） | 守卫/脚本主运行时（stdlib-only 已满足 Phase 0） |
| python3 | 3.12.10 | 备用解释器（PlatformIO 等兼容性备选） |
| pip | 26.2.1 | 依赖安装 |
| node / npm | v24.19.0 / 11.19.0 | 前端工程、Marp CLI |

## 待安装（按模块启用时再装，Phase 0 不阻塞）

| 工具 | 用途 | 安装命令 |
|---|---|---|
| marp-cli | 答辩 PPT（Markdown → pptx/pdf） | `npm install -g @marp-team/marp-cli` |
| typst | 项目报告排版 | `winget install --id Typst.Typst` |
| platformio | 固件编译与板级测试 | `python3 -m pip install platformio`（建议挂在 3.12 环境） |
| kicad-cli | PCB 设计文件生成 | 随 KiCad 安装（winget install KiCad.KiCad） |

## 已随能力层（T1）安装

| 工具 | 版本 | 用途 |
|---|---|---|
| pyyaml | 6.0.3 | lint_kb.py frontmatter 解析 |
| jsonschema | 4.26.0 | lint_kb.py 契约校验 |

## 说明

- 守卫钩子（`.zcode/config.json`）以 `process` 方式调用 `python`（无 shell，Windows 兼容）；若换机器 `python` 不在 PATH，改用 `py` 并同步改 `args`。
- `.venv/`（既存目录）已被 .gitignore 排除，未在 Phase 0 中使用。
