"""Promote the exact technically verified bytes only after independent acceptance."""
import hashlib
import json
import shutil
import tarfile
from pathlib import Path

from compare_round8 import compare, read

ROOT=Path(__file__).resolve().parent
SOURCE_HASH='9fa83701138e80e3e5f9a6479cc2fa1c7e8a8965c4bd85d4e45d05ec5d4ffd4e'
ARCHIVE_HASH='017b3ee7a82943f378f0bb455a575dca796558c557bd823bcde039715daf3977'
V7_HASH='273ca38d83d110166af4e2f2c6748892328488d5292f39fdbe4ef87b11350197'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def count_execution_records(path):
    """Keep failed attempts visible; a JSONL row is not necessarily a game."""
    counts=dict(recorded_executions=0,completed_games=0,valid_games=0,
                invalid_records=0,incomplete_records=0,completed_invalid_games=0,
                malformed_json_records=0)
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.strip():continue
        counts['recorded_executions']+=1
        try:
            row=json.loads(line)
        except json.JSONDecodeError:
            row=None
            counts['malformed_json_records']+=1
        complete=isinstance(row,dict) and row.get('states')==720 and row.get('statuses')==['DONE','DONE']
        valid=complete and row.get('valid') is True
        counts['completed_games']+=int(complete)
        counts['valid_games']+=int(valid)
        counts['invalid_records']+=int(not valid)
        counts['incomplete_records']+=int(not complete)
        counts['completed_invalid_games']+=int(complete and not valid)
    return counts


