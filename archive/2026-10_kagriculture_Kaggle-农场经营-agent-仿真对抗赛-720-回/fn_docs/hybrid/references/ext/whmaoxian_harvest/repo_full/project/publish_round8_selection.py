"""Promote only the locally selected, technically verified frozen archive.

No network requests or Kaggle uploads. Earlier releases are preserved.
"""
import json
import shutil
import tarfile
from pathlib import Path

from assess_round8 import CONFIG, ROOT, V7_HASH, confirmation, development
from finalize_round8 import count_execution_records, sha


def main():
    decision = confirmation(development())
    chosen = decision['selected']
    assert chosen is not None, 'No candidate passed the predeclared independent gate'
    c = CONFIG[chosen]
    stage = ROOT / c['stage']
    tech = json.loads((stage / 'validation.json').read_text(encoding='utf-8'))
    source_hash, archive_hash = c['sha256'], tech['archive_sha256']
    assert tech['technical_acceptance_passed'] and sha(stage / 'main.py') == source_hash
    assert sha(stage / 'submission.tar.gz') == archive_hash
    with tarfile.open(stage / 'submission.tar.gz', 'r:gz') as tf:
        assert tf.getnames() == ['main.py', 'NOTICE.txt', 'LICENSE.txt']
        for name in tf.getnames():
            assert tf.extractfile(name).read() == (stage / name).read_bytes()
    assert sha(ROOT / 'main.py') in {V7_HASH, source_hash}, 'Preserve independently changed root entry'
    wrapper_targets = ['build_release_v8.py', 'build_submission.py', 'validate_submission.py']
    prior_v7_wrapper = '9a670e8f20392d320c3e94d2ae39c883b7076ed5a61bf1e2f4cbd0473979b607'
    published_marker = ROOT / 'submissions/release_v8/wrapper_hashes.json'
    existing_wrapper_hashes = json.loads(published_marker.read_text()) if published_marker.exists() else {}
    for name in wrapper_targets:
        target = ROOT / name
        if target.exists():
            allowed = {existing_wrapper_hashes[name]} if name in existing_wrapper_hashes else ({prior_v7_wrapper} if name != 'build_release_v8.py' else set())
            assert sha(target) in allowed, f'Preserve independently changed wrapper: {name}'
    release = ROOT / 'submissions/release_v8'
    for name in ['main.py', 'submission.tar.gz', 'NOTICE.txt', 'LICENSE.txt']:
        if (release / name).exists():
            assert sha(release / name) == sha(stage / name), 'Never overwrite a different frozen release'
    release.mkdir(exist_ok=True)
    for name in ['main.py', 'submission.tar.gz', 'NOTICE.txt', 'LICENSE.txt']:
        shutil.copy2(stage / name, release / name)
    shutil.copy2(stage / 'validation.json', release / 'technical_validation.json')
    (release / 'selection.json').write_text(json.dumps(decision, indent=2), encoding='utf-8')
    runs = {p.name: count_execution_records(p) for p in (ROOT / 'results').glob('round8_*.jsonl')}
    total = {k: sum(x[k] for x in runs.values()) for k in next(iter(runs.values()))}
    manifest = {
        'version': 'v8', 'selected_candidate': chosen, 'candidate': c['source'],
        'source_sha256': source_hash, 'archive_sha256': archive_hash,
        'archive_bytes': (release / 'submission.tar.gz').stat().st_size,
        'entry': tech['entry_name'], 'technical_pass': True, 'local_strength_pass': True,
        'online_submitted': False, 'online_rating': None,
        'confirmation_worlds': 40, 'confirmation_games_per_policy': 480,
        'familywise_comparisons': decision['familywise_comparisons'],
        'confirmation_totals': decision['totals'],
        'league_execution_summary': total, 'league_executions': runs,
        'decision_evidence': 'submissions/release_v8/selection.json',
        'technical_evidence': c['stage'] + '/validation.json',
        'protocol': 'research/round8/PROTOCOL.md',
        'limitations': ['Shared source ancestry in the opponent pool.',
                       'Demonstration proxies are not private top-player programs.',
                       'Some seed funding and inventory projection edge cases remain.',
                       'Local results cannot establish a Kaggle rating.'],
    }
    (release / 'release_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    shutil.copy2(release / 'main.py', ROOT / 'main.py')
    args = ['--candidate', c['source'], '--stage', 'submissions/release_v8',
            '--expected-sha256', source_hash, '--entry', tech['entry_name'],
            '--profile', tech['profile'], '--label', tech['label']]
    if tech['profile'] == 'generic':
        args += ['--notice-file', 'submissions/release_v8/NOTICE.txt',
                 '--license-file', 'submissions/release_v8/LICENSE.txt']
    wrapper = ('"""Rebuild and technically validate the frozen v8 archive."""\n'
               'from pathlib import Path\nimport subprocess\nimport sys\n\n'
               'def main():\n    root=Path(__file__).resolve().parent\n'
               f'    args={args!r}\n'
               '    subprocess.run([sys.executable,str(root/"build_release_round8.py"),*args],cwd=root,check=True)\n\n'
               'if __name__=="__main__":main()\n')
    (ROOT / 'build_release_v8.py').write_text(wrapper, encoding='utf-8')
    for name in ['build_submission.py', 'validate_submission.py']:
        (ROOT / name).write_text('"""Frozen v8 build and technical validation."""\nfrom build_release_v8 import main\n\nif __name__=="__main__":main()\n', encoding='utf-8')
    published_marker.write_text(json.dumps({name: sha(ROOT / name) for name in wrapper_targets}, indent=2), encoding='utf-8')
    metrics = decision['comparisons'][chosen + '_vs_v7']['metrics']['points_change']
    ci = metrics['world_bootstrap_familywise_95']
    labels = {'primary': '市场融合候选', 'dsm': 'DSM示范重构与现金修复候选', 'v7': 'v7'}
    opponent_labels = {
        'experiments/round8_top2_dsm_strict.py': 'DSM公开回放重构代理',
        'external/orderbook.py': 'Orderbook',
        'external/round8/fieldcraft/main.py': 'Fieldcraft',
        'external/round8/master2965/main.py': 'Master2965',
        'submissions/release_v6/main.py': 'v6',
        'submissions/release_v7/main.py': 'v7',
    }
    rows = ['| 对手 | v7 胜/负/平 | 新版 胜/负/平 |', '|---|---:|---:|']
    for opp, v in decision['totals'][chosen]['opponents'].items():
        b = decision['totals']['v7']['opponents'][opp]
        rows.append(f"| {opponent_labels.get(opp, opp)} | {b['wins']}/{b['losses']}/{b['ties']} | {v['wins']}/{v['losses']}/{v['ties']} |")
    summaries = '\n'.join(f"- {labels[label]}：{v['wins']}胜、{v['losses']}负、{v['ties']}平；平均对战积分{v['points']:.3f}。" for label, v in decision['totals'].items())
    if chosen == 'dsm':
        changes = '采用24场DSM公开示范构建的状态约束生产代理，结合可见市场与库存决策。在现金不足时将原已计划、当回合物理操作后有库存的卖单前置，使原定雇工与购种能及时付款；未改变示范的物理工作路线。修复官方最终可调用入口并压缩部署代码。它是我们的示范重构程序，没有取得DSM的私有源码。'
    else:
        changes = '在v7基础上融合公开Master方案的提前出售、无货卖单清理与仓库保护；第696步后交还原收官规划。番茄19株分支修正人工、施肥和运输，但随机开发面板中未触发，不能称为普遍收益来源。'
    between = ''
    if 'dsm_vs_primary' in decision['comparisons']:
        m = decision['comparisons']['dsm_vs_primary']['metrics']['points_change']
        interval = m['world_bootstrap_familywise_95']
        between = f"\nDSM修复与市场融合候选的配对积分差为{m['mean']*100:+.2f}个百分点，校正区间{interval[0]*100:+.2f}～{interval[1]*100:+.2f}。" + ('区间跨0，二者相互优劣仍有不确定性。' if interval[0] <= 0 <= interval[1] else '') + '\n'
    doc = f'''# Kaggriculture v8 提交说明

本轮选择：**{labels[chosen]}**。完成本地独立对抗与归档验收；尚未上传Kaggle，线上分数未知。原v7保留。

## 提交文件

- 上传 `submissions/release_v8/submission.tar.gz`，{manifest['archive_bytes']:,}字节。
- 根`main.py`已同步；包内只有`main.py`、`NOTICE.txt`、`LICENSE.txt`，无需外部模型或联网。
- 源码SHA-256：`{source_hash}`。
- 归档SHA-256：`{archive_hash}`。

## 独立验证

先完成20开发世界筛选，再比较40个预先冻结、未参与调参的确认世界，6类对手，交换双方席位，每策略480局。按世界聚类重采样，换边和同图多对手不作为独立地图。

{summaries}

新版相对v7的平均积分提高 **{metrics['mean']*100:.2f}个百分点**；用于选择的区间为 **{ci[0]*100:.2f}～{ci[1]*100:.2f}个百分点**。本次共{decision['familywise_comparisons']}组预定比较，按协议使用Bonferroni校正；完整原始95%与校正区间均保留在`selection.json`。
{between}
{chr(10).join(rows)}

本轮联赛记录{total['recorded_executions']:,}次执行，其中 **{total['completed_games']:,}局完整比赛**、{total['valid_games']:,}局通过运行检查；{total['invalid_records']:,}条异常记录保留，不冒充完整比赛。其中旧DSM入口的240次立即报错不计入完整比赛。另80场短前缀检查、48场高手历史原局复现、定向诊断及技术重放单列，不扩大独立样本数。

## 改动与边界

{changes}

研究了DSM与Vadim各24场公开研究回放。新程序对公开重构代理的胜负不代表对作者真正私有程序的胜负。对手池也含共同代码祖先，线上环境的对手分布更广。

实际归档字节已通过官方文件加载、连续两局隔离重放、不同JSON键顺序及跨局状态检查；详见`technical_validation.json`。技术文件的`strength_approval=false`表示技术工具不负责选择，最终强度准入记录在`selection.json`。

仍存在种子资金紧张与库存投影边界，并未声称每个经济请求都会成功。3000～3200是目标，必须等待线上充分匹配后的真实评分验证。研究过程、被淘汰实验及来源见根`RESEARCH_ROUND8.md`、`SOURCES_REGISTRY.md`。
'''
    (ROOT / 'RELEASE_V8.md').write_text(doc, encoding='utf-8')
    dev_path = ROOT / 'DEVELOPMENT.md'
    current = dev_path.read_text(encoding='utf-8')
    current = current.replace('**当前版本为 release_v7。以下为第一轮历史记录；最新策略、验收及提交方式见 RELEASE_V7.md，提交文件位于 submissions/release_v7/。**',
                              '**以下为第一轮历史记录；上一版策略与验收见 RELEASE_V7.md，原文件保留于 submissions/release_v7/。**')
    banner = '**当前版本为 release_v8。最新验收与提交方式见 RELEASE_V8.md，原 v7 保留。**\n\n'
    if not current.startswith(banner):
        dev_path.write_text(banner + current, encoding='utf-8')
    assert sha(ROOT / 'main.py') == source_hash and sha(release / 'submission.tar.gz') == archive_hash
    print(json.dumps({'published_local_release': 'v8', 'selected': chosen,
                      'source_sha256': source_hash, 'archive_sha256': archive_hash,
                      'league': total}, indent=2))


if __name__ == '__main__':
    main()
