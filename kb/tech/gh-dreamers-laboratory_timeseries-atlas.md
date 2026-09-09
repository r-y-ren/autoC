---
id: gh-dreamers-laboratory_timeseries-atlas
name: "Time Series Atlas：现代时序预测架构活地图（每篇一个可跑最小实现 + 基线纪律）"
field: [time series forecasting]
directions: [数模与时序预测]
published: "2026-09-02"
maturity: demo
signal:
  venue: GitHub
  stars: 152
  runnable: true
competition_fit:
  - track: "数模-预测与评估"
    edge: "数模赛题含预测问时的『基线纪律』武器库：仓库立场直给——先跑 DLinear（50 行、笔记本一分钟）打不过就别上重模型；ETT 榜单增益大多是 lookback/归一化/通道处理的噪声，先定协议再谈架构；11 个目录按机制分类（线性基线/attention 时代/PatchTST/iTransformer/CycleNet/混合器/SSM/扩散/基础模型/经典统计），01/03/04/05 是自包含实现、合成数据笔记本一分钟出 MSE/MAE 对照 seasonal-naive——赛前搭预测管线时当骨架与 sanity check，避免在调参噪声上烧掉赛期"
    reuse_cost: "低"
    open_source: "https://github.com/dreamers-laboratory/timeseries-atlas（Apache-2.0；另指向 thuml/Time-Series-Library 跑原版）"
  - track: "Kaggle-竞赛"
    edge: "时序赛开局选型地图：零样本前沿在哪（Chronos-2 在 GIFT-Eval 79.8% 胜率，2025-10 口径）、短季节序列上经典统计（AutoETS/AutoARIMA/季节朴素）仍是对照组、何时该用 patch/通道独立/显式周期残差各是哪个家族——比翻论文快，且每个结论带可复跑代码或权威库指针"
    reuse_cost: "低"
    open_source: "https://github.com/dreamers-laboratory/timeseries-atlas（Apache-2.0）"
sources:
  - url: https://github.com/dreamers-laboratory/timeseries-atlas
    title: "dreamers-laboratory/timeseries-atlas: A map of modern time-series forecasting architectures"
    accessed: "2026-09-09"
  - url: https://raw.githubusercontent.com/dreamers-laboratory/timeseries-atlas/main/README.md
    title: "README 全文（架构地图/可跑命令/三条立场/评测指针）"
    accessed: "2026-09-09"
---

# Time Series Atlas：现代时序预测架构活地图

## 是什么

Dreamers Inc（商业预测/agent 团队）2026-09-02 开源的时序预测架构导览仓库（152 star，Python，Apache-2.0，API 实查 2026-09-09：推送至 2026-09-02）。动机自述："文献是有意让人迷惑的——2021 年以来每篇论文都在同样八个数据集上声称 SOTA，增量极小"，并引用一篇 ICML 2026 position paper（arXiv 2512.22702，README 内链接）指出归一化选择往往比被宣传的架构更重要。主体是 11 个机制分类目录的"地图"：01 线性基线（DLinear/NLinear）、02 attention 时代（Informer/Autoformer/FEDformer/Pyraformer）、03 PatchTST、04 iTransformer、05 CycleNet、06 混合器（TimeMixer/xPatch/WPMixer）、07 SSM 与 xLSTM（S-Mamba/xLSTMTime/TiRex）、08 KAN（TimeKAN）、09 扩散（TimeDiff/CCDM/ARMD）、10 预训练基础模型（Chronos-2/TimesFM 2.5/Moirai 2.0/Toto/Sundial）、11 经典统计基线（AutoETS/AutoARIMA/季节朴素）。其中 01/03/04/05 目录是自包含最小实现（几百行内），`python common/train.py --model dlinear|patchtst|itransformer|cyclenet` 在合成多季节合成数据上笔记本一分钟内训练并打印对照 seasonal-naive 的 MSE/MAE；其余目录是"导览 + 指向权威实现"（并点名 thuml/Time-Series-Library 可一站式复跑）。README 另给三条实践立场与评测指针（GIFT-Eval、fev-bench）。

## 解决什么问题

时序预测文献不可信与不可复现：论文增量淹没在协议差异（lookback 长度、归一化、通道处理都能翻转排名）里，队伍选型缺少诚实的对照组。本仓库把"并排读机制"变成可执行动作——每个重要架构都有短 README 与（条件允许时的）可跑最小实现，让使用者自己形成判断。

## 相比前方法优势

- 相比论文清单式 awesome 列表：有立场（线性基线优先、榜单噪声警告、前沿已移向预训练模型）且关键四目录可跑，一分钟内建立"我的模型必须打过谁"的基准线；
- 相比 thuml/Time-Series-Library 等大而全库：这是教学级最小实现 + 地图，目标是理解而非刷榜，两者 README 内互补引用；
- 相比综述论文：附可复跑命令与前沿榜单指针（Chronos-2 于 GIFT-Eval 79.8% 胜率，2025-10 快照，README 自注"leaderboard 会动，引用前重查"）。

## 局限（如实标注）

- 仅 4/11 目录是自包含实现，其余是指针导览——"每篇都可跑"只在子集上成立（README 如实声明）；
- 自包含实现跑合成数据，直接用于真实赛题数据需自己接数据加载与协议；非玩具级精度工程（无调参配方、无集成策略）；
- 基础模型目录是指针而非微调配方，零样本之外的适配（few-shot/微调/协变量）未覆盖；
- 团队背景是商业咨询公司（README 页尾有业务引流），立场三条属经验性主张而非系统实证；年轻仓库（2026-09-02 创建），覆盖范围会漂移。

## 如何用于比赛

1. **数模赛前基建（主用）**：把 01 线性基线 + 11 经典统计作为任何预测问的强制第一层——"打过 DLinear 了吗"写成队内 checklist；04 iTransformer / 05 CycleNet 的最小实现当骨架改造（通道独立、显式周期残差都是数模高频有效结构）；其"先声明协议再报提升"的立场直接对应数模论文的敏感性分析章节，评审可信度加分。reuse_cost 低：pip install torch numpy 即跑，一分钟出第一条基线。
2. **Kaggle 时序赛开局选型（次用）**：按数据形态查地图选家族——强周期选 CycleNet 类、多变量通道独立选 iTransformer/PatchTST 类、冷启动大数据直接试 Chronos-2/TimesFM 零样本打基线、短季节序列先跑 AutoETS/AutoARIMA；再用 GIFT-Eval/fev-bench 榜单指针复核当前前沿。
