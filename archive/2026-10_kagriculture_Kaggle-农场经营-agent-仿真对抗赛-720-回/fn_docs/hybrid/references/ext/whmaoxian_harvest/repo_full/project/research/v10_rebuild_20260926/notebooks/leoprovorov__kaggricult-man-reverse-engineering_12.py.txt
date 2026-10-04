# Builds MarketShock-M1-WR1K from a hash-checked Kaggle Input. Standard library only.
from pathlib import Path
import gzip, hashlib, importlib.util, io, os, sys, tarfile, zipfile

AGENT_NAME = "MarketShock-M1-WR1K"
DATASET_AGENT_NAME = 'marketshock_m1_wr1k_main.py'
EXPECTED_MAIN_SHA256 = '12ad317ecac6c07fb2c2e10bf4820ecd1fd4551a5a36aa0e34ab93b2c33c2693'
EXPECTED_ARCHIVE_SHA256 = '4d8cf20c2281dca5816eb3615a179a0087f33b10f7f460bbe258741521693461'
INPUT_ROOT = Path(os.environ.get('KAGGLE_INPUT_ROOT', '/kaggle/input'))
if os.environ.get('KAGGLE_WORKING_ROOT'):
    OUTPUT_ROOT = Path(os.environ['KAGGLE_WORKING_ROOT'])
elif os.name != 'nt' and Path('/kaggle/working').is_dir():
    OUTPUT_ROOT = Path('/kaggle/working')
else:
    OUTPUT_ROOT = Path.cwd()

matches = []
if INPUT_ROOT.is_dir():
    # Preferred input: the companion Kaggle Dataset file.
    for candidate in INPUT_ROOT.rglob(DATASET_AGENT_NAME):
        try:
            payload = candidate.read_bytes()
            if hashlib.sha256(payload).hexdigest() == EXPECTED_MAIN_SHA256:
                matches.append((candidate, payload))
        except OSError:
            pass

    # Also accept the prepared ZIP if Kaggle keeps it packed.
    for candidate in INPUT_ROOT.rglob('*.zip'):
        try:
            with zipfile.ZipFile(candidate) as packed:
                names = [name for name in packed.namelist() if Path(name).name == DATASET_AGENT_NAME]
                for name in names:
                    payload = packed.read(name)
                    if hashlib.sha256(payload).hexdigest() == EXPECTED_MAIN_SHA256:
                        matches.append((candidate, payload))
        except (OSError, KeyError, zipfile.BadZipFile):
            pass

    # Alternative input: Output of the self-contained Ice and Fire notebook.
    for candidate in INPUT_ROOT.rglob('submission.tar.gz'):
        try:
            with tarfile.open(candidate, 'r:gz') as archive:
                member = archive.extractfile('main.py')
                if member is None:
                    continue
                payload = member.read()
            if hashlib.sha256(payload).hexdigest() == EXPECTED_MAIN_SHA256:
                matches.append((candidate, payload))
        except (KeyError, OSError, tarfile.TarError):
            pass

if not matches:
    raise FileNotFoundError(
        'Required MarketShock-M1-WR1K input is missing. Attach the Dataset '
        '`marketshock-m1-wr1-agent` (recommended), or attach the Output of the '
        'self-contained Ice and Fire notebook. No hash-matching agent was found.'
    )

SOURCE_INPUT, main_bytes = matches[0]
compile(main_bytes, 'main.py', 'exec')
MAIN = OUTPUT_ROOT / 'main.py'
MAIN.write_bytes(main_bytes)

ARCHIVE = OUTPUT_ROOT / 'submission.tar.gz'
with ARCHIVE.open('wb') as raw:
    with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as zipped:
        with tarfile.open(fileobj=zipped, mode='w', format=tarfile.GNU_FORMAT) as archive:
            info = tarfile.TarInfo('main.py')
            info.size = len(main_bytes); info.mode = 0o644; info.mtime = 0
            info.uid = info.gid = 0; info.uname = info.gname = ''
            archive.addfile(info, io.BytesIO(main_bytes))

assert hashlib.sha256(ARCHIVE.read_bytes()).hexdigest() == EXPECTED_ARCHIVE_SHA256
with tarfile.open(ARCHIVE, 'r:gz') as archive:
    assert archive.getnames() == ['main.py']
    assert archive.extractfile('main.py').read() == main_bytes

sys.path.insert(0, str(OUTPUT_ROOT))
spec = importlib.util.spec_from_file_location('marketshock_m1_wr1k_submission_check', MAIN)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
assert callable(module.agent)

RECEIPT = OUTPUT_ROOT / 'marketshock_m1_wr1k_build_receipt.json'
RECEIPT.write_text(__import__('json').dumps({
    'agent': AGENT_NAME,
    'source_input': str(SOURCE_INPUT),
    'main_bytes': len(main_bytes),
    'main_sha256': EXPECTED_MAIN_SHA256,
    'archive_bytes': ARCHIVE.stat().st_size,
    'archive_sha256': EXPECTED_ARCHIVE_SHA256,
    'archive_members': ['main.py'],
    'runtime_parent': 'byte-exact Kaggriculture: A Smaller Market Shock',
}, indent=2), encoding='utf-8')

print('READY_TO_SUBMIT', AGENT_NAME)
print('Agent input:', SOURCE_INPUT)
print('Archive:', ARCHIVE)
print('Archive bytes:', ARCHIVE.stat().st_size)
print('Archive SHA-256:', EXPECTED_ARCHIVE_SHA256)
print('Root main.py:', MAIN)
print('Build receipt:', RECEIPT)
