"""Archive round-8 contributions without copying the venv or changing originals."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default='round8_20260922_checkpoint')
    parser.add_argument('--include-live-confirmation', action='store_true')
    a = parser.parse_args()
    assert a.name.replace('_', '').replace('-', '').isalnum()
    files = set()
    for pattern in ['*.py', '*.md', '*.ps1', '*requirements*.txt']:
        files.update(ROOT.glob(pattern))
    for folder in ['experiments', 'agents', 'external', 'research/round8',
                   'submissions/release_v6', 'submissions/release_v7',
                   'submissions/candidate_v8', 'submissions/candidate_v8_dsm',
                   'submissions/release_v8']:
        files.update(p for p in (ROOT / folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    files.update(p for p in (ROOT / 'results').glob('round8_*') if p.is_file())
    excluded = []
    if not a.include_live_confirmation:
        for p in list(files):
            if p.parent == ROOT / 'results' and p.name.startswith('round8_dsm_contract_entry_confirmation'):
                excluded.append(str(p.relative_to(ROOT))); files.remove(p)
    target = ROOT / 'checkpoints' / (a.name + '.zip')
    target.parent.mkdir(exist_ok=True)
    assert not target.exists(), 'Do not overwrite an earlier checkpoint'
    manifest = {'created_utc': datetime.now(timezone.utc).isoformat(), 'root': str(ROOT),
                'excluded_active_files': sorted(excluded), 'files': {}}
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=1) as z:
        for p in sorted(files):
            data = p.read_bytes(); rel = p.relative_to(ROOT).as_posix()
            manifest['files'][rel] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
            z.writestr(rel, data)
        z.writestr('CHECKPOINT_MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2))
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(manifest['files']) + 1
    print(json.dumps({'archive': str(target), 'files': len(manifest['files']),
                      'bytes': target.stat().st_size,
                      'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
                      'excluded_active_files': excluded}, ensure_ascii=False))


if __name__ == '__main__':
    main()
