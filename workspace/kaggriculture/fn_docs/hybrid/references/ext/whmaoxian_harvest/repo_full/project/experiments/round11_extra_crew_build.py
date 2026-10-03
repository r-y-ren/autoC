"""Build isolated extra-crew candidate from byte-verified frozen V9."""
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'submissions/release_v9/main.py'
TAIL = ROOT / 'experiments/round11_extra_crew_tail.py'
OUTPUT = ROOT / 'experiments/round11_extra_crew.py'
EXPECTED = '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3'


def main():
    source = PARENT.read_bytes()
    assert hashlib.sha256(source).hexdigest() == EXPECTED
    result = source.rstrip(b'\r\n') + b'\n\n' + TAIL.read_bytes()
    OUTPUT.write_bytes(result)
    print(OUTPUT, hashlib.sha256(result).hexdigest())


if __name__ == '__main__':
    main()
