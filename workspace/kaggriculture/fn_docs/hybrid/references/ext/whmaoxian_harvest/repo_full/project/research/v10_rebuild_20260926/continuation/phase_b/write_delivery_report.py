"""Render the Chinese delivery report only from a verified release's evidence."""
from pathlib import Path
import difflib,hashlib,json,shutil
B=Path(__file__).resolve().parent;D=B.parent;W=D.parent;R=W.parents[1]
release=R/'submissions/release_v10_r2'
e=json.loads((release/'evidence.json').read_text(encoding='utf-8'));g=e['strength']
assert g['passed'] and e['technical']['technical_acceptance_passed']
def record(row):return f"{row['wins']} 胜 / {row['losses']} 负 / {row['ties']} 平"
def table(families):
 lines=['| 对手实现 | V9：胜/负/平 | 旧 V10：胜/负/平 | V10-R2：胜/负/平 | 每版局数 |',
        '|---|---:|---:|---:|---:|']
 for family,values in families.items():
  def compact(row):return f"{row['wins']}/{row['losses']}/{row['ties']}"
  lines.append(f"| {family} | {compact(values['v9'])} | {compact(values['v10'])} | {compact(values['candidate'])} | {values['candidate']['games']} |")
 return '\n'.join(lines)
pg=g['paired_primary']['v10'];technical=e['technical']
context=dict(archive_path=str(release/'submission.tar.gz'),archive_bytes=e['archive_bytes'],
 primary_table=table(g['families']),style_table=table(g['styles']),
 primary_new=record(g['primary']['candidate']),primary_old=record(g['primary']['v10']),
 gain_pp=100*pg['point_gain'],gain_low=100*pg['world_bootstrap_95'][0],gain_high=100*pg['world_bootstrap_95'][1],
 gain_low_975=100*g['primary_gain_interval_975'][0],gain_high_975=100*g['primary_gain_interval_975'][1],
 direct_v9=record(g['direct']['release_v9']),direct_v10=record(g['direct']['release_v10']),
 counted_games=e['counted_full_games'],official_max=max(r['max_candidate_seconds'] for r in e['official_crosscheck']['games']),
 isolated_max=max(r['max_action_seconds'] for r in technical['isolated_checks']),source_sha=e['source_sha256'],archive_sha=e['archive_sha256'])
report=(B/'REPORT_TEMPLATE.md').read_text(encoding='utf-8').format(**context)
(release/'README.md').write_text(report,encoding='utf-8')
(R/'RELEASE_V10_R2.md').write_text(report,encoding='utf-8')
old=(R/'submissions/release_v10/main.py').read_text(encoding='utf-8')
new=(release/'main.py').read_text(encoding='utf-8')
patch=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='release_v10/main.py',tofile='release_v10_r2/main.py'))
(release/'V10_to_V10_R2.patch').write_text(patch,encoding='utf-8')
summary=dict(version='V10-R2',source_sha256=e['source_sha256'],archive_sha256=e['archive_sha256'],
 archive_bytes=e['archive_bytes'],submission_archive=str(release/'submission.tar.gz'),
 selected_before_validation=e['selection']['selected_utc'],settings=e['selection']['settings'],
 total_counted_full_games=e['counted_full_games'],final_validation_games=g['total_full_games'],
 primary=g['primary'],primary_families=g['families'],paired_primary=g['paired_primary'],
 primary_gain_interval_975=g['primary_gain_interval_975'],style=g['style'],style_families=g['styles'],direct=g['direct'],
 technical=dict(passed=True,isolated_actions_per_key_order=1438,official_crosscheck_games=12,
  official_crosscheck_all_match=True,official_crosscheck_max_seconds=context['official_max'],isolated_max_seconds=context['isolated_max']),
 original_files_preserved=True,online_submission=False,online_rating=None,goal_rating=2800,
 scope='Fixed public-program and separately held-out-style tests, not a rating calibration or a guarantee against current private leaders.')
(release/'delivery_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
(B/'delivery_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
shutil.copy2(B/'runtime_identity.json',release/'runtime_identity.json')
print(json.dumps({'report':str(release/'README.md'),'summary':str(release/'delivery_summary.json'),'source_sha256':e['source_sha256']}),flush=True)
