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

## 已知局限（诚实条款）

- 单位随身库存用全队合计近似（回放不标 unit↔inventory 对应）；
- 市场头 non-NONE 31% < 多数类 39.7%（订单条件结构未学会，票 03 用
  开局剧本注入+解码约束兜底）；
- 纯 Python 前向 ~13ms/回合（720 回合 ≈ 9s/局，1s/回合预算内）。

## 票 03 迭代结果（2026-09-20，判定=弃牌）

五级单变量阶梯（8 局 held-out 同口径，详见 issues/03 + metrics `bc_iter2_*`）：

| 变量 | 中位 |
|---|---:|
| 诚实基线（v1；M1"2/8 赢局"系 bc_eval 席位错位伪影，已修复） | 2,967 |
| +A1 市场剧本 d0-d3 | 338.5 |
| +A2 全剧本 d0-d3 | 604.5 |
| +schema 1.2 维护特征重训（op acc 34.3%→49.0%） | 910 |
| +B 市场解码约束（SELL 锚棚存/预算/HIRE 去重）= 最好候选 | **1,995** |

门 A（中位 ≥32k）达成 6.2%，塌方 12/12 ≠ 0 → 按票面收刀。终态归因：
条件 op 头健康（站作物格 87.8% 发 WATER），学不会的是**目标导向工作面
轮换调度**（下一步去哪块地/何时雇人/口粮物流）——与 island-ga "walking
is the money" 实证一致。种子稳定性 4 种子 1,299-1,631（结构性塌方）。

新增模块：`scripts/bc_opening.py`（v48 开局剧本注入）、`scripts/bc_decode.py`
（市场解码约束）、`scripts/bc_seed_stability.py`（合成季×v48 路由陪练）、
`models/bc_model_v2.py`（schema 1.2）、`data/v48_default_d0d3_actions.json`
（v48 default 路由 d0-d3 解码动作表，可审计）。

