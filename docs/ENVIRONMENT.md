# 环境基线（Phase 0 检测于 2026-08-27，Windows 10 22H2 / Git Bash）

## 已就绪

| 工具 | 版本 | 用途 |
|---|---|---|
| git | 2.48.1.windows.1 | L3 审计、归档 tag |
| python | 3.14.7（`python` / `py`） | 守卫/脚本主运行时（stdlib-only 已满足 Phase 0） |
| python3 | 3.12.10 | 备用解释器（PlatformIO 等兼容性备选） |
| pip | 26.2.1 | 依赖安装 |
| node / npm | v24.19.0 / 11.19.0 | 前端工程、Marp CLI |

## 待安装（按需，当前无阻塞项）

| 工具 | 用途 | 状态 |
|---|---|---|
| wokwi-mcp（E-05/E-12） | 有状态电路仿真 | 需账号/许可，密钥类；用户提供前维持登记态 |
| RSSHub（E-07） | 公众号信源中转 | D5 缓判至挑战杯类方向启用；届时 clone 进 gitignored `tools/` |
| Kaggle API key（E-08） | 赛题/榜单拉取 | Kaggle 方向启用时由用户提供 |

## 已随能力层安装

| 工具 | 版本 | 用途 |
|---|---|---|
| pyyaml | 6.0.3 | lint_kb.py frontmatter 解析 |
| jsonschema | 4.26.0 | lint_kb.py 契约校验 |
| Tesseract OCR（UB-Mannheim） | 5.4.0 | S-13 扫描件 OCR；chi_sim 为 tessdata_fast 用户级包（~/.tessdata） |
| pypdfium2 / pdfplumber / pillow | — | S-13 渲染与表格化、winners 名单机读 |
| typst | 0.15.1（winget） | K-07 报告排版；⚠ PATH 需新 shell，绝对路径见 WinGet/Links |
| marp-cli | 4.5.0（npm -g） | K-06 PPT；pptx 导出经本机 Chromium 实测可用 |
| PlatformIO Core | 6.1.19（挂 python3=3.12） | C-04 固件编译；调用方式 `python3 -m platformio` |
| KiCad + kicad-cli | 10.0.5（winget，用户级） | C-04 PCB；路径 `%LOCALAPPDATA%\Programs\KiCad\10.0\bin\kicad-cli.exe`，不在 PATH |
| OpenSCAD | 2025.x（winget） | C-04 结构件；路径 `C:\Program Files\OpenSCAD\openscad.exe`，无头模式 `-o` 可用 |
| wokwi-cli | 0.26.1（官方脚本装至 `%USERPROFILE%\.wokwi\bin`） | C-04 固件仿真；token=WOKWI_CLI_TOKEN（用户级环境变量，Community License） |

### Linux 主力机（~/.venvs/autoc，2026-09-16 升级装）

| 工具 | 版本 | 用途 |
|---|---|---|
| typst（pip 包，python API） | 0.15.0 | K-07 编译通道（`typst.compile(..., root='<战役根>')`，root 实参必带——彩排实证勘误） |
| Flask | 3.1.3 | ppt-master 实时预览服务（svg_editor/server.py --live） |
| python-pptx | 1.0.2 | ppt-master pptx 导出（svg_to_pptx.py） |
| MinerU 4.0.4（~/.venvs/mineru：py3.12 + torch 2.14 CPU；模型 ~/.mineru/models ≈2G） | E-14 PDF/图片→md 本地解析主力（C-01/C-02 难读文档）；`~/.venvs/mineru/bin/mineru parse <pdf> -p all --tier standard -o <out>.md`，前置 `mineru server start`，**禁 --remote** |
| tesseract（系统 5.x）+ ~/.tessdata 用户包（chi_sim/eng=tessdata_fast + afr/osd + configs/） | S-13 OCR 兜底链（2026-09-20 修复本机断链并端到端验证） |
| pdfplumber 0.11.10 / pypdfium2 5.13 / pillow 12.3（autoc venv，2026-09-20 补装） | E-10 表格机读 / S-13 页面渲染 |
| poppler（pdftotext/pdftoppm）、soffice、ffmpeg、rg（系统自带） | 文本层快检 / Office→PDF 前置转换（接 MinerU）/ 媒体处理 / 快速检索 |

