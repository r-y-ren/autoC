"""Build one standalone Round 11 fertilizer overlay from frozen V9."""
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'submissions/release_v9/main.py'
TAIL = ROOT / 'experiments/round11_fertilizer_overlay_tail.py'
OUTPUT = ROOT / 'experiments/round11_fertilizer_overlay.py'
EXPECTED = '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3'


def main():
    original = PARENT.read_bytes()
    assert hashlib.sha256(original).hexdigest() == EXPECTED
    result = original.rstrip(b'\r\n') + b'\n\n' + TAIL.read_bytes()
    OUTPUT.write_bytes(result)
    print(OUTPUT)
    print(hashlib.sha256(result).hexdigest())


if __name__ == '__main__':
    main()
