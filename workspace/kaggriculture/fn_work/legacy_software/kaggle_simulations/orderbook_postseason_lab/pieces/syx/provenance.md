# provenance — syx（sunyuxiang136/kaggriculture-silver-agent）

- **repo URL**: https://github.com/sunyuxiang136/kaggriculture-silver-agent
- **commit sha**: `be16043a8b6842357fea0b86a150629d62c7ab32`（HEAD，2026-10-01T16:23:47+08:00 "docs: update repository url"）
- **抓取时间**: 2026-10-02 12:06Z（git clone --depth 1，GitHub REST 11:0xZ 复核 license=Apache-2.0、pushed=2026-10-01T08:29:30Z）
- **许可**: Apache-2.0（仓内 LICENSE 全文；main.py 头部保留上游 Apache-2.0 署名链：haideptry "The 2965 Master Hybrid Engine"→Thomas Tschinkel/yhay81/destbreso/aurax7/tetsutani/prvsiyan/Dmitrii Gluzdov/Ahmed Berat Ozer 等 V39/V46 系谱）
- **自报声明**（README，抓取 2026-10-02，自报未复核）:
  - "Kaggle 模拟博弈对抗赛 Kaggriculture 银牌方案完整源码"（README §标题/首段）
  - "achieving a prestigious **Silver Medal**"，作者口径 "Engineered by **Shawn404**"
  - 徽章口径 "Step Latency < 3ms / step"
  - 官方未发奖（终榜 ~10-15）；"银牌"为自报
- **装载形态**: 整包单文件交件形态——`main.py`（5,814,850B，纯标准库，requirements.txt 明言 "Pure Python standard library only"）；入口=末 callable `agent(observation, configuration=None)`（文件尾 `agent = globals().pop('agent')` 主动挪到命名空间末位，贴合官方 last-callable 语义）。`decompressed/` 为模块拆解副本（非运行路径）。零修改直跑（j23._load_entry 全新命名空间）。
- **归档说明**: 本目录=仓库 shallow clone 原样归档（含 .git）；判决 harness 只读 `main.py`。
- clone HEAD: be16043a8b6842357fea0b86a150629d62c7ab32（.git 已按嵌套仓纪律移除，源树全保留）
