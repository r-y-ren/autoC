**当前版本为 release_v8。最新验收与提交方式见 RELEASE_V8.md，原 v7 保留。**

# 开发记录

**以下为第一轮历史记录；上一版策略与验收见 RELEASE_V7.md，原文件保留于 submissions/release_v7/。**

更新：2026-09-20。原有 AGENTS.md、README.md 为官方参考材料，未修改；其 SHA-256 与安装的官方环境附带文件一致。

## 当前成果

- Python 3.12.11 独立环境 `.venv`，官方模拟器 `kaggle-environments==1.32.7`。
- `main.py`：仅依赖 Python 标准库、离线运行、无需跨回合内存的基础策略。
- `evaluate.py`：使用官方 `make` / `env.run` 及文件路径加载智能体，输出逐局金币、胜负、完成状态和代码哈希。
- `test_agent.py`：种子共享预算、当日浇水、成熟日增产、期末出售、不修改输入等边界检查。
- `requirements-lock.txt`：固定本机已验证依赖；`setup.ps1` 可重建环境。

安装采用最小依赖集合，未安装其他游戏所需的机器学习库。导入时可能出现与本比赛无关的环境加载提示，评估报告保存了这些提示。Kaggriculture 本身使用未经修改的官方环境正常运行。此环境不用于运行其他 Kaggle 游戏。

## 策略

每天雇佣最多六名便宜工人，经营初始地块。根据市场库存、已经种下的产量、已有种子和携带库存，估算小麦、胡萝卜、甜瓜的种植收益。优先浇水及收获，按距离分配不同地块给工人。最后阶段停止播种，预留回仓与出售时间。

第一版尚未加入动物、肥料、扩地、连续产出作物或显式对手建模。收益估算使用默认市场曲线，未支持自定义 marketParams；当前价格与已在田产量只是未来价格的近似。当前参数适用于默认 720 步赛季；非默认配置不作为已验证支持范围。

## 验证结果

全部通过官方文件加载入口运行，未修改游戏引擎：

| 测试 | 结果 |
|---|---|
| 5 项边界测试 | 全部通过 |
| 对官方 starter，种子 0–4，交换位置 | 10 局全胜，平均最终金币 43,108.9 |
| 上述 10 局最终金币范围 | 41,358–47,014 |
| 自我对战，种子 10、11，交换位置 | 4 局全部正常完成，平均金币 27,189 |
| 上述 14 局结束状态 | 均为 DONE / DONE，720 个记录状态 |
| 上述 14 局结束时携带物及仓库剩余 | 均为 0 |

原始报告位于 `results/starter.json`、`results/selfplay.json`。种子 0 的完整回放保存在 `results/baseline-seed0-seat0-replay.json`。

自我对战包含同一局交换视角的重复，主要用于稳定性检查，不是四个独立强度样本。starter 很弱；上述胜率不代表线上排名。自我对战收益较低与双方共同生产导致的市场供给变化相符，后续需要对强对手验证。

## 运行

在本文件所在目录的 PowerShell 中：

```powershell
.venv/Scripts/python.exe -m unittest -v test_agent
.venv/Scripts/python.exe evaluate.py --seeds 0 1 2 3 4 --both-seats --output results/starter.json
.venv/Scripts/python.exe evaluate.py --opponent main.py --seeds 10 11 --both-seats --output results/selfplay.json
```

重建环境：运行 `./setup.ps1`，需要已安装的 uv。不要安装到系统 Python。

## 已核对的比赛要求

2026-09-20 已通过比赛规则网页读取完整正文：
https://www.kaggle.com/competitions/kaggriculture/rules

- 每队最多五人，每日最多五次提交。
- 对局运行期间不得从提交包与环境之外引入信息，也不得向外发送信息。因此智能体没有网络/API 调用。
- 不得跨队私下共享比赛代码或数据；若主动公开代码，需在比赛相关 Kaggle 论坛或 Notebook 同步共享。
- 外部工具和数据需要符合规则中的可获得性、成本及许可要求。
- 规则写明可选最多两个最终提交，概览写明使用最新两个提交；正式提交前以届时官方说明核对这一操作差异。
- 本地环境 specification 的 actTimeout 为 1 秒。概览列出的提交资源为 6.5 GiB RAM、1.6 vCPU、8 GiB HDD、100 MiB 文件限制；尚未进行线上容器验证。

官方接口参考：
https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kaggriculture

## 下一阶段

1. 增加更强的独立策略对手及未用于开发的随机种子集合。
2. 比较畜牧、肥料回收、按商店需求分配产能和扩地投资的真实收益。
3. 从回放统计无效动作、工人闲置、滞销和作物损失，改进调度。
4. 核对用户账号的报名状态和线上环境后，再进行首次提交。

目前没有登录账号、接受规则、下载受限比赛数据或提交作品。页面未登录不代表用户账号未报名；报名状态尚未核验。
报名截止北京时间 2026-09-24 07:59，最终提交截止 2026-10-01 07:59，以官网后续更新为准。