def main():
    raise SystemExit('Retired single-candidate publisher. Use publish_round8_selection.py, which enforces the updated development and multiplicity gates.')
    baseline=read([ROOT/'results/round8_v7_confirmation.json'])
    candidate=read([ROOT/'results/round8_candidate_confirmation.json'])
    assert len(baseline)==len(candidate)==480,'Independent panel not complete'
    assert baseline.keys()==candidate.keys(),'Unpaired confirmation cases'
    for rows,expected in [(baseline,V7_HASH),(candidate,SOURCE_HASH)]:
        assert {r['candidate_sha256'] for r in rows.values()}=={expected}
        assert len({r['seed'] for r in rows.values()})==40
        for r in rows.values():
            assert r['valid'] and r['states']==720 and r['statuses']==['DONE','DONE']
            assert not r['stderr'] and not any(t['nonzero'] for t in r['telemetry'])
    comp=compare(baseline,candidate)
    comparison_path=ROOT/'results/round8_confirmation_comparison.json'
    comparison_path.write_text(json.dumps(comp,indent=2),encoding='utf-8')
    assert comp['metrics']['points_change']['world_bootstrap_95'][0]>0,'Independent improvement not established; do not promote'
    stage=ROOT/'submissions/candidate_v8'
    technical=json.loads((stage/'validation.json').read_text(encoding='utf-8'))
    assert technical['technical_acceptance_passed']
    assert technical['source_sha256']==SOURCE_HASH and technical['archive_sha256']==ARCHIVE_HASH
    assert sha(stage/'main.py')==SOURCE_HASH and sha(stage/'submission.tar.gz')==ARCHIVE_HASH
    with tarfile.open(stage/'submission.tar.gz','r:gz') as tf:
        assert tf.getnames()==['main.py','NOTICE.txt','LICENSE.txt']
        assert tf.extractfile('main.py').read()==(stage/'main.py').read_bytes()
    assert sha(ROOT/'main.py') in {V7_HASH,SOURCE_HASH},'Root main.py changed outside this experiment; preserve it'
    release=ROOT/'submissions/release_v8';release.mkdir(exist_ok=True)
    for name in ['main.py','submission.tar.gz','NOTICE.txt','LICENSE.txt']:
        if (release/name).exists():assert sha(release/name)==sha(stage/name),'Do not overwrite a different frozen release'
        shutil.copy2(stage/name,release/name)
    shutil.copy2(stage/'validation.json',release/'technical_validation.json')
    shutil.copy2(comparison_path,release/'confirmation_comparison.json')
    totals={}
    for label,rows in [('v7',baseline),('v8',candidate)]:
        values=list(rows.values())
        totals[label]={'wins':sum(r['delta']>0 for r in values),'losses':sum(r['delta']<0 for r in values),
                       'ties':sum(r['delta']==0 for r in values),'points':sum(r['points'] for r in values)/len(values)}
    runs={p.name:count_execution_records(p) for p in (ROOT/'results').glob('round8_*.jsonl')}
    run_totals={key:sum(counts[key] for counts in runs.values()) for key in
                ('recorded_executions','completed_games','valid_games','invalid_records',
                 'incomplete_records','completed_invalid_games','malformed_json_records')}
    manifest={'version':'v8','source_sha256':SOURCE_HASH,'archive_sha256':ARCHIVE_HASH,
              'archive_bytes':(release/'submission.tar.gz').stat().st_size,
              'entry':'round8_production_fusion_agent','technical_pass':True,'local_strength_pass':True,
              'online_submitted':False,'online_rating':None,'confirmation_worlds':40,'confirmation_games_per_policy':480,
              'confirmation_totals':totals,'paired_metrics':comp['metrics'],
              'league_executions':runs,'league_execution_count':run_totals['recorded_executions'],
              'league_execution_summary':run_totals,
              'league_counting_rule':'Completed means states=720 and both statuses=DONE; valid additionally requires valid=true. Invalid includes incomplete, failed-validation and malformed records; records remain preserved.',
              'technical_evidence':'submissions/candidate_v8/validation.json',
              'decision_frozen_before_confirmation':'research/round8/finalist_frozen.json',
              'limitations':['Several opponents share source ancestry.','Replay proxies are not the original private top-player programs.',
                             'Nineteen-tomato branch lacks broad activation evidence.','Local results do not establish a Kaggle rating.']}
    (release/'release_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    shutil.copy2(release/'main.py',ROOT/'main.py')
    wrapper='''"""Rebuild and technically recheck the frozen v8; performance evidence stays separate."""
from pathlib import Path
import subprocess
import sys

def main():
    root=Path(__file__).resolve().parent
    subprocess.run([sys.executable,str(root/'build_release_round8.py'),
        '--candidate','experiments/round8_bounded_production.py',
        '--stage','submissions/release_v8',
        '--expected-sha256','''+repr(SOURCE_HASH)+''',
        '--entry','round8_production_fusion_agent','--profile','bounded-production',
        '--label','candidate_v8'],cwd=root,check=True)

if __name__=='__main__':main()
'''
    (ROOT/'build_release_v8.py').write_text(wrapper,encoding='utf-8')
    for name in ['build_submission.py','validate_submission.py']:
        (ROOT/name).write_text('"""Build and verify frozen v8; earlier releases remain preserved."""\nfrom build_release_v8 import main\n\nif __name__ == "__main__":\n    main()\n',encoding='utf-8')
    labels={'submissions/release_v6/main.py':'v6','submissions/release_v7/main.py':'v7',
            'external/orderbook.py':'Orderbook','external/round8/master2965/main.py':'Master2965',
            'experiments/round8_top2_dsm_strict.py':'DSM 回放重构代理','external/round8/fieldcraft/main.py':'Fieldcraft'}
    table=['| 对手 | v7 胜/负/平 | v8 胜/负/平 | 平均配对金币差改善 |','|---|---:|---:|---:|']
    for opp in labels:
        counts=[]
        for rows in [baseline,candidate]:
            g=[r for r in rows.values() if r['opponent']==opp]
            counts.append('/'.join(str(sum((r['delta']>0 if sign==1 else r['delta']<0 if sign==-1 else r['delta']==0) for r in g)) for sign in [1,-1,0]))
        table.append(f"| {labels[opp]} | {counts[0]} | {counts[1]} | {comp['opponents'][opp]['margin_change']:+.1f} |")
    ci=comp['metrics']['points_change']['world_bootstrap_95'];gain=comp['metrics']['points_change']['mean']
    doc=f'''# Kaggriculture v8 提交说明

本地独立对抗通过，提交包已准备好；尚未上传 Kaggle，没有线上 3000 或 3200 分承诺。原 v7 完整保留。

## 提交文件

- 推荐上传 `submissions/release_v8/submission.tar.gz`，645,772 字节。
- 单文件入口为 `submissions/release_v8/main.py`；根目录 `main.py` 已同步。
- 包内仅有 `main.py`、`NOTICE.txt`、`LICENSE.txt`，无需外部模型、网络或其他文件。
- 压缩包 SHA-256：`{ARCHIVE_HASH}`。
- 源码 SHA-256：`{SOURCE_HASH}`。

## 独立验证

先用20个开发世界筛选并冻结源码，再用40个未参与调参的世界、6类对手、交换双方位置验证。v7与v8各480局，总计960局；两个席位及同图不同对手按同一世界聚合，未当成独立地图。

v7：{totals['v7']['wins']}胜、{totals['v7']['losses']}负、{totals['v7']['ties']}平；v8：{totals['v8']['wins']}胜、{totals['v8']['losses']}负、{totals['v8']['ties']}平。按胜1、平0.5、负0计，平均积分提高 **{gain*100:.2f} 个百分点**；按世界重采样的95%区间为 **{ci[0]*100:.2f}～{ci[1]*100:.2f} 个百分点**。

{chr(10).join(table)}

全部960局默认规则对抗完成720状态，无stderr或双方已暴露的内部错误。完整配对证据见 `results/round8_confirmation_comparison.json`，逐局数据见对应JSONL与源码哈希清单。

本轮联赛累计记录 **{run_totals['recorded_executions']:,} 次执行尝试**，其中 **{run_totals['completed_games']:,} 局达到720状态且双方DONE**，**{run_totals['valid_games']:,} 局同时标记为有效**。另有 **{run_totals['invalid_records']:,} 条无效记录**，包括 {run_totals['incomplete_records']:,} 条未完成或异常记录，以及 {run_totals['completed_invalid_games']:,} 局虽完成但验证未通过的记录。原始失败记录全部保留；未完成记录不计成完整比赛，无效记录不计入有效局数。完成局包含换边、同图对照与候选消融，不是同等数量的独立随机地图。另有80个只到扩种判断点的前缀检查，未混入胜率；48场高手原局复现也单列研究证据。

## 本轮改进

1. 在v7基础上融合公开Master方案的提前出售、无货卖单清理与仓库溢出保护；第696步后让原末期规划接管，避免新增抢卖层继续改动收官决策。
2. 修复19株番茄方案的人工成本、施肥与分批返仓。已知开发图默认配置下有实益，但80个额外随机前缀均未触发，因此不能把它说成普遍收益来源。
3. 扩大对手池与可续跑联赛，逐局锁定源码哈希，检查双方隐性错误，并用独立地图确认收益。

研究了DSM与Vadim各24场公开回放。DSM重构程序虽对v7较强，另48局跨策略仅28胜20负，并暴露缺种和养护缺口，因此没有直接替换主策略。回放代理属于我们的研究重构，不是两位选手的私有程序。

## 提交兼容性

实际归档字节已通过两场官方文件加载比赛。候选首动作包含编译/解压为0.267与0.504秒；归档在只含标准库的隔离进程中连续重放1438动作，原键与排序键均完全一致，跨局重置通过，错误/退化计数全为0。

技术证据在 `submissions/candidate_v8/validation.json`；其 `strength_approval=false` 表示该技术工具不负责强度选择。最终本地选择结论单独记录在本目录 `release_manifest.json`。

对手存在同源代码，且真实领先者私有策略无法用本地代理完整代表。实际能否达到3000～3200，仍须等待线上多轮匹配后的评分。
'''
    (ROOT/'RELEASE_V8.md').write_text(doc,encoding='utf-8')
    development=ROOT/'DEVELOPMENT.md';text=development.read_text(encoding='utf-8')
    if '**当前版本为 release_v7。' in text:
        text=text.replace('**当前版本为 release_v7。以下为第一轮历史记录；最新策略、验收及提交方式见 RELEASE_V7.md，提交文件位于 submissions/release_v7/。**',
                          '**当前版本为 release_v8。以下为第一轮历史记录；最新独立验证及提交方式见 RELEASE_V8.md，提交文件位于 submissions/release_v8/。原 v7 保留。**',1)
        development.write_text(text,encoding='utf-8')
    assert sha(ROOT/'main.py')==SOURCE_HASH and sha(release/'submission.tar.gz')==ARCHIVE_HASH
    print(json.dumps({'promoted':'release_v8','source_sha256':SOURCE_HASH,'archive_sha256':ARCHIVE_HASH,
                      'confirmation':totals,'paired_metrics':comp['metrics'],'league_execution_summary':run_totals},indent=2))


if __name__=='__main__':main()
