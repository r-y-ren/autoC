---
name: ppt-self
description: PPT 阶段人工副驾模式（K-13，升级票11）：/ppt 产线之上的人工微调会话——用户亲自掌控内容与版式细节，主会话为副驾。语义沿用 /self（K-11），豁免范围限战役 docs 子树。当用户触发 /ppt-self 时使用。
---

# K-13 ppt-self：PPT 阶段人工副驾（升级票11，2026-09-16）

## 定位

- /self（K-11）在 PPT 阶段的同款副驾模式：**人指挥、主会话动手**（v2 起波次编排已退役）。
- **豁免范围限 `<战役根>/docs/` 子树**（ppt_brief.md、docs/ppt/ 项目文件）——其余不变量一概不豁免（acceptance/ 只读、metrics 汇总物禁写、蓝图未动、数字纪律照旧）。
- 与 /ppt 可互换续跑：/ppt 自动产线走完 Gate2 后想手工打磨，或直接以副驾从简报开始，均由本入口承接。

## 前置

- 战役 verify 态（accept 已过、未 archive——同 K-12 窗口）；ppt-master 插件在位。

## 流程

1. 进入副驾：主会话声明副驾身份与豁免边界（docs 子树），读 `docs/ppt_brief.md` 与 `docs/ppt/` 现状。
2. 按用户指令工作：改简报、调页序/版式、跑 ppt-master 的 Edit Native PPTX 路线微调既有 pptx、重生成图片等——一切写操作限 docs 子树。
3. 数字改动：简报中任何数字调整必须回 `metrics.json` 对应键核对，不得凭空改数（铁律 4）。
4. 每完成一轮有意义修改：JOURNAL 记行 + 项目仓库 commit（docs 子树内产物）。
5. 收尾：产物核验（同 K-12 第 3 步）→ 提示 `/archive`。

## 禁止

- 禁越出 docs 子树写任何文件；禁改验收记录/蓝图；禁绕过数字溯源；禁在窗口外运行。
