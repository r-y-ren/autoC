"""Attach complete continuation evidence; never change verified agent/archive bytes."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
C=Path(__file__).resolve().parent;D=C.parent;B=D/'phase_b';W=D.parent;R=W.parents[1]
release=R/'submissions/release_v10_r2'
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
e=read(release/'evidence.json');source_hash=e['source_sha256'];archive_hash=e['archive_sha256']
assert sha(release/'main.py')==source_hash and sha(release/'submission.tar.gz')==archive_hash
study=read(C/'study_decision.json');assert study['retained_sha256']==source_hash
limitations=read(B/'known_limitations.json')
fresh=[json.loads(line) for line in (C/'fresh_loss_results.jsonl').read_text(encoding='utf-8').splitlines()]
new=[r for r in fresh if r['candidate']==e['selection']['candidate']]
old={r['episode']:r for r in fresh if r['candidate']=='submissions/release_v10/main.py'}
assert len(new)==len(old)==3
assert all(r['money']==[r['recorded_rewards'][r['seat']],r['recorded_rewards'][1-r['seat']]] for r in old.values())
fresh_summary=[dict(episode=r['episode'],seed=r['seed'],seat=r['seat'],
                    old_v10_margin=old[r['episode']]['margin'],revision_margin=r['margin']) for r in new]
if 'counted_full_games_before_phase_c' not in e:
    e['counted_full_games_before_phase_c']=e['counted_full_games']
e['counted_full_games']=e['counted_full_games_before_phase_c']+study['additional_full_games']
e['additional_phase_c']=study
e['fixed_replay_diagnostics']=limitations
e['newest_three_loss_diagnostics']=fresh_summary
e['count_scope']='Completed experiment/control/diagnostic games; includes rejected candidates, prior Phase-A validation and Phase-C probes. Not final-candidate games or independent-world count. Failed loader attempts and prefix-only runs excluded.'
e['known_limitations_explicit']=['90 of 92 primary added wins come from Aurax opening recovery.',
 'Recent fixed-ladder traces: revision 11/15 wins versus old V10 13/15; fixed tapes are not responsive private opponents.',
 'Newest three old losses: two flip, one worsens; this is diagnostic, not online performance.',
 'Three final-validation cases retain one unplaced cow. No measured 2800 rating exists.']
(release/'evidence.json').write_text(json.dumps(e,indent=2),encoding='utf-8')
subprocess.run([sys.executable,str(B/'write_delivery_report.py')],check=True)
notes='''

## 追加研究与已知弱点（必须与高胜率一起阅读）

后续增加两组机制消融及三场新败局诊断：合计 **2,747 场完整有效对局**，包含 1,744 场货物入仓时机实验、976 场领先风险控制实验及 27 场新败局对照。它们没有提供足够一致的胜场增益，最终没有加入提交源码。全部失败与对照结果保留在 `continuation/phase_c/`。

**主要面板新增的 92 场胜利中，90 场来自 Aurax，另 2 场来自 Fieldcraft。** 这支持修复特定严重开局缺陷，不支持声称对所有策略都明显增强。MarketShock、ShopRouter、Structured 的胜场数没有下降，但平均金币差有所减少。

独立确认后检查的 15 条近期排行榜固定动作回放中，旧 V10 为 13 胜，新版为 11 胜；这项退步保留。固定回放不能随改变后的市场作出反应，既不能当作真实私有智能体，也不能把其胜率用于估计线上分数。

11 场历史真实败局已由旧 V10 完整复现；新版在固定动作对照中翻转 6 场。后来新抓取的三场败局中又翻转 2 场，但剩余一场的劣势扩大。合起来是 14 场败局诊断中的 8 场翻转，而不是 14 场真实线上重赛。

| 新增败局编号 | 旧 V10 金币差 | 新版金币差 |
|---|---:|---:|
'''
notes+='\n'.join(f"| {r['episode']} | {r['old_v10_margin']:+.0f} | {r['revision_margin']:+.0f} |" for r in fresh_summary)
notes+='\n\n最后，最终验证保留了 3 个未放置牛的库存案例（同一个世界、席位的不同对照）。所有有限批次均已完成，未自动提交 Kaggle。新版线上实力尚未测得，不能将本地 98.26% 的胜率换算为 2800 分。\n'
for path in (release/'README.md',R/'RELEASE_V10_R2.md'):
    text=path.read_text(encoding='utf-8')
    text=text.replace('累计纳入统计的开发与验证账本含','累计纳入统计的实验、对照与诊断账本含')
    path.write_text(text+notes,encoding='utf-8')
summary=read(release/'delivery_summary.json')
summary.update(additional_phase_c=study,newest_three_loss_diagnostics=fresh_summary,
               known_limitations=e['known_limitations_explicit'])
for path in (release/'delivery_summary.json',B/'delivery_summary.json'):
    path.write_text(json.dumps(summary,indent=2),encoding='utf-8')
for path in (C/'study_decision.json',B/'known_limitations.json'):
    shutil.copy2(path,release/path.name)
assert sha(release/'main.py')==source_hash and sha(release/'submission.tar.gz')==archive_hash
print(json.dumps(dict(source_sha256=source_hash,archive_sha256=archive_hash,
 total_counted_full_games=e['counted_full_games'],additional_full_games=study['additional_full_games'],
 archive_bytes=e['archive_bytes'],report=str(release/'README.md'),
 limitations_preserved=True,online_submission=False)),flush=True)