（本节为 Linux 侧增量；上表 Windows 基线照旧，双机各管各的运行时。）

## T3-c 冒烟记录（2026-08-27）

- `typst compile config/templates/report_template.typ` → PDF 25KB，exit 0，中文章节进文本层 ✓
- `marp config/templates/presentation.marp.md -o …pptx` → 467KB ✓（HTML 导出 112KB ✓）
- `ocr_pdf.py` 文本层路径（typst 产物）与 OCR 路径（cumcm 扫描件 11 页，无低置信页）双验证 ✓
- OCR 注意：`TESSDATA_PREFIX` 是整体替换——用户级目录须自带 configs/ 与默认语言包（ensure_lang 已自动处理）

## T3-d 硬件工具链冒烟记录（2026-08-27）

- PlatformIO：`platform=native` 工程 `python3 -m platformio run` 编译+运行 ✓（本机 MinGW gcc 14.2；首次真实嵌入式构建将下载对应工具链，属正常流量）
- kicad-cli：最小板件 `pcb export gerbers` → 12 个 gerber 文件 ✓
- OpenSCAD：`cube([10,10,10])` 无头渲染 STL（6 面/1589B）✓
## T3-e wokwi-cli 冒烟记录（2026-08-27）

- 官方 esp-idf-hello-world 仓库：`--expect-text "Hello world!"` → TEST PASSED，exit 0 ✓（token/仿真/串口/断言链路验证）
- 自建 pio+Arduino ESP32（serial 打印 AUTOC_READY）：TEST PASSED，exit 0 ✓
- 踩坑实录（已固化进 acceptance-cmds.md 模板）：wokwi.toml 须同时有 `elf`+`firmware` 键；diagram 板类型名 `wokwi-esp32-devkit-v1`；串口监视器须显式接线 `esp:TX0→$serialMonitor:RX`——缺任一项仿真静默无输出（连 ROM 启动横幅都没有），CLI 不报错只超时
- `wokwi-cli init` 需要交互终端（无 TTY 报 uv_tty_init）；diagram/toml 建议手写（模板见 acceptance-cmds.md）
- 附注：wokwi-cli 自带实验性 MCP server（`wokwi-cli mcp`）——D8 维持不启用，CLI 断言已覆盖验收需求

## E-14 MinerU 冒烟记录（2026-09-20，Linux 主力机）

- standard 档（onnx 全家 + 1.2B VLM GGUF，纯 CPU）：17 页中文评审规则全量 **11s**，评审表格完整还原 markdown；basic 档 13.5s
- 扫描件（合成无文本层 PDF，basic 档 OCR）：6.6s/页，中文与表格基本无损（仅引号全半角微差）；PNG 图片输入直接可解析
- 部署要点：`parse` 不自动拉服务（先 `mineru server start`）；档位切换须 `mineru config set parse_server.local.managed_tier <档>` + `mineru server restart`（`parse --tier` 不能跨已加载档）；模型下载用 **modelscope 源**（HuggingFace 大文件在本机网络会卡死）；4.0.4 自带 GGUF 运行时，无需 llama-cpp-python；**parse 会在 cwd 生成 `blobs/` 内容缓存——先 cd 到 /tmp 工作目录再跑，勿在仓库根执行**
- 同日修复：~/.tessdata 用户级 chi_sim+eng（此前本机 tesseract 仅 afr/osd，S-13 中文 OCR 断链）；pdfplumber 装入 autoc venv（表格机读验证通过）

## 说明

- 守卫钩子（`.zcode/config.json`）以 `process` 方式调用 `python`（无 shell，Windows 兼容）；若换机器 `python` 不在 PATH，改用 `py` 并同步改 `args`。
- `.venv/`（既存目录）已被 .gitignore 排除，未在 Phase 0 中使用。
- 第三方开源工具（如未来 RSSHub）一律 clone 进 gitignored `tools/`，本页登记版本（CAPABILITIES D5 纪律）。
