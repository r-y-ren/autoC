# Kaggriculture 软件交付（workspace/software）

Kaggle Simulation Competition **Kaggriculture**（Google/Kaggle 农场经营 720 回合博弈）的
bot、本地评估基建、机制量化工具与增强策略 A/B。

**引擎边界声明**：本地对局运行在**官方引擎**上——PyPI `kaggle-environments` 1.32.7 的
`kaggriculture` 场景（本仓 vendor 了去依赖元数据/去可视化资源的重打包 wheel，引擎代码未改动，
见 `vendor/WHEEL_PROVENANCE.md`）。本地评估结果代表官方规则语义，但**不等价于** Kaggle 线上
天梯（对手分布不同、未做线上提交）。

## 一键命令（仓库根目录执行）

```bash
# 1) 依赖安装（锁定）
python -m pip install -q -r workspace/software/requirements.txt

# 2) 冒烟自检（起环境 -> 自博弈 -> 契约校验 -> 退出码判定，超时看门狗 300s）
python workspace/software/smoke_boot.py

# 3) 测试套件
python -m pytest workspace/software/tests -q

# 4) 全量评估（40 局，约 2 分钟：2 主打 x 4 对手 x 4 种子 + 8 局 A/B 对决）
python workspace/software/scripts/run_eval.py --rounds 4
```

## 目录

```
workspace/software/
├── kaggle_simulations/agent/main.py   可提交 bot（官方 kit 结构，自包含 stdlib-only；
│                                      上传：kaggle competitions submit kaggriculture -f main.py）
├── kgenv/                             本地评估包
│   ├── engine.py                      官方引擎单局对局器（结构化结果/每日资金曲线）
│   ├── gym_env.py                     gym 风格单智能体封装（可插拔对手策略）
│   ├── economy.py                     收益模型（价格曲线/作物周期/动物产出/雇佣/地价）
│   ├── redlines.py                    机制红线检查表（浇水/喂养/产出上限/shed/期限）
│   ├── elo.py                         Elo 评级（只按胜负平，对齐官方天梯语义）
│   ├── arena.py                       对局编排 + 复盘日志 + 提交 bot 加载
│   └── bots/                          baseline_wheat / greedy_carrot / LLM provider（默认关）
├── scripts/run_eval.py                评估矩阵 + Elo + exports 产出
├── smoke_boot.py                      冒烟自检（验收命令）
├── tests/                             pytest：收益模型/红线/agent 契约/对局器
├── exports/
│   ├── schema.json                    软件->文档接口契约（评估结果 JSON Schema）
│   ├── eval_results.json              实测评估样例（40 局）
│   └── logs/replay_log.jsonl          复盘日志（每局一行的对局记录）
├── metrics.json                       实测指标分片（只写实测值，禁编造）
├── requirements.txt                   锁定依赖（含 vendor wheel，需从仓库根安装）
└── vendor/                            官方引擎 nodeps 重打包 wheel + 出处说明
```

## Bot 策略（kaggle_simulations/agent/main.py）

"鹅引擎 + 瓜波段"三段式（全部机制来自官方 How-to-Play/engine 源码）：

1. **鹅引擎**：shed 近区建 coop 养鹅；每日 FEED（小麦）+ CARE（喂养日照护银行化 +1 蛋/日，
   即每日照护使产蛋翻倍）+ COLLECT_FERTILIZER（每只存活动物每日 1 肥料，~$100）+ 批量 HARVEST。
   蛋与肥料的价格曲线对抛压耐受（log 上行目标 0.2），可每日倾销。
2. **瓜波段**：第 0-2 天 6 块西瓜进窗口期浇水（6-12 天龄，1+6=6 果/块），第 12-13 天收获，
   按价格闸门分批出货（西瓜 glut 曲线 sq 3.6，乱抛直接砸穿到 $1）；价格仍在 $180 以上时第
   13-16 天续第二波。
3. **小麦基座**：剩余格种小麦（自给鹅粮 + 现金），max_yield_day 收获，只卖喂养储备外的盈余。
4. **劳动与土地**：晨间按负载雇佣（fib 成本 1,1,2,3,...）、资金闸门下买地（NE 早期/SW/SE）。
5. **终局清算**：第 28 天起停 CARE（银行奖金要下个产出日才付），第 29 天清仓一切——只计银行存款。

### LLM 可插拔决策接口（默认关闭）

`kgenv/bots/llm_provider.py`：`NullProvider`（默认）/ `OpenAICompatProvider`
（读 `KG_LLM_PROVIDER` / `KG_LLM_BASE_URL` / `KG_LLM_API_KEY` / `KG_LLM_MODEL` 环境变量）。
带调用次数与时长预算闸（Reasonableness Standard 的机械化落地，参照 ProgRouter 成本路由与
Bayesian Self-Escalation 思路），任何失败超时都回退启发式决策，绝不阻塞回合。
main.py 中的 `LLM_PROVIDER=None` 钩子同样默认关闭——提交形态不依赖任何外部模型。
（规则依据：赛事 rules 允许外部模型，LLM 订阅级费用符合 Reasonableness Standard。）

## 实测结果摘要（2026-08-28，详见 metrics.json 与 exports/eval_results.json）

- 评估：40 局全长度（720 回合），评估脚本 110.19s，平均 2.73s/局
- submission bot：24 局 24 胜 0 负（对 pass/random/starter/greedy_carrot 各 4 局全胜；
  对 baseline_wheat 8 局全胜），平均终局资金 30548.5
- A/B：submission 29325.13 vs baseline_wheat 11475.25（同 8 局头对头均值，约 2.56 倍）
- Elo（k=32）：submission 1460.9 > baseline_wheat 1245.8 > greedy_carrot 1162.2 >
  starter 1122.9 > random 1111.2 > pass 1097.0
- 测试：45 passed（收益模型对照官方价格表逐项断言 / 红线检查 / agent 契约 / 对局器与 Elo）

## 已知边界

- 未做 Kaggle 线上提交（队伍人工步骤，蓝图 man-submit）；线上指标在 metrics.json 中为 null。
- 引擎为官方 1.32.7；若 Kaggle 线上 kit 升级机制，需以官方页面直抓为准复核。
- baseline 对手池偏弱（最强 greedy_carrot Elo 1162）；天梯真实对手分布需线上反馈校准。
