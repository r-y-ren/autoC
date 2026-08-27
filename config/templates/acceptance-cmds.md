# 验收 cmd 模板库（供 K-02 写蓝图验收清单时直接复用）

> 目标：机检项（category=software/hardware/document 且 method 可命令化）尽量带 `cmd`，
> 让 `run_acceptance.py` 自动执行存证，减少 pending 项。原则：**cmd 必须自包含、可重复执行、
> 退出码即判定**（0=pass）；路径一律相对仓库根；不依赖交互输入。
>
> 取证类（截图/录屏）不走 cmd——按 acceptor 章程的 browser-use 标准动作执行，证据回填 run-*.json。

## 软件类

```yaml
# 单元/集成测试全过
- {id: sw-test, category: software, item: 测试套件全过, method: 自动, cmd: "python -m pytest workspace/software/tests -q"}

# 一键启动健康检查（自包含：后台起、探测、清理，超时即非零退出）
- {id: sw-boot, category: software, item: 服务可启动且健康, method: 自动,
   cmd: "python workspace/software/smoke_boot.py"}

# 依赖安装可复现
- {id: sw-deps, category: software, item: 依赖锁定安装通过, method: 自动,
   cmd: "python -m pip install -q -r workspace/software/requirements.txt"}

# 前端构建（有前端时）
- {id: sw-fe, category: software, item: 前端构建通过, method: 自动,
   cmd: "npm --prefix workspace/software/web run build"}
```

## 硬件类（CLI 路线）

```yaml
# 固件编译（PlatformIO）
- {id: hw-fw, category: hardware, item: 固件编译通过, method: 自动,
   cmd: "python3 -m platformio run -d workspace/hardware/firmware"}

# PCB 生产文件导出（kicad-cli，路径按实际工程调整）
- {id: hw-gerber, category: hardware, item: Gerber 导出成功, method: 自动,
   cmd: "\"%LOCALAPPDATA%/Programs/KiCad/10.0/bin/kicad-cli.exe\" pcb export gerbers --output workspace/hardware/gerbers workspace/hardware/pcb/board.kicad_pcb"}

# 结构件 STL 渲染（OpenSCAD 无头）
- {id: hw-stl, category: hardware, item: STL 渲染成功, method: 自动,
   cmd: "\"C:/Program Files/OpenSCAD/openscad.exe\" -o workspace/hardware/case/case.stl workspace/hardware/case/case.scad"}
```

## 文档类

```yaml
# 报告 PDF 编译（Typst）
- {id: doc-report, category: document, item: 报告 PDF 编译通过, method: 自动,
   cmd: "typst compile workspace/docs/report.typ workspace/docs/report.pdf"}

# 答辩 PPT 导出（Marp → pptx）
- {id: doc-deck, category: document, item: PPT 导出成功, method: 自动,
   cmd: "marp workspace/docs/deck.md -o workspace/docs/deck.pptx --pptx"}

# 必备交付物存在性断言
- {id: doc-files, category: document, item: 交付物齐备, method: 自动,
   cmd: "python -c \"from pathlib import Path; [assert Path(p).is_file() for p in ['workspace/docs/report.pdf','workspace/docs/deck.pptx','workspace/metrics.json']]\""}
```

## 编写守则

1. **禁用无限阻塞命令**（`serve`/`run` 裸跑）——启动类验收用 smoke 脚本封装：起、探、杀，全程有超时。
2. 跨平台引号：Windows 路径含空格用双引号包裹；模板里的写法已按 Git Bash 校验。
3. 一项一义：一个 cmd 只验一件事，复合验收拆成多项，证据才可归因。
4. cmd 失败时证据（stdout/stderr/退出码）自动落 `workspace/acceptance/evidence/<id>.log`——工单直接引用。
