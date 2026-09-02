---
description: 人工主导交付入口：副驾模式，人指挥主会话直接动手（K-11 编排；/deliver 的姊妹入口，熔断后人工接管亦走此）
---

# /self —— 人工主导交付会话入口

用法：执行 `/self <cid>`（单战役在册可省略 cid）。蓝图须已存在且过校验；**执行本命令即视为对该蓝图的人工确认**（否则先回 /attack）。

执行流程（编排细节见 `.zcode/skills/self-run/SKILL.md` K-11）：

1. **前置闸门**：blueprint 存在且过 schema 校验（缺失/不过 → 指 /attack）；`compliance.mode=assist` 拒绝；phase=verify/archive 指回对应命令；tripped=true 不拒（人工接管出口）
2. `python scripts/guard/init_state.py --campaign <cid> --phase deliver --by self`
3. **身份切换**：主会话从编排者转为副驾——瘦协调者/角色写入矩阵/波次编排对本会话豁免（限战役根内），人定粒度与顺序，主会话直接读写战役根；需要时可按 K-03 派单个角色任务包
4. **不变量不豁免**：archive/ 只读；state.json 只归脚本；acceptance/ 只经 /accept；顶层 metrics.json 只经 merge_metrics；外部材料进 references/ 并登记；性能数字只来自实测分片；蓝图改必重校验+JOURNAL 留痕；战役文件圈禁在战役根（D14：活跃期根/工程目录守卫锁定，含临时试验与下载）
5. 收尾：JOURNAL 记行（self 标注）+ git commit → 提示 /accept 终验；与 /deliver 可随时互换续跑

铁律：人工主导 ≠ 绕过验收——终验仍走 /accept 全量清单；副驾不写 acceptance/ 与顶层 metrics.json。
