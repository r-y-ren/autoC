"""Freeze the selected public baseline and verify its real submission path."""
import contextlib
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parent
EXPECTED = "10f58185b916392ca39697c83f67f455df81a74dfb6eb1aacd60fd81d50c9970"


def main():
    source = (ROOT / "external/one_more_wheat.py").read_bytes()
    assert hashlib.sha256(source).hexdigest() == EXPECTED
    release = ROOT / "submissions/release_v6"
    release.mkdir(exist_ok=True)
    entry = release / "main.py"
    entry.write_bytes(source)
    archive = release / "submission.tar.gz"
    with archive.open("wb") as raw, gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w") as tf:
            info = tarfile.TarInfo("main.py")
            info.size, info.mode, info.mtime = len(source), 0o644, 0
            tf.addfile(info, io.BytesIO(source))
            for name in ("NOTICE.txt", "LICENSE.txt"):
                payload = (ROOT / ("external/one_more_wheat_" + name)).read_bytes()
                (release / name).write_bytes(payload)
                member = tarfile.TarInfo(name)
                member.size, member.mode, member.mtime = len(payload), 0o644, 0
                tf.addfile(member, io.BytesIO(payload))
    stage = release / "validation"
    stage.mkdir(exist_ok=True)
    with tarfile.open(archive) as tf:
        assert tf.getnames() == ["main.py", "NOTICE.txt", "LICENSE.txt"]
        unpacked = tf.extractfile("main.py").read()
    assert unpacked == source
    actual = stage / "main.py"
    actual.write_bytes(unpacked)
    with contextlib.redirect_stdout(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    assert get_last_callable(source.decode(), path=str(actual)).__name__ == "agent"
    fixtures, expected, games = [], [], []
    # Two complete sequential episodes exercise persistent state and game reset.
    for seed, opponent in [(91001, str(actual)), (91002, str(ROOT / "external/rayk_c95.py"))]:
        env = make("kaggriculture", configuration={"seed": seed}, debug=True)
        env.run([str(actual), opponent])
        assert len(env.steps) == 720
        assert [s.status for s in env.steps[-1]] == ["DONE", "DONE"]
        logs = [v for row in env.logs for v in row if isinstance(v, dict)]
        assert not any(v.get("stderr", "").strip() for v in logs)
        for t in range(719):
            obs = dict(env.steps[t][0].observation)
            obs["step"] = t
            fixtures.append({"obs": obs, "cfg": dict(env.configuration)})
            action = env.steps[t + 1][0].action
            assert set(action) == {"farmer", "hands", "market"}
            assert len(action["market"]) <= 10
            expected.append(action)
        games.append({"seed": seed, "opponent": opponent,
                      "money": [s.reward for s in env.steps[-1]],
                      "max_action_seconds_both": max(v.get("duration", 0) for v in logs)})
        print(json.dumps(games[-1]), flush=True)
    worker = ("import json,runpy,sys\nf=runpy.run_path(sys.argv[1])['agent']\n"
              "for line in sys.stdin:\n r=json.loads(line); a=f(r['obs'],r['cfg'])\n"
              " errors={k:v for k,v in getattr(f,'telemetry',{}).items() "
              "if 'error' in k.lower() and isinstance(v,(int,float)) and v>0}\n"
              " print(json.dumps({'action':a,'errors':errors}))\n")
    parity = []
    for sorted_keys in (False, True):
        result = subprocess.run([sys.executable, "-I", "-S", "-c", worker, str(actual)],
                                input="\n".join(json.dumps(r, sort_keys=sorted_keys) for r in fixtures),
                                text=True, encoding="utf-8", capture_output=True, timeout=240, check=True)
        assert not result.stderr.strip(), result.stderr[:1000]
        records = [json.loads(line) for line in result.stdout.splitlines()]
        actions = [r["action"] for r in records]
        telemetry_errors = [(i, r["errors"]) for i, r in enumerate(records) if r["errors"]]
        assert not telemetry_errors, telemetry_errors[:10]
        differences = [i for i, (a, b) in enumerate(zip(actions, expected)) if a != b]
        assert len(actions) == len(expected) and not differences, differences[:10]
        parity.append({"sorted_observation_keys": sorted_keys, "matching_actions": len(actions),
                       "nonzero_exposed_error_counters": len(telemetry_errors)})
    report = {"source_sha256": EXPECTED, "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
              "archive_members": ["main.py", "NOTICE.txt", "LICENSE.txt"], "games": games, "isolated_checks": parity,
              "third_party_packages_disabled": True, "state_reset_between_episodes": True}
    (release / "validation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    manifest = {"release": "v6", "strategy": "Dmitrii Gluzdov One More Wheat, frozen public source, unmodified",
                "source_url": "https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-one-more-wheat",
                "license": "Apache-2.0; original attribution and license embedded in main.py",
                "environment": "kaggle-environments 1.32.7", "online_score": None,
                "source_sha256": EXPECTED, "archive_sha256": report["archive_sha256"],
                "source_bytes": len(source), "archive_bytes": archive.stat().st_size}
    (release / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("Archive and continuous isolated action parity passed.", flush=True)


if __name__ == "__main__":
    main()
