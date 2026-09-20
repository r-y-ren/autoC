# bc_track —— Track-C 行为克隆（BC）轨（spec: docs/track-C-bc-spec.md）

从顶部选手官方回放训练行为克隆 agent，目标直进口 diagnosed 短板：
day-11 后每回合微观执行效率（路线/发呆率/CARE 覆盖）。standalone——
不嫁接 v14.x chassis、不改 src//planner/；评估缝=孪生 d0 全季注入协议。

## 一键复现（全管线，约 15 分钟 CPU）

```bash
cd workspace/kaggressure/software
# 0) （可选，语料已在 references/data/online-replays/bc-top/）
python bc_track/scripts/harvest_top_replays.py --top 30 --per-team 3 --max-games 72
# 1) 样本抽取（克隆席过滤内置；含本机语料高分席兜底）
python bc_track/scripts/extract_samples.py --include-rounds
# 2) 训练（numpy 训练侧；导出纯 Python 量化权重）
python bc_track/scripts/train_bc.py --epochs 15 --lr 1e-3
# 3) 评估（孪生 d0 全季，对手=回放真实动作，对照 v14.2 基线）
python bc_track/scripts/bc_eval.py --games 8
```

## 目录

| 路径 | 内容 |
|---|---|
| `scripts/harvest_top_replays.py` | M0-1 榜单 top-N 队官方回放抓取（kaggle CLI，幂等 manifest） |
| `scripts/bc_schema.py` | **唯一契约**：特征/动作 schema（版本 `bc-schema/1.1`，167 维全局 + 14 维单位特征；单位动作 18 op/12 arg/14 qty 桶；市场 10 槽 7 op/12 item/14 qty） |
| `scripts/extract_samples.py` | M0-2/M0-3 样本抽取 + 克隆席过滤（1-51 步动作签名≥3 队=量产克隆家族，非 top 席剔除） |
| `scripts/train_bc.py` | M1-1 训练：unit-net/market-net 两解耦 MLP（128-64 tanh，Adam，条件掩码 CE），导出 int8 量化权重硬编码 .py |
| `scripts/bc_policy.py` | M1 推理：纯 Python 前向（stdlib-only、确定性、shared-G 每回合一次优化、合法性掩码）+ 行为诊断计数 |
| `scripts/bc_eval.py` | M1-2 评估 harness：twin d0 全季注入，对手=回放真实动作；BC vs v14.2（build_v13_namespace）同局同席单变量对照 |
| `models/bc_model_v1.py` | 量化权重（自动生成，勿手改） |
| `models/train_report.json` | 逐头准确率（train/held-out + 多数类基线） |
| `exports/eval_v1.{json,md}` | 首跑评估数字与行为诊断 |
| `data/`（gitignore: samples/） | 样本缓存 + corpus_manifest.json + split.json（game 级 held-out 切分） |

## 配对口径（与 planner/twin 同一解读）

`(obs, action) = (steps[t-1][seat].observation, steps[t][seat].action)`
—— steps[t] 记录的 action 驱动 t-1→t 转移。已在 bc-top 语料上逐语义
验证（WATER 落作物 13961/13962、棚操作落访问格 3888/3914、PLANT 落
空地 3118/3123）。

## 已知局限（首跑 v1，诚实条款）

- 单位随身库存用全队合计近似（回放不标 unit↔inventory 对应）；
- 35% 单位动作 top-1（多数类 14.5%）不足以支撑闭环一致微观执行；
- 市场头 non-NONE 31% < 多数类 39.7%，闭环欠交易；
- 纯 Python 前向 ~13ms/回合（720 回合 ≈ 9s/局，1s/回合预算内）。
