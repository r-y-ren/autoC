---
description: 人工主导会话入口：副驾模式，人指挥主会话直接动手（K-11；v2 起推进由人工自主，熔断后人工接管亦走此）
---

# /self —— 人工主导交付会话入口

用法：执行 `/self <cid>`（单战役在册可省略 cid）。战役已登记即可进入；`/attack` 方案书为纯参考信息、**非闸门**。

执行流程（编排细节见 `.zcode/skills/self-run/SKILL.md` K-11）：

1. **前置闸门**：战役已登记；`compliance.mode=assist` 拒绝；phase=verify/archive 指回对应命令；tripped=true 不拒（人工接管出口）
2. `python scripts/guard/init_state.py --campaign <cid> --phase deliver --by self`
3. **身份切换**：主会话转为副驾——角色写入矩阵对本会话豁免（限战役根内；瘦协调者 v2 已限慢循环），人定粒度与顺序，主会话直接读写战役根；需要时可派发子 agent 任务包（按角色章程）
4. **不变量不豁免**：archive/ 只读；state.json 只归脚本；acceptance/ 只经 /accept；顶层 metrics.json 只经 merge_metrics；外部材料进 references/ 并登记；实测数字须可溯至项目实测产物；契约改必重校验+JOURNAL 留痕；战役文件圈禁在战役根（D14：活跃期根/工程目录守卫锁定，含临时试验与下载）
5. 收尾：JOURNAL 记行（self 标注）+ 项目仓库 commit → 提示 /accept 终验；项目迭代主力为 fn-ladder，需要工作流工具时再进 /self

铁律：人工主导 ≠ 绕过验收——终验仍走 /accept 全量清单；副驾不写 acceptance/ 与顶层 metrics.json。
