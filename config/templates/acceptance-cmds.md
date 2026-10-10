# 验收 cmd 模板库（供 K-02 写蓝图验收清单时直接复用）

> 目标：机检项（category=software/hardware/document 且 method 可命令化）尽量带 `cmd`，
> 让 `run_acceptance.py` 自动执行存证，减少 pending 项。原则：**cmd 必须自包含、可重复执行、
> 退出码即判定**（0=pass）；路径一律相对仓库根；不依赖交互输入。
>
> 取证类（截图/录屏）不走 cmd——按 acceptor 章程的 browser-use 标准动作执行，证据回填 run-*.json。

## 软件类

```yaml
# 单元/集成测试全过
- {id: sw-test, category: software, item: 测试套件全过, method: 自动, cmd: "python -m pytest workspace/<cid>/software/tests -q"}

# 一键启动健康检查（自包含：后台起、探测、清理，超时即非零退出）
- {id: sw-boot, category: software, item: 服务可启动且健康, method: 自动,
   cmd: "python workspace/<cid>/software/smoke_boot.py"}

# 依赖安装可复现
- {id: sw-deps, category: software, item: 依赖锁定安装通过, method: 自动,
   cmd: "python -m pip install -q -r workspace/<cid>/software/requirements.txt"}

# 前端构建（有前端时）
- {id: sw-fe, category: software, item: 前端构建通过, method: 自动,
   cmd: "npm --prefix workspace/<cid>/software/web run build"}
```

## 硬件类（CLI 路线）

```yaml
# 固件编译（PlatformIO）
- {id: hw-fw, category: hardware, item: 固件编译通过, method: 自动,
   cmd: "python3 -m platformio run -d workspace/<cid>/hardware/firmware"}

# PCB 生产文件导出（kicad-cli，路径按实际工程调整）
- {id: hw-gerber, category: hardware, item: Gerber 导出成功, method: 自动,
   cmd: "\"%LOCALAPPDATA%/Programs/KiCad/10.0/bin/kicad-cli.exe\" pcb export gerbers --output workspace/<cid>/hardware/gerbers workspace/<cid>/hardware/pcb/board.kicad_pcb"}

# 结构件 STL 渲染（OpenSCAD 无头）
- {id: hw-stl, category: hardware, item: STL 渲染成功, method: 自动,
   cmd: "\"C:/Program Files/OpenSCAD/openscad.exe\" -o workspace/<cid>/hardware/case/case.stl workspace/<cid>/hardware/case/case.scad"}

# 固件仿真（Wokwi 断言式：串口出现期望文本即 pass，T3-e 实测全链路通过——E-12）
# ⚠ 三项前置（缺一仿真静默无输出，T3-e 踩坑实录）：
#   ① wokwi.toml 必须同时声明 elf 与 firmware 两个键（各指向 .elf / .bin）
#   ② diagram.json 板类型名必须是 wokwi-esp32-devkit-v1（不是 board-esp32-devkit-c-v4）
#   ③ 串口监视器必须显式接线：esp:TX0 → $serialMonitor:RX（无接线=无串口输出，连 ROM 启动横幅都没有）
- {id: hw-sim, category: hardware, item: 固件仿真就绪, method: 自动,
   cmd: "wokwi-cli workspace/<cid>/hardware/firmware --expect-text AUTOC_READY --fail-text PANIC --timeout 60000"}
# 注：wokwi-cli 位于 %USERPROFILE%\\.wokwi\\bin（不在 PATH 时写全路径）；Community License 口径为公开/开源项目；
#     仿真工程目录需含 wokwi.toml + diagram.json（由 Hardware 角色随固件一起产出）
```

## 文档类

```yaml
# 报告 PDF 编译（Typst）
- {id: doc-report, category: document, item: 报告 PDF 编译通过, method: 自动,
   cmd: "typst compile workspace/<cid>/docs/report.typ workspace/<cid>/docs/report.pdf"}

# 答辩 PPT 导出（Marp → pptx）
- {id: doc-deck, category: document, item: PPT 导出成功, method: 自动,
   cmd: "marp workspace/<cid>/docs/deck.md -o workspace/<cid>/docs/deck.pptx --pptx"}

# 必备交付物存在性断言
- {id: doc-files, category: document, item: 交付物齐备, method: 自动,
   cmd: "python -c \"from pathlib import Path; [assert Path(p).is_file() for p in ['workspace/<cid>/docs/report.pdf','workspace/<cid>/docs/deck.pptx','workspace/<cid>/metrics.json']]\""}
```

## 编写守则

1. **禁用无限阻塞命令**（`serve`/`run` 裸跑）——启动类验收用 smoke 脚本封装：起、探、杀，全程有超时。
2. 跨平台引号：Windows 路径含空格用双引号包裹；模板里的写法已按 Git Bash 校验。
3. 一项一义：一个 cmd 只验一件事，复合验收拆成多项，证据才可归因。
4. cmd 失败时证据（stdout/stderr/退出码）自动落 `workspace/<cid>/acceptance/evidence/<id>.log`——工单直接引用。
