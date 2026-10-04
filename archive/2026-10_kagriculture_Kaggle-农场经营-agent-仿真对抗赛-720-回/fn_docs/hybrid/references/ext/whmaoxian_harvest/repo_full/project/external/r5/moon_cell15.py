assert len(demo) == 1 and demo[0]['tested_source_sha256'] == CANDIDATE_SHA
assert demo[0]['candidate_calls'] == demo[0]['opponent_calls'] == 719
assert demo[0]['runtime_errors'] == 0
assert all(report['calls'] == 719 and report['errors'] == 0 for report in smoke_final_order_reports)
assert Path('main.py').read_bytes() == candidate_bytes
package_files = {'main.py':candidate_bytes, 'LICENSE.txt':LICENSE_TEXT.encode('utf-8'),
                 'NOTICE.txt':NOTICE_TEXT.encode('utf-8')}
for name, data in package_files.items():
    Path(name).write_bytes(data)
buffer=io.BytesIO()
with gzip.GzipFile(filename='',mode='wb',fileobj=buffer,mtime=0) as gz:
    with tarfile.open(fileobj=gz,mode='w') as tf:
        for name,data in package_files.items():
            member=tarfile.TarInfo(name); member.size=len(data); member.mode=0o644
            member.uid=member.gid=member.mtime=0
            tf.addfile(member,io.BytesIO(data))
bundle_file=Path('submission.tar.gz'); bundle_file.write_bytes(buffer.getvalue())
with tarfile.open(bundle_file,'r:gz') as tf:
    assert tf.getnames() == list(package_files)
    for name,data in package_files.items():
        assert tf.extractfile(name).read() == data
print('Exact source SHA256:',CANDIDATE_SHA)
print('Deterministic bundle SHA256:',hashlib.sha256(bundle_file.read_bytes()).hexdigest())
