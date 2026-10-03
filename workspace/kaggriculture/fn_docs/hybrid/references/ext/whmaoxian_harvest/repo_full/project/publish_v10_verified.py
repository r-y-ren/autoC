"""Publish V10 locally only after frozen confirmation and packed execution pass.
Does not upload to Kaggle or modify the frozen V9 or root main.py.
"""
import hashlib, io, json, shutil, tarfile
from datetime import datetime, timezone
from pathlib import Path
import arena_round11 as arena

ROOT = Path(__file__).resolve().parent
RUN = 'v10-pressure-ledger-v2'
SHA = '3a4601081cc909ae7baf97ec5ddb0e1a8a5a1a27c9cd072cdeaaf7d34c803e0b'
V9_SHA = '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3'
ARCHIVE_SHA = 'a7a5ca566142cec64dec084f0bad3a0abce62f4e38e71c9f406c64db4f89ac87'
STAGE = ROOT / 'submissions/candidate_v10_ledger'
DEST = ROOT / 'submissions/release_v10'

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    protected = [ROOT/'main.py', ROOT/'submissions/release_v9/main.py']
    assert all(digest(p) == V9_SHA for p in protected), 'V9 changed'
    frozen = json.loads(arena.freeze_path(RUN).read_text(encoding='utf-8'))
    assert frozen['candidate']['sha256'] == SHA
    reports, ledgers, provenance = {}, {}, {}
    for split in ('development', 'confirmation'):
        manifest, rows, report = arena.get_existing(RUN, split)
        assert manifest['candidate']['sha256'] == SHA
        assert report['complete_and_valid'], split
        reports[split], ledgers[split] = report, rows
        assert manifest['opponents'] == frozen['opponents']
        for key in ('arena_sha256','game_runner_sha256','engine_version','episode_steps'):
            assert manifest[key] == frozen[key], key
        locations = arena.paths(RUN, split)
        provenance[split] = {k: {'path':str(p.relative_to(ROOT)), 'sha256':digest(p)}
                             for k,p in locations.items() if p.is_file()}
    development = arena.paths(RUN, 'development')
    assert digest(development['manifest']) == frozen['development_manifest_sha256']
    assert digest(development['ledger']) == frozen['development_ledger_sha256']
    gate = arena.confirmation_gate(reports['confirmation'])
    assert gate['passed'], gate
    validation = json.loads((STAGE/'validation.json').read_text(encoding='utf-8'))
    assert validation['technical_acceptance_passed']
    assert validation['source_sha256'] == SHA
    assert digest(STAGE/'main.py') == SHA
    assert digest(STAGE/'submission.tar.gz') == ARCHIVE_SHA
    with tarfile.open(STAGE/'submission.tar.gz', 'r:gz') as archive:
        assert archive.getnames() == ['main.py','NOTICE.txt','LICENSE.txt']
        for name in archive.getnames():
            assert archive.extractfile(name).read() == (STAGE/name).read_bytes()
    confirmation = reports['confirmation']
    core = confirmation['promotion_pool']['families_excluding_self']
    points = {who:sum(confirmation['families'][family][who]['wins']
                      for family in core) for who in ('candidate','baseline')}
    core_games = sum(confirmation['families'][family]['candidate']['games'] for family in core)
    pool = confirmation['promotion_pool']
    direct = confirmation['families']['self_v9']['candidate']
    ci = pool['point_gain_world_bootstrap_95']
    candidate_rows = [r for r in ledgers['confirmation'] if r['participant']=='candidate']
    timing = max(r.get('max_action_seconds',0) for r in candidate_rows)
    pairs = {(r['seed'],r['seat'],r['family'],r['participant']):r for r in ledgers['confirmation']}
    changed_shops = sum(r.get('shops') != pairs[(r['seed'],r['seat'],r['family'],'baseline')].get('shops')
                        for r in candidate_rows)
    evidence = {'version':'V10','created_utc':datetime.now(timezone.utc).isoformat(),
        'source_sha256':SHA,'archive_sha256':ARCHIVE_SHA,'entry':'v10_ledger_agent',
        'run_name':RUN,'environment':'kaggle-environments==1.32.7',
        'confirmation_gate':gate,'reports':reports,'provenance':provenance,
        'core_confirmation_games_per_version':core_games,'core_wins':points,
        'max_confirmation_action_seconds_observed':timing,
        'paired_final_shop_lists_changed':changed_shops,
        'reserve_results_present':arena.paths(RUN,'reserve')['ledger'].exists(),
        'technical_validation_sha256':digest(STAGE/'validation.json'),
        'online_submission':False,'online_rating':None,'v9_preserved':True,
        'root_main_remains_v9':True,
        'limitations':['Fixed local public opponent pool; not current private leaderboard agents.',
          'Paired confidence interval groups both seats by random world.',
          'Some public opponents share source lineage; families are not fully independent.',
          'Observed timings are not a universal guarantee on Kaggle hardware.',
          'Local gains cannot be converted into a promised 3000 online rating.']}
    lines = ['# Kaggriculture V10 提交说明','',
        '正式文件：`submissions/release_v10/submission.tar.gz`。未自动上传 Kaggle。',
        '根目录 main.py 与 release_v9 均保留原 V9；请勿误上传根目录 main.py。','',
        '## 独立确认','',
        '源码在测试前冻结；48 个未参与开发的随机世界、4 类对手、双席位。',
        '每个版本 384 局，总计 768 条有效对局记录；其中非自战主面板每版本 288 局。',
        f'非自战胜点提升：{100*pool["mean_point_gain"]:.2f} 个百分点。',
        f'按世界重采样的 95% 区间：{100*ci[0]:.2f}～{100*ci[1]:.2f} 个百分点。','']
    lines += ['| 对手 | V9 胜/负/平 | V10 胜/负/平 | 每版局数 |',
              '|---|---:|---:|---:|']
    labels = {'frontier':'Frontier 公开程序','master':'Master2965 公开程序',
              'dsm_proxy':'DSM 旧公开回放重构代理（不是私有程序）'}
    for family in core:
        stats = confirmation['families'][family]
        b, c = stats['baseline'], stats['candidate']
        lines.append(f'| {labels[family]} | {b["wins"]}/{b["losses"]}/{b["ties"]} | '
                     f'{c["wins"]}/{c["losses"]}/{c["ties"]} | {c["games"]} |')
    lines += ['', f'另列与 V9 直接对战：{direct["wins"]} 胜、{direct["losses"]} 负、{direct["ties"]} 平，'
              f'共 {direct["games"]} 局；不计入上述非自战提升。','',
        '## 提交版改动','',
        '保留 V9 的完整生产、资金、库存和收官保护；未把新前排回放直接塞进提交包。',
        '根据公开信息估计的对手库存压力与当前商店需求，有限度地扩大提前销售窗口。',
        '以最终发出的自身卖单修正供给观察账本，减少把自身追加交易误计为对手供给的情况。','',
        '## 技术验收','',
        '实际压缩包通过两场官方文件路径加载对局；两种 JSON 键顺序下各 1438 步连续动作复现均一致。',
        '隔离标准库进程、连续跨局重置、异常计数及每回合订单数量检查通过。',
        f'独立确认中观察到的候选单步最长时间：{timing:.6f} 秒；不是 Kaggle 硬件保证。','',
        '## 范围与限制','',
        '独立确认仅证明相对于这组固定本地公开对手的改进；不能据此推断击败当前榜首私有程序。',
        '开发与确认均按世界分组比较双席位；完整逐局账本和来源哈希保存在 evidence.json 指向的路径。',
        f'配对后最终商店列表不同的案例数：{changed_shops}/{len(candidate_rows)}。',
        '尚无 V10 线上分数，不能保证 3000 分。没有自动上传 Kaggle。','',
        f'源码 SHA-256：`{SHA}`',f'提交包 SHA-256：`{ARCHIVE_SHA}`','',
        '复验入口：`publish_v10_verified.py` 只在冻结确认与技术验收均通过后发布到新目录。']
    report_text = '\n'.join(lines) + '\n'
    payloads = {name:(STAGE/name).read_bytes() for name in
                ('main.py','NOTICE.txt','LICENSE.txt','submission.tar.gz')}
    if DEST.exists():
        for name, data in payloads.items():
            if (DEST/name).exists():
                assert (DEST/name).read_bytes() == data, 'Different release already exists'
    DEST.mkdir(parents=True, exist_ok=True)
    for name, data in payloads.items():
        (DEST/name).write_bytes(data)
    (DEST/'validation.json').write_bytes((STAGE/'validation.json').read_bytes())
    (DEST/'evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
    (DEST/'README.md').write_text(report_text,encoding='utf-8')
    (ROOT/'RELEASE_V10.md').write_text(report_text,encoding='utf-8')
    assert digest(DEST/'main.py') == SHA
    assert digest(DEST/'submission.tar.gz') == ARCHIVE_SHA
    assert all(digest(p) == V9_SHA for p in protected)
    print(json.dumps({'release':str(DEST),'archive':str(DEST/'submission.tar.gz'),
        'source_sha256':SHA,'archive_sha256':ARCHIVE_SHA,
        'confirmation_gate':gate,'nonself_gain':pool['mean_point_gain'],
        'nonself_interval':ci,'direct_v9':direct,'online_submission':False},ensure_ascii=False),flush=True)

if __name__ == '__main__':
    main()
