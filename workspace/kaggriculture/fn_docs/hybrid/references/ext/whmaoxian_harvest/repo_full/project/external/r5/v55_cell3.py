import ast, gzip, hashlib, io, tarfile
source_bytes = MAIN.read_bytes()
assert hashlib.sha256(source_bytes).hexdigest() == EXPECTED_MAIN_SHA256
assert [n.name for n in ast.parse(source_bytes).body if isinstance(n, ast.FunctionDef)][-1] == 'final_price_guard'
ARCHIVE = OUTPUT_ROOT / 'submission_competitive_v55.tar.gz'
buffer = io.BytesIO()
with tarfile.open(fileobj=buffer, mode='w') as tar:
    info = tarfile.TarInfo('main.py')
    info.size = len(source_bytes); info.mtime = 0; info.mode = 0o644
    tar.addfile(info, io.BytesIO(source_bytes))
with ARCHIVE.open('wb') as stream:
    with gzip.GzipFile(fileobj=stream, mode='wb', mtime=0, filename='') as zipper:
        zipper.write(buffer.getvalue())
with tarfile.open(ARCHIVE) as tar:
    assert tar.getnames() == ['main.py']
    assert tar.extractfile('main.py').read() == source_bytes
print('Ready:', ARCHIVE)
print('main.py SHA256:', EXPECTED_MAIN_SHA256)
print('No Kaggle competition submission was made.')
