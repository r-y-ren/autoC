---
description: PPT 阶段人工副驾（K-13）：/ppt 之后亲自微调内容与版式——人指挥、主会话动手，豁免限战役 docs 子树
---

# /ppt-self —— PPT 阶段副驾入口

用法：`/ppt-self <cid>`（战役 verify 态，/accept 已过、未 /archive；通常在 /ppt 之后用于细节打磨，也可直接从简报阶段接管）。规程见 `.zcode/skills/ppt-self/SKILL.md` K-13。

- 主会话身份切**副驾**：豁免瘦协调者/编排语义（沿用 /self），**豁免范围限 `<战役根>/docs/`**——简报与 ppt-master 项目文件随手改，其余不变量照旧（acceptance 只读、metrics 汇总物禁写、数字必须回 metrics 键溯源）。
- 每轮修改 JOURNAL 记行 + commit；收尾产物核验后提示 `/archive`。

铁律：窗口外拒绝运行；越出 docs 子树的写操作一律拒绝（守卫拦截 + 自律）；禁编造数字。
