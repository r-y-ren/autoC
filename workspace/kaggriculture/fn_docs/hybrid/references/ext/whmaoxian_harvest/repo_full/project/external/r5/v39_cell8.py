import gzip, io, tarfile
from IPython.display import FileLink, display

ARCHIVE = WORKDIR / 'submission_competitive_v39.tar.gz'
EXPECTED_ARCHIVE_SHA256 = '3778c7dbbd8be710d55e6effcc3bb3ec17948e97856bda1f776e94a05b2e2d02'
with ARCHIVE.open('wb') as file:
    with gzip.GzipFile(filename='', mode='wb', fileobj=file, mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode='w', format=tarfile.GNU_FORMAT) as tar:
            info = tarfile.TarInfo('main.py')
            info.size, info.mode, info.mtime = len(source_bytes), 0o644, 0
            tar.addfile(info, io.BytesIO(source_bytes))
with tarfile.open(ARCHIVE) as tar:
    assert tar.getnames() == ['main.py']
    assert tar.extractfile('main.py').read() == source_bytes
assert hashlib.sha256(ARCHIVE.read_bytes()).hexdigest() == EXPECTED_ARCHIVE_SHA256
build_manifest = {
    'version': 'v39', 'classification': 'tested_submission_candidate',
    'original_independent_gate_passed': False, 'main_sha256': EXPECTED_MAIN_SHA256,
    'archive_sha256': EXPECTED_ARCHIVE_SHA256, 'source_integrity': 'PASS',
    'archive_integrity': 'PASS', 'optional_game_checks': 'NOT RUN',
    'live_rating_guarantee': None,
}
(WORKDIR / 'v39_manifest.json').write_text(json.dumps(build_manifest, indent=2))
print('PACKAGE READY:', ARCHIVE.name, '|', ARCHIVE.stat().st_size, 'bytes', flush=True)
print('SHA-256:', EXPECTED_ARCHIVE_SHA256, flush=True)
display(FileLink(ARCHIVE.name))
