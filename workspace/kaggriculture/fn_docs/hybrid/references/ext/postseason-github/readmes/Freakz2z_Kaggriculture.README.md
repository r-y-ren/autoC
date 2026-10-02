<p align="center">
  <img src="assets/readme/hero.svg" width="100%" alt="Kaggriculture：从农场决策到市场博弈，研究种植、生产与交易的多智能体农业对战策略">
</p>

# Kaggriculture · 农业对战策略研究

从单文件 Agent 到市场分配、末期调度与强化学习试验，这里保存了 Kaggle **[Kaggriculture](https://www.kaggle.com/competitions/kaggriculture)** 比赛中的源码、对照实验、失败方案和提交回执。你可以沿着版本记录，追溯每一次改动与对应证据。

**[研究导航](docs/generated/RESEARCH_INDEX.md) · [策略包索引](docs/generated/PACKAGES.md) · [复现指南](docs/REPRODUCIBILITY.md) · [Release 附件](https://github.com/Freakz2z/Kaggriculture/releases) · [公开范围](docs/PUBLICATION.md)**

> **代码与研究档案已公开。** 比赛仍处于榜单收敛阶段，最终提交身份、名次与赛后结论待后续补充。下文结果来自已保存的实验记录；本地对照结果与平台评分分别阅读。

## 一组结果，完整追溯

以 **0930 一小时候选**的独立确认实验为例：

| 独立世界 | 配对对局 | 相对原附件的平均分差 | 两版胜 / 平 / 负 |
| :---: | :---: | :---: | :---: |
| **12** | **96** | **+14.17** | **88 / 2 / 6** |

分差改善，胜平负相同；这组结果尚未证明胜率提高，记录标注**未提交新包**。

[实验状态与边界](reports/0930-continuous/STATUS.md) → [实验说明](reports/0930-continuous/README.md) → [固定策略包](dist/0930-final-1h.tar.gz) → [完整 SHA256 索引](docs/generated/PACKAGES.json)

## 研究什么

- **生产决策**：土地与种子预算、工人分配、作物路线、资金保护和末日资源调度。
- **市场博弈**：逐单位收益、销售槽位分配、对手行为情景和市场价值门控。
- **学习与评测**：GRPO / PPO、固定回放、反应式对手，以及 Python / Rust 引擎核对。

源码、seed、对手、引擎和结果共同描述一次实验。版本号用于定位记录，是否采用候选由相应评测证据决定。

## 选择你的入口

| 想做什么 | 从这里开始 |
| --- | --- |
| 阅读完整研究与失败记录 | [研究与报告导航](docs/generated/RESEARCH_INDEX.md) |
| 获取指定版本及内容哈希 | [固定策略包](docs/generated/PACKAGES.md) · [JSON 清单](docs/generated/PACKAGES.json) |
| 在本地运行或复现评测 | [复现指南](docs/REPRODUCIBILITY.md) |
| 获取公开产物与受限回放指引 | [发布范围与获取说明](docs/PUBLICATION.md) |
| 查看版本沿革和历史线上记录 | [历史首页](docs/HISTORY.md) |

<details>
<summary><strong>展开版本沿革与近期实验</strong></summary>

下表保留记录中的结果和提交状态。平台后续状态以有时间戳的回执为准。

| 版本 / 方向 | 记录中的结论 | 证据 |
| --- | --- | --- |
| 0930 一小时候选 | 12 世界、96 配对；平均分差 +14.17，胜平负不变；记录标注未提交 | [状态](reports/0930-continuous/STATUS.md) · [策略包](dist/0930-final-1h.tar.gz) |
| 0930 DDL 种子缓冲 | 3 新世界、18 配对；平均分差 +6.67，胜平负不变 | [结果](reports/0930-deadline-seed/README.md) · [策略包](dist/0930-ddl.tar.gz) |
| 0930 收官路线组合 | 独立快速检查平均分差 −8.94，1 场胜转负；不推荐替换原附件 | [完整结果](reports/0930-final-iteration/README.md) |
| 0930 公开策略检索 | 8 个公开参考包；作者团队分数与公开文件身份分别核查 | [来源搜索](reports/public-source-search-20260930/README.md) |
| V28 GPU 市场门控 | 本地均值改善，尾部风险未过门槛；经授权作为线上实验提交 | [研究](research/v28/market_value/RESULTS.md) · [回执](reports/v28/SUBMISSION.md) |
| V21～V31 | 作物与劳动规划、GRPO / PPO、市场分配、公开方案迁移和淘汰试验 | [研究索引](docs/generated/RESEARCH_INDEX.md) |
| V20 | 末期种子预算与重复施肥保护；保留冻结包及线上记录 | [结果](research/v20/RESULTS.md) · [提交](research/v20/SUBMISSION.md) |
| V17～V19 | 完整核心与市场分配、资金保护、末日调度 | [V17](research/v17_round4/RESULTS.md) · [V18](research/v18_major/RESULTS.md) · [V19](research/v19/RESULTS.md) |

</details>

## 在本地开始

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tools/evaluate.py --opponent starter --seeds 11 37 73
```

这条命令运行根目录的**历史 V8**。后续版本位于 `research/` 和固定 `dist/` 包中；按[包索引](docs/generated/PACKAGES.md)选择版本，再阅读对应 `REPRODUCE.md`。官方引擎固定为 `kaggle-environments==1.32.7`。

外部 Rust 模拟器、历史环境路径和各类评测的解释边界见[复现指南](docs/REPRODUCIBILITY.md)。

## 仓库地图

```text
Kaggriculture/
├── main.py       历史 V8 单文件入口
├── research/     策略源码、构建、训练与对照实验
├── reports/      评测报告、线上回执与时点分析
├── dist/         冻结策略包与公开参考包
├── tools/        提取、构建、评测与归档工具
├── tests/        协议、保护逻辑、结算与归档检查
├── docs/         导航、复现、历史记录与开源说明
└── assets/       README 视觉素材
```

可再分发的运行日志与研究产物通过 Release 分卷提供。线上下载的原始回放、日志和相关完整状态轨迹保留本地，公开其[路径与 SHA256 清单](docs/generated/WITHHELD.json)及[获取指引](docs/PUBLICATION.md)。历史实验目录保持原位置。

<details>
<summary><strong>维护索引与准备新的发布快照</strong></summary>

```bash
.venv/bin/python tools/prepare_open_source.py index
.venv/bin/python tools/prepare_open_source.py audit --history
```

本地审阅产物位于 `.release/`；导出、恢复及赛后发布条件见[开源交接](docs/OPEN_SOURCE.md)。新增内容后需重新生成快照。

</details>

## 来源、许可与参与

本地工具和原创改动采用 **[Apache-2.0](LICENSE)**。第三方源码、路线、权重及公共比赛资料保留各自的许可与署名，再分发条件逐项核对。

感谢 Ahmed Berat Ozer、Thomas Tschinkel、KoshinM、Dmitrii Gluzdov、Seyit Kaan Gunes、Nathan Jacob、tetsutani 等公开方案作者。具体继承关系、上游贡献及本地修改见[第三方声明](THIRD_PARTY_NOTICES.md)。

**[参与研究](CONTRIBUTING.md) · [第三方声明](THIRD_PARTY_NOTICES.md) · [NOTICE](NOTICE)**  
维护者：[Freakz2z](https://github.com/Freakz2z)
