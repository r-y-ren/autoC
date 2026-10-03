"""Build the standalone Round 11 sheep-route candidate from frozen V9."""
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "submissions/release_v9/main.py"
TAIL = ROOT / "experiments/round11_early_expansion_tail.py"
OUTPUT = ROOT / "experiments/round11_early_expansion.py"
EXPECTED_V9 = "6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3"


def main():
    original = PARENT.read_bytes()
    assert hashlib.sha256(original).hexdigest() == EXPECTED_V9
    candidate = original.rstrip(b"\r\n") + b"\n\n" + TAIL.read_bytes()
    OUTPUT.write_bytes(candidate)
    print(OUTPUT)
    print("sha256", hashlib.sha256(candidate).hexdigest())


if __name__ == "__main__":
    main()
