"""Publish only the frozen candidate after independent and technical acceptance."""
import json,hashlib,shutil,tarfile
from pathlib import Path
from assess_round9 import confirm,ROOT

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
 decision=confirm();assert decision['local_strength_pass'],'Independent gate failed; do not promote'
 selection=decision['selection'];source_hash=selection['sha256'];stage=ROOT/'submissions/candidate_v9'
 direct=[json.loads(line) for line in (ROOT/'results/round9_direct_v8.jsonl').read_text(encoding='utf-8').splitlines()]
 assert len(direct)==96 and all(r['valid'] and r['candidate_sha256']==source_hash for r in direct)
 assert sum(r['points'] for r in direct)>48,'Direct V8 check failed; keep candidate unpromoted'
 top2=[json.loads(line) for line in (ROOT/'results/round9_top2_locked_stress.jsonl').read_text(encoding='utf-8').splitlines()]
 assert len(top2)==36 and all(r['valid'] for r in top2), 'Replay stress execution checks incomplete'
 technical=json.loads((stage/'validation.json').read_text(encoding='utf-8'))
 assert technical['technical_acceptance_passed'] and technical['source_sha256']==source_hash
 assert sha(stage/'main.py')==source_hash and sha(stage/'submission.tar.gz')==technical['archive_sha256']
 with tarfile.open(stage/'submission.tar.gz') as tf:
  assert tf.getnames()==['main.py','NOTICE.txt','LICENSE.txt']
  for name in tf.getnames():assert tf.extractfile(name).read()==(stage/name).read_bytes()
 v8='9fa83701138e80e3e5f9a6479cc2fa1c7e8a8965c4bd85d4e45d05ec5d4ffd4e'
 assert sha(ROOT/'submissions/release_v8/main.py')==v8
 assert sha(ROOT/'main.py') in {v8,source_hash},'Preserve user changes to the root entry'
 release=ROOT/'submissions/release_v9';release.mkdir(exist_ok=True)
 for name in ['main.py','NOTICE.txt','LICENSE.txt','submission.tar.gz']:
  if (release/name).exists():assert sha(release/name)==sha(stage/name),'Never replace different frozen release bytes'
  shutil.copy2(stage/name,release/name)
 shutil.copy2(stage/'validation.json',release/'technical_validation.json')
 (release/'selection.json').write_text(json.dumps(decision,indent=2),encoding='utf-8')
 unique={}
 for p in (ROOT/'results').glob('round9_*.jsonl'):
  for line in p.read_text(encoding='utf-8').splitlines():
   row=json.loads(line)
   if 'id' in row:
    if row['id'] in unique:assert unique[row['id']].get('delta')==row.get('delta')
    unique[row['id']]=row
 manifest={'version':'v9','candidate':selection['candidate'],'source_sha256':source_hash,'archive_sha256':technical['archive_sha256'],
 'archive_bytes':(release/'submission.tar.gz').stat().st_size,'entry':technical['entry_name'],
 'technical_pass':True,'local_strength_pass':True,'online_submitted':False,'online_rating':None,
 'confirmation_worlds':48,'confirmation_games_per_policy':384,'baseline':decision['baseline'],'candidate_totals':decision['candidate'],
 'direct_vs_v8':{'games':96,'wins':sum(r['delta']>0 for r in direct),'losses':sum(r['delta']<0 for r in direct),'ties':sum(r['delta']==0 for r in direct)},
 'paired_point_gain':decision['comparison']['metrics']['points_change'],
 'paired_final_shop_lists_differ':decision['paired_final_shop_lists_differ'],
 'unique_league_games_recorded':len(unique),'unique_valid_league_games':sum(r['valid'] for r in unique.values()),
 'profile_calibration_games_excluded':40,'recorded_top2_stress_excluded_from_primary':True,
 'limitations':['Opponent pool shares public-policy ancestry.','Fixed-action replay stress is not the private adaptive top-player agent.',
 'Same seeds can yield different shops after policy-dependent farm changes.','Local results cannot establish a Kaggle rating.']}
 (release/'release_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
 wrapper=('"""Rebuild and validate the frozen v9 package; no Kaggle upload."""\n'
 'from pathlib import Path\nimport subprocess,sys\n\n'
 'def main():\n    root=Path(__file__).resolve().parent\n'
 f'    args={ ["--candidate",selection["candidate"],"--stage","submissions/candidate_v9","--expected-sha256",source_hash,"--entry",technical["entry_name"],"--profile","generic","--notice-file","research/round9/NOTICE_v9.txt","--label","candidate_v9","--resume"]!r}\n'
 '    subprocess.run([sys.executable,str(root/"build_release_round8.py"),*args],cwd=root,check=True)\n'
 '    subprocess.run([sys.executable,str(root/"publish_round9.py")],cwd=root,check=True)\n\n'
 'if __name__=="__main__":main()\n')
 if (ROOT/'build_release_v9.py').exists():assert (ROOT/'build_release_v9.py').read_text(encoding='utf-8')==wrapper
 previous_marker=release/'wrapper_hashes.json'
 previous=json.loads(previous_marker.read_text()) if previous_marker.exists() else json.loads((ROOT/'submissions/release_v8/wrapper_hashes.json').read_text())
 for name in ['build_submission.py','validate_submission.py']:assert sha(ROOT/name)==previous[name],'Preserve independent wrapper edits'
 (ROOT/'build_release_v9.py').write_text(wrapper,encoding='utf-8')
 for name in ['build_submission.py','validate_submission.py']:
  (ROOT/name).write_text('"""Frozen v9 build and technical validation."""\nfrom build_release_v9 import main\n\nif __name__=="__main__":main()\n',encoding='utf-8')
 previous_marker.write_text(json.dumps({n:sha(ROOT/n) for n in ['build_release_v9.py','build_submission.py','validate_submission.py']},indent=2),encoding='utf-8')
 shutil.copy2(release/'main.py',ROOT/'main.py')
 labels={'external/round9/frontier/main.py':'Frontier 当前公开快照','external/orderbook.py':'Orderbook',
 'external/round8/master2965/main.py':'Master2965','experiments/round8_top2_dsm_strict.py':'DSM旧公开回放重构代理（非私有程序）'}
 lines=['| 对手 | V8 胜场 | V9 胜场 | 局数 |','|---|---:|---:|---:|']
 for opp,stats in decision['comparison']['opponents'].items():lines.append(f"| {labels.get(opp,opp)} | {stats['base_wins']} | {stats['new_wins']} | {stats['paired_games']} |")
 b=decision['baseline'];c=decision['candidate'];m=decision['comparison']['metrics']['points_change'];ci=m['world_bootstrap_95']
 doc=f"""# Kaggriculture V9 提交说明

已完成本地独立确认与实际归档技术验收。未自动上传Kaggle，尚无V9线上分数，不能保证3000分。

## 提交文件

上传 `submissions/release_v9/submission.tar.gz`，{manifest['archive_bytes']:,}字节。包内只有main.py、NOTICE.txt、LICENSE.txt，无外部模型或联网依赖。根main.py与压缩包源码一致，旧V8完整保留。

源码SHA256：`{source_hash}`。
归档SHA256：`{manifest['archive_sha256']}`。

## 独立确认

开发结束后冻结唯一候选，再使用48个未参与调参的种子，4类对手、双席位，每个版本384局。

- V8：{b['wins']}胜、{b['losses']}负、{b['ties']}平，胜负积分{b['points']:.2%}。
- V9：{c['wins']}胜、{c['losses']}负、{c['ties']}平，胜负积分{c['points']:.2%}。
- 配对提升{m['mean']*100:.2f}个百分点；按世界聚类的95%自助区间为{ci[0]*100:.2f}～{ci[1]*100:.2f}个百分点。

{chr(10).join(lines)}

这组对手与上一轮480局面板不同，不能直接比较两个原始胜率。相同种子干预后商店序列可能变化，本轮{decision['paired_final_shop_lists_differ']}个配对的最终商店列表不同。完整逐局证据见results/round9_selected_confirmation.jsonl和round9_v8_confirmation.jsonl。

额外的V8直接对抗独立列出：{sum(r['delta']>0 for r in direct)}胜、{sum(r['delta']<0 for r in direct)}负、{sum(r['delta']==0 for r in direct)}平，共96局；没有并入主面板提升总胜率。

## 真正进入提交版的改动

1. 在最终可执行市场队列上处理卖单顺序，调整提前出售的衔接；停用更早、容易被后续层改变前提的克隆队列重排。
2. 只利用本日原有任务已经全部结束的雇工补做照料、收获和收肥；不增加雇工，不挤占后续必做工作，并保留仓容余量。
3. 保留V8的资金、库存、种植和收官保护，以及原19株番茄分支。

更激进的路线预测、单边收益换养、双方分差换养及劳动日程换养，都保留了源码和失败结果，没有因为思路新颖而强行合并。过程与局限详见RESEARCH_ROUND9.md。

## 技术验收与范围

实际压缩包经过官方文件路径加载的两场720状态对局；1438次连续动作在隔离标准库进程中复现，两种JSON键顺序均一致；重置和异常计数检查通过。技术验收并不等于达到目标排名。

固定DSM/Vadim回放的额外反事实压力测试另列，不计入上述384局，不声称测到其私有自适应程序的胜率。测试池仍有公共代码谱系相似性，最终强度应结合V9上线后的充分对局确认。

重建与复验：使用项目虚拟环境运行build_release_v9.py。这个入口不会向Kaggle提交。
"""
 (ROOT/'RELEASE_V9.md').write_text(doc,encoding='utf-8')
 print(json.dumps(manifest,indent=2))

if __name__=='__main__':main()
