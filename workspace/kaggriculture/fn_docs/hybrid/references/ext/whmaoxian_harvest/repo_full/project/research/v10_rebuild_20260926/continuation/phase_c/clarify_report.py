"""Clarify rating limitations without touching source or archive bytes."""
from pathlib import Path
import hashlib
C=Path(__file__).resolve().parent;R=C.parents[3]
release=R/'submissions/release_v10_r2'
archive=release/'submission.tar.gz'
before=hashlib.sha256(archive.read_bytes()).hexdigest()
text=(release/'README.md').read_text(encoding='utf-8')
old='状态：独立实力验收与实际提交包技术验收均已通过。**未自动上传 Kaggle，尚无新版线上评分。**'
new='状态：修订版已生成，通过固定本地测试门槛和提交包技术验收。**未自动上传 Kaggle，2800 分的目标尚未在线验证。主要提升集中在开局缺陷修复，部分近期回放诊断仍有退步。**'
assert old in text or new in text
text=text.replace(old,new)
text=text.replace('源码与压缩包都按哈希冻结，包内没有测试数据或额外对手程序。',
                  '源码与压缩包都按哈希冻结；本轮测试记录与新增外部对手程序没有打入提交包。')
for path in (release/'README.md',R/'RELEASE_V10_R2.md'):
    path.write_text(text,encoding='utf-8')
assert hashlib.sha256(archive.read_bytes()).hexdigest()==before
print('Report scope clarified; archive unchanged',flush=True)
