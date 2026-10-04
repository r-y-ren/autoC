"""Promote only the independently confirmed, package-validated candidate."""
import hashlib
import json
from pathlib import Path

r=Path(__file__).parent
release=r/'submissions/release_v7'
manifest=json.loads((release/'manifest.json').read_text())
source=(release/'main.py').read_bytes()
assert hashlib.sha256(source).hexdigest()==manifest['source_sha256']
assert hashlib.sha256((release/'submission.tar.gz').read_bytes()).hexdigest()==manifest['archive_sha256']
assert (release/'validation.json').exists()
rows=[]
for label,title in [('v6','我们的 v6'),('v56','公开 V56'),('mirror','公开 Orderbook')]:
    baseline=json.loads((r/f'results/round7_final_orderbook_{label}.json').read_text())
    candidate=json.loads((r/f'results/round7_final_fusion_{label}.json').read_text())
    assert baseline['games']==candidate['games']==12
    gains=[b['delta']-a['delta'] for a,b in zip(baseline['results'],candidate['results'])]
    assert min(gains)>=0
    record=lambda d:f"{d['wins']}/{d['games']-d['wins']-d['ties']}/{d['ties']}"
    rows.append(f"| {title} | {record(baseline)} | {record(candidate)} | {sum(gains)/12:.1f} |")
report='''# v7：交易顺序与投入品预算融合

2026-09-22。本地已经生成并验证，可上传 Kaggle；本轮没有代为线上提交。3000 分仍是目标，当前没有 v7 的线上分数。

## 本次选择

采用 shiiin9 的 Orderbook 完整公开策略，再追加 Ahmed V56 的剩余种子预算、无收益施肥抑制。保留全部原有作者和 Apache-2.0 署名。我们完成了接口融合、独立对照、错误审查和实际包验证，没有声称这些上游算法是自行训练成果。

与此前 v6 相比，本版改进买卖订单的执行顺序、晚期番茄投资判断，以及种子与肥料投入。前两位的回放研究帮助确认生产、资金与交易共同优化的方向；其模仿路线尚不足够稳定，没有用作本包的核心生产路线。

## 冻结后的独立确认

种子56100–56105，三个会反应的真实公开程序，双方席位，各12局。表中为胜/负/平，金币差改善相对于同种子同席位的原Orderbook基线。

| 对手 | 原Orderbook基线 | v7融合版 | 平均金币差改善 |
|---|---:|---:|---:|
ROWS

候选合计 **30胜4负2平**，基线16胜8负12平；36组配对金币差均非负，平均改善345.8。对v6直接12局为10胜2负，两场败局来自同一个世界，两席都差267金币；本版仍有弱点，不能用总胜率掩盖。

这些程序有共同上游，双方席位及多对手复用同一世界种子存在相关性，不能理解成36个独立环境。种子不是排行榜评级，金币差也不能直接换算成评级。

另做DSM公开回放编译策略的可反应对照：v7和v6各4局均胜，v7平均自身金币多26。这只是一个根据DSM历史动作制作的模仿程序，不是DSM当前的私有智能体。

## 本轮没有纳入的改动

- 闲工更早送鸡蛋/西红柿：6局1胜5负，淘汰。
- 直接照抄Vadim/DSM的动作：原请求存在因钱不够而失败的订单，换对手后会断资金或多雇工；已编译实际成交并保存研究路线，但单路线泛化仍有大幅亏损。
- 19株番茄：原开发地图曾多赚约9800，后续改调度却出现约9860回退，且额外施肥/收获仍需严格验收；本次保留为研究，未加入提交包。

## 实际提交包验证

- 官方环境1.32.7，两个完整对局均DONE；无stderr。
- 将实际包解出后，在禁用第三方包的同一进程连续核对1438个动作；原始观测键序和排序键序各一轮，均完全一致。
- 检查种子、肥料、订单排序、番茄判断以及所有顶层REPORT/STATS和底层fallback计数；错误为零。
- 核验跨局状态重置；仅诊断用累计计数没有被误当作策略状态。
- 包内为main.py、NOTICE.txt、LICENSE.txt。源码运行不需要联网、外部模型或额外数据文件。

## 文件与来源

- 提交包：`submissions/release_v7/submission.tar.gz`（635043字节）。
- 单文件入口：`submissions/release_v7/main.py`；根目录main.py已更新为同一内容，旧v6保留。
- 研究：[RESEARCH_ROUND7.md](RESEARCH_ROUND7.md)，反馈：[FEEDBACK3_REPORT.md](FEEDBACK3_REPORT.md)。
- [Orderbook，Notebook版本2](https://www.kaggle.com/code/shiiin9/your-market-list-is-an-order-book)
- [Ahmed V56，Notebook版本1](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer)
- 源码SHA-256：SOURCEHASH
- 包SHA-256：ARCHIVEHASH

完整逐局结果在results/round7_final_*.json，打包与隔离记录在submissions/release_v7/validation.json。
'''.replace('ROWS','\n'.join(rows)).replace('SOURCEHASH',manifest['source_sha256']).replace('ARCHIVEHASH',manifest['archive_sha256'])
(r/'RELEASE_V7.md').write_text(report,encoding='utf-8')
(r/'main.py').write_bytes(source)
for file in ['build_submission.py','validate_submission.py']:
    (r/file).write_text('"""Build and verify the selected v7; previous releases remain frozen."""\nfrom build_release_v7 import main\n\nif __name__ == "__main__":\n    main()\n',encoding='utf-8')
dev=(r/'DEVELOPMENT.md').read_text(encoding='utf-8')
dev=dev.replace('**当前版本已更新为 release_v4。以下为第一轮历史记录，最新策略、验收及提交方式见 `RELEASE_V4.md`。可提交文件在 `submissions/release_v4/`。**',
                '**当前版本为 release_v7。以下为第一轮历史记录；最新策略、验收及提交方式见 RELEASE_V7.md，提交文件位于 submissions/release_v7/。**')
(r/'DEVELOPMENT.md').write_text(dev,encoding='utf-8')
print('Promoted validated v7 locally; no online upload.')
