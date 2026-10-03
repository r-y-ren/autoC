# Kaggriculture v4 提交版

2026-09-20。本轮完成策略强化、对照实验、未参与调参场景验收和提交包验证。没有向 Kaggle 上传，也没有代替用户接受比赛规则。

## 交付文件

- `submissions/release_v4/main.py`：推荐直接提交的单文件智能体。
- `submissions/release_v4/submission.tar.gz`：等价压缩包，根目录仅一个 `main.py`。
- `submissions/release_v4/manifest.json`：大小和 SHA-256 校验值。
- `submissions/release_v4/validation.json`：实际压缩包解包验证结果。
- `submissions/release_v4/benchmark_summary.json`：最终验收摘要。

提交时选择 main.py 或 submission.tar.gz 中的一个即可，不要上传整个项目目录。提交包中没有账号信息、环境目录、历史实验或回放。

## 本轮的策略变化

采用种植与畜牧混合经营：两只鹅、一头牛、一只羊，安排专人取饲料、喂养、照料、收获并收集肥料出售。完成畜牧任务后工人参与种植。种植仍覆盖小麦、胡萝卜和甜瓜，选择时计入市场库存及自身未来供给；维持饲料储备并避免同时取走同一份物资。

在资金与赛季剩余时间充足、已占用土地较多时购买第二块土地。工人规模随土地增加，播种截止与最后回仓出售继续受赛季剩余时间约束。

这是经过对照实验筛选的确定性策略程序，没有进行神经网络或深度强化学习训练。它仅使用观察值和配置，不依赖跨回合全局记忆、网络、外部 API 或第三方 Python 库。

## 实验取舍

开发场景使用种子 20、21、22。比较了扩地种植、四只动物混合经营、一块/三块土地、两只动物，以及关闭/单独开启需求预测和对手供给预测等变体。各版本和原始报告分别保存在 `agents/`、`experiments/`、`results/`。

- 初步扩地种植版对旧版 6 局赢 4 局。
- 四只动物混合经营初版对旧版 6 局全胜。
- 三块土地的开发平均收益低于两块，最终最多使用两块。
- 关闭远期供需预测的混合版，在开发场景对旧版的平均金币为 49,225.3。
- 单独开启需求预测、单独开启对手供给预测的版本，各对关闭预测版本打了 3 局，均为 0 胜。最终移除了这些预测计算，避免保留表现不佳的复杂度。

这些小样本只用于选择候选，不是泛化结论。版本选定后使用下面的新场景验收，未再依照验收结果调整参数。

## 最终验收

测试环境：Windows，Python 3.12.11，未修改的 kaggle-environments 1.32.7，默认 720 步。不同对手均是本项目独立保存的历史版本，并非排行榜强手。

| 对手 | 新场景种子 | 对局（双方位置） | 胜局 | 平均最终金币 |
|---|---|---:|---:|---:|
| 第一轮基线 v1 | 100–107 | 16 | 16 | 49,479.4 |
| 扩地种植 v2 | 110–113 | 8 | 8 | 49,339.9 |
| 混合经营实验 v3 | 114–117 | 8 | 8 | 54,972.0 |

这 32 局全部正常完成，结束时携带物与仓库均清空。按双方位置配对的结果存在相关性，不能视为 32 个完全独立场景。原始报告：`results/release-vs-v1.json`、`results/release-vs-crop-v2.json`、`results/release-vs-mixed-v3.json`。

另外完成两局自我对战，以及从实际提交压缩包取出代码进行的一局完整自我对战。全部正常完成。九项边界测试通过；对十个不同游戏阶段的观察，在 Python 的 `-I -S` 隔离模式（禁用第三方包）下验证动作一致。

本轮验收记录的最长单步决策约 0.0502 秒，低于本地 specification 的 1 秒限制；这是本机测量，不是 Kaggle 容器性能保证。单文件约 12 KB，压缩包约 3.7 KB。

## 提交方法

在比赛页面确认已报名并接受规则后，选择提交入口，上传：

`submissions/release_v4/main.py`

也可在已安装并完成登录的 Kaggle CLI 中，于项目根目录执行：

```powershell
kaggle competitions submit kaggriculture -f submissions/release_v4/submission.tar.gz -m "v4 mixed farming - local validation passed"
```

本轮没有安装或配置 Kaggle CLI。提交后应查看服务器验证对局是否成功；成功上传不等于已通过线上验证。只有服务器验证成功后，才开始观察实战排名。

入口为 `agent(obs, configuration=None)`，也支持只传入 obs。主文件只导入标准库 math。压缩包根目录位置已经核验。

## 复现与打包

```powershell
.venv/Scripts/python.exe -m unittest -v test_agent
.venv/Scripts/python.exe evaluate.py --opponent agents/baseline_v1.py --seeds 100 101 102 103 104 105 106 107 --both-seats --output results/release-vs-v1.json
.venv/Scripts/python.exe build_submission.py
.venv/Scripts/python.exe validate_submission.py
```

构建脚本固定压缩包时间戳并核验唯一成员；原始源码及压缩包哈希保存在 manifest 中。修改代码后必须重新构建和验证，不应沿用旧结果。

## 当前限制

尚未与外部强手对战，也未取得线上分数。动物组合目前固定，未根据商店类型调整；尚未加入肥料施用、番茄/草莓种植和更精细的销售时机优化。自定义地图、市场参数和短赛季不属于已验证配置。后续最有价值的是获取线上验证与对局回放，再按真实失败模式改进。

官方接口及提交说明参考本项目保留的 AGENTS.md、README.md，以及比赛页面：
https://www.kaggle.com/competitions/kaggriculture/overview
