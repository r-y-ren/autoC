# kb/ 知识库导览（库志）

> 本文件是人读的第一页：库的结构、各层含义、检索入口。条目内容以 `INDEX.md` 与各条目为准，本文件不承载事实。

## 两座库（交付物 1 / 2）

| 库 | 交付物 | 内容 | 条目形态 |
|---|---|---|---|
| KB-1 赛事库 | 交付物 1 | 赛事信息 + 历年获奖解构 + 模式库 | `competitions/<id>/`（meta / winners / patterns 三层） |
| KB-2 科技库 | 交付物 2 | 前沿技术卡片（带比赛映射） | `tech/<规范化ID>.md` |

## KB-1 条目内三层

```
competitions/<id>/
├── meta.md        # 事实层：主办方/时间/规则/AI政策——schema 强制，逐条带来源
├── winners/<年>.md # 解构层：当年获奖名单数据 + 获奖论文深构（正文层，lint 跳过）
└── patterns.md    # 总结层：评审偏好/方法论分布/差异化点——喂给 K-02 与验收报告
```

信息流：meta（是什么）→ winners（谁赢了、怎么赢的）→ patterns（对我们意味着什么）。**分析增量只允许发生在条目层。**

## 检索入口

| 读者 | 入口 | 说明 |
|---|---|---|
| agent（主会话） | `INDEX.md` | 瘦协调者唯一入口，只读索引做路由（AGENTS.md 铁律 5） |
| agent（子 agent） | 按任务包指定的条目路径 | 分片精读，返回结构化结论 |
| 人 | `export/digest-<方向>-<月>.md` | 方向情报简报（S-15 周更，月末转正式版，D6 裁决：读者=团队自用） |

## 支撑目录

- `quarantine/`——schema 不合格条目隔离区（附 `.reason`），周六深度评估处置
- `raw/`——原始快照与 PDF（gitignore，不入 git 主干；`raw/candidates/` 为采集队列，消费后移 `processed/`）
- `tech/.rejections.yaml`——Hunter 拒绝台账（stars 达快照 ×2 自动重评）

## 维护机制

每 3 天 09:00 全量深度跑批（D7 合并节奏：增量拉取 + 存量深度 + 简报刷新，单 cron）；跑批记录见 `INDEX.md` 跑批表（append-only）；
流程 SOP 见 `.zcode/skills/kb-sync`（K-01）与 `kb-deep-sync`（K-08）。
