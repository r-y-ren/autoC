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

## 已随能力层安装

| 工具 | 版本 | 用途 |
|---|---|---|
| pyyaml | 6.0.3 | lint_kb.py frontmatter 解析 |
| jsonschema | 4.26.0 | lint_kb.py 契约校验 |
| Tesseract OCR（UB-Mannheim） | 5.x | S-13 扫描件 OCR；chi_sim 为 tessdata_fast 用户级包（~/.tessdata） |
| pypdfium2 / pdfplumber / pillow | — | S-13 渲染与表格化、winners 名单机读 |
| typst | 0.15.1（winget） | K-07 报告排版；⚠ PATH 需新 shell，绝对路径见 WinGet/Links |
| marp-cli | 4.5.0（npm -g） | K-06 PPT；pptx 导出经本机 Chromium 实测可用 |

## T3-c 冒烟记录（2026-08-27）

- `typst compile config/templates/report_template.typ` → PDF 25KB，exit 0，中文章节进文本层 ✓
- `marp config/templates/presentation.marp.md -o …pptx` → 467KB ✓（HTML 导出 112KB ✓）
- `ocr_pdf.py` 文本层路径（typst 产物）与 OCR 路径（cumcm 扫描件 11 页，无低置信页）双验证 ✓
- OCR 注意：`TESSDATA_PREFIX` 是整体替换——用户级目录须自带 configs/ 与默认语言包（ensure_lang 已自动处理）

## 说明

- 守卫钩子（`.zcode/config.json`）以 `process` 方式调用 `python`（无 shell，Windows 兼容）；若换机器 `python` 不在 PATH，改用 `py` 并同步改 `args`。
- `.venv/`（既存目录）已被 .gitignore 排除，未在 Phase 0 中使用。
- 第三方开源工具（如未来 RSSHub）一律 clone 进 gitignored `tools/`，本页登记版本（CAPABILITIES D5 纪律）。
